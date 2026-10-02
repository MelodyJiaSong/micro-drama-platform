# -*- coding: utf-8 -*-
"""出片后逐次施法回读（follow-up 054 / 057；w28 §3 ⑧；shengji_zhilu lessons L12）。

文字闸门管得到「给 Seedance 的东西对不对」，管不到它画出来的光落没落在对的人身上。出片落盘后：

    python tools/cast_readback.py <shot 目录> [视频.mp4]

- 人在哪：previz 同一秒的 ID 色人偶（颜色唯一定义在 build_previz.COLORS）→ 每种颜色一个框、一块轮廓；同卡同色的几只分不开，
  合成一组。Seedance 跟白模走位（w28 实测时刻差约 ±0.35 s、位置大致跟），所以框放宽、轮廓外扩、时刻给容差。
- 光是什么色：这张卡这一阶段的色相带（skills_lib.card_hue，阶段可换法系色：保护祝福放手那一下是圣光金、光壳是银蓝），
  一次施法按色带分开查。查哪几段：锁定串写到了光的阶段（skills_lib.lit_phases）——空手一推、跪下按胸的
  手势段不查手上，冲锋这类目标只僵一下的技能不查目标身上。
- 背景逐像素估：同一机位段里只数这个像素没被人挡的帧；本技能色在这些帧里常在（施法前后以外也有空帧时，那里也常在）的是静止的同色背景
  （金条、地上的光带、墙上的火把、被挡住的金像露出的边），量的时候整块挖掉，不算谁的光。
- 人身上本来的颜色：他不亮的帧（避开所有同色施法前后）里轮廓内本技能色的低 / 高分位，同机位段优先；不够就借别的机位段，
  这时不低于本段他不在光里的帧的中位数（凑不到就不查）。判「亮了」扣高分位，判「没亮」扣低分位，落在两者之间的记未查——
  随身的金饰、盔甲的金边、挡在身前的静止金色都不算他亮了。
- 每次施法查：施法者手上亮没亮（要连着亮够一段，一闪不算）、光起得早晚（渐亮、切点前看不到的记未查）、目标身上亮没亮、
  生效光落没落反、被挡下时光离没离开施法者、别人框里有没有冒出同色光（串了）。同一时段别人自己的同色光那些帧不拿来比。
- 结论三态：通过 / 不通过 / 未查。查不成（人偶切不出来、不在画、量不到背景、分不清光和身上本来的颜色、目标对不上）
  一律记未查，不算通过。退出码：有不通过 1；只有未查 3；全通过 0。
人数 / 分身仍归 render_review R1。不通过就回排程闸门，或用 tools/cast_repair.py 只修这一个人——不改 prompt 碰运气。
"""
from __future__ import annotations

import ast
import bisect
import colorsys
import functools
import json
import subprocess
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import shot_overhead  # noqa: E402
import skills_lib  # noqa: E402
from previz import seedance_ref  # noqa: E402

W, H = 640, 360                 # 分析分辨率：previz 与出片都缩到这里
FPS = 8
DOLL_SAT_MIN = 0.5              # 人偶色饱和度低于它（白 / 灰 / 深灰）按色相切不出来
ID_HUE_TOL_MAX = 22.0           # 人偶色相容差上限（度）：previz 打光后实测蓝从 225° 偏到 210° 上下
ID_HUE_TOL_MIN = 7.0            # 与同镜别的颜色近到容差不足这么多，就分不开、不查
ID_GAP_SHARE = 0.45             # 容差取「与同镜最近颜色的色相差」的这个比例，两边色带不重叠
ID_SAT_MIN, ID_VAL_MIN = 0.30, 0.12
ID_MIN_PIX = 150                # 少于这么多像素算这人此刻不在画
PAD = 0.25                      # 框向外放宽的比例
DOLL_DILATE = 4                 # 人偶轮廓向外放宽的像素（分析分辨率下）：Seedance 画的人与白模只是大致重合
LIFT_MIN = 0.004                # 该亮的框里本技能色至少比基线多出框面积的这么多
BLEED_MAX = 0.003               # 别人框里多出这么多即判串了
ONSET_TOL = 1.0                 # 光起时刻的放行容差：光只写在 prompt 的整秒里、不在白模里；previz 代理（w28 MC-B）通过后收到 0.35
ONSET_RUN = 2                   # 连续这么多帧够 LIFT_MIN 才算起光；「没亮」要光晚到 DRIFT 之后还量到这么多帧暗的
LIT_RUN_S = 0.5                 # 「亮了」要连着亮这么久（他在该亮段里量得到的不到它两倍长时，取一半）：一闪而过、闪烁的火把不算
RUN_GAP = 4.0 / FPS             # 连着亮的两帧之间只隔着量不到的帧（切点两侧各一帧加切点本身、同色光重叠）、不超过这么久，不算断
BODY_SHARE = 0.5                # 多出来的光至少这么大一份落在人偶轮廓里：轮廓外扫过的同色物（火把、金旗）撑不起「亮了」
HAND_REACH = 2 * DOLL_DILATE    # 施法者手上的光离他轮廓这么近也算在他身上：接触式施法的手常伸出白模轮廓、落在框边
CONTACT_GROW = 8                # 目标身上查光时挖掉施法者轮廓外扩这么多像素的一圈：按在目标胳膊上的那只手
HIDDEN_MAX = 0.25               # 轮廓里被当成静止同色背景挖掉超过这个比例，光可能藏在那块里：不下「没亮」
MIN_CORE_FRAMES = 4             # 落反：两人同框量到的帧不足这么多、又不到同框帧的一半时不比
DRIFT = 0.5                     # 光可能晚到这么久（prompt 整秒取整；白模实测 ±0.35 s）
EARLY_LOOK = 1.0                # 光起时刻往容差前再多看这么久，找「早亮」；这段也不拿来估人本来的颜色
RAMP = 0.25                     # 晚过容差才够阈、之前已有 ONSET_RUN 帧稳亮到阈的这么多：渐亮，起光时刻要人看
STATIC_MIN_FRAMES = 4           # 一个像素要有这么多「空帧」（没被人挡、不挨着该亮的人）才知道它背后是什么
STATIC_SHARE = 0.25             # 空帧里本技能色占到这个比例：静止的同色背景
STATIC_GROW = 2                 # 静止背景向外放宽的像素：出片逐帧有一两个像素的抖动
SKIN_PCT = (10, 90)             # 人本来的颜色取他不亮时的这两个分位：判「没亮」扣低的，判「亮了」扣高的
SIL_MIN = 50                    # 轮廓（挖掉静止背景后）少于这么多像素的帧不拿来估人本来的颜色
MEASURE_MIN = 0.2               # 框里量得到的像素（挖掉静止背景与看不清背后的）不到这个比例，不下「没亮」「没串」的结论
BASE_MIN_FRAMES = 6             # 估人本来的颜色至少要这么多帧
REGION_SAMPLES = 24             # 估人本来的颜色最多取这么多帧
DUR_TOL = 0.6                   # 出片与 previz 差这么多以内算整条（cast_repair 判窗口 / 整条也用它）
ASPECT_TOL = 0.02
# blocked（被挡下）：光飞向目标、在他身前的挡板上炸开——挡的人是谁镜表里不写，这一段只查光离没离开施法者

Box = tuple[int, int, int, int]
Band = tuple[float, float, float, float]      # 色相 lo, hi（lo > hi 跨 0°）, 饱和度下限, 亮度下限
Win = tuple[float, float]


@dataclass(frozen=True)
class Doll:
    """previz 里一种颜色的人偶；同卡同色的几只分不开，合成一组。"""
    color: str
    hue: float
    tol: float
    labels: tuple[str, ...]       # 画面称呼（overhead label ＝ previz 角色.名）
    keys: tuple[str, ...]         # 人物卡目录

    @property
    def name(self) -> str:
        return "/".join(self.labels)


@dataclass(frozen=True)
class Clip:
    """整镜按 FPS 取的帧：时刻、各帧人偶框与轮廓、所在机位段、是否贴着切点，以及各色相带的特效像素。"""
    ts: list[float]
    bx: list[dict[int, Box]]
    dm: list[dict[int, np.ndarray]]      # 各帧人偶轮廓（np.packbits 压过的 H×W 布尔）
    px: list[dict[int, int]]             # 各帧人偶像素数（不到 ID_MIN_PIX、没成框的也记）
    seg: list[int]
    edge: list[bool]
    fx: dict[Band, list[np.ndarray]]


@dataclass(frozen=True)
class Back:
    """一个机位段里每个像素背后是什么：只数它的「空帧」——没被任何人偶挡住、也不在任何该亮的人框里的帧。"""
    known: np.ndarray             # 空帧够 STATIC_MIN_FRAMES
    static: np.ndarray            # 空帧里本技能色常在（≥ STATIC_SHARE，再放宽 STATIC_GROW）：静止的同色背景
    share: np.ndarray             # 空帧里本技能色出现的比例（float32）


@dataclass(frozen=True)
class Skin:
    """他身上本来的本技能色（轮廓内挖掉静止背景后的本技能色像素）的低 / 高分位：占轮廓、占整框各一份——随身的金饰
    跟着轮廓还是跟着框缩放说不准，判「亮了」取两种里扣得多的，判「没亮」取扣得少的。"""
    sil: tuple[float, float]
    box: tuple[float, float]
    borrowed: bool                # 同机位段凑不够，借了别的机位段
    held: tuple[float, float] | None = None     # 借的时候本段把高分位抬了上去：(本段下限, 别段高分位)，占轮廓


@dataclass(frozen=True)
class Lift:
    """一帧里一个人框中多出来的本技能色，占框面积。"""
    sure: float                   # 扣他本来颜色的高分位：够阈就一定是亮了
    most: float                   # 扣低分位：不够阈就一定没亮
    body: float                   # sure 里落在人偶轮廓内（施法者手上再放宽 HAND_REACH）的那份
    seen: float                   # 框里量得到的比例（挖掉静止背景、看不清背后的）
    hid: float                    # 轮廓里压在静止同色背景前、被挖掉的比例
    cov: float                    # 轮廓被别人（施法者、目标）的框或轮廓挖掉的比例
    own: tuple[float, float]      # 此刻扣的他本来的颜色（占轮廓）：低、高


@dataclass(frozen=True)
class Verdict:
    key: str
    name: str
    who: str
    target: str
    t: float
    status: str                   # pass / fail / unchecked
    lines: tuple[str, ...]
    peak_t: float | None


@functools.lru_cache(maxsize=1)
def _previz_ast() -> ast.Module:
    return ast.parse((REPO / "tools" / "previz" / "build_previz.py").read_text(encoding="utf-8"))


def palette() -> dict[str, tuple[float, float, float]]:
    """人偶色的唯一定义在 build_previz.COLORS；那个文件一 import 就要 bpy，这里只读出字面量。"""
    for node in _previz_ast().body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "COLORS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("tools/previz/build_previz.py 里找不到 COLORS")


def held_colors() -> set[str]:
    """build_previz 给持物（柄、盾）写死的颜色，即 _mat_for("褐") 这类调用的字面量：它们也会落进人偶的色带。"""
    return {n.args[0].value for n in ast.walk(_previz_ast())
            if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "_mat_for" and n.args
            and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)}


def previz_of(shot_dir: Path) -> tuple[Path, Path]:
    d = shot_dir / "previz"
    cfg, mp4 = d / "previz_config.toml", d / f"{shot_dir.name}_previz.mp4"
    for p in (cfg, mp4):
        if not p.is_file():
            raise SystemExit(f"{shot_dir.name}：没有 previz/{p.name}，施法回读要靠白模找人")
    return cfg, mp4


def _hue_gap(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def dolls(shot_dir: Path) -> tuple[list[Doll], list[str]]:
    """本镜能按色相切出来的人偶组；切不出来的写进说明。间距按本镜出现的全部饱和色算（人偶、道具、持物）。"""
    cfg_path, _ = previz_of(shot_dir)
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    key_of = {a.get("label", a["key"]): a["key"] for a in shot_overhead.load(shot_dir).get("actor", [])}
    pal = palette()
    names_of: dict[str, list[str]] = {}
    for r in cfg.get("角色", []):
        if "色" not in r:
            raise SystemExit(f"{shot_dir.name}：previz 角色「{r.get('名')}」没写色")
        names_of.setdefault(r["色"], []).append(r["名"])
    extra = {p["色"] for p in cfg.get("道具", []) if p.get("色")}
    if any(r.get("持物") for r in cfg.get("角色", [])):
        extra |= held_colors()
    hs: dict[str, tuple[float, float]] = {}
    for c in set(names_of) | extra:
        if c not in pal:
            raise SystemExit(f"{shot_dir.name}：previz 用了调色板里没有的颜色「{c}」")
        h, s, _ = colorsys.rgb_to_hsv(*pal[c])
        hs[c] = (h * 360.0, s)
    sat = {c: h for c, (h, s) in hs.items() if s >= DOLL_SAT_MIN}
    out: list[Doll] = []
    notes: list[str] = []
    for c, names in names_of.items():
        who = "/".join(names)
        if c not in sat:
            notes.append(f"{who}（{c}）按色相切不出来，不查")
            continue
        gap = min((_hue_gap(sat[c], h) for c2, h in sat.items() if c2 != c), default=360.0)
        tol = min(ID_HUE_TOL_MAX, ID_GAP_SHARE * gap)
        if tol < ID_HUE_TOL_MIN:
            near = "、".join(c2 for c2, h in sat.items() if c2 != c and _hue_gap(sat[c], h) == gap)
            notes.append(f"{who}（{c}）与{near}色相太近，切不出来，不查")
            continue
        if len(names) > 1:
            notes.append(f"{who} 同为{c}，按整群框查（串光阈值被摊薄）")
        out.append(Doll(c, sat[c], tol, tuple(names), tuple(sorted({key_of[n] for n in names if n in key_of}))))
    return out, notes


def labels(shot_dir: Path) -> dict[str, str]:
    """卡目录 → 画面称呼；同卡几只的称呼用「/」连起来。"""
    out: dict[str, str] = {}
    for a in shot_overhead.load(shot_dir).get("actor", []):
        lab = a.get("label", a["key"])
        out[a["key"]] = f"{out[a['key']]}/{lab}" if a["key"] in out else lab
    return out


def matches(groups: list[Doll], who: str) -> list[int]:
    return [i for i, g in enumerate(groups) if who in g.keys or who in g.labels]


def resolve(groups: list[Doll], who: str) -> int | None:
    """卡目录或称呼 → 人偶组下标；对不上、或同卡几只颜色不同分不出是哪只时为 None。"""
    hit = matches(groups, who)
    return hit[0] if len(hit) == 1 else None


def _run(cmd: list[str], video: Path, text: bool) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, capture_output=True, text=text, check=True)
    except subprocess.CalledProcessError:
        raise SystemExit(f"读不了 {video.name}（ffmpeg / ffprobe 报错）：文件可能还没写完（previz 还在渲染、出片还在下载），写完再跑") from None


def grab(video: Path, a: float, b: float) -> tuple[list[float], np.ndarray]:
    """[a, b] 秒按 FPS 取帧、缩到 W×H：(各帧时刻, N×H×W×3 uint8)。"""
    a = max(0.0, a)
    raw = _run(["ffmpeg", "-v", "error", "-ss", "%.3f" % a, "-t", "%.3f" % max(0.1, b - a), "-i", str(video),
                "-vf", "fps=%d,scale=%d:%d" % (FPS, W, H), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], video, False).stdout
    n = len(raw) // (W * H * 3)
    return [a + i / FPS for i in range(n)], np.frombuffer(raw[: n * W * H * 3], np.uint8).reshape(n, H, W, 3)


def stream(video: Path) -> tuple[float, int, int]:
    """视频流时长（不含比画面长的音轨）与宽高。"""
    out = _run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration,width,height",
                "-show_entries", "format=duration", "-of", "json", str(video)], video, True)
    j = json.loads(out.stdout)
    s = j["streams"][0]
    return float(s.get("duration") or j["format"]["duration"]), int(s["width"]), int(s["height"])


def hsv(img: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = img.astype(np.float32) / 255.0
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    mx = x.max(-1)
    d = mx - x.min(-1)
    dd = np.where(d > 1e-6, d, 1.0)
    h = np.where(mx == r, ((g - b) / dd) % 6.0, np.where(mx == g, (b - r) / dd + 2.0, (r - g) / dd + 4.0)) * 60.0
    return np.where(d > 1e-6, h, 0.0), np.where(mx > 1e-6, d / np.where(mx > 1e-6, mx, 1.0), 0.0), mx


def _dilate(m: np.ndarray, k: int) -> np.ndarray:
    c = np.pad(m.astype(np.int32), ((k + 1, k), (k + 1, k))).cumsum(0).cumsum(1)
    w = 2 * k + 1
    return (c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]) > 0


def dolls_px(frame: np.ndarray, groups: list[Doll]) -> tuple[dict[int, tuple[Box, np.ndarray]], dict[int, int]]:
    """previz 帧里每组人偶：框（取 2–98 分位，防背景零星同色像素把框拉大，再放宽 PAD）与轮廓（放宽 DOLL_DILATE 像素）；
    以及各组的像素数（不到 ID_MIN_PIX 的不成框，但记下数，好分清「太小」和「不在画」）。"""
    h, s, v = hsv(frame)
    ok = (s >= ID_SAT_MIN) & (v >= ID_VAL_MIN)
    out: dict[int, tuple[Box, np.ndarray]] = {}
    count: dict[int, int] = {}
    for i, g in enumerate(groups):
        m = ok & (np.abs((h - g.hue + 180.0) % 360.0 - 180.0) <= g.tol)
        ys, xs = np.nonzero(m)
        if len(xs):
            count[i] = len(xs)
        if len(xs) < ID_MIN_PIX:
            continue
        x0, x1 = np.percentile(xs, [2, 98])
        y0, y1 = np.percentile(ys, [2, 98])
        px, py = (x1 - x0) * PAD + 4, (y1 - y0) * PAD + 4
        box = (int(max(0, x0 - px)), int(max(0, y0 - py)), int(min(W, x1 + px + 1)), int(min(H, y1 + py + 1)))
        out[i] = (box, _dilate(m, DOLL_DILATE))
    return out, count


def dolls_in(frame: np.ndarray, groups: list[Doll]) -> dict[int, tuple[Box, np.ndarray]]:
    return dolls_px(frame, groups)[0]


def boxes(frame: np.ndarray, groups: list[Doll]) -> dict[int, Box]:
    return {i: b for i, (b, _) in dolls_in(frame, groups).items()}


def _arcs(lo: float, hi: float) -> list[Win]:
    return [(lo, hi)] if lo <= hi else [(lo, 360.0), (0.0, hi)]


def bands_meet(a: Band, b: Band) -> bool:
    """两条色相带在色环上有没有交集（任一条可以跨 0°）。"""
    return any(x0 <= y1 and y0 <= x1 for x0, x1 in _arcs(a[0], a[1]) for y0, y1 in _arcs(b[0], b[1]))


def _mask(h: np.ndarray, s: np.ndarray, v: np.ndarray, band: Band) -> np.ndarray:
    lo, hi, sat_min, val_min = band
    inb = (h >= lo) & (h <= hi) if lo <= hi else (h >= lo) | (h <= hi)
    return inb & (s >= sat_min) & (v >= val_min)


def fx_mask(frame: np.ndarray, band: Band) -> np.ndarray:
    return _mask(*hsv(frame), band)


def inside(t: float, wins: list[Win]) -> bool:
    return any(a <= t <= b for a, b in wins)


def clip_of(video: Path, previz: Path, cuts: list[float], groups: list[Doll], bands: set[Band]) -> Clip:
    d = stream(previz)[0]
    ts, prev = grab(previz, 0.0, d)
    bx: list[dict[int, Box]] = []
    dm: list[dict[int, np.ndarray]] = []
    px: list[dict[int, int]] = []
    for f in prev:
        found, count = dolls_px(f, groups)
        bx.append({g: b for g, (b, _) in found.items()})
        dm.append({g: np.packbits(m) for g, (_, m) in found.items()})
        px.append(count)
    del prev
    _, rend = grab(video, 0.0, d)
    n = min(len(ts), len(rend))
    fx: dict[Band, list[np.ndarray]] = {b: [] for b in bands}
    for i in range(n):
        h, s, v = hsv(rend[i])
        for b in bands:
            fx[b].append(_mask(h, s, v, b))
    return Clip(ts[:n], bx[:n], dm[:n], px[:n], [bisect.bisect_right(cuts, t + 1e-6) for t in ts[:n]],
                [any(abs(t - c) <= 1.0 / FPS for c in cuts) for t in ts[:n]], fx)


def body(clip: Clip, i: int, g: int) -> np.ndarray:
    return np.unpackbits(clip.dm[i][g], count=H * W).reshape(H, W).astype(bool)


def backs(clip: Clip, band: Band, casting: list[Win], glow: list[tuple[int, list[Win]]]) -> dict[int, Back]:
    """各机位段每个像素的背景。空帧：这个像素没被人偶挡住、也不在正在发光的人框里（glow：这条色相带上该亮的（人偶组, 时段））。
    casting：这条色相带上每次施法的整段时间窗（±ONSET_TOL）；窗外也有空帧的像素，静止还要窗外同样常见这个颜色——施法时的
    光圈、宽光柱只在窗里，不能当成静止背景把施法者站过的地方挖掉。"""
    fx = clip.fx[band]
    out: dict[int, Back] = {}
    for s in sorted(set(clip.seg)):
        free_n, on_n = np.zeros((H, W), np.int32), np.zeros((H, W), np.int32)
        free_o, on_o = np.zeros((H, W), np.int32), np.zeros((H, W), np.int32)
        for j in range(len(clip.ts)):
            if clip.seg[j] != s or clip.edge[j]:
                continue
            free = np.ones((H, W), bool)
            for g in clip.bx[j]:
                free &= ~body(clip, j, g)
            for g, wins in glow:
                if g in clip.bx[j] and inside(clip.ts[j], wins):
                    x0, y0, x1, y1 = clip.bx[j][g]
                    free[y0:y1, x0:x1] = False
            free_n += free
            on_n += fx[j] & free
            if not inside(clip.ts[j], casting):
                free_o += free
                on_o += fx[j] & free
        known = free_n >= STATIC_MIN_FRAMES
        share = (on_n / np.maximum(free_n, 1)).astype(np.float32)
        still = (share >= STATIC_SHARE) & ((free_o == 0) | (on_o >= STATIC_SHARE * free_o))
        out[s] = Back(known, _dilate(known & still, STATIC_GROW), share)
    return out


def _pct(v: float) -> str:
    return f"{v * 100:+.2f}%"


@dataclass(frozen=True)
class Run:
    """连着够阈的一段：首帧、末帧时刻，够阈的帧数。"""
    a: float
    b: float
    k: int

    @property
    def dur(self) -> float:
        return self.b - self.a + 1.0 / FPS


def _runs(seq: list[tuple[float, bool]]) -> list[Run]:
    """按时间排好的 (时刻, 够阈) → 连着够阈的各段。两帧够阈之间只隔着量不到的帧（不超过 RUN_GAP）不算断；单独一帧没够阈
    （压缩、动态模糊的掉帧）也不算断，但两次掉帧之间至少要连着亮两帧——亮一灭一的闪烁、隔几帧才闪一下的火把连不起来。"""
    out: list[Run] = []
    last: float | None = None
    dark, since = 0, 0
    for t, ok in seq:
        if not ok:
            dark += 1
            continue
        if out and last is not None and t - last <= RUN_GAP + 1e-6 and (dark == 0 or (dark == 1 and since >= 2)):
            out[-1] = Run(out[-1].a, t, out[-1].k + 1)
            since = 1 if dark else since + 1
        else:
            out.append(Run(t, t, 1))
            since = 1
        last, dark = t, 0
    return out


def check_cast(clip: Clip, card: skills_lib.Card, cast: skills_lib.Cast, band: Band, groups: list[Doll],
               label: dict[str, str], lit: list[tuple[int, list[Win]]], back: dict[int, Back],
               others: list[Win], only: frozenset[str] | None = None) -> Verdict:
    """一次施法在一条色相带上的检查（only：这条带管的阶段；None＝全部）。lit：同一时段别人自己的同色光（人偶组下标, 时段），
    这些 (人, 帧) 不拿来比，也不拿来估人本来的颜色。back：这条色相带各机位段的逐像素背景（backs）。others：别的同色施法的
    整段时间窗，谁本来的颜色都不从里面估。"""
    spans = skills_lib.phases(card, cast)
    mine = [(ph, a, b) for ph, a, b in spans if only is None or ph in only]
    lights = skills_lib.lit_phases(card, cast)
    t0 = min([cast.t] + [a for _, a, _ in spans])
    t1 = max(b for _, _, b in spans)
    self_all = [(a, b) for ph, a, b in spans if ph in skills_lib.SELF_PHASES]
    self_w = [(a, b) for ph, a, b in mine if ph in skills_lib.SELF_PHASES and ph in lights]
    tgt_w = [(a, b) for ph, a, b in mine if ph in skills_lib.TARGET_PHASES and ph in lights]
    block_w = [(a, b) for ph, a, b in mine if ph == "blocked"]
    first_other = min((a for ph, a, _ in spans if ph not in skills_lib.SELF_PHASES), default=float("inf"))
    last_self = max((b for _, b in self_all), default=float("-inf"))
    after_gather = min((a for ph, a, _ in spans if ph != "gather"), default=t1)
    self_cast = cast.target in ("", cast.who)
    aims = not self_cast and cast.outcome in ("成", "挡")          # 断 / 空：光没放出去，目标和旁人一样不该亮
    me = resolve(groups, cast.who)
    tg = me if self_cast else resolve(groups, cast.target)
    one_doll = aims and me is not None and me == tg                  # 异卡同色：施法者和目标是同一组人偶
    mixed = {g for g in (me, tg) if g is not None and len(set(groups[g].keys)) > 1}    # 他和别的卡同色一组，分不出是谁
    who_l = label.get(cast.who, cast.who)
    tgt_l = who_l if self_cast else label.get(cast.target, cast.target)
    known = set(label) | {x for v in label.values() for x in v.split("/")}
    head = f"{who_l} {card.key} {card.name} {cast.t:g}s（{cast.outcome}）→ {tgt_l}"
    ts, fx, n = clip.ts, clip.fx[band], len(clip.ts)
    lines: list[str] = []
    fails, missing = 0, 0
    peak_t: float | None = None

    def bad(msg: str) -> None:
        nonlocal fails
        fails += 1
        lines.append(f"✗ {head}：{msg}")

    def unchecked(msg: str) -> None:
        nonlocal missing
        missing += 1
        lines.append(f"· {head}：{msg}，未查")

    if not n or ts[-1] + 1.0 / FPS < t1 - 1.0 / FPS:
        unchecked(f"出片只到 {ts[-1] + 1.0 / FPS if n else 0:.1f}s，施法到 {t1:g}s，尾巴没拍进来")
        return Verdict(card.key, card.name, cast.who, cast.target, cast.t, "unchecked", tuple(lines), None)
    tol = ONSET_TOL
    glow = list(lit)                                   # 每个人该亮的时段：别人的同色光 + 本次施法
    if me is not None:
        glow.append((me, [(t0 - tol, t1 + tol)] if self_cast else [(a - tol, b + tol) for a, b in self_all]))
    if aims and tg is not None:
        glow.append((tg, [(after_gather - tol, t1 + tol)]))
    busy = {(i, g) for g, wins in lit for i in range(n) if inside(ts[i], wins)}
    shining = [{g for g, wins in glow if inside(ts[i], wins)} for i in range(n)]
    glowing = [(me, [(t0, t1)] if self_cast else self_all), (tg, [(after_gather, t1)] if aims else [])]
    lit_now = [{g for g, wins in glowing if g is not None and inside(ts[i], wins)} for i in range(n)]   # 卡上此刻该亮（不放宽容差）
    quiet = (t0 - tol - EARLY_LOOK, t1 + tol)          # 本次施法前后：错光可能整段挂在谁身上，谁本来的颜色都不从这段估
    near = [quiet] + others
    at = {t: i for i, t in enumerate(ts)}

    @functools.lru_cache(maxsize=512)
    def body_of(i: int, g: int) -> np.ndarray:
        return body(clip, i, g)

    def dens(g: int, k: int) -> tuple[float, float] | None:
        """g 在第 k 帧轮廓内（挖掉静止背景）本技能色像素，占轮廓、占整框。"""
        x0, y0, x1, y1 = clip.bx[k][g]
        sil = body_of(k, g)[y0:y1, x0:x1] & ~back[clip.seg[k]].static[y0:y1, x0:x1]
        m, on = int(sil.sum()), float((fx[k][y0:y1, x0:x1] & sil).sum())
        return (on / m, on / ((x1 - x0) * (y1 - y0))) if m >= SIL_MIN else None

    def calm(g: int) -> list[int]:
        return [k for k in range(n) if not clip.edge[k] and g in clip.bx[k] and g not in shining[k]
                and (k, g) not in busy and not inside(ts[k], near)]

    def here(g: int, s: int) -> list[tuple[float, float]]:
        """本机位段他在画、卡上此刻不该亮（本次施法的阶段本身，不放宽容差）、也没被别人同色光照着的帧的轮廓密度。"""
        return [v for k in range(n) if clip.seg[k] == s and not clip.edge[k] and g in clip.bx[k] and g not in lit_now[k]
                and (k, g) not in busy and (v := dens(g, k)) is not None]

    @functools.cache
    def skin(g: int, s: int) -> Skin | None:
        """g 身上本来的本技能色：他在画、不亮、没被别人同色光照着、又不挨着任何同色施法的帧，同机位段优先。同段不够就借全镜的，
        这时高分位不低于本段他不在光里的帧的中位数（凑不到 ONSET_RUN 帧就不借）——他站着不动时挡在身前的静止同色物，
        同段每一帧都有，别段没有；本次施法自己的光不算进去。"""
        pool = calm(g)
        same = [v for k in pool if clip.seg[k] == s and (v := dens(g, k)) is not None]
        borrowed = len(same) < BASE_MIN_FRAMES
        vals = same if not borrowed else [v for k in pool[:: max(1, len(pool) // REGION_SAMPLES)] if (v := dens(g, k)) is not None]
        if len(vals) < BASE_MIN_FRAMES:
            return None
        lo, hi = ([float(np.percentile([v[j] for v in vals], p)) for j in (0, 1)] for p in SKIN_PCT)
        if not borrowed:
            return Skin((lo[0], hi[0]), (lo[1], hi[1]), False)
        own = here(g, s)
        if len(own) < ONSET_RUN:
            return None
        cap = [max([float(np.median([v[j] for v in own]))] + [v[j] for v in same]) for j in (0, 1)]
        held = (cap[0], hi[0]) if cap[0] > hi[0] else None
        return Skin((lo[0], max(hi[0], cap[0])), (lo[1], max(hi[1], cap[1])), True, held)

    @functools.cache
    def lift(g: int, i: int, minus: tuple[int | None, ...] = (), shade: tuple[int | None, ...] = (), reach: int = 0) -> Lift | None:
        """g 此刻框里多出来的本技能色。minus 各框整块挖掉；shade 各人挖掉轮廓外扩 CONTACT_GROW 的一圈（按在他身上的手）；
        reach：离轮廓这么近的光也算在他身上。轮廓外只量背后看清了、又不是静止同色背景的像素，扣它们平时的本技能色；
        轮廓内挖掉静止背景，扣他身上本来的颜色（高 / 低分位各算一个）。"""
        if clip.edge[i] or g not in clip.bx[i] or (i, g) in busy:
            return None
        sk = skin(g, clip.seg[i])
        if sk is None:
            return None
        x0, y0, x1, y1 = clip.bx[i][g]
        reg = np.ones((y1 - y0, x1 - x0), bool)
        for m in minus:
            if m is not None and m != g and m in clip.bx[i]:
                mx0, my0, mx1, my1 = clip.bx[i][m]
                ya, yb, xa, xb = max(my0, y0) - y0, min(my1, y1) - y0, max(mx0, x0) - x0, min(mx1, x1) - x0
                if ya < yb and xa < xb:
                    reg[ya:yb, xa:xb] = False
        for m in shade:
            if m is not None and m != g and m in clip.bx[i]:
                reg &= ~_dilate(body_of(i, m), CONTACT_GROW)[y0:y1, x0:x1]
        area = int(reg.sum())
        if not area:
            return None
        bk = back[clip.seg[i]]
        static = bk.static[y0:y1, x0:x1]
        known = bk.known[y0:y1, x0:x1]
        doll = body_of(i, g)[y0:y1, x0:x1]
        whole = int((doll & ~static).sum())
        in_reg = doll & reg
        sil = in_reg & ~static
        out = reg & ~doll & known & ~static
        f = fx[i][y0:y1, x0:x1]
        share = bk.share[y0:y1, x0:x1]
        o = int((f & out).sum()) - float(share[out].sum())
        on_sil, n_sil = int((f & sil).sum()), int(sil.sum())
        per = (x1 - x0) * (y1 - y0) / max(whole, 1)          # 占整框的分位折成此刻轮廓上的密度
        hi, lo = max(sk.sil[1], sk.box[1] * per), min(sk.sil[0], sk.box[0] * per)
        inner = (on_sil - hi * n_sil) / area
        if reach:
            ring = _dilate(doll, reach) & out
            inner += (int((f & ring).sum()) - float(share[ring].sum())) / area
        return Lift((o + on_sil - hi * n_sil) / area, (o + on_sil - lo * n_sil) / area, inner, (n_sil + int(out.sum())) / area,
                    1.0 - n_sil / max(int(in_reg.sum()), 1), 1.0 - int(in_reg.sum()) / max(int(doll.sum()), 1), (lo, hi))

    def lit_(x: Lift, thr: float) -> bool:
        return x.sure >= thr and x.body >= BODY_SHARE * thr

    def clean(x: Lift, thr: float) -> bool:
        """量得到、确定没多出光（串色的旁人用：被施法者、目标的框挡住的部分不管）。"""
        return x.most < thr and x.seen >= MEASURE_MIN and x.hid <= HIDDEN_MAX

    def dark(x: Lift, thr: float) -> bool:
        """一定没亮：还要他的轮廓没被施法者挖掉一大块——光可能正落在被挖掉的那块上。"""
        return clean(x, thr) and x.cov <= HIDDEN_MAX

    def aside(x: Lift, thr: float) -> bool:
        """框里够阈，落在他轮廓里的却不到一半：光晕、比人宽的光柱，或身后扫过的同色物。"""
        return x.sure >= thr and x.body < BODY_SHARE * thr

    def no_skin(g: int, s: int) -> str:
        if len(here(g, s)) < ONSET_RUN:
            return "本机位段他在画时都在光里（这次施法的，或别人的同色光），没有他不亮的画面可比，分不清光和他身上本来的颜色"
        seen_k = [k for k in range(n) if not clip.edge[k] and g in clip.bx[k]]
        by_cast = [k for k in seen_k if inside(ts[k], near)]
        if len(by_cast) * 2 >= len(seen_k):
            merged: list[list[float]] = []
            for a, b in sorted(near):
                if merged and a <= merged[-1][1]:
                    merged[-1][1] = max(merged[-1][1], b)
                else:
                    merged.append([a, b])
            spans_txt = "、".join(f"{a:.1f}–{b:.1f}s" for a, b in merged)
            return (f"他在画的帧大多挨着这次或别的同色施法（{spans_txt} 不拿来估他本来的颜色），别的时候只有 {len(calm(g))} 帧、"
                    f"要 {BASE_MIN_FRAMES} 帧，分不清光和他身上本来的颜色")
        return "没有他不亮的画面可比（本机位段他一直在光里或被别人的同色光照着，别的机位段也凑不够），分不清光和他身上本来的颜色"

    def why(g: int, on: list[int], got: list[tuple[float, Lift]] | None = None, late_from: float | None = None,
            thr: float = LIFT_MIN, need: float | None = None) -> str:
        if not on:
            return f"previz 里这段不在画（或人偶太小，不到 {ID_MIN_PIX} 像素）"
        if len(on) < ONSET_RUN:
            return f"previz 里这段只有 {len(on)} 帧在画"
        sk = skin(g, clip.seg[on[0]])
        if sk is None:
            return no_skin(g, clip.seg[on[0]])
        got = got or []
        amb = [x for _, x in got if x.sure < thr <= x.most]
        low = [x for _, x in got if x.most < -thr]
        away = [x for _, x in got if aside(x, thr)]
        if len(away) >= ONSET_RUN:
            return (f"{len(away)} 帧框里多出了同色光（最多 {_pct(max(x.sure for x in away))}），落在他轮廓里的却不到一半："
                    f"光晕、比人宽的光柱，或身后扫过的同色物，不算他亮")
        if len(amb) >= ONSET_RUN and len(low) >= ONSET_RUN:
            return (f"{len(amb)} 帧分不清：他「不亮时」的样子里多半挂着光（或他身上的同色衣物这会儿被挡住了）——另有 {len(low)} 帧"
                    f"比那还暗 {_pct(-min(x.most for x in low))}，他本来的颜色估高了")
        if len(amb) >= ONSET_RUN and sk.held is not None:
            return (f"{len(amb)} 帧分不清：本机位段他身上一直有 {sk.held[0] * 100:.1f}% 这个颜色，别的机位段只有 "
                    f"{sk.sil[0] * 100:.1f}%–{sk.held[1] * 100:.1f}%——是整段挂着的光，还是挡在他身前的同色物")
        if len(amb) >= ONSET_RUN:
            lo, hi = min(x.own[0] for x in amb), max(x.own[1] for x in amb)
            return (f"{len(amb)} 帧分不清是光还是他身上本来的颜色（他不亮时轮廓里本技能色按站位折算在 {lo * 100:.1f}%–{hi * 100:.1f}% 之间"
                    + ("，借自别的机位段" if sk.borrowed else "") + "，扣多扣少差出了阈值：他身上这个颜色时有时无，或空闲帧里挂着早亮、拖尾的光）")
        parts = []
        hits = [(t, x) for t, x in got if lit_(x, thr)]
        if hits and need is not None:
            best = max(_runs([(t, lit_(x, thr)) for t, x in got]), key=lambda r: r.dur)
            parts.append(f"量到 {len(got)} 帧，够阈的 {len(hits)} 帧、最长连着 {best.dur:.2f}s（要 ≥ {need:.2f}s）")
        busy_n = sum((i, g) in busy for i in on)
        thin = [x for _, x in got if x.most < thr and x.seen < MEASURE_MIN]
        hid = [x for _, x in got if x.most < thr and x.seen >= MEASURE_MIN and x.hid > HIDDEN_MAX]
        cov = [x for _, x in got if clean(x, thr) and x.cov > HIDDEN_MAX]
        parts += ([f"{busy_n} 帧与别人同色的光重叠"] if busy_n else []) \
            + ([f"{len(thin)} 帧框里大半是静止的同色背景或看不清背后（量得到的不到 {MEASURE_MIN:.0%}）"] if thin else []) \
            + ([f"{len(hid)} 帧他身上一大块压在静止的同色背景前，光可能藏在那块里"] if hid else []) \
            + ([f"{len(cov)} 帧他被施法者挡住一大块，光可能正落在那块上"] if cov else [])
        if late_from is not None and not (thin or hid or cov):
            k = sum(1 for t, x in got if t >= late_from and dark(x, thr))
            parts.append(f"{late_from:.1f}s 之后只量到 {k} 帧暗的，光晚到 {DRIFT:g}s 以内也看不见")
        return "、".join(parts) or "量不成"

    def who_msg(name: str) -> str:
        return f"「{label.get(name, name)}」" + ("对不上本镜的人" if name not in known else
                                                "同卡几只颜色不同、分不出是哪只" if len(matches(groups, name)) > 1 else "的人偶切不出来")

    def measure(g: int, core: list[Win], exp: list[Win], cut: tuple = ((), (), 0)
                ) -> tuple[list[tuple[float, Lift]], list[int], list[int]]:
        """(容差窗内量到的 (时刻, 多出来的光)，本体里在画的帧，其中不被别人同色光占着的帧)。容差只在量到的机位段里放宽。
        cut：lift 的 (minus, shade, reach)。"""
        on_all = [i for i in range(n) if inside(ts[i], core) and not clip.edge[i] and g in clip.bx[i]]
        on = [i for i in on_all if (i, g) not in busy]
        segs = {clip.seg[i] for i in on if lift(g, i, *cut) is not None}
        got = [(ts[i], x) for i in range(n) if inside(ts[i], exp) and clip.seg[i] in segs and (x := lift(g, i, *cut)) is not None]
        return got, on_all, on

    def borrowed_note(g: int, t: float) -> str:
        sk = skin(g, clip.seg[at[t]])
        return "；他不亮的样子借自别的机位段" if sk is not None and sk.borrowed else ""

    def presence(g: int | None, name: str, core: list[Win], exp: list[Win], side: str,
                 cut: tuple = ((), (), 0)) -> tuple[str, list[tuple[float, Lift]]]:
        """亮了：连着亮够 need（LIT_RUN_S；他在本体里量得到的不足它两倍时取一半）。一闪一闪连不成段的、光落在轮廓外的，记未查。
        没亮：本体一半以上量得到，光晚到 DRIFT 之后、本体结束 DRIFT 之内还量到 ONSET_RUN 帧一定没亮的，且分不清的帧不到
        ONSET_RUN；否则记未查。"""
        nonlocal peak_t
        if g is None:
            unchecked(f"{side}：{who_msg(name)}")
            return "n/a", []
        if g in mixed:
            unchecked(f"{side}：{groups[g].name} 和别的卡同色一组，分不出光落在谁身上")
            return "n/a", []
        got, on_all, on = measure(g, core, exp, cut)
        n_ok = sum(1 for i in on if lift(g, i, *cut) is not None)
        cover = f"（量到 {n_ok}/{len(on)} 帧）" if on and n_ok < len(on) else ""
        need = max(ONSET_RUN / FPS, min(LIT_RUN_S, n_ok / FPS / 2))      # 按他在这段里量得到的时长算：晚入画的只露一小截
        seq = [(t, lit_(x, LIFT_MIN)) for t, x in got]
        runs = [r for r in _runs(seq) if r.k >= ONSET_RUN]
        best = max(runs, key=lambda r: r.dur, default=None)
        if best is not None and best.dur >= need - 1e-6:
            t_pk, x_pk = max(((t, x) for t, x in got if best.a <= t <= best.b), key=lambda h: h[1].sure)
            lines.append(f"✓ {head}：{side}本技能色 {_pct(x_pk.sure)}，峰在 {t_pk:.1f}s{cover}{borrowed_note(g, t_pk)}")
            peak_t = t_pk
            return "lit", got
        hits = [(t, x) for t, x in got if lit_(x, LIFT_MIN)]
        length = sum(b - a for a, b in core)
        if hits and not runs and length <= 3 / FPS + 1e-6:
            unchecked(f"{side}：只 {len(hits)} 帧够阈（峰 {_pct(max(x.sure for _, x in hits))}）——这一段本身只有 {length:.2f}s，"
                      f"按每秒 {FPS} 帧可能只采到一帧，要人看" + cover)
            return "n/a", got
        if len(hits) >= max(2 * ONSET_RUN, n_ok / 3):
            longest = max(_runs(seq), key=lambda r: r.dur)
            unchecked(f"{side}：一闪一闪——量到 {len(got)} 帧，够阈的 {len(hits)} 帧，最长连着 {longest.dur:.2f}s、连不成段"
                      f"（要 ≥ {need:.2f}s）：是闪烁的光还是反光要人看" + cover)
            return "n/a", got
        start = next((ts[i] for i in on if lift(g, i, *cut) is not None), core[0][0])
        late_from, late_to = start + DRIFT, max(b for _, b in core) + DRIFT
        late = [x for t, x in got if late_from <= t <= late_to and dark(x, LIFT_MIN)]
        amb = [x for _, x in got if x.sure < LIFT_MIN <= x.most or aside(x, LIFT_MIN)]
        if len(late) >= ONSET_RUN and len(amb) < ONSET_RUN and n_ok >= ONSET_RUN and 2 * n_ok >= len(on_all):
            if hits:
                longest = max(_runs(seq), key=lambda r: r.dur)
                bad(f"{side}只亮了 {longest.dur:.2f}s（{len(hits)} 帧够阈，峰 {_pct(max(x.sure for _, x in hits))}），"
                    f"要连着亮 ≥ {need:.2f}s" + cover)
            else:
                usual = max(x.own[0] for x in late)
                bad(f"{side}本技能色最多 {_pct(max(x.most for x in late))}（阈 {LIFT_MIN * 100:g}%），没亮" + cover
                    + (f"——比他平时多不出来，而他平时轮廓里就有 {usual * 100:.0f}% 这个颜色：若是一直亮着，也是这样" if usual >= 0.05 else ""))
            return "dark", got
        unchecked(f"{side}：" + why(g, on_all, got, late_from if len(amb) < ONSET_RUN else None, need=need) + cover)
        return "n/a", got

    def onset(g: int, got: list[tuple[float, Lift]], cw: list[Win]) -> None:
        """光起时刻：往容差前再多看 EARLY_LOOK（跨切点也看）找早亮，只认一路连进容差窗里的那段光（早就断了的——上一次施法的
        拖尾、别人串过来的光、上一镜的金饰——不算）；它前一帧他在画却看不清（切点、同色光重叠、分不清），看不到几时起的。
        晚过容差的，之前已在渐亮就记未查，平地突起才判晚。"""
        card_t = self_w[0][0]
        enter = next((ts[i] for i in range(n) if inside(ts[i], cw) and not clip.edge[i] and g in clip.bx[i]), card_t)
        due = max(card_t, enter)                      # 施法者晚入画时，光最早也只能在他入画时看见
        due_txt = f"卡是 {card_t:g}s" + (f"，他 {enter:.1f}s 才入画，按入画算" if enter > card_t + 1e-6 else "")
        cut = ((), (), HAND_REACH)
        pre = [(ts[i], x) for i in range(n) if due - tol - EARLY_LOOK <= ts[i] < cw[0][0] and (x := lift(g, i, *cut)) is not None]
        series = sorted(pre + got, key=lambda p: p[0])
        runs = [r for r in _runs([(t, lit_(x, LIFT_MIN)) for t, x in series]) if r.k >= ONSET_RUN]
        main = next((r for r in runs if r.b >= due - tol - 1e-6), None)
        on_t = main.a if main else None
        first = series[0][0] if series else None
        if on_t is not None and on_t < due - tol:
            bad(f"光起在 {on_t:.1f}s" + ("（再往前量不到）" if on_t == first else "") + f"，早过{due_txt}（容差 ±{tol:g}s）")
            return
        if on_t is not None and on_t <= due + tol:
            before = [i for i in range(n) if on_t - 0.5 <= ts[i] < on_t and g in clip.bx[i] and not clip.edge[i]]
            last = lift(g, before[-1], *cut) if before else None
            if on_t > due - tol + 1e-6 and before and (last is None or not dark(last, LIFT_MIN)):
                unchecked(f"光起时刻：{on_t:.1f}s 已经亮着，前一帧（{ts[before[-1]]:.1f}s）他在画却看不清"
                          f"（切点前、与别人的同色光重叠，或分不清光和他本来的颜色），看不到几时起的（{due_txt}）")
            else:
                lines.append(f"✓ {head}：光起在 {on_t:.1f}s，{due_txt}")
            return
        probe = [x for t, x in series if due + tol - 0.5 <= t <= due + tol]
        if on_t is not None and len(probe) >= ONSET_RUN:
            ramp = [t for t, x in series if due - tol <= t < on_t and x.sure >= RAMP * LIFT_MIN]
            if len(ramp) >= ONSET_RUN:
                unchecked(f"光起时刻：{ramp[0]:.1f}s 起渐亮，{on_t:.1f}s 才够阈（{due_txt}，容差 ±{tol:g}s）；渐亮的光算几时起要人看")
            else:
                bad(f"光起在 {on_t:.1f}s，{due_txt}（晚过容差 {tol:g}s）")
        elif on_t is None and len(probe) >= ONSET_RUN and max(x.most for x in probe) < LIFT_MIN:
            bad(f"手上在 {due:.1f}s ±{tol:g}s 内没起光（{due_txt}）")
        else:
            k = sum(1 for t, _ in series if due - tol <= t <= due + tol)
            unchecked(f"光起时刻：{due_txt}；{due - tol:.1f}–{due + tol:.1f}s 量到 {k} 帧、容差边上 {len(probe)} 帧"
                      + (f"，{on_t:.1f}s 才连着够阈" if on_t is not None else "，没有连着两帧够阈的") + "，拿不准")

    hand = ((), (), HAND_REACH)
    dust = cast.outcome == "空" and "fizzle" in lights and not self_cast and "{目标}" in skills_lib.looks(card, cast).get("fizzle", "")
    if cast.outcome == "空" and "fizzle" in lights:
        # 卡里「没放出来」也写了光（光停在自己掌心里打转）：查手上有这团光；它没落到目标身上，归下面的串色查
        fz = [(a, b) for ph, a, b in spans if ph == "fizzle"]
        presence(me, cast.who, fz, [(a - tol, b + tol) for a, b in fz], f"施法者{who_l}手上（没放出去、停在掌心的光）", hand)
    elif cast.outcome == "空":
        if me is None:
            unchecked(f"施法者{who_l}手上：{who_msg(cast.who)}")
        elif me in mixed:
            unchecked(f"施法者{who_l}手上：{groups[me].name} 和别的卡同色一组，分不出光落在谁身上")
        else:
            got, on_all, on = measure(me, [(cast.t, t1)], [(cast.t - tol, t1 + tol)], hand)
            glare = [r for r in _runs([(t, lit_(x, LIFT_MIN)) for t, x in got]) if r.k >= ONSET_RUN]
            n_ok = sum(1 for i in on if lift(me, i, *hand) is not None)
            if glare:
                bad(f"该空的手上亮了（{glare[0].a:.1f}s 起 {glare[0].dur:.2f}s，"
                    f"{_pct(max(x.sure for t, x in got if glare[0].a <= t <= glare[0].b))}）")
            elif on and n_ok == len(on) and n_ok >= ONSET_RUN and all(dark(x, LIFT_MIN) for _, x in got):
                lines.append(f"✓ {head}：该空的手上没亮")
            else:
                cover = f"（量到 {n_ok}/{len(on)} 帧，没亮要全覆盖才算数）" if n_ok < len(on) else ""
                unchecked(f"施法者{who_l}手上：{why(me, on_all, got, need=ONSET_RUN / FPS)}{cover}")
    elif self_w:
        cw = [(a - tol, min(b + tol, first_other)) for a, b in self_w]      # 生效段起就不算手上的光（落反时它正罩在施法者身上）
        state, got = presence(me, cast.who, self_w, cw, f"施法者{who_l}手上", hand)
        if state == "lit" and me is not None:
            onset(me, got, cw)
    if tgt_w and one_doll:
        unchecked(f"目标{tgt_l}身上：施法者和目标是同色一组的人偶，分不出光落在谁身上")
    elif tgt_w:
        tw = [(max(a - tol, last_self), b + tol) for a, b in tgt_w]
        side = f"施法者{who_l}身上的生效光" if self_cast else f"目标{tgt_l}身上"
        # 目标轮廓里挖掉施法者轮廓外扩的一圈：接触式施法按在目标胳膊上的那只手，手上的光不算目标亮了
        state, _ = presence(tg, cast.who if self_cast else cast.target, tgt_w, tw, side, ((), () if self_cast else (me,), 0))
        if state != "n/a" and not self_cast and me is not None and tg is not None:
            # 生效光落反（光柱罩在施法者身上）：各自挖掉对方的框逐帧比；有人亮着的帧里，过半是施法者一定亮着、又比目标最多亮的
            # 还多才算。光可能晚到：生效段头上让过 DRIFT（短段让一半），尾巴放宽 DRIFT；蓄 / 放段不比
            core = [(a + min(DRIFT, (b - a) / 2), b + DRIFT) for a, b in tgt_w]
            both = [i for i in range(n) if inside(ts[i], core) and not clip.edge[i] and me in clip.bx[i] and tg in clip.bx[i]]
            pairs = [(x, y) for i in both if (x := lift(tg, i, (me,))) is not None and (y := lift(me, i, (tg,))) is not None]
            active = [(x, y) for x, y in pairs if lit_(x, LIFT_MIN) or lit_(y, LIFT_MIN)]
            rev = [(x, y) for x, y in active if lit_(y, LIFT_MIN) and y.sure > x.most and x.seen >= MEASURE_MIN]
            if len(pairs) >= ONSET_RUN and (len(pairs) >= MIN_CORE_FRAMES or 2 * len(pairs) >= len(both)) \
                    and len(rev) >= max(ONSET_RUN, (len(active) + 1) // 2):
                bad(f"生效光在{who_l}身上（{_pct(float(np.median([y.sure for _, y in rev])))}）反而多于{tgt_l}"
                    f"（最多 {_pct(float(np.median([x.most for x, _ in rev])))}；{len(rev)}/{len(active)} 帧）")
    if block_w:
        bw = [(a - DRIFT, b + DRIFT) for a, b in block_w]      # 爆光可能早到、晚到
        span = sum(b - a for a, b in block_w)
        if self_cast or me is None or tg is None or one_doll or mixed:
            unchecked("挡段：施法者或目标定不了位" if not (one_doll or mixed) else "挡段：施法者或目标和别人同色一组，分不出光在谁那边")
        else:
            idx = [i for i in range(n) if inside(ts[i], bw) and not clip.edge[i]]
            cs = [(ts[i], x) for i in idx if (x := lift(me, i, (tg,))) is not None]
            vs = [(ts[i], x) for i in idx if (x := lift(tg, i, (me,))) is not None]
            t_card = [i for i in idx if inside(ts[i], block_w) and lift(tg, i, (me,)) is not None]

            def longest(ser: list[tuple[float, Lift]]) -> float:
                return max((r.dur for r in _runs([(t, lit_(x, LIFT_MIN)) for t, x in ser]) if r.k >= ONSET_RUN), default=0.0)
            c_run, v_run = longest(cs), longest(vs)
            if len(vs) >= ONSET_RUN and v_run > 0:
                if c_run >= span - 1e-6 and c_run > v_run:
                    unchecked(f"挡段：两边都有光——{who_l}手上连着亮了 {c_run:.2f}s（盖满挡段），{tgt_l}那边只亮了 {v_run:.2f}s："
                              "光是飞过去了还是大半留在手上，要人看")
                else:
                    lines.append(f"✓ {head}：挡段的光飞到了{tgt_l}这边（{_pct(max(x.sure for _, x in vs))}，连着 {v_run:.2f}s）")
            elif len(cs) >= ONSET_RUN and c_run >= max(ONSET_RUN / FPS, min(LIT_RUN_S, span / 2)) - 1e-6 \
                    and len(vs) >= ONSET_RUN and all(dark(x, LIFT_MIN) for _, x in vs):
                bad(f"挡段的光还在{who_l}身上（{_pct(max(x.sure for _, x in cs))}，连着 {c_run:.2f}s），没飞到{tgt_l}身前"
                    f"（最多 {_pct(max(x.most for _, x in vs))}）")
            elif len(cs) < ONSET_RUN or len(vs) < ONSET_RUN or len(t_card) < ONSET_RUN:
                g = me if len(cs) < ONSET_RUN else tg
                unchecked(f"挡段：{groups[g].name}：{why(g, [i for i in idx if inside(ts[i], block_w) and g in clip.bx[i]])}")
            else:
                unchecked("挡段：两边都没连着稳亮到阈值" + (f"（{who_l}手上亮了 {c_run:.2f}s，不到要求）" if c_run else "")
                          + "：可能炸在挡的人身上，或分不清光和身上本来的颜色")
    if not (cast.outcome == "空" or self_w or tgt_w or block_w):
        unchecked("锁定串里没写到光的阶段，这次施法手上 / 身上没有可查的")
    span_i = [i for i in range(n) if t0 - tol <= ts[i] <= t1 + tol]
    tg_boxed = tg is not None and any(tg in clip.bx[i] for i in span_i)
    tg_px = max((clip.px[i].get(tg, 0) for i in span_i), default=0) if tg is not None else 0
    if aims and cast.target not in known:
        unchecked(f"串色：目标「{tgt_l}」对不上本镜的人，真目标可能是任何一个人")
    elif me is None or (aims and tg is None):
        unchecked(f"串色：{'施法者' if me is None else '目标'}{who_msg(cast.who if me is None else cast.target)}，他身上的光挖不掉")
    elif aims and not tg_boxed and tg_px:
        unchecked(f"串色：目标{tgt_l}在 previz 里太小（最多 {tg_px} 像素，不到 {ID_MIN_PIX}），没成框，他身上的光挖不掉")
    else:
        # 串色看整次施法（空 的蓄光、没光的起手 / 收尾也看），尾巴放宽 DRIFT；目标整段不在画时，他的光落不进谁的框，照查
        own_groups = set(matches(groups, cast.who)) | (set(matches(groups, cast.target)) if aims or self_cast or dust else set())
        if dust:
            unchecked(f"目标{tgt_l}身上：卡里写了光尘落到他身上，光尘和落上去的整团光分不开，要人看")
        quiet_x = [(a - DRIFT, b + DRIFT) for a, b in block_w]      # 挡下的爆光可能落在挡的人身上
        for g in range(len(groups)):
            if g in own_groups:
                continue
            on_all = [i for i in range(n) if t0 <= ts[i] <= t1 + DRIFT and not inside(ts[i], quiet_x)
                      and not clip.edge[i] and g in clip.bx[i]]
            on = [i for i in on_all if (i, g) not in busy]            # 他身上本来就有别人同色光的帧，谁的光分不清，不算
            if not on:
                continue
            ser = [(ts[i], x) for i in on if (x := lift(g, i, (me, tg if aims else None))) is not None]
            spill = [r for r in _runs([(t, lit_(x, BLEED_MAX)) for t, x in ser]) if r.k >= ONSET_RUN]
            blips = [x for _, x in ser if lit_(x, BLEED_MAX)]
            unsure = [x for _, x in ser if not clean(x, BLEED_MAX) and not lit_(x, BLEED_MAX)]
            if spill:
                r = max(spill, key=lambda q: q.dur)
                t_b, x_b = max(((t, x) for t, x in ser if r.a <= t <= r.b), key=lambda h: h[1].sure)
                bad(f"串到{groups[g].name}身上（{t_b:.1f}s 框里本技能色 {_pct(x_b.sure)}，阈 {BLEED_MAX * 100:g}%；连着 {r.dur:.2f}s）")
            elif len(ser) < len(on):
                unchecked(f"串色：{groups[g].name}：{why(g, on_all, ser, thr=BLEED_MAX)}（量到 {len(ser)}/{len(on)} 帧）")
            elif len(blips) >= 2 * ONSET_RUN:
                unchecked(f"串色：{groups[g].name}：{len(blips)} 帧一闪一闪的同色光，连不成段——是串过来的光还是闪烁、反光，要人看")
            elif len(unsure) >= ONSET_RUN:
                unchecked(f"串色：{groups[g].name}：{why(g, on_all, ser, thr=BLEED_MAX)}（{len(unsure)}/{len(ser)} 帧拿不准）")
    status = "fail" if fails else ("unchecked" if missing else "pass")
    return Verdict(card.key, card.name, cast.who, cast.target, cast.t, status, tuple(lines), peak_t)


def readback(shot_dir: Path, video: Path) -> tuple[list[Verdict], list[str]]:
    md = (shot_dir / f"{shot_dir.name}.md").read_text(encoding="utf-8")
    casts = skills_lib.casts_in(md)
    if not casts:
        return [], []
    cfg_path, previz = previz_of(shot_dir)
    d_r, w_r, h_r = stream(video)
    d_p, w_p, h_p = stream(previz)
    if abs(d_r - d_p) > DUR_TOL:
        raise SystemExit(f"出片 {d_r:.2f}s，previz {d_p:.2f}s：不是本镜现行的整条出片。局部重拍的窗口片先 "
                         f"`python tools/cast_repair.py … --splice` 拼回底片再回读；镜长改过的旧版出片要按现行镜头重出")
    if abs(w_r / h_r - w_p / h_p) > ASPECT_TOL * (w_p / h_p):
        raise SystemExit(f"出片画幅 {w_r}×{h_r} 与 previz {w_p}×{h_p} 不一致，人的位置对不上")
    drama = skills_lib.drama_of(shot_dir)
    cards = skills_lib.load(drama)
    groups, notes = dolls(shot_dir)
    label = labels(shot_dir)
    cuts = seedance_ref.cuts_of(tomllib.loads(cfg_path.read_text(encoding="utf-8")))
    info = []
    for c in casts:
        card = skills_lib.find(cards, c.key)
        sp = skills_lib.phases(card, c)
        info.append((c, card, sp, {ph: skills_lib.card_hue(drama, card, ph) for ph, _, _ in sp}))
    clip = clip_of(video, previz, cuts, groups, {b for *_, pb in info for b in pb.values()})

    def falls(o: skills_lib.Cast, ocard: skills_lib.Card, osp: list[tuple[str, float, float]], pb: dict[str, Band],
              band: Band, lit_only: bool = True) -> list[tuple[int, list[Win]]]:
        """一次施法里与 band 同色的光落在谁身上、什么时候（各阶段 ±ONSET_TOL）：施法者、目标（自施就是施法者）、挡下的爆光
        落在任何人身前。lit_only：只算锁定串写到了光的阶段（占着谁的帧）；量背景时全算（宁可少几个空帧）。"""
        lp = skills_lib.lit_phases(ocard, o) if lit_only else {ph for ph, _, _ in osp}
        keep = [(ph, a - ONSET_TOL, b + ONSET_TOL) for ph, a, b in osp if bands_meet(pb[ph], band)]
        mine = [(a, b) for ph, a, b in keep if ph in skills_lib.SELF_PHASES and ph in lp]
        theirs = [(a, b) for ph, a, b in keep if ph in skills_lib.TARGET_PHASES and ph in lp]
        burst = [(a, b) for ph, a, b in keep if ph == "blocked"]
        return [(g, mine) for g in matches(groups, o.who)] + [(g, theirs) for g in matches(groups, o.target or o.who)] \
            + ([(g, burst) for g in range(len(groups))] if burst else [])

    def spans_near(c: skills_lib.Cast | None, band: Band) -> list[Win]:
        """与 band 同色的各次施法（c 除外）的整段时间窗 ±ONSET_TOL。"""
        return [(min([o.t] + [a for _, a, _ in osp]) - ONSET_TOL, max(b for _, _, b in osp) + ONSET_TOL)
                for o, _, osp, pb in info if o is not c and any(bands_meet(b, band) for b in pb.values())]

    bands = {b for *_, pb in info for b in pb.values()}
    back = {band: backs(clip, band, spans_near(None, band), [w for o, oc, osp, pb in info for w in falls(o, oc, osp, pb, band, False)])
            for band in bands}
    out = []
    for c, card, sp, pb in info:
        lp = skills_lib.lit_phases(card, c)
        split: dict[Band, set[str]] = {}
        for ph, _, _ in sp:                        # 一次施法按色带分开查（保护祝福：放手那一下金、光壳银蓝）
            if ph in lp or ph == "blocked" or c.outcome == "空":
                split.setdefault(pb[ph], set()).add(ph)

        def one(b: Band, phs: set[str]) -> Verdict:
            lit = [w for o, oc, osp, opb in info if o is not c for w in falls(o, oc, osp, opb, b)]
            return check_cast(clip, card, c, b, groups, label, lit, back[b], spans_near(c, b), frozenset(phs))
        parts = [one(b, phs) for b, phs in split.items()] or [one(pb[sp[0][0]], set())]
        out.append(parts[0] if len(parts) == 1 else Verdict(
            card.key, card.name, c.who, c.target, c.t,
            "fail" if any(v.status == "fail" for v in parts) else "unchecked" if any(v.status == "unchecked" for v in parts)
            else "pass", tuple(dict.fromkeys(ln for v in parts for ln in v.lines)),
            next((v.peak_t for v in parts if v.peak_t is not None), None)))
    return out, notes


def save(shot_dir: Path, video: Path, verdicts: list[Verdict], notes: list[str]) -> Path:
    """逐次结论写进这条出片的审片目录（render_review.review_dir）：castcheck.json。"""
    import render_review
    out = render_review.review_dir(shot_dir, video) / "castcheck.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"video": video.name, "verdicts": [asdict(v) for v in verdicts], "notes": notes},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    import render_review
    shot_dir = Path(sys.argv[1]).resolve()
    if shot_dir.suffix == ".md":
        shot_dir = shot_dir.parent
    video = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else render_review.find_render(shot_dir)
    if video is None or not video.is_file():
        print(f"没找到 {shot_dir.name} 的出片")
        return 1
    verdicts, notes = readback(shot_dir, video)
    for v in verdicts:
        print("\n".join(v.lines))
    for s in notes:
        print("（说明）" + s)
    if not verdicts:
        print(f"{shot_dir.name}：本镜没有施法")
        return 0
    out = save(shot_dir, video, verdicts, notes)
    n = {s: sum(v.status == s for v in verdicts) for s in ("pass", "fail", "unchecked")}
    print(f"{n['pass']} 通过 / {n['fail']} 不通过 / {n['unchecked']} 未查 → {out.relative_to(REPO)}")
    return 1 if n["fail"] else (3 if n["unchecked"] else 0)


if __name__ == "__main__":
    raise SystemExit(main())
