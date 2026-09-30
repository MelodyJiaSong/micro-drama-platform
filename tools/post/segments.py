# -*- coding: utf-8 -*-
"""成片时间线 v2（{视频名}.segments.json）：一段＝一个剪辑事件，带 take 与源片入 / 出点；旧读者要的 shot / start_s / end_s / dur_s 照留。

v1（pc.write_segments）只有镜与成片起止；v2 多 event / take（sha256 前 pc.TAKE_ID_LEN 位）/ src_in / src_out（源秒）/
gain_db（对白配平增益）。源片 t 秒在成片里的时刻＝start + (t − src_in)。
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

VERSION = 2
KEYS = ("shot", "start_s", "dur_s", "event", "take", "src_in", "src_out", "gain_db")
WHOLE_ID = "s%02d"          # 没有 edl 的整镜顺接：第 i 镜的事件号（finish_ep 写，qc 读 v1 segments 时补）


@dataclass(frozen=True)
class Part:
    event: str
    shot: str
    take: str
    src_in: float
    src_out: float
    start: float
    dur: float
    gain_db: float

    @property
    def end(self) -> float:
        return self.start + self.dur

    def at(self, t: float) -> float:
        """源片 t 秒 → 成片秒。"""
        return self.start + t - self.src_in


def write(path: Path, parts: list[Part]) -> None:
    rows = [{"shot": p.shot, "start_s": round(p.start, 3), "end_s": round(p.end, 3), "dur_s": round(p.dur, 3),
             "event": p.event, "take": p.take, "src_in": round(p.src_in, 6), "src_out": round(p.src_out, 6),
             "gain_db": round(p.gain_db, 2)} for p in parts]
    total = parts[-1].end if parts else 0.0
    part = path.with_name(path.name + ".part")
    part.write_text(json.dumps({"version": VERSION, "approx": False, "total_s": round(total, 3), "segments": rows},
                               ensure_ascii=False, indent=2), encoding="utf-8")
    part.replace(path)


def read_parts(path: Path) -> list[Part] | None:
    """v2 → 各段；不是 v2（旧的 v1）→ None，调用方走 pc.read_segments。"""
    j = json.loads(path.read_text(encoding="utf-8"))
    if j.get("version") != VERSION:
        return None
    bad = [f"第 {i} 段缺 {[k for k in KEYS if k not in s]}" for i, s in enumerate(j["segments"], 1) if not set(KEYS) <= set(s)]
    if bad:
        raise SystemExit(f"{path.name} 标了 version {VERSION} 却不全：{'；'.join(bad)}——重跑 finish_ep（或 --proxy）重写这份 segments")
    return [Part(str(s["event"]), str(s["shot"]), str(s["take"]), float(s["src_in"]), float(s["src_out"]),
                 float(s["start_s"]), float(s["dur_s"]), float(s["gain_db"])) for s in j["segments"]]
