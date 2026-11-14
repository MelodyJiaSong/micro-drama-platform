# -*- coding: utf-8 -*-
"""出片「人像摆件」筛查（chuanyue_yiri follow-up 054；prompts-generate「审核」表演一节）：找画面里某个人静止太久。

    python tools/person_motion.py <视频.mp4> [--still 1.5] [--sheet out.jpg]

做法：每秒 6 帧，用 OpenCV 自带的人脸检测（正脸 + 侧脸）找人，把每张脸往下扩成「头肩到上身」的框，
相邻检测按位置连成一条条人物轨迹；每条轨迹逐帧算框内灰度变化（缩到 64 宽），低于阈值的连续段 ≥ --still 秒
就报「静止」，给出时间段与人在画面的位置（左 / 中 / 右）。说话的人嘴在动，上身框里通常有变化；听的人
如果一动不动就会被报出来（EP1 s3 st4 Felix）。

这是筛查：静止也可能是分镜写的安静一拍（≤1 秒的愣一下不报），报出的段一定回看拼图判断。
检测不到脸的人（背对、太远、太小）不覆盖——报告里写明覆盖了几条轨迹。依赖 opencv-python-headless，不调用任何服务。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

FPS = 6
STILL_DIFF = 2.2      # 上身框内平均灰度差（0–255）低于它算「这一帧没动」——实测说话/干活的人 ≥ 4，定住的人 1–2


def detect(gray: np.ndarray, front: cv2.CascadeClassifier, side: cv2.CascadeClassifier) -> list[tuple[int, int, int, int]]:
    h = gray.shape[0]
    mins = max(18, h // 30)
    boxes = list(front.detectMultiScale(gray, 1.1, 6, minSize=(mins, mins)))
    for flip in (False, True):
        g = cv2.flip(gray, 1) if flip else gray
        for (x, y, w, hh) in side.detectMultiScale(g, 1.1, 6, minSize=(mins, mins)):
            if flip:
                x = gray.shape[1] - x - w
            boxes.append((x, y, w, hh))
    out: list[tuple[int, int, int, int]] = []
    for b in sorted(boxes, key=lambda b: -b[2]):          # 去重：中心落在已有框里的丢掉
        cx, cy = b[0] + b[2] / 2, b[1] + b[3] / 2
        if not any(o[0] <= cx <= o[0] + o[2] and o[1] <= cy <= o[1] + o[3] for o in out):
            out.append(tuple(int(v) for v in b))
    return out


def body_box(face: tuple[int, int, int, int], W: int, H: int) -> tuple[int, int, int, int]:
    x, y, w, h = face
    bx, by = max(0, x - w), max(0, y - h // 3)
    bw, bh = min(W - bx, w * 3), min(H - by, h * 4)
    return bx, by, bw, bh


def run(video: Path, still: float) -> tuple[list[str], int]:
    cap = cv2.VideoCapture(str(video))
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 24
    step = max(1, round(src_fps / FPS))
    front = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    side = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
    tracks: list[dict] = []
    prev = None
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if i % step:
            i += 1
            continue
        t = i / src_fps
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        H, W = gray.shape
        faces = detect(gray, front, side)
        for f in faces:
            box = body_box(f, W, H)
            cx = box[0] + box[2] / 2
            tr = next((tr for tr in tracks if abs(tr["cx"] - cx) < W * 0.12 and t - tr["last"] < 1.0), None)
            if tr is None:
                tr = {"cx": cx, "t": [], "d": [], "box": box, "last": t}
                tracks.append(tr)
            tr["cx"], tr["box"], tr["last"] = cx, box, t
            if prev is not None:
                x, y, w, h = box
                a = cv2.resize(gray[y:y + h, x:x + w], (64, max(8, int(64 * h / max(w, 1)))))
                b = cv2.resize(prev[y:y + h, x:x + w], a.shape[::-1])
                tr["t"].append(t)
                tr["d"].append(float(np.mean(cv2.absdiff(a, b))))
        prev = gray
        i += 1
    cap.release()
    W = W if prev is not None else 1
    report = []
    real = [tr for tr in tracks if len(tr["t"]) >= FPS * 2]
    for tr in real:
        pos = "左" if tr["cx"] < W / 3 else ("右" if tr["cx"] > 2 * W / 3 else "中")
        run_start = None
        end = tr["t"][-1] + 1.0 / FPS
        for t, d in zip(tr["t"] + [end], tr["d"] + [99.0]):
            if d < STILL_DIFF:
                run_start = t if run_start is None else run_start
            else:
                if run_start is not None and t - run_start >= still:
                    report.append(f"画面{pos}的人 {run_start:.1f}–{t:.1f} 秒静止 {t - run_start:.1f} 秒")
                run_start = None
    return report, len(real)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--still", type=float, default=1.5)
    a = ap.parse_args()
    report, n = run(a.video, a.still)
    print(f"人物轨迹 {n} 条（只覆盖检测得到脸的人）")
    for r in report:
        print("  ⚠", r)
    if not report:
        print("  未见单人静止超过 %.1f 秒（仍要看拼图确认）" % a.still)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
