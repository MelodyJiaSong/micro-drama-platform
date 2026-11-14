"""Composite RGBA character frames over the plate, animating water regions of the still plate.
composite_anim.py plate.png frames_dir out_dir
"""
import sys, os, glob, math
import numpy as np
from PIL import Image, ImageFilter

plate, fdir, odir = sys.argv[1:4]
os.makedirs(odir, exist_ok=True)
files = sorted(glob.glob(os.path.join(fdir, "f*.png")))
first = Image.open(files[0]); Wo, Ho = first.size
P0 = Image.open(plate).convert("RGB")
sx, sy = Wo / P0.size[0], Ho / P0.size[1]
PL = np.asarray(P0.resize((Wo, Ho), Image.LANCZOS), np.float32) / 255

def rect(x0, y0, x1, y1):
    return int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy)
FALLS = [rect(1424, 420, 1462, 492), rect(1252, 496, 1304, 650)]   # spout, overflow sheet
# wet-street shimmer: bright pixels in the lower street area
yy, xx = np.mgrid[0:Ho, 0:Wo]
lum = PL @ np.array([0.2126, 0.7152, 0.0722], np.float32)
street = (yy > 470 * sy) & (xx > 470 * sx) & (xx < 1240 * sx)
wet = np.clip((lum - 0.45) * 4, 0, 1) * street
wet = np.asarray(Image.fromarray((wet * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), np.float32) / 255

def bilinear(img, X, Y):
    X = np.clip(X, 0, img.shape[1] - 1.001); Y = np.clip(Y, 0, img.shape[0] - 1.001)
    x0 = X.astype(int); y0 = Y.astype(int); fx = (X - x0)[..., None]; fy = (Y - y0)[..., None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy) +
            img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)

for k, f in enumerate(files):
    t = k / 24.0
    bg = PL.copy()
    for (x0, y0, x1, y1) in FALLS:
        h = y1 - y0
        sub = PL[y0:y1, x0:x1]
        period = max(8, h // 3)
        off = (t * 60.0) % period
        Y, X = np.mgrid[0:h, 0:x1 - x0].astype(np.float32)
        a = bilinear(sub, X + 0.6 * np.sin(Y * 0.5 + t * 9), (Y - off) % h)
        b = bilinear(sub, X + 0.6 * np.sin(Y * 0.5 + t * 9 + 2), (Y - off - period / 2) % h)
        w = (0.5 + 0.5 * np.cos(2 * math.pi * off / period))
        flow = a * w + b * (1 - w)
        # feather the patch edges
        ex = np.minimum(X, (x1 - x0 - 1) - X) / 4; ey = np.minimum(Y, h - 1 - Y) / 4
        m = np.clip(np.minimum(ex, ey), 0, 1)[..., None]
        bg[y0:y1, x0:x1] = sub * (1 - m) + flow * m
    # shimmer on wet street: small travelling displacement
    dx = 0.9 * np.sin(yy * 0.35 - t * 7.0) * wet
    dy = 0.5 * np.sin(xx * 0.21 + t * 5.0) * wet
    bg = bilinear(bg, xx + dx, yy + dy)
    im = np.asarray(Image.open(f).convert("RGBA"), np.float32) / 255
    a = im[..., 3:4]
    out = im[..., :3] * a + bg * (1 - a)
    Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(odir, os.path.basename(f)))
print("composited", len(files))
