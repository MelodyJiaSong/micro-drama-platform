"""Shared API-test setup: the real global config made safe for test mode (localhost start_url, bundled chromium)."""
from __future__ import annotations

import re
from pathlib import Path

REAL_GLOBAL_TOML: Path = Path(__file__).resolve().parents[2] / "config" / "global.toml"
FAKE_START_URL: str = "http://127.0.0.1:9/fake-jimeng"
_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ('start_url = "https://jimeng.jianying.com/ai-tool/generate?type=video"', f'start_url = "{FAKE_START_URL}"'),
    ('channel = "chrome"', 'channel = "chromium"'),
)


def test_global_toml_text(port: int = 8790) -> str:
    text = REAL_GLOBAL_TOML.read_text(encoding="utf-8")
    for old, new in _REPLACEMENTS:
        assert old in text, f"config/global.toml no longer contains {old!r}; update tests/api/support.py"
        text = text.replace(old, new)
    return re.sub(r"(?m)^port = \d+$", f"port = {port}", text, count=1)


test_global_toml_text.__test__ = False  # type: ignore[attr-defined]


def write_test_global_toml(path: Path, port: int = 8790) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(test_global_toml_text(port), encoding="utf-8")
