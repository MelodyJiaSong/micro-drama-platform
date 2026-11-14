import asyncio
import json
from pathlib import Path
import subprocess
import time
import urllib.request

import websockets

from libs.common.options import CHROME_PATHS, CHROME_PROFILE
from libs.infrastructure.daos.cookie__dao import CookieDao
from libs.infrastructure.errors.library__error import BrowserError

_PORT_WAIT = 10.0


def _chrome() -> Path:
    chrome = next((path for path in CHROME_PATHS if path.is_file()), None)
    if chrome is None:
        raise BrowserError("找不到 Chrome")
    return chrome


async def _cookies(ws_url: str) -> list[dict]:
    async with websockets.connect(ws_url, max_size=None) as socket:
        await socket.send(json.dumps({"id": 1, "method": "Storage.getCookies"}))
        while True:
            reply = json.loads(await socket.recv())
            if reply.get("id") == 1:
                return reply["result"]["cookies"]


class ChromeClient:
    """独立配置目录：登录时不开调试端口（避免 Google 拦截），关窗后再无头读取 cookies。"""

    def open_and_wait(self, url: str) -> None:
        CHROME_PROFILE.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(_chrome()), f"--user-data-dir={CHROME_PROFILE}", "--no-first-run",
                        "--no-default-browser-check", url])

    def read_cookies(self) -> list[CookieDao]:
        port_file = CHROME_PROFILE / "DevToolsActivePort"
        port_file.unlink(missing_ok=True)
        process = subprocess.Popen([str(_chrome()), f"--user-data-dir={CHROME_PROFILE}", "--headless=new",
                                    "--remote-debugging-port=0", "--no-first-run", "about:blank"])
        try:
            deadline = time.monotonic() + _PORT_WAIT
            while not (port_file.is_file() and port_file.read_text().strip()):
                if time.monotonic() > deadline or process.poll() is not None:
                    raise BrowserError("Chrome 没有启动调试端口；登录窗口关掉了吗？")
                time.sleep(0.1)
            port = port_file.read_text().splitlines()[0]
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version") as response:
                raw = asyncio.run(_cookies(json.load(response)["webSocketDebuggerUrl"]))
        finally:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)
        return [CookieDao(c["domain"], c["path"], bool(c["secure"]),
                          0 if c.get("session") else max(int(c.get("expires", 0)), 0), c["name"], c["value"])
                for c in raw]
