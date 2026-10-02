# -*- coding: utf-8 -*-
"""整集通读章（follow-up 037 对白通读 · 038 冷眼观众）：「这套机制应该时刻检查所有 shot prompt，每当有任何修改」。

两道通读都由没写过这集的子代理做，读完改完各盖一枚章，记进 `4_剧本/episodes/{ep}/dialogue_review.toml`：
  · dialogue ＝ `ai_videos__对白通读`（带全剧上下文：对话接不接得上、母语口语、声口、称呼、信息边界）
  · viewer   ＝ `ai_videos__冷眼观众`（只拿观众看得到、听得到的：他们在做什么、为什么、哪里看不懂）
指纹 ＝ 剧本每镜正文（台词 + 画面动作 + 情绪，去掉备注）＋ 生成器每镜的情节与动作——shot prompt 里跟剧情有关的全部文字。
任何一处再改，两枚章都对不上，生成器 build 时即 blocker：两道都重读、重盖，才能出 prompt。

    python tools/gen_shots_{剧}_{ep}.py --dialogue-stamp "对白通读 · 审稿人 · 备注"
    python tools/gen_shots_{剧}_{ep}.py --viewer-stamp   "冷眼观众 · 审稿人 · 备注"
"""
from __future__ import annotations

import datetime
import hashlib
import re
import tomllib
from pathlib import Path

import script_tools

STAMP = "dialogue_review.toml"
KINDS = {                                   # 章名 → (toml 节名, 中文名, 该跑的 skill)
    "dialogue": ("review", "对白通读", "ai_videos__对白通读"),
    "viewer": ("viewer", "冷眼观众", "ai_videos__冷眼观众"),
}
_NOTE = re.compile(r"^- 备注:.*$", re.M)


def fingerprint(script_md: Path, gen_parts: dict[str, list[str]]) -> tuple[str, int]:
    """(sha256 前 12 位, 台词句数)。gen_parts：镜号 → 生成器里进 prompt 的情节 / 动作文字。"""
    shots, _ = script_tools.parse(str(script_md))
    h = hashlib.sha256()
    n = 0
    for s in shots:
        h.update(("\x00%s\x00" % s.key).encode("utf-8"))
        h.update(_NOTE.sub("", s.body).encode("utf-8"))
        for part in gen_parts.get(s.key, []):
            h.update(("\x01" + part).encode("utf-8"))
        n += len(s.lines)
    return h.hexdigest()[:12], n


def _load(ep_dir: Path) -> dict:
    f = ep_dir / STAMP
    return tomllib.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}


def status(ep_dir: Path, fp: str, kind: str = "dialogue") -> tuple[bool, str]:
    sec, name, _skill = KINDS[kind]
    rev = _load(ep_dir).get(sec)
    if not rev:
        return False, "本集还没过%s" % name
    if rev.get("fingerprint") != fp:
        return False, "%s之后（%s）台词 / 动作 / 情节改过（章上是 %s，现在是 %s）" % (name, rev.get("date", "?"), rev.get("fingerprint"), fp)
    return True, "%s通过 · %s" % (name, rev.get("date", "?"))


def gate(ep_dir: Path, fp: str) -> list[str]:
    out = []
    for kind, (_sec, name, skill) in KINDS.items():
        ok, why = status(ep_dir, fp, kind)
        if not ok:
            out.append("%s：%s——跑 %s（整集），改完再 --%s-stamp（follow-up 037 / 038）" % (name, why, skill, kind))
    return out


def stamp(ep_dir: Path, fp: str, n_lines: int, note: str, kind: str = "dialogue") -> None:
    old = _load(ep_dir)
    hist = list(old.get("history", []))
    sec = KINDS[kind][0]
    if old.get(sec):
        hist.append({"kind": kind, **old[sec]})
    today = datetime.date.today().isoformat()
    cur = {s: old[s] for s, _n, _k in KINDS.values() if old.get(s)}
    cur[sec] = {"fingerprint": fp, "lines": n_lines, "date": today, "note": note.replace('"', "'")}

    def row(k: str, v) -> str:
        return '%s = %s' % (k, ('"%s"' % v) if isinstance(v, str) else v)

    out = ["# 整集通读章（tools/dialogue_review.py）：本集台词 + 画面动作 + 生成器情节 / 动作的 sha256 前 12 位。",
           "# review ＝ 对白通读，viewer ＝ 冷眼观众；生成器 build 时两枚都要对得上——任何一处改了，两道都得重读、重盖。"]
    for s, _n, _k in KINDS.values():
        if s in cur:
            out += ["", "[%s]" % s] + [row(k, v) for k, v in cur[s].items()]
    for h in hist[-30:]:
        out += ["", "[[history]]"] + [row(k, v) for k, v in h.items()]
    (ep_dir / STAMP).write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
