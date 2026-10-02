# -*- coding: utf-8 -*-
"""每个场景 bg 出一张锚点图（2026-09-25 用户定调，shengji follow-up 008）。

bg 卡 `{dir}/{dir}.md` 里首行 ＝ 目录名的 ```text 块 → `{dir}/{dir}.png`。这张图是场景的**长相**；
它与 `props/p{N}_*/mesh/p{N}.glb`（**单个物体**的几何）、`planning/blocks.toml`（布局）一起由
`build_scene.py` 汇总成 `_blender/{bg}.blend`——**没有这张图，build_scene 不建 blend**（图先行、3D 在后）。

· 世界锚点 ＝ 各卡 `参考:` 行点名最多的那张（一个世界只有一张自由生成图，rule 4e ②）：零参考图文生图；
  其余一律挂它图生图，卡里缺 `参考:` 行的也挂它。
· 方位 plate（`bg{N}/bg{N}-{M}_{方位}/`，shot 的 `参考:` 真正点名的是它们）同一套做法，参考图按卡里 `参考:`
  行解析（通常是所属 bg 的锚点图）。按依赖分层出：世界锚点 → bg 锚点 → plate；并发进程遇到参考图未出就等。
· 送审稿 ＝ 卡 prompt 去掉 `参考:` 与画幅 / 参数行——参考图与画幅作参数传入，不该占字数。
· **场景引用物件**（follow-up 013）：所属 bg 的 blocks.toml 里占地最大的前 3 件 prop 的正面图跟着世界基调图一起上传，
  送审稿末尾加一行「物件参考」说明它们是谁、只借长相——场景图里的物件与它的 GLB 才长得一样。即梦字数容不下就逐件减。
· 引擎按 `tools/image_engine.py`（rule 4l）：世界锚点与 bg 锚点先走 ElevenLabs，plate 先走即梦；
  首选失败再退另一家（送审稿超即梦 1600 字硬限时只能走 ElevenLabs）。
· 骨架卡（正文不足 800 字）不出图。
· 状态变体卡（正文有 `只改:` 行，rule 4f）照参考图的构图：参考说明换成 KEEP_IN，不加 KEEP_OUT。
· plan 打两个数：「正文」＝ `check_world_scenes_szzl.prompt_len`（W4 同一把尺，rule 4f 的 1500–1600 说的是它）；
  「送审」＝ 正文 + 参考 / 物件说明行 + 负向，只按引擎硬限判（即梦 `PROMPT_MAX`，超了只能走 ElevenLabs）。
· `ref/` 里的原版区图是权利人的图，**绝不进模型**（divergence #8 / #108）；只有世界锚点图作参考。

用法（仓库根目录；范围可以是 bg 目录、区目录或 scenes 根）：
    python tools/gen_bg_images.py plan <范围…>        # 每个 bg 的正文 / 送审字数、引擎、参考图，不花钱
    python tools/gen_bg_images.py run  <范围…> [--shard k/n] [--force] [--engine auto|dreamina|elevenlabs]
已出图的跳过（`--force` 重出），可中断可续跑；即梦按 prompt 全文找回任务，多进程并发安全。
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
import sys
import tempfile
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import gen_bg_assets as gba  # noqa: E402  即梦并发安全提交
from tools import gen_images_xianjian as dm  # noqa: E402
from tools import image_fetch as el  # noqa: E402
from tools import image_engine as ie  # noqa: E402
from tools import props_lib  # noqa: E402
from tools import check_world_scenes_szzl as cws  # noqa: E402  正文字数与 W4 同一把尺
import tomllib  # noqa: E402

BG_DIR = re.compile(r"^bg\d+_[^_]+$")
PLATE_DIR = re.compile(r"^bg\d+-\d+_.+$")
REF_WAIT_S = 900
PROP_REFS = 3        # 场景图最多挂几件物件正面图（世界基调 / 所属 bg 锚点图之外）
UPLOAD_EDGE = 1600    # 参考图上传副本的长边像素（见 _upload_copy）
NO_PROPS = False      # --no-props
VIEW_MAX_M = 120.0    # 超过这个距离的物件在画里太小，不值得挂参考图
ENCLOSING = ("hall", "hall_shell", "abbey_hall", "wing", "entrance_wing", "chamber", "barracks", "stable")
CAMERA_WORDS = re.compile(r"相机|摄影机|摄像机|镜头架")   # 会被画成一台实物相机（实测 bg19 / bg19-4 画出了三脚架相机）
KEEP_OUT = ("参考用法补充: 参考图一只给材质、配色、光与胶片质感；取景、机位与画面里有什么，全部按上文重建，"
            "不照搬参考图的构图与其中的建筑物件。")
# 状态变体（rule 4f：同一块地只换时辰 / 天气 / 状态）要的正好相反——构图照参考图（shengji follow-up 048，bg808 照 bg805）
VARIANT = re.compile(r"^只改[:：]", re.M)
KEEP_IN = "参考用法补充: 构图、机位、焦段与裁切与参考图一致，只改上文「只改」列出的项。"
UPLOAD_RETRIES = 3   # 即梦上传 / 连接阶段失败的重试次数（请求没发出去，不扣费）
RETRYABLE = re.compile(r"upload|do request|connection|timeout|deadline|EOF|reset|没回 JSON", re.I)
DM_WAIT_S = 900     # 即梦排队慢时（实测 2026-09-25 上午 >20 分钟）多等：提交即扣费，放弃就换引擎、基调会岔
RATIOS = ("21:9", "16:9", "3:2", "4:3", "1:1", "3:4", "2:3", "9:16")
PARAM_LINE = re.compile(r"^(参考:|比例:|参数:|\[参数\]|画幅)")
REF_LINE = re.compile(r"^参考:\s*`([^`]+)`", re.M)
SKELETON_MIN = 800


class Job:
    def __init__(self, d: Path) -> None:
        self.dir = d
        self.name = d.name
        self.card = d / f"{d.name}.md"
        self.out = d / f"{d.name}.png"
        text = self.card.read_text(encoding="utf-8")
        m = re.search(rf"```text\n({re.escape(d.name)}\n.*?)\n```", text, re.S)
        self.body = m.group(1) if m else ""
        neg = re.search(r"^## 负向\s*\n+```[a-z]*\n(.*?)\n```", text, re.S | re.M)
        self.neg = gba.neg_line(neg.group(1)) if neg else ""
        r = REF_LINE.search(self.body)
        self.ref_name = (re.sub(r"\.png$", "", r.group(1).split("/")[0].split()[0].split("(")[0])
                         if r else None)
        self.plate = bool(PLATE_DIR.match(d.name))

    @property
    def sort_key(self) -> tuple[int, int, int]:
        m = re.match(r"^bg(\d+)(?:-(\d+))?_", self.name)
        return int(self.plate), int(m.group(1)), int(m.group(2) or 0)

    @property
    def skeleton(self) -> bool:
        return len(re.sub(r"\s", "", self.body)) < SKELETON_MIN

    @property
    def ratio(self) -> str:
        for line in self.body.split("\n"):
            if re.match(r"^(比例|参数|画幅|构图|\[参数\])", line) or "画幅" in line:
                m = re.search("|".join(RATIOS), line)
                if m:
                    return m.group(0)
        return "16:9"

    def send(self, with_neg: bool) -> str:
        lines = self.body.split("\n")
        keep, skip_next = [], False
        for line in lines:
            if skip_next:
                skip_next = False
                if line.startswith("画幅"):
                    continue
            if line.startswith("[参数]"):
                skip_next = True
                continue
            if PARAM_LINE.match(line):
                continue
            keep.append(line)
        s = "\n".join(keep).strip()
        return s + "\n" + self.neg if with_neg and self.neg else s


def find_jobs(paths: list[str]) -> list[Job]:
    out: dict[Path, Job] = {}
    for p in paths:
        root = Path(p).resolve()
        # 传卡片 md ＝ 只要这一张（不连带它下面的方位 plate）；传目录 ＝ 目录及其下全部
        cands = [root.parent] if root.suffix == ".md" else [root] + [d for d in root.rglob("bg*_*") if d.is_dir()]
        for d in cands:
            if (BG_DIR.match(d.name) or PLATE_DIR.match(d.name)) and (d / f"{d.name}.md").is_file():
                out[d] = Job(d)
    return sorted(out.values(), key=lambda j: j.sort_key)


def scenes_root(d: Path) -> Path:
    for p in d.parents:
        if p.name == "scenes":
            return p
    raise SystemExit(f"{d} 不在任何 scenes/ 目录下")


class World:
    """整棵 scenes 树的目录索引 + 世界锚点 —— 读整棵树，不只读本次范围。"""

    def __init__(self, jobs: list[Job]) -> None:
        root = scenes_root(jobs[0].dir)
        everyone = find_jobs([str(root)])
        self.by_name: dict[str, list[Path]] = collections.defaultdict(list)
        for j in everyone:
            self.by_name[j.name].append(j.out)
        name = collections.Counter(j.ref_name for j in everyone if j.ref_name and not j.plate).most_common(1)[0][0]
        self.anchor = self.resolve(name)

    def resolve(self, name: str) -> Path:
        hits = self.by_name.get(name, [])
        if len(hits) != 1:
            raise SystemExit(f"参考图「{name}」在 scenes 树里找到 {len(hits)} 个目录")
        return hits[0]

    def refs(self, j: Job) -> list[Path]:
        if j.out == self.anchor:
            return []
        return [self.resolve(j.ref_name)] if j.ref_name else [self.anchor]


def _camera(cfg: dict, j: Job) -> dict | None:
    """这张图自己的机位：plate ＝ key 与 plate 目录同名的 [[anchor]]；bg 锚点图 ＝ `image` 绑了这张图的 [[anchor]]。"""
    for a in cfg.get("anchor", []):
        if a.get("key") == j.name or a.get("image") == j.out.name:
            return a
    return None


def _in_view(cam: dict, xy: tuple[float, float], radius: float) -> float:
    """块在这台机位视锥里的「显眼度」（角半径 ÷ 距离，0 ＝ 不在画内）。平面图坐标 x 东 y 南；水平视场按 36 mm 画幅算。"""
    ex, ey = cam["eye"]
    tx, ty = cam["target"]
    fx, fy, vx, vy = tx - ex, ty - ey, xy[0] - ex, xy[1] - ey
    dist = math.hypot(vx, vy)
    if dist < 0.5:
        return 0.0
    half = math.atan(18.0 / float(cam.get("lens_mm", 35)))
    off = abs(math.atan2(fx * vy - fy * vx, fx * vx + fy * vy))
    if off > half + math.atan(radius / dist) or dist > VIEW_MAX_M:
        return 0.0
    return radius / dist


def _occluded(cfg: dict, cam: dict, xy: tuple[float, float], self_id: str) -> bool:
    """物件在一栋房子里、机位却在房子外 ＝ 被墙挡住（实测：院外立面的锚点图挂上了图书馆的书架与长桌）。"""
    ex, ey = cam["eye"]
    for b in cfg.get("block", []):
        if b.get("id") == self_id or b.get("kind") not in ENCLOSING and not (
                b.get("kind") == "asset" and float(b.get("h_m", 0)) >= 3.0 and max(b["size"]) >= 6.0):
            continue
        (cx, cy), (sx, sy) = b["xy"], b["size"]
        inside = lambda x, y: abs(x - cx) <= sx / 2 and abs(y - cy) <= sy / 2   # noqa: E731
        if inside(*xy) and not inside(ex, ey):
            return True
    return False


def scene_props(j: Job) -> list[tuple[str, str, Path]]:
    """这张图里真正入画的物件：只看这张图自己的机位（没有机位的图不挂物件图——宁缺，不乱挂），
    取视锥内、没被房子挡住的 prop，按显眼度排，只取已有正面图的前 PROP_REFS 件 → [(键, 中文名, 正面图)]。
    实测「全 bg 占地最大的前 3 件」会把芦苇窝棚贴进矿道、把书架贴到修道院门外（QC 2026-09-25）。"""
    bg = j.dir.parent if j.plate else j.dir
    t = bg / "planning" / "blocks.toml"
    if not t.is_file():
        return []
    cfg = tomllib.loads(t.read_text(encoding="utf-8"))
    cam = _camera(cfg, j)
    if cam is None:
        return []
    if "props" in cam:
        # 机位显式点名（空表 ＝ 一件都不挂）：本场景主体是脚本几何（bg2 修道院 = abbey_hall）时视锥挑不到对应 prop；
        # 视锥里的 prop 与卡冲突时（bg18-4 卡写「不出现任何建筑」、bg175 的木墩被规划成铁砧）也在这里改
        area = {k: float(len(cam["props"]) - i) for i, k in enumerate(cam["props"])}
    else:
        area = _frustum_props(cfg, cam)
    out = []
    for k in sorted(area, key=lambda k: -area[k]):
        d = props_lib.find(bg, k)
        front = sorted(d.glob(f"{k}-1_*.png")) if d else []
        if front:
            out.append((k, tomllib.loads((d / "asset.toml").read_text(encoding="utf-8"))["asset"]["name_zh"], front[0]))
        if len(out) == PROP_REFS:
            break
    return out


def _frustum_props(cfg: dict, cam: dict) -> dict[str, float]:
    area: dict[str, float] = {}
    for b in cfg.get("block", []):
        if b.get("kind") != "asset":
            continue
        (cx, cy), (sx, sy) = b["xy"], b["size"]
        parts = b.get("parts") or ([{"asset": b["asset"], "at": [0, 0]}] if b.get("asset") else [])
        for p in parts:
            xy = (cx + float(p.get("at", [0, 0])[0]), cy - float(p.get("at", [0, 0])[1]))
            s = _in_view(cam, xy, max(sx, sy) / 2 if not b.get("parts") else 1.0)
            if s > 0 and not _occluded(cfg, cam, xy, b["id"]):
                area[p["asset"]] = max(area.get(p["asset"], 0.0), s)
    return area


def prop_line(props: list[tuple[str, str, Path]]) -> str:
    # 短：锚点卡正文本身就逼近即梦 1600 字（W4 下限 1500），这一行要挤进剩下的那点余量
    names = "、".join(n for _, n, _ in props)
    return f"物件参考: 其后{len(props)}张依次是{names}，入画时照图的形制比例材质配色，不借构图机位光线。"


def plan_for(j: Job, world: World, engine: str) -> tuple[str, str, list[Path]]:
    """引擎、送审稿与参考图。物件参考图在即梦字数容得下时才挂（容不下就逐件减）；正文与负向词一个字都不丢——
    带着负向词塞不进即梦就改走 ElevenLabs（实测 bg807-1 三次都被悄悄删掉「不要楼梯」，斜坡三次画成楼梯，2026-09-30）。"""
    base = world.refs(j)
    # 世界锚点守 rule 4e ② 零参考、纯文字：实测挂物件图的 bg1 两次都卡死在即梦「生成中」（>12 / >50 分钟），
    # 同一时段别的带参考图任务照常出图；它的物件一致性交给挂它的 bg 锚点与 plate
    props = [] if (j.out == world.anchor or NO_PROPS) else scene_props(j)
    body = j.send(with_neg=False)
    hit = CAMERA_WORDS.findall(body)
    if hit:
        raise SystemExit(f"{j.name}：prompt 里有「{'、'.join(sorted(set(hit)))}」——会被画成一台实物相机，改成「视点在…」再出图")
    # 挂了参考图就一定加这一句：实测 plate 与 bg 锚点会照搬参考图的整幅构图（QC 2026-09-25，bg1-1…4 / bg18 / bg20 各镜）
    body += ("\n" + (KEEP_IN if VARIANT.search(body) else KEEP_OUT)) if base else ""
    for n in range(len(props), -1, -1):
        extra = ("\n" + prop_line(props[:n])) if n else ""
        text = body + extra + (("\n" + j.neg) if j.neg else "")
        if engine == "dreamina" and len(text) <= dm.PROMPT_MAX:
            return "dreamina", text, base + [p for _, _, p in props[:n]]
    extra = ("\n" + prop_line(props)) if props else ""
    return "elevenlabs", body + extra + (("\n" + j.neg) if j.neg else ""), base + [p for _, _, p in props]


def log(j: Job, **kw: object) -> None:
    p = j.dir / "planning" / "anchor_gen.json"
    p.parent.mkdir(exist_ok=True)
    data = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    data.update(kw)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _upload_copy(p: Path) -> Path:
    """参考图的上传副本：长边 ≤ UPLOAD_EDGE 的 JPEG。即梦一次上传总量有上限——实测 4 张原图（世界锚点 6 MB +
    3 张 4–5 MB 物件图，共 20 MB）每次都卡在 `upload phase`，2 张（10 MB）能过；参考图用不着原尺寸。
    缓存在系统临时目录（可随时重建，不进仓库）。"""
    from PIL import Image
    st = p.stat()
    key = hashlib.sha1(f"{p.resolve()}|{st.st_size}|{st.st_mtime_ns}".encode()).hexdigest()[:12]
    out = Path(tempfile.gettempdir()) / "dm_refs" / f"{key}.jpg"
    if not out.is_file():
        out.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(p).convert("RGB")
        im.thumbnail((UPLOAD_EDGE, UPLOAD_EDGE))
        im.save(out, "JPEG", quality=90)
    return out


def _fetch(url: str, dest: Path) -> None:
    """先落 `.part` 再改名：别的进程在等这张图作参考，看见半截文件就会把半截图传上去（实测 bg20-2 上传失败）。"""
    part = dest.with_name(dest.stem + ".part" + dest.suffix)
    dm.download(url, part)
    part.replace(dest)


def _dreamina(j: Job, text: str, refs: list[Path], t0: float) -> bool:
    # 上传阶段失败没提交、不扣费（实测多进程同时传同一张 6 MB 大图就会撞上），先退避重试，别急着换引擎
    for attempt in range(UPLOAD_RETRIES + 1):
        try:
            url, cost = gba._dm_submit(text, [_upload_copy(r) for r in refs], j.ratio, wait_s=DM_WAIT_S)
            _fetch(url, j.out)
            log(j, engine="dreamina", ratio=j.ratio, chars=len(text), ref=[r.name for r in refs], credits=cost)
            print(f"  ✓ {j.name} 即梦 {len(text)} 字 {j.ratio} {time.time() - t0:.0f}s", flush=True)
            return True
        except Exception as e:     # noqa: BLE001 —— 上传失败重试；其余即梦失败交给调用方换引擎
            msg = str(e)
            print(f"  ! {j.name} 即梦失败（第 {attempt + 1} 次）：{msg[:400]}", flush=True)
            if not RETRYABLE.search(msg) or attempt == UPLOAD_RETRIES:
                return False
            time.sleep(45 * (attempt + 1))
    return False


def _elevenlabs(j: Job, text: str, refs: list[Path], t0: float) -> None:
    key = el.api_key()
    gid = el.create(key, text, model=el.DEFAULT_MODEL, quality="medium", aspect=j.ratio,
                    resolution="2K", refs=[el.inline(_upload_copy(p)) for p in refs] or None)
    part = j.out.with_name(j.out.stem + ".part" + j.out.suffix)
    el.wait_download(key, gid, part)
    part.replace(j.out)
    log(j, engine="elevenlabs", ratio=j.ratio, chars=len(text), ref=[r.name for r in refs], gid=gid)
    print(f"  ✓ {j.name} ElevenLabs {len(text)} 字 {j.ratio} {time.time() - t0:.0f}s", flush=True)


def generate(j: Job, world: World, engine: str) -> None:
    j = Job(j.dir)      # 出图前重读卡：长批次里卡常被同时修（实测 bg19-5 进程启动后才压字数）
    eng, text, refs = plan_for(j, world, ie.first_choice(not j.plate, engine))
    waited = 0
    while refs and not refs[0].is_file():      # 别的进程还在出上一层；等，不重交
        if waited >= REF_WAIT_S:
            raise RuntimeError(f"参考图 {refs[0].name} 等了 {REF_WAIT_S}s 仍未出")
        time.sleep(15)
        waited += 15
    t0 = time.time()
    if eng == ie.DREAMINA:
        if not _dreamina(j, text, refs, t0):
            _, text, refs = plan_for(j, world, ie.ELEVENLABS)   # 同一套物件参考，外加 ElevenLabs 不受字数限制的完整负向
            _elevenlabs(j, text, refs, t0)
        return
    try:
        _elevenlabs(j, text, refs, t0)
    except (Exception, SystemExit) as e:   # noqa: BLE001 —— 锚点 ElevenLabs 失败（审核 / 超时）退即梦，字数容不下就放弃
        eng2, text2, refs2 = plan_for(j, world, ie.DREAMINA)
        if eng2 != ie.DREAMINA:
            raise
        print(f"  ! {j.name} ElevenLabs 失败，退即梦：{str(e)[:200]}", flush=True)
        if not _dreamina(j, text2, refs2, t0):
            raise RuntimeError(f"{j.name}：ElevenLabs 与即梦都失败") from e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("plan", "run"))
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--engine", default=ie.AUTO, choices=ie.CHOICES, help="auto ＝ 按 rule 4l：锚点 ElevenLabs、plate 即梦")
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-props", action="store_true",
                    help="不挂物件参考图（实测个别 prop 组合让即梦卡死在「生成中」时用；只挂世界 / 所属 bg 锚点图）")
    args = ap.parse_args()
    global NO_PROPS
    NO_PROPS = args.no_props
    k, n = (int(x) for x in args.shard.split("/"))
    if not 0 <= k < n:
        raise SystemExit(f"--shard {k}/{n}：k 从 0 数到 n-1")
    jobs = find_jobs(args.paths)
    if not jobs:
        raise SystemExit("范围内没有 bg 目录")
    world = World(jobs)
    todo = [j for j in jobs if not j.skeleton]
    print(f"bg / plate {len(jobs)} · 骨架跳过 {len(jobs) - len(todo)} · 世界锚点 {world.anchor.parent.name}")
    if args.step == "plan":
        c = collections.Counter()
        for j in todo:
            eng, text, refs = plan_for(j, world, ie.first_choice(not j.plate, args.engine))
            c[eng] += 1
            print(f"  {j.name:<24} {eng:<10} 正文 {cws.prompt_len(j.body):>5} · 送审 {len(text):>5} 字 {j.ratio:<5} "
                  f"参考={refs[0].parent.name if refs else '无（世界锚点）'}"
                  f"{'  已出图' if j.out.is_file() else ''}")
        print(dict(c))
        return 0
    todo = [j for j in todo if args.force or not j.out.is_file()][k::n]
    skipped = []
    for j in todo:
        try:
            generate(j, world, args.engine)
        except (Exception, SystemExit) as e:   # noqa: BLE001 —— 一张卡住就跳过；image_fetch 超时抛 SystemExit（实测整个进程随之退出）
            print(f"  ⏭ {j.name}：{str(e)[:200]}", flush=True)
            skipped.append(j.name)
    print(f"\n完成 {len(todo) - len(skipped)} / {len(todo)}；跳过 {len(skipped)} {' '.join(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
