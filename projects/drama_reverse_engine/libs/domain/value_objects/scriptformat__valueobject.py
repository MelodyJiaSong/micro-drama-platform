from __future__ import annotations

import re
from dataclasses import dataclass

_NIGHT_TOKENS = ("深夜", "夜色", "夜晚", "夜", "月光", "月色")
_SCENE_LINE_RE = re.compile(r"^\d+-\d+\s+[日夜]\s+[内外]\s+")
_DIALOGUE_LINE_RE = re.compile(r"^(?!△)([^：（【\s]{1,12})(（[^）]*）)?\s*：")
_EXTERIOR_TOKENS = ("外景", "殿外", "门外", "户外", "街", "巷", "郊", "野外", "空中", "山", "林间", "湖", "庭院", "院中", "城头")
_INTERIOR_TOKENS = ("内景", "室内", "内堂", "殿", "厅", "堂", "房", "屋", "阁", "牢")


@dataclass(frozen=True)
class SceneBlock:
    scene_index: int
    location: str
    time_of_day: str  # 日 | 夜
    interior: str  # 内 | 外
    shot_indexes: tuple[int, ...]


def location_of(scene_desc: str) -> str:
    head = re.split(r"[，,。.；;]", scene_desc)[0].strip()
    for suffix in ("内景", "外景"):
        head = head.replace(suffix, "")
    return head or "未知场景"


def group_scenes(shots: list[dict], analyses: dict[int, dict]) -> list[SceneBlock]:
    """样例剧本按「场」组织：same-location consecutive shots collapse into one scene."""
    scenes: list[SceneBlock] = []
    for shot in shots:
        analysis = analyses[shot["index"]]
        location = location_of(analysis["scene_desc"])
        if scenes and scenes[-1].location == location:
            prev = scenes[-1]
            scenes[-1] = SceneBlock(prev.scene_index, prev.location, prev.time_of_day, prev.interior,
                                    prev.shot_indexes + (shot["index"],))
            continue
        text = analysis["scene_desc"] + analysis.get("lighting", "")
        time_of_day = "夜" if any(t in text for t in _NIGHT_TOKENS) else "日"
        if any(t in text for t in _EXTERIOR_TOKENS):
            interior = "外"
        elif any(t in text for t in _INTERIOR_TOKENS):
            interior = "内"
        else:
            interior = "内"
        scenes.append(SceneBlock(len(scenes) + 1, location, time_of_day, interior, (shot["index"],)))
    return scenes


def classify_script_line(line: str) -> str:
    """按行类型分类剧本行 (follow-up 008/009) — webapp ScriptView 多色渲染与 docx 导出
    着色共用的分类：ep/outline/scene/cast/action/insert/line(对白)/os(内心独白·旁白)/
    plain/blank."""
    if not line.strip():
        return "blank"
    if _SCENE_LINE_RE.match(line):
        return "scene"
    if re.match(r"^第\d+集：", line) or line == "正文：":
        return "ep"
    if line.startswith("分集大纲："):
        return "outline"
    if line.startswith("人物："):
        return "cast"
    if line.startswith("△"):
        return "action"
    if line.startswith("【"):
        return "insert"
    m = _DIALOGUE_LINE_RE.match(line)
    if m:
        paren = m.group(2) or ""
        if "内心独白" in paren or "旁白" in paren or m.group(1) == "旁白":
            return "os"
        return "line"
    return "plain"


def _scene_atmosphere(analysis: dict) -> str:
    """场次首行环境氛围 △ 行 (follow-up 008, sample_juben.docx 密度): scene_desc +
    lighting merged into one descriptive line."""
    parts = [analysis["scene_desc"].rstrip("。")]
    lighting = str(analysis.get("lighting", "")).strip()
    if lighting and lighting not in parts[0]:
        parts.append(lighting.rstrip("。"))
    return "，".join(parts) + "。"


def _shot_action_line(analysis: dict) -> str:
    """每镜 △ 行融合 blocking + action + performance (follow-up 008)."""
    action = str(analysis["action"]).rstrip("。")
    blocking = str(analysis.get("blocking", "")).strip().rstrip("。")
    performance = str(analysis.get("performance", "")).strip().rstrip("。")
    segments = [action]
    if blocking and blocking not in action:
        segments.insert(0, blocking)
    if performance and performance not in action:
        segments.append(performance)
    return "，".join(segments) + "。"


def render_episode_script(episode_index: int, narrative: str, shots: list[dict],
                          analyses: dict[int, dict], lines_by_shot: dict[int, list[dict]]) -> str:
    """标准影视剧本体 (follow-up 006/008, format per sample_juben.docx): 第N集：→
    分集大纲：→ 正文：→ per-scene heading `{集}-{场} 日/夜 内/外 {地点}` + 人物：
    list + 氛围 △ 行 + 每镜 △ 行(blocking+action+performance) + `角色名（括注）：台词`
    verbatim dialogue — 每镜首句对白带 mood 表演括注."""
    out = [f"第{episode_index}集：", "", f"分集大纲：{narrative}", "", "正文：", ""]
    for scene in group_scenes(shots, analyses):
        names: list[str] = []
        for si in scene.shot_indexes:
            for name in analyses[si]["characters"]:
                if name not in names:
                    names.append(name)
        out.append(f"{episode_index}-{scene.scene_index} {scene.time_of_day} {scene.interior} {scene.location}")
        out.append("人物：" + ("、".join(names) if names else "（无具名角色）"))
        out.append(f"△{_scene_atmosphere(analyses[scene.shot_indexes[0]])}")
        for si in scene.shot_indexes:
            analysis = analyses[si]
            out.append(f"△{_shot_action_line(analysis)}")
            mood = re.split(r"[，、；]", str(analysis.get("mood", "")).strip())[0].rstrip("。")
            mood_used = False
            for line in lines_by_shot.get(si, []):
                dtype = line.get("dialogue_type", "对白")
                speaker = line.get("speaker") or "未归属"
                if dtype == "旁白":
                    out.append(f"旁白：{line['text']}")
                elif dtype == "对白":
                    if mood and not mood_used:
                        out.append(f"{speaker}（{mood}）：{line['text']}")
                        mood_used = True
                    else:
                        out.append(f"{speaker}：{line['text']}")
                else:
                    out.append(f"{speaker}（{dtype}）：{line['text']}")
        out.append("")
    return "\n".join(out)
