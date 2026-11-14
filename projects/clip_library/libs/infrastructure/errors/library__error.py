class LibraryError(Exception):
    pass


class ToolFailedError(LibraryError):
    def __init__(self, tool: str, code: int, tail: str) -> None:
        hint = ""
        if "confirm you" in tail and "not a bot" in tail:
            hint = "\nYouTube 要求登录验证：加 --browser edge（或 firefox）使用本机浏览器登录，或 --cookies 文件。"
        super().__init__(f"{tool} 退出码 {code}\n{tail}{hint}")


class SourceMissingError(LibraryError):
    def __init__(self, source_id: str) -> None:
        super().__init__(f"素材库里没有 {source_id}，先用 download 下载")


class VideoFileMissingError(LibraryError):
    def __init__(self, folder: str) -> None:
        super().__init__(f"下载结束但没有找到视频文件：{folder}")


class FontMissingError(LibraryError):
    def __init__(self) -> None:
        super().__init__("找不到中文字体（微软雅黑 / 黑体），无法写出处卡")


class BrowserError(LibraryError):
    pass
