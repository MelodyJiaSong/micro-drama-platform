"""只读：自检登记表（仓库级 / 剧级）、缺陷记录、出片 qc.json、follow-up 日志健康度。"""
from __future__ import annotations

import datetime as dt
import json
import re
import tomllib
from pathlib import Path

from libs.common.drama_ref import drama_dirs
from libs.common.process_qc import DRAMA_REGISTRY_NAME, MAX_BYTES, REPO_REGISTRY, SPEC_ROOT
from libs.infrastructure.daos.process_qc__dao import FollowupHealthDao, QcCheckDao, QcDefectDao, QcRenderDao

FU_HEAD = re.compile(r"^## (\d+) — (\d{4}-\d\d-\d\d)", re.M)
CL_HEAD = re.compile(r"^## .*$", re.M)
CL_CANON = re.compile(r"^## Follow-up (\d{3,}) — [^\n]*$", re.M)


class ProcessQcReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root.resolve()

    def _path(self, rel: str) -> Path:
        candidate = self.root / rel
        for parent in (candidate, *candidate.parents):
            if parent == self.root:
                break
            if parent.is_symlink():
                raise ValueError("linked path refused")
        if self.root not in candidate.resolve().parents:
            raise ValueError("path outside repo")
        return candidate

    def _text(self, rel: str) -> str | None:
        p = self._path(rel)
        if not p.is_file():
            return None
        with p.open("rb") as fh:
            data = fh.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError(f"{rel} exceeds read limit")
        return data.decode("utf-8-sig")

    def _checks(self, rel: str, level: str) -> list[QcCheckDao]:
        text = self._text(rel)
        if text is None:
            return []
        return [QcCheckDao(c["id"], c["stage"], c["kind"], bool(c.get("gate")), bool(c.get("auto")), level,
                           c.get("when", ""), c.get("desc", ""), c.get("how", ""), c.get("basis", ""),
                           tuple(c.get("sources", [])), c.get("perspective", "director" if c["kind"] == "review" else ""))
                for c in tomllib.loads(text).get("check", [])]

    def repo_checks(self) -> list[QcCheckDao]:
        return self._checks(REPO_REGISTRY, "仓库级")

    def drama_checks(self, drama: str) -> list[QcCheckDao]:
        return self._checks(f"{drama}/{DRAMA_REGISTRY_NAME}", "剧级")

    def has_registry(self, drama: str) -> bool:
        return self._path(f"{drama}/{DRAMA_REGISTRY_NAME}").is_file()

    def dramas(self) -> list[str]:
        return [p.relative_to(self.root).as_posix() for p in drama_dirs(self.root)]

    def defects(self, spec: str) -> list[QcDefectDao]:
        text = self._text(f"{SPEC_ROOT}/{spec}/defects.jsonl") or ""
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
        return [QcDefectDao(r.get("ts", ""), r.get("category", ""), r.get("caught_by", ""), r.get("artifact", ""),
                            str(r.get("followup", "")), r.get("note", "")) for r in rows]

    def renders(self, drama: str, limit: int) -> tuple[list[QcRenderDao], int]:
        base = self._path(drama)
        found = sorted((p for p in base.glob("**/renders/*/qc.json") if base in p.resolve().parents),
                       key=lambda p: p.parent.name, reverse=True)
        out = []
        for p in found[:limit]:
            qc = json.loads(p.read_text(encoding="utf-8"))
            out.append(QcRenderDao(p.parent.relative_to(self.root).as_posix(), qc.get("artifact", ""),
                                   {k: v.get("verdict", "") for k, v in qc.get("checks", {}).items()}))
        return out, len(found)

    def verdict(self, artifact: str, check_id: str) -> str | None:
        if not artifact:
            return None
        text = self._text(str(Path(artifact).parent / "qc.json"))
        return json.loads(text).get("checks", {}).get(check_id, {}).get("verdict") if text else None

    def followup_health(self, spec: str, days: int, today: dt.date) -> FollowupHealthDao:
        since = (today - dt.timedelta(days=days)).isoformat()
        heads: list[tuple[int, str]] = []
        fu_dir = self._path(f"{SPEC_ROOT}/{spec}/user_input/follow_ups")
        for f in sorted(fu_dir.glob("*.md")) if fu_dir.is_dir() else []:
            heads += [(int(n), d) for n, d in FU_HEAD.findall(self._text(f.relative_to(self.root).as_posix()) or "")]
        cl = self._text(f"{SPEC_ROOT}/{spec}/changelog.md") or ""
        covered: set[int] = set()
        for h in CL_HEAD.findall(cl):
            if "follow" in h.lower():
                for a, b in re.findall(r"(\d{3})\s*[–\-~]\s*(\d{3})", h):
                    covered.update(range(int(a), int(b) + 1))
                covered.update(int(x) for x in re.findall(r"(?<!\d)(\d{3})(?!\d)", re.sub(r"\d{4}-\d\d-\d\d\S*", "", h)))
        window = [(n, d) for n, d in heads if d >= since]
        counts: dict[int, int] = {}
        for n, _ in heads:
            counts[n] = counts.get(n, 0) + 1
        pending = sum("（待补" in body for body in re.split(r"(?=^## )", cl, flags=re.M) if CL_CANON.match(body))
        return FollowupHealthDao(days, len(window), sum(n in covered for n, _ in window),
                                 tuple(sorted({n for n, _ in window if counts[n] > 1})), pending,
                                 max((n for n, _ in heads), default=0))
