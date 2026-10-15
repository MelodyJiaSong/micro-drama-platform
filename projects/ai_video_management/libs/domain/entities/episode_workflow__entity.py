from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import re

from libs.common.episode_workflow import (ANIMAL_COUNT_RULE, ANTI_TWIN_RULE, BASE_NEGATIVES, CAST_KEY_RE, CAST_USAGE, COMPILER_VERSION,
                                          LIP_SYNC_RULE, MODULES, NATURAL_MOTION_RULE, ONE_TAKE_RULE, OVERHEAD_USAGE,
                                          PREVIZ_USAGE, PROMPT_MAX_CHARS, PROP_KEY_RE, PROP_USAGE, SCENE_USAGE, SILENT_SHOT_RULE, VIDEO_SOUND_RULE,
                                          VOICE_USAGE, fingerprint, scene_revision)
from libs.common.production_key import SCENE_ID_RE, SHOT_ID_RE, first_shot_key, shot_key
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError
from libs.domain.value_objects.shot_materials__valueobject import PromptSettings, ShotMaterials

SHOT_FIELDS = {"id", "duration", "action", "camera", "dialogue", "cast", "blocking", "beats", "lighting"}
OPTIONAL_SHOT_FIELDS = {"props"}    # v8 (follow-up 231): story props in frame, by prop key


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
            if not isinstance(scene, dict) or set(scene) - {"source"} != {"id", "shots"} or not isinstance(scene.get("source", ""), str)                     or not isinstance(scene["id"], str) or not SCENE_ID_RE.fullmatch(scene["id"]) or scene["id"] in scenes:
                raise EpisodeWorkflowError("无效或重复的编译场次编号")
            scenes.add(scene["id"])
            if not isinstance(scene["shots"], list) or not scene["shots"]:
                raise EpisodeWorkflowError("编译场次须包含镜头")
            for shot in scene["shots"]:
                # v5 adds the ordered reference list the prompt's @图片N / @视频N / @音频N tags point at; v4 files have none.
                if not isinstance(shot, dict) or set(shot) - {"refs"} != {"id", "text"} \
                        or not isinstance(shot["id"], str) or not isinstance(shot["text"], str) \
                        or not all(isinstance(r, dict) and set(r) in ({"key", "kind", "role", "path"}, {"tag", "kind", "role", "path"})
                                   and all(isinstance(v, str) for v in r.values()) for r in shot.get("refs", [])):
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

    def compile(self, materials: dict[str, ShotMaterials] | None = None, settings: PromptSettings | None = None,
                scene_id: str | None = None) -> None:
        """Whole episode, or one scene (follow-up 259): a scene compiles once its own shots have every reference, and
        replaces only its own entry; other scenes keep their prompts. Each compiled scene records `source` (what it was
        compiled from), so tools tell a stale scene from a current one; the module stays stale until every scene is."""
        if self.status("filming") != "approved":
            raise EpisodeWorkflowError("请先确定影视改编版本", 409)
        scenes = self.documents["filming"]["content"]["scenes"]
        self.validate_content("filming", {"scenes": scenes})
        current = self.documents["prompts"]["content"]
        if scene_id is not None:
            if scene_id not in {scene["id"] for scene in scenes}:
                raise EpisodeWorkflowError(f"分镜里没有场次 {scene_id}", 409)
            if current.get("scenes") and current.get("compiler_version") != COMPILER_VERSION:
                raise EpisodeWorkflowError("已有的 Prompt 是旧版编译器的结果，请整集编译", 409)
        targets = [scene for scene in scenes if scene_id in (None, scene["id"])]
        materials = materials or {}
        settings = settings or PromptSettings()
        missing = []
        for scene in targets:
            for shot in scene["shots"]:
                key = shot_key(self.episode_id, scene["id"], shot["id"]).value
                found = materials.get(key)
                problems = ["缺参考资料"] if found is None else list(found.errors)
                missing += [f"{key}：{p}" for p in problems]
        if missing:
            raise EpisodeWorkflowError("参考资料不全，不能编译：" + "；".join(missing[:8]) + ("……" if len(missing) > 8 else ""), 409)
        filming_source = self.documents["filming"]["source_revision"]
        compiled = {}
        for scene in targets:
            shots = []
            for shot in scene["shots"]:
                key = shot_key(self.episode_id, scene["id"], shot["id"]).value
                prompt, refs = self._prompt(key, scene, shot, materials[key], settings)
                if len(prompt) > PROMPT_MAX_CHARS:
                    raise EpisodeWorkflowError(f"{key} 的 prompt 有 {len(prompt)} 字，超过 {PROMPT_MAX_CHARS}：拆镜或精简分镜", 409)
                shots.append({"id": key, "text": prompt, "refs": refs})
            compiled[scene["id"]] = {"id": scene["id"], "source": scene_revision(scene, filming_source), "shots": shots}
        previous_approval = self.documents["prompts"]["approved_revision"]
        if scene_id is None:
            self.documents["prompts"] = {"content": {"compiler_version": COMPILER_VERSION, "scenes": list(compiled.values())},
                                         "source_revision": self.revision("filming"), "approved_revision": None}
        else:
            kept = {scene["id"]: scene for scene in current.get("scenes", [])}
            kept.update(compiled)
            order = [scene["id"] for scene in scenes if scene["id"] in kept]
            ordered = [kept[i] for i in order] + [scene for i, scene in kept.items() if i not in order]
            self.documents["prompts"] = {"content": {"compiler_version": COMPILER_VERSION, "scenes": ordered},
                                         "source_revision": self.documents["prompts"]["source_revision"], "approved_revision": None}
        if previous_approval == self.revision("prompts"):
            self.documents["prompts"]["approved_revision"] = previous_approval

    @staticmethod
    def _prompt(key: str, scene: dict[str, Any], shot: dict[str, Any], found: ShotMaterials,
                settings: PromptSettings) -> tuple[str, list[dict[str, str]]]:
        """One labelled field per line (follow-up 226). The 参考 line lists every referenced file as `key_id=>@`
        (motion reference, every person's three-view sheet, every prop's anchor image, the background, every person's
        voice; follow-up 228/229/231);
        the body names references by key id. `@` is a placeholder the shot's 资料包 fills with the upload number."""
        refs: list[dict[str, str]] = []

        def add(ref_key: str, kind: str, role: str, path: str) -> str:
            refs.append({"key": ref_key, "kind": kind, "role": role, "path": path})
            return ref_key

        video = found.motion_kind == "video"
        motion = add(f"{key}_previz" if video else f"{key}_overhead", found.motion_kind,
                     "走位预演（绿幕小人偶）" if video else "俯视站位图", found.motion)
        people = [(m, add(m.image_key, "image", m.name + "三视图", m.image)) for m in found.cast]
        props = [(p, add(p.image_key, "image", "道具 " + p.name, p.image)) for p in found.props]
        place = add(found.scene_key, "image", "场景 " + scene["location"], found.scene_image) if found.scene_image else ""
        voices = {m.key: add(m.voice_key, "audio", m.name + "的声音", m.voice) for m in found.cast if m.voice}
        marker = "人偶" if video else "圆点"
        usage = (PREVIZ_USAGE if video else OVERHEAD_USAGE).format(tag=motion)
        usage += CAST_USAGE.format(keys="、".join(f"`{tag}`" for _, tag in people)) if people else ""
        usage += PROP_USAGE.format(keys="、".join(f"`{tag}`" for _, tag in props)) if props else ""
        usage += SCENE_USAGE.format(scene=place, motion=motion) if place else ""
        usage += VOICE_USAGE.format(keys="、".join(f"`{tag}`" for tag in voices.values())) if voices else ""
        lines = [line.strip() for line in shot["dialogue"].splitlines() if line.strip()]
        sound = "声音：" + VIDEO_SOUND_RULE + ("" if lines else SILENT_SHOT_RULE)
        people_lines = [f"  {m.name}（三视图`{tag}`" + (f"；声音`{voices[m.key]}`" if m.key in voices else "")
                        + f"；`{motion}`里的{m.color}色{marker}）：{m.look}" for m, tag in people]
        prompt = [key, sound, f"时长：{shot['duration']}秒", f"比例：{settings.ratio}",
                  "参考：" + "、".join(f"`{r['key']}=>@`" for r in refs),
                  f"参考用法：{usage}"]
        prompt += ["人物：", *people_lines] if people_lines else ["人物：画面里没有人物"]
        prompt += ["道具：", *(f"  {p.name}（道具图`{tag}`）：{p.look}" for p, tag in props)] if props else []
        prompt += [f"本场：{scene['purpose']}",
                   f"场景：{scene['location']} · {scene['time']}" + (f"（`{place}`）" if place else "")
                   + (f"：{found.scene_text}" if found.scene_text else ""),
                   f"画面：{shot['action']}"]
        prompt += [f"走位：{shot['blocking']}"] if shot["blocking"].strip() else []
        prompt += [f"动作：{shot['beats']}", f"镜头：{shot['camera']}", f"光线：{shot['lighting']}"]
        prompt += ["台词：", *(f"  {line}" for line in lines), f"口型：{LIP_SYNC_RULE}"] if lines else ["台词：无"]
        prompt += [f"风格：{settings.style}"] if settings.style else []
        prompt += ["负面词：" + "，".join(x for x in (BASE_NEGATIVES, settings.negatives) if x)]
        animals = "、".join(f"`{tag}`" for m, tag in people if m.key.startswith("m"))
        animal_rule = ANIMAL_COUNT_RULE.format(keys=animals) if animals else ""
        prompt += [f"要求：{ONE_TAKE_RULE}{ANTI_TWIN_RULE}{animal_rule}{NATURAL_MOTION_RULE if people else ''}", sound]
        return "\n".join(prompt), refs

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
                if not isinstance(shot, dict) or not SHOT_FIELDS <= set(shot) <= SHOT_FIELDS | OPTIONAL_SHOT_FIELDS:
                    raise EpisodeWorkflowError("每镜仅包含编号、时长、动作、摄影、对白、出场人物、走位、动作分拍和光线")
                if not isinstance(shot["id"], str) or not SHOT_ID_RE.fullmatch(shot["id"]) or shot["id"] in shot_ids:
                    raise EpisodeWorkflowError("镜头编号须在本场唯一，例如st1；重排不改号")
                shot_ids.add(shot["id"])
                if type(shot["duration"]) is not int or shot["duration"] < 1:
                    raise EpisodeWorkflowError("镜头时长须为正整数秒")
                for field in ("action", "camera", "dialogue", "blocking", "beats", "lighting"):
                    if not isinstance(shot[field], str) or (field in ("action", "camera", "beats", "lighting") and not shot[field].strip()):
                        raise EpisodeWorkflowError("请填写动作、摄影、动作分拍和光线；无对白可留空")
                cast = shot["cast"]
                if not isinstance(cast, list) or not all(isinstance(k, str) and re.fullmatch(CAST_KEY_RE, k) for k in cast) \
                        or len(set(cast)) != len(cast):
                    raise EpisodeWorkflowError('出场人物写资产键列表，例如["c1-1", "c14"]，不重复')
                props = shot.get("props", [])
                if not isinstance(props, list) or not all(isinstance(k, str) and re.fullmatch(PROP_KEY_RE, k) for k in props)                         or len(set(props)) != len(props):
                    raise EpisodeWorkflowError('道具写资产键列表，例如["p475"]，不重复')
                if cast and not shot["blocking"].strip():
                    raise EpisodeWorkflowError("有出场人物的镜头要写走位")
