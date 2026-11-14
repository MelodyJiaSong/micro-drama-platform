"""Depth Anything V2 (ONNX) -> 16-bit disparity PNG (normalized 0..65535, near = bright)."""
import sys
import numpy as np
import onnxruntime as ort
from PIL import Image

model, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert("RGB")
W, H = im.size
# multiples of 14; keep aspect, long side ~ 1022
tw = 1022
th = int(round(tw * H / W / 14)) * 14
x = np.asarray(im.resize((tw, th), Image.BICUBIC), dtype=np.float32) / 255.0
x = (x - np.array([0.485, 0.456, 0.406], np.float32)) / np.array([0.229, 0.224, 0.225], np.float32)
x = x.transpose(2, 0, 1)[None]
sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
name = sess.get_inputs()[0].name
out = sess.run(None, {name: x})[0]
d = np.squeeze(out).astype(np.float32)
d = np.asarray(Image.fromarray(d, mode="F").resize((W, H), Image.BICUBIC))
lo, hi = float(d.min()), np.percentile(d, 99.5)
d = np.clip((d - lo) / (hi - lo), 0, 1)
Image.fromarray((d * 65535).astype(np.uint16)).save(dst)
Image.fromarray((d * 255).astype(np.uint8)).save(dst.replace(".png", "_preview.png"))
print("depth", W, H, "->", dst)
