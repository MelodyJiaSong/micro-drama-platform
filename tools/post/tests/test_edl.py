# -*- coding: utf-8 -*-
"""edl.py 自测（纯 assert 脚本）：python tools/post/tests/test_edl.py

在系统临时目录搭一集假剧：3 镜各 10 s，take 是固定种子的随机字节（sha 现算），对齐缓存按 spec §3 的 JSON 写
（speech 用 align.speech_spans 并），shot md 只写 edl 读的字段；不碰真剧、不跑模型、不调 ffmpeg，跑完删掉。
1. 恒等 edl：锚点解析成整镜、plan.json 取整到帧、verify 一条不报；init 已有 edl 拒绝、--force 覆盖、接着已批准版本编号。
2. spec §5 的 10 个故意埋错：切在词中、take sha 不符、base_version 旧、flash 超长、flash 超个数、事件过短、删半句
   → verify 报对应的 V 号且只报它；锚点不存在、in ≥ out、fps 不符 → verify 报错停下并写明事件与锚点（spec §4 的 raise）。
3. 其余各项各一例：V1 审片结论（--proxy-ok 降为警告；render_review 没有 verdict_ok 也不放行；旧 take 没缓存）、
   V3、V4（含整镜相接的承接缝）、V6（含剧本改过没重出片的近似）、V7、V8、V9、V10 记账。
4. line: / cut: 锚点的 basis：缺了、配在 start / end 上都报错；md 改了台词、align 重算后编号挪了，按旧 basis 解析报错停下。
   end 取缓存的 frames（CFR 帧数，比容器时长 × FPS 多一帧的 VFR 片不丢末帧）。
5. candidates 的可切区间离词 ≥ WORD_MARGIN；CLI（命令放前放后都认）退出码跟 verify 一致。
script_tools 只认仓库里的 script.toml（_config 以 script_tools.REPO 为界），所以把 script_tools.REPO 指到临时目录，
让 V5–V7 读得到假剧的 [episode] / [scenery]。
"""
from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

POST = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POST))
import post_common as pc  # noqa: E402
import align  # noqa: E402
import edl  # noqa: E402
import render_review  # noqa: E402
import script_tools  # noqa: E402
import subs  # noqa: E402

EP = "ep01"
DUR = 10.0
Words = tuple[tuple[str, float, float], ...]
FakeLine = tuple[str, str, str, tuple[float, float], Words | None]     # （人, 类型, 句子, 计划窗, 词；None＝画外 / 独白）


@dataclass(frozen=True)
class FakeShot:
    key: str
    jb: str
    mood: str
    planned: tuple[float, ...]
    detected: tuple[float, ...]
    lines: tuple[FakeLine, ...]


SHOTS: dict[str, FakeShot] = {
    "shot01": FakeShot("S01", "远景0.12 → 中景0.6（机位 `S1·远` → `S1·中`）", "开阔", (6.8,), (6.8,), (
        ("Aaron", "正常台词", "Hello there friend.", (5.0, 7.0), (("Hello", 5.2, 5.5), ("there", 5.6, 5.9), ("friend.", 6.0, 6.4))),
        ("Duke", "正常台词", "We go north now.", (7.0, 9.0),
         (("We", 7.0, 7.2), ("go", 7.25, 7.4), ("north", 7.5, 7.8), ("now.", 8.3, 8.6))))),
    "shot02": FakeShot("S02", "远景0.15 → 近景0.8（机位 `S2·远` → `S2·近`）", "好笑", (5.0,), (5.04,), (
        ("Eagan", "正常台词", "I hate those wolves.", (1.0, 3.0),
         (("I", 1.0, 1.2), ("hate", 1.25, 1.5), ("those", 1.55, 1.8), ("wolves.", 1.85, 2.3))),
        ("Eagan", "正常台词", "But I like steaks.", (6.0, 8.0),
         (("But", 6.0, 6.2), ("I", 6.25, 6.3), ("like", 6.35, 6.6), ("steaks.", 6.65, 7.1))),
        ("Aaron", "内心独白", "I should run.", (8.2, 9.4), None))),
    "shot03": FakeShot("S03", "远景0.12 → 中景0.5（机位 `S3·远` → `S3·中`）", "安静", (), (), (
        ("Duke", "正常台词", "Dad's boots are fine.", (0.5, 2.5),
         (("Dad's", 0.6, 0.9), ("boots", 0.95, 1.3), ("are", 1.35, 1.5), ("fine.", 1.55, 1.9))),
        ("Aaron", "正常台词", "Thank you.", (4.0, 6.0), (("Thank", 4.2, 4.5), ("you.", 4.55, 4.9))),
        ("Aaron", "正常台词", "Let's go.", (7.5, 9.0), (("Let's", 7.6, 7.9), ("go.", 7.95, 8.3))))),
}
SCRIPT_TOML = """[episode]
min_s = 20
max_s = 40

[scenery]
new_zone_min_s = 6
new_bg_min_s = 3
idle_max_s = 4
post_trim_zone_s = 4
post_trim_bg_s = 2
"""
GOALS_TOML = """[ledger]
breathers = []

[[goal]]
id = "north"
who = "杜克"
what = "往北走"
why = "北边有事"
stated = ["S01", "Hello there friend"]
resolved = ["S03", "Thank you"]
cues = ["north"]

[[skill]]
who = "杜克"
what = "举盾"
used = ["S02", "杜克举盾"]
"""


def script_text(s01_dur: str = "10", s01_beat: str = "，2.5s 他抬头", s01_win: str = "5–7") -> str:
    return f"""# EP01 — 假剧

> **本集**：S01–S03（3 镜）｜ **30s**

### 镜 S01
- 时长: {s01_dur}s
- 场景: `bg1` 草地（bg1-1 草地）
- 场景展示: 【0–5s】远景推近：一片草地。展示的是：开阔。
- 画面动作: 【0–5s】亚伦走过草地{s01_beat}。
  【5–10s】两人说话。
- 台词:
  - [对白] Aaron: "Hello there friend."　*(【{s01_win}s】)*
  - [对白] Duke: "We go north now."　*(【7–9s】)*
- 情绪氛围: 开阔

### 镜 S02
- 时长: 10s
- 场景: `bg1` 草地（bg1-2 林缘）
- 画面动作: 【0–5s】狼扑上来，3s 杜克举盾。
  【5–10s】伊根收刀，8s 他转身。
- 台词:
  - [对白] Eagan: "I hate those wolves."　*(【1–3s】)*
  - [对白] Eagan: "But I like steaks."　*(【6–8s】)*
  - [OS] Aaron: "I should run."　*(【8.2–9.4s】内心独白)*
- 情绪氛围: 好笑

### 镜 S03
- 时长: 10s
- 场景: `bg2` 溪边（bg2-1 溪边）
- 场景展示: 【0–3s】溪边：一条小溪。展示的是：安静。
- 画面动作: 【0–3s】溪水流过。
  【3–10s】两人道别，5.5s 亚伦点头。
- 台词:
  - [对白] Duke: "Dad's boots are fine."　*(【0.5–2.5s】)*
  - [对白] Aaron: "Thank you."　*(【4–6s】)*
  - [对白] Aaron: "Let's go."　*(【7.5–9s】)*
- 情绪氛围: 安静
"""


@dataclass(frozen=True)
class Fake:
    root: Path
    drama: Path
    epd: Path
    sha: dict[str, str]

    def take(self, shot: str) -> str:
        return self.sha[shot][:12]

    @property
    def script(self) -> Path:
        return edl.script_md(self.drama, EP)


def align_json(shot: str, sha: str, fs: FakeShot) -> dict:
    recs = []
    for i, (who, kind, text, win, words) in enumerate(fs.lines, 1):
        rec: dict = {"idx": i, "speaker": who, "kind": kind, "text": text, "planned": list(win)}
        if words is None:
            rec |= {"start": win[0], "end": win[1], "conf": None, "words": [], "status": align.OFFSCREEN}
        else:
            rec |= {"start": words[0][1], "end": words[-1][2], "conf": 0.9, "status": align.OK,
                    "words": [{"w": w, "s": s, "e": e, "p": 0.9} for w, s, e in words]}
        recs.append(rec)
    return {"version": align.VERSION, "shot": shot, "take": f"shots/{shot}/{shot}.mp4", "take_sha256": sha,
            "model": align.MODEL, "duration": DUR, "frames": round(DUR * pc.FPS), "lines": recs,
            "asr": {"text": " ".join(ln[2] for ln in fs.lines if ln[4] is not None), "wer": 0.0},
            "speech": align.speech_spans(recs), "cuts": {"planned": list(fs.planned), "detected": list(fs.detected)}}


def shot_md_text(shot: str, fs: FakeShot) -> str:
    n = shot[-2:]
    return (f"---\nepisode: {EP}\nshot: {n}\nscript: {fs.key}\ntitle: 假镜{n}\nseam: 硬切\n---\n\n"
            f"# {EP} · {shot}《假镜{n}》\n\n## Shot context\n\n- **景别档**: {fs.jb}\n- **情绪目的**: {fs.mood}\n")


def write_align(epd: Path, shot: str, sha: str) -> None:
    p = edl.align_path(epd, shot, sha)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(align_json(shot, sha, SHOTS[shot]), ensure_ascii=False, indent=1), encoding="utf-8")


def write_verdict(epd: Path, shot: str, sha: str) -> Path:
    d = epd / "shots" / shot / "renders" / "review" / f"{shot}.{sha[:render_review.SHA_KEY]}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "verdict.md").write_text(f"通过\n{render_review.SHA_HEAD}: {sha}\n", encoding="utf-8")
    return d / "verdict.md"


def build(root: Path) -> Fake:
    drama = root / "fake_drama"
    epd = drama / "5_6_分镜与prompt" / "episodes" / EP
    (drama / "4_剧本").mkdir(parents=True)
    (drama / "4_剧本" / "script.toml").write_text(SCRIPT_TOML, encoding="utf-8")
    for bg in ("bg1_meadow", "bg2_brook"):
        d = drama / "2_世界观人设" / "scenes" / "zoneA" / bg
        d.mkdir(parents=True)
        (d / f"{bg}.md").write_text(f"# {bg}\n", encoding="utf-8")
    sha: dict[str, str] = {}
    for i, (shot, fs) in enumerate(SHOTS.items(), 1):
        d = epd / "shots" / shot
        d.mkdir(parents=True)
        (d / f"{shot}.md").write_text(shot_md_text(shot, fs), encoding="utf-8")
        (d / f"{shot}.mp4").write_bytes(random.Random(i).randbytes(4096))
        sha[shot] = pc.sha256(d / f"{shot}.mp4")
        write_align(epd, shot, sha[shot])
        write_verdict(epd, shot, sha[shot])
    fake = Fake(root, drama, epd, sha)
    fake.script.parent.mkdir(parents=True)
    fake.script.write_text(script_text(), encoding="utf-8")
    return fake


# ─────────────────────────── edl 变体 ───────────────────────────

F: Fake
RESULTS: list[tuple[str, str, str]] = []


def basis_of(shot: str, take: str) -> str:
    return edl.basis(edl.read_align(edl.align_path(F.epd, shot, take), shot, take))


def ev(eid: str, shot: str, a_in: str | float = "start", a_out: str | float = "end", kind: str = "shot", *,
       take: str | None = None, **extra: str) -> dict:
    """一个事件；用了 line: / cut: 锚点就按这条 take 当前的对齐缓存补上 basis（candidates 给的同一个值）。"""
    row: dict = {"id": eid, "shot": shot, "take": take or F.take(shot), "in": a_in, "out": a_out, "kind": kind}
    if (a_in, a_out, kind) != ("start", "end", "shot"):
        row["why"] = "自测"
    if any(isinstance(a, str) and a not in ("start", "end") for a in (a_in, a_out)):
        row["basis"] = basis_of(shot, row["take"])
    return row | extra


def ident() -> list[dict]:
    return [ev("e01", "shot01"), ev("e02", "shot02"), ev("e03", "shot03")]


def _val(v: object) -> str:
    return json.dumps(v, ensure_ascii=False) if isinstance(v, str) else repr(v)


def write_edl(events: list[dict], *, version: int = 1, base: int = 0, status: str = "draft", approved_by: str = "",
              fps: int = pc.FPS, notes: tuple[dict, ...] = ()) -> None:
    out = [f"version = {version}", f"base_version = {base}", f"status = {_val(status)}", f"approved_by = {_val(approved_by)}",
           f"fps = {fps}"]
    for table, rows in (("event", events), ("note", notes)):
        for r in rows:
            out += ["", f"[[{table}]]"] + [f"{k} = {_val(v)}" for k, v in r.items()]
    p = edl.edl_path(F.epd)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(out) + "\n", encoding="utf-8")


def expect(name: str, events: list[dict], fails: set[str], *, proxy_ok: bool = False, has: tuple[str, ...] = (),
           **kw: object) -> list[edl.Finding]:
    """写一份 edl → verify；不过项的 V 号必须恰好是 fails，has 里的字样必须出现在报告里。"""
    write_edl(events, **kw)
    items = edl.verify(F.drama, F.epd, proxy_ok)
    got = {f.code for f in items if f.level == edl.FAIL}
    text = "\n".join(f"{f.level} {f.code} {f.msg}" for f in items)
    assert got == fails, f"{name}：期望不过 {sorted(fails)}，实得 {sorted(got)}\n{text}"
    assert all(h in text for h in has), f"{name}：报告里缺 {[h for h in has if h not in text]}\n{text}"
    RESULTS.append((name, "、".join(sorted(fails, key=lambda c: int(c[1:]))) or "—",
                    "、".join(f"{f.code}" for f in items if f.level == edl.WARN) or "—"))
    return items


def expect_raise(name: str, events: list[dict], must: tuple[str, ...], **kw: object) -> str:
    """spec §4：这几类 verify 不出 V 行，直接报错停下，报错里要写明事件与锚点。"""
    write_edl(events, **kw)
    try:
        edl.verify(F.drama, F.epd)
    except SystemExit as e:
        msg = str(e)
        assert all(m in msg for m in must), f"{name}：报错里缺 {[m for m in must if m not in msg]}：{msg}"
        RESULTS.append((name, "报错停下", msg.splitlines()[-1].strip()[:60]))
        return msg
    raise AssertionError(f"{name}：verify 没有报错停下")


def cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(POST / "edl.py"), *args], capture_output=True)


# ─────────────────────────── 测试 ───────────────────────────

def t_identity() -> None:
    write_edl(ident())
    e = edl.load(F.epd)
    cur = edl.current_takes(F.epd, (x.shot for x in e.events))
    cuts = edl.resolve(e, edl.aligns_for(F.drama, F.epd, e.events, cur))
    end = round(DUR * pc.FPS)
    assert cuts == [edl.Cut(f"e0{i}", s, F.take(s), 0, end, "shot") for i, s in enumerate(SHOTS, 1)], cuts
    assert not expect("恒等 edl（整镜顺接）", ident(), set()), "恒等 edl 连警告都不该有"
    edl.plan(F.drama, F.epd)
    rows = json.loads((edl.out_dir(F.epd) / edl.PLAN_NAME).read_text(encoding="utf-8"))
    assert [(r["id"], r["src_in"], r["src_out"], r["dur"]) for r in rows] == [(f"e0{i}", 0.0, DUR, DUR) for i in (1, 2, 3)], rows


def t_plan_frames() -> None:
    write_edl([ev("e01", "shot01", a_out="cut:1"), ev("e02", "shot02", "line:2.start-0.3"), ev("e03", "shot03")])
    edl.plan(F.drama, F.epd)
    rows = json.loads((edl.out_dir(F.epd) / edl.PLAN_NAME).read_text(encoding="utf-8"))
    for r in rows:
        for k in ("src_in", "src_out", "dur"):
            assert abs(r[k] * pc.FPS - round(r[k] * pc.FPS)) < 1e-4, (r, k)
    assert rows[0]["src_out"] == round(163 / pc.FPS, 6) and rows[1]["src_in"] == round(137 / pc.FPS, 6), rows
    RESULTS.append(("plan：cut:1 / line:2.start-0.3 取整到帧", "—", "6.8→163 帧、5.7→137 帧"))


def t_init() -> None:
    p = edl.edl_path(F.epd)
    p.unlink(missing_ok=True)
    edl.init(F.epd, None, False)
    e = edl.load(F.epd)
    assert (e.version, e.base_version, e.status) == (1, 0, "draft"), e
    assert [(x.shot, x.take, x.a_in, x.a_out) for x in e.events] == [(s, F.take(s), "start", "end") for s in SHOTS]
    try:
        edl.init(F.epd, None, False)
        raise AssertionError("已有 edl 时 init 应当拒绝")
    except SystemExit as x:
        assert "--force" in str(x), x
    edl.approved_path(F.epd).write_text('{"versions": [1, 2]}\n', encoding="utf-8")
    edl.init(F.epd, "1-2", True)
    e = edl.load(F.epd)
    assert (e.version, e.base_version, [x.shot for x in e.events]) == (3, 2, ["shot01", "shot02"]), e
    edl.approved_path(F.epd).unlink()
    RESULTS.append(("init：v1 草稿 / 已有即拒绝 / --force 接着批准版本编号", "—", "v1 base 0 → v3 base 2"))


def t_planted() -> None:
    """spec §5 的 10 个故意埋错。"""
    ok = {"match_ok": "自测：只查别的项"}
    expect("① 切在词中", [*ident()[:2], ev("e03", "shot03", a_out="line:3.start+0.1")], {"V2"}, has=("切在词上",))
    old = pc.sha256(F.epd / "shots" / "shot02" / "shot02.mp4")[::-1]          # 旧 take：换过出片、旧缓存还在
    write_align(F.epd, "shot02", old)
    expect("② take sha 不符", [ident()[0], ev("e02", "shot02", take=old[:12]), ident()[2]], {"V1"}, has=("钉的 take",))
    edl.approved_path(F.epd).write_text('{"versions": [1, 2]}\n', encoding="utf-8")
    expect("③ base_version 旧", ident(), {"V10"}, version=3, base=1, has=("上一个已批准的是 v2",))
    edl.approved_path(F.epd).unlink()
    expect("④ flash 超长", [ev("f1", "shot03", 2.0, 7.5, "flash"), ident()[0] | ok, *ident()[1:]], {"V5"}, has=("FLASH_MAX",))
    expect("⑤ flash 超个数", [ev("f1", "shot03", 2.0, 3.0, "flash"), ev("f2", "shot02", 3.0, 4.0, "flash", **ok),
                            ev("f3", "shot01", 1.0, 2.0, "flash", **ok), ident()[0] | ok, *ident()[1:]], {"V5"}, has=("闪前 3 个",))
    expect("⑥ 事件过短", [*ident(), ev("e04", "shot02", 3.0, 3.5, **ok)], {"V5"}, has=("0.50s < 1s",))
    expect("⑦ 删半句", [ev("e01", "shot01", a_out=8.05), *ident()[1:]], {"V2"}, has=("删了半句", "3/4 个词"))
    expect_raise("⑧ 锚点不存在", [ident()[0], ev("e02", "shot02", "line:9.start"), ident()[2]],
                 ("e02", '"line:9.start"', "没有第 9 句"))
    expect_raise("⑨ in ≥ out", [ident()[0], ev("e02", "shot02", "line:2.end", "line:1.start"), ident()[2]],
                 ("e02", '"line:2.end"', '"line:1.start"', "in ≥ out"))
    expect_raise("⑩ fps 不符", ident(), ("fps = 25", f"pc.FPS {pc.FPS}"), fps=25)


def t_v1() -> None:
    v = F.epd / "shots" / "shot02" / "renders" / "review"
    shutil.rmtree(v)
    expect("V1 缺审片结论", ident(), {"V1"}, has=("shot02", "verdict.md"))
    expect("V1 缺审片结论 --proxy-ok", ident(), set(), proxy_ok=True, has=("--proxy-ok",))
    write_verdict(F.epd, "shot02", F.sha["shot02"])
    fn = render_review.verdict_ok
    del render_review.verdict_ok
    try:
        expect("V1 render_review 没有 verdict_ok", ident(), {"V1"}, has=("没有 verdict_ok",))
        expect("V1 没有 verdict_ok --proxy-ok", ident(), set(), proxy_ok=True, has=("没有 verdict_ok",))
    finally:
        render_review.verdict_ok = fn
    expect("V1 旧 take 没有对齐缓存", [ident()[0], ev("e02", "shot02", take="0123456789ab"), ident()[2]], {"V1"},
           has=("V2–V8 没查",))
    for fn in (edl.plan, edl.candidates):
        try:
            fn(F.drama, F.epd)
            raise AssertionError(f"{fn.__name__}：钉的是旧 take，应当报错停下")
        except SystemExit as x:
            assert "e02 shot02" in str(x) and F.take("shot02") in str(x), x
    RESULTS.append(("plan / candidates 钉旧 take：报错停下并给出当前 sha", "报错停下", "—"))


def t_stale() -> None:
    """md 写了 duration_s、出片长差 > pc.STALE_TOL_S → V1 报旧片，plan 报错停下（假 take 不是真视频，片长换成假的）。
    其余用例的假 md 不写 duration_s——没写就不判，命令行子进程也就不去 ffprobe 假 take。"""
    md = pc.shot_md(F.epd / "shots" / "shot02")
    orig, probe = md.read_text(encoding="utf-8"), pc.probe
    md.write_text(orig.replace("seam: 硬切", f"duration_s: {DUR:g}\nseam: 硬切", 1), encoding="utf-8")
    try:
        pc.probe = lambda _p: pc.Media(DUR + 0.02, DUR + 0.02, 1280, 720, True)
        expect("V1 出片与 md 同长（差 0.02s）", ident(), set())
        pc.probe = lambda _p: pc.Media(DUR + 2.0, DUR + 2.0, 1280, 720, True)
        expect("V1 旧片（md 改了时长、片没重出）", ident(), {"V1"}, has=("shot02", "md 改过、片没重出"))
        try:
            edl.plan(F.drama, F.epd)
            raise AssertionError("plan：出片是旧片，应当报错停下")
        except SystemExit as x:
            assert "旧片" in str(x) and "shot02" in str(x), x
        RESULTS.append(("plan 遇旧片：报错停下", "报错停下", "—"))
    finally:
        md.write_text(orig, encoding="utf-8")
        pc.probe = probe


def t_v3() -> None:
    goals = F.script.parent / "goals.toml"
    goals.write_text(GOALS_TOML, encoding="utf-8")
    try:
        expect("V3 恒等：锚点句都在", ident(), set())
        expect("V3 剪掉了结句", [*ident()[:2], ev("e03", "shot03", a_out=3.5)], {"V3"}, has=("resolved「Thank you」",))
        expect("V3 画面锚点窗剪了一截", [ident()[0], ev("e02", "shot02", 3.0), ident()[2]], {"V3"}, has=("used「杜克举盾」",))
        expect("V3 已出片镜整镜没进剪辑", ident()[:2], {"V3", "V6"}, has=("整镜没进剪辑",))
    finally:
        goals.unlink()


def t_v4() -> None:
    expect("V4 新接缝景别差不够（中景0.6 → 近景0.8）", [ident()[0], ev("e02", "shot02", 5.5), ident()[2]], {"V4"}, has=("弱",))
    expect("V4 同上 + match_ok", [ident()[0], ev("e02", "shot02", 5.5, match_ok="自测"), ident()[2]], set())
    flash = ev("f1", "shot03", 3.0, 4.0, "flash")
    expect("V4 单段镜中间切：取景推不出", [*ident()[:2], flash, ident()[2]], {"V4"}, has=("取景推不出",))
    expect("V4 同上 + match_ok", [*ident()[:2], flash | {"match_ok": "自测"}, ident()[2] | {"match_ok": "自测"}], set())


def t_chengjie() -> None:
    md = F.epd / "shots" / "shot02" / "shot02.md"
    text = md.read_text(encoding="utf-8")
    md.write_text(text.replace("seam: 硬切", "seam: 承接"), encoding="utf-8")
    try:
        expect("V4 承接缝整镜相接（edl 还表达不了）", ident(), {"V4"}, has=("承接缝",))
        expect("V4 承接缝 + match_ok 也不放行", [ident()[0], ident()[1] | {"match_ok": "自测"}, ident()[2]], {"V4"})
    finally:
        md.write_text(text, encoding="utf-8")


def t_basis() -> None:
    line2 = ev("e02", "shot02", "line:2.start")
    expect_raise("basis 缺了", [ident()[0], {k: v for k, v in line2.items() if k != "basis"}, ident()[2]], ("e02", "要写 basis"))
    expect_raise("basis 配在 start / end 上", [ident()[0], ident()[1] | {"basis": "0" * edl.BASIS_LEN}, ident()[2]],
                 ("e02", "basis 只配"))
    p = edl.align_path(F.epd, "shot02", F.take("shot02"))
    kept = p.read_text(encoding="utf-8")
    moved = json.loads(kept)                                   # md 在前面插了一句、align 按新 md 重算：原来的第 2 句变成第 3 句
    new = {"idx": 1, "speaker": "Duke", "kind": "画外", "text": "Hey there!", "planned": [0.2, 0.9], "start": 0.2, "end": 0.9,
           "conf": None, "words": [], "status": align.OFFSCREEN}
    moved["lines"] = [new] + [x | {"idx": x["idx"] + 1} for x in moved["lines"]]
    p.write_text(json.dumps(moved, ensure_ascii=False), encoding="utf-8")
    try:
        msg = expect_raise("md 改了台词、align 重算：按旧编号的 line:2 报错停下", [ident()[0], line2, ident()[2]],
                           ("e02", "另一版编号", line2["basis"]))
        assert basis_of("shot02", F.take("shot02")) in msg, msg
    finally:
        p.write_text(kept, encoding="utf-8")
    write_edl([ident()[0], ev("e02", "shot02", "cut:1"), ident()[2]])
    assert edl.plan(F.drama, F.epd)[1].fin == edl.frame(5.04)


def t_end_frames() -> None:
    """即梦 VFR 片：容器 10.0s，fps=24 转出来却是 241 帧——end 取缓存的 frames，不丢末帧；秒数锚点可到 241/24。"""
    p = edl.align_path(F.epd, "shot03", F.take("shot03"))
    kept = p.read_text(encoding="utf-8")
    p.write_text(json.dumps(json.loads(kept) | {"frames": round(DUR * pc.FPS) + 1}, ensure_ascii=False), encoding="utf-8")
    try:
        write_edl(ident())
        cuts = edl.plan(F.drama, F.epd)
        assert (cuts[2].fin, cuts[2].fout) == (0, round(DUR * pc.FPS) + 1), cuts[2]
        write_edl([*ident()[:2], ev("e03", "shot03", 1.0, 10.04)])
        assert edl.plan(F.drama, F.epd)[2].fout == 241
        RESULTS.append(("end 取 CFR 帧数（容器 10.0s、实出 241 帧）", "—", "e03 0–241 帧"))
    finally:
        p.write_text(kept, encoding="utf-8")


def t_v6_v7() -> None:
    expect("V6 新地区的场景展示剪到 2s", [ev("e01", "shot01", 3.0), *ident()[1:]], {"V6"}, has=("只剩 2.00s < 4s",))
    try:
        F.script.write_text(script_text(s01_dur="17"), encoding="utf-8")
        expect("V6 剧本改过没重出片：按镜首无词区间近似", [ev("e01", "shot01", 3.0), *ident()[1:]], {"V6"}, has=("近似",))
        expect("V7 剧本改过没重出片：节拍查不了", ident(), {"V7"}, has=("节拍查不了",))
        F.script.write_text(script_text(s01_beat="", s01_win="5.3–7"), encoding="utf-8")
        expect("V7 片头 5.2s 没台词没节拍", ident(), {"V7"}, has=("0.00–5.20s",))
        expect("V7 同上 + quiet_ok", [ident()[0] | {"quiet_ok": "自测"}, *ident()[1:]], set())
    finally:
        F.script.write_text(script_text(), encoding="utf-8")


def t_v8() -> None:
    expect("V8 好笑句后 0.3s 就切", [ident()[0], ev("e02", "shot02", a_out=7.4), ident()[2]], {"V8"}, has=("0.32s < 0.8s", "笑点后面留气口"))
    expect("V8 好笑句后留 0.9s", [ident()[0], ev("e02", "shot02", a_out=8.0), ident()[2]], set())


def t_v9() -> None:
    view = F.epd / "viewing_animatic"
    view.mkdir()
    video = F.epd / f"{EP}_animatic.mp4"
    video.write_bytes(random.Random(99).randbytes(2048))
    sha = pc.sha256(video)
    (view / "packet.json").write_text(json.dumps({"version": 1, "video": {"path": video.as_posix(), "sha256": sha}}), encoding="utf-8")
    (view / "review.md").write_text(f"# {EP} 整集观感\n> 视频: `x`（animatic）· 视频 sha256: {sha}\n\n## 注意力曲线\n\n"
                                    "## 最该改的 3 处\n1. **甲**：…\n2. **乙**：…\n3. **丙**：…\n\n## 其他\n4. 不算\n", encoding="utf-8")
    refs = [f"viewing_animatic {sha[:8]} #{n}" for n in (1, 2, 3)]
    try:
        expect("V9 审稿三条都没记账", ident(), {"V9"}, has=tuple(refs))
        done = tuple({"ref": r, "status": s, "detail": "自测"} for r, s in zip(refs, ("patched", "ticket", "waived")))
        expect("V9 三条都记了", ident(), set(), notes=done)
        expect("V9 有一条还 open", ident(), {"V9"}, notes=(*done[:2], done[2] | {"status": "open"}), has=("还是 open",))
        video.write_bytes(random.Random(100).randbytes(2048))
        expect("V9 审的视频变了：review 作废只提示", ident(), set(), has=("不作数",))
    finally:
        shutil.rmtree(view)
        video.unlink()


def t_v10_ledger() -> None:
    expect("V10 批准 v1 记进 approved.json", ident(), set(), status="approved", approved_by="自测")
    assert edl.approved_versions(F.epd) == {1}
    expect("V10 v2 草稿基于 v1", ident(), set(), version=2, base=1)
    expect("V10 v2 草稿却写 base 0", ident(), {"V10"}, version=2, base=0)
    edl.approved_path(F.epd).unlink()


def t_candidates() -> None:
    write_edl(ident())
    rows = json.loads(edl.candidates(F.drama, F.epd).read_text(encoding="utf-8"))
    m = edl.WORD_MARGIN
    for r in rows["events"]:
        blocks = [(s, e) for ln in SHOTS[r["shot"]].lines for s, e in ([(w[1], w[2]) for w in ln[4]] if ln[4] else [ln[3]])]
        for g in r["gaps"]:
            for s, e in blocks:
                assert not (s - m < g["lo"] < e + m or s - m < g["hi"] < e + m or g["lo"] < s and e < g["hi"]), (r["shot"], g, s, e)
    by = {r["shot"]: r for r in rows["events"]}
    assert [(c["t"], c["legal"]) for c in by["shot01"]["cuts"]] == [(6.8, True)], by["shot01"]["cuts"]
    assert [(q["a"], q["b"], q["dead"]) for q in by["shot01"]["quiet"]] == [(0.0, 5.2, False)], by["shot01"]["quiet"]
    edl.edl_path(F.epd).unlink()
    rows = json.loads(edl.candidates(F.drama, F.epd).read_text(encoding="utf-8"))
    assert rows["edl_version"] is None and [r["shot"] for r in rows["events"]] == list(SHOTS), rows
    RESULTS.append(("candidates：可切区间离词 ≥ WORD_MARGIN；没有 edl 按整镜列", "—", "—"))


def t_cli() -> None:
    write_edl(ident())
    for argv in (("verify", str(F.drama), EP), (str(F.drama), EP, "verify")):
        r = cli(*argv)
        assert r.returncode == 0, (argv, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace"))
    write_edl([ev("f1", "shot03", 2.0, 7.5, "flash"), ident()[0] | {"match_ok": "自测"}, *ident()[1:]])
    r = cli("verify", str(F.drama), EP)
    out = r.stdout.decode("utf-8", "replace")
    assert r.returncode == 1 and "✗ V5" in out, (r.returncode, out)
    write_edl(ident(), fps=25)
    r = cli("plan", str(F.drama), EP)
    assert r.returncode == 1 and "fps = 25" in r.stderr.decode("utf-8", "replace"), r.stderr
    RESULTS.append(("CLI：verify 命令放前 / 放后退出 0；埋错退出 1；plan 遇 fps 不符报错", "—", "—"))


def main() -> int:
    pc.utf8_console()
    global F
    root = Path(tempfile.mkdtemp(prefix="edl_selftest_"))
    repo_bound = script_tools.REPO
    script_tools.REPO = str(root)
    edl.ALIGN_PY = root / "没有这个_align.py"          # 缓存缺了就报错，不去真跑模型
    try:
        F = build(root)
        for t in (t_identity, t_plan_frames, t_init, t_planted, t_v1, t_stale, t_v3, t_v4, t_chengjie, t_basis, t_end_frames, t_v6_v7,
                  t_v8, t_v9, t_v10_ledger, t_candidates, t_cli):
            t()
    finally:
        script_tools.REPO = repo_bound
        shutil.rmtree(root, ignore_errors=True)
    col = max(subs.width(n) for n, _f, _w in RESULTS) + 2
    print("\n" + "场景" + " " * (col - subs.width("场景")) + "不过项 / 结果" + " " * 4 + "警告")
    for name, fails, warns in RESULTS:
        print(name + " " * (col - subs.width(name)) + fails + " " * max(2, 16 - subs.width(fails)) + warns)
    print(f"\n全部通过（{len(RESULTS)} 组，其中 spec §5 的 10 个埋错全部抓到）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
