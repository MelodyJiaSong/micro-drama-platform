from dataclasses import dataclass
import re
from urllib.parse import parse_qs, urlsplit

from libs.common.options import BROWSERS, HEIGHTS, MODES
from libs.domain.errors.download__error import DownloadError


@dataclass(frozen=True)
class Download:
    url: str
    directory: str
    mode: str = "video"
    height: int = 1080
    browser: str = ""

    def __post_init__(self) -> None:
        try:
            parsed = urlsplit(self.url.strip())
            host = parsed.hostname
            port = parsed.port
        except ValueError as error:
            raise DownloadError("视频链接格式不正确。") from error
        if (parsed.scheme not in ("http", "https") or parsed.username is not None
                or parsed.password is not None or port is not None):
            raise DownloadError("请粘贴不含账号、密码和端口的 YouTube 视频链接。")
        video_id = ""
        if host == "youtu.be":
            video_id = parsed.path.strip("/")
        elif host in ("youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"):
            if parsed.path == "/watch":
                ids = parse_qs(parsed.query).get("v", [])
                video_id = ids[0] if len(ids) == 1 else ""
            else:
                match = re.fullmatch(r"/(?:shorts|live|embed)/([\w-]{11})/?", parsed.path)
                video_id = match[1] if match else ""
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
            raise DownloadError("请提供 YouTube 单视频链接；不支持频道或纯播放列表。")
        if self.mode not in MODES or self.height not in HEIGHTS or self.browser not in BROWSERS:
            raise DownloadError("下载格式、清晰度或浏览器选项无效。")
        if not self.directory.strip():
            raise DownloadError("请选择保存目录。")
        object.__setattr__(self, "url", f"https://www.youtube.com/watch?v={video_id}")
