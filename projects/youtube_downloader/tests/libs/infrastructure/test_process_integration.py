import ctypes
from ctypes import wintypes
from pathlib import Path
import subprocess
import sys
from threading import Event, Thread
import time

import pytest

from libs.infrastructure.clients.process__client import ProcessClient
from libs.infrastructure.errors.download__error import DownloadCancelledError


pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows PID tree cleanup contract")


def alive(pid: int) -> bool:
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    handle = kernel.OpenProcess(0x00100000, False, pid)
    if not handle:
        return False
    try:
        return kernel.WaitForSingleObject(handle, 0) == 258
    finally:
        kernel.CloseHandle(handle)


def wait_file(path: Path) -> None:
    deadline = time.monotonic() + 10
    while not path.is_file() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert path.is_file(), f"Process did not become ready: {path.name}"


@pytest.mark.parametrize("mode", ["stream-open", "stream-closed", "root-exited"])
@pytest.mark.parametrize("interpreter", [sys.executable, sys._base_executable], ids=["venv", "base"])
def test_scope_stops_own_tree_preserves_unrelated_process_and_part(tmp_path: Path, mode: str, interpreter: str) -> None:
    child = tmp_path / "child.py"
    child.write_text("import os,sys,time\nfrom pathlib import Path\n"
                     "Path(sys.argv[1]).write_text(str(os.getpid()))\ntime.sleep(60)\n", encoding="utf-8")
    root = tmp_path / "root.py"
    root.write_text(
        "import os,subprocess,sys,time\nfrom pathlib import Path\n"
        "folder=Path(sys.argv[1])\n(folder/'root.pid').write_text(str(os.getpid()))\n"
        "(folder/'video.part').write_bytes(b'resume-data')\n"
        "subprocess.Popen([sys.executable,str(folder/'child.py'),str(folder/'child.pid')],"
        "stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)\n"
        "while not (folder/'child.pid').is_file(): time.sleep(0.01)\n"
        "print('READY',flush=True)\n"
        + ("os.close(1)\nos.close(2)\n(folder/'output.closed').touch()\n" if mode == "stream-closed" else "")
        + ("sys.exit(0)\n" if mode == "root-exited" else "time.sleep(60)\n"), encoding="utf-8")
    sentinel = subprocess.Popen([sys._base_executable, "-c", "import time;time.sleep(60)"],
                                creationflags=subprocess.CREATE_NO_WINDOW)
    cancel = Event()
    errors: list[Exception] = []

    def run() -> None:
        try:
            assert ProcessClient().run([interpreter, str(root), str(tmp_path)], cancel, lambda line: None) == 0
        except Exception as error:
            errors.append(error)

    worker = Thread(target=run, daemon=True)
    worker.start()
    try:
        wait_file(tmp_path / "child.pid")
        parent_pid = int((tmp_path / "root.pid").read_text())
        child_pid = int((tmp_path / "child.pid").read_text())
        assert sentinel.poll() is None
        if mode != "root-exited":
            assert alive(parent_pid) and alive(child_pid)
            if mode == "stream-closed":
                wait_file(tmp_path / "output.closed")
                time.sleep(0.15)
            cancel.set()
        worker.join(timeout=5)
        assert not worker.is_alive(), "Cancellation blocked after stdout EOF"
        if mode == "root-exited":
            assert not errors
        else:
            assert len(errors) == 1 and isinstance(errors[0], DownloadCancelledError)
        deadline = time.monotonic() + 3
        while (alive(parent_pid) or alive(child_pid)) and time.monotonic() < deadline:
            time.sleep(0.05)
        assert not alive(parent_pid) and not alive(child_pid)
        assert sentinel.poll() is None, "Unrelated process was terminated"
        assert (tmp_path / "video.part").read_bytes() == b"resume-data"
    finally:
        cancel.set()
        for marker in ("root.pid", "child.pid"):
            path = tmp_path / marker
            if path.is_file():
                pid = int(path.read_text())
                if alive(pid):
                    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                                   capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        sentinel.terminate()
        sentinel.wait(timeout=5)
        worker.join(timeout=5)
