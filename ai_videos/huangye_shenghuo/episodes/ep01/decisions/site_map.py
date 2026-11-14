"""EP01 场地俯视图 + 门口视线剖面（按 decisions/story.md「地形与房子」锁定坐标画）。
坐标：x 向东、y 向南（米），原点＝锚点树树干中心；阶地顶 z=0。
运行：python ai_videos/huangye_shenghuo/episodes/ep01/decisions/site_map.py  → 同目录 site_map.png
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = Path(__file__).with_name("site_map.png")

# ---- 锁定数值 ----
BANK_X, BANK_FOOT_X = -11.0, -11.6          # 阶地西缘（岩坎顶）、岩壁脚
STREAM_W_X = -21.5                           # 平水时溪西岸（砾石滩东沿）
GRAVEL = (-29.0, -21.5, -6.0, 8.0)           # 对岸砾石滩 x0,x1,y0,y1
TREES_X = -30.0                              # 对岸挂漂积物的那排树
Z_STREAM, Z_FLOOD, Z_GRAVEL, Z_FAR = -4.5, -2.0, -4.3, -3.0
DOOR_X, EYE = -4.6, 1.65                     # 门、门口跪姿眼高（离阶地面）
PLAT = (-4.6, -1.8, -1.1, 1.1)
GIANT = (-10.0, -18.0)

fig = plt.figure(figsize=(16, 15), dpi=110)
gs = fig.add_gridspec(2, 1, height_ratios=[1.35, 1.0], hspace=0.18)

# ================= 俯视图 =================
ax = fig.add_subplot(gs[0])
P = lambda x, y: (x, -y)                     # 画图时北朝上：y 向南 → 取负
# 阶地
ax.add_patch(Rectangle((BANK_X, -22), 16 - BANK_X, 44, color="#e9e2cf", zorder=0))
ax.text(7, 9, "东岸阶地\n（比平水面高 4.5 米）", fontsize=12, color="#6b5a3a", ha="center")
# 岩坎
ax.add_patch(Rectangle((BANK_FOOT_X, -22), BANK_X - BANK_FOOT_X, 44, color="#9a9a9a", zorder=1))
ax.text(BANK_X + 0.3, -20.5, "灰色岩坎（陡岸）", fontsize=10, color="#555", rotation=90, va="bottom")
# 洪水范围
ax.add_patch(Rectangle((-34, -22), BANK_FOOT_X + 34, 44, facecolor="#c9a27a", alpha=0.35, hatch="//", edgecolor="#8a5a2b", lw=0, zorder=1))
# 平水溪
ax.add_patch(Rectangle((STREAM_W_X, -22), BANK_FOOT_X - STREAM_W_X, 44, color="#8fc1e3", zorder=2))
ax.text((STREAM_W_X + BANK_FOOT_X) / 2, 13.5, "溪（平水）\n宽约 10 米\n由北往南流", fontsize=11, ha="center", color="#1d4f73")
ax.annotate("", xy=((STREAM_W_X + BANK_FOOT_X) / 2, -14), xytext=((STREAM_W_X + BANK_FOOT_X) / 2, 9),
            arrowprops=dict(arrowstyle="->", color="#1d4f73", lw=1.5))
# 砾石滩
x0, x1, y0, y1 = GRAVEL
ax.add_patch(Rectangle(P(x0, y1), x1 - x0, y1 - y0, color="#d8d2c4", ec="#999", zorder=3))
ax.text((x0 + x1) / 2, -(y0 + y1) / 2, "对岸砾石滩\n（平水时露出，\n洪水淹没）", fontsize=10, ha="center", va="center")
# 对岸树 + 泥痕
for yy in (-4, 0, 4, 8):
    ax.add_patch(Circle(P(TREES_X, yy), 0.5, color="#5a7d4a", zorder=4))
ax.text(TREES_X - 0.8, -12, "挂枯枝、带泥痕的那排树\n（泥痕＝洪水线，\n比平水高 2.5 米）", fontsize=9.5, ha="right", va="center")
ax.text(-33.5, 15.5, "洪水范围\n（平水面 +2.5 米）", fontsize=10, color="#7a4a1b", ha="left")
# 巨树
ax.add_patch(Circle(P(*GIANT), 1.4, color="#6f8a5c", zorder=5))
for dx, dy in ((2.6, 1.6), (-2.2, 2.0), (1.8, -2.4), (-2.6, -1.4)):
    ax.plot([GIANT[0], GIANT[0] + dx], [-GIANT[1], -(GIANT[1] + dy)], color="#6f8a5c", lw=5, solid_capstyle="round", zorder=4)
ax.text(GIANT[0] + 3.2, -GIANT[1] - 1.5, "巨树（最高，不选）", fontsize=10.5)
# 锚点树 + 树根
ax.add_patch(Circle((0, 0), 0.5, color="#4d6b3c", zorder=6))
for dx, dy in ((1.5, -3.5), (2.5, 2.8), (-1.6, -2.6), (-1.5, 2.7), (3.0, 0.3)):
    ax.plot([0, dx], [0, -dy], color="#7c8f5f", lw=4, solid_capstyle="round", zorder=5)
ax.text(0.8, 1.2, "锚点树（树干 Ø1 米）", fontsize=10.5)
# 房子：檐口外廓、平台、门、雨棚、踏木、灶、床
ax.add_patch(Rectangle((-4.6, -1.8), 2.8, 3.6, fill=False, ls="--", ec="#2e6b2e", lw=1.3, zorder=6))
ax.add_patch(Rectangle(P(PLAT[0], PLAT[3]), PLAT[1] - PLAT[0], PLAT[3] - PLAT[2], color="#c7a46b", ec="#7a5a2a", zorder=7))
ax.plot([-4.6, -4.6], [-0.35, 0.35], color="#a0201b", lw=4, zorder=8)
ax.add_patch(Rectangle((-5.4, -0.6), 0.8, 1.2, fill=False, ec="#2e6b2e", lw=1, zorder=7))
ax.plot([-4.9, -4.9], [-0.8, 0.8], color="#7a5a2a", lw=3, zorder=7)
ax.add_patch(Rectangle((-4.0, -0.3), 0.8, 0.6, color="#c46a3c", zorder=8))
ax.add_patch(Rectangle((-2.6, -1.0), 0.8, 2.0, color="#8fae6a", zorder=8))
for sx in (-1.8, -4.6):
    for sy in (-1.5, 1.5):
        ax.add_patch(Circle((sx, sy), 0.07, color="#5a3a1a", zorder=8))
ax.text(-3.2, 2.6, "小屋（平台 2.8×2.2 米，虚线＝檐口）", fontsize=10.5, ha="center", color="#2e5a1e")
ax.text(-4.75, 0.9, "门", fontsize=10, color="#a0201b", ha="right")
ax.text(-3.6, -0.55, "灶", fontsize=8.5, ha="center")
ax.text(-2.2, -1.25, "床", fontsize=8.5, ha="center")
# 排水沟
for sy in (-2.0, 2.0):
    ax.plot([-1.0, BANK_X], [-sy, -sy - (0.6 if sy > 0 else -0.6)], color="#b5653a", lw=1.2, ls=":", zorder=6)
ax.text(-8.5, -3.2, "排水沟（檐口外，通向陡岸）", fontsize=8.5, color="#b5653a")
# 对比帧 N1 机位
ax.add_patch(Polygon([(-10.5, 0), (-9.7, 0.45), (-9.7, -0.45)], color="#333", zorder=9))
ax.text(-8.6, 1.5, "对比帧机位 (N1, 24mm, 朝东)", fontsize=8.5, ha="center")
# 去材料、钓鱼的方向
ax.annotate("倒木林隙（材料）\n在阶地下游约 40 米", xy=(-4, -21.5), xytext=(2, -15.5), fontsize=9.5,
            arrowprops=dict(arrowstyle="->", color="#555"))
ax.annotate("潭尾（钓鱼）在下游", xy=(-16, -21.8), xytext=(-25, -17), fontsize=9.5, arrowprops=dict(arrowstyle="->", color="#555"))


# 距离标注
def dim(xa, xb, y, text, color="#a0201b", dy=0.6):
    ax.add_patch(FancyArrowPatch((xa, y), (xb, y), arrowstyle="<->", mutation_scale=12, color=color, lw=1.4, zorder=10))
    ax.text((xa + xb) / 2, y + dy, text, ha="center", fontsize=10, color=color, zorder=10,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))


dim(DOOR_X, BANK_X, -5.0, "门→岩坎边 6.4 米")
dim(DOOR_X, BANK_FOOT_X, -6.6, "门→平水溪东沿 7.0 米", dy=-1.1)
dim(DOOR_X, STREAM_W_X, -8.6, "门→砾石滩 16.9 米", dy=-1.1)
dim(DOOR_X, TREES_X, -10.6, "门→对岸泥痕那排树 25.4 米", dy=-1.1)
dim(-1.8, -0.5, 3.6, "东山墙→树干 1.3 米", color="#2e5a1e")
ax.set_xlim(-34, 16)
ax.set_ylim(-22, 22)
ax.set_aspect("equal")
ax.set_title("EP01 场地俯视图（北朝上；按锁定坐标，单位：米）", fontsize=15, pad=10)
ax.set_xlabel("x（向东，米）；原点＝锚点树树干")
ax.set_ylabel("南 ← y → 北")
ax.grid(color="#bbb", lw=0.4, alpha=0.5)
ax.text(14.5, 20.5, "N ↑", fontsize=16, ha="right", fontweight="bold")

# ================= 剖面 =================
bx = fig.add_subplot(gs[1])
bx.fill_between([BANK_X, 6], -6, 0, color="#e9e2cf")
bx.fill_between([BANK_FOOT_X, BANK_X], -6, [-4.6, 0], color="#9a9a9a")
bx.fill_between([STREAM_W_X, BANK_FOOT_X], -6, -5.2, color="#c9b99a")
bx.fill_between([-29, STREAM_W_X], -6, Z_GRAVEL, color="#d8d2c4")
bx.fill_between([-36, -29], -6, Z_FAR, color="#cdbf9f")
bx.fill_between([STREAM_W_X, BANK_FOOT_X], -5.2, Z_STREAM, color="#8fc1e3")
bx.fill_between([-36, BANK_FOOT_X], Z_FLOOD - 0.02, Z_FLOOD + 0.02, color="#8a5a2b")
bx.fill_between([-36, BANK_FOOT_X], [Z_STREAM] * 2, [Z_FLOOD] * 2, color="#c9a27a", alpha=0.35)
bx.text(-24, Z_FLOOD + 0.25, "洪水面（平水 +2.5 米，仍比阶地低 2 米）", fontsize=10, color="#7a4a1b", ha="center")
bx.text(-16.5, Z_STREAM - 0.55, "平水溪面（比阶地低 4.5 米）", fontsize=10, color="#1d4f73", ha="center")
bx.plot([TREES_X, TREES_X], [Z_FAR, 6], color="#5a7d4a", lw=6)
bx.plot([TREES_X - 0.4, TREES_X + 0.4], [Z_FLOOD, Z_FLOOD], color="#6b3d17", lw=3)
bx.text(TREES_X - 0.6, 3.5, "对岸那排树\n（泥痕＝洪水线）", fontsize=9.5, ha="right")
# 小屋
bx.add_patch(Rectangle((-4.6, 0.82), 2.8, 0.08, color="#c7a46b"))
bx.plot([-4.6, -4.6, -1.8, -1.8], [0, 0.9, 0.9, 0], color="#7a5a2a", lw=1.5)
bx.add_patch(Polygon([(-4.6, 0.9), (-4.6, 3.0), (-1.8, 3.0), (-1.8, 0.9)], fill=False, ec="#2e6b2e", lw=1.5))
bx.plot([-4.6, -4.6], [0.9, 2.1], color="#a0201b", lw=4)
bx.add_patch(Circle((0, 6), 0.0))
bx.plot([0, 0], [0, 6], color="#4d6b3c", lw=14, solid_capstyle="butt")
bx.text(0.7, 4.5, "锚点树", fontsize=10)
bx.text(-3.2, 3.3, "小屋（屋脊 3 米）", fontsize=10, ha="center")
# 视线
ex, ez = DOOR_X, EYE
k = (0 - ez) / (BANK_X - ex)                 # 擦过岩坎边的视线斜率
xs = [ex, -36]
bx.plot(xs, [ez, ez + k * (xs[1] - ex)], color="#a0201b", lw=1.6, ls="--")
x_flood = ex + (Z_FLOOD - ez) / k
x_norm = ex + (Z_STREAM - ez) / k
bx.plot([ex], [ez], "o", color="#a0201b")
bx.text(ex + 0.2, ez + 0.35, "门口跪姿眼高 1.65 米", fontsize=10, color="#a0201b")
bx.plot([x_flood], [Z_FLOOD], "v", color="#a0201b", ms=9)
bx.text(x_flood + 0.3, Z_FLOOD - 0.85, f"洪水时：视线在 x≈{x_flood:.0f}（离门约 {ex - x_flood:.0f} 米）碰到水面，\n从这里往西到对岸那排树的水面都高过视线 → 一开门就看见",
        fontsize=9.5, color="#a0201b")
bx.text(-35.5, -5.75, f"平水时：视线要到 x≈{x_norm:.0f}（离门约 {ex - x_norm:.0f} 米）才降到溪面高度，可溪在 7–17 米处，整条溪都在岩坎后面、视线下方 → 门口看不到溪水",
        fontsize=9.5, color="#1d4f73", bbox=dict(fc="white", ec="none", alpha=0.85))
bx.set_xlim(-36, 6)
bx.set_ylim(-6, 6.5)
bx.set_aspect("equal")
bx.set_title("沿门口往西的剖面（y=0；竖向与横向同比例）", fontsize=14)
bx.set_xlabel("x（向东，米）")
bx.set_ylabel("高度（米，阶地顶＝0）")
bx.grid(color="#bbb", lw=0.4, alpha=0.5)

fig.savefig(OUT, bbox_inches="tight")
print(OUT)
