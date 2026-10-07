from pathlib import Path
from queue import Empty, Queue
import re
from threading import Event, Thread
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.scrolledtext import ScrolledText

from libs.application.commands.download__command import DownloadCommand
from libs.common.options import BROWSERS, FILE_PREFIX, HEIGHTS, PROGRESS_PREFIX


class DownloadWindow:
    def __init__(self, root: tk.Tk, command: DownloadCommand) -> None:
        self.root, self.command = root, command
        self.events: Queue[tuple[str, object]] = Queue()
        self.cancel = Event()
        self.worker: Thread | None = None
        self.closing = False
        root.title("YouTube 下载工具")
        root.geometry("760x590")
        root.minsize(640, 520)
        root.configure(background="#f5f7fa")
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fa")
        style.configure("TLabel", background="#f5f7fa", foreground="#182230")
        frame = ttk.Frame(root, padding=24)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(10, weight=1)
        ttk.Label(frame, text="YouTube 下载", font=("Microsoft YaHei UI", 20, "bold")).grid(sticky="w")
        ttk.Label(frame, text="粘贴单视频或 Shorts 链接，保存到本机。").grid(row=1, sticky="w", pady=(4, 18))
        ttk.Label(frame, text="视频链接").grid(row=2, sticky="w")
        self.url = tk.StringVar()
        self.link_entry = ttk.Entry(frame, textvariable=self.url)
        self.link_entry.grid(row=3, sticky="ew", pady=(5, 12))
        ttk.Label(frame, text="保存目录").grid(row=4, sticky="w")
        folder = ttk.Frame(frame)
        folder.grid(row=5, sticky="ew", pady=(5, 12))
        folder.columnconfigure(0, weight=1)
        self.directory = tk.StringVar(value=str(Path.home() / "Downloads" / "YouTube"))
        ttk.Entry(folder, textvariable=self.directory).grid(row=0, column=0, sticky="ew")
        ttk.Button(folder, text="选择…", command=self.choose_directory).grid(row=0, column=1, padx=(8, 0))
        choices = ttk.Frame(frame)
        choices.grid(row=6, sticky="ew")
        self.quality_labels = ("最佳可用", *(f"高度 ≤ {height}p" for height in HEIGHTS[1:]), "仅音频 MP3")
        self.quality = ttk.Combobox(choices, values=self.quality_labels, state="readonly", width=22)
        self.quality.current(HEIGHTS.index(1080))
        self.quality.grid(row=0, column=0, sticky="w")
        ttk.Label(choices, text="登录（可选）").grid(row=0, column=1, padx=(18, 8))
        self.browser = ttk.Combobox(choices, values=("不读取登录", "Chrome", "Edge", "Firefox"),
                                    state="readonly", width=16)
        self.browser.current(0)
        self.browser.grid(row=0, column=2)
        ttk.Label(frame, text="实际画质取决于源视频；视频保存 MP4，最高画质可能需要较新的播放器。",
                  wraplength=650).grid(row=7, sticky="w", pady=(10, 12))
        actions = ttk.Frame(frame)
        actions.grid(row=8, sticky="ew")
        self.start_button = ttk.Button(actions, text="开始下载", command=self.start)
        self.start_button.pack(side="left")
        self.cancel_button = ttk.Button(actions, text="取消", command=self.cancel_download, state="disabled")
        self.cancel_button.pack(side="left", padx=8)
        self.status = tk.StringVar(value="准备就绪")
        ttk.Label(actions, textvariable=self.status).pack(side="left", padx=8)
        self.progress = ttk.Progressbar(frame, maximum=100)
        self.progress.grid(row=9, sticky="ew", pady=12)
        self.log = ScrolledText(frame, height=9, state="disabled", wrap="word",
                                background="white", foreground="#182230", font=("Microsoft YaHei UI", 9))
        self.log.grid(row=10, sticky="nsew")
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.link_entry.focus_set()
        root.after(80, self.drain)

    def choose_directory(self) -> None:
        selected = filedialog.askdirectory(parent=self.root, title="选择保存目录")
        if selected:
            self.directory.set(selected)

    def append_log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        if int(self.log.index("end-1c").split(".")[0]) > 300:
            self.log.delete("1.0", "100.0")
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self) -> None:
        if self.worker and self.worker.is_alive():
            return
        index = self.quality.current()
        mode = "mp3" if index == len(HEIGHTS) else "video"
        height = 0 if mode == "mp3" else HEIGHTS[index]
        args = (self.url.get(), self.directory.get(), mode, height, BROWSERS[self.browser.current()])
        self.cancel = Event()
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.progress["value"] = 0
        self.status.set("正在解析视频…")
        self.append_log("开始新任务")

        def download() -> None:
            try:
                result = self.command.download(*args, self.cancel,
                                               lambda line: self.events.put(("line", line)))
                self.events.put(("done", result.paths))
            except InterruptedError as error:
                self.events.put(("cancelled", str(error)))
            except Exception as error:
                self.events.put(("error", str(error)))

        self.worker = Thread(target=download, daemon=True)
        self.worker.start()

    def cancel_download(self) -> None:
        self.cancel.set()
        self.status.set("正在取消…")
        self.cancel_button.configure(state="disabled")

    def drain(self) -> None:
        for _ in range(150):
            try:
                kind, payload = self.events.get_nowait()
            except Empty:
                break
            if kind == "line":
                line = str(payload)
                if line.startswith(PROGRESS_PREFIX):
                    percent, speed, eta = line[len(PROGRESS_PREFIX):].split("|", 2)
                    match = re.search(r"(\d+(?:\.\d+)?)%", percent)
                    if match:
                        self.progress["value"] = float(match[1])
                    self.status.set(f"下载 {percent.strip()} · {speed.strip()} · 剩余 {eta.strip()}")
                elif not line.startswith(FILE_PREFIX):
                    self.append_log(line)
                    self.status.set("正在下载 / 合并 / 转换…")
            else:
                self.start_button.configure(state="normal")
                self.cancel_button.configure(state="disabled")
                self.status.set({"done": "完成", "error": "下载失败，详见下方日志", "cancelled": "已取消"}[kind])
                if kind == "done":
                    self.progress["value"] = 100
                    self.append_log("文件已就绪：\n" + "\n".join(payload))
                else:
                    self.append_log(str(payload))
        if self.closing and (not self.worker or not self.worker.is_alive()):
            self.root.destroy()
            return
        self.root.after(80, self.drain)

    def close(self) -> None:
        self.closing = True
        self.cancel_download()
