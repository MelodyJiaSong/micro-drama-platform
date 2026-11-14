"""把 p29 锚点图抠成透明 PNG：背景 = 与边框连通的低梯度区域。"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
src, out, chk = sys.argv[1], sys.argv[2], sys.argv[3]
rgb = np.asarray(Image.open(src).convert("RGB")).astype(float)
g = ndi.gaussian_filter(rgb.mean(-1), 2.0)
grad = np.hypot(ndi.sobel(g, 0), ndi.sobel(g, 1))
sat = rgb.max(-1) - rgb.min(-1)
for t in (6, 8, 10, 14):
    smooth = grad < t
    lab, n = ndi.label(smooth)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bgm = np.isin(lab, border[border > 0])
    fg = ndi.binary_fill_holes(ndi.binary_closing(~bgm, iterations=3))
    fg = ndi.binary_opening(fg, iterations=3)
    ys, xs = np.where(fg)
    print(t, "fg frac %.3f" % fg.mean(), "bbox", xs.min(), ys.min(), xs.max(), ys.max())
t = int(sys.argv[4]) if len(sys.argv) > 4 else 8
smooth = grad < t
lab, n = ndi.label(smooth)
border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
bgm = np.isin(lab, border[border > 0])
fg = ndi.binary_fill_holes(ndi.binary_closing(~bgm, iterations=3))
fg = ndi.binary_opening(fg, iterations=3)
# 只留最大连通块（去掉背景斑点、地面阴影碎块）：先腐蚀断开薄连接，再膨胀回来
core = ndi.binary_erosion(fg, iterations=8)
lab2, n2 = ndi.label(core)
sizes = ndi.sum(fg, lab2, range(1, n2 + 1))
fg = ndi.binary_dilation(lab2 == (np.argmax(sizes) + 1), iterations=8) & fg
# 握把窗口：最大块内部的平滑、接近背景色的封闭洞
alpha = ndi.gaussian_filter(fg.astype(float), 1.0)
rgba = np.dstack([rgb.astype(np.uint8), (alpha * 255).astype(np.uint8)])
ys, xs = np.where(fg); print("final bbox", xs.min(), ys.min(), xs.max(), ys.max())
Image.fromarray(rgba, "RGBA").save(out)
bg = Image.new("RGBA", (rgba.shape[1], rgba.shape[0]), (255, 0, 255, 255)); bg.alpha_composite(Image.fromarray(rgba, "RGBA"))
bg.convert("RGB").resize((1024, 1024)).save(chk)
