import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SERVICE_NAME = "suno_browser_service"
SUNO_URL = "https://suno.com/create"
AUTOMATION_PAUSE_FILENAME = "automation-paused.json"


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    endpoint: str = ""
    channel: str = "chrome"
    headless: bool = True
    keep_browser: bool = False
    generation_timeout: int = 600
    poll_seconds: float = 5
    challenge_wait: int = 600
    # Seconds after Create (or after a person finished a verification) to see this job's clip rows before reporting
    # uncertain; 0 = off. Live 2026-11-03: rows appeared 3-5 minutes after Create, so an early cut misfires.
    clip_appear_wait: int = 0
    # The work tab does not show new clips by itself; it is reloaded this often while waiting after Create.
    refresh_seconds: float = 45
    # Seconds after Create without Suno's answer to it before the work tab is reloaded anyway.
    unanswered_create_wait: float = 240
    port: int = 8770
    # Local port of the always-open window (open-window.ps1); 0 means the service launches Chrome itself.
    attach_port: int = 0
    # Attached: with jobs queued and the window gone (or stuck), the worker reopens the window itself.
    window_auto_open: bool = False

    @property
    def profile_dir(self) -> Path:
        return self.data_dir / "profile"

    @property
    def attached(self) -> bool:
        return bool(self.attach_port) and not self.endpoint

    @property
    def window_port(self) -> int:
        """Port the window was actually opened on: attach_port unless that one was jammed (see open_window)."""
        try:
            return int((self.data_dir / "window_port").read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            return self.attach_port

    @property
    def cdp_url(self) -> str:
        return f"http://127.0.0.1:{self.window_port}"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            data_dir=REPO_ROOT / ".audit" / "service_requests" / SERVICE_NAME,
            endpoint=os.getenv("SUNO_BROWSER_WS", ""),
            channel=os.getenv("SUNO_BROWSER_CHANNEL", cls.channel),
            # Visible by default so a person can complete Suno's verification in place (SUNO_BROWSER_HEADLESS=1 hides it).
            headless=os.getenv("SUNO_BROWSER_HEADLESS", "0") != "0",
            # One local window stays open across jobs instead of a new Chrome per job (SUNO_BROWSER_KEEP=0 restores that).
            keep_browser=os.getenv("SUNO_BROWSER_KEEP", "1") != "0",
            challenge_wait=int(os.getenv("SUNO_CHALLENGE_WAIT", str(cls.challenge_wait))),
            generation_timeout=int(os.getenv("SUNO_GENERATION_TIMEOUT", str(cls.generation_timeout))),
            clip_appear_wait=int(os.getenv("SUNO_CLIP_APPEAR_WAIT", str(cls.clip_appear_wait))),
            port=int(os.getenv("SUNO_SERVICE_PORT", str(cls.port))),
            # The service works inside the window a person keeps open (SUNO_BROWSER_ATTACH_PORT=0 restores self-launched Chrome).
            attach_port=int(os.getenv("SUNO_BROWSER_ATTACH_PORT", "9333")),
            window_auto_open=os.getenv("SUNO_WINDOW_AUTO_OPEN", "1") != "0",
        )
