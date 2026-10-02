# -*- coding: utf-8 -*-
"""抓取游戏内地图，建**内部参考图库**（不入画、不上传给生成模型）。

用法（仓库根目录）：
    python tools/fetch_wow_maps.py --all           # 大陆 + 全部区 + 微型地下城 + 副本
    python tools/fetch_wow_maps.py --season1       # 只抓第一季要拍的
    python tools/fetch_wow_maps.py --zone elwynn_forest --dry-run
    python tools/fetch_wow_maps.py --index         # 只重建 INDEX.md

产物：`{drama}/0_research/map/refs/`，**目录结构镜像世界树**：

    refs/
    ├── INDEX.md
    ├── eastern_kingdoms/
    │   ├── _continent/WorldMap-Azeroth-vanilla.jpg
    │   └── kingdom_of_stormwind/
    │       └── elwynn_forest/
    │           ├── WorldMap-Elwynn_c60.jpg
    │           ├── refs.md
    │           └── microdungeons/WorldMap-MicroDungeon-Elwynn-FargodeepMine.jpg
    └── kalimdor/…

## 版本优先级（本项目的命门）

wiki 上同一个区有七八个版本。本剧锚定 **Vanilla 1.12**，而 **4.0.3a 把人族 1–30 级区域整体重画过**——
**挑错版本 ＝ 把头号雷区直接请进来**。所以：

    c60（经典旧世）  >  -vanilla  >  主图（无后缀）  >  其余一律不要

**硬排除**：`-tbc` / `-cata` / `-wotlk` / `-mop` / `-legion` / `-bfa` / `-alpha` / `-beta` /
`-old*` / `PetBattle` / 结尾数字的重复版。每张图的实际版本写进 `refs.md`，**拿不到 c60 的会在结尾单独列出来警告**。

## 用途边界（`divergence #8` / sk2 `#108`，不可商量）

**图只进人眼，不进模型。** 唯一用途是人（含 Claude 读图）逐张看过、把地貌与布局写成**中文锁定串**，
锁定串才进 prompt。**一张都不上传给生成模型**——① 暴雪美术资产不可再分发；
② 实测「喂图出图」会把游戏引擎的光照、材质、边缘锐度 1:1 带进画面，正是半写实路线要防的那件事。

媒体在 `ai_videos/` 下本来就被 gitignore；要同步走 `tools/assets_sync.py`。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DRAMA = os.path.join(REPO, "ai_videos", "shengji_zhilu")
TREE = os.path.join(DRAMA, "0_research", "map", "world_tree.json")
REFS = os.path.join(DRAMA, "0_research", "map", "refs")
API = "https://warcraft.wiki.gg/api.php"
UA = {"User-Agent": "shengji_zhilu-research/1.0 (internal reference; not redistributed)"}

SEASON1 = ("northshire_valley", "elwynn_forest", "westfall", "stormwind_city",
           "redridge_mountains", "duskwood")

# 后缀 → 版本标签。顺序即优先级；不在表里的一律拒绝。
VERSION_RANK: tuple[tuple[str, str], ...] = (
    (" c60", "经典旧世 1.12（c60）"),
    ("-vanilla", "经典旧世（vanilla）"),
    ("", "⚠ 现行零售版（无经典变体）"),
)
REJECT = re.compile(r"(-tbc|-cata|-wotlk|-mop|-legion|-bfa|-sl|-df|-alpha|-beta|-old|"
                    r"petbattle|-early|-\d+\.\d+|VON |Classic-alpha)", re.I)

# wiki 的地图 key ≠ 区名。只写确实查证过的，**不猜**。
KEY_OVERRIDE: dict[str, str] = {
    "northshire_valley": "Elwynn", "stormwind_city": "StormwindCity", "redridge_mountains": "Redridge",
    "the_barrens": "Barrens", "eastern_plaguelands": "EasternPlaguelands",
    "western_plaguelands": "WesternPlaguelands", "the_hinterlands": "Hinterlands",
    "un_goro_crater": "UnGoroCrater", "thousand_needles": "ThousandNeedles",
    "dustwallow_marsh": "DustwallowMarsh", "stranglethorn_vale": "StranglethornVale",
    "swamp_of_sorrows": "SwampOfSorrows", "blasted_lands": "BlastedLands",
    "burning_steppes": "BurningSteppes", "searing_gorge": "SearingGorge",
    "deadwind_pass": "DeadwindPass", "loch_modan": "LochModan", "dun_morogh": "DunMorogh",
    "alterac_mountains": "Alterac", "arathi_highlands": "Arathi", "hillsbrad_foothills": "Hillsbrad",
    "silverpine_forest": "SilverpineForest", "tirisfal_glades": "Tirisfal",
    "stonetalon_mountains": "StonetalonMountains", "thunder_bluff": "ThunderBluff",
    "moonglade": "Moonglade", "un_goro": "UnGoroCrater", "azshara": "Azshara",
    "blackrock_mountain": "BlackrockMountain", "booty_bay": "StranglethornVale",
    "shadowforge_city": "BlackrockDepths",
}
CONTINENT_KEY = {"eastern_kingdoms": "Azeroth", "kalimdor": "Kalimdor"}


def api(params: dict[str, str]) -> dict:
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def search_files(q: str, limit: int = 30) -> list[str]:
    try:
        d = api({"action": "query", "list": "search", "srsearch": q, "srnamespace": "6", "srlimit": str(limit)})
        return [r["title"] for r in d.get("query", {}).get("search", [])]
    except Exception as e:
        print("      搜索失败:", type(e).__name__, str(e)[:70])
        return []


def pick_versioned(files: list[str], key: str) -> tuple[str, str] | None:
    """在候选里按版本优先级挑一张：c60 > -vanilla > 主图。拒绝后续资料片与各种 old/alpha。"""
    for suffix, label in VERSION_RANK:
        pat = re.compile(r"^File:WorldMap-" + re.escape(key) + re.escape(suffix) + r"\.jpg$", re.I)
        for f in files:
            if pat.match(f) and not REJECT.search(f.replace(suffix, "")):
                return f, label
    return None


def info(title: str) -> dict:
    d = api({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|size|mime"})
    pg = next(iter(d["query"]["pages"].values()))
    return (pg.get("imageinfo") or [{}])[0]


def download(url: str, dest: str) -> int:
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        return -1  # 已有，跳过（可断点续）
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        data = r.read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(data)
    return len(data)


class Tree:
    def __init__(self) -> None:
        raw = json.load(io.open(TREE, encoding="utf-8"))
        self.n = {x["id"]: x for x in raw["nodes"]}

    def chain(self, nid: str) -> list[str]:
        out, cur = [], nid
        while cur:
            out.append(cur)
            cur = self.n.get(cur, {}).get("parent")
        return list(reversed(out))

    def path_of(self, zid: str) -> str:
        """镜像世界树：refs/{大陆}/{分区}/{区}/"""
        parts = [p for p in self.chain(zid) if self.n[p]["type"] in ("continent", "region", "zone", "city")]
        return os.path.join(REFS, *parts)

    def zone_of(self, nid: str) -> str | None:
        cur = self.n[nid].get("parent")
        while cur and cur in self.n:
            if self.n[cur]["type"] in ("zone", "city"):
                return cur
            cur = self.n[cur].get("parent")
        return None


def write_refs_md(d: str, z: dict, got: list[tuple[str, str, str, dict]], zid: str) -> None:
    rows = "\n".join(
        f"| `{fn}` | {title} | {ii.get('width')} × {ii.get('height')} | **{ver}** |"
        for fn, title, ver, ii in got)
    io.open(os.path.join(d, "refs.md"), "w", encoding="utf-8", newline="\n").write(
        f"""# 参考图 · {z['name_zh']}（{z['name_en']}）

> **用途边界（`divergence #8` / sk2 `#108`，不可商量）：图只进人眼，不进模型。**
> 唯一用途是人逐张看过、把地貌与布局写成**中文锁定串**，锁定串才进 prompt。
> **一张都不上传给生成模型**——① 暴雪美术资产不可再分发；
> ② 实测「喂图出图」会把游戏引擎的光照与材质 1:1 带进画面，正是半写实路线要防的那件事。
> 版权归**暴雪娱乐**；本目录是内部参考，不再分发。

| 文件 | 来源 | 尺寸 | 版本 |
|---|---|---|---|
{rows}

## 怎么用它

1. **人眼核点位**：对着它看我们生成的点位图（`../../../images/zones/{zid}.png`）标得对不对。
2. **写锁定串**：把地貌 / 道路 / 水系 / 建筑群的**形制**写成中文，落进场景卡的锁定描述符。
3. **补坐标**：在图上量百分比坐标，回填 `map/g*.yaml` 的 `coords`，生成图就会越来越密。
4. **出 floor plan**：本图是 `ai_video.md` rule 4j 航线俯视图的底图依据之一。

抓取：`python tools/fetch_wow_maps.py --zone {zid}`
""")


def build_index(t: Tree) -> None:
    lines = ["# 参考图库索引 · 游戏内地图", "",
             "> 由 `tools/fetch_wow_maps.py --index` 生成。**目录结构镜像世界树**（大陆 / 分区 / 区）。",
             "> **图只进人眼，不进模型**（`divergence #8`）。版权归暴雪娱乐，内部参考，不再分发。", ""]
    total = 0
    retail: list[str] = []
    for dp, _, fs in sorted(os.walk(REFS)):
        imgs = [f for f in fs if f.lower().endswith((".jpg", ".png"))]
        if not imgs:
            continue
        rel = os.path.relpath(dp, REFS).replace(os.sep, "/")
        depth = rel.count("/")
        name = os.path.basename(dp)
        zh = t.n.get(name, {}).get("name_zh", name)
        lines.append("  " * depth + f"- **{zh}** `{rel}/` — {len(imgs)} 张")
        for f in sorted(imgs):
            # **微型地下城图在 wiki 上根本没有 `_c60` 变体**——它们只有一个版本。
            # 把「没有经典变体」一律标成「⚠ 只拿到零售版」，等于把 50 张本来就只有一版的图
            # 指控成版本错置，然后在结尾印一句「54 张只有零售版」的假警报。
            # 真正需要人工减掉后加内容的，只有**区域地图**里拿不到 c60 的那几张。
            if "c60" in f:
                tag = "c60"
            elif "vanilla" in f.lower():
                tag = "vanilla"
            elif "MicroDungeon" in f:
                tag = "单版本（微型地下城无 c60 变体）"
            else:
                tag = "⚠ 零售"
                retail.append(f"{zh} / {f}")
            lines.append("  " * depth + f"  - `{f}` · {tag}")
            total += 1
    lines += ["", f"**合计 {total} 张。**", ""]
    if retail:
        lines += ["## ⚠ 只拿到现行零售版的区域地图（没有经典变体）", "",
                  "**4.0.3a 把人族 1–30 级区域整体重画过**，看这些图时要自己减掉后加的东西。",
                  "微型地下城图**不在此列**——它们在 wiki 上本来就只有一个版本，不是版本错置。", ""]
        lines += [f"- {r}" for r in retail]
    io.open(os.path.join(REFS, "INDEX.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print(f"\nINDEX.md：{total} 张图" + (f"；其中 {len(retail)} 张只有零售版" if retail else ""))


def fetch_zone(t: Tree, zid: str, dry: bool) -> tuple[int, str | None]:
    z = t.n[zid]
    key = KEY_OVERRIDE.get(zid) or re.sub(r"[^A-Za-z]", "", (z["name_en"] or "").replace("The ", "").split()[0])
    d = t.path_of(zid)
    print(f"\n{z['name_zh']}（{z['name_en']}）  key={key}")
    got: list[tuple[str, str, str, dict]] = []

    chosen = pick_versioned(search_files("WorldMap-" + key), key)
    if not chosen:
        print("      ✗ 没找到区域地图")
        return 0, zid
    title, ver = chosen
    ii = info(title)
    if not ii.get("url"):
        return 0, zid
    fn = title.replace("File:", "").replace(" ", "_")
    print(f"      {fn}  {ii.get('width')}x{ii.get('height')}  [{ver}]")
    if not dry:
        n = download(ii["url"], os.path.join(d, fn))
        print("      " + ("已有，跳过" if n < 0 else f"→ {n/1024:.0f} KB"))
    got.append((fn, title, ver, ii))

    # 微型地下城（矿洞 / 洞穴内部）——ep02 回音山、ep03 法戈第正要用
    micro = [f for f in search_files(f"WorldMap-MicroDungeon-{key}", 30)
             if re.match(rf"^File:WorldMap-MicroDungeon-{re.escape(key)}-", f, re.I) and not REJECT.search(f)]
    for m in micro[:12]:
        mi = info(m)
        if not mi.get("url"):
            continue
        mfn = m.replace("File:", "").replace(" ", "_")
        print(f"      · 微型地下城 {mfn}  {mi.get('width')}x{mi.get('height')}")
        if not dry:
            download(mi["url"], os.path.join(d, "microdungeons", mfn))
            time.sleep(0.4)
        got.append((f"microdungeons/{mfn}", m, "微型地下城", mi))

    if not dry:
        os.makedirs(d, exist_ok=True)
        write_refs_md(d, z, got, zid)
        time.sleep(0.6)
    return len(got), None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zone")
    ap.add_argument("--season1", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    t = Tree()
    if args.index:
        build_index(t)
        return 0

    # 大陆图
    if args.all or args.season1:
        for cid, key in CONTINENT_KEY.items():
            if cid not in t.n:
                continue
            chosen = pick_versioned(search_files("WorldMap-" + key), key)
            if not chosen:
                continue
            title, ver = chosen
            ii = info(title)
            fn = title.replace("File:", "").replace(" ", "_")
            print(f"\n【大陆】{t.n[cid]['name_zh']}  {fn}  {ii.get('width')}x{ii.get('height')}  [{ver}]")
            if not args.dry_run and ii.get("url"):
                n = download(ii["url"], os.path.join(REFS, cid, "_continent", fn))
                print("      " + ("已有，跳过" if n < 0 else f"→ {n/1024:.0f} KB"))

    zones = [n["id"] for n in t.n.values() if n["type"] in ("zone", "city")]
    targets = [args.zone] if args.zone else (list(SEASON1) if args.season1 else sorted(zones))
    total, miss = 0, []
    for zid in targets:
        if zid not in t.n:
            print("没有这个区：", zid)
            continue
        n, m = fetch_zone(t, zid, args.dry_run)
        total += n
        if m:
            miss.append(m)

    print(f"\n共 {total} 张；{len(miss)} 个区没找到区域地图" +
          (f"：{'、'.join(t.n[m]['name_zh'] for m in miss)}" if miss else ""))
    if not args.dry_run:
        build_index(t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
