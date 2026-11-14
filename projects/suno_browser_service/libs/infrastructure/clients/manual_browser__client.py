import json
import os
import shutil
import socket
import subprocess
import time
import urllib.request
from urllib.parse import urlsplit
from pathlib import Path

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings, SUNO_URL
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient


WINDOW_RENDER_FLAGS = ("--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
                       "--disable-background-timer-throttling")


def port_free(port: int) -> bool:
    """Nothing holds the local port. A Chrome stuck while exiting kept 9333 listening without answering (2026-11-03)."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        probe.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        probe.close()


def window_open(settings: Settings) -> bool:
    """True when the always-open window answers on its local debugging port."""
    if not settings.attach_port:
        return False
    try:
        with urllib.request.urlopen(settings.cdp_url + "/json/version", timeout=0.75) as response:
            return response.status == 200 and "webSocketDebuggerUrl" in json.loads(response.read() or b"{}")
    except Exception:
        return False


def close_hung_tabs(settings: Settings, wait: float = 5.0) -> dict:
    """Close tabs of the window whose page no longer answers. Playwright attaches to every tab, so one hung tab made
    each connect time out (2026-11-03: two hung /create tabs, every job window_not_open). Closing goes through the
    browser's own /json/close, which works even when the tab's renderer is stuck."""
    from websockets.sync.client import connect

    with urllib.request.urlopen(settings.cdp_url + "/json", timeout=5) as response:
        targets = json.loads(response.read() or b"[]")
    closed = []
    for target in targets:
        if target.get("type") != "page" or not target.get("webSocketDebuggerUrl"):
            continue
        try:
            with connect(target["webSocketDebuggerUrl"], open_timeout=wait, close_timeout=1, max_size=None) as socket_:
                socket_.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": "1", "returnByValue": True}}))
                deadline = time.monotonic() + wait
                while json.loads(socket_.recv(timeout=max(0.1, deadline - time.monotonic()))).get("id") != 1:
                    pass
        except Exception:
            with urllib.request.urlopen(settings.cdp_url + "/json/close/" + target["id"], timeout=5) as response:
                response.read()
            closed.append(urlsplit(target.get("url", "")).path or "/")
    return {"pages": sum(t.get("type") == "page" for t in targets), "closed": closed}


class ManualBrowserClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def executable(self) -> Path:
        if self.settings.channel != "chrome":
            raise ServiceError("manual_login_channel", "手动登录目前使用已安装的 Google Chrome，请设置 SUNO_BROWSER_CHANNEL=chrome")
        found = shutil.which("chrome") or shutil.which("google-chrome")
        candidates = ([Path(found)] if found else []) + [
            Path(root) / "Google/Chrome/Application/chrome.exe"
            for key in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")
            if (root := os.getenv(key))
        ]
        for path in candidates:
            if path.is_file():
                return path
        raise ServiceError("browser_unavailable", "未找到已安装的 Google Chrome，无法打开手动登录窗口")

    def login(self, audit: AuditClient) -> None:
        if self.settings.endpoint:
            raise ServiceError("remote_login", "远程 Browserless 请使用其交互登录会话；本命令只打开本机 Chrome")
        argv = [str(self.executable()), f"--user-data-dir={self.settings.profile_dir}",
                "--no-first-run", "--disable-background-mode", "--new-window", SUNO_URL]
        process: subprocess.Popen | None = None

        def launch() -> dict:
            nonlocal process
            process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL)
            return {"pid": process.pid}

        audit.call("manual_login_launch", {"url": SUNO_URL, "browser": "installed Chrome",
                   "profile": "service dedicated", "control": "human only", "remote_debugging": False}, launch)
        print("已打开普通 Chrome 专用窗口。请手动登录 Suno，看到自己的账号后关闭这个专用窗口；随后程序保存登录状态。", flush=True)
        assert process is not None
        code = process.wait()
        if code != 0:
            raise ServiceError("manual_login_closed", f"Chrome 登录窗口异常退出（{code}），登录尚未验证")

    def profile_in_use(self) -> bool:
        """Chrome keeps the profile's lockfile open; a second Chrome on the same profile would ignore the debugging port."""
        lockfile = self.settings.profile_dir / "lockfile"
        if not lockfile.exists():
            return False
        try:
            with lockfile.open("ab"):
                return False
        except OSError:
            return True

    def profile_processes(self) -> list[int]:
        """Chrome processes started on the service's own profile (matched by its folder in the command line)."""
        if os.name != "nt":
            return []
        profile = str(self.settings.profile_dir).replace("'", "''")
        script = ("Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
                  f"Where-Object {{ $_.CommandLine -and $_.CommandLine.Contains('{profile}') }} | "
                  "ForEach-Object { $_.ProcessId }")
        try:
            out = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                                 capture_output=True, text=True, timeout=30).stdout
        except Exception:
            return []
        return [int(line) for line in out.split() if line.strip().isdigit()]

    def end_profile_processes(self) -> dict:
        """End a service-profile Chrome that holds the profile but no longer answers; other Chrome windows are untouched."""
        pids = self.profile_processes()
        for pid in pids:
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, timeout=30)
        deadline = time.monotonic() + 15
        while self.profile_in_use() and time.monotonic() < deadline:
            time.sleep(0.5)
        return {"ended": len(pids), "profile_free": not self.profile_in_use()}

    def open_window(self, audit: AuditClient) -> str:
        """Open the always-open window: ordinary installed Chrome on the service profile, debugging port on 127.0.0.1 only."""
        config = self.settings
        if not config.attached:
            raise ServiceError("attach_disabled", "常驻窗口模式已关闭（SUNO_BROWSER_ATTACH_PORT=0 或使用远程 Browserless）")
        if window_open(config):
            return f"常驻 Suno 窗口已经开着（127.0.0.1:{config.window_port}）"
        if self.profile_in_use():
            raise ServiceError("profile_busy", "服务专用 Chrome 配置正被另一个窗口占用（旧登录窗口或旧模式服务）；关掉它后重试")
        # The configured port, or the next free one when a dead Chrome still holds it; the choice is kept in window_port.
        port = next((p for p in range(config.attach_port, config.attach_port + 11) if port_free(p)), config.attach_port)
        record = config.data_dir / "window_port"
        if port == config.attach_port:
            record.unlink(missing_ok=True)
        else:
            record.parent.mkdir(parents=True, exist_ok=True)
            record.write_text(str(port), encoding="utf-8")
        argv = [str(self.executable()), f"--user-data-dir={config.profile_dir}", f"--remote-debugging-port={port}",
                "--no-first-run", "--no-default-browser-check", "--disable-background-mode",
                # A covered or minimised window must keep rendering the service's tab: throttled, the form took longer
                # than the control wait and screenshots never finished (2026-11-03). Same switches Playwright launches with.
                *WINDOW_RENDER_FLAGS, "--new-window", SUNO_URL]
        flags = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0

        def launch() -> dict:
            process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                       creationflags=flags, start_new_session=os.name != "nt")
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                if window_open(config):
                    return {"pid": process.pid, "listening": True}
                time.sleep(0.5)
            return {"pid": process.pid, "listening": False}

        result = audit.call("open_window_launch", {"url": SUNO_URL, "browser": "installed Chrome", "profile": "service dedicated",
                            "remote_debugging": f"127.0.0.1:{port}"}, launch)
        if not result["listening"]:
            raise ServiceError("window_not_open", "Chrome 已启动但调试端口没有响应；关掉这个窗口后重试")
        return (f"已打开常驻 Suno 窗口（127.0.0.1:{port}）。请保持它开着；没登录就直接在里面登录，"
                "服务会在单独的标签页里操作，弹出验证码时在同一窗口完成。")
