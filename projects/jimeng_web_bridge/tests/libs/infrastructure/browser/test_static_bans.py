"""NFR 安全 static bans (SEC-B02 / SEC-B03 / SEC-B05 / SEC-T01 / SEC-T02): the service never intercepts or
forges requests, never exposes bindings to the page, never opens a CDP port and ships no anti-detection code."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT: Path = Path(__file__).resolve().parents[4]
SCANNED_DIRS: tuple[str, ...] = ("apps", "libs")
BANNED_CODE: dict[str, re.Pattern[str]] = {
    "route interception": re.compile(r"\b\w*(?:page|context)\w*\.(?:route|unroute)\(|route_from_har|route\.(?:fulfill|continue_|abort|fallback)\("),
    "APIRequestContext": re.compile(r"\b(?:context|page)\.request\b"),
    "page bindings": re.compile(r"expose_binding|expose_function|add_init_script"),
    "CDP port": re.compile(r"remote-debugging-(?:port|address)|new_cdp_session"),
    "anti-detection": re.compile(r"stealth|navigator\.webdriver|AutomationControlled|disable-blink-features", re.IGNORECASE),
    "session tampering": re.compile(r"set_extra_http_headers|add_cookies|clear_cookies|storage_state\(\s*path"),
    "coordinate input": re.compile(r"mouse\.(?:click|move|down|up)\("),
}
DENYLISTED_PACKAGES: frozenset[str] = frozenset(
    {
        "playwright-stealth", "undetected-playwright", "patchright", "rebrowser-playwright", "camoufox", "botasaurus",
        "undetected-chromedriver", "selenium-stealth", "nodriver", "zendriver", "browserforge", "curl-cffi",
        "tls-client", "2captcha-python", "anticaptchaofficial", "capsolver", "python-anticaptcha", "ddddocr",
    }
)


def scan(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for label, pattern in BANNED_CODE.items():
                if pattern.search(line):
                    hits.append(f"{path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path}:{number} [{label}] {line.strip()}")
    return hits


def source_files() -> list[Path]:
    return [
        path
        for directory in SCANNED_DIRS
        for path in (PROJECT_ROOT / directory).rglob("*.py")
        if "__pycache__" not in path.parts and "node_modules" not in path.parts
    ]


def test_service_source_has_no_banned_browser_apis() -> None:
    files = source_files()
    assert any(path.name == "jimeng_browser__client.py" for path in files)
    assert scan(files) == []


@pytest.mark.parametrize(
    "line",
    [
        "await page.route('**/*', handler)",
        "await context.route('**/*', handler)",
        "response = await context.request.get(url)",
        "await page.expose_binding('x', fn)",
        "args=['--remote-debugging-port=9222']",
        "from playwright_stealth import stealth_async",
        "await page.mouse.click(10, 20)",
    ],
)
def test_scanner_catches_planted_violation(tmp_path: Path, line: str) -> None:
    planted = tmp_path / "planted.py"
    planted.write_text(line + "\n", encoding="utf-8")
    assert len(scan([planted])) == 1


def test_no_denylisted_dependencies() -> None:
    declared = (PROJECT_ROOT / "requirements.txt").read_text(encoding="utf-8") + (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    names = {re.split(r"[<>=;\[\s]", line.strip().strip('",'), maxsplit=1)[0].lower().replace("_", "-") for line in declared.splitlines()}
    assert names.isdisjoint(DENYLISTED_PACKAGES)


def test_browser_launch_passes_no_extra_args() -> None:
    client_source = (PROJECT_ROOT / "libs/infrastructure/clients/jimeng_browser__client.py").read_text(encoding="utf-8")
    assert '"args"' not in client_source and "ignore_default_args" not in client_source
