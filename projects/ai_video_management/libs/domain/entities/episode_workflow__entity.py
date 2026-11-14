from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import re

from libs.common.episode_workflow import (EXTRAS_COUNT_RULE, GROUP_BOARD_USAGE, GROUP_CUT_RULE, GROUP_MAX_SECONDS, GROUP_OVERHEAD_USAGE, GROUP_COUNT_RULE, GROUP_DROPPED_NEGATIVE, FIRST_FRAME_USAGE, ANTI_TWIN_RULE, BASE_NEGATIVES, CAST_KEY_RE, CAST_USAGE, COMPILER_VERSION,
                                          LIP_SYNC_RULE, MODULES, NATURAL_MOTION_RULE, ONE_TAKE_RULE, OVERHEAD_USAGE,
                                          PREVIZ_USAGE, PROMPT_MAX_CHARS, PROP_KEY_RE, PROP_USAGE, SCENE_USAGE, SILENT_SHOT_RULE, VIDEO_SOUND_RULE, DIALOGUE_PRIORITY_RULE,
                                          VOICE_USAGE, fingerprint, scene_revision)
from libs.common.production_key import GROUP_ID_RE, GROUP_KEY_RE, SCENE_ID_RE, SHOT_ID_RE, first_shot_key, group_key, shot_key
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError
from libs.domain.value_objects.shot_materials__valueobject import PromptSettings, ShotMaterials

SHOT_FIELDS = {"id", "duration", "action", "camera", "dialogue", "cast", "blocking", "beats", "lighting"}
OPTIONAL_SHOT_FIELDS = {"props", "background", "allow_negatives", "extras", "point"}    # v8 (follow-up 231): story props in frame, by prop key;
# follow-up 261: a shot facing another way names its own background view (bg key), replacing the scene's for that shot;
# v12 (follow-up 282): allow_negatives lists drama-level negatives this one shot lifts (a spell shot that must glow)
# extras (chuanyue_yiri follow-up 036): how many uncarded passers-by the shot puts in frame; like a group card it drops
# 「多出来的人」 and adds the count rule. Absent → output unchanged, so no compiler version bump.


def sent_length(prompt: str, refs: list) -> int:
    """送给模型的长度：资料包给每个参考补上「图片N」等编号（每个 3–4 字），超长判断要算进去
    （chuanyue_yiri follow-up 068，审查 I8：编译时 5000 字以内、资料包里却 5025 字）。"""
    return len(prompt) + sum(len(f"图片{i + 1}") for i in range(len(refs or [])))


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
            if not isinstance(scene, dict) or set(scene) - {"source", "groups"} != {"id", "shots"} or not isinstance(scene.get("source", ""), str)                     or not isinstance(scene["id"], str) or not SCENE_ID_RE.fullmatch(scene["id"]) or scene["id"] in scenes:
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
            for group in scene.get("groups", []):
                if not isinstance(group, dict) or set(group) != {"id", "shots", "text", "refs"} \
                        or not isinstance(group["id"], str) or not GROUP_KEY_RE.fullmatch(group["id"]) \
                        or group["id"].split("_")[1] != scene["id"] or group["id"] in keys \
                        or not isinstance(group["text"], str) or group["text"].split("\n", 1)[0] != group["id"] \
                        or not isinstance(group["shots"], list) or not all(k in keys for k in group["shots"]):
                    raise EpisodeWorkflowError("无效的编译镜组")
                keys.add(group["id"])

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
                scene_id: str | None = None, boards: dict[str, str] | None = None) -> None:
        """Whole episode, or one scene (follow-up 259): a scene compiles once its own shots have every reference, and
        replaces only its own entry; other scenes keep their prompts. Each compiled scene records `source` (what it was
        compiled from), so tools tell a stale scene from a current one; the module stays stale until every scene is.
        `boards` maps each 镜组 key to its board image (follow-up 331); a group without one refuses to compile."""
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
            for group in scene.get("groups", []):
                gkey = group_key(self.episode_id, scene["id"], group["id"])
                if not (boards or {}).get(gkey):
                    missing.append(f"{gkey}：镜组板未出（scenes/{scene['id']}/groups/{group['id']}/board.png）")
        if missing:
            raise EpisodeWorkflowError("参考资料不全，不能编译：" + "；".join(missing[:8]) + ("……" if len(missing) > 8 else ""), 409)
        filming_source = self.documents["filming"]["source_revision"]
        compiled = {}
        for scene in targets:
            shots = []
            for shot in scene["shots"]:
                key = shot_key(self.episode_id, scene["id"], shot["id"]).value
                prompt, refs = self._prompt(key, scene, shot, materials[key], settings)
                if sent_length(prompt, refs) > PROMPT_MAX_CHARS:
                    raise EpisodeWorkflowError(f"{key} 的 prompt 送出时有 {sent_length(prompt, refs)} 字，超过 {PROMPT_MAX_CHARS}：拆镜或精简分镜", 409)
                shots.append({"id": key, "text": prompt, "refs": refs})
            entry = {"id": scene["id"], "source": scene_revision(scene, filming_source), "shots": shots}
            if scene.get("groups"):
                entry["groups"] = []
                for group in scene["groups"]:
                    gkey = group_key(self.episode_id, scene["id"], group["id"])
                    members = [next(s for s in scene["shots"] if s["id"] == sid) for sid in group["shots"]]
                    keys = [shot_key(self.episode_id, scene["id"], s["id"]).value for s in members]
                    prompt, refs = self._group_prompt(gkey, scene, members, [materials[k] for k in keys],
                                                      (boards or {})[gkey], settings)
                    if sent_length(prompt, refs) > PROMPT_MAX_CHARS:
                        raise EpisodeWorkflowError(f"{gkey} 的 prompt 送出时有 {sent_length(prompt, refs)} 字，超过 {PROMPT_MAX_CHARS}：少放几个镜头或精简分镜", 409)
                    entry["groups"].append({"id": gkey, "shots": keys, "text": prompt, "refs": refs})
            compiled[scene["id"]] = entry
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
        first = add(f"{key}_first_frame", "image", "首帧画面", found.first_frame) if found.first_frame else ""
        motion = add(f"{key}_previz" if video else f"{key}_overhead", found.motion_kind,
                     "走位预演（绿幕小人偶）" if video else "俯视站位图", found.motion)
        people = [(m, add(m.image_key, "image", m.name + "三视图", m.image)) for m in found.cast]
        props = [(p, add(p.image_key, "image", "道具 " + p.name, p.image)) for p in found.props]
        place = add(found.scene_key, "image", "场景 " + scene["location"], found.scene_image) if found.scene_image else ""
        # v13: only people who speak in this shot carry their voice; a silent shot sends no voice at all
        voices = {m.key: add(m.voice_key, "audio", m.name + "的声音", m.voice) for m in found.cast if m.voice and m.speaks}
        marker = "人偶" if video else "圆点"
        usage = FIRST_FRAME_USAGE.format(tag=first) if first else ""
        usage += (PREVIZ_USAGE if video else OVERHEAD_USAGE).format(tag=motion)
        usage += CAST_USAGE.format(keys="、".join(f"`{tag}`" for _, tag in people)) if people else ""
        usage += PROP_USAGE.format(keys="、".join(f"`{tag}`" for _, tag in props)) if props else ""
        usage += SCENE_USAGE.format(scene=place, motion=motion) if place else ""
        usage += VOICE_USAGE.format(keys="、".join(f"`{tag}`" for tag in voices.values())) if voices else ""
        lines = [line.strip() for line in shot["dialogue"].splitlines() if line.strip()]
        sound = "声音：" + VIDEO_SOUND_RULE + (DIALOGUE_PRIORITY_RULE if lines else SILENT_SHOT_RULE)
        people_lines = [f"  {m.name}" + (f" ×{m.count}" if m.count > 1 else "") + f"（三视图`{tag}`"
                        + (f"；同一张三视图画 {m.count} 个人，各在自己的位置" if m.count > 1 else "")
                        + (f"；声音`{voices[m.key]}`" if m.key in voices else "")
                        + f"；`{motion}`里的{m.color}色{marker}）：{m.look}" for m, tag in people]
        prompt = [key, sound, f"时长：{shot['duration']}秒", f"比例：{settings.ratio}",
                  "参考：" + "、".join(f"`{r['key']}=>@`" for r in refs),
                  f"参考用法：{usage}"]
        extras_n = int(shot.get("extras", 0))
        extras_line = [f"  另有 {extras_n} 个没有三视图的当地人，样子、位置和动作按「画面」写的来"] if extras_n else []
        prompt += ["人物：", *people_lines, *extras_line] if people_lines or extras_line else ["人物：画面里没有人物"]
        prompt += ["道具：", *(f"  {p.name}（道具图`{tag}`）：{p.look}" for p, tag in props)] if props else []
        prompt += [f"场景：{scene['location']} · {scene['time']}" + (f"（`{place}`）" if place else "")
                   + (f"：{found.scene_text}" if found.scene_text else ""),
                   f"画面：{shot['action']}"]
        prompt += [f"走位：{shot['blocking']}"] if shot["blocking"].strip() else []
        prompt += [f"动作：{shot['beats']}", f"镜头：{shot['camera']}", f"光线：{shot['lighting']}"]
        prompt += ["台词：", *(f"  {line}" for line in lines), f"口型：{LIP_SYNC_RULE}"] if lines else ["台词：无"]
        prompt += [f"风格：{settings.style}"] if settings.style else []
        groups = "、".join(f"`{tag}`" for m, tag in people if m.key.startswith("m") or m.count > 1)
        extras = int(shot.get("extras", 0))
        prompt += ["负面词：" + EpisodeWorkflowEntity._negatives(key, shot.get("allow_negatives", []), settings, bool(groups or extras))]
        group_rule = GROUP_COUNT_RULE.format(keys=groups) if groups else ""
        group_rule += EXTRAS_COUNT_RULE.format(n=extras) if extras else ""
        prompt += [f"要求：{ONE_TAKE_RULE}{ANTI_TWIN_RULE}{group_rule}{NATURAL_MOTION_RULE if people or extras else ''}", sound]
        return "\n".join(prompt), refs

    @staticmethod
    def _negatives(key: str, allow: list[str], settings: PromptSettings, crowd: bool) -> str:
        base = BASE_NEGATIVES.replace(GROUP_DROPPED_NEGATIVE, "") if crowd else BASE_NEGATIVES
        drama = settings.negatives
        if allow:
            terms = [x.strip() for x in re.split("[，,]", drama) if x.strip()]
            unknown = [x for x in allow if x not in terms]
            if unknown:
                raise EpisodeWorkflowError(f"{key} 要放开的负面词不在剧负面词里：{'、'.join(unknown)}", 409)
            drama = "，".join(x for x in terms if x not in allow)
        return "，".join(x for x in (base, drama) if x)

    @staticmethod
    def _group_prompt(key: str, scene: dict[str, Any], shots: list[dict[str, Any]], found: list[ShotMaterials],
                      board: str, settings: PromptSettings) -> tuple[str, list[dict[str, str]]]:
        """One 镜组 (follow-up 331): the shots' references merged — board first, each shot's overhead in order, then
        every distinct person, prop, background and voice — and one 镜头 N section per shot. Cuts fall between shots."""
        if any(m.motion_kind == "video" for m in found):
            raise EpisodeWorkflowError(f"{key}：镜组里有镜头用走位预演视频，镜组暂只支持俯视站位图", 409)
        refs: list[dict[str, str]] = []

        def add(ref_key: str, kind: str, role: str, path: str) -> str:
            if all(r["key"] != ref_key for r in refs):
                refs.append({"key": ref_key, "kind": kind, "role": role, "path": path})
            return ref_key

        n = len(shots)
        prefix = key.rsplit("_", 1)[0]
        board_tag = add(f"{key}_board", "image", "镜组板", board)
        motions = [add(f"{prefix}_{s['id']}_overhead", "image", f"镜头 {i} 俯视站位图", m.motion)
                   for i, (s, m) in enumerate(zip(shots, found), 1)]
        people: dict[str, tuple[Any, str]] = {}
        props: dict[str, tuple[Any, str]] = {}
        places: dict[str, tuple[str, str]] = {}
        for m in found:
            for c in m.cast:
                if c.key not in people:
                    people[c.key] = (c, add(c.image_key, "image", c.name + "三视图", c.image))
            for p in m.props:
                if p.key not in props:
                    props[p.key] = (p, add(p.image_key, "image", "道具 " + p.name, p.image))
        for m in found:
            if m.scene_image and m.scene_key not in places:
                places[m.scene_key] = (add(m.scene_key, "image", "场景 " + scene["location"], m.scene_image), m.scene_text)
        speaking = {c.key for m in found for c in m.cast if c.speaks}      # v13: voices only for who speaks in some member shot
        voices = {c.key: add(c.voice_key, "audio", c.name + "的声音", c.voice) for c, _ in people.values()
                  if c.voice and c.key in speaking}
        usage = GROUP_BOARD_USAGE.format(tag=board_tag, n=n)
        usage += GROUP_OVERHEAD_USAGE.format(tags="、".join(f"`{t}`" for t in motions), n=n)
        usage += CAST_USAGE.format(keys="、".join(f"`{t}`" for _, t in people.values())) if people else ""
        usage += PROP_USAGE.format(keys="、".join(f"`{t}`" for _, t in props.values())) if props else ""
        usage += "".join(SCENE_USAGE.format(scene=t, motion="各镜头的俯视站位示意图") for t, _ in places.values())
        usage += VOICE_USAGE.format(keys="、".join(f"`{t}`" for t in voices.values())) if voices else ""
        total = sum(s["duration"] for s in shots)
        spoken = any(line.strip() for s in shots for line in s["dialogue"].splitlines())
        sound = "声音：" + VIDEO_SOUND_RULE.replace("本镜", "各镜头") + (DIALOGUE_PRIORITY_RULE if spoken else SILENT_SHOT_RULE.replace("本镜", "本镜组"))
        people_lines = [f"  {c.name}" + (f" ×{c.count}" if c.count > 1 else "") + f"（三视图`{tag}`"
                        + (f"；声音`{voices[c.key]}`" if c.key in voices else "")
                        + f"；各镜头俯视图里的{c.color}色圆点）：{c.look}" for c, tag in people.values()]
        prompt = [key, sound, f"时长：{total}秒", f"比例：{settings.ratio}",
                  "参考：" + "、".join(f"`{r['key']}=>@`" for r in refs), f"参考用法：{usage}"]
        prompt += ["人物：", *people_lines] if people_lines else ["人物：画面里没有人物"]
        prompt += ["道具：", *(f"  {p.name}（道具图`{t}`）：{p.look}" for p, t in props.values())] if props else []
        prompt += [f"场景：{scene['location']} · {scene['time']}（`{t}`）" + (f"：{text}" if text else "")
                   for t, text in places.values()] or [f"场景：{scene['location']} · {scene['time']}"]
        prompt += [f"镜组：共 {n} 个镜头，总长 {total} 秒，按顺序切换："]
        start = 0
        for i, (shot, motion) in enumerate(zip(shots, motions), 1):
            end = start + shot["duration"]
            prompt += [f"镜头 {i}（第 {start}–{end} 秒，{shot['duration']} 秒；镜组板第 {i} 格；俯视图`{motion}`）：",
                       f"  画面：{shot['action']}"]
            prompt += [f"  走位：{shot['blocking']}"] if shot["blocking"].strip() else []
            prompt += [f"  动作（秒数从本镜头开始算）：{shot['beats']}", f"  镜头：{shot['camera']}", f"  光线：{shot['lighting']}"]
            lines = [line.strip() for line in shot["dialogue"].splitlines() if line.strip()]
            prompt += ["  台词：" + " / ".join(lines) if lines else "  台词：无"]
            start = end
        prompt += [f"口型：{LIP_SYNC_RULE}"] if spoken else []
        prompt += [f"风格：{settings.style}"] if settings.style else []
        crowd = "、".join(f"`{t}`" for c, t in people.values() if c.key.startswith("m") or c.count > 1)
        allow = list(dict.fromkeys(x for s in shots for x in s.get("allow_negatives", [])))
        prompt += ["负面词：" + EpisodeWorkflowEntity._negatives(key, allow, settings, bool(crowd))]
        group_rule = GROUP_COUNT_RULE.format(keys=crowd) if crowd else ""
        prompt += [f"要求：{GROUP_CUT_RULE.format(n=n)}{ANTI_TWIN_RULE}{group_rule}{NATURAL_MOTION_RULE if people else ''}", sound]
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
            if not isinstance(scene, dict) or set(scene) - {"groups"} != {"id", "background", "location", "time", "purpose", "shots"}:
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
                if "background" in shot and not (isinstance(shot["background"], str)
                                                 and re.fullmatch(r"bg[1-9]\d*(?:-[1-9]\d*)?", shot["background"])):
                    raise EpisodeWorkflowError("镜头的环境引用使用bg编号，例如bg2或bg2-2；不另选视角就不写")
                # point (chuanyue_yiri follow-up 058): one sentence of what the viewer must get from this shot. Review-only:
                # never compiled into the prompt; take review writes what it saw first, then compares with this.
                if "point" in shot and (not isinstance(shot["point"], str) or not shot["point"].strip()):
                    raise EpisodeWorkflowError("看点写一句话：这一镜要观众看懂或感到什么")
                allow = shot.get("allow_negatives", [])
                if not isinstance(allow, list) or not allow and "allow_negatives" in shot                         or not all(isinstance(x, str) and x.strip() and not re.search("[，,]", x) for x in allow) or len(set(allow)) != len(allow):
                    raise EpisodeWorkflowError('本镜放开的负面词写剧负面词里的词语列表，例如["夸张金光"]，不重复；不放开就不写')
                if "extras" in shot and not (isinstance(shot["extras"], int) and not isinstance(shot["extras"], bool) and shot["extras"] > 0):
                    raise EpisodeWorkflowError("路人数写正整数，例如 2；画里没有路人就不写")
                if cast and not shot["blocking"].strip():
                    raise EpisodeWorkflowError("有出场人物的镜头要写走位")
            if "groups" in scene:
                EpisodeWorkflowEntity._validate_groups(scene)

    @staticmethod
    def _validate_groups(scene: dict[str, Any]) -> None:
        """镜组 (follow-up 331): `[{"id": "g2", "shots": ["st4", "st5"]}]` — two or more consecutive shots of this scene,
        no shot in two groups, total within GROUP_MAX_SECONDS. Shots not listed are generated one by one as before."""
        groups = scene["groups"]
        if not isinstance(groups, list) or not groups:
            raise EpisodeWorkflowError('镜组写成列表，例如[{"id": "g2", "shots": ["st4", "st5"]}]；没有镜组就不写')
        order = [shot["id"] for shot in scene["shots"]]
        ids: set[str] = set()
        used: set[str] = set()
        for group in groups:
            if not isinstance(group, dict) or set(group) != {"id", "shots"} or not isinstance(group["id"], str) \
                    or not GROUP_ID_RE.fullmatch(group["id"]) or group["id"] in ids:
                raise EpisodeWorkflowError("镜组编号须在本场唯一，例如g2")
            ids.add(group["id"])
            members = group["shots"]
            if not isinstance(members, list) or len(members) < 2 or not all(isinstance(m, str) and m in order for m in members):
                raise EpisodeWorkflowError(f"镜组 {group['id']} 要列出本场两个以上的镜头")
            first = order.index(members[0])
            if members != order[first:first + len(members)]:
                raise EpisodeWorkflowError(f"镜组 {group['id']} 的镜头须按分镜顺序连续")
            if used & set(members):
                raise EpisodeWorkflowError(f"镜组 {group['id']} 的镜头已在别的镜组里")
            used |= set(members)
            total = sum(next(s for s in scene["shots"] if s["id"] == m)["duration"] for m in members)
            if total > GROUP_MAX_SECONDS:
                raise EpisodeWorkflowError(f"镜组 {group['id']} 共 {total} 秒，超过一次生成上限 {GROUP_MAX_SECONDS} 秒")
