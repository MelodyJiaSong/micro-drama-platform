"""Build plate RGBA (sky cut out), lamp mask, star mask from plate + depth + sky.
usage: prep.py plate.png depth16.png sky.png outdir sky_thresh"""
import sys
import numpy as np
from PIL import Image, ImageFilter

plate, depth, sky, out = sys.argv[1:5]
thr = float(sys.argv[5]) if len(sys.argv) > 5 else 0.06
im = np.asarray(Image.open(plate).convert("RGB"), np.float32) / 255
d = np.asarray(Image.open(depth), np.float32) / 65535
H, W = d.shape

# sky = very far AND above the city silhouette; use column-wise first "solid" row from top
far = d < thr
alpha = np.ones((H, W), np.float32)
for x in range(W):
    col = far[:, x]
    # rows from top that are still sky until first non-sky run
    nz = np.where(~col)[0]
    top = nz[0] if len(nz) else H
    alpha[:top, x] = 0
a = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
rgba = np.dstack([im, np.asarray(a, np.float32) / 255])
Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").save(f"{out}/plate_rgba.png")

# lamp mask: warm & bright pixels (oil lamps), softened
lum = im @ np.array([0.2126, 0.7152, 0.0722], np.float32)
warm = (im[..., 0] > im[..., 2] * 1.6) & (lum > 0.32)
m = Image.fromarray((warm * alpha * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4))
Image.fromarray(np.clip(np.asarray(m, np.float32) * 2.5, 0, 255).astype(np.uint8)).save(f"{out}/lamp_mask.png")

# star mask on sky: local high-pass peaks
s = np.asarray(Image.open(sky).convert("L"), np.float32) / 255
bl = np.asarray(Image.fromarray((s * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
hp = np.clip((s - bl - 0.10) * 6, 0, 1)
Image.fromarray((hp * 255).astype(np.uint8)).save(f"{out}/star_mask.png")
print("alpha sky frac", 1 - alpha.mean(), "lamp px", int(warm.sum()))
