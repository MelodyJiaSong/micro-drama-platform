"""把抠好的 p29 月刃按比例贴到无武器底图的两只拳头下，拳头再盖回最上层。"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
base_p, glaive_p, out_p = sys.argv[1:4]
GW = float(sys.argv[4]) if len(sys.argv) > 4 else 634     # 月刃目标宽（px）
base = Image.open(base_p).convert("RGBA"); A = np.asarray(base.convert("RGB")).astype(int)
sat = A.max(-1) - A.min(-1)
gl = Image.open(glaive_p); bb = gl.getbbox(); gl = gl.crop(bb)
GRIP = (1024 - bb[0], 1130 - bb[1])                         # 锚点图握把中心（原图坐标）→ 裁切后坐标
s = GW / gl.width
gls = gl.resize((round(gl.width * s), round(gl.height * s)), Image.LANCZOS)
grip = (GRIP[0] * s, GRIP[1] * s)
out = base.copy()
fists = []
for guess in [tuple(map(int, g.split(","))) for g in sys.argv[5:7]]:
    x0, y0 = guess[0] - 60, guess[1] - 60
    box = sat[y0:y0 + 120, x0:x0 + 120] > 18
    lab, n = ndi.label(box); sizes = ndi.sum(box, lab, range(1, n + 1))
    m = lab == (np.argmax(sizes) + 1)
    ys, xs = np.where(m); cx, cy = x0 + xs.mean(), y0 + ys.mean()
    fists.append((cx, cy, x0, y0, m))
    out.alpha_composite(gls, (round(cx - grip[0]), round(cy + 6 - grip[1])))
    print("fist", round(cx), round(cy), "glaive", gls.size)
# 拳头盖回
for cx, cy, x0, y0, m in fists:
    m2 = ndi.binary_dilation(m, iterations=2)
    alpha = (ndi.gaussian_filter(m2.astype(float), 1.0) * 255).astype(np.uint8)
    patch = base.crop((x0, y0, x0 + 120, y0 + 120)); patch.putalpha(Image.fromarray(alpha))
    out.alpha_composite(patch, (x0, y0))
out.convert("RGB").save(out_p)
