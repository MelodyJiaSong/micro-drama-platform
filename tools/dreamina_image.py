# -*- coding: utf-8 -*-
"""即梦（Dreamina）出图的共用辅助：CLI 路径、服务端 prompt 硬限、回执解析与图片下载。

出图器（gen_bg_assets / gen_bg_images / gen_char_images / gen_equipment / gen_outfit_views）都以
`from tools import dreamina_image as dm` 模块级引用它；提交与取回由各出图器自己实现
（`gen_bg_assets._dm_submit` 按 prompt 全文找回任务，并发安全）。每次调用都经 `tools/service_request.RequestLog`
先记日志再调用；引擎分工的唯一出处是 `tools/image_engine.py`（scene/bg 图禁止即梦）。

来历：原为仙剑旧剧的批量出图 CLI `tools/gen_images_xianjian.py`。follow-up 233 删除旧流程时去掉了仙剑专用的
清单、校验、提交与命令行部分，只留出图器共用的这几项，并改为现名。
"""
from __future__ import annotations

import json
import ssl
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from tools.service_request import RequestLog  # noqa: E402  出图器经 `dm.RequestLog` 记日志

DREAMINA = Path.home() / "bin" / "dreamina.exe"
PROMPT_MAX = 1600           # 服务端硬限，实测（ret=1046 / limited len: 1600）


def _payload(text: str) -> dict[str, object] | None:
    """CLI 输出里从第一个 `{` 起的 JSON 回执；解析不了返回 None。"""
    try:
        return json.loads(text[text.index("{"):])
    except (ValueError, json.JSONDecodeError):
        return None


def _url_of(payload: dict[str, object]) -> str | None:
    """成功回执里的第一张图片 URL。"""
    images = (payload.get("result_json") or {}).get("images") or []      # type: ignore[union-attr]
    return images[0]["image_url"] if images else None


def download(url: str, dest: Path) -> int:
    """下载结果图到 `dest`（经 RequestLog 记日志）；内容不是 PNG / JPEG 就报错，不落盘。返回字节数。"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data, _, _ = RequestLog(dest).http("dreamina", req, timeout=180, context=ssl.create_default_context())
    if data[:8] != b"\x89PNG\r\n\x1a\n" and data[:3] != b"\xff\xd8\xff":
        raise RuntimeError(f"下载内容不是图片：{dest.name}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data)
