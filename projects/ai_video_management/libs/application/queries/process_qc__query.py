from __future__ import annotations

import datetime as dt
import json
import tomllib
from dataclasses import asdict

from libs.application.dtos.process_qc__dto import ProcessQcDramaQdto, ProcessQcRepoQdto
from libs.common.drama_ref import drama_root_rel
from libs.common.process_qc import STAGE_ORDER, escape, escape_rate, real_defects
from libs.infrastructure.errors.process_qc__error import ProcessQcError
from libs.infrastructure.readers.process_qc__reader import ProcessQcReader

READ_ERRORS = (OSError, ValueError, KeyError, tomllib.TOMLDecodeError, json.JSONDecodeError)
WINDOW_DAYS = 7
RENDER_LIMIT = 40


class ProcessQcQuery:
    def __init__(self, reader: ProcessQcReader) -> None:
        self.reader = reader

    def repo(self) -> ProcessQcRepoQdto:
        try:
            today = dt.date.today()
            dramas = []
            for drama in self.reader.dramas():
                spec = drama.rsplit("/", 1)[-1]
                enabled = self.reader.has_registry(drama)
                defects = self.reader.defects(spec)
                dramas.append({"drama": drama, "spec": spec, "enabled": enabled,
                               "drama_checks": len(self.reader.drama_checks(drama)) if enabled else 0,
                               "defects": len(real_defects(defects)), "user_caught": sum(d.caught_by == "user" for d in defects),
                               "false_positives": sum(d.caught_by == "override" for d in defects),
                               "escape_rate": escape_rate(defects),
                               "renders_total": self.reader.renders(drama, 0)[1] if enabled else 0,
                               "followup": asdict(self.reader.followup_health(spec, WINDOW_DAYS, today))})
            return ProcessQcRepoQdto(list(STAGE_ORDER), [asdict(c) for c in self.reader.repo_checks()], dramas)
        except READ_ERRORS as exc:
            raise ProcessQcError("自检登记或日志不可读取", 503) from exc

    def drama(self, drama: str) -> ProcessQcDramaQdto:
        drama = drama.strip("/")
        if drama_root_rel(self.reader.root, drama.split("/")) != drama:
            raise ProcessQcError("不是剧目录")
        try:
            spec = drama.rsplit("/", 1)[-1]
            repo, local = self.reader.repo_checks(), self.reader.drama_checks(drama)
            dup = {c.id for c in repo} & {c.id for c in local}
            if dup:
                raise ProcessQcError(f"检查 id 在仓库级与剧级重复：{sorted(dup)}", 409)
            merged = {c.id: c for c in (*repo, *local)}
            defects = self.reader.defects(spec)
            escapes = []
            for d in defects:
                if d.caught_by != "user":
                    continue
                why, todo = escape(d, merged, self.reader.verdict(d.artifact, d.category))
                escapes.append({**asdict(d), "reason": why, "action": todo,
                                "level": merged[d.category].level if d.category in merged else "剧级（待新增）"})
            renders, total = self.reader.renders(drama, RENDER_LIMIT)
            return ProcessQcDramaQdto(drama, spec, self.reader.has_registry(drama), list(STAGE_ORDER),
                                      [asdict(c) for c in local], [asdict(c) for c in repo],
                                      [asdict(d) for d in defects], escapes, escape_rate(defects),
                                      [asdict(r) for r in renders], total,
                                      asdict(self.reader.followup_health(spec, WINDOW_DAYS, dt.date.today())))
        except READ_ERRORS as exc:
            raise ProcessQcError("自检登记或日志不可读取", 503) from exc
