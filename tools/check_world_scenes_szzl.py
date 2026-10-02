# -*- coding: utf-8 -*-
"""《圣光刚好够用》全图 scene 的机检闸门 —— follow-up 006 四项裁定的可执行版。

用法（仓库根目录）：
    python tools/check_world_scenes_szzl.py                       # 全部 scenes
    python tools/check_world_scenes_szzl.py <区目录 | bg 目录>     # 只查一个范围
    python tools/check_world_scenes_szzl.py --summary             # 只打印覆盖率表，不判错

每个 bg 目录查（blocker 任一命中即 exit 1）：
    W1  目录名 `bg{N}_主体` + 同名 md（主体判据，12.9）；在 registry.toml 登记且落在登记的 大陆/区 目录下
    W2  主体 md 里没有留下生成器的 `〔作者填写〕` 占位；没有 hex；五个必需节齐
    W3  一句话锁定 非空且 ≤30 字（K8）
    W4  锚点 prompt：首行 ＝ 目录名（4b-A）；正文（去空白）1500–2000 字；不含红级 IP 词（魔兽/暴雪/Warcraft/Blizzard/WoW）
    W5  版本红线：`tools/wow_version_gate.py` HARD 命中即 blocker（SCOPED 只 warning）
    W6  平面图按 `planschema.resolve` 解析得到：自己拥有 `planning/blocks.toml`，或 `planning/plan.toml` 指向拥有它的目录
        （指针目录到此为止，W6 / W7 由被指的目录答）；拥有的那份过 `planschema.check`（bg 键只许指同级目录）且 `[meta] bg` ＝ 目录键
    W7  （拥有平面图的目录）floor plan 已出且是最新的：`planning/{bg}_floorplan.png` 与 `{bg}_blocks.md` 存在，md 抬头的 `blocks.toml@sha8` ＝ 当前 toml 的 sha8
    W8  `ref/` 里至少一个 `.link.json` 指向存在的原版地图（图只进人眼）
    W9  prompt 正文（去掉首行路由键与 `参考:` 行）不含黄级专名（concept C3：世界内地名 / 种族名 / 职业名，
        text-only 实测放行之前一律不进生成块）。词表取世界树里 大陆 / 分区 / 地区 / 主城 / 聚居点 的
        简中名（≥3 字，城区是普通名词不收）+ 子区域名（≥4 字）+ 本剧特有的种族 / 职业译名；泛称（矮人、兽人、精灵）不算
    W10 （warning）同一区内两张卡的 prompt 正文共用 ≥2 句 ≥24 字的原句——复制粘贴出来的卡，出图会一模一样
        （`风格:` / `比例:` 行与「画面里没有……」反向声明按设计就是共用的，不算）
    W11 bg 目录树里不许有任何 `.glb`；本剧 `props/` 里 GLB 只许是 `p{N}_{名}/mesh/p{N}.glb`
        ——一个 GLB 只装一个物体，多物体的场景由 blend 汇总（2026-09-25 用户定调）
    W12 （warning）还没有场景图 `{目录}.png`——build_scene 见不到它就不建 blend（图先行）
    W13 prompt 正文里有「相机 / 摄影机 / 摄像机 / 镜头架」——出图模型会把它画成一台实物相机；写「视点在…」
每个区目录查：同名区卡 md、`ref/` 有区图链接、至少一个 bg、不再有 `_assets/`（Z4：物件只住 props/）。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import tomllib
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, REPO)
from tools import check_stage2, wow_version_gate  # noqa: E402
from tools.previz import planschema  # noqa: E402
from tools.gen_world_scenes_szzl import TREE  # noqa: E402
from tools import props_lib  # noqa: E402

DRAMA = os.path.join(REPO, "ai_videos", "shengji_zhilu")
SCENES = os.path.join(DRAMA, "2_世界观人设", "scenes")
REGISTRY = os.path.join(SCENES, "registry.toml")
FILL = "〔作者填写〕"
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
BG_DIR = re.compile(r"^bg(\d+)_[^_]+$")
LOCK_ROW = re.compile(r"^\|[^|]*\|[^|]*一句话锁定[^|]*\|(.+?)\|\s*$", re.M)
IP_RED = ("魔兽", "暴雪", "Warcraft", "warcraft", "Blizzard", "blizzard", "WoW", "wow.gg")
SECTIONS = ("## 场景定位", "## 锁定描述符", "## 关键变化态", "## 出现镜头", "步骤一")
SHA_RE = re.compile(r"blocks\.toml@([0-9a-f]{8})")
PROMPT_MIN, PROMPT_MAX = 1500, 2000
SKIP = frozenset({"_deleted", "renders", "previz", "frames", "__pycache__"})
# follow-up 006 之前建好的 9 张 v3 卡：字数口径与负向写法与新骨架不同，W4 字数 / W5 红线降为 warning。
# **显式清单，只减不增**（同 prompt_light 的 legacy 口径）——新卡一犯就是 blocker。
LEGACY = frozenset({"bg1", "bg2", "bg3", "bg17", "bg18", "bg19", "bg20", "bg21", "bg22"})
# W9 黄级词表的非地名部分：只收魔兽特有的译名，泛奇幻词（矮人 / 兽人 / 精灵 / 巨魔 / 侏儒 / 食人魔）不收——
# 它们是有用的形制描述（「矮人式石屋」），收进来就是一道天天误报的闸门。
YELLOW_EXTRA = ("艾泽拉斯", "卡利姆多", "洛丹伦", "卡兹莫丹", "奎尔萨拉斯", "艾尔文",
                "暗夜精灵", "牛头人", "被遗忘者", "豺狼人", "狗头人", "鱼人", "熊怪", "鹰身人", "其拉",
                "血色十字军", "天灾军团", "迪菲亚", "圣骑士", "萨满祭司", "德鲁伊")
# 世界树里字面就是描述的地名（「十字路口」「芦苇海滩」）——正文里用它是在描写，不是在点名
YELLOW_GENERIC = frozenset({"十字路口", "芦苇海滩"})
_YELLOW: tuple[str, ...] | None = None


def yellow_words() -> tuple[str, ...]:
    global _YELLOW
    if _YELLOW is None:
        tree = json.load(io.open(TREE, encoding="utf-8"))
        words = set(YELLOW_EXTRA)
        for n in tree["nodes"]:
            zh = (n.get("name_zh") or "").strip()
            t = n.get("type")
            # 城区（贸易区 / 住宅区 / 王座厅）是普通名词，不收
            if (t in ("continent", "region", "zone", "city", "settlement") and len(zh) >= 3) or \
               (t == "subzone" and len(zh) >= 4):
                words.add(zh)
        words -= YELLOW_GENERIC
        _YELLOW = tuple(sorted(words, key=len, reverse=True))
    return _YELLOW


def prompt_body(block: str) -> str:
    """锚点 prompt 里真正喂给模型的正文：去掉首行路由键与 `参考:` 行（两者按规定就带专名）。"""
    return "\n".join(l for l in block.split("\n")[1:] if not l.startswith("参考:"))


@dataclass
class Issue:
    where: str
    level: str
    code: str
    detail: str


def rel(p: str) -> str:
    return os.path.relpath(p, REPO).replace(os.sep, "/")


def prompt_len(block: str) -> int:
    body = "\n".join(block.split("\n")[1:])
    return len(re.sub(r"\s+", "", body))


def check_bg(d: str, reg: dict[str, dict], siblings: dict[str, str]) -> list[Issue]:
    name = os.path.basename(d)
    out: list[Issue] = []
    key = name.split("_", 1)[0]
    md = os.path.join(d, name + ".md")
    if not os.path.isfile(md):
        return [Issue(rel(d), "blocker", "W1", "目录里没有同名主体 md")]
    r = reg.get(name)
    if r is None:
        out.append(Issue(rel(d), "blocker", "W1", "registry.toml 里没有登记这个目录"))
    else:
        want = os.path.join(SCENES, r["continent"], r["zone"], name)
        if os.path.abspath(want) != os.path.abspath(d):
            out.append(Issue(rel(d), "blocker", "W1", "目录落点与登记不符，应在 %s" % rel(want)))
    text = io.open(md, encoding="utf-8").read()
    if FILL in text:
        out.append(Issue(rel(md), "blocker", "W2", "还有 %d 处「%s」占位没填" % (text.count(FILL), FILL)))
    for h in sorted(set(HEX.findall(text))):
        out.append(Issue(rel(md), "blocker", "W2", "出现 hex 色值 %s" % h))
    # 没写「档级」的老卡按 v3 五 plate 档处理（check_stage2 管它们的 plate），这里不判
    for s in SECTIONS:
        if s not in text:
            out.append(Issue(rel(md), "blocker", "W2", "缺「%s」节" % s))
    lock = check_stage2._lock_string(text)     # 与 check_stage2 同一把尺（K8）
    if lock is None:
        out.append(Issue(rel(md), "blocker", "W3", "锁定描述符缺「一句话锁定」行"))
    elif not lock or FILL in lock:
        out.append(Issue(rel(md), "blocker", "W3", "一句话锁定为空"))
    elif len(lock) > 30:
        out.append(Issue(rel(md), "blocker", "W3", "一句话锁定 %d 字 > 30：%s" % (len(lock), lock)))
    if lock:
        # 一句话锁定会 byte-identical 进每个 shot 的 `场景:` 行 ＝ 进生成块，C3 同样管它
        hit = sorted({w for w in yellow_words() if w in lock})
        if hit:
            out.append(Issue(rel(md), "warning" if key in LEGACY else "blocker", "W9",
                             "一句话锁定含黄级专名（它会进每个 shot 的 `场景:` 行）：%s——换成形制描述" % "、".join(hit)))
    blocks = re.findall(r"```text\n(.*?)\n```", text, re.S)
    if not blocks:
        out.append(Issue(rel(md), "blocker", "W4", "没有 ```text 锚点 prompt 块"))
    else:
        b = blocks[0]
        first = b.split("\n")[0].strip()
        if first != name:
            out.append(Issue(rel(md), "blocker", "W4", "prompt 首行「%s」≠ 目录名（路由键要在首位）" % first[:40]))
        n = prompt_len(b)
        lvl = "warning" if key in LEGACY else "blocker"
        if n < PROMPT_MIN:
            out.append(Issue(rel(md), lvl, "W4", "锚点 prompt %d 字 < %d（写短了后面所有图一起降级）" % (n, PROMPT_MIN)))
        elif n > PROMPT_MAX:
            out.append(Issue(rel(md), lvl, "W4", "锚点 prompt %d 字 > %d 硬顶" % (n, PROMPT_MAX)))
        for tok in IP_RED:
            if tok in b:
                out.append(Issue(rel(md), "blocker", "W4", "prompt 里出现红级 IP 词「%s」" % tok))
        body = prompt_body(b)
        hit = sorted({w for w in yellow_words() if w in body})
        if hit:
            out.append(Issue(rel(md), "warning" if key in LEGACY else "blocker", "W9",
                             "prompt 正文出现黄级专名（C3，实测放行前不进生成块）：%s——改成不点名的形制描述" % "、".join(hit[:8])))
        cam = sorted(set(re.findall(r"相机|摄影机|摄像机|镜头架", body)))
        if cam:
            out.append(Issue(rel(md), "blocker", "W13", "prompt 里有「%s」——会被画成一台实物相机（实测 bg19 画出三脚架），改「视点在…」" % "、".join(cam)))
        for i in wow_version_gate.check(name, text):
            out.append(Issue(rel(md), "warning" if key in LEGACY else i.level, "W5", "版本红线「%s」：%s" % (i.token, i.detail)))
    toml_p = os.path.join(d, planschema.PLAN_FILE)
    try:
        owner: str | None = planschema.resolve(d)[0]
    except (planschema.Unresolved, tomllib.TOMLDecodeError) as e:
        owner = None
        out.append(Issue(rel(d), "blocker", "W6", str(e) if os.path.isfile(os.path.join(d, planschema.POINTER_FILE))
                         else "没有 planning/blocks.toml，也没有指向同一块地的 planning/plan.toml（rule 4k：每个 bg 必备）"))
    # 指针目录（plan.toml 指回同一块地，如 bg808 → bg805）不拥有几何：W6 / W7 由被指的目录自己答
    if owner == os.path.abspath(d):
        try:
            with open(toml_p, "rb") as f:
                cfg = tomllib.load(f)
            errs = planschema.check(cfg, d, known_bg=siblings)
            for e in errs:
                out.append(Issue(rel(toml_p), "blocker", "W6", e))
            if cfg.get("meta", {}).get("bg") != key:
                out.append(Issue(rel(toml_p), "blocker", "W6", "[meta] bg=%s ≠ 目录键 %s" % (cfg.get("meta", {}).get("bg"), key)))
        except tomllib.TOMLDecodeError as e:
            out.append(Issue(rel(toml_p), "blocker", "W6", "TOML 解析失败：%s" % e))
            cfg = None
        png = os.path.join(d, "planning", key + "_floorplan.png")
        bmd = os.path.join(d, "planning", key + "_blocks.md")
        if not os.path.isfile(png) or not os.path.isfile(bmd):
            out.append(Issue(rel(d), "blocker", "W7", "floor plan 未出（缺 %s_floorplan.png / %s_blocks.md）" % (key, key)))
        else:
            head = io.open(bmd, encoding="utf-8").read(600)
            m = SHA_RE.search(head)
            cur = planschema.sha(d)
            if not m or m.group(1) != cur:
                out.append(Issue(rel(d), "blocker", "W7", "floor plan 过期：blocks.md 记的是 %s，toml 现在是 %s——重跑 build_floorplan" % (m.group(1) if m else "无", cur)))
    ref = os.path.join(d, "ref")
    links = [f for f in os.listdir(ref)] if os.path.isdir(ref) else []
    ok = False
    for f in links:
        if f.endswith(".link.json"):
            try:
                t = json.load(io.open(os.path.join(ref, f), encoding="utf-8")).get("target", "")
                if os.path.isfile(os.path.join(REPO, t)):
                    ok = True
            except (OSError, ValueError):
                pass
    if not ok:
        out.append(Issue(rel(d), "blocker", "W8", "ref/ 里没有指向存在文件的原版地图 .link.json"))
    for root, _, files in os.walk(d):
        for f in files:
            if f.lower().endswith(".glb"):
                out.append(Issue(rel(os.path.join(root, f)), "blocker", "W11",
                                 "bg 目录里不许有 GLB——GLB 只装单个物体，住本剧 props/p{N}_*/mesh/；多物体的场景是 blend 的活"))
    if not os.path.isfile(os.path.join(d, name + ".png")):
        out.append(Issue(rel(d), "warning", "W12", "还没有场景图 %s.png（build_scene 不建 blend：python tools/gen_bg_images.py run）" % name))
    return out


def check_props_glbs(scope: str) -> list[Issue]:
    """W11：本剧 props/ 里 GLB 只许是 `p{N}_{名}/mesh/p{N}.glb`——一件物件一个物体一个网格（follow-up 012 / 013）。"""
    out: list[Issue] = []
    lib = props_lib.props_root(scope)
    for root, _, files in os.walk(lib):
        for f in files:
            if not f.lower().endswith(".glb"):
                continue
            parts = os.path.relpath(os.path.join(root, f), lib).replace("\\", "/").split("/")
            ok = len(parts) == 3 and parts[1] == "mesh" and parts[0].startswith(f[:-4] + "_") and props_lib.KEY.match(f[:-4])
            if not ok:
                out.append(Issue(rel(os.path.join(root, f)), "blocker", "W11",
                                 "props 里的 GLB 只许是 p{N}_{名}/mesh/p{N}.glb（单个物体）"))
    return out


def check_zone(zdir: str, bgs: list[str]) -> list[Issue]:
    out: list[Issue] = []
    zid = os.path.basename(zdir)
    if not os.path.isfile(os.path.join(zdir, zid + ".md")):
        out.append(Issue(rel(zdir), "blocker", "Z1", "区目录缺同名区卡 md"))
    ref = os.path.join(zdir, "ref")
    if not (os.path.isdir(ref) and any(f.endswith(".link.json") for f in os.listdir(ref))):
        out.append(Issue(rel(zdir), "blocker", "Z2", "区目录 ref/ 里没有原版区图链接"))
    if not bgs:
        out.append(Issue(rel(zdir), "blocker", "Z3", "区目录下没有任何 bg"))
    if os.path.isdir(os.path.join(zdir, "_assets")):
        out.append(Issue(rel(zdir), "blocker", "Z4", "区里还有 _assets/——物件只住本剧 props/（follow-up 013），区里只留 _plan/"))
    return out


def walk(scope: str) -> tuple[list[str], list[str]]:
    """→ (bg 目录, 区目录)。bg 目录 ＝ `bg\\d+_` + 同名 md；区目录 ＝ scenes/{大陆}/{区}。"""
    bgs, zones = [], []
    for dp, dirs, _ in os.walk(scope):
        dirs[:] = sorted(x for x in dirs if x not in SKIP and not x.startswith("."))
        base = os.path.basename(dp)
        if BG_DIR.match(base):
            dirs[:] = []
            bgs.append(dp)
            continue
        relp = os.path.relpath(dp, SCENES).replace(os.sep, "/")
        if relp.count("/") == 1 and not relp.startswith(".") and base != "ref":
            zones.append(dp)
    if BG_DIR.match(os.path.basename(scope)) and scope not in bgs:
        bgs.append(scope)
    return sorted(bgs), sorted(zones)


_CLAUSE = re.compile(r"[。；！？\n]")


def clauses(block: str) -> set[str]:
    out: set[str] = set()
    shared_field = False     # 字段会折行，续行没有字段名，按「当前在哪个字段里」判
    for line in prompt_body(block).split("\n"):
        if re.match(r"^(\S{1,6}[:：]|\[\S{1,6}\])", line):     # `字段:` 或 `[字段]` 两种写法
            shared_field = line.lstrip("[").startswith(("负向", "负面词", "风格", "比例", "参数"))
        if shared_field:
            continue
        for c in _CLAUSE.split(line):
            c = re.sub(r"\s+", "", c)
            if len(c) >= 24 and not c.startswith(("画面里没有", "没有任何", "画面中没有")):
                out.add(c)
    return out


def check_dups(bgs: list[str]) -> list[Issue]:
    """W10：同一父目录（区）内的卡两两比对共用原句。"""
    out: list[Issue] = []
    by_parent: dict[str, list[tuple[str, set[str]]]] = {}
    for b in bgs:
        name = os.path.basename(b)
        md = os.path.join(b, name + ".md")
        if not os.path.isfile(md):
            continue
        blocks = re.findall(r"```text\n(.*?)\n```", io.open(md, encoding="utf-8").read(), re.S)
        if blocks:
            by_parent.setdefault(os.path.dirname(b), []).append((name, clauses(blocks[0])))
    for parent, cards in by_parent.items():
        for i, (a, ca) in enumerate(cards):
            for bname, cb in cards[i + 1:]:
                shared = ca & cb
                if len(shared) >= 2:
                    ex = sorted(shared, key=len)[-1]
                    out.append(Issue(rel(os.path.join(parent, a)), "warning", "W10", "与 %s 共用 %d 句原句（例：「%s」）——各写各的" % (bname, len(shared), ex[:40])))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scope", nargs="?", default=SCENES)
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--json", action="store_true", help="逐条输出 {level, code, where, detail} 的 JSON（给编排脚本读）")
    ap.add_argument("--no-prompt-len", action="store_true", help="跳过 W4 的字数区间（骨架期用）")
    args = ap.parse_args()
    global PROMPT_MIN, PROMPT_MAX
    if args.no_prompt_len:
        PROMPT_MIN, PROMPT_MAX = 0, 10 ** 9
    scope = os.path.abspath(args.scope)
    with open(REGISTRY, "rb") as f:
        reg = {r["dir"]: r for r in tomllib.load(f).get("bg", [])}
    bgs, zones = walk(scope)
    issues: list[Issue] = []
    for z in zones:
        zbgs = [b for b in bgs if os.path.dirname(b) == z]
        issues.extend(check_zone(z, zbgs))
    for b in bgs:
        parent = os.path.dirname(b)
        sib = {n.split("_", 1)[0]: n for n in os.listdir(parent) if BG_DIR.match(n) and os.path.isdir(os.path.join(parent, n))}
        issues.extend(check_bg(b, reg, sib))
    issues.extend(check_dups(bgs))
    issues.extend(check_props_glbs(scope))
    blockers = [i for i in issues if i.level == "blocker"]
    warns = [i for i in issues if i.level == "warning"]
    if args.json:
        print(json.dumps([i.__dict__ for i in blockers + warns], ensure_ascii=False, indent=1))
        return 1 if blockers else 0
    by_code: dict[str, int] = {}
    for i in blockers:
        by_code[i.code] = by_code.get(i.code, 0) + 1
    print("范围 %s：区 %d · bg %d —— blocker %d · warning %d %s"
          % (rel(scope), len(zones), len(bgs), len(blockers), len(warns),
             ("(" + " ".join(f"{k}={v}" for k, v in sorted(by_code.items())) + ")") if by_code else ""))
    if args.summary:
        return 0
    for i in blockers:
        print("  ❌ [%s] %s: %s" % (i.code, i.where, i.detail))
    for i in warns:
        print("  ⚠ [%s] %s: %s" % (i.code, i.where, i.detail))
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
