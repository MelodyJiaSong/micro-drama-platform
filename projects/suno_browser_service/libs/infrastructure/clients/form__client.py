import re
import time
from pathlib import Path
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, TimeoutError as PlaywrightTimeoutError

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.generation import ASSET_MIME_TYPES, GenerationRequest
from projects.suno_browser_service.libs.infrastructure.clients.asset__client import AssetClient

if TYPE_CHECKING:
    from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient


class FormClient:
    def __init__(self, ui: "SunoClient") -> None:
        self.ui, self.page = ui, ui.page
        self.checks: list[tuple[Locator, str, str]] = []
        self.applied: dict = {}

    def find(self, key: str, label: str, roles: tuple[str, ...] = ("textbox",)) -> Locator:
        if key in self.ui.overrides:
            return self.unique(self.page.locator(self.ui.overrides[key]), key)
        exact = re.compile("^(?:" + label + ")$", re.I)
        # Panels render a moment after tab switches; wait like control() instead of failing on the first look.
        deadline = time.monotonic() + 15
        while True:
            for role in roles:
                candidate = self.page.get_by_role(role, name=exact).filter(visible=True)
                if candidate.count():
                    return self.unique(candidate, key)
            candidate = self.page.get_by_placeholder(exact).filter(visible=True)
            if candidate.count():
                return self.unique(candidate, key)
            if time.monotonic() >= deadline:
                break
            self.page.wait_for_timeout(250)
        raise ServiceError("ui_changed", f"找不到 {key}；未提交。请校准 selectors.json")

    @staticmethod
    def unique(locator: Locator, key: str) -> Locator:
        visible = locator.filter(visible=True)
        if visible.count() != 1:
            raise ServiceError("ui_ambiguous", f"{key} 需唯一可见控件，实际 {visible.count()}；未提交")
        return visible

    def section(self, label: str) -> Locator:
        node = self.unique(self.page.get_by_text(label, exact=True), label)
        # Use the nearest UI group containing its label and actual controls.
        for _ in range(5):
            node = node.locator("..")
            if node.locator('input,button,[role="slider"],[role="switch"],[role="combobox"]').filter(visible=True).count():
                return node
        raise ServiceError("ui_changed", f"无法定位 {label} 分组；未提交")

    def text(self, key: str, control: Locator, value: str) -> None:
        limit = control.get_attribute("maxlength")
        if limit and len(value) > int(limit):
            raise ServiceError("prompt_too_long", f"{key} 最长 {limit} 字符；未提交")
        if control.get_attribute("type") == "number":
            low, high = control.get_attribute("min"), control.get_attribute("max")
            if (low and float(value) < float(low)) or (high and float(value) > float(high)):
                raise ServiceError("option_out_of_range", f"{key} 超出页面范围 {low}–{high}；未提交")
        control.fill(value, timeout=10000)
        attribute = "text" if control.get_attribute("contenteditable") == "true" else "value"
        self.checks.append((control, attribute, value))
        self.applied[key] = value

    def selected(self, control: Locator, key: str) -> None:
        for attribute in ("aria-pressed", "aria-selected", "aria-checked", "data-selected", "data-state"):
            value = control.get_attribute(attribute)
            if value in {"true", "on", "checked", "active"}:
                self.checks.append((control, attribute, value))
                return
        raise ServiceError("unverified_option", f"{key} 无法读回选中状态，未提交")

    def choose(self, key: str, opener_label: str, value: str) -> None:
        opener = self.find(key, opener_label, ("combobox", "button"))
        if opener.evaluate("e => e.tagName") == "SELECT":
            opener.select_option(label=value)
            self.checks.append((opener, "value", opener.input_value()))
        else:
            opener.click()
            entry = self.find(key + "_choice", re.escape(value), ("option", "menuitemradio", "menuitem", "button"))
            entry.click()
            self.page.wait_for_timeout(200)
            opener = self.find(key, opener_label + "|" + re.escape(value), ("combobox", "button"))
            if value.casefold() not in opener.inner_text().casefold() and value.casefold() not in (opener.get_attribute("aria-label") or "").casefold():
                raise ServiceError("unverified_option", f"{key} 选择后未显示 {value}；未提交")
            self.checks.append((opener, "text", opener.inner_text()))
        self.applied[key] = value

    def toggle(self, key: str, label: str, enabled: bool) -> None:
        if key in self.ui.overrides:
            control = self.unique(self.page.locator(self.ui.overrides[key]), key)
        else:
            direct = self.page.get_by_role("switch", name=label, exact=True).or_(self.page.get_by_role("checkbox", name=label, exact=True)).filter(visible=True)
            control = self.unique(direct, key) if direct.count() else None
        if control is not None:
            control.set_checked(enabled)
            self.checks.append((control, "checked", str(enabled)))
        else:
            button = self.unique(self.section(label).get_by_role("button", name="On" if enabled else "Off", exact=True), key)
            button.click()
            self.selected(button, key)
        self.applied[key] = enabled

    def slider(self, key: str, label: str, value: float) -> None:
        if key in self.ui.overrides:
            slider = self.unique(self.page.locator(self.ui.overrides[key]), key)
        else:
            named = self.page.get_by_role("slider", name=label, exact=True).filter(visible=True)
            slider = self.unique(named, key) if named.count() else self.unique(self.section(label).get_by_role("slider"), key)
        minimum = float(slider.get_attribute("aria-valuemin") or slider.get_attribute("min") or 0)
        maximum = float(slider.get_attribute("aria-valuemax") or slider.get_attribute("max") or 100)
        step = float(slider.get_attribute("step") or 1)
        target = minimum + value / 100 * (maximum - minimum)
        count = round((target - minimum) / step)
        if count > 1000 or step <= 0 or abs(minimum + count * step - target) > 1e-6:
            raise ServiceError("unsupported_precision", f"{key} 值与页面步长不匹配；未提交")
        slider.focus()
        slider.press("Home")
        for _ in range(count):
            slider.press("ArrowRight")
        attr = "aria-valuenow" if slider.get_attribute("aria-valuenow") is not None else "value"
        actual = slider.get_attribute(attr) if attr != "value" else slider.input_value()
        if actual is None or abs(float(actual) - target) > 1e-5:
            raise ServiceError("unverified_option", f"{key} 读回值不符；未提交")
        self.checks.append((slider, attr, actual))
        self.applied[key] = value

    def references(self, request: GenerationRequest, assets: AssetClient) -> None:
        for index, ref in enumerate(request.references):
            if ref.asset_id:
                meta = assets.get(ref.asset_id)
                def upload() -> dict:
                    self.ui.guard()
                    key = "upload_input"
                    inputs = self.page.locator(self.ui.overrides.get(key, 'input[type="file"]'))
                    if inputs.count() != 1:
                        self.find("add_reference", "Add audio.*|Add reference.*|Add files.*|Upload.*|Attach.*", ("button",)).click()
                        inputs = self.page.locator(self.ui.overrides.get(key, 'input[type="file"]'))
                    if inputs.count() != 1:
                        raise ServiceError("ui_ambiguous", "上传入口不唯一；未上传")
                    # Preserve the user's visible file name while sending the verified immutable bytes.
                    inputs.set_input_files({"name": meta["name"], "mimeType": ASSET_MIME_TYPES[Path(meta["name"]).suffix.lower()], "buffer": assets.path(meta).read_bytes()})
                    consent = self.page.get_by_role("checkbox", name=re.compile(r"rights|own|permission", re.I)).filter(visible=True)
                    if consent.count():
                        if consent.count() != 1 or not meta["rights_confirmed"]:
                            raise ServiceError("reference_rights_required", "页面要求参考权利确认；请确认有权使用后重新上传本机素材并设 rights_confirmed=true")
                        consent.set_checked(True)
                        self.find("upload_confirm", "Upload|Confirm upload|Continue", ("button",)).click()
                    chip = self.page.locator(self.ui.overrides["reference_chip"]).filter(has_text=meta["name"]) if "reference_chip" in self.ui.overrides else self.page.get_by_text(meta["name"], exact=True)
                    chip.wait_for(state="visible", timeout=60000)
                    chip = self.unique(chip, "uploaded_reference")
                    self.checks.append((chip, "text", chip.inner_text()))
                    return {"asset_id": meta["id"], "attached": True}
                self.ui.audit.call("upload_reference", {"index": index, "reference": meta}, upload)
            else:
                def attach() -> dict:
                    self.ui.guard()
                    self.find("add_reference", "Add audio.*|Add reference.*|Add files.*|Attach.*", ("button",)).click()
                    self.find("reference_url", "Paste.*(?:link|URL).*|Song URL|Reference URL").fill(ref.url)
                    self.find("attach_reference", "Add|Attach|Use reference", ("button",)).click()
                    chip = self.unique(self.page.locator(self.ui.overrides["reference_chip"]) if "reference_chip" in self.ui.overrides else self.page.get_by_role("link", name=ref.url, exact=True), "reference_chip")
                    self.checks.append((chip, "text", chip.inner_text()))
                    return {"attached": True}
                self.ui.audit.call("attach_reference", {"index": index, "url": ref.url}, attach)

    def verify(self) -> None:
        self.ui.guard()
        for control, attr, expected in self.checks:
            if not control.is_visible():
                raise ServiceError("form_changed", "已准备的控件已消失；未提交")
            actual = control.inner_text() if attr == "text" else (control.input_value() if attr == "value" else (str(control.is_checked()) if attr == "checked" else control.get_attribute(attr)))
            if (actual or "").strip() != expected.strip():
                raise ServiceError("form_changed", "已准备的选项读回不一致；未提交")

    def prompt_box(self, label: str, mode: str) -> Locator:
        """The description box. Since 2026-11 Suno's Simple panel has one textarea without any label or placeholder
        (its hint is drawn elsewhere); that single visible textarea is used only when no labelled box exists."""
        try:
            return self.find("prompt", label)
        except ServiceError:
            if mode != "simple" or "prompt" in self.ui.overrides:
                raise
            box = self.page.locator("textarea").filter(visible=True)
            if box.count() != 1:
                raise
            return box

    def clear_form(self) -> None:
        """Empty the form left by an earlier job. Since 2026-11 Suno asks "Clear entire form?" and, until confirmed,
        its modal hides the whole form from the page (every later control lookup failed as ui_changed)."""
        clear = self.page.get_by_role("button", name="Clear all form inputs", exact=True).filter(visible=True)
        if clear.count() != 1 or not clear.is_enabled():
            return
        clear.click()
        # Matched by visible text: the dialog's role and the button's accessible name are not stable.
        ask = self.page.get_by_text(re.compile(r"Clear entire form", re.I)).filter(visible=True).first
        try:
            ask.wait_for(state="visible", timeout=3000)
        except PlaywrightTimeoutError:
            return  # cleared without asking
        confirm = self.page.locator("button").filter(has_text=re.compile(r"^\s*Confirm\s*$")).filter(visible=True)
        if confirm.count() != 1:
            raise ServiceError("ui_changed", "清空表单的确认框里找不到唯一的 Confirm；未提交")
        confirm.click(timeout=5000)
        ask.wait_for(state="hidden", timeout=5000)

    def prepare(self, request: GenerationRequest, title: str, assets: AssetClient) -> list[str]:
        def action() -> list[str]:
            self.ui.guard()
            self.clear_form()
            tab = "Sounds" if request.mode == "sounds" else "Songs"
            root = self.page.get_by_role("tab", name=tab, exact=True).filter(visible=True)
            if root.count() == 1 and root.get_attribute("aria-selected") != "true":
                root.click()
            if root.count() == 1:
                self.selected(root, "surface")
            if request.mode != "sounds":
                mode = self.ui.control("custom") if request.mode == "advanced" else self.find("simple", "Simple", ("tab", "button"))
                if mode.get_attribute("aria-selected") != "true" and mode.get_attribute("aria-pressed") != "true":
                    mode.click()
                self.selected(mode, "mode")
            options = request.options.model_dump(exclude_none=True)
            if options.get("model"):
                self.choose("model", r"v\d.*|Model|Select model", options["model"])
            for key, label in (("voice_name", "Add Voice|Voice"), ("inspiration_name", "Add inspiration from a playlist|Inspo")):
                if options.get(key):
                    self.choose(key, label, options[key])
            self.references(request, assets)
            if request.mode == "advanced":
                self.text("style", self.ui.control("style"), request.prompt)
                self.text("lyrics", self.ui.control("lyrics"), "" if request.instrumental else request.lyrics or "")
                checkbox = self.page.get_by_role("checkbox", name="Instrumental", exact=True).filter(visible=True)
                if checkbox.count() == 1:
                    self.toggle("instrumental", "Instrumental", request.instrumental)
            else:
                label = "Describe the sound you want" if request.mode == "sounds" else "Song description|Describe.*(?:song|music).*|Prompt"
                self.text("prompt", self.prompt_box(label, request.mode), request.prompt)
                if request.mode == "simple":
                    self.toggle("instrumental", "Instrumental", request.instrumental)
            # Suno v6 Sounds has no title field; results are then matched as new clips since the baseline.
            title_box = self.page.get_by_role("textbox", name=re.compile(r"Title|Song Title", re.I)).filter(visible=True)
            if request.mode == "sounds" and "title" not in self.ui.overrides and not title_box.count():
                self.ui.title_field = False
                self.ui.match_prompt = request.prompt
            else:
                self.text("title", self.ui.control("title"), title)
            extra = {k: v for k, v in options.items() if k not in {"model", "voice_name", "inspiration_name"}}
            if extra:
                more = self.page.get_by_role("button", name="More Options", exact=True).filter(visible=True)
                if more.count() == 1 and more.get_attribute("aria-expanded") != "true":
                    more.click()
            if "exclude_styles" in extra:
                self.text("exclude_styles", self.find("exclude_styles", "Exclude styles"), extra["exclude_styles"])
            if "vocal_gender" in extra:
                button = self.unique(self.page.locator(self.ui.overrides["vocal_gender"]) if "vocal_gender" in self.ui.overrides else self.section("Vocal Gender").get_by_role("button", name=extra["vocal_gender"].capitalize(), exact=True), "vocal_gender")
                button.click()
                self.selected(button, "vocal_gender")
                self.applied["vocal_gender"] = extra["vocal_gender"]
            for key, label in (("weirdness", "Weirdness"), ("style_influence", "Style Influence"), ("audio_influence", "Audio Influence"), ("variety", "Variety")):
                if key in extra:
                    self.slider(key, label, extra[key])
            for key, label in (("max_mode", "Max Mode"), ("my_taste", "My Taste")):
                if key in extra:
                    self.toggle(key, label, extra[key])
            if "duration_seconds" in extra:
                group = self.section("Duration")
                custom = group.get_by_role("button", name="Custom", exact=True).filter(visible=True)
                if custom.count() == 1:
                    custom.click()
                if "duration_seconds" in self.ui.overrides:
                    self.text("duration_seconds", self.unique(self.page.locator(self.ui.overrides["duration_seconds"]), "duration_seconds"), str(extra["duration_seconds"]))
                else:
                    seconds = group.get_by_role("spinbutton", name=re.compile(r"^(?:Duration[ (]*seconds\)?|Seconds)$", re.I)).filter(visible=True)
                    minutes = group.get_by_role("spinbutton", name="Minutes", exact=True).filter(visible=True)
                    clock = group.get_by_placeholder(re.compile(r"^(?:mm:ss|m:ss)$", re.I)).filter(visible=True)
                    if seconds.count() == 1:
                        value = extra["duration_seconds"]
                        if minutes.count() == 1:
                            self.text("duration_minutes", minutes, str(value // 60))
                            value %= 60
                        self.text("duration_seconds", seconds, str(value))
                    elif clock.count() == 1:
                        value = extra["duration_seconds"]
                        self.text("duration_clock", clock, f"{value//60}:{value%60:02d}")
                    else:
                        raise ServiceError("unverified_units", "Duration 控件单位不明确；校准 duration_seconds selector 后再执行，未提交")
                self.applied["duration_seconds"] = extra["duration_seconds"]
            if "sound_type" in extra:
                label = "One-Shot|One Shot" if extra["sound_type"] == "one_shot" else "Loop"
                button = self.find("sound_type", label, ("radio", "button", "tab"))
                button.click()
                self.selected(button, "sound_type")
                self.applied["sound_type"] = extra["sound_type"]
            if "bpm" in extra:
                self.text("bpm", self.find("bpm", "BPM|Tempo|Auto", ("spinbutton",)), str(extra["bpm"]))
            self.verify()
            if not self.ui.control("create").is_enabled():
                raise ServiceError("create_disabled", "Create 不可用；未提交")
            self.ui.before_submit_check = self.verify
            self.ui.applied_options = self.applied
            return self.ui.song_links()
        return self.ui.audit.call("prepare", {"request": request.model_dump(exclude_none=True), "title": title}, action)
