# -*- coding: utf-8 -*-
"""出片审片（follow-up 042：shot04 出片两个亚伦、两个杜克，锤子搭在肩上没手扶；shot05 见狼低头、锤变斧、没打到狼）。

文字闸门与 previz 自检只管「给 Seedance 的东西对不对」，管不到「Seedance 还回来的对不对」。出片一落盘就跑这里：

    python tools/render_review.py <shot 目录> [视频.mp4]

不给视频就找最新的那条：本镜目录与 renders/ 里的 mp4（previz 除外），以及下载目录里文件名带 `shotNN_` 的即梦出片
（即梦下载名里带参考行，参考行里有 shotNN_…）；下载目录里的先拷进 renders/。
产物在 renders/review/{视频名前 40 字}.{sha256 前 12 位}/：逐秒拼图 sheet.png、命中与跳切前后的特写 beats.png、审片清单 checklist.md（头部 take_sha256）。
然后按 `ai_videos__出片审片` 派子代理看图逐项判，结论写进同目录 verdict.md（首行 通过 / 不通过，抄 checklist 的 take_sha256 行）——不通过就回到对应的闸门补，不直接改 prompt 碰运气。
剪辑校验（tools/post/edl.py verify V1）用 verdict_ok：按 take 的 sha 找结论，不认文件名。
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
for _p in (REPO / "tools", REPO / "tools" / "post"):
    sys.path.insert(0, str(_p))
import post_common as pc  # noqa: E402
import shot_overhead  # noqa: E402

DOWNLOADS = Path.home() / "Downloads"
FENCE = "`" * 3
SHA_KEY = pc.TAKE_ID_LEN                      # 审片目录名里 take sha256 取的位数（与 edl 的 take 同一口径）
SHA_HEAD = "take_sha256"                      # checklist.md 写、verdict.md 照抄的头部行
SHA_LINE = re.compile(r"^%s:\s*([0-9a-f]{64})\s*$" % SHA_HEAD, re.M)
PASSED = re.compile(r"[#*>\s]*通过")          # verdict.md 首行以「通过」开头（「不通过」不算）


def find_render(shot_dir: Path) -> Path | None:
    tag = shot_dir.name + "_"
    cands = [p for p in [*shot_dir.glob("*.mp4"), *(shot_dir / "renders").glob("*.mp4")] if "previz" not in p.name]
    cands += [p for p in DOWNLOADS.glob("jimeng-*.mp4") if tag in p.name]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def review_dir(shot_dir: Path, video: Path) -> Path:
    """一条出片的审片目录（按 take 的 sha 分，重出同名片不会沿用旧结论）：sheet / beats / checklist / verdict，
    以及 cast_readback 的 castcheck.json。"""
    return shot_dir / "renders" / "review" / ("%s.%s" % (video.stem[:40], pc.sha256(video)[:SHA_KEY]))


def verdict_ok(shot_dir: Path, take: Path) -> bool:
    """这条 take 审过且通过：按 sha 找到的每份 verdict.md 都是首行「通过」、头部 take_sha256 与 take 相符。"""
    sha = pc.sha256(take)
    found = [p.read_text(encoding="utf-8-sig")
             for p in (shot_dir / "renders" / "review").glob("*.%s/verdict.md" % sha[:SHA_KEY])]
    return bool(found) and all(PASSED.match(t) is not None and SHA_LINE.findall(t)[:1] == [sha] for t in found)


def frames(video: Path, times: list[float], out: Path, cols: int, width: int = 480) -> None:
    tmp = out.parent / (out.stem + "_f")
    tmp.mkdir(parents=True, exist_ok=True)
    for i, t in enumerate(times):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % max(0.0, t), "-i", str(video), "-frames:v", "1",
                        "-vf", "scale=%d:-1" % width, str(tmp / ("%03d.png" % i))], check=True)
    rows = -(-len(times) // cols)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "%03d.png"), "-vf", "tile=%dx%d" % (cols, rows),
                    "-frames:v", "1", str(out)], check=True)
    shutil.rmtree(tmp)


_CHANGE = re.compile(r"亮起|亮了一下|浮出|淡了|淡下去|暗下去|暗到|稳住|熄了|熄灭|起光|一闪|聚起|砸在|劈在|拍在|撞进")


def key_beats(shot_dir: Path) -> list[str]:
    """本镜关键拍（follow-up 043）：目标账本里在本镜学会 / 用出的本事（带时间窗）＋ `动作:` 里写到秒的变化。"""
    import tomllib
    import script_tools
    md = (shot_dir / (shot_dir.name + ".md")).read_text(encoding="utf-8")
    key = "S%s" % shot_dir.name[-2:]
    sc = next((p for p in shot_dir.parents if p.name == "5_6_分镜与prompt"), None)
    out: list[str] = []
    if sc is not None:
        ep = shot_dir.parent.parent.name
        script = sc.parent / "4_剧本" / "episodes" / ep / "script.md"
        goals = script.parent / "goals.toml"
        if goals.is_file():
            sshot = next((x for x in script_tools.parse(str(script))[0] if x.key == key), None)
            for k in tomllib.loads(goals.read_text(encoding="utf-8")).get("skill", []):
                for fld, word in (("learned", "学会"), ("used", "用出")):
                    if k.get(fld, [None])[0] == key and sshot is not None:
                        w = script_tools.snippet_window(sshot, k[fld][1])
                        out.append("%s%s「%s」%s" % ("%g–%gs " % w if w else "", word, k["what"], "（" + k[fld][1] + "）"))
    body = (re.search(FENCE + r"text\n(.*?)\n" + FENCE, md, re.S) or [None, ""])[1]
    act = (re.search(r"^动作: (.*)$", body, re.M) or [None, ""])[1]
    out += ["动作里的变化：" + cl.strip() for cl in re.split(r"[；。]", act) if _CHANGE.search(cl) and re.search(r"\d+(?:\.\d+)?s", cl)]
    return out


TAIL_DROP = 12.0     # 最后 0.25 s 要比前 2 s 的中位响度低这么多 dB，才算声音在镜内收住了


def tail_db(video: Path, secs: float) -> tuple[float, float]:
    """最后 0.25 s 的响度与它前面 2 s（每 0.25 s 一格）的中位响度，dB。"""
    import math
    import statistics
    import struct
    import tempfile
    import wave
    w = Path(tempfile.gettempdir()) / "render_review_tail.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % max(0.0, secs - 2.25), "-i", str(video), "-ac", "1", "-ar", "16000", str(w)], check=True)
    with wave.open(str(w)) as f:
        x = struct.unpack("<%dh" % f.getnframes(), f.readframes(f.getnframes()))
    step = 4000

    def db(seg):
        return 20 * math.log10(max(1e-9, math.sqrt(sum(v * v for v in seg) / max(1, len(seg))) / 32768))
    wins = [db(x[i:i + step]) for i in range(0, len(x) - step + 1, step)]
    return (wins[-1] if wins else -99.0), (statistics.median(wins[:-1]) if len(wins) > 1 else -99.0)


VIDEO: Path | None = None


def tail_verdict(shot_dir: Path, secs: float) -> str:
    if VIDEO is None:
        return "（没有音轨）"
    last, body = tail_db(VIDEO, secs)
    ok = body - last >= TAIL_DROP or last < -45
    return "%s：最后 0.25 s %.0f dB，前 2 s 中位 %.0f dB，%s（要低 ≥ %g dB）" % (
        "通过" if ok else "不通过", last, body, "收住了" if ok else "声音在镜尾被切断", TAIL_DROP)


CAST_WORD = {"pass": "通过", "fail": "不通过", "unchecked": "未查"}


def cast_lines(shot_dir: Path) -> list[str]:
    """R9：每次施法的光落没落在对的人身上（tools/cast_readback.py 机测，逐次结论另存 castcheck.json）。"""
    import cast_readback
    if VIDEO is None:
        return ["- （没有出片）"]
    try:
        verdicts, notes = cast_readback.readback(shot_dir, VIDEO)
    except SystemExit as e:
        return ["- 未查：%s" % e]
    if not verdicts:
        return ["- （本镜无施法）"]
    cast_readback.save(shot_dir, VIDEO, verdicts, notes)
    return ["- %s：%s %s %gs" % (CAST_WORD[v.status], v.key, v.name, v.t) + "".join("\n  - " + ln for ln in v.lines)
            for v in verdicts] + ["- （说明）" + s for s in notes]


def checklist(shot_dir: Path, secs: float, hits: list[dict], jumps: list[float], sha: str) -> str:
    md = (shot_dir / (shot_dir.name + ".md")).read_text(encoding="utf-8")
    body = (re.search(FENCE + r"text\n(.*?)\n" + FENCE, md, re.S) or [None, ""])[1]
    field = {k: (re.search(r"^%s: (.*)$" % k, body, re.M) or [None, ""])[1] for k in ("角色", "台词", "动作")}
    chars = re.findall(r"(?:^|；)([cm]\d+_[^＝；]+)＝", field["角色"])
    gear = re.findall(r"(e\d{4}_[^＝；]+)＝([^；]+(?:；不是[^；]+)?)", field["角色"])
    carry = [c for c in re.split(r"[；。]", field["角色"] + "；" + field["动作"]) if re.search(r"扛|挎|背在|搭在.{0,3}肩", c)]
    L = ["# %s 出片审片清单（tools/render_review.py 生成；按 ai_videos__出片审片 逐项判）" % shot_dir.name,
         "%s: %s" % (SHA_HEAD, sha), "",
         "时长 %gs。每一项写 通过 / 不通过 + 哪几秒 + 看见了什么。" % secs,
         "结论写同目录 verdict.md：首行 通过 / 不通过，下一行照抄上面的 %s 行。" % SHA_HEAD, "",
         "## R1 人数：每个具名角色每一帧最多一个（没有分身、双胞胎）"]
    L += ["- %s" % c for c in chars]
    if jumps:
        L.append("- 跳切 %s：切之前新位置上不许先出现这个人（beats.png 里切前切后各一帧）" % "、".join("%gs" % j for j in jumps))
    L += ["", "## R2 道具形制：对得上锁定串，没变成易混的东西"] + ["- %s：%s" % g for g in gear]
    L += ["", "## R3 持物：扛 / 挎 / 背着的东西有手握着或带子挂着，不悬空"] + (["- %s" % c.strip() for c in carry] or ["- （本镜无）"])
    L += ["", "## R4 命中：打中的那一下武器真的碰到目标身上（beats.png 每下前 0.2 s / 当下 / 后 0.2 s）"]
    L += ["- %gs %s用%s%s %s%s" % (float(h["t"]), h["who"], h["with"], "（故意落空）" if h.get("miss") else "打",
                                   h["target"], ("：" + h["result"]) if h.get("result") else "") for h in hits] or ["- （本镜无）"]
    L += ["", "## R7 关键拍兑现：剧本里学会 / 用出本事、亮起 / 变暗 / 稳住这类变化，在出片里看得见、时刻大致对得上"]
    L += ["- %s" % k for k in key_beats(shot_dir)] or ["- （本镜无）"]
    L += ["", "## R8 镜尾声音收住（机测，follow-up 044）", "- " + tail_verdict(shot_dir, secs)]
    L += ["", "## R9 施法的光落在对的人身上（机测，follow-up 057；不通过 / 未查的那几次看 sheet.png 复核）"] + cast_lines(shot_dir)
    L += ["", "## R5 视线与脸：对着敌人 / 说话对象时不低头、不背对（剧本写了背影的除外）；说话的人看得见脸和嘴",
          "- 台词：" + (field["台词"] or "无"), "", "## R6 其他：剧本里没有的人、物、字、特效", ""]
    return "\n".join(L)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    shot_dir = Path(sys.argv[1]).resolve()
    if shot_dir.suffix == ".md":
        shot_dir = shot_dir.parent
    video = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else find_render(shot_dir)
    if video is None or not video.is_file():
        print("没找到 %s 的出片（本镜目录、renders/、下载目录里带 %s_ 的即梦文件都没有）" % (shot_dir.name, shot_dir.name))
        return 1
    if shot_dir not in video.parents:
        (shot_dir / "renders").mkdir(exist_ok=True)
        dst = shot_dir / "renders" / video.name
        if not dst.exists():
            shutil.copy2(video, dst)
        video = dst
    why = pc.stale_take(shot_dir / (shot_dir.name + ".md"), video)
    if why:
        print("旧片不审（按旧 md 审出来的结论对不上现在的剧本）：" + why)
        return 1
    secs = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                                capture_output=True, text=True, check=True).stdout.strip())
    global VIDEO
    VIDEO = video
    ov = shot_overhead.load(shot_dir)
    hits = sorted(ov.get("hit", []), key=lambda h: float(h["t"]))
    jumps = shot_overhead.jump_cuts(ov)
    out = review_dir(shot_dir, video)
    out.mkdir(parents=True, exist_ok=True)
    frames(video, [float(t) for t in range(int(secs) + 1) if t < secs], out / "sheet.png", 6)
    beats = sorted({round(t, 2) for h in hits for t in (float(h["t"]) - 0.2, float(h["t"]), float(h["t"]) + 0.2)}
                   | {round(t, 2) for j in jumps for t in (j - 0.3, j + 0.1)})
    if beats:
        frames(video, [t for t in beats if 0 <= t < secs], out / "beats.png", 3, 640)
    (out / "checklist.md").write_text(checklist(shot_dir, secs, hits, jumps, pc.sha256(video)), encoding="utf-8")
    print("审片素材 → %s（sheet.png%s、checklist.md）" % (out.relative_to(REPO), "、beats.png" if beats else ""))
    print("下一步：派 ai_videos__出片审片 子代理看图逐项判，结论写 %s" % (out / "verdict.md").relative_to(REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
