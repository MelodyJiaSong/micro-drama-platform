"""剪辑模块（follow-up 269）：一集各场的草稿剪辑与正片剪辑，每版的时间线与成片。只读。"""
from __future__ import annotations

from typing import Any

from libs.application.dtos.scene_cut__dto import (CutEventQdto, CutVersionQdto, EpisodeCutsQdto, EpisodeJoinQdto, GalleryEntryQdto,
                                                  GalleryQdto, JoinSegmentQdto, JoinTransitionQdto, SceneCutsQdto)
from libs.common.scene_cut import CUT_STAGES, EDGES, TRANSITIONS
from libs.domain.errors.scene_cut__error import SceneCutError
from libs.infrastructure.readers.scene_cut__reader import SceneCutReader


def _num(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _texts(value: Any) -> list[str]:
    return [str(item) for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


class SceneCutQuery:
    def __init__(self, reader: SceneCutReader) -> None:
        self.reader = reader

    @staticmethod
    def events(raw: Any) -> list[CutEventQdto]:
        """按播放顺序累加出每段在成片里的起点。"""
        out, t = [], 0.0
        for item in raw if isinstance(raw, list) else []:
            if not isinstance(item, dict):
                continue
            shot, reason, notes = str(item.get("shot", "")), str(item.get("reason", "")), _texts(item.get("notes"))
            if item.get("placeholder"):
                length = _num(item.get("duration")) or 0.0
                out.append(CutEventQdto(shot, round(t, 3), length, True, reason=reason, notes=notes, text=_texts(item.get("text"))))
            else:
                a, b = _num(item.get("in")) or 0.0, _num(item.get("out")) or 0.0
                ai, ao = _num(item.get("audio_in")), _num(item.get("audio_out"))
                decoupled = (ai is not None and ai != a) or (ao is not None and ao != b)
                length = max(0.0, b - a)
                out.append(CutEventQdto(shot, round(t, 3), round(length, 3), False, str(item.get("take", "")), a, b,
                                        (a if ai is None else ai) if decoupled else None,
                                        (b if ao is None else ao) if decoupled else None, reason, notes))
            t += length
        return out

    def media(self, folder: str, files: dict[str, Any], kind: str) -> str:
        """output.files 里记的是同目录的文件名；文件不在（没渲染、被删）就当没有。"""
        name = _dict(files.get(kind)).get("path")
        if not isinstance(name, str) or not name or "/" in name or "\\" in name or name.startswith("."):
            return ""
        rel = f"{folder}/{name}"
        return rel if self.reader.exists(rel) else ""

    def version(self, stage: str, raw: dict[str, Any]) -> CutVersionQdto:
        number = raw["version"] if isinstance(raw.get("version"), int) and not isinstance(raw.get("version"), bool) else raw["_file_version"]
        if raw.get("_error"):
            return CutVersionQdto(number, stage, "", "", raw["_path"], error=raw["_error"])
        output = _dict(raw.get("output"))
        files = _dict(output.get("files"))
        events = self.events(raw.get("events"))
        error = "" if raw.get("stage") == stage else f"stage 字段（{raw.get('stage')}）与所在目录（{stage}）不一致"
        base = raw.get("base_version")
        return CutVersionQdto(
            number, stage, str(raw.get("phase", "")), str(raw.get("status", "")), raw["_path"],
            raw["approved_by"] if isinstance(raw.get("approved_by"), str) else None, str(raw.get("made_by", "")),
            base if isinstance(base, int) and not isinstance(base, bool) else None,
            self.media(raw["_dir"], files, "clean"), self.media(raw["_dir"], files, "label"),
            _num(_dict(files.get("clean")).get("duration_s")) or round(sum(e.duration for e in events), 3),
            str(output.get("rendered_at", "")),
            sum(1 for e in events if not e.placeholder), sum(1 for e in events if e.placeholder), events,
            _texts(raw.get("notes")), [v for v in raw.get("intentional_violations", []) if isinstance(v, dict)]
            if isinstance(raw.get("intentional_violations"), list) else [], error)

    def joined(self, stage: str, raw: dict[str, Any], scene_cuts: dict[str, dict[int, CutVersionQdto]]) -> EpisodeJoinQdto:
        """集级剪辑决定 → 各场在成片里的位置、转场（含中文名与时刻）、独立审稿结论（只认绑的是这版成片 sha 的）。"""
        number = raw["version"] if isinstance(raw.get("version"), int) and not isinstance(raw.get("version"), bool) else raw["_file_version"]
        if raw.get("_error"):
            return EpisodeJoinQdto(number, stage, "", "", raw["_path"], error=raw["_error"])
        output = _dict(raw.get("output"))
        trans = [t for t in raw.get("transitions", []) if isinstance(t, dict)] if isinstance(raw.get("transitions"), list) else []
        segments, transitions, t, missing = [], [], 0.0, []
        for k, item in enumerate(s for s in raw.get("scenes", []) if isinstance(s, dict)):
            sid, cv = str(item.get("scene", "")), item.get("cut_version")
            sc = scene_cuts.get(sid, {}).get(cv) if isinstance(cv, int) else None
            length = sc.duration if sc else 0.0
            if not sc:
                missing.append(f"{sid} v{cv}")
            if k and k - 1 < len(trans):
                tr = trans[k - 1]
                kind = str(tr.get("type", ""))
                name, xfade = TRANSITIONS.get(kind, (kind, None))[:2]
                overlap = (_num(tr.get("duration")) or 0.0) if xfade else 0.0
                t -= overlap
                audio = _dict(tr.get("audio"))
                transitions.append(JoinTransitionQdto(str(tr.get("from", "")), str(tr.get("to", "")), kind, name, overlap, round(t, 3),
                                                      _num(audio.get("j")), _num(audio.get("l")), str(tr.get("reason", ""))))
            segments.append(JoinSegmentQdto(sid, cv if isinstance(cv, int) else 0, round(t, 3), length))
            t += length
        review = _dict(raw.get("independent_review"))
        stale = bool(review) and review.get("sha256") != output.get("sha256")
        name = output.get("path")
        video = ""
        if isinstance(name, str) and name and "/" not in name and "\\" not in name and not name.startswith("."):
            video = self.media(raw["_dir"], {"clean": {"path": name}}, "clean")
        edge = lambda key: EDGES.get(str(_dict(raw.get(key)).get("type", "cut")), ("?",))[0]
        base = raw.get("base_version")
        error = "" if raw.get("stage") == stage else f"stage 字段（{raw.get('stage')}）与所在目录（{stage}）不一致"
        if missing:
            error = (error + "；" if error else "") + "找不到场剪辑：" + "、".join(missing)
        return EpisodeJoinQdto(
            number, stage, str(raw.get("phase", "")), str(raw.get("status", "")), raw["_path"],
            raw["approved_by"] if isinstance(raw.get("approved_by"), str) else None,
            base if isinstance(base, int) and not isinstance(base, bool) else None,
            video, _num(output.get("duration_s")) or round(t, 3), str(output.get("rendered_at", "")), edge("head"), edge("tail"),
            segments, transitions, "" if stale else str(review.get("verdict", "")), stale,
            [] if stale else _texts(review.get("open_items")), _texts(raw.get("changes_from_base")), str(raw.get("note", "")), error)

    @staticmethod
    def gallery(video: str, a: str, b: str, index: str) -> GalleryQdto:
        entries = []
        for line in index.splitlines():
            head, _, label = line.strip().partition("s ")
            try:
                entries.append(GalleryEntryQdto(float(head), label.strip()))
            except ValueError:
                continue
        return GalleryQdto(a, b, video, entries)

    def read(self, episode_path: str) -> EpisodeCutsQdto:
        try:
            path, scenes = self.reader.scenes(episode_path)
        except FileNotFoundError as exc:
            raise SceneCutError(str(exc), 404) from exc
        except ValueError as exc:
            raise SceneCutError("模块文件格式无效，请检查JSON内容") from exc
        out = []
        for scene in scenes:
            sid = str(scene.get("id", ""))
            found = self.reader.cuts(path, sid)
            versions = {stage: sorted((self.version(stage, raw) for raw in found[stage]), key=lambda v: -v.version)
                        for stage in CUT_STAGES}
            out.append(SceneCutsQdto(sid, f"{scene.get('location', '')} · {scene.get('time', '')}", versions["draft"], versions["final"]))
        joined, galleries = {}, {}
        found = self.reader.cuts(path, None)
        for stage in CUT_STAGES:
            by_scene = {s.scene: {v.version: v for v in getattr(s, stage)} for s in out}
            joined[stage] = sorted((self.joined(stage, raw, by_scene) for raw in found[stage]), key=lambda v: -v.version)
            galleries[stage] = [self.gallery(*item) for item in self.reader.galleries(path, stage)]
        return EpisodeCutsQdto(path, out, joined, galleries)
