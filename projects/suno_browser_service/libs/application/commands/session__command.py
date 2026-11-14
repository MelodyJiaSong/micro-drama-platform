import json
from pathlib import Path

from projects.suno_browser_service.libs.common.settings import Settings, SUNO_URL
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.browser__client import BrowserClient
from projects.suno_browser_service.libs.infrastructure.clients.lock__client import LockClient
from projects.suno_browser_service.libs.infrastructure.clients.manual_browser__client import ManualBrowserClient
from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient
from projects.suno_browser_service.libs.infrastructure.writers.private_directory__writer import PrivateDirectoryWriter
from projects.suno_browser_service.libs.infrastructure.writers.runtime__writer import RuntimeWriter


class SessionCommand:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def window(self) -> str:
        """Open (or confirm) the always-open window; no service stop is needed, the person logs in there."""
        PrivateDirectoryWriter.ensure(self.settings.data_dir)
        return ManualBrowserClient(self.settings).open_window(AuditClient(self.settings.data_dir))

    def open(self, inspect: bool = False) -> Path | str:
        config = self.settings
        if config.attached and not inspect:
            return self.window()
        PrivateDirectoryWriter.ensure(config.data_dir)
        audit = AuditClient(config.data_dir)
        lock = LockClient(config.data_dir / "browser.lock")
        lock.acquire()
        output = config.data_dir / "controls.json"
        try:
            if not inspect:
                ManualBrowserClient(config).login(audit)
            with BrowserClient(config).session(audit) as context:
                page = context.pages[0] if context.pages else context.new_page()
                audit.call("verify_login_navigate" if not inspect else "inspect_navigate", {"url": SUNO_URL},
                           lambda: page.goto(SUNO_URL, wait_until="domcontentloaded", timeout=60000))
                if not inspect:
                    def verify() -> None:
                        page.wait_for_timeout(2000)
                        SunoClient(page, audit, config.data_dir / "selectors.json").guard()
                        page.get_by_role("button", name="Profile menu button", exact=True).wait_for(timeout=20000)
                    audit.call("verify_login", {"url": SUNO_URL}, verify)
                    def save_state() -> dict:
                        context.storage_state(path=str(config.data_dir / "storage-state.json"), indexed_db=True)
                        return {"saved": True}
                    audit.call("save_login_state", {"local_only": True}, save_state)
                    RuntimeWriter(config.data_dir).clear_automation_pause()
                def snapshot() -> dict:
                    page.wait_for_timeout(2000)
                    controls = page.locator("input,textarea,button,[role=button],[role=switch],[role=checkbox],[role=tab]").evaluate_all(
                        "els => els.filter(e => e.getClientRects().length).map(e => ({tag:e.tagName,role:e.getAttribute('role'),"
                        "text:e.tagName==='INPUT'||e.tagName==='TEXTAREA'?'':e.innerText,placeholder:e.getAttribute('placeholder'),"
                        "label:e.getAttribute('aria-label'),id:e.id,type:e.getAttribute('type')}))")
                    output.write_text(json.dumps(controls, ensure_ascii=False, indent=2), encoding="utf-8")
                    return {"controls_path": str(output), "count": len(controls)}
                audit.call("inspect_controls", {"input_values": "omitted"}, snapshot)
            return output
        finally:
            lock.release()
