from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from libs.common.writers_room import RELATION_DIMENSIONS
from libs.domain.errors.writers_room__error import WritersRoomError


@dataclass
class StoryMemoryEntity:
    facts: dict[str, str] = field(default_factory=dict)
    knowledge: dict[str, dict[str, dict[str, str]]] = field(default_factory=dict)
    relationships: dict[str, dict[str, int]] = field(default_factory=dict)
    physical: dict[str, str] = field(default_factory=dict)
    threads: dict[str, str] = field(default_factory=dict)
    foreshadowing: dict[str, str] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    accepted_scenes: list[str] = field(default_factory=list)

    def character_view(self, character_id: str) -> dict[str, Any]:
        beliefs = self.knowledge.get(character_id, {})
        return {"knowledge": {key: entry for key, entry in beliefs.items() if entry.get("status") != "unknown"}, "physical": self.physical.get(character_id, ""), "relationships": {key: value for key, value in self.relationships.items() if key.startswith(character_id + "->")}, "recent_events": [e for e in self.events[-20:] if e.get("actor") == character_id and e.get("kind") != "fact"]}

    def project(self, scene_id: str, draft: dict[str, Any], participants: list[str]) -> tuple[StoryMemoryEntity, list[dict[str, Any]]]:
        state = deepcopy(self)
        findings: list[dict[str, Any]] = []
        ids = {e["id"] for e in state.events}
        locators: set[str] = set()
        for beat in draft["beats"]:
            screen = beat["action"] + "\n" + "\n".join(line["text"] for line in beat["lines"])
            for line in beat["lines"]:
                if line["id"] in locators or line["speaker"] not in participants:
                    findings.append(self._finding("identity", line["id"], line["text"], "对白 ID 重复或说话人不在场。"))
                locators.add(line["id"])
                for proposition in line["uses_knowledge"]:
                    status = state.knowledge.get(line["speaker"], {}).get(proposition, {}).get("status", "unknown")
                    if status == "unknown":
                        findings.append(self._finding("knowledge_consistency", line["id"], line["text"], f"人物尚未获得命题 {proposition}。"))
            if beat["id"] in locators:
                findings.append(self._finding("identity", beat["id"], beat["action"], "Beat ID 重复。"))
            locators.add(beat["id"])
            for raw in beat["events"]:
                event = dict(raw, scene_id=scene_id, beat_id=beat["id"], order=len(state.events))
                if event["id"] in ids or not event["id"].startswith(scene_id + "_"):
                    findings.append(self._finding("timeline", beat["id"], event["evidence_quote"], "事件 ID 重复或未带场景前缀。"))
                    continue
                if not event["evidence_quote"] or event["evidence_quote"] not in screen:
                    findings.append(self._finding("grounding", beat["id"], event["evidence_quote"], "状态变化没有当前画面/对白的原文证据。"))
                    continue
                if (event["kind"] in {"knowledge", "physical", "relationship"} or event["actor"]) and event["actor"] not in participants:
                    findings.append(self._finding("identity", beat["id"], event["evidence_quote"], "事件人物不在场。"))
                    continue
                kind, proposition = event["kind"], event["proposition_id"]
                if kind == "fact":
                    if not proposition or (proposition in state.facts and state.facts[proposition] != event["value"]):
                        findings.append(self._finding("plot_logic", beat["id"], event["evidence_quote"], "命题为空或与已有事实冲突；不能覆盖旧事实。"))
                        continue
                    state.facts[proposition] = event["value"]
                elif kind == "knowledge":
                    source = next((e for e in state.events if e["id"] == event["source_event_id"]), None)
                    if source is None or source.get("proposition_id") != proposition:
                        findings.append(self._finding("knowledge_consistency", beat["id"], event["evidence_quote"], "知情来源不存在、来自未来或命题不匹配。"))
                        continue
                    if event["epistemic_status"] == "known" and proposition not in state.facts:
                        findings.append(self._finding("knowledge_consistency", beat["id"], event["evidence_quote"], "未经建立的事实只能记录为相信/怀疑。"))
                        continue
                    if event["epistemic_status"] == "known" and state.facts.get(proposition) != event["value"]:
                        findings.append(self._finding("knowledge_consistency", beat["id"], event["evidence_quote"], "已知命题内容与事实不匹配，须记录为相信/误信。"))
                        continue
                    if event["epistemic_status"] == "known" and (source.get("value") != event["value"] or not (source.get("kind") == "fact" or (source.get("kind") == "knowledge" and source.get("epistemic_status") == "known"))):
                        findings.append(self._finding("knowledge_consistency", beat["id"], event["evidence_quote"], "不能把来源中的怀疑/误信转成已知事实，来源内容须一致。"))
                        continue
                    state.knowledge.setdefault(event["actor"], {})[proposition] = {"status": event["epistemic_status"], "text": event["value"], "source_event_id": source["id"]}
                elif kind == "relationship":
                    if event["target"] not in participants or event["target"] == event["actor"] or any(k not in RELATION_DIMENSIONS or abs(v) > 1 for k, v in event["relationship_changes"].items()):
                        findings.append(self._finding("relationship_consistency", beat["id"], event["evidence_quote"], "关系对象/维度错误或单事件变化超过一档。"))
                        continue
                    pair = event["actor"] + "->" + event["target"]
                    relation = state.relationships.setdefault(pair, {key: 0 for key in RELATION_DIMENSIONS})
                    for key, delta in event["relationship_changes"].items():
                        relation[key] = max(0, min(4, relation[key] + delta))
                elif kind == "physical":
                    state.physical[event["actor"]] = event["value"]
                elif kind == "thread":
                    state.threads[proposition] = event["value"]
                elif kind == "foreshadowing":
                    state.foreshadowing[proposition] = event["value"]
                state.events.append(event)
                ids.add(event["id"])
        if not findings:
            if scene_id in state.accepted_scenes:
                raise WritersRoomError("场景已接受，修改须新建工作分支。", "scene_already_accepted", 409)
            state.accepted_scenes.append(scene_id)
        return state, findings

    @staticmethod
    def _finding(dimension: str, locator: str, quote: str, reason: str) -> dict[str, Any]:
        return {"id": f"{dimension}:{locator}", "severity": "blocker", "dimension": dimension, "locator": locator, "quote": quote, "reason": reason, "evidence_refs": [], "repair_hint": "修改剧情或补齐有来源的信息/行为，再重新审查。"}
