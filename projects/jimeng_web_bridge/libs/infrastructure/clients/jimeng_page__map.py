"""Selector and flow registry for the 即梦 web page (FR-28).

Every locator is role / text / label / title first. CSS appears only where the real DOM was observed
directly (the TipTap editor) or for read-only structure (mention nodes, hover targets). No coordinates.
`verified_web_version` stays None until the user-assisted read-only probe resolves the entry on the
real site; the offline fake site mirrors these entries, so None means "fake-verified only".
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from libs.infrastructure.readers.jimeng_history__reader import RESPONSE_PATTERNS


class LocatorStrategy(StrEnum):
    ROLE = "role"
    TEXT = "text"
    LABEL = "label"
    TITLE = "title"
    CSS = "css"
    KEYS = "keys"
    URL = "url"
    RESPONSE = "response"


DOM_STRATEGIES: frozenset[LocatorStrategy] = frozenset(
    {LocatorStrategy.ROLE, LocatorStrategy.TEXT, LocatorStrategy.LABEL, LocatorStrategy.TITLE, LocatorStrategy.CSS}
)


@dataclass(frozen=True)
class PageSelector:
    """`name` is an exact accessible name / text; `pattern` a regex name; `has_text` a regex content filter
    (needed for roles such as alert / status / tooltip whose accessible name never comes from content)."""

    step: str
    strategy: LocatorStrategy
    role: str | None = None
    name: str | None = None
    pattern: str | None = None
    has_text: str | None = None
    css: str | None = None
    keys: tuple[str, ...] = ()
    within: str | None = None
    optional: bool = False
    read_only: bool = False
    verified_web_version: str | None = None
    note: str = ""


def _role(step: str, role: str, **extra: object) -> PageSelector:
    return PageSelector(step, LocatorStrategy.ROLE, role=role, **extra)  # type: ignore[arg-type]


_TYPES = r"^(Agent 模式|图片生成|视频生成|音乐生成|音频生成|数字人|动作模仿)$"
_MODES = r"^(全能参考|首尾帧|智能多帧|智能编辑|超长视频)"
_RECORD = "history_record_by_prompt_prefix"
_FORM = "entity_new_form_dialog"

ENTRIES: tuple[PageSelector, ...] = (
    PageSelector("generate_page", LocatorStrategy.URL, name="/ai-tool/generate"),
    PageSelector("entity_page", LocatorStrategy.URL, name="/ai-tool/elements"),
    PageSelector("history_response_patterns", LocatorStrategy.RESPONSE,
                 pattern=f"{RESPONSE_PATTERNS['history_by_ids']}|{RESPONSE_PATTERNS['history_queue_info']}"),
    PageSelector("submit_response_pattern", LocatorStrategy.RESPONSE, pattern=RESPONSE_PATTERNS["submit"],
                 note="requires_probe: the submit endpoint was never observed (recon did not click generate)"),
    PageSelector("subject_response_pattern", LocatorStrategy.RESPONSE, pattern=RESPONSE_PATTERNS["subject_get"]),
    _role("login_marker", "img", name="用户头像"),
    _role("login_button", "button", name="登录", optional=True, read_only=True),
    _role("login_expired_notice", "dialog", pattern=r"登录", optional=True, read_only=True),
    _role("captcha_or_risk_popup", "dialog", pattern=r"安全验证|验证码|异常行为|风险", optional=True, read_only=True),
    _role("insufficient_credit_notice", "alert", has_text=r"积分不足", optional=True, read_only=True),
    PageSelector("parallel_limit_notice", LocatorStrategy.TEXT, pattern=r"并行任务已达上限", within="toolbar",
                 optional=True, read_only=True),
    _role("parallel_limit_toast", "alert", has_text=r"并行任务已达上限", optional=True, read_only=True),
    _role("moderation_notice", "alert", has_text=r"审核未通过|违规内容|不符合社区规范", optional=True, read_only=True),
    _role("real_face_notice", "alert", has_text=r"真人人脸", optional=True, read_only=True),
    _role("upload_rejected", "alert", has_text=r"上传失败|格式或大小", optional=True, read_only=True),
    _role("composer_region", "region", name="视频创作输入区"),
    _role("toolbar", "toolbar", name="创作工具栏", within="composer_region"),
    _role("creation_type.open", "button", pattern=_TYPES, within="toolbar"),
    _role("creation_type.menu", "listbox", name="创作类型"),
    _role("creation_type.set", "option", within="creation_type.menu", note="filtered by exact option title"),
    _role("creation_type.readback", "button", pattern=_TYPES, within="toolbar", read_only=True),
    _role("model.open", "button", pattern=r"Seedance", within="toolbar"),
    _role("model.menu", "listbox", name="模型"),
    _role("model.set", "option", within="model.menu", note="filtered by exact option title"),
    _role("model.readback", "button", pattern=r"Seedance", within="toolbar", read_only=True),
    _role("reference_mode.open", "button", pattern=_MODES, within="toolbar"),
    _role("reference_mode.menu", "listbox", name="参考模式"),
    _role("reference_mode.set", "option", within="reference_mode.menu", note="filtered by exact option title"),
    _role("reference_mode.readback", "button", pattern=_MODES, within="toolbar", read_only=True),
    _role("ratio.open", "button", pattern=r"^\d+:\d+", within="toolbar"),
    _role("ratio.menu", "dialog", name="比例与分辨率"),
    _role("ratio.group", "radiogroup", name="比例", within="ratio.menu"),
    _role("ratio.set", "radio", within="ratio.group"),
    _role("ratio.readback", "button", pattern=r"^\d+:\d+", within="toolbar", read_only=True),
    _role("resolution.group", "radiogroup", name="分辨率", within="ratio.menu"),
    _role("resolution.set", "radio", within="resolution.group"),
    _role("resolution.readback", "button", pattern=r"^\d+:\d+", within="toolbar", read_only=True),
    _role("count.group", "radiogroup", name="生成数量", within="ratio.menu"),
    _role("count.set", "radio", within="count.group"),
    _role("count.readback", "button", pattern=r"^\d+:\d+", within="toolbar", read_only=True),
    _role("duration.open", "button", pattern=r"^\d+s$", within="toolbar"),
    _role("duration.menu", "dialog", name="时长设置"),
    _role("duration.set", "spinbutton", name="时长", within="duration.menu"),
    _role("duration.readback", "button", pattern=r"^\d+s$", within="toolbar", read_only=True),
    _role("mention_trigger", "button", name="@", within="toolbar", read_only=True, note="typing @ is used instead"),
    PageSelector("estimated_credits_text", LocatorStrategy.LABEL, name="预计积分", within="toolbar", read_only=True),
    _role("generate_button", "button", name="发送", within="toolbar"),
    PageSelector("inflight_badge", LocatorStrategy.TEXT, pattern=r"\d+/\d+\s*生成中", optional=True, read_only=True),
    _role("upload_input", "button", name="上传参考内容", within="composer_region",
          note="no persistent input[type=file]; the click creates one (expect_file_chooser)"),
    _role("upload_list", "list", name="参考素材", within="composer_region"),
    _role("upload_tile", "listitem", within="upload_list", note="filtered by exact file stem"),
    _role("upload_done_signal", "progressbar", within="upload_tile", read_only=True,
          note="requires_probe: done = the tile exists and its progressbar is gone"),
    _role("upload_tile_remove", "button", name="删除", within="upload_tile"),
    PageSelector("editor", LocatorStrategy.CSS, css="div.tiptap.ProseMirror[contenteditable=true][role=textbox]",
                 within="composer_region", note="observed on the real page (7.5.0); a hidden layout copy exists"),
    _role("negative_field", "textbox", name="负向提示词", within="composer_region", optional=True),
    _role("mention_popup", "listbox", name="可能@的内容"),
    _role("mention_option_by_name", "option", within="mention_popup", note="filtered by exact candidate name"),
    PageSelector("mention_create_entity", LocatorStrategy.TEXT, pattern=r"创建主体", within="mention_popup",
                 optional=True, read_only=True, note="never clicked"),
    PageSelector("mention_node", LocatorStrategy.CSS, css='[data-type="mention"]', within="editor", read_only=True,
                 optional=True, note="requires_probe: chip markup on the real editor"),
    PageSelector("editor_clear", LocatorStrategy.KEYS, keys=("Control+a", "Delete"), within="editor"),
    PageSelector("popover_close", LocatorStrategy.KEYS, keys=("Escape",)),
    _role("history_list", "list", name="生成记录"),
    _role(_RECORD, "listitem", within="history_list", note="filtered by prompt prefix text"),
    PageSelector("record_progress_text", LocatorStrategy.TEXT, pattern=r"\d+%造梦中", within=_RECORD, read_only=True),
    PageSelector("record_media", LocatorStrategy.CSS, css="video", within=_RECORD, read_only=True,
                 note="hover target that reveals the 下载/⋯/收藏 icons"),
    PageSelector("record_download_control", LocatorStrategy.TITLE, name="下载", within=_RECORD),
    PageSelector("record_more_control", LocatorStrategy.TITLE, name="更多", within=_RECORD, optional=True, read_only=True),
    PageSelector("record_details_trigger", LocatorStrategy.TEXT, pattern=r"^详细信息", within=_RECORD, read_only=True),
    _role("record_details_credits", "tooltip", has_text=r"消耗积分数", optional=True, read_only=True),
    _role("entity_list", "list", name="主体列表"),
    _role("entity_card_by_name", "listitem", within="entity_list", read_only=True),
    _role("entity_new_form_open", "button", name="新建主体", within="entity_list"),
    _role(_FORM, "dialog", name="设置主体"),
    _role("entity_new_form_image_add", "button", name="添加参考主体图片", within=_FORM),
    PageSelector("entity_new_form_image_pending", LocatorStrategy.CSS, css='[data-state="uploading"]', within=_FORM,
                 read_only=True, optional=True, note="requires_probe"),
    _role("entity_new_form_name", "textbox", name="名称", within=_FORM),
    _role("entity_new_form_description", "textbox", name="描述", within=_FORM),
    _role("entity_new_form_save", "button", name="保存", within=_FORM),
    _role("entity_new_form_add_role", "button", name="添加角色", within=_FORM, optional=True, read_only=True,
          note="never clicked"),
)

CANARY_STEPS: tuple[str, ...] = (
    "login_marker",
    "creation_type.readback",
    "model.readback",
    "reference_mode.readback",
    "ratio.readback",
    "duration.readback",
    "editor",
    "upload_input",
    "generate_button",
    "estimated_credits_text",
)

MODEL_DISPLAY_NAMES: dict[str, str] = {
    "seedance2.5": "即梦 Seedance 2.5",
    "seedance2.0_vip": "Seedance 2.0 VIP",
    "seedance2.0fast_vip": "Seedance 2.0 Fast VIP",
    "seedance2.0": "Seedance 2.0",
    "seedance2.0fast": "Seedance 2.0 Fast",
}
VIDEO_CREATION_TYPE: str = "视频生成"
OMNI_REFERENCE_MODE: str = "全能参考"
SKELETON_CREATION_TYPE: str = "Agent 模式"
RATIO_READBACK: re.Pattern[str] = re.compile(r"(\d+:\d+)\s*[|·]\s*(\d+P)\s*[|·]\s*(\d+)\s*个?")
DURATION_READBACK: re.Pattern[str] = re.compile(r"^(\d+)\s*s$")
CREDITS_NUMBER: re.Pattern[str] = re.compile(r"(\d[\d,]*)")
DETAILS_CREDITS: re.Pattern[str] = re.compile(r"消耗积分数\s*[:：]?\s*(\d+)")
INFLIGHT_TEXT: re.Pattern[str] = re.compile(r"(\d+)/(\d+)\s*生成中")


class JimengPageMap:
    def __init__(self, entries: tuple[PageSelector, ...] = ENTRIES) -> None:
        self._entries: dict[str, PageSelector] = {}
        for entry in entries:
            if entry.step in self._entries:
                raise ValueError(f"duplicate page map step: {entry.step}")
            self._entries[entry.step] = entry

    def get(self, step: str) -> PageSelector:
        return self._entries[step]

    def steps(self) -> tuple[str, ...]:
        return tuple(self._entries)

    def entries(self) -> tuple[PageSelector, ...]:
        return tuple(self._entries.values())

    def unverified(self) -> tuple[str, ...]:
        return tuple(step for step, entry in self._entries.items() if entry.verified_web_version is None)

    @staticmethod
    def model_display(model_key: str) -> str:
        return MODEL_DISPLAY_NAMES[model_key]

    @staticmethod
    def resolution_display(resolution: str) -> str:
        return resolution.upper()
