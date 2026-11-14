import base64
import json
from typing import Any
from urllib.parse import quote, quote_plus

from libs.common.types import Auth
from libs.infrastructure.clients.ytdlp__client import YtdlpClient
from libs.infrastructure.daos.source__dao import SearchHitDao, SourceInfoDao

_SEARCH = "https://www.youtube.com/results?search_query="
_VIDEO_ID_LENGTH = 11


def search_filter(duration: int, order: int, cc_only: bool) -> str:
    filters = (bytes([0x18, duration]) if duration else b"") + (b"\x30\x01" if cc_only else b"")
    data = (bytes([0x08, order]) if order else b"") + (bytes([0x12, len(filters)]) + filters if filters else b"")
    return base64.b64encode(data).decode() if data else ""


def _text(info: dict[str, Any], *keys: str) -> str:
    return next((str(info[key]) for key in keys if info.get(key)), "")


class YoutubeReader:
    def __init__(self, ytdlp: YtdlpClient) -> None:
        self._ytdlp = ytdlp

    def search(self, query: str, limit: int, duration: int, order: int, cc_only: bool,
               auth: Auth) -> list[SearchHitDao]:
        url = _SEARCH + quote_plus(query)
        sp = search_filter(duration, order, cc_only)
        if sp:
            url += "&sp=" + quote(sp, safe="")
        data = json.loads(self._ytdlp.capture(["--flat-playlist", "--playlist-end", str(limit), "-J", url], auth))
        hits = []
        for entry in data.get("entries") or []:
            video_id = str(entry.get("id") or "")
            if len(video_id) != _VIDEO_ID_LENGTH:
                continue
            hits.append(SearchHitDao(video_id, f"https://www.youtube.com/watch?v={video_id}",
                                     _text(entry, "title"), _text(entry, "channel", "uploader"),
                                     float(entry.get("duration") or 0), int(entry.get("view_count") or 0)))
        return hits

    def info(self, url: str, auth: Auth) -> SourceInfoDao:
        raw = self._ytdlp.capture(["-J", url], auth)
        info = json.loads(raw)
        return SourceInfoDao(str(info["id"]), _text(info, "webpage_url") or url, _text(info, "title"),
                             _text(info, "channel", "uploader"), _text(info, "channel_url", "uploader_url"),
                             float(info.get("duration") or 0), _text(info, "upload_date"),
                             int(info.get("view_count") or 0), _text(info, "license"), raw)
