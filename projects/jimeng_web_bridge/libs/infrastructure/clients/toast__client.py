from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger("jimeng_web_bridge.toast")

APP_TITLE: str = "即梦桥接"


class ToastClient:
    """Best-effort Windows toast (FR-56). Never raises: job state, not the toast, is the source of truth.

    With `sink_path` set (test mode only) notifications are appended to a JSONL file instead of shown.
    """

    def __init__(self, enabled: bool, sink_path: Path | None = None) -> None:
        self._enabled = enabled
        self._sink_path = sink_path

    def notify(self, title: str, body: str, launch_url: str | None) -> bool:
        if not self._enabled:
            return False
        if self._sink_path is not None:
            self._sink_path.parent.mkdir(parents=True, exist_ok=True)
            with self._sink_path.open("a", encoding="utf-8") as sink:
                sink.write(json.dumps({"title": title, "body": body, "launch_url": launch_url}, ensure_ascii=False) + "\n")
            return True
        try:
            from windows_toasts import Toast, WindowsToaster

            toast = Toast([title, body])
            if launch_url is not None and hasattr(toast, "launch_action"):
                toast.launch_action = launch_url
            WindowsToaster(APP_TITLE).show_toast(toast)
            return True
        except Exception as error:  # toast is best-effort by contract; log and move on
            logger.warning("toast_failed", extra={"kind": "toast_failed", "error": str(error)[:200]})
            return False
