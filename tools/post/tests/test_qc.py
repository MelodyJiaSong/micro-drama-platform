# -*- coding: utf-8 -*-
"""qc.py / aigc.py 自测（纯 assert 脚本）：python tools/post/tests/test_qc.py

全部样片落在 ep01/post/qc_selftest/（可再生，逐件带戳，重跑跳过已做的）：
1. AIGC 写回实测：shot05 前 3 s 流复制，不带 / 带 aigc.ffmpeg_args / 再叠 +faststart → 回读、moov 位置；collect 的合并与去重。
2. 好片：shot05（0–4 s）+ shot06（0–4 s）→ 母带尺寸 1920×1080 / 24 fps / AAC 48 kHz，两遍响度归一，pc.DELIVER 交付编码并写 AIGC；
   配 plan 与 subs.srt_text 写的字幕。
3. 故意做坏的副本逐条跑 qc.run，逐项断言：25 fps（Q2）、没有 AIGC（Q8）、边界前 0.25 s 一帧白闪（Q3）、
   紧挨边界垫 1 帧 shot05 镜内切后的机位（Q3：scdet 的分压掉第二下，靠 mafd 尖峰抓）、字幕越尾与超 CPS（Q7）、
   plan 总长不符（Q1）、没归一的原片（Q5）；Q6 用合成 align 缓存（spec 的 JSON 格式，放 qc_selftest/align*/，不碰真的 post/align/）
   配粉噪声音轨：两侧同响 PASS、后一事件响 6 dB FAIL、缓存缺失 FAIL / 自测模式 SKIP、缓存与 take 对不上 FAIL。
4. CLI：--selftest 跑好片（退出码与报告一致），跑没有 AIGC 的副本必须非零退出。
测试写进 post/qc/ 的 qcst_*.qc.json 全过后删掉（留着的话说明有断言没过）。
"""
from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

POST = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POST))
import post_common as pc  # noqa: E402
import aigc  # noqa: E402
import edl  # noqa: E402
import mux_av  # noqa: E402
import qc  # noqa: E402
import subs  # noqa: E402

DRAMA, EP = "shengji_zhilu", "ep01"
EPD = pc.ep_dir(pc.drama_root(DRAMA), EP)
ST = EPD / pc.POST_DIR / "qc_selftest"
SHOTS = ("shot05", "shot06")
CLIP_S = 4.0
FLASH_FRAME = 90            # 3.75 s：离 4.0 s 的边界 0.25 s，落在 FLASH_WIN_S 内
SLIVER_SRC_S = 7.0          # shot05 镜内切（7 s）后的新机位：取 1 帧垫在 e01 末帧，紧挨边界——真实的「差一帧」
DX_JUMP_DB = 6.0
NOISE = "anoisesrc=color=pink:amplitude=0.1:seed=7"
SPEECH = {"shot05": [[1.0, 3.9]], "shot06": [[0.1, 2.5]]}      # 源秒：边界左侧 2.0–3.9、右侧 4.1–6.0 有「对白」
GOOD_CUES = [subs.Cue(0.5, 3.0, "Heading north, then.", "那就往北走。"),
             subs.Cue(4.4, 7.4, "Nine. Ten each, or ten total?", "九只。每人十只，还是一共十只？")]
BAD_CUES = [subs.Cue(3.0, 4.6, "This one runs past the cut.", "这句越过了切点。"),
            subs.Cue(5.0, 5.6, "Far too many words for half a second of screen.", "半秒钟里塞了太多太多的字幕内容。")]
PASS, FAIL, WARN, SKIP = qc.PASS, qc.FAIL, qc.WARN, qc.SKIP


# ─────────────────────────── 样片 ───────────────────────────

def made(out: Path, inputs: list[Path], make: Callable[[Path], object], **params: object) -> Path:
    """逐件落盘：输入与参数没变就跳过；先写 .part 再换名。"""
    sig = pc.signature(inputs, **params)
    if not pc.fresh(out, sig):
        part = out.with_name(out.stem + ".part" + out.suffix)
        make(part)
        part.replace(out)
        pc.stamp(out, sig)
    return out


def ff(out: Path, inputs: list[Path], *args: str | Path) -> Path:
    argv = [str(a) for a in args]
    return made(out, inputs, lambda part: pc.run([pc.FFMPEG, "-y", "-v", "error", *argv, part]), argv=argv)


def moov_first(p: Path) -> bool:
    order = []
    with open(p, "rb") as f:
        while len(h := f.read(8)) == 8:
            size, typ = struct.unpack(">I4s", h)
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0] - 8
            f.seek(size - 8, 1)
            order.append(typ)
    return order.index(b"moov") < order.index(b"mdat")


def write_srts(video: Path, cues: list[subs.Cue], size: tuple[int, int]) -> None:
    max_u = subs.style_for(*size).max_units
    for lang, suffix in zip(("src", "zh"), qc.SRT_SUFFIXES):
        video.with_name(video.stem + suffix).write_text(subs.srt_text(cues, lang, max_u), encoding="utf-8")


def align_fixture(d: Path, shot: str, take: Path, sha: str, speech: list[list[float]], recorded: str | None = None) -> None:
    """spec §3 的缓存格式，逐键照写（qc 只用 speech / take_sha256）。recorded：缓存里记的 take sha 与文件名不符（过期缓存）。"""
    lines = [{"idx": i, "speaker": "Duke", "kind": "正常台词", "text": "Ten each.", "planned": [a, b], "start": a, "end": b,
              "conf": 0.9, "words": [{"w": "Ten", "s": a, "e": (a + b) / 2, "p": 0.9}, {"w": "each.", "s": (a + b) / 2, "e": b, "p": 0.9}],
              "status": "ok"} for i, (a, b) in enumerate(speech, 1)]
    dur = pc.probe(take).v_dur
    cache = {"version": edl.align.VERSION, "shot": shot, "take": pc.rel(take), "take_sha256": recorded or sha, "model": "medium.en",
             "duration": dur, "frames": round(dur * pc.FPS), "lines": lines, "asr": {"text": "Ten each.", "wer": 0.0},
             "speech": speech, "cuts": {"planned": [], "detected": []}}
    d.mkdir(parents=True, exist_ok=True)
    (d / edl.align_path(EPD, shot, sha[:12]).name).write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")


# ─────────────────────────── 断言 ───────────────────────────

results: list[tuple[str, dict[str, str]]] = []


def qc_run(name: str, video: Path, plan: list[dict], expect: dict[str, str | tuple[str, ...]], **kw: object) -> dict[str, str]:
    rp = qc.report_path(EPD, video)
    rp.unlink(missing_ok=True)
    print(f"\n── {name}")
    try:
        qc.run(video, plan, EPD, **kw)
        raised = False
    except SystemExit as e:
        print(f"  （raise：{e}）")
        raised = True
    rep = json.loads(rp.read_text(encoding="utf-8"))
    got = {k: c["status"] for k, c in rep["checks"].items()}
    assert rep["video_sha256"] == pc.sha256(video), name
    assert raised == (FAIL in got.values()) == (rep["result"] == FAIL), f"{name}：raise 与 FAIL 不一致 {got}"
    for k, want in expect.items():
        assert got[k] in ((want,) if isinstance(want, str) else want), f"{name} {k}：要 {want}，得 {got[k]}（{rep['checks'][k]['detail']}）"
    results.append((name, got))
    return got


def main() -> int:
    pc.utf8_console()
    ST.mkdir(parents=True, exist_ok=True)
    takes = [pc.shot_mp4(EPD / "shots" / s) for s in SHOTS]
    shas = [pc.sha256(t) for t in takes]
    tags = aigc.collect(takes)

    # 1. AIGC 写回 / 回读 / 与 +faststart 叠加
    ids = [json.loads(aigc.format_tags(t)[aigc.KEY])["ProduceID"] for t in takes]
    assert json.loads(tags[aigc.KEY])["ProduceID"] == ",".join(ids), tags
    assert tags[aigc.COMMENT] == aigc.format_tags(takes[0])[aigc.COMMENT]
    assert json.loads(aigc.collect([takes[0], takes[0]])[aigc.KEY])["ProduceID"] == ids[0]
    snip = ("-t", "3", "-i", takes[0], "-map", "0", "-c", "copy", "-map_metadata", "-1")
    plain = ff(ST / "aigc_plain.mp4", takes[:1], *snip)
    tagged = ff(ST / "aigc_tagged.mp4", takes[:1], *snip, *aigc.ffmpeg_args(tags))
    fast = ff(ST / "aigc_faststart.mp4", takes[:1], *snip, "-movflags", "+faststart", *aigc.ffmpeg_args(tags))
    assert aigc.readback(plain) == [aigc.KEY], aigc.readback(plain)
    assert aigc.readback(tagged, tags) == [] and aigc.format_tags(tagged)[aigc.KEY] == tags[aigc.KEY]
    assert aigc.readback(fast, tags) == [] and moov_first(fast) and not moov_first(tagged)
    extra = {**tags, aigc.KEY: json.dumps({**json.loads(tags[aigc.KEY]), "ProduceID": ids[0] + ",vEXTRA"})}
    assert aigc.readback(tagged, extra) == [f"{aigc.KEY}.ProduceID:vEXTRA"]
    assert json.loads(aigc.collect([plain, takes[1]])[aigc.KEY])["ProduceID"] == ids[1]     # 缺标签的 take 警告后跳过
    print("AIGC：流复制不带 flag 丢标签；+use_metadata_tags 写回可读；与 +faststart 叠加 moov 在前、标签在")

    # 2. 好片
    m0 = pc.probe(takes[0])
    master = pc.master_size(m0.w, m0.h)
    n = round(CLIP_S * pc.FPS)
    args: list[str | Path] = []
    fc = []
    for k, t in enumerate(takes):
        args += ["-t", f"{CLIP_S + 1:g}", "-i", t]
        fc += [f"[{k}:v]fps={pc.FPS},trim=end_frame={n},setpts=PTS-STARTPTS,"
               f"scale={master[0]}:{master[1]}:flags=lanczos,setsar=1[v{k}]",
               f"[{k}:a]atrim=0:{CLIP_S:g},asetpts=PTS-STARTPTS,aresample={pc.AR}[a{k}]"]
    fc.append("".join(f"[v{k}][a{k}]" for k in range(len(takes))) + f"concat=n={len(takes)}:v=1:a=1[v][a]")
    mezz = ff(ST / "qcst_mezz.mp4", takes, *args, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
              *pc.MEZZ, "-c:a", "aac", "-ar", str(pc.AR), "-ac", "2")
    norm = made(ST / "qcst_norm.mp4", [mezz], lambda part: mux_av.loudnorm_file(pc.FFMPEG, mezz, part),
                target=[mux_av.LOUD_I, mux_av.LOUD_TP, mux_av.LOUD_LRA])
    enc = [*pc.DELIVER, "-c:a", "copy", *aigc.ffmpeg_args(tags)]
    deliver = ["-map", "0:v", "-map", "0:a", *enc]
    good = ff(ST / "qcst_good.mp4", [norm], "-i", norm, *deliver)
    plan = [{"id": f"e{k:02d}", "shot": s, "take": sha[:12], "src_in": 0.0, "src_out": CLIP_S, "dur": CLIP_S, "kind": "shot"}
            for k, (s, sha) in enumerate(zip(SHOTS, shas), 1)]
    plan_json = ST / "plan.json"
    plan_json.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    assert qc.events([edl.Cut(e["id"], e["shot"], e["take"], 0, n, e["kind"]) for e in plan]) == qc.events(plan)

    # 3. 做坏的副本
    fps25 = ff(ST / "qcst_fps25.mp4", [good], "-i", good, "-vf", "fps=25", *deliver)
    noaigc = ff(ST / "qcst_noaigc.mp4", [good], "-i", good, "-map", "0", "-c", "copy", "-map_metadata", "-1")
    flash = ff(ST / "qcst_flash.mp4", [good], "-i", good,
               "-vf", f"drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='eq(n,{FLASH_FRAME})'", *deliver)
    last = n - 1
    sliver = ff(ST / "qcst_sliver.mp4", [good, takes[0]], "-i", good, "-ss", f"{SLIVER_SRC_S:g}", "-t", "1", "-i", takes[0],
                "-filter_complex", f"[1:v]fps={pc.FPS},scale={master[0]}:{master[1]}:flags=lanczos,setsar=1,"
                                   f"setpts=PTS-STARTPTS+{last}/{pc.FPS}/TB[s];"
                                   f"[0:v][s]overlay=eof_action=pass:enable='eq(n,{last})'[v]",
                "-map", "[v]", "-map", "0:a", *enc)
    badsub = made(ST / "qcst_badsub.mp4", [good], lambda part: shutil.copy2(good, part))
    total = CLIP_S * len(SHOTS)
    noise = ["-i", good, "-f", "lavfi", "-i", f"{NOISE}:sample_rate={pc.AR}:duration={total:g}", "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-ar", str(pc.AR), "-ac", "2", *aigc.ffmpeg_args(tags)]
    dx_even = ff(ST / "qcst_dx_even.mp4", [good], *noise)
    dx_jump = ff(ST / "qcst_dx_jump.mp4", [good], *noise, "-af", f"volume={DX_JUMP_DB:g}dB:enable='gte(t,{CLIP_S:g})'")
    for v in (mezz, good, fps25, noaigc, flash, sliver, dx_even, dx_jump):
        write_srts(v, GOOD_CUES, master)
    write_srts(badsub, BAD_CUES, master)
    align_ok, align_none, align_stale = ST / "align", ST / "align_none", ST / "align_stale"
    for shot, take, sha in zip(SHOTS, takes, shas):
        align_fixture(align_ok, shot, take, sha, SPEECH[shot])
        align_fixture(align_stale, shot, take, sha, SPEECH[shot], recorded="0" * 64 if shot == SHOTS[0] else None)
    shutil.rmtree(align_none, ignore_errors=True)

    # 4. 逐项断言
    core = {"Q1": PASS, "Q2": PASS, "Q3": PASS, "Q8": PASS}
    st = {"selftest": True, "align_dir": align_none}
    qc_run("好片（自测模式，无 align 缓存）", good, plan,
           {**core, "Q4": PASS, "Q5": (PASS, WARN), "Q6": SKIP, "Q7": PASS, "Q9": PASS}, **st)
    qc_run("好片（正常模式，无 align 缓存）", good, plan, {**core, "Q6": FAIL}, align_dir=align_none)
    qc_run("25 fps", fps25, plan, {**core, "Q2": FAIL}, **st)
    qc_run("没有 AIGC", noaigc, plan, {**core, "Q8": FAIL}, **st)
    qc_run("边界前 0.25 s 一帧白闪", flash, plan, {**core, "Q3": FAIL, "Q4": PASS}, **st)
    qc_run("紧挨边界 1 帧别的机位", sliver, plan, {**core, "Q3": FAIL, "Q4": PASS}, **st)
    for v, t in ((flash, FLASH_FRAME / pc.FPS), (sliver, last / pc.FPS)):
        q3 = json.loads(qc.report_path(EPD, v).read_text(encoding="utf-8"))["checks"]["Q3"]["detail"]
        assert f"{t:.3f}s" in q3, (v.name, q3)
    qc_run("字幕越尾 + 超 CPS", badsub, plan, {**core, "Q7": FAIL}, **st)
    long_plan = [plan[0], {**plan[1], "src_out": CLIP_S + 0.5, "dur": CLIP_S + 0.5}]
    qc_run("plan 总长多 0.5 s", good, long_plan, {"Q1": FAIL, "Q2": PASS, "Q3": PASS}, **st)
    qc_run("没归一的原片（−31 LUFS、没写 AIGC）", mezz, plan, {"Q1": PASS, "Q2": PASS, "Q5": FAIL, "Q8": FAIL}, **st)
    qc_run("两侧对白同响", dx_even, plan, {**core, "Q6": PASS}, align_dir=align_ok)
    qc_run("后一事件对白响 6 dB", dx_jump, plan, {**core, "Q6": FAIL}, align_dir=align_ok)
    qc_run("align 缓存与 take 对不上（自测模式也 FAIL）", dx_even, plan, {"Q6": FAIL}, selftest=True, align_dir=align_stale)
    seams = json.loads(qc.report_path(EPD, dx_jump).read_text(encoding="utf-8"))["checks"]["Q6"]["data"]["seams"]
    assert abs(seams[0]["right"] - seams[0]["left"] - DX_JUMP_DB) < 1.0, seams

    # 5. CLI
    cli = [sys.executable, str(POST / "qc.py"), DRAMA, EP, "--plan", str(plan_json), "--selftest"]
    r = subprocess.run(cli + ["--video", str(good)], capture_output=True)
    rep = json.loads(qc.report_path(EPD, good).read_text(encoding="utf-8"))
    ch = rep["checks"]
    assert r.returncode == (0 if rep["result"] == PASS else 1), (r.returncode, rep["result"])
    assert all(ch[k]["status"] == PASS for k in core) and ch["Q6"]["status"] in (SKIP, PASS, FAIL)
    print(f"\nCLI 好片：退出码 {r.returncode}，{rep['result']}（Q6 {ch['Q6']['status']}：真 post/align/ 缓存"
          f"{'还没有' if ch['Q6']['status'] == SKIP else '已在，按真对白判'}）")
    r = subprocess.run(cli + ["--video", str(noaigc)], capture_output=True)
    assert r.returncode != 0 and "Q8" in r.stderr.decode("utf-8", "replace"), r.stderr[-500:]
    print(f"CLI 没有 AIGC 的副本：退出码 {r.returncode}")

    col = max(subs.width(name) for name, _ in results) + 2
    print("\n" + "场景" + " " * (col - subs.width("场景")) + " ".join(f"{k:<5}" for k in results[0][1]))
    for name, got in results:
        print(name + " " * (col - subs.width(name)) + " ".join(f"{got[k]:<5}" for k in got))
    for p in (EPD / pc.POST_DIR / qc.QC_SUB).glob("qcst_*.qc.json"):
        p.unlink()
    print(f"\n全部通过（{len(results)} 组 qc.run + 2 条 CLI + AIGC 写回）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
