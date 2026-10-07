from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libs.common.episode_workflow import fingerprint
from libs.common.story_run_io import INPUT_LABELS, IO_GROUPS
from libs.common.global_workflow import global_source_id


class StoryRunIoReader:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def _source(self, path: str, expected: str | None, episode: str, folder: str) -> dict[str, Any]:
        parts = path.split("/")
        drama = episode.split("/episodes/", 1)[0]
        allowed = path in {"AGENTS.md", "CONVENTIONS.md"} or path.startswith(
            (f"{drama}/", ".agents/skills/ai-videos-pipeline/", ".agents/references/project/", f"{folder}/"))
        if not allowed or any(part in {"", ".", ".."} or ":" in part or "\\" in part for part in parts):
            return {"status": "unavailable"}
        candidate = self.root.joinpath(*parts)
        for parent in (candidate, *candidate.parents):
            if parent == self.root:
                break
            if parent.is_symlink() or getattr(parent, "is_junction", lambda: False)():
                return {"status": "unavailable"}
        if self.root not in candidate.resolve().parents:
            return {"status": "unavailable"}
        try:
            digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        except OSError:
            return {"status": "missing"}
        return {"status": "same" if expected and digest == expected else "changed" if expected else "unverified",
                "sha256": digest}

    def read(self, run: dict[str, Any], audit_path: str) -> dict[str, Any]:
        items: list[dict[str, Any]] = []
        folder = audit_path.rsplit("/", 1)[0]

        def add(identity: str, group: str, name: str, value: Any, pointer: str,
                source: dict[str, Any] | None = None, note: str = "") -> None:
            item = {"id": identity, "group": group, "group_label": IO_GROUPS[group], "name": name,
                    "value": value, "target": f"{audit_path}#{pointer}", "snapshot_hash": fingerprint(value),
                    "note": note, "scope": "run", "kind": "output" if group == "outputs" else "process" if group == "process" else "input"}
            if source and isinstance(source.get("path"), str):
                item.update(source_path=source["path"], source_hash=source.get("sha256"), selection=source.get("selection"),
                            source_status=self._source(source["path"], source.get("sha256"), run["episode_path"], folder))
                identity = global_source_id(source["path"], episode=run["episode_path"])
                if identity:
                    item["global_source_id"] = identity
            items.append(item)

        source = run["input"]
        for key, value in source.items():
            if key not in {"sources", "rules"}:
                pointer_key = key.replace("~", "~0").replace("/", "~1")
                add(f"setting-{key}", "settings", INPUT_LABELS.get(key, key), value, f"/input/{pointer_key}")
        for group in ("sources", "rules"):
            for index, value in enumerate(source[group]):
                record = value if isinstance(value, dict) else {}
                name = record.get("name")
                if not isinstance(name, str) or not name:
                    name = str(record.get("path", f"{IO_GROUPS[group]} {index + 1}")).split("/")[-1]
                add(f"{group}-{index}", group, name, record.get("content", value), f"/input/{group}/{index}", record,
                    "只采用明确选定摘录；来源文件其他内容未作为输入。" if record.get("selection") == "explicit_excerpt" else "")
        for key, label in (("user_requests", "当次用户指令"), ("comparison_plan", "本轮对照设计与限制")):
            if key in run:
                add(f"run-{key}", "settings", label, run[key], f"/{key}",
                    note="按当次记录列出，包含组织与展示要求；不代表全部派发给故事作者。")
        participants = []
        for index, participant in enumerate(run["participants"]):
            if participant["scope"] != "story":
                continue
            add(f"task-{index}", "tasks", f"{participant['name']} · 实际指令", participant["prompt"],
                f"/participants/{index}/prompt", note="包含实际派发时的约束；与规则快照一起影响本次工作。")
            add(f"reply-{index}", "process", f"{participant['name']} · 完整回复", participant["output"], f"/participants/{index}/output")
            for key in ("messages", "follow_up_prompts"):
                if key in participant:
                    add(f"task-{index}-{key}", "tasks", f"{participant['name']} · 追加通信", participant[key],
                        f"/participants/{index}/{key}", note="实际留存的追加通信，按原记录完整展示。")
            participants.append({key: participant.get(key, "未记录") for key in
                                 ("id", "name", "role", "runtime_id", "model", "started_at", "finished_at", "settings", "sampling_parameters")})
        add("runtime", "runtime", "运行与模型设置", {"participants": participants, "runtime_settings": run.get("runtime_settings", "未记录"),
            "sampling_parameters": run.get("sampling_parameters", "未记录"), "shared_profile": run.get("shared_profile", "未记录")}, "/",
            note="模型未知或采样参数未记录时，不能据此确认两次运行的全部模型条件相同。共享profile是关联说明；实际采用版本以冻结输入为准。")
        for key, label in (("fictional_facts", "候选虚构设定"), ("causal_outline", "候选因果骨架")):
            if key in run["candidate"]:
                add(f"candidate-{key}", "outputs", label, run["candidate"][key], f"/candidate/{key}")
        add("candidate", "outputs", "完整候选数据", run["candidate"], "/candidate")
        for key, label in (("review", "审稿结论与检查"), ("decision_summary", "主编决策摘要"),
                           ("events", "完整事件时间线"), ("proposals", "逐项提议与取舍")):
            if key in run:
                add(key, "process", label, run[key], f"/{key}")
        documents = {
            "review_packet.json": ("tasks", "独立审稿实际输入包"),
            "spawns/writer/output.json": ("outputs", "作者初稿与因果骨架"),
            "spawns/writer/observations.md": ("process", "作者实际观察记录"),
            "spawns/editor/steering_requests.json": ("tasks", "主编收到的追加指令"),
            **{f"spawns/{role}/messages.json": ("tasks", f"{label}追加通信")
               for role, label in (("writer", "作者"), ("reviewer", "审稿人"), ("editor", "主编"))},
        }
        for relative, (group, label) in documents.items():
            artifact = next((entry for entry in run["artifacts"] if isinstance(entry, dict)
                             and entry.get("path") == f"{folder}/{relative}"), None)
            if not artifact:
                continue
            source_info = {"path": artifact["path"], "sha256": artifact.get("sha256"), "selection": "full_file"}
            state = self._source(source_info["path"], source_info["sha256"], run["episode_path"], folder)
            value: Any = {"status": state["status"], "note": "文件无法与历史登记指纹核对，未展示当前内容冒充当时输入。"}
            if state["status"] == "same":
                try:
                    data = (self.root / source_info["path"]).read_bytes()
                    if hashlib.sha256(data).hexdigest() == source_info["sha256"]:
                        text = data.decode("utf-8")
                        value = json.loads(text) if relative.endswith(".json") else text
                except (OSError, UnicodeError, ValueError):
                    value = {"status": "unavailable", "note": "历史登记文件无法解析。"}
            add(f"file-{relative.replace('/', '-').replace('.', '-')}", group, label, value, "/artifacts", source_info,
                note="关联本run实际登记的独立文件；只有与历史SHA256一致时才展示内容。审稿输入不自动代表作者输入。")
            items[-1]["target"] = source_info["path"]
        return {"items": items, "audit_path": audit_path, "coverage":
                "此清单按本run已保存的冻结输入、实际任务和回复生成。历史未保存的父代理上下文、系统指令、模型或采样条件无法补证；未把后续配置整理文件算作当次输入。"}
