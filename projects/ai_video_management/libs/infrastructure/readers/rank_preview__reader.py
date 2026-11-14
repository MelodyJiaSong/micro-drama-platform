"""排行榜预览（follow-up 320）：读 `ai_videos/paihangbang` 系列与各期产物给审片页。只读。

一期目录 `episodes/<期>/`：`data.json`（items / insights）、`assets.json`（图片账本，按 `file` 对应）、
`render/*.mp4` 与同名 `.manifest.json`、`render/thumbnail.png`、`qc.md`、`publish.md`、`_build/handoff.md`。
文件陆续生成，缺什么就空着，不报错；JSON 坏了写进 `error`。路径只接受系列根或其下一期目录。
契约 v1.3 列表期（`mode: list`）不出冠军，另给首个 / 末个；公司卡字段（corner / logo / person / notes 等）照传（follow-up 321）。
"""
from __future__ import annotations

import json
import re
import struct
from dataclasses import replace
from pathlib import Path
from typing import Any

from libs.application.dtos.rank_preview__dto import (
    RankDocQdto, RankEpisodeCardQdto, RankEpisodeQdto, RankImageQdto, RankImageStatsQdto, RankInsightQdto,
    RankItemQdto, RankPersonQdto, RankPreviewQdto, RankSeriesQdto, RankVideoQdto,
)
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.drama__error import DramaNotFoundError, InvalidDramaPathError

SERIES = "ai_videos/paihangbang"
EPISODES = "episodes"
FLAGS = "_assets/flags"
FOCUS = list(range(11, 21))
MAX_JSON = 5_000_000
MAX_TEXT = 400_000
EXCERPT_LINES = 30
RISK_TAG = "_with-risk-images"
EP_NUMBER = re.compile(r"^ep(\d+)")
VERDICT = re.compile(r"^\s*(#{1,6}\s*)?(\*\*)?\s*(结论|verdict)", re.IGNORECASE)
HEADING = re.compile(r"^\s*#{1,6}\s")
MUSIC_NAME = re.compile(r"(music|bgm)", re.IGNORECASE)
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")
HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
FOUNDED = re.compile(r"^EST\.?\s*\d{4}$", re.IGNORECASE)   # 列表期 corner 全是 EST. YYYY → 按成立年份


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return ""


def _is_ai(licence: str) -> bool:
    return "ai-generated" in licence.lower()


def mp4_duration(path: Path) -> float | None:
    """`moov/mvhd` 的时长（秒）；读不出为 None。只走盒子头，不读媒体数据。"""
    try:
        with path.open("rb") as f:
            size = path.stat().st_size
            pos = 0
            while pos + 8 <= size:
                f.seek(pos)
                box, kind = struct.unpack(">I4s", f.read(8))
                head = 8
                if box == 1:
                    box, head = struct.unpack(">Q", f.read(8))[0], 16
                elif box == 0:
                    box = size - pos
                if box < head:
                    return None
                if kind == b"moov":
                    inner = pos + head
                    while inner + 8 <= pos + box:
                        f.seek(inner)
                        sub, sub_kind = struct.unpack(">I4s", f.read(8))
                        if sub < 8:
                            return None
                        if sub_kind == b"mvhd":
                            version = f.read(4)[0]
                            if version == 1:
                                f.read(16)
                                scale, dur = struct.unpack(">IQ", f.read(12))
                            else:
                                f.read(8)
                                scale, dur = struct.unpack(">II", f.read(8))
                            return round(dur / scale, 3) if scale else None
                        inner += sub
                    return None
                pos += box
    except (OSError, struct.error, IndexError):
        return None
    return None


def verdict_of(text: str) -> tuple[str, str]:
    """(最新结论一行, 从它所在小节起约 30 行)。没有结论段时摘录开头。"""
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if VERDICT.match(line)]
    if not hits:
        return "", "\n".join(lines[:EXCERPT_LINES])
    at = hits[-1]
    start = at
    for i in range(at, max(at - 6, -1), -1):
        if HEADING.match(lines[i]):
            start = i
            break
    headline = re.sub(r"[#*]", "", lines[at]).strip()
    return headline, "\n".join(lines[start:start + EXCERPT_LINES])


class RankPreviewReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.resolver = SafeResolver(repo_root)

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def read(self, rel: str) -> RankPreviewQdto:
        norm = rel.strip().replace("\\", "/").strip("/")
        prefix = f"{SERIES}/{EPISODES}/"
        is_series = norm == SERIES
        if not is_series and not (norm.startswith(prefix) and "/" not in norm[len(prefix):] and norm != prefix.rstrip("/")):
            raise InvalidDramaPathError(f"不是排行榜系列或期目录：{rel}")
        resolved = self.resolver.resolve(norm)
        if resolved is None:
            raise InvalidDramaPathError(f"不是排行榜系列或期目录：{rel}")
        if not resolved.is_dir():
            raise DramaNotFoundError(f"目录不存在：{rel}")
        if is_series:
            return RankPreviewQdto("series", series=self._series(resolved))
        return RankPreviewQdto("episode", episode=self._episode(resolved))

    def _series(self, series: Path) -> RankSeriesQdto:
        ep_root = series / EPISODES
        dirs = [d for d in ep_root.iterdir() if d.is_dir() and not d.is_symlink() and EP_NUMBER.match(d.name)] if ep_root.is_dir() else []
        cards = [self._episode(d).card for d in dirs]
        cards.sort(key=lambda c: (c.number if c.number is not None else 10**6, c.key))
        return RankSeriesQdto(self._rel(series), FOCUS, cards)

    def _json(self, path: Path) -> tuple[Any, str]:
        if not path.is_file() or path.is_symlink():
            return None, ""
        try:
            if path.stat().st_size > MAX_JSON:
                raise ValueError("文件过大")
            return json.loads(path.read_text(encoding="utf-8")), ""
        except (OSError, ValueError) as exc:
            return None, f"读不了 {path.name}：{exc}"

    def _doc(self, path: Path) -> RankDocQdto:
        if not path.is_file() or path.is_symlink():
            return RankDocQdto("")
        try:
            return RankDocQdto(self._rel(path), path.read_text(encoding="utf-8", errors="replace")[:MAX_TEXT])
        except OSError:
            return RankDocQdto(self._rel(path))

    def _file(self, ep: Path, declared: str) -> str:
        text = declared.replace("\\", "/")
        if not text or text.startswith("/") or ":" in text or ".." in text.split("/"):
            return ""
        path = ep / text
        return self._rel(path) if path.is_file() and not path.is_symlink() else ""

    def _videos(self, ep: Path) -> list[RankVideoQdto]:
        render = ep / "render"
        if not render.is_dir():
            return []
        out: list[tuple[RankVideoQdto, float]] = []
        for mp4 in render.glob("*.mp4"):
            if mp4.is_symlink() or not mp4.is_file():
                continue
            manifest, _ = self._json(mp4.with_suffix(".manifest.json"))
            manifest = manifest if isinstance(manifest, dict) else None
            music = self._music(mp4.name, manifest)
            moov = mp4_duration(mp4)          # 没有 moov：还在渲染或写坏了
            duration = manifest.get("duration_s") if manifest else None
            if not isinstance(duration, (int, float)) or isinstance(duration, bool):
                duration = moov
            risk = RISK_TAG in mp4.stem
            label = self._label(mp4.stem, risk, music) if moov is not None else f"{self._label(mp4.stem, risk, None)} · 未完成"
            out.append((RankVideoQdto(mp4.name, self._rel(mp4), label, risk, music,
                                      float(duration) if moov is not None and duration is not None else None, moov is not None),
                        mp4.stat().st_mtime))
        done = [v for v in out if v[0].complete]
        best = max(done, key=lambda v: (2 * bool(v[0].music) + v[0].risk, v[1]))[0] if done else None
        order = lambda v: (not v.name.endswith("_master.mp4"), not v.risk, v.name)  # noqa: E731
        return sorted((replace(v, recommended=v is best) for v, _ in out), key=order)

    @staticmethod
    def _music(name: str, manifest: dict[str, Any] | None) -> bool | None:
        if manifest is not None:
            inputs = manifest.get("inputs")
            if isinstance(inputs, dict) and inputs.get("music"):
                return True
            args = manifest.get("ffmpeg")
            if isinstance(args, list) and any(isinstance(a, str) and a.lower().endswith(AUDIO_EXTS) for a in args):
                return True
            return bool(MUSIC_NAME.search(name))
        return True if MUSIC_NAME.search(name) else None

    @staticmethod
    def _label(stem: str, risk: bool, music: bool | None) -> str:
        base = "风险图版" if risk else "默认母版" if stem.endswith("_master") else stem
        return base + (" · 配乐" if music else " · 无配乐" if music is False else "")

    def _image(self, ep: Path, declared: Any, ledger: dict[str, dict[str, Any]]) -> RankImageQdto | None:
        text = _text(declared)
        if not text:
            return None
        entry = ledger.get(text, {})
        licence = _text(entry.get("licence"))
        source = _text(entry.get("source_page")) or _text(entry.get("commons_page")) or _text(entry.get("source_url"))
        return RankImageQdto(self._file(ep, text), text, licence, _text(entry.get("author")), source, _is_ai(licence))

    def _person(self, ep: Path, raw: Any, ledger: dict[str, dict[str, Any]]) -> RankPersonQdto | None:
        if not isinstance(raw, dict) or not (_text(raw.get("name")) or _text(raw.get("image"))):
            return None
        return RankPersonQdto(_text(raw.get("name")), _text(raw.get("role")), self._image(ep, raw.get("image"), ledger),
                              _text(raw.get("image_risk")), _text(raw.get("credit")))

    def _item(self, ep: Path, raw: dict[str, Any], ledger: dict[str, dict[str, Any]], flags: Path) -> RankItemQdto:
        iso = _text(raw.get("country_iso2")).lower()
        flag = flags / f"{iso}.png" if re.fullmatch(r"[a-z]{2}(-[a-z]+)?", iso) else None
        rank = raw.get("rank")
        logo_bg = _text(raw.get("logo_bg"))
        return RankItemQdto(
            rank if isinstance(rank, int) and not isinstance(rank, bool) else 0, _text(raw.get("name")), _text(raw.get("subtitle")),
            iso.upper(), _text(raw.get("country_name")), self._rel(flag) if flag and flag.is_file() else "",
            _text(raw.get("value_display")), _text(raw.get("badge")),
            self._image(ep, raw.get("image"), ledger), self._image(ep, raw.get("image_alt"), ledger), _text(raw.get("image_risk")),
            _text(raw.get("corner")), self._image(ep, raw.get("logo"), ledger), logo_bg if HEX_COLOR.match(logo_bg) else "",
            self._person(ep, raw.get("person"), ledger), _text(raw.get("image_alt_credit")),
            _text(raw.get("secondary_display")), _text(raw.get("notes")))

    def _episode(self, ep: Path) -> RankEpisodeQdto:
        data, error = self._json(ep / "data.json")
        if data is not None and not isinstance(data, dict):
            data, error = None, "data.json 不是对象"
        data = data or {}
        assets, asset_error = self._json(ep / "assets.json")
        ledger = {_text(a.get("file")): a for a in assets if isinstance(a, dict)} if isinstance(assets, list) else {}
        flags = ep.parent.parent / FLAGS
        items = [self._item(ep, raw, ledger, flags) for raw in data.get("items") or [] if isinstance(raw, dict)]
        items.sort(key=lambda i: i.rank)
        # 契约 v1.3 `mode`：list 是不排名的列表，rank 只是出场位置，没有冠军（follow-up 321）
        is_list = _text(data.get("mode")).lower() == "list"
        insights = [RankInsightQdto(i.get("after_rank") if isinstance(i.get("after_rank"), int) else None, _text(i.get("text")))
                    for i in data.get("insights") or [] if isinstance(i, dict) and _text(i.get("text"))]
        videos = self._videos(ep)
        qc = self._doc(ep / "qc.md")
        verdict, excerpt = verdict_of(qc.text) if qc.text else ("", "")
        top = min((i.rank for i in items if i.rank > 0), default=None)
        thumb = ep / "render" / "thumbnail.png"
        main = next((v for v in videos if v.recommended), None)
        number = EP_NUMBER.match(ep.name)
        stats = RankImageStatsQdto(
            len(items), sum(1 for i in items if i.image and i.image.path),
            sum(1 for i in items if not (i.image and i.image.path)), sum(1 for i in items if i.image_risk),
            sum(1 for i in items if i.image_alt), sum(1 for i in items if (i.image and i.image.ai) or (i.image_alt and i.image_alt.ai)))
        musics = [v.music for v in videos]
        card = RankEpisodeCardQdto(
            ep.name, int(number.group(1)) if number else None, self._rel(ep), _text(data.get("title")), len(items),
            " / ".join(i.name for i in items if i.rank == top) if top is not None and not is_list else "",
            main.duration_s if main else None, self._rel(thumb) if thumb.is_file() else "", verdict,
            True if any(musics) else (False if musics and all(m is False for m in musics) else None),
            len(videos), stats, "；".join(e for e in (error, asset_error) if e),
            "list" if is_list else "rank", items[0].name if is_list and items else "", items[-1].name if is_list and items else "",
            "成立年份" if is_list and items and all(FOUNDED.match(i.corner) for i in items) else "")
        return RankEpisodeQdto(
            card, _text(data.get("kicker")), _text(data.get("theme")), _text(data.get("metric_label")),
            _text(data.get("period_label")), _text(data.get("source_line")), _text(data.get("scope_note")),
            videos, excerpt, qc, self._doc(ep / "publish.md"), self._doc(ep / "_build" / "handoff.md"), items, insights)
