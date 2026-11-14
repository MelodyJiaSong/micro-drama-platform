"""p29 竖握合成：月刃旋转 90°（开口朝身体、外缘刃口朝外），兽颅护手单独转回正，握把中心对准拳心。
用法: composite_vertical.py <底图> <抠好的月刃RGBA> <输出> <月刃竖向长度px> <左拳x,y> <右拳x,y>"""
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
base_p, glaive_p, out_p = sys.argv[1:4]
L = float(sys.argv[4])
guesses = [tuple(map(int, g.split(","))) for g in sys.argv[5:7]]
GRIP, DISC, R = (1024, 1130), (1026, 1380), 236          # 锚点图坐标：握把中心、护手圆心、半径
g0 = Image.open(glaive_p).convert("RGBA")

def upright_disc(img, pre_angle):
    """把护手圆盘先反向转 pre_angle，整体旋转后它就是正的。"""
    x, y = DISC
    disc = img.crop((x - R, y - R, x + R, y + R))
    mask = Image.new("L", disc.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
    rot = disc.rotate(pre_angle, resample=Image.BICUBIC)
    out = img.copy(); out.paste(rot, (x - R, y - R), mask)
    return out

def make(side):
    W, H = g0.size
    if side == "L":   # 开口朝右：顺时针 90°
        img = upright_disc(g0, 90).rotate(-90, expand=True, resample=Image.BICUBIC)
        grip = (H - 1 - GRIP[1], GRIP[0])
    else:             # 开口朝左：逆时针 90°
        img = upright_disc(g0, -90).rotate(90, expand=True, resample=Image.BICUBIC)
        grip = (GRIP[1], W - 1 - GRIP[0])
    bb = img.getbbox(); img = img.crop(bb); grip = (grip[0] - bb[0], grip[1] - bb[1])
    s = L / img.height
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    return img, (grip[0] * s, grip[1] * s)

base = Image.open(base_p).convert("RGBA"); A = np.asarray(base.convert("RGB")).astype(int)
sat = A.max(-1) - A.min(-1)
out = base.copy(); fists = []
for side, guess in zip("LR", guesses):
    x0, y0 = guess[0] - 60, guess[1] - 60
    box = sat[y0:y0 + 120, x0:x0 + 120] > 18
    lab, n = ndi.label(box); sizes = ndi.sum(box, lab, range(1, n + 1))
    m = lab == (np.argmax(sizes) + 1)
    ys, xs = np.where(m); cx, cy = x0 + xs.mean(), y0 + ys.mean()
    img, grip = make(side)
    out.alpha_composite(img, (round(cx - grip[0]), round(cy - grip[1])))
    fists.append((x0, y0, m)); print(side, "fist", round(cx), round(cy), "glaive", img.size)
for x0, y0, m in fists:
    m2 = ndi.binary_dilation(m, iterations=2)
    alpha = (ndi.gaussian_filter(m2.astype(float), 1.0) * 255).astype(np.uint8)
    patch = base.crop((x0, y0, x0 + 120, y0 + 120)); patch.putalpha(Image.fromarray(alpha))
    out.alpha_composite(patch, (x0, y0))
out.convert("RGB").save(out_p)
