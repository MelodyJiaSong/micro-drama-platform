from __future__ import annotations

from dataclasses import dataclass

from libs.common.constants import DEFAULT_ASPECT, PROMPT_CHAR_LIMIT
from libs.common.vocab import STANDARD_NEGATIVES, SUBTITLE_FORBIDDEN_TOKENS
from libs.domain.errors.shot__error import PromptBudgetExceededError, SubtitleContaminationError
from libs.domain.value_objects.promptbudget__valueobject import visible_char_count


@dataclass(frozen=True)
class DialogueForShot:
    speaker: str
    text: str
    dialogue_type: str  # 对白 | 内心独白 | 旁白


@dataclass(frozen=True)
class ShotPromptFields:
    index: int
    reference_line: str
    characters: dict[str, str]  # name -> locked descriptor (byte-identical paste)
    plot: str
    scene: str
    shot_size: str
    camera_angle: str
    camera_move: str
    blocking: str
    action: str
    dialogue: tuple[DialogueForShot, ...]
    lighting: str
    pacing: str
    render_style: str
    duration_s: float
    link: str  # 承接 | 硬切
    tail_locked: bool


def _dialogue_block(lines: tuple[DialogueForShot, ...]) -> str:
    """武神觉醒台词体 (follow-up 008): header + 逐条 `· 角色〔类型〕：「台词」`."""
    if not lines:
        return "台词: （本镜无台词）"
    out = ["台词:（画面不显示文字、仅供口型与配音参考；逐条↓）"]
    for d in lines:
        label = d.dialogue_type
        if d.dialogue_type in ("内心独白", "旁白"):
            label += "·口型不动不对口型·声音为画外"
        out.append(f"· {d.speaker}〔{label}〕：「{d.text}」")
    return "\n".join(out)


def _action_timeline(action: str, duration_s: float) -> str:
    """武神觉醒动作体 (follow-up 008): time-segmented beats. Merged units (joined with
    （镜内跳切）) get equal integer spans; a single action spans the whole shot."""
    total = int(round(duration_s))
    parts = [p.strip("；").strip() for p in action.split("（镜内跳切）") if p.strip("；").strip()]
    if len(parts) <= 1:
        return f"0-{total}s {action}"
    bounds = [round(i * total / len(parts)) for i in range(len(parts) + 1)]
    segments = [f"{bounds[i]}-{bounds[i + 1]}s {p}" for i, p in enumerate(parts)]
    return " /（镜内跳切）".join(segments)


def _alloc_line(f: ShotPromptFields) -> str:
    head = ("本镜首帧＝上一镜末帧(承接上镜·用户上传上一镜渲染末帧)" if f.link == "承接"
            else "本镜起幅为独立首帧(硬切无承接帧)")
    refs = "、".join(f"@{n}参考图锁定角色{n}" for n in f.characters) if f.characters else "无人物参考"
    return f"参考分配: `{head}、{refs}；保持角色服装/场景/光线一致、只生成本镜运动·不改造主体外观`"


def build_video_prompt_body(f: ShotPromptFields, char_limit: int = PROMPT_CHAR_LIMIT) -> tuple[str, list[str]]:
    """Assemble the ## 视频 prompt body in the 武神觉醒 field order (follow-up 008)
    with generation-time self-checks (FR-5.4). Budget enforcement per CLAUDE.md trim
    guidance: the ~22-item standard negative set is the floor we keep, NOT the first
    sacrifice — droppable sections go 渲染样式 → 节奏 → 光线, each drop is logged, and
    overflow after that fails hard. Returns (body, dropped_section_names)."""
    chars = ("角色: " + "；".join(f"`{n} — {d}`" for n, d in f.characters.items())
             if f.characters else "角色: （空镜·无具名角色）")
    required_head = [
        f.reference_line,
        _alloc_line(f),
        chars,
    ]
    if f.characters:
        names = "、".join(f.characters)
        required_head.append(f"角色识别 / 参考图: {names}＝参考图锁定; 脸以参考图为准, 不写五官")
    required_head += [
        f"情节: `{f.plot}`",
        f"场景: `{f.scene}`",
        f"镜头: `{f.shot_size}、{f.camera_angle}、{f.camera_move}`",
        f"走位: `{f.blocking}`",
        f"动作: `{_action_timeline(f.action, f.duration_s)}`",
        _dialogue_block(f.dialogue),
    ]
    required_tail = [STANDARD_NEGATIVES, f"比例: {DEFAULT_ASPECT}", f"时长: {f.duration_s:.0f}秒"]
    droppable: list[tuple[str, str]] = [
        ("光线", f"光线 / 色调: `{f.lighting}`"),
        ("节奏", f"节奏: `{f.pacing}`"),
        ("渲染样式", f"渲染样式: {f.render_style}"),
    ]
    dropped: list[str] = []
    while True:
        body = "\n".join(required_head + [line for _, line in droppable] + required_tail)
        if visible_char_count(body) <= char_limit:
            break
        if not droppable:
            raise PromptBudgetExceededError(
                f"shot{f.index:02d} prompt still {visible_char_count(body)} chars with only required sections"
            )
        name, _ = droppable.pop()
        dropped.append(name)
    assert_subtitle_free(body, f.index)
    return body, dropped


def assert_subtitle_free(body: str, index: int) -> None:
    for token in SUBTITLE_FORBIDDEN_TOKENS:
        if token in body:
            raise SubtitleContaminationError(f"shot{index:02d} prompt contains forbidden subtitle token: {token}")


def decide_link(is_first_shot: bool, continuous_with_prev: bool) -> str:
    if is_first_shot:
        return "硬切"
    return "承接" if continuous_with_prev else "硬切"
