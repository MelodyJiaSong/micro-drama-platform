import argparse
from pathlib import Path
import sys
from threading import Event, Thread

from apps.cli.container import Container
from libs.common.options import BROWSERS, HEIGHTS, MODES


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="YouTube 单视频下载")
    parser.add_argument("url")
    parser.add_argument("-o", "--directory", default=str(Path.home() / "Downloads" / "YouTube"))
    parser.add_argument("--height", type=int, choices=HEIGHTS, default=1080)
    parser.add_argument("--mode", choices=MODES, default="video")
    parser.add_argument("--browser", choices=BROWSERS, default="")
    args = parser.parse_args()
    container = Container()
    container.wire(modules=[__name__])
    cancel = Event()
    errors: list[Exception] = []

    def download() -> None:
        try:
            result = container.command().download(args.url, args.directory, args.mode,
                                                   args.height, args.browser, cancel, print)
            print("文件已就绪：", *result.paths, sep="\n")
        except Exception as error:
            errors.append(error)

    worker = Thread(target=download)
    worker.start()
    try:
        while worker.is_alive():
            worker.join(timeout=0.1)
    except KeyboardInterrupt:
        cancel.set()
        while worker.is_alive():
            try:
                worker.join(timeout=0.1)
            except KeyboardInterrupt:
                cancel.set()
        return 130
    if errors:
        print(str(errors[0]))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
