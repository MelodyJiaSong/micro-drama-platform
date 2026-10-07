from pathlib import Path
from threading import Event, get_ident
import gc
import subprocess
import sys
import time
import tkinter as tk

from dependency_injector import providers
import pytest

from apps.desktop.container import Container
from apps.desktop.window import DownloadWindow
from libs.application.dtos.download__dto import DownloadCdto
from libs.common.options import PROGRESS_PREFIX


class ControlledCommand:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.release = Event()
        self.calls: list[tuple[object, ...]] = []
        self.worker_ids: list[int] = []
        self.error: Exception | None = None

    def download(self, url, directory, mode, height, browser, cancel, notify):
        self.calls.append((url, directory, mode, height, browser, cancel))
        self.worker_ids.append(get_ident())
        notify("合并媒体")
        notify(PROGRESS_PREFIX + "42.5%|1MiB/s|00:02")
        while not self.release.wait(0.01):
            if cancel.is_set():
                raise InterruptedError("已取消；保留分片")
        if self.error:
            raise self.error
        return DownloadCdto((str(self.path),))


def run_until(root: tk.Misc, predicate, timeout: float = 3) -> None:
    deadline = time.monotonic() + timeout
    observed: list[bool] = []

    def poll():
        if predicate():
            observed.append(True)
            root.quit()
        elif time.monotonic() >= deadline:
            root.quit()
        else:
            root.after(10, poll)

    root.after(0, poll)
    root.mainloop()
    assert observed, "Tk event loop timed out waiting for the observable state"


@pytest.fixture(scope="session")
def tk_interpreter():
    app = tk.Tk()
    app.withdraw()
    yield app
    app.destroy()
    gc.collect()


@pytest.fixture
def root(tk_interpreter):
    app = tk.Toplevel(tk_interpreter)
    app.withdraw()
    yield app
    if app.winfo_exists():
        app.destroy()
    for callback in tk_interpreter.tk.call("after", "info"):
        tk_interpreter.tk.call("after", "cancel", callback)
    gc.collect()


@pytest.fixture
def window(root, tmp_path):
    output = tmp_path / "fixture.mp4"
    output.write_bytes(b"UI fixture, not a media download")
    command = ControlledCommand(output)
    container = Container()
    container.command.override(providers.Object(command))
    app = DownloadWindow(root, container.command())
    app.url.set("https://youtu.be/BaW_jenozKc")
    app.directory.set(str(tmp_path))
    yield app, command
    app.cancel.set()
    command.release.set()
    if app.worker:
        app.worker.join(timeout=2)
        assert not app.worker.is_alive()


def test_start_progress_done_and_responsive_single_task(root, window):
    app, command = window
    main_thread = get_ident()
    app.start_button.invoke()
    run_until(root, lambda: float(app.progress["value"]) == 42.5)
    assert app.start_button.instate(["disabled"])
    assert app.cancel_button.instate(["!disabled"])
    assert "1MiB/s" in app.status.get() and "00:02" in app.status.get()
    assert "合并媒体" in app.log.get("1.0", "end")
    assert command.worker_ids[0] != main_thread
    responsive = []
    root.after(0, lambda: responsive.append(True))
    run_until(root, lambda: bool(responsive))
    app.start_button.invoke()
    assert len(command.calls) == 1
    assert command.calls[0][4] == ""
    assert app.status.get() != "完成"
    command.release.set()
    run_until(root, lambda: app.status.get() == "完成")
    assert float(app.progress["value"]) == 100
    assert str(command.path) in app.log.get("1.0", "end")
    assert app.start_button.instate(["!disabled"])
    assert app.cancel_button.instate(["disabled"])


def test_command_error_is_visible_and_controls_recover(root, window):
    app, command = window
    command.error = RuntimeError("cookies 读取失败")
    command.release.set()
    app.start_button.invoke()
    run_until(root, lambda: "下载失败" in app.status.get())
    assert "cookies 读取失败" in app.log.get("1.0", "end")
    assert "文件已就绪" not in app.log.get("1.0", "end")
    assert app.start_button.instate(["!disabled"])
    assert app.cancel_button.instate(["disabled"])


@pytest.mark.parametrize("quality,browser,mode,height,selected", [
    (6, 3, "mp3", 0, "firefox"),
    (5, 1, "video", 480, "chrome"),
    (0, 2, "video", 0, "edge"),
])
def test_user_choices_reach_command(root, window, quality, browser, mode, height, selected):
    app, command = window
    app.quality.current(quality)
    app.browser.current(browser)
    app.start_button.invoke()
    run_until(root, lambda: len(command.calls) == 1)
    assert command.calls[0][2:5] == (mode, height, selected)


def test_cancel_is_not_success_and_retry_has_fresh_token(root, window):
    app, command = window
    app.start_button.invoke()
    run_until(root, lambda: len(command.calls) == 1)
    token = command.calls[0][5]
    app.cancel_button.invoke()
    run_until(root, lambda: app.status.get() == "已取消")
    assert token.is_set()
    assert "保留分片" in app.log.get("1.0", "end")
    assert "文件已就绪" not in app.log.get("1.0", "end")
    app.start_button.invoke()
    run_until(root, lambda: len(command.calls) == 2)
    assert command.calls[1][5] is not token
    assert not command.calls[1][5].is_set()
    command.release.set()
    run_until(root, lambda: app.status.get() == "完成")


def test_close_waits_for_worker_to_cancel_before_destroying(root, window):
    app, command = window
    app.start_button.invoke()
    run_until(root, lambda: len(command.calls) == 1)
    root.tk.call(root.protocol("WM_DELETE_WINDOW"))
    assert app.cancel.is_set()
    assert root.winfo_exists()
    root.bind("<Destroy>", lambda event: root.quit() if event.widget is root else None)
    timed_out = []
    root.after(3000, lambda: (timed_out.append(True), root.quit()))
    root.mainloop()
    assert not timed_out
    assert app.worker is not None and not app.worker.is_alive()
    assert not root.winfo_exists()


def test_real_di_command_rejects_invalid_link_in_window(root, tmp_path):
    app = DownloadWindow(root, Container().command())
    app.url.set("https://youtube.com.evil.example/watch?v=BaW_jenozKc")
    app.directory.set(str(tmp_path))
    app.start_button.invoke()
    run_until(root, lambda: "下载失败" in app.status.get())
    assert app.log.get("1.0", "end").strip()
    assert "文件已就绪" not in app.log.get("1.0", "end")
    assert not list(tmp_path.iterdir())
    app.worker.join(timeout=2)


def test_actual_cli_subprocess_rejects_invalid_input(tmp_path):
    project = Path(__file__).resolve().parents[3]
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "https://example.com/video", "-o", str(tmp_path)],
        cwd=project, capture_output=True, text=True, encoding="utf-8", timeout=10,
    )
    assert result.returncode == 1
    assert result.stdout.strip()
    assert "Traceback" not in result.stderr
    assert not list(tmp_path.iterdir())
