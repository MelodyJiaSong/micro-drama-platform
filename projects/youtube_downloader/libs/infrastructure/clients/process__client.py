import os
from queue import Empty, Queue
import subprocess
from threading import Event, Thread
from typing import Callable

from libs.infrastructure.errors.download__error import DownloadCancelledError
from libs.infrastructure.clients.process_scope__client import ProcessScopeClient


class ProcessClient:
    def run(self, arguments: list[str], cancel: Event, notify: Callable[[str], None]) -> int:
        if cancel.is_set():
            raise DownloadCancelledError()
        options = ({"creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP}
                   if os.name == "nt" else {"start_new_session": True})
        scope = ProcessScopeClient()
        try:
            process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       stdin=subprocess.DEVNULL, text=True, encoding="utf-8",
                                       errors="replace", **options)
        except Exception:
            scope.close()
            raise
        try:
            scope.attach(process)
        except Exception:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                               capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            scope.close()
            if process.poll() is None:
                process.kill()
            process.wait()
            if process.stdout is not None:
                process.stdout.close()
            raise
        lines: Queue[str | None] = Queue()

        def read() -> None:
            assert process.stdout is not None
            try:
                for line in process.stdout:
                    lines.put(line.rstrip("\r\n"))
            finally:
                lines.put(None)

        reader = Thread(target=read, daemon=True)
        reader.start()
        try:
            eof = False
            while True:
                if cancel.is_set():
                    raise DownloadCancelledError()
                if eof:
                    try:
                        result = process.wait(timeout=0.1)
                    except subprocess.TimeoutExpired:
                        continue
                    if cancel.is_set():
                        raise DownloadCancelledError()
                    return result
                try:
                    line = lines.get(timeout=0.1)
                except Empty:
                    if process.poll() is not None:
                        scope.close()
                    continue
                if line is None:
                    eof = True
                else:
                    notify(line)
        finally:
            scope.close()
            if process.poll() is None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    scope.force_close()
                    if process.poll() is None:
                        process.kill()
                    process.wait()
            reader.join(timeout=2)
            if process.stdout is not None:
                process.stdout.close()
