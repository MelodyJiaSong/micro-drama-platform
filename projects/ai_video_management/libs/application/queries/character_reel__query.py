"""人物卡「样片与正片」（follow-up 286）：正片＝人物视频＋各技能最新正式条，样片＝各技能全部草稿，再加接进这个人物素材的剪辑成片。只读。"""
from __future__ import annotations

import re
from typing import Any

from libs.application.dtos.character_reel__dto import CharacterReelQdto, ReelClipQdto, ReelCutQdto, SkillReelQdto
from libs.common.scene_cut import CUT_STAGES
from libs.infrastructure.daos.character_reel__dao import SkillCardDao
from libs.infrastructure.readers.character_reel__reader import EPISODES, CharacterReelReader

STAMP_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})_")


def _num(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def clip(take: dict[str, Any], stage: str) -> ReelClipQdto | None:
    """ShotRendersReader 的一条生成 → 一条可播放的视频；目录里没有视频就不列。"""
    if not take["videos"]:
        return None
    gen = take["generation"]
    stamp = STAMP_RE.match(take["id"])
    made = str(gen.get("downloaded_at") or "") or (f"{stamp[1]}-{stamp[2]}-{stamp[3]}T{stamp[4]}:{stamp[5]}:{stamp[6]}" if stamp else "")
    return ReelClipQdto(take["id"], take["videos"][0], stage, str(gen.get("submit_id") or "")[:8], _num(gen.get("credits")), made,
                        _num(gen.get("duration_s")), str(gen.get("resolution") or ""), take["review_status"])


def _clips(takes: list[dict[str, Any]], stage: str) -> list[ReelClipQdto]:
    return [c for c in (clip(t, stage) for t in takes) if c is not None]


def skill(dao: SkillCardDao) -> SkillReelQdto:
    finals = _clips(dao.finals, "final")
    return SkillReelQdto(dao.key, dao.title, dao.path, dao.card, dao.icon, dao.peak, finals[0] if finals else None, finals,
                         _clips(dao.drafts, "draft"))


class CharacterReelQuery:
    def __init__(self, reader: CharacterReelReader) -> None:
        self.reader = reader

    def output(self, raw: dict[str, Any]) -> tuple[str, float | None]:
        """成片文件与时长：`output.file` / `output.duration`（集级拼接），或 `output.files.clean`（场剪辑）；只认同目录、实际存在的文件。"""
        out = _dict(raw.get("output"))
        clean = _dict(_dict(out.get("files")).get("clean"))
        name = out.get("file") or clean.get("path")
        duration = _num(out.get("duration")) or _num(out.get("duration_s")) or _num(clean.get("duration_s"))
        if not isinstance(name, str) or not name or "/" in name or "\\" in name or name.startswith("."):
            return "", duration
        rel = f"{raw['_dir']}/{name}"
        return (rel if self.reader.exists(rel) else ""), duration

    def cut(self, stage: str, raw: dict[str, Any]) -> ReelCutQdto:
        number = raw.get("version")
        version = number if isinstance(number, int) and not isinstance(number, bool) else raw["_file_version"]
        video, duration = self.output(raw) if "_error" not in raw else ("", None)
        return ReelCutQdto(version, stage, raw["_episode"], raw["_path"], video, duration, str(raw.get("note") or ""),
                           str(raw.get("status") or ""), str(raw.get("phase") or ""), str(raw.get("_error") or ""),
                           bool(raw.get("_own")))

    def read(self, path: str) -> CharacterReelQdto:
        dao = self.reader.read(path)
        turntable = ReelClipQdto(dao.turntable.rsplit("/", 1)[-1], dao.turntable, "turntable") if dao.turntable else None
        cuts = {stage: sorted((self.cut(stage, raw) for raw in dao.cuts.get(stage, [])), key=lambda c: (c.own, c.version, c.episode), reverse=True)
                for stage in CUT_STAGES}
        return CharacterReelQdto(dao.name, dao.path, turntable, [skill(s) for s in dao.skills], cuts,
                                 [dao.path, f"{dao.drama}/{EPISODES}"])
