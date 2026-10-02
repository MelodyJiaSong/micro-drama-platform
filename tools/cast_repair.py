# -*- coding: utf-8 -*-
"""多人同镜施法串了，只修这一个人（follow-up 054 / 057；w28 §3 ⑦；shengji_zhilu lessons L12）。

    python tools/cast_repair.py <shot 目录> <技能键> [施法者卡目录] [--at <起手秒>]
        → 即梦网页操作单：打印，并写 renders/repair/{技能键}_{施法者}_{a}-{b}s.md
    python tools/cast_repair.py <shot 目录> <技能键> [施法者卡目录] [--at 秒] --splice <修好的.mp4> --base <底片.mp4> [--as window|whole]
        → 按窗口把修好的那一段拼回底片（只换画面、声音保留底片），写 renders/fix_{技能键}_{底片名}.mp4

窗口 ＝ [起手前 2 s（回读判「早亮」往前看这么远）, 最后一个阶段结束后 0.5 s]，按 0.1 s 向外取整，不足 4 s 往两边补。
窗口里别人自己的光写进编辑 prompt 当保留项；和本技能同色、分不开的不出单，改整段重生。
网页上：1080P 正片底片的结果卡 →「局部重拍」截窗口 →「视频帧标注」在施法者入画的出手帧框住他、箭头指目标 → 挂锁定图 / 样片
→ 输入框 @ 主体后粘贴编辑 prompt。每次重试都回底片结果卡重点「局部重拍」（「重新编辑」不保留截取窗口），不在编辑产物上叠改；
同一个错 4 次全中就停，回排程闸门。拼回后跑 tools/cast_readback.py 复核。
"""
from __future__ import annotations

import dataclasses
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import animatic  # noqa: E402
import cast_readback  # noqa: E402
import prompt_compact  # noqa: E402
import seedance_kit  # noqa: E402
import skills_lib  # noqa: E402

PRE = cast_readback.ONSET_TOL + cast_readback.EARLY_LOOK     # 窗口起点：盖住回读判「早亮」往前看的那段
POST = 0.5                      # 窗口终点：最后一个阶段结束后 0.5 s
REPAIR_MIN, REPAIR_MAX = 4.0, 30.0    # 即梦「局部重拍」截取窗口（前端 edit_min / edit_max_video_duration）
WEB_VIDEO_TOTAL = 30.2          # 即梦一次任务视频合计上限（前端 max_total_video_duration；截取段也计入）
EDIT_MAX = 2000                 # 即梦编辑提示词上限（前端 edit_config.max_prompt_length）
FIT_TOL = cast_readback.DUR_TOL
AT_TOL = 1.0                    # --at 与起手时刻最多差这么多秒
RELEASE = ("release", "interrupt", "fizzle", "blocked")     # 出手时刻：第一段属于这里的阶段起点
FLAGS = ("--splice", "--base", "--at", "--as")


def pick(casts: list[skills_lib.Cast], key: str, who: str, at: float | None) -> skills_lib.Cast:
    hit = [c for c in casts if c.key == key and (not who or c.who == who)]
    if at is not None and hit:
        best = min(hit, key=lambda c: abs(c.t - at))
        if abs(best.t - at) > AT_TOL:
            raise SystemExit(f"--at {at:g}：{key} 最近的一次在 {best.t:g}s，差 {abs(best.t - at):.1f}s")
        return best
    if len(hit) != 1:
        raise SystemExit(f"{key}{('（' + who + '）') if who else ''} 在本镜命中 {len(hit)} 次："
                         f"{[(c.who, c.t) for c in hit]}；{'加' if who else '加施法者卡目录或'} --at <起手秒> 选一次")
    return hit[0]


def window(spans: list[tuple[str, float, float]], total: float) -> tuple[float, float]:
    """十分之一秒整数运算：两端向外取整盖住整次施法，不足 4 s 以中点为心补足，贴片头 / 片尾时往另一边让。"""
    n = math.floor(total * 10 + 1e-6)
    lo, hi = round(REPAIR_MIN * 10), round(REPAIR_MAX * 10)
    a = max(0, math.floor((min(s for _, s, _ in spans) - PRE) * 10 + 1e-6))
    b = min(n, math.ceil((max(e for _, _, e in spans) + POST) * 10 - 1e-6))
    if b - a < lo:
        a = max(0, min((a + b - lo) // 2, n - lo))
        b = min(n, a + lo)
    if not lo <= b - a <= hi:
        raise SystemExit(f"窗口 {a / 10:g}–{b / 10:g}s 不在局部重拍的 {REPAIR_MIN:g}–{REPAIR_MAX:g}s 内（镜长 {total:g}s）")
    return a / 10, b / 10


def seen(shot_dir: Path, groups: list[cast_readback.Doll], who: dict[str, list[cast_readback.Win]]) -> dict[str, tuple[float, str]]:
    """每人在给定时段里第一次在 previz 露面的时刻与画面哪一边（左 / 中 / 右）；整段看不见的不在结果里。"""
    spans = [w for ws in who.values() for w in ws]
    if not spans:
        return {}
    _, mp4 = cast_readback.previz_of(shot_dir)
    ts, fr = cast_readback.grab(mp4, min(a for a, _ in spans), max(b for _, b in spans))
    out: dict[str, tuple[float, str]] = {}
    for name, wins in who.items():
        g = cast_readback.resolve(groups, name)
        if g is None:
            continue
        for t, f in zip(ts, fr):
            bx = cast_readback.boxes(f, [groups[g]]) if cast_readback.inside(t, wins) else {}
            if 0 in bx:
                cx = (bx[0][0] + bx[0][2]) / 2 / cast_readback.W
                out[name] = (t, "左" if cx < 1 / 3 else ("右" if cx > 2 / 3 else "中"))
                break
    return out


def sheet(shot_dir: Path, key: str, who: str, at: float | None) -> tuple[str, float, float, skills_lib.Cast]:
    md = shot_dir / f"{shot_dir.name}.md"
    drama = skills_lib.drama_of(shot_dir)
    casts = skills_lib.casts_in(md.read_text(encoding="utf-8"))
    cast = pick(casts, key, who, at)
    cards = skills_lib.load(drama)
    card = skills_lib.find(cards, cast.key)
    groups, _ = cast_readback.dolls(shot_dir)
    label = cast_readback.labels(shot_dir)
    total = animatic.duration(md)
    spans = skills_lib.phases(card, cast)
    a, b = window([("起手", cast.t, cast.t)] + spans, total)      # 空：蓄光那几秒手上也不该有光，窗口从起手前算
    self_cast = cast.target in ("", cast.who)
    who_l = label.get(cast.who, cast.who)
    tgt_l = "" if self_cast else label.get(cast.target, cast.target)
    drift = cast_readback.DRIFT
    ours = [(skills_lib.card_hue(drama, card, ph), s, e) for ph, s, e in spans
            if ph in skills_lib.lit_phases(card, cast) | {"blocked"}]

    def sec(t: float) -> int:
        return max(0, min(prompt_compact._round(t - a), prompt_compact._round(b - a)))

    mine = {cast.who} | ({cast.target} if not self_cast else set())
    keep, clash = [], []
    for o in casts:
        if o is cast:
            continue
        oc = skills_lib.find(cards, o.key)
        glows = skills_lib.lit_phases(oc, o) | {"blocked"}          # 只看落进窗口、画面里真有光的阶段（空手一推不算）
        osp = [(ph, s, e) for ph, s, e in skills_lib.phases(oc, o) if ph in glows and s < b + drift and a - drift < e]
        if not osp:
            continue
        # 第三个人身上、与我这一次某段光同时（前后差 DRIFT 内）又同色的光：编辑分不开
        if any((o.who if ph in skills_lib.SELF_PHASES else o.target or o.who) not in mine
               and cast_readback.bands_meet(tint, skills_lib.card_hue(drama, oc, ph)) and s1 - drift < e and s - drift < e1
               for ph, s, e in osp for tint, s1, e1 in ours):
            clash.append(f"{label.get(o.who, o.who)} {oc.name}（{o.t:g}s）")
            continue
        p, q = sec(max(a, min(s for _, s, _ in osp))), sec(min(b, max(e for _, _, e in osp)))
        whose = (f"{who_l}的另一次" if o.key == cast.key else f"{who_l}的") if o.who == cast.who \
            else f"{label.get(o.who, o.who)}自己的"
        keep.append(f"第{p}{'–' + str(q) if q > p else ''}秒{whose}{oc.name}照旧")
    if clash:
        raise SystemExit(f"窗口 {a:g}–{b:g}s 里还有和{card.name}同色的施法：{'；'.join(clash)}。局部重拍分不开两道同色的光，"
                         "整段重生（先让排程闸门把它们错开）")
    self_w = [(s, e) for ph, s, e in spans if ph in skills_lib.SELF_PHASES] or [(cast.t, cast.t + 0.1)]
    first = seen(shot_dir, groups, {cast.who: self_w})
    rel = next((s for ph, s, _ in spans if ph in RELEASE), spans[0][1])
    mark = max(rel, first[cast.who][0]) if cast.who in first else rel
    aims = cast.outcome in ("成", "挡") and bool(tgt_l)          # 断 / 空：光没放出去，不牵涉目标
    look = seen(shot_dir, groups, {x: [(mark, mark + 0.2)] for x in (cast.who, cast.target if aims else "") if x})
    ents = {r.label: r.entity for r in seedance_kit.parse(md, seedance_kit.config(drama))[0] if r.kind == "主体"}

    def tag(x: str) -> str:
        bits = [f"画面{look[x][1]}"] if x in look else []
        bits += [f"@{ents[x]}"] if x in ents else []
        return f"（{'，'.join(bits)}）" if bits else ""
    beats = skills_lib.compose(card, cast, label)
    said = "，".join(f"第{sec(bt.t)}秒{bt.text}" for bt in beats if a <= bt.t <= b)
    # 绑定句与原片精简稿【技能】同一个函数；秒数换成窗口里的（局部重拍的截取段从 0 秒起）
    moved = dataclasses.replace(cast, t=round(cast.t - a, 3), at_break=None if cast.at_break is None else round(cast.at_break - a, 3))
    bind = skills_lib.binding_clause(card, moved, label)
    if bind and cast.outcome == "挡" and aims:
        bind += f"，光飞向{tgt_l}、在他身前被挡下"
    prompt = (f"只改源视频里{who_l}{tag(cast.who)}" + (f"对{tgt_l}{tag(cast.target)}" if aims else "") + f"的这一次施法：{said}。"
              + (bind + "。" if bind else "")
              + ("；".join(keep) + "。" if keep else "")
              + skills_lib.BINDING_TAIL + "。"
              + "其余人物、动作、口型、镜头与剪辑保持不变。标注线条不出现在画面中。")
    if len(prompt) > EDIT_MAX:
        raise SystemExit(f"编辑 prompt {len(prompt)} 字，超过即梦编辑框 {EDIT_MAX} 字")
    still, sample = card.file(card.sample_still), card.file(card.sample_video)
    refs = [f"- 锁定图：`{still.relative_to(REPO)}`" if still else "- 锁定图：技能卡还没有 sample.still（先定图再修，否则每次修出来都不一样）"]
    if sample:
        d = cast_readback.stream(sample)[0]
        refs.append(f"- 样片：`{sample.relative_to(REPO)}`（{d:.1f}s）" if (b - a) + d <= WEB_VIDEO_TOTAL
                    else f"- 样片放不下（窗口 {b - a:.1f}s + 样片 {d:.1f}s > {WEB_VIDEO_TOTAL:g}s），只挂锁定图")
    def where_note(x: str) -> str:
        if x in look:
            return f"画面{look[x][1]}"
        return ("previz 切不出他，按画面认人" if cast_readback.resolve(groups, x) is None
                else "previz 里这一帧看不到他，按画面认人")
    box_c = f"矩形框住{who_l}（{where_note(cast.who)}）"
    arrow = f"，箭头指向{tgt_l}（{where_note(cast.target)}）" if aims else ""
    L = [f"# {shot_dir.name} 修施法：{who_l} {card.key} {card.name} {cast.t:g}s（窗口 {a:g}–{b:g}s）", "",
         "1. 底片：本镜 **1080P 正片** 的结果卡（不是 480P 样片，也不是编辑产物）。",
         f"2. 点「局部重拍」，截 **{a:g}–{b:g}s**（{b - a:.1f}s）。",
         f"3. 在窗口内 **{mark - a:.1f}s**（全镜 {mark:g}s）暂停 →「视频帧标注」：{box_c}{arrow} →「添加至输入框」。",
         "4. 上传参考：", *refs,
         "5. 输入框里 @ 主体 " + ("、".join(ents[x] for x in (cast.who, cast.target) if x in ents) or "（本镜资料包里没有这些人的主体）")
         + "，再粘贴下面这段：", "", "```text", prompt, "```", f"（{len(prompt)} / {EDIT_MAX} 字）", ""]
    if keep:
        L += ["窗口里还有别人自己的光，已写成保留项：" + "；".join(keep) + "。", ""]
    L += ["6. 重试：回底片结果卡重新点「局部重拍」（「重新编辑」会丢掉截取窗口）；同一个错 4 次全中就停，回排程闸门。",
          f"7. 下载修好的片子后拼回：`python tools/cast_repair.py {shot_dir.relative_to(REPO)} {cast.key} {cast.who} "
          f"--at {cast.t:g} --splice <修好的.mp4> --base <1080P 正片底片.mp4>`，再跑 `python tools/cast_readback.py` 复核。"]
    return "\n".join(L), a, b, cast


COMMON_RATES = (Fraction(24), Fraction(25), Fraction(30), Fraction(50), Fraction(60), Fraction(24000, 1001), Fraction(30000, 1001))


def _rate(video: Path) -> Fraction:
    """画面的实际帧率：即梦出片是 60 Hz 时间网格上的 24 帧画面（r_frame_rate 报 60），取 avg_frame_rate，贴近常见帧率就吸过去。"""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate,r_frame_rate",
                          "-of", "json", str(video)], capture_output=True, text=True, check=True)
    s = json.loads(out.stdout)["streams"][0]
    r = Fraction(s["avg_frame_rate"] if s.get("avg_frame_rate", "0/0") != "0/0" else s["r_frame_rate"])
    near = min(COMMON_RATES, key=lambda c: abs(c - r))
    return near if abs(near - r) <= r / 100 else r


def splice(shot_dir: Path, base: Path, fixed: Path, a: float, b: float, key: str, as_: str | None) -> Path:
    total = animatic.duration(shot_dir / f"{shot_dir.name}.md")
    base_d, w, h = cast_readback.stream(base)
    fix_d = cast_readback.stream(fixed)[0]
    if base.resolve() == fixed.resolve() or seedance_kit.sha(base) == seedance_kit.sha(fixed):
        raise SystemExit(f"底片和修好的片子是同一个文件（{base.name}）：--base 给 1080P 正片底片")
    if abs(base_d - total) > FIT_TOL:
        raise SystemExit(f"底片 {base.name} 长 {base_d:.2f}s，本镜 {total:g}s：不是本镜整条出片，--base 给 1080P 正片底片")
    win = b - a
    is_win, is_whole = abs(fix_d - win) <= FIT_TOL, abs(fix_d - base_d) <= FIT_TOL
    if as_ is None:
        if is_win and is_whole and a > 0:
            raise SystemExit(f"修好的片子 {fix_d:.2f}s 既像窗口（{win:.2f}s）又像整条（{base_d:.2f}s）：加 --as window 或 --as whole")
        as_ = "window" if is_win else ("whole" if is_whole else "")
    if not as_ or (as_ == "window" and not is_win) or (as_ == "whole" and not is_whole):
        raise SystemExit(f"修好的片子 {fix_d:.2f}s，{'对不上' + ('窗口' if as_ == 'window' else '整条') if as_ else '既不像窗口也不像整条'}"
                         f"（窗口 {win:.2f}s，整条 {base_d:.2f}s）")
    fps = _rate(base)
    first = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=start_time",
                                             "-of", "json", str(base)], capture_output=True, text=True, check=True).stdout)
                  ["streams"][0].get("start_time") or 0.0)
    if abs(first) > 0.5 / float(fps):
        raise SystemExit(f"底片 {base.name} 的画面首帧在 {first:.3f}s、不在 0 秒：拼回后画面从 0 秒起、声音不动，声画会错开 "
                         f"{first:.3f}s。用即梦原样下载的出片当底片（它们都从 0 秒起）")
    head, tail = math.ceil(Fraction(str(a)) * fps), math.ceil(Fraction(str(b)) * fps)   # 按底片的恒定帧格：窗口前留几帧、从第几帧接回
    vf = (f"[0:v]setpts=PTS-STARTPTS,fps={fps},split=2[b0][b2];[b0]trim=end_frame={head},setpts=PTS-STARTPTS[v0];"
          f"[b2]trim=start_frame={tail},setpts=PTS-STARTPTS[v2];"
          f"[1:v]setpts=PTS-STARTPTS,fps={fps},trim=start_frame={head if as_ == 'whole' else 0},setpts=PTS-STARTPTS,scale={w}:{h},"
          f"tpad=stop_mode=clone:stop_duration={win + FIT_TOL:.3f},trim=end_frame={tail - head},setpts=PTS-STARTPTS[v1];"
          f"[v0][v1][v2]concat=n=3:v=1:a=0[v]")
    out = shot_dir / "renders" / f"fix_{key}_{base.stem}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(base), "-i", str(fixed), "-filter_complex", vf,
                    "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    str(out)], check=True)
    got = cast_readback.stream(out)[0]
    if abs(got - base_d) > 1.5 / float(fps):
        out.unlink()                                   # 判废的产物不留，免得 find_render 把它当成最新出片
        raise SystemExit(f"拼回后画面 {got:.3f}s，底片 {base_d:.3f}s，差了不止一帧，已删掉 {out.name}")
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    opt: dict[str, str] = {}
    pos: list[str] = []
    i = 0
    while i < len(args):
        if args[i] in FLAGS:
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                raise SystemExit(f"{args[i]} 后面要跟值")
            opt[args[i]] = args[i + 1]
            i += 2
        elif args[i].startswith("--"):
            raise SystemExit(f"不认识的参数 {args[i]}（可用：{' '.join(FLAGS)}）")
        else:
            pos.append(args[i])
            i += 1
    if len(pos) < 2:
        print(__doc__)
        return 2
    if opt.get("--as", "window") not in ("window", "whole"):
        raise SystemExit("--as 只能是 window 或 whole")
    shot_dir = Path(pos[0]).resolve()
    if shot_dir.suffix == ".md":
        shot_dir = shot_dir.parent
    try:
        at = float(opt["--at"]) if "--at" in opt else None
    except ValueError:
        raise SystemExit(f"--at 要写起手秒数，得到「{opt['--at']}」") from None
    if at is not None and not math.isfinite(at):
        raise SystemExit(f"--at 要写起手秒数，得到「{opt['--at']}」")
    text, a, b, cast = sheet(shot_dir, pos[1], pos[2] if len(pos) > 2 else "", at)
    if "--splice" not in opt:
        out = shot_dir / "renders" / "repair" / f"{cast.key}_{cast.who}_{a:g}-{b:g}s.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(text)
        print(f"\n→ {out.relative_to(REPO)}")
        return 0
    if "--base" not in opt:
        raise SystemExit("--splice 要同时给 --base <1080P 正片底片>（不按「最新 mp4」猜底片）")
    base = Path(opt["--base"]).resolve()
    out = splice(shot_dir, base, Path(opt["--splice"]).resolve(), a, b, cast.key, opt.get("--as"))
    print(f"底片 {base.name} 的 {a:g}–{b:g}s 换成修好的画面（声音仍是底片的）→ {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
