# -*- coding: utf-8 -*-
"""场景物件：平面图编号块 → 物件卡 → 真实照片参考 → 正 / 侧 / 背三视图 → Rodin GLB（follow-up 007 / 013）。

一个物件 ＝ 本剧 props/ 下一个目录 `props/p{N}_{名}/`（2026-09-25 起各区 `_assets/` 并入 props，编号见 `tools/props_lib.py`）：
    {key}_{名}.md       资产卡：三个 ```text 块，首行路由键 {key}-1_正面 / {key}-2_侧面 / {key}-3_背面
    asset.toml          [asset] key / name_zh / size_m=[东西, 南北, 高] / queries=[英文检索词] / prompt_en / yaw_deg
                        可选 no_text = true（禁字物件：不抓、不挂照片）· views = ["正面", …]（出哪几面，缺省三面；缺面的不出模）
    ref/                真实世界照片（Wikimedia Commons，许可干净）+ refs.md 逐张记作者与许可
    {key}-1_正面.png …  三视图
    mesh/{key}.glb      Rodin 原始网格（build_scene.py 的 `asset` kind 读它）
    gen_log.json        每一步花了多少（即梦积分 / Rodin credits）
块在 blocks.toml 里写 `kind = "asset"` + `asset = "p{N}"`（或 `parts`）引用它；**同一件东西全剧只出一份**（rule 4i ①）。
一个物件 ＝ 一个 GLB ＝ 一个物体（2026-09-25）；剧情物件（p1–p14）的卡与 asset.toml 由 `tools/gen_props_szzl.py` 生成，同样走本工具出侧 / 背。

**参考图只用真实照片**：权利人的官方图与游戏截图绝不进生成模型（divergence #8 / #108）。

用法（仓库根目录；参数可以是 prop 目录 / props 根，或 bg / 区 / scenes 目录——后者 ＝ 这些场景的 blocks.toml 引用到的 prop）：
    python tools/gen_bg_assets.py check  <目录…>        # 卡 / toml 契约，不花钱
    python tools/gen_bg_assets.py plan   <目录…>        # 每面的送审稿字数、参考图、负面词末行，不花钱
    python tools/gen_bg_assets.py refs   <目录…>        # 抓真实照片
    python tools/gen_bg_assets.py images <目录…> [--engine auto|dreamina|elevenlabs]
    python tools/gen_bg_assets.py mesh   <目录…> [--tier Sketch|Regular]
    python tools/gen_bg_assets.py all    <目录…>
    python tools/gen_bg_assets.py all    <目录…> --shard 0/4   # 四个进程各跑一份（即梦按 prompt 找回任务，并发安全）
每一步只补缺的产物（已存在即跳过，`--force` 覆盖），可中断可续跑。
"""
from __future__ import annotations

import argparse
import html
import io
import json
import re
import sys
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import gen_images_xianjian as dm  # noqa: E402  即梦 CLI 提交 / 取回（提交即扣费，失败只重查不重交）
from tools import hyper3d_fetch as rodin  # noqa: E402
from tools import image_engine as ie  # noqa: E402
from tools import image_fetch as el  # noqa: E402
from tools import check_world_scenes_szzl as gate  # noqa: E402
from tools import props_lib  # noqa: E402

VIEWS = ("1_正面", "2_侧面", "3_背面")
VIEW_NAMES = tuple(v.split("_", 1)[1] for v in VIEWS)   # asset.toml `views` 的取值
NO_TEXT = "no_text"    # 布尔：物件上不许有可读文字 → refs 不抓照片、正面不挂照片（照片常带字；shengji lessons L14）
VIEWS_KEY = "views"    # 出哪几面：VIEW_NAMES 里取、必含正面，缺省三面；缺面的只当镜头参考、不出模（lessons L15）
# asset.toml [asset] 允许的键，多出来的报错（拼错的键不许静默失效）。brief / from 是给写卡人与溯源看的说明，不驱动产物
FIELDS = ("key", "name_zh", "size_m", "queries", "prompt_en", "yaw_deg", "single", NO_TEXT, VIEWS_KEY, "brief", "from")
NEG_BLOCK = re.compile(r"^## 负面词\s*\n+```text\n(.*?)\n```", re.S | re.M)
UA = "micro-drama-platform/1.0 (asset refs; contact: repo owner)"
LICENSE_OK = re.compile(r"^(cc0|public domain|pd|cc[ -]by(-sa)?[ -]?[0-9.]*)", re.I)
N_REFS = 3
MULTI = re.compile(r"与|和|及|、|群$|杂物|木箱木桶")   # 资产名读起来是几样东西（并列 / 「…群」/ 混杂的一堆）
MIN_BALANCE = 10.0    # Rodin 保底：低于它不再出模（实测 0.5 credit / 件，10 credits ≈ 20 件重出的余量）


def neg_line(block: str) -> str:
    """卡里的负面词块 → 送审稿末行。即梦与 ElevenLabs 都没有独立的负向参数，出图工具一律拼进 prompt 末行
    （gen_bg_images / gen_char_images 共用本函数）。"""
    return "负面词: " + re.sub(r"\s*\n\s*", "", block).strip()


class Asset:
    def __init__(self, d: Path) -> None:
        self.dir = d
        with open(d / "asset.toml", "rb") as f:
            self.spec = tomllib.load(f)["asset"]
        self.key = self.spec["key"]
        self.card = d / f"{d.name}.md"
        self.log_p = d / "gen_log.json"

    def view(self, i: int) -> Path:
        return self.dir / f"{self.key}-{VIEWS[i]}.png"

    @property
    def glb(self) -> Path:
        return self.dir / "mesh" / f"{self.key}.glb"

    def refs(self) -> list[Path]:
        return sorted(p for p in (self.dir / "ref").glob("r*.*") if p.suffix.lower() in (".jpg", ".jpeg", ".png"))

    def prompts(self) -> list[str]:
        """三个 ```text 块的正文（去掉首行路由键），按 -1 / -2 / -3 排。"""
        blocks = re.findall(r"```text\n(.*?)\n```", self.card.read_text(encoding="utf-8"), re.S)
        got = {}
        for b in blocks:
            first = b.split("\n")[0].strip()
            for i, v in enumerate(VIEWS):
                if first == f"{self.key}-{v}":
                    got[i] = "\n".join(b.split("\n")[1:]).strip()
        return [got.get(i, "") for i in range(3)]

    @property
    def no_text(self) -> bool:
        return self.spec.get(NO_TEXT, False)

    @property
    def views(self) -> list[int]:
        """要出的面（VIEWS 下标）；取值由 check() 校验。"""
        return sorted(VIEW_NAMES.index(v) for v in self.spec.get(VIEWS_KEY, VIEW_NAMES))

    def neg(self) -> str:
        m = NEG_BLOCK.search(self.card.read_text(encoding="utf-8"))
        return neg_line(m.group(1)) if m else ""

    def send(self, i: int) -> str:
        """第 i 面的送审稿 ＝ prompt 块 + 卡里「## 负面词」块拼成的末行（场景物件卡没有这一块，负向写在正文里）。"""
        n = self.neg()
        return self.prompts()[i] + ("\n" + n if n else "")

    def log(self, **kw) -> None:
        d = json.loads(self.log_p.read_text(encoding="utf-8")) if self.log_p.is_file() else {}
        d.update(kw)
        self.log_p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def used_keys(scope: Path) -> set[str]:
    """scope 下所有 blocks.toml 里 `asset` 与 `parts` 引用到的 prop 键。"""
    keys: set[str] = set()
    for t in scope.rglob("planning/blocks.toml"):
        for b in tomllib.loads(t.read_text(encoding="utf-8")).get("block", []):
            keys |= {p["asset"] for p in b.get("parts", [])} | ({b["asset"]} if b.get("asset") else set())
    return keys


def find_assets(paths: list[str]) -> list[Asset]:
    out: dict[Path, Asset] = {}
    for p in paths:
        root = Path(p).resolve()
        if root.name == "props" or props_lib.DIR.match(root.name) and root.parent.name == "props":
            dirs = props_lib.scene_objects(root) if root.name == "props" else [root] if (root / "asset.toml").is_file() else []
        else:
            dirs = [d for d in (props_lib.find(root, k) for k in sorted(used_keys(root))) if d and (d / "asset.toml").is_file()]
        out.update({d: Asset(d) for d in dirs})
    return sorted(out.values(), key=lambda a: int(props_lib.KEY.match(a.key).group(1)))


# ── check ─────────────────────────────────────────────────────────────
def check(a: Asset) -> list[str]:
    errs = []
    for k in ("key", "name_zh", "size_m", "queries", "prompt_en"):
        if k not in a.spec:
            errs.append(f"asset.toml 缺 {k}")
    extra = sorted(set(a.spec) - set(FIELDS))
    if extra:
        errs.append(f"asset.toml 有未登记的键 {extra}——拼错了，或新键没登记进 gen_bg_assets.FIELDS 并被代码读取")
    if not isinstance(a.spec.get(NO_TEXT, False), bool):
        errs.append(f"{NO_TEXT} 只能是 true / false")
    vs = a.spec.get(VIEWS_KEY, list(VIEW_NAMES))
    if not (isinstance(vs, list) and all(isinstance(v, str) for v in vs) and len(set(vs)) == len(vs)
            and set(vs) <= set(VIEW_NAMES) and VIEW_NAMES[0] in vs):
        return errs + [f"{VIEWS_KEY} = {vs!r}：取 {list(VIEW_NAMES)} 里不重复的几面，且必须含{VIEW_NAMES[0]}（侧 / 背挂正面图作参考）"]
    if not a.dir.name.startswith(a.key + "_"):
        errs.append(f"目录名 {a.dir.name} 不以键 {a.key}_ 开头")
    if not props_lib.KEY.match(a.key) or a.dir.parent.name != "props":
        errs.append(f"键 {a.key} 不是 p{{N}}，或目录不在 props/ 下——物件只住 props，编号从 props_lib.allocate() 领")
    if MULTI.search(a.spec.get("name_zh", "")) and not a.spec.get("single"):
        # 一个 GLB 只装一个物体（2026-09-25 用户定调）：名字里并列了几样东西，就拆成几件资产，
        # 在 plan 里用 parts 让 build_scene 摆在一起。确实是一件东西的（树屋连着它的环干平台）写 single = "理由"。
        errs.append(f"「{a.spec['name_zh']}」读起来是几样东西——拆成单物体资产、在 plan 里用 parts 组合；"
                    f"确是一件就在 asset.toml 写 single = \"理由\"")
    if not a.card.is_file():
        return errs + [f"没有资产卡 {a.card.name}"]
    yw = gate.yellow_words()
    prompts = a.prompts()
    for i in a.views:
        p = prompts[i]
        if not p:
            errs.append(f"缺 {a.key}-{VIEWS[i]} 的 ```text 块（首行必须是路由键）")
            continue
        n = len(a.send(i))
        if n > dm.PROMPT_MAX:
            errs.append(f"{VIEWS[i]} 送审稿（prompt + 负面词）{n} 字，超即梦 {dm.PROMPT_MAX} 硬限")
        hit = [w for w in yw if w in p]
        if hit:
            errs.append(f"{VIEWS[i]} prompt 含黄级专名：{'、'.join(hit[:5])}")
        for tok in gate.IP_RED:
            if tok in p:
                errs.append(f"{VIEWS[i]} prompt 含红级 IP 词：{tok}")
    stale = [a.view(i).name for i in range(len(VIEWS)) if i not in a.views and a.view(i).is_file()]
    if stale:
        errs.append(f"{VIEWS_KEY} 不出这几面，盘上却还有 {stale}——删掉")
    return errs


# ── refs：Wikimedia Commons 真实照片 ────────────────────────────────────
def _get(url: str) -> bytes:
    """Wikimedia 限流严格（实测四进程并发 → 一批 429）：429 按 Retry-After 退避，其余网络错短退避。"""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                time.sleep(1.0)                      # 串行节流：每次请求之间至少 1 秒
                return r.read()
        except urllib.error.HTTPError as e:
            if i == 5:
                raise
            wait = float(e.headers.get("Retry-After") or 0) if e.code == 429 else 0
            time.sleep(max(wait, 15.0 * (i + 1)) if e.code == 429 else 4 * (i + 1))
        except Exception:
            if i == 5:
                raise
            time.sleep(5 * (i + 1))
    return b""


def commons_search(q: str, limit: int = 12) -> list[dict]:
    qs = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{q} filetype:bitmap", "gsrlimit": limit, "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1280})
    data = json.loads(_get(f"https://commons.wikimedia.org/w/api.php?{qs}"))
    out = []
    for page in sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = (page.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        if ii.get("mime") not in ("image/jpeg", "image/png") or ii.get("width", 0) < 800:
            continue
        if not LICENSE_OK.match(lic.strip()):
            continue
        artist = html.unescape(re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", ""))).strip()
        out.append({"title": page["title"], "url": ii.get("thumburl") or ii["url"],
                    "page": ii.get("descriptionurl", ""), "license": lic, "artist": artist[:80]})
    return out


def do_refs(a: Asset, force: bool) -> None:
    if a.no_text:
        print(f"  · {a.key} {NO_TEXT}：不抓照片（照片常带字，会被画进禁字物件）")
        return
    if a.refs() and not force:
        print(f"  · {a.key} refs 已有 {len(a.refs())} 张，跳过")
        return
    (a.dir / "ref").mkdir(exist_ok=True)
    picked, seen = [], set()
    for q in a.spec["queries"]:
        for hit in commons_search(q):
            if hit["title"] in seen:
                continue
            seen.add(hit["title"])
            picked.append(dict(hit, query=q))
            break                              # 每个检索词先拿最相关的一张，保证多样
        if len(picked) >= N_REFS:
            break
    for q in a.spec["queries"]:                # 检索词不够三个时，用第一个词补
        if len(picked) >= N_REFS:
            break
        for hit in commons_search(q):
            if hit["title"] not in seen and len(picked) < N_REFS:
                seen.add(hit["title"])
                picked.append(dict(hit, query=q))
    rows = ["# 参考照片 · " + a.spec["name_zh"], "",
            "> **只收真实世界照片（Wikimedia Commons，许可见下表）**；游戏截图与权利人官方图不进生成模型（divergence #8 / #108）。",
            "", "| 文件 | 检索词 | 标题 | 作者 | 许可 | 出处 |", "|---|---|---|---|---|---|"]
    for i, h in enumerate(picked, 1):
        ext = ".png" if h["url"].lower().endswith(".png") else ".jpg"
        dest = a.dir / "ref" / f"r{i}{ext}"
        dest.write_bytes(_get(h["url"]))
        rows.append(f"| `{dest.name}` | {h['query']} | {h['title'].replace('|', '/')} | "
                    f"{h['artist'].replace('|', '/')} | {h['license']} | {h['page']} |")
    (a.dir / "ref" / "refs.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"  ✓ {a.key} refs {len(picked)} 张")


# ── images：即梦优先（rule 4l）；auto 失败退 ElevenLabs，显式 dreamina 只用即梦 ──────────
DM_RETRIES = 3
DM_RETRYABLE = re.compile(r"do request|connection|timeout|deadline|EOF|reset|没回 JSON|upload", re.I)


def _dm_tasks() -> list[dict]:
    r = dm.subprocess.run([str(dm.DREAMINA), "list_task"], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=120)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return []


def _dm_submit(prompt: str, refs: list[Path], ratio: str = "1:1", wait_s: int = 240) -> tuple[str | None, int]:
    """即梦提交 + 取回，**可多进程并发**。

    `gen_images_xianjian.submit` 在 CLI 没回 JSON 时用「提交前后 list_task 差集」找回任务——
    两个进程同时提交时差集里有别人的任务，会把 A 的图存成 B 的。这里改按 **prompt 全文**匹配
    （每件资产每个视角的 prompt 都不同），于是并发安全。即梦提交即扣费：找回只重查、绝不重交。
    """
    cmd = [str(dm.DREAMINA)] + (["image2image", "--images", ",".join(str(r) for r in refs)] if refs else ["text2image"])
    # 只提交、不让 CLI 自己轮询：它轮询时网络超时就整条报错、不吐 submit_id（实测 2026-09-25，三个任务其实都已成功扣费），
    # 下面的 query_result 循环对单次超时是容忍的
    cmd += [f"--prompt={prompt}", f"--ratio={ratio}", "--resolution_type=2k", "--model_version=5.0", "--poll=0"]
    res = dm.subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=420)
    payload = dm._payload(res.stdout)
    if payload and payload.get("gen_status") == "success" and dm._url_of(payload):
        return dm._url_of(payload), int(payload.get("credit_count") or 0)
    if payload and payload.get("gen_status") == "fail":
        raise RuntimeError(f"即梦生成失败：{str(payload.get('fail_reason'))[:200]}")
    sid = str(payload.get("submit_id")) if payload and payload.get("submit_id") else None
    if not sid:
        mine = [t for t in _dm_tasks() if (t.get("prompt") or "").strip() == prompt.strip()]
        if not mine:
            # list_task 对长 prompt（实测场景图 ~1500 字）不回 prompt 字段，找不到 ≠ 没提交：可能已扣费，别急着重交，
            # 先用 `dreamina list_task` 看最近几条无 prompt 的任务、按尺寸认领（实测 bg1 世界锚点就是这样找回的）
            raise RuntimeError(f"即梦没回 JSON、list_task 里也按 prompt 找不到（可能已提交扣费）：{res.stdout.strip()[:120]}")
        sid = str(mine[0]["submit_id"])
    for _ in range(max(1, wait_s // 20)):      # 默认再等 4 分钟；超时抛出 → 外层跳过 / 退 ElevenLabs（积分已扣，别急着放弃）
        q = dm.subprocess.run([str(dm.DREAMINA), "query_result", f"--submit_id={sid}"], capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=120)
        got = dm._payload(q.stdout)
        if got and got.get("gen_status") == "success" and dm._url_of(got):
            return dm._url_of(got), int(got.get("credit_count") or 0)
        if got and got.get("gen_status") == "fail":
            raise RuntimeError(f"即梦生成失败：{str(got.get('fail_reason'))[:200]}")
        time.sleep(20)
    raise RuntimeError(f"即梦 {sid} 等了 {wait_s // 60} 分钟仍未出图（积分已扣；稍后 dreamina query_result --submit_id={sid} 可取回）")


def _dreamina(a: Asset, i: int, prompt: str, refs: list[Path]) -> bool:
    url, cost = _dm_submit(prompt, refs, wait_s=900)   # 排队慢时 4 分钟不够（实测 2026-09-25 晚），积分已扣，多等
    dm.download(url, a.view(i))
    a.log(**{f"dreamina_{VIEWS[i]}": cost})
    return True


def _elevenlabs(a: Asset, i: int, prompt: str, refs: list[Path]) -> bool:
    key = el.api_key()
    gid = el.create(key, prompt, model=el.DEFAULT_MODEL, quality="medium", aspect="1:1",
                    resolution="2K", refs=[el.inline(p) for p in refs] or None)
    el.wait_download(key, gid, a.view(i))
    a.log(**{f"elevenlabs_{VIEWS[i]}": gid})
    return True


def request(a: Asset, i: int, engine: str) -> tuple[str, list[Path]]:
    """第 i 面交给 engine 的（送审稿, 参考图）——images 与 plan 共用。正面挂真实照片，只借材质与构造；
    no_text 物件正面不挂（照片常带字：实测把卢恩手稿、手写信、纪念牌、书封的字带进了 ep02 物件图）；
    侧 / 背只挂正面图（钉死同一件东西，只换机位）。即梦超 1600 字先丢负面词、不丢正文（同 gen_bg_images.plan_for；
    props 的 check 已把送审稿压在限内，丢词只会落在不过 check 的装备卡上）。"""
    refs = ([] if a.no_text else a.refs()[:N_REFS]) if i == 0 else [a.view(0)]
    text = a.send(i)
    return (a.prompts()[i] if engine == ie.DREAMINA and len(text) > dm.PROMPT_MAX else text), refs


def do_plan(a: Asset, engine: str) -> None:
    print(f"■ {a.key} {a.spec['name_zh']} · 出{'/'.join(VIEW_NAMES[i] for i in a.views)}"
          f"{' · ' + NO_TEXT if a.no_text else ''}")
    for i in a.views:
        text, refs = request(a, i, engine)
        tail = text.rsplit("\n", 1)[-1]
        neg = (f"末行 {len(tail)} 字：{tail[:12]}…{tail[-36:]}" if text != a.prompts()[i]
               else "负面词没进（即梦超字数丢了）" if a.neg() else "卡里没有「## 负面词」块")
        print(f"  {VIEWS[i]} 送审 {len(text)} 字 · 参考 {[r.name for r in refs] or '无'}"
              f"{' · 已出图' if a.view(i).is_file() else ''}\n    {neg}")


def do_images(a: Asset, engine: str, force: bool) -> None:
    for i in a.views:
        out = a.view(i)
        if out.is_file() and not force:
            continue
        if i and not a.view(0).is_file():
            print(f"  ! {a.key} 没有正面图，侧 / 背无从参考")
            return
        t0 = time.time()
        ok = False
        if engine in (ie.DREAMINA, ie.AUTO):
            prompt, refs = request(a, i, ie.DREAMINA)
            # 网络超时先退避重试（实测 2026-09-25 即梦接口 2–5s 才回头），别一失败就花贵的 ElevenLabs
            for attempt in range(DM_RETRIES + 1):
                try:
                    ok = _dreamina(a, i, prompt, refs)
                    break
                except Exception as e:     # noqa: BLE001
                    print(f"  ! {a.key}-{VIEWS[i]} 即梦失败（第 {attempt + 1} 次）：{str(e)[:160]}")
                    if not DM_RETRYABLE.search(str(e)) or attempt == DM_RETRIES:
                        break
                    time.sleep(45 * (attempt + 1))
        if not ok and engine == ie.DREAMINA:
            # 显式 --engine dreamina ＝ 只用即梦（rule 4l）：失败就报出来、不退 ElevenLabs，重跑同一条命令即续
            raise RuntimeError(f"{a.key}-{VIEWS[i]} 即梦失败，未退 ElevenLabs")
        if not ok:
            print(f"  · {a.key}-{VIEWS[i]} 改走 ElevenLabs")
            prompt, refs = request(a, i, ie.ELEVENLABS)
            ok = _elevenlabs(a, i, prompt, refs)
        print(f"  ✓ {out.name}  {time.time() - t0:.0f}s")


# ── mesh：三视图 → Rodin GLB ───────────────────────────────────────────
def balance(key: str) -> float | None:
    try:
        req = urllib.request.Request(f"{rodin.API}/check_balance", headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return float(json.loads(r.read())["balance"])
    except Exception:   # noqa: BLE001 —— 余额只做记账，查不到不影响出模
        return None


def do_mesh(a: Asset, tier: str, force: bool) -> None:
    if len(a.views) < len(VIEWS):
        print(f"  · {a.key} 只出{'/'.join(VIEW_NAMES[i] for i in a.views)}（{VIEWS_KEY}）：只当镜头参考，不出模")
        return
    if a.glb.is_file() and not force:
        return
    views = [a.view(i) for i in range(3)]
    if not all(v.is_file() for v in views):
        print(f"  ! {a.key} 三视图不齐，不出模")
        return
    key = rodin.api_key()
    b0 = balance(key)
    if b0 is not None and b0 < MIN_BALANCE:
        raise RuntimeError(f"Rodin 余额 {b0} < 保底 {MIN_BALANCE}（留给第一季重出模），本件不出模——充值后重跑 mesh 即补")
    t0 = time.time()
    job = rodin.create_job(key, a.spec["prompt_en"], views, list(a.spec["size_m"]), tier, "Raw")
    rodin.wait(key, job["jobs"]["subscription_key"], 600)   # 10 分钟不出就跳过（超时 raise，外层记账后继续）
    rodin.download(key, job["uuid"], a.glb)
    b1 = balance(key)
    a.log(rodin_uuid=job["uuid"], rodin_tier=tier, rodin_cost=(b0 - b1) if b0 is not None and b1 is not None else None,
          rodin_balance_after=b1)
    print(f"  ✓ {a.glb.name}  {a.glb.stat().st_size // 1024} KB  {time.time() - t0:.0f}s  credits {b0}→{b1}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("check", "plan", "refs", "images", "mesh", "all"))
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--engine", default=ie.AUTO, choices=ie.CHOICES,
                    help="auto ＝ 即梦、失败退 ElevenLabs；显式指定 ＝ 只用那一家（rule 4l）")
    ap.add_argument("--tier", default="Sketch", choices=("Sketch", "Regular"))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--shard", default="0/1", help="k/n：只做第 k 份（共 n 份），多进程并发时各拿不相交的一份")
    args = ap.parse_args()
    assets = find_assets(args.paths)
    k, n = (int(x) for x in args.shard.split("/"))
    if not 0 <= k < n:
        raise SystemExit(f"--shard {k}/{n}：k 从 0 数到 n-1（{k}/{n} 会漏掉第 0 份）")
    assets = assets[k::n]
    if not assets:
        raise SystemExit("范围里没有任何场景物件（props/p{N}_*/asset.toml）")
    bad = 0
    for a in assets:
        errs = check(a)
        if errs:
            bad += 1
            print(f"❌ {a.dir.relative_to(REPO)}")
            for e in errs:
                print(f"   - {e}")
    print(f"资产 {len(assets)} 个 · 契约不过 {bad}")
    if args.step == "check" or bad:
        return 1 if bad else 0
    if args.step == "plan":
        for a in assets:
            do_plan(a, ie.ELEVENLABS if args.engine == ie.ELEVENLABS else ie.DREAMINA)
        return 0
    # 一件资产卡住（即梦不回、Rodin 超时、网络断）就记下来跳过，接着做下一件——
    # 用户 2026-09-24：「哪一步太久没反应就跳过，继续做剩下的」。产物按文件落盘，下次重跑只补缺的。
    skipped: list[str] = []
    for a in assets:
        print(f"■ {a.key} {a.spec['name_zh']}", flush=True)
        for step, fn in (("refs", lambda: do_refs(a, args.force)),
                         ("images", lambda: do_images(a, args.engine, args.force)),
                         ("mesh", lambda: do_mesh(a, args.tier, args.force))):
            if args.step not in (step, "all"):
                continue
            try:
                fn()
            except (Exception, SystemExit) as e:   # noqa: BLE001
                msg = f"{a.key} {step}：{str(e)[:200]}"
                a.log(**{f"skipped_{step}": str(e)[:300]})
                if step == "refs":
                    # 找不到参考照片不该拖住整件资产：退成纯文字出图，日志里记下来，之后可以 --force 补照片重出
                    print(f"  ⚠ {msg} —— 无参考照片，改纯文字出图", flush=True)
                    continue
                print(f"  ⏭ 跳过 {msg}", flush=True)
                skipped.append(msg)
                break
    print(f"\n完成 {len(assets) - len(skipped)} / {len(assets)}；跳过 {len(skipped)}")
    for s in skipped:
        print(f"  ⏭ {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
