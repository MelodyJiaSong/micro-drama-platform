from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import re

from libs.common.episode_workflow import COMPILER_VERSION, MODULES, SILENT_SHOT_RULE, VIDEO_SOUND_RULE, fingerprint
from libs.common.production_key import SCENE_ID_RE, SHOT_ID_RE, first_shot_key, shot_key
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError


@dataclass
class EpisodeWorkflowEntity:
    documents: dict[str, dict[str, Any]]
    episode_id: str = "ep01"

    def __post_init__(self) -> None:
        self.validate_content("story", self.documents["story"]["content"])
        self.validate_content("filming", self.documents["filming"]["content"])
        content = self.documents["prompts"]["content"]
        if set(content) - {"compiler_version", "scenes"} or not isinstance(content.get("scenes"), list):
            raise EpisodeWorkflowError("无效的编译场次列表")
        keys: set[str] = set()
        scenes: set[str] = set()
        for scene in content["scenes"]:
            if not isinstance(scene, dict) or set(scene) != {"id", "shots"} or not isinstance(scene["id"], str) or not SCENE_ID_RE.fullmatch(scene["id"]) or scene["id"] in scenes:
                raise EpisodeWorkflowError("无效或重复的编译场次编号")
            scenes.add(scene["id"])
            if not isinstance(scene["shots"], list) or not scene["shots"]:
                raise EpisodeWorkflowError("编译场次须包含镜头")
            for shot in scene["shots"]:
                if not isinstance(shot, dict) or set(shot) != {"id", "text"} or not all(isinstance(v, str) for v in shot.values()):
                    raise EpisodeWorkflowError("无效的编译镜头")
                key = first_shot_key(shot["id"])
                if key is None or key.value != shot["id"] or shot["id"] in keys or key.value != shot_key(self.episode_id, scene["id"], f"st{key.shot}").value:
                    raise EpisodeWorkflowError("编译镜头key与所属集或场次不一致")
                if not shot["text"].splitlines() or shot["text"].splitlines()[0] != key.value:
                    raise EpisodeWorkflowError("Prompt首行必须是完整镜头key")
                keys.add(key.value)

    def revision(self, module: str) -> str:
        doc = self.documents[module]
        return fingerprint({"content": doc["content"], "source_revision": doc["source_revision"]})

    def upstream(self, module: str) -> str | None:
        index = MODULES.index(module)
        return MODULES[index - 1] if index else None

    def status(self, module: str) -> str:
        doc = self.documents[module]
        content = doc["content"]
        populated = bool(content.get("text", "").strip()) if module == "story" else bool(content["scenes"])
        if module == "prompts" and populated and content.get("compiler_version") != COMPILER_VERSION:
            return "stale"
        upstream = self.upstream(module)
        if upstream and populated and doc["source_revision"] != self.revision(upstream):
            return "stale"
        if upstream and self.status(upstream) != "approved":
            return "blocked"
        if not populated:
            return "empty"
        return "approved" if doc["approved_revision"] == self.revision(module) else "draft"

    def check_edit(self, module: str, expected: str, source: str | None) -> None:
        if module not in MODULES:
            raise EpisodeWorkflowError("未知模块")
        if fingerprint(self.documents[module]) != expected:
            raise EpisodeWorkflowError("内容已被其他会话修改，请刷新后重试", 409)
        upstream = self.upstream(module)
        if upstream and (self.status(upstream) != "approved" or source != self.revision(upstream)):
            raise EpisodeWorkflowError("上游版本尚未确定或已改变，请刷新后重试", 409)

    def save(self, module: str, content: dict[str, Any]) -> None:
        if module == "prompts":
            raise EpisodeWorkflowError("Prompt 只能从已确定的分镜编译")
        self.validate_content(module, content)
        upstream = self.upstream(module)
        self.documents[module]["content"] = content
        self.documents[module]["source_revision"] = self.revision(upstream) if upstream else None
        if self.documents[module]["approved_revision"] != self.revision(module):
            self.documents[module]["approved_revision"] = None

    def approve(self, module: str) -> None:
        if self.status(module) not in {"draft", "approved"}:
            raise EpisodeWorkflowError("请先保存完整内容，并更新到当前上游版本")
        self.documents[module]["approved_revision"] = self.revision(module)

    def compile(self) -> None:
        if self.status("filming") != "approved":
            raise EpisodeWorkflowError("请先确定影视改编版本", 409)
        scenes = self.documents["filming"]["content"]["scenes"]
        self.validate_content("filming", {"scenes": scenes})
        compiled = []
        for scene in scenes:
            shots = []
            for shot in scene["shots"]:
                key = shot_key(self.episode_id, scene["id"], shot["id"]).value
                sound = VIDEO_SOUND_RULE + ("" if shot["dialogue"].strip() else SILENT_SHOT_RULE)
                prompt = "\n".join((key, sound, f"时长：{shot['duration']}秒。",
                                    f"地点：{scene['location']}；时间：{scene['time']}。",
                                    f"环境资产：{scene['background'] or '未绑定'}。",
                                    f"画面与表演：{shot['action']}", f"摄影：{shot['camera']}",
                                    f"对白：{shot['dialogue'] or '无'}", "连续镜头，不要切镜。不要字幕或水印。", sound))
                shots.append({"id": key, "text": prompt})
            compiled.append({"id": scene["id"], "shots": shots})
        previous_approval = self.documents["prompts"]["approved_revision"]
        self.documents["prompts"] = {"content": {"compiler_version": COMPILER_VERSION, "scenes": compiled},
                                     "source_revision": self.revision("filming"), "approved_revision": None}
        if previous_approval == self.revision("prompts"):
            self.documents["prompts"]["approved_revision"] = previous_approval

    @staticmethod
    def validate_content(module: str, content: dict[str, Any]) -> None:
        if module == "story":
            if set(content) != {"brief", "text"} or not all(isinstance(v, str) for v in content.values()):
                raise EpisodeWorkflowError("故事仅包含故事方向和正文")
            return
        if set(content) != {"scenes"} or not isinstance(content["scenes"], list):
            raise EpisodeWorkflowError("分镜必须包含场次列表")
        scene_ids: set[str] = set()
        for scene in content["scenes"]:
            if not isinstance(scene, dict) or set(scene) != {"id", "background", "location", "time", "purpose", "shots"}:
                raise EpisodeWorkflowError("每场包含编号、环境引用、地点、时间、目标变化和镜头列表")
            if not isinstance(scene["id"], str) or not SCENE_ID_RE.fullmatch(scene["id"]) or scene["id"] in scene_ids:
                raise EpisodeWorkflowError("场次编号须为唯一的s1、s2等稳定编号")
            scene_ids.add(scene["id"])
            for field in ("background", "location", "time", "purpose"):
                if not isinstance(scene[field], str) or (field != "background" and not scene[field].strip()):
                    raise EpisodeWorkflowError("请填写地点、时间和本场目标变化；未选环境可留空")
            if scene["background"] and not re.fullmatch(r"bg[1-9]\d*(?:-[1-9]\d*)?", scene["background"]):
                raise EpisodeWorkflowError("环境引用使用bg编号，例如bg2或bg2-2")
            if not isinstance(scene["shots"], list) or not scene["shots"]:
                raise EpisodeWorkflowError("每场至少包含一个镜头")
            shot_ids: set[str] = set()
            for shot in scene["shots"]:
                if not isinstance(shot, dict) or set(shot) != {"id", "duration", "action", "camera", "dialogue"}:
                    raise EpisodeWorkflowError("每镜仅包含编号、时长、动作、摄影和对白")
                if not isinstance(shot["id"], str) or not SHOT_ID_RE.fullmatch(shot["id"]) or shot["id"] in shot_ids:
                    raise EpisodeWorkflowError("镜头编号须在本场唯一，例如st1；重排不改号")
                shot_ids.add(shot["id"])
                if type(shot["duration"]) is not int or shot["duration"] < 1:
                    raise EpisodeWorkflowError("镜头时长须为正整数秒")
                for field in ("action", "camera", "dialogue"):
                    if not isinstance(shot[field], str) or (field != "dialogue" and not shot[field].strip()):
                        raise EpisodeWorkflowError("请填写动作和摄影；无对白可留空")
