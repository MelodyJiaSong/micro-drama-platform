"""follow-up 045：k401 后期版——底片 0388c4a1，重排成 斧→B→A→C→D，每跳画一道连接两只的电弧，跳跃段加速。"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = Path(__file__).parent
SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
W, H, FPS = 1280, 720, 24
fr = np.load(S / "v5_frames.npy")

B = (812, 395)
A = (601, 405)
C = (995, 405)
D = (1163, 400)

# 输出帧：(源帧号, [(起点, 终点), …], D 闪光强度)
seq = [(i, [], 0) for i in range(0, 64)]
seq += [(i, [], 0) for i in (64, 65, 66, 67, 69, 71, 73)]          # 斧 → B（底片自带）
# v3（用户：再慢一倍）：每跳 8 帧
seq += [(s, [(B, A)], 0) for s in range(81, 89)]                     # B → A
seq += [(100, [(A, C)], 0, 0.35)] + [(s, [(A, C)], 0) for s in range(101, 108)]   # A → C；100 是剪接点：全画面闪光遮跳变
seq += [(s, [(C, D)], f) for s, f in zip(range(108, 116), (1.0, 1.0, 1.0, 0.95, 0.9, 0.9, 0.85, 0.8))]  # C → D（D 的命中光补画）
seq += [(s, [], f) for s, f in ((116, 0.65), (117, 0.5), (118, 0.35))]
n_chain = len(seq) - 64
seq += [(i, [], 0) for i in range(119, len(fr))]
chain_src = (64 / FPS, 119 / FPS)
chain_out = (64 / FPS, (64 + n_chain) / FPS)


def bolt(p0, p1, rng, rough=0.22, depth=6):
    pts = [np.array(p0, float), np.array(p1, float)]
    disp = np.linalg.norm(pts[1] - pts[0]) * rough
    for _ in range(depth):
        new = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            m = (a + b) / 2
            d = b - a
            n = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-6)
            new += [m + n * rng.uniform(-disp, disp), b]
        pts = new
        disp *= 0.55
    return [tuple(p) for p in pts]


def arc_layer(p0, p1, rng):
    core = Image.new("L", (W, H))
    dc = ImageDraw.Draw(core)
    main = bolt(p0, p1, rng)
    dc.line(main, fill=255, width=5)
    for _ in range(rng.integers(3, 6)):                 # 细分叉
        k = rng.integers(len(main) // 5, len(main) * 4 // 5)
        s = np.array(main[k])
        ang = np.arctan2(p1[1] - p0[1], p1[0] - p0[0]) + rng.uniform(-1.2, 1.2)
        L = rng.uniform(25, 70)
        e = s + L * np.array([np.cos(ang), np.sin(ang)])
        dc.line(bolt(tuple(s), tuple(e), rng, 0.3, 4), fill=190, width=2)
    for p in (p0, p1):                                   # 两端命中火花
        r = 14
        dc.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=255)
    return core


def flash_layer(p, k, rng):
    lay = Image.new("L", (W, H))
    d = ImageDraw.Draw(lay)
    for _ in range(14):
        ang = rng.uniform(0, 2 * np.pi)
        L = rng.uniform(20, 75) * k
        d.line(bolt(p, (p[0] + L * np.cos(ang), p[1] + L * np.sin(ang)), rng, 0.3, 3), fill=int(220 * k), width=1)
    r = 16 * k
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=int(255 * k))
    return lay


def composite(img, layers):
    f = img.astype(np.float32) / 255
    add = np.zeros((H, W, 3), np.float32)
    for lay in layers:
        core = np.asarray(lay, np.float32) / 255
        g1 = np.asarray(lay.filter(ImageFilter.GaussianBlur(4)), np.float32) / 255
        g2 = np.asarray(lay.filter(ImageFilter.GaussianBlur(16)), np.float32) / 255
        g3 = np.asarray(lay.filter(ImageFilter.GaussianBlur(60)), np.float32) / 255
        add += core[..., None] * np.array([1.0, 1.0, 1.0])
        add += g1[..., None] * np.array([1.6, 1.9, 2.4])
        add += g2[..., None] * np.array([0.9, 1.3, 2.2])
        add += g3[..., None] * np.array([1.2, 1.6, 2.6])    # 照亮地面与身体的冷白蓝泛光
    out = 1 - (1 - f) * np.exp(-add)                         # 柔性加亮，不死白
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


rng = np.random.default_rng(45)
tmpv = S / "k401_post_video.mp4"
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
                        "-pix_fmt", "yuv420p", str(tmpv)], stdin=subprocess.PIPE)
for item in seq:
    src, arcs, fl = item[:3]
    gflash = item[3] if len(item) > 3 else 0
    img = fr[src]
    layers = [arc_layer(p0, p1, rng) for p0, p1 in arcs]
    if fl:
        layers.append(flash_layer(D, fl, rng))
    out = composite(img, layers) if layers else img
    if gflash:
        f = out.astype(np.float32) / 255
        out = (np.clip(1 - (1 - f) * (1 - gflash * np.array([0.75, 0.85, 1.0])), 0, 1) * 255).astype(np.uint8)
    enc.stdin.write(out.tobytes())
enc.stdin.close()
enc.wait()

# 音轨：跳跃段按同样比例压缩，其余原样
a0, a1 = chain_src
tempo = (a1 - a0) / (chain_out[1] - chain_out[0])
t1 = tempo / 2
fc = (f"[1:a]atrim=0:{a0},asetpts=PTS-STARTPTS[x];"
      f"[1:a]atrim={a0}:{a1},asetpts=PTS-STARTPTS,atempo=2.0,atempo={t1:.4f}[y];"
      f"[1:a]atrim=start={a1},asetpts=PTS-STARTPTS[z];[x][y][z]concat=n=3:v=0:a=1[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmpv), "-i", str(SRC), "-filter_complex", fc,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT)],
               check=True)
print(OUT, len(seq), "frames", f"{len(seq) / FPS:.2f}s", f"tempo {tempo:.2f}")
