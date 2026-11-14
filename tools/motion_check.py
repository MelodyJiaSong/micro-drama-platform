# -*- coding: utf-8 -*-
"""技能条 / 镜头成片的动作流畅自检：找「中间突然慢下来」的慢动作嫌疑段、定格与卡顿（dota_yingxiong follow-up 245）。

逐帧算相邻两帧（缩成 192×108 灰度）的平均像素变化，除以两帧时间差，得到「每秒画面变化量」；
按 0.5 s 一格汇总。只在「动作段」（默认起势之后、收势之前）里比较：
- 慢动作嫌疑：连续 ≥ 1 s 的格子变化量低于前一段动作格的 45%（突然变慢），且之后又恢复——画面里动作还在进行却明显变慢；
- 定格：相邻帧几乎完全相同（变化量 < 0.02），连续 ≥ 0.25 s；
- 另出一张每秒 4 帧的拼图（带时间码），给代理逐帧看速度是否一致。
- 剪切（一镜到底用，dota_yingxiong follow-up 295）：相邻两帧比较「明显边缘」的重合比例——固定机位下特效闪光只改亮度，
  树干、地平线等边缘还在原处；切镜头时边缘整体移位。重合 < 0.6 报「疑似剪切」并给时刻，代理抽前后两帧确认。
  实测：Lina k421 b3a9b37f 3.51 s 与 k424 45b3c4be 3.76 s 真剪切 0.53 / 0.50；闪电、火柱等特效段 ≥ 0.7。

全局速度（用户 2026-10-26，follow-up 246）：画面变化量只看「相对前段」的骤降，整段匀速偏慢测不出来。
`--xt 图.png --band 上-下`（比例，默认 0.55-0.85，选小兵身体所在的水平带）出时空切片图：每帧一行、每秒一条黄线，
跑动主体是斜线，越平越快，竖线＝原地不动。`--scale 比例:米`（已知高度的主体占画面高度的比例，如树精 4 米占 0.55 → `0.55:4`）
加 `--expect 秒-秒:米每秒`（可重复，食尸鬼全速冲刺约 6 m/s）时，在该时段画红色参考斜线（要求速度）与蓝色斜线（走路 1.5 m/s），
并打印该时段应横移多少像素。代理比对主体斜线：接近蓝线或竖直＝全局偏慢。自动测速在 AI 视频上不可靠（模糊、四肢乱晃），不自动判定。
只看横向，朝镜头的冲刺要结合拼图。

这是筛查工具：变化量低也可能是剧本里本来就静（站定、收势）。报出的段一定要回看拼图与原片判断，
结论写进该条 review.md 的「流畅自检」一节。不调用任何服务。

    python tools/motion_check.py <视频.mp4> [--action 1.5-11] [--sheet out.jpg] [--xt xt.png --band 0.55-0.85 --scale 0.55:4 --expect 0.5-3.6:6]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

W, H = 192, 108
FONT = "C\\:/Windows/Fonts/arial.ttf"


def frames(video: Path) -> tuple[np.ndarray, np.ndarray]:
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=pts_time",
                            "-of", "json", str(video)], capture_output=True, text=True, check=True)
    ts = np.array([float(f["pts_time"]) for f in json.loads(probe.stdout)["frames"] if "pts_time" in f])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-fps_mode", "passthrough",
                          "-vf", "scale=%d:%d,format=gray" % (W, H), "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (W * H)
    imgs = np.frombuffer(raw[:n * W * H], dtype=np.uint8).reshape(n, H, W).astype(np.float32)
    m = min(n, len(ts))
    return imgs[:m], ts[:m]


CUT_OVERLAP = 0.6


def edge_overlap(x: np.ndarray, y: np.ndarray) -> float:
    """两帧「明显边缘」（各自梯度前 30%）落在同一位置的比例，以前一帧的边缘为分母。"""
    def strong(a: np.ndarray) -> np.ndarray:
        gx = np.zeros_like(a)
        gy = np.zeros_like(a)
        gx[:, 1:-1] = a[:, 2:] - a[:, :-2]
        gy[1:-1, :] = a[2:, :] - a[:-2, :]
        m = np.hypot(gx, gy)
        return m > np.percentile(m, 70)
    ex, ey = strong(x), strong(y)
    return float((ex & ey).sum() / max(ex.sum(), 1))


def cuts(imgs: np.ndarray, ts: np.ndarray) -> list[dict]:
    out = []
    for k in range(1, len(imgs)):
        ov = edge_overlap(imgs[k - 1], imgs[k])
        if ov < CUT_OVERLAP:
            out.append({"t": round(float(ts[k]), 2), "overlap": round(ov, 2)})
    return out


def analyse(video: Path, action: tuple[float, float] | None) -> dict:
    imgs, ts = frames(video)
    dt = np.diff(ts)
    diff = np.abs(np.diff(imgs, axis=0)).mean(axis=(1, 2))
    rate = diff / np.maximum(dt, 1e-3)                       # 每秒画面变化量
    mid = (ts[1:] + ts[:-1]) / 2
    dur = float(ts[-1] + (dt[-1] if len(dt) else 0))
    a0, a1 = action if action else (1.5, max(1.5, dur - 2.0))
    bins = []
    t = 0.0
    while t < dur - 1e-6:
        sel = (mid >= t) & (mid < t + 0.5)
        bins.append({"t0": round(t, 2), "t1": round(min(t + 0.5, dur), 2),
                     "rate": round(float(rate[sel].mean()), 2) if sel.any() else 0.0,
                     "action": a0 <= t + 0.25 <= a1})
        t += 0.5
    act = [b for b in bins if b["action"]]
    med = float(np.median([b["rate"] for b in act])) if act else 0.0
    # 慢动作嫌疑：动作段里相对「前 1.5 s 动作格的均值」骤降到 45% 以下，连续 ≥ 2 格（1 s），之后在动作段内又回升
    flags = []
    i = 0
    while i < len(act):
        prev = [b["rate"] for b in act[max(0, i - 3):i]]
        ref = float(np.mean(prev)) if prev else med
        if ref > 0 and act[i]["rate"] < 0.45 * ref:
            j = i
            while j + 1 < len(act) and act[j + 1]["rate"] < 0.45 * ref:
                j += 1
            recovers = any(b["rate"] >= 0.6 * ref for b in act[j + 1:j + 4])   # 之后 1.5 s 内又快起来
            if j - i + 1 >= 2 and recovers:
                flags.append({"kind": "慢动作嫌疑", "t0": act[i]["t0"], "t1": act[j]["t1"],
                              "rate": round(float(np.mean([b["rate"] for b in act[i:j + 1]])), 2), "ref": round(ref, 2)})
            i = j + 1
        else:
            i += 1
    frozen, run0 = [], None
    for k, d in enumerate(diff):
        if d < 0.02 and a0 <= mid[k] <= a1:
            run0 = mid[k] if run0 is None else run0
        else:
            if run0 is not None and mid[k - 1] - run0 >= 0.25:
                frozen.append({"kind": "定格", "t0": round(float(run0), 2), "t1": round(float(mid[k - 1]), 2)})
            run0 = None
    return {"video": str(video), "duration": round(dur, 2), "frames": int(len(ts)),
            "avg_fps": round(len(ts) / dur, 2) if dur else 0, "action": [a0, a1], "action_median": round(med, 2),
            "bins": bins, "flags": flags + frozen, "cuts": cuts(imgs, ts)}


XW, XH, XFPS, ROW = 640, 360, 24, 4       # 时空切片：缩放尺寸、采样帧率、每帧占几行


def xt_plot(video: Path, band: tuple[float, float], out: Path, scale: str | None, expects: list[str]) -> dict:
    """时空切片图：取画面高度 band（比例）这条水平带，每帧压成一行按时间往下堆（每秒一条黄线）。
    跑动的主体在图上是斜线，越斜（越接近水平）越快，竖线＝原地不动。
    给了 --scale 与 --expect 时，在对应时段画参考斜线：红＝剧本要求的最低速度，蓝＝普通走路 1.5 m/s，
    代理拿主体的斜线去比——比红线更平才算够快。AI 视频的运动模糊、四肢乱晃会让自动测速失真（follow-up 246 实测），
    所以这里不自动下结论，只出图和换算，判断写进 review.md。"""
    from PIL import Image, ImageDraw
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", "fps=%d,scale=%d:%d,format=gray" % (XFPS, XW, XH),
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    n = len(raw) // (XW * XH)
    f = np.frombuffer(raw[:n * XW * XH], dtype=np.uint8).reshape(n, XH, XW).astype(np.float32)
    d = f[:, int(band[0] * XH):max(int(band[1] * XH), int(band[0] * XH) + 1)].mean(axis=1)
    img = np.clip(np.abs(d - np.median(d, axis=0)) * 4, 0, 255).astype(np.uint8).repeat(ROW, axis=0)
    im = Image.fromarray(img).convert("RGB")
    dr = ImageDraw.Draw(im)
    for sec in range(int(n / XFPS) + 1):
        dr.line([(0, sec * XFPS * ROW), (XW, sec * XFPS * ROW)], fill=(255, 255, 0))
        dr.text((2, sec * XFPS * ROW + 1), "%ds" % sec, fill=(255, 255, 0))
    info = {"band": list(band), "plot": str(out)}
    if scale:
        frac, meters = (float(x) for x in scale.split(":"))
        ppm = frac * XH / meters                                  # 每米多少像素（640 宽画面）
        info["px_per_m"] = round(ppm, 1)
        for e in expects:
            win, need = e.split(":")
            w0, w1 = (float(x) for x in win.split("-"))
            for mps, col in ((float(need), (255, 60, 60)), (1.5, (80, 140, 255))):
                dx = mps * ppm * (w1 - w0)                        # 该时段内应横移的像素
                y0, y1 = w0 * XFPS * ROW, w1 * XFPS * ROW
                for x0 in (XW * 0.1, XW * 0.9):
                    sgn = 1 if x0 < XW / 2 else -1
                    dr.line([(x0, y0), (x0 + sgn * dx, y1)], fill=col, width=2)
            info.setdefault("expect", []).append({"t0": w0, "t1": w1, "need_mps": float(need),
                                                  "need_px": round(float(need) * ppm * (w1 - w0)), "walk_px": round(1.5 * ppm * (w1 - w0))})
    im.save(out)
    return info


def sheet(video: Path, out: Path) -> None:
    """每秒 4 帧、每行 8 格；行数按片长给足，整条都进拼图（原来固定 8×8 只到 16 秒，
    长镜头的结尾审稿人看不到、只能判「拿不准」，chuanyue_yiri follow-up 059）。"""
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                           capture_output=True, text=True).stdout.strip()
    rows = max(1, -(-int(float(probe or 16) * 4) // 8))
    vf = ("fps=4,scale=320:-2,drawtext=fontfile='%s':text='%%{pts\\:hms}':x=4:y=4:fontsize=18:"
          "fontcolor=yellow:box=1:boxcolor=black@0.6,tile=8x%d" % (FONT, rows))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", vf, "-frames:v", "1", str(out)], check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("video")
    ap.add_argument("--action", help="动作段 秒-秒，默认 1.5 到 片长-2")
    ap.add_argument("--sheet", help="另存每秒 4 帧拼图")
    ap.add_argument("--band", default="0.55-0.85", help="测速水平带（画面高度比例），默认 0.55-0.85")
    ap.add_argument("--xt", help="另存时空切片图")
    ap.add_argument("--scale", help="画面尺度 比例:米，如 0.55:4（4 米高的主体占画面高度 55%%）")
    ap.add_argument("--expect", action="append", default=[], help="秒-秒:最低速度（有 --scale 时为米/秒），可重复")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    action = tuple(float(x) for x in a.action.split("-")) if a.action else None
    r = analyse(Path(a.video), action)
    if a.sheet:
        sheet(Path(a.video), Path(a.sheet))
    if a.xt:
        band = tuple(float(x) for x in a.band.split("-"))
        r["xt"] = xt_plot(Path(a.video), band, Path(a.xt), a.scale, a.expect)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    print("%s · %.2f s · %d 帧（平均 %.1f fps）· 动作段 %.1f–%.1f s · 动作段中位变化量 %.2f"
          % (Path(r["video"]).name, r["duration"], r["frames"], r["avg_fps"], *r["action"], r["action_median"]))
    print("  " + " ".join("%.1f:%s%.1f" % (b["t0"], "*" if b["action"] else "", b["rate"]) for b in r["bins"]))
    if "xt" in r:
        x = r["xt"]
        print("  时空切片图 %s（切片带 %.2f–%.2f）%s" % (x["plot"], *x["band"], "，1 m ≈ %.1f px" % x["px_per_m"] if "px_per_m" in x else ""))
        for e in x.get("expect", []):
            print("    %.1f–%.1f s 要求 ≥ %.1f m/s：红线斜率＝该速度（全程应横移 %d px），蓝线＝走路（%d px）——打开图比对主体斜线的斜率，主体中途停下不必走满全程"
                  % (e["t0"], e["t1"], e["need_mps"], e["need_px"], e["walk_px"]))
    if not r["flags"]:
        print("  未见慢动作嫌疑或定格（仍要看拼图%s确认）" % ("与时空切片图" if "xt" in r else ""))
    for f in r["flags"]:
        extra = "（变化量 %.2f，前段 %.2f）" % (f["rate"], f["ref"]) if "rate" in f else ""
        print("  ⚠ %s %.1f–%.1f s%s" % (f["kind"], f["t0"], f["t1"], extra))
    if r["cuts"]:
        print("  ⚠ 疑似剪切 " + "、".join("%.2f s（边缘重合 %.2f）" % (c["t"], c["overlap"]) for c in r["cuts"])
              + "——抽前后两帧确认；一镜到底的条不过")
    else:
        print("  剪切：无（边缘重合均 ≥ %.1f）" % CUT_OVERLAP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
