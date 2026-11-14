"""英雄 demo 定版标记（follow-up 315）：哪些人物的 demo 已定版、定版是哪一版、发布文案对不对得上。只读。

人物目录 `characters/[{分组}/]{卡}/demo/edit/final/cut_v{N}.json`：`status`（没有取 `phase`）以「定版」或「锁片」
开头算定版，取版本号最大的一条。成片是 cut 的 `output.file`（没有取 `ep01_final_v{N}.mp4`）。发布文案
`demo/publish.md` 开头（前 20 行）第一处 `edit/final/*.mp4` 就是它写的成片，与定版成片同名为 ok，否则 stale。
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from libs.application.dtos.demo_status__dto import DemoStatusQdto
from libs.common import drama_layout, drama_ref, series_shared

CUT_RE = re.compile(r"^cut_v(\d+)\.json$")
FINAL_PREFIXES = ("定版", "锁片")
PUBLISH_VIDEO_RE = re.compile(r"edit/final/([^`\s)]+\.mp4)")
PUBLISH_HEAD_LINES = 20


def is_final(status: str) -> bool:
    return status.strip().startswith(FINAL_PREFIXES)


def _status(data: dict[str, Any]) -> str:
    return str(data.get("status") or data.get("phase") or "")


class DemoStatusReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def read(self) -> list[DemoStatusQdto]:
        out: list[DemoStatusQdto] = []
        seen: set[Path] = set()
        for drama in drama_ref.drama_dirs(self.root):
            for hero in series_shared.asset_dirs(drama, drama_layout.characters_dir):
                if hero in seen:
                    continue
                seen.add(hero)
                status = self.hero(hero)
                if status is not None:
                    out.append(status)
        return sorted(out, key=lambda s: s.hero)

    @staticmethod
    def _cuts(final_dir: Path) -> list[tuple[int, Path, dict[str, Any]]]:
        cuts: list[tuple[int, Path, dict[str, Any]]] = []
        for entry in final_dir.iterdir():
            match = CUT_RE.match(entry.name)
            if not match or not entry.is_file() or entry.is_symlink():
                continue
            try:
                data = json.loads(entry.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(data, dict):
                cuts.append((int(match.group(1)), entry, data))
        return cuts

    @staticmethod
    def _publish_video(publish: Path) -> str:
        try:
            with publish.open(encoding="utf-8", errors="replace") as fh:
                head = "".join(next(fh, "") for _ in range(PUBLISH_HEAD_LINES))
        except OSError:
            return ""
        found = PUBLISH_VIDEO_RE.search(head)
        return found.group(1) if found else ""

    def hero(self, hero: Path) -> DemoStatusQdto | None:
        final_dir = hero / "demo" / "edit" / "final"
        if not final_dir.is_dir() or final_dir.is_symlink():
            return None
        cuts = self._cuts(final_dir)
        finals = [c for c in cuts if is_final(_status(c[2]))]
        if not finals:
            return None
        version, cut, data = max(finals, key=lambda c: c[0])
        output = data.get("output")
        name = output["file"] if isinstance(output, dict) and isinstance(output.get("file"), str) else f"ep01_final_v{version}.mp4"
        video = final_dir / name
        publish = hero / "demo" / "publish.md"
        has_publish = publish.is_file() and not publish.is_symlink()
        publish_video = self._publish_video(publish) if has_publish else ""
        state = "missing" if not has_publish else ("ok" if publish_video == name else "stale")
        return DemoStatusQdto(
            hero=self._rel(hero), folder=hero.name, version=version, cut=self._rel(cut),
            video=self._rel(video) if video.is_file() else "", status=_status(data),
            newer=sorted(v for v, _, _ in cuts if v > version),
            publish=self._rel(publish) if has_publish else "", publish_video=publish_video, publish_state=state,
        )
