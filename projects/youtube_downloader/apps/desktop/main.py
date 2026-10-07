import tkinter as tk

from apps.desktop.container import Container
from apps.desktop.window import DownloadWindow


def main() -> None:
    container = Container()
    container.wire(modules=[__name__])
    root = tk.Tk()
    DownloadWindow(root, container.command())
    root.mainloop()


if __name__ == "__main__":
    main()
