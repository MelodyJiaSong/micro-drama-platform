# -*- coding: utf-8 -*-
"""装备卡 / 装备表 / 索引生成器（`ai_video.md` rule 4m；通用引擎，任何剧的 `equipment/` 都走它）。

用法（仓库根目录；参数是剧里任意路径，解析到该剧的 equipment/）：
    python tools/gen_equipment.py build  <路径>        # 闸门 → 按 registry 建 / 搬目录 → 写卡、装备表 md、索引 → 回读
    python tools/gen_equipment.py lint   <路径> --item <暂存 item.toml> --name 名 --slot 槽 --tier 档 --category 类   # 没领号的卡先查
    python tools/gen_equipment.py check  <路径> [--only e5101,e5102]   # 只跑闸门，不写盘；--only 只查这几件（不看装备表）
    python tools/gen_equipment.py images <条目目录或 equipment…> [--force] [--only e5110,e5111] [--shard 0/4] [--only-engine elevenlabs]   # 引擎逐件定（follow-up 027）

出处（rule 4i ①：一样东西只一个出处，这里只拼装不抄写）：
- 名字 / 槽位 / 品质 ← `registry.toml`；形制与 prompt 素材 ← 各条目 `item.toml`；
- 陈列方式、空槽反向声明、品质做工语法 ← `equipment.toml`；
- 渲染串与负向基线 ← `equipment.toml [meta]` 指向的 style_guide 标题下第一个 ```text 围栏；
- 谁在哪一段穿 ← `loadouts/*.toml`（卡上的「谁穿」由它反推）。
卡、`loadouts/*.md`、`equipment_index.md` 都是生成物，手改无效。

prompt 纪律：**世界内专名（物品原名）不进 prompt**，prompt 只用 item.toml 的 `noun`（「一把双手锤」）——
物品名多是 IP 专名（concept C3 黄级）；正面图纯文字自由生成、零参考图，侧 / 背只挂正面图（rule 4e ①）；
出图 prompt 不写「相机 / 摄影机 / 镜头架」（W13）；装备本体不自发光，除非原典模型自带特效（item.toml `effect`）。
出图沿用 props 的做法：正 / 侧 / 背三张、侧背挂正面图；引擎**逐件**由 `Config.engine_for` 定（rule 4l / 4m，follow-up 027）——
武器两类（近战武器 / 法系与远程）蓝档及以上走 ElevenLabs（prompt 上限 EL_PROMPT_MAX），其余一律即梦（1600 字硬限）；
各走各的、失败不退另一家，重跑同一条命令续。`--engine X` 显式点名时整批照它。
"""
from __future__ import annotations

import argparse
import importlib
import time
import io
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import equipment_lib as el  # noqa: E402
from tools import gen_images_xianjian as dm  # noqa: E402  PROMPT_MAX 的唯一出处（即梦服务端硬限）
from tools import image_engine as ie  # noqa: E402  出图引擎枚举的唯一出处（rule 4l）

FENCE = "`" * 3
VIEWS = ("1_正面", "2_侧面", "3_背面")
NEG_OBJ = "人物，手，环境背景，地面，投影，多个物件同框，比例参照物，标尺"
CAMERA_WORDS = ("相机", "摄影机", "镜头架")
# concept C2：游戏截图只进人眼、不进生成模型——prompt 里出现这些来源（多半是把考据图路径抄了进来）直接拦
GAME_IMAGE_SOURCES = ("zamimg", "wowhead", "classicdb", "nfuwow", "twinhead", ".audit", "webthumbs")
# 侧 / 背字段写死绝对方位，往往正好就是正面的朝向，于是派生图成了正面的复制（W21-QA r2 / r4 各踩了十几次）——只许写相对说法
ABSOLUTE_POS = re.compile(r"画面(?:的)?(?:右上|左上|右下|左下|左侧|右侧|左边|右边)")
# 即梦没有负向通道：「无护鼻 / 没有刻纹 / 没有裙甲」会把护鼻、刻纹、裙甲画出来（W21-QA r4）——正面只写有什么
NAMED_ABSENCE = re.compile(r"(?:没有|无)(?:护鼻|刻纹|花纹|纹饰带|裙甲|面甲|羽饰|护颈|第二|尖刺|宝石|文字|刻字|铭文|五官|手臂|手指|把手|臂带)")
# 槽位陈列串进每一张正面 prompt，更严：连「没有衣服 / 人台 / 头」也不许（单卡的「空手套，里面没有手」是 rule 4m ⑦③ 的既定写法，不在此列）
DISPLAY_ABSENCE = re.compile(r"(?:没有|无)(?:[^，。；、\s]{0,2})(?:五官|衣服|人台|头|手臂|手指|手|把手|臂带|护鼻|刻纹|花纹|宝石)")
FRONT_VIEW = "四分之三俯视，单主体居中，完整入画不裁切"
BACKDROP = "纯中性灰无缝背景，无地面、无投影面、无环境元素——本图只锁形制，不建场"
DERIVED_CLOSE = ("纯中性灰无缝背景，无地面、无投影面、无环境元素；均匀柔和的散射光，物体下方没有投影，没有戏剧光；"
                 "保持与参考图相同的轻微俯角，单主体居中、完整入画不裁切；画面里没有任何人物、手、文字、水印。")
NO_GLOW = "本体不发光，没有任何光效"
EL_PROMPT_MAX = 3000        # ElevenLabs 那一路（蓝档及以上武器）的单块上限：没有即梦的 1600 字硬限，留足写细节的余地
ERA = "中世纪手工缝制与手工锻打的制品，没有任何现代工业做法"
# 侧 / 背挂正面图作参考时，即梦爱照搬参考图的构图（W21-QA r1：35 件里十几件侧背是正面的复制）——转角写成硬性要求
TURN = {1: "画面必须和参考图明显不同：物体整体转过 90°，参考图里朝向画面的那一大面在这张里只剩侧棱与厚度，不得照搬参考图的角度与构图。",
        2: "画面必须和参考图明显不同：这是物体的另一面，整件与参考图左右对调，参考图朝左的部分这里朝右，不得照搬参考图的角度与构图。"}


def display(slot: el.Slot, sp: dict) -> str:
    """单侧装备（原典只有一只）不能用槽位的「一对」陈列，否则模型补出另一只。"""
    if sp.get("one_side"):
        return f"只有这一只（{sp['one_side']}侧的），单独摆在灰背景前，下面是空的，没有衣服、没有人台，整张图里就这一只"
    return slot.display


# ─────────────────────────── 出处 ───────────────────────────

def _fence_after(text: str, heading: str, src: Path) -> str:
    i = text.find(heading)
    if i < 0:
        raise SystemExit(f"{src} 里找不到「{heading}」")
    a = text.index(FENCE + "text\n", i) + len(FENCE + "text\n")
    return "".join(text[a:text.index("\n" + FENCE, a)].split("\n"))


class Drama:
    """一部剧的装备库：配置、编号、条目、装备表，外加渲染串 / 负向基线 / 专名闸门。"""

    def __init__(self, anywhere: str) -> None:
        self.root = el.equipment_root(anywhere)
        self.cfg = el.config(self.root)
        m = self.cfg.meta
        sg = (self.root / m["style_guide"]).resolve()
        text = sg.read_text(encoding="utf-8")
        self.style = _fence_after(text, m["style_heading"], sg)
        self.neg_base = _fence_after(text, m["negative_heading"], sg)
        self.gate = importlib.import_module(m["gate"]) if m.get("gate") else None
        self.rows = el.registry(self.root)
        self.loadouts = [el.loadout(self.root, p.stem) for p in el.loadout_paths(self.root)]

    def spec(self, r: el.Row) -> dict:
        return el.item(self.root, r.key)

    def wearers(self, key: str) -> list[str]:
        out = []
        for lo in self.loadouts:
            ids = [s.id for s in lo.stages if key in s.wear]
            if ids:
                out.append(f"{lo.character}：{ids[0]}" + (f"–{ids[-1]}" if len(ids) > 1 else ""))
        return out

    def banned(self, text: str) -> list[str]:
        hits = [w for w in CAMERA_WORDS if w in text]
        if self.gate is not None:
            hits += [w for w in getattr(self.gate, "IP_RED", ()) if w in text]
            if hasattr(self.gate, "yellow_words"):
                hits += [w for w in self.gate.yellow_words() if w in text]
        return hits


# ─────────────────────────── 卡片 ───────────────────────────

def _clean(s: str) -> str:
    return s.replace("**", "").strip()


def light(t: el.Tier, sp: dict, derived: bool = False) -> str:
    """「光:」一行：蓝紫橙＝该件 effect＋本档光芒语法（follow-up 027），灰白绿＝明写不发光。
    侧 / 背不整句照抄 effect：effect 点名的是正面的部位（节缝、宝石、纹章），抄进背面 prompt，
    背面就长出正面的结构、或在没有光源的一面凭空打光（027 验图 e3405 / e3406 / e4805 / e4806）——派生视图只锁光色与强度，部位照参考图。"""
    if not sp.get("effect"):
        return NO_GLOW
    if derived:
        return (f"{t.glow}光的部位、形态与强度都照参考图：这个角度看得到的发光部位照样透出{t.glow}光，"
                f"参考图里只在另一面的发光部位这里不画，没有发光部位的面保持材质原色；光色只有{t.glow}一种")
    return _clean(sp["effect"]) + "；" + t.glow_grammar


def front_prompt(d: Drama, r: el.Row, sp: dict) -> str:
    t, slot = d.cfg.tier(r.tier), d.cfg.slot(r.slot)
    rows = [
        f"{r.key}-1_正面",
        f"主体: {_clean(sp['noun'])}。{_clean(sp['subject'])}",
        f"尺寸: {_clean(sp['size'])}",
        f"做工（只指表面处理与装饰的讲究程度，不改变上面写的形制）: {t.family[sp['family']]}；{t.positive}",
        f"年代: {ERA}",
        f"配色: {_clean(sp['colors'])}",
        f"材质: {_clean(sp['material'])}",
        f"纹饰: {_clean(sp['ornament'])}",
        f"使用痕迹: {_clean(sp['wear'])}",
        f"辨识点: {_clean(sp['tell'])}",
        f"光: {light(t, sp)}",
        f"陈列: {display(slot, sp)}",
        f"视角: {FRONT_VIEW}",
        f"背景: {BACKDROP}",
        f"渲染样式: {d.style}",
        "比例: 1:1",
    ]
    return "\n\n".join(rows)


def derived_prompt(d: Drama, r: el.Row, sp: dict, i: int) -> str:
    view, turn, default = (
        ("2_侧面", "正左侧 90°", "侧面的厚度、弧度与轮廓清楚可见；" + _clean(sp["tell"]) + "在这个角度仍能认出。"),
        ("3_背面", "正背面 180°", "背面的内衬、系带、铆钉与握把一类结构清楚可见，与正面同一套配色与磨损。"),
    )[i - 1]
    body = _clean(sp.get("side" if i == 1 else "back", "") or default)
    return (f"{r.key}-{view}\n与参考图完全是同一{_clean(sp['noun']).lstrip('一')}，只把机位绕物体水平转到{turn}；"
            f"形制、比例、材质、配色、破损位置一律不变。{TURN[i]}\n{body}\n光: {light(d.cfg.tier(r.tier), sp, derived=True)}\n{DERIVED_CLOSE}")


def card(d: Drama, r: el.Row, sp: dict) -> str:
    t = d.cfg.tier(r.tier)
    who = d.wearers(r.key) or ([sp["owner"]] if sp.get("owner") else ["（尚未排进任何装备表）"])
    wow = (f"item {sp['wow_id']} · 需求 {sp.get('req_level', '—')} 级 · 物品等级 {sp.get('item_level', '—')}"
           if sp.get("wow_id") else "剧里原创（原典无此物）" + (f"；对照原典 {sp['analog']}" if sp.get("analog") else ""))
    urls = " · ".join(f"[{i + 1}]({u})" for i, u in enumerate(sp.get("urls", [])))
    facts = "、".join(f"`{f}`" for f in sp.get("facts", [])) or "—"
    moved = f"\n> 迁自物件卡 {'、'.join(r.moved_from)}（follow-up 021：甲胄兵器一律归装备）。" if r.moved_from else ""
    neg = f"{d.neg_base}，\n{NEG_OBJ}，\n{t.negative}，\n{_clean(sp['negative'])}"
    blocks = "、".join(sp.get("blocks", []))
    return f"""# {r.name_zh}{('（' + sp['name_en'] + '）') if sp.get('name_en') else ''} · {r.tier}{('（' + t.label + '）') if t.label else ''}

> **本文件由 `tools/gen_equipment.py` 生成，不要手改。** 内容改同目录 `item.toml`，名字 / 槽位 / 品质改 `../../registry.toml`，再重跑。
> 路由键 `{r.key}-1_正面` / `{r.key}-2_侧面` / `{r.key}-3_背面`（rule 4b-A：**键必须在可粘贴块的首行**）。{moved}

| 项 | 值 |
|---|---|
| 目录 | `{el.item_dir(d.root, r, d.cfg).parent.relative_to(d.root).as_posix()}/`{('（旧键 ' + r.was + '，follow-up 028 改层级码前）') if r.was else ''} |
| 槽位 | {r.slot}{('（同时占' + blocks + '）') if blocks else ''}{('（原典只有一只，在' + sp['one_side'] + '侧）') if sp.get('one_side') else ''} |
| 品质 | {r.tier} —— {t.rule} |
| 类型 | {_clean(sp.get('kind', sp['noun']))} |
| 原典 | {wow} {urls} |
| 来源 | {_clean(sp.get('source', '—'))} |{(chr(10) + '| 原典描述与传说 | ' + _clean(sp['lore']) + ' |') if sp.get('lore') else ''}
| 谁穿 / 哪一段 | {'；'.join(who)} |
| 事实 | {facts} |
| 出图引擎 | {'ElevenLabs' if d.cfg.engine_for(r) == 'elevenlabs' else '即梦 CLI'}（equipment.toml [meta]，follow-up 027） |
| 外观依据 | {sp.get('basis', '—')}（{sp.get('confidence', '—')}） |{chr(10) + '| ⚠ 图的已知偏差 | ' + _clean(sp['known_issue']) + '（出图 3 次后仍在，待人工挑图或手修） |' if sp.get('known_issue') else ''}

## 锁定描述符

| # | 字段 | 值 |
|---|---|---|
| 1 | 尺寸 | {_clean(sp['size'])} |
| 2 | 形制 | {_clean(sp['subject'])} |
| 3 | 配色（自然色名） | {_clean(sp['colors'])} |
| 4 | 材质 | {_clean(sp['material'])} |
| 5 | 纹饰 | {_clean(sp['ornament'])} |
| 6 | 使用痕迹 | {_clean(sp['wear'])}{('。状态变体（不进锚点图）：' + _clean(sp['variants'])) if sp.get('variants') else ''} |
| 7 | 辨识点 | {_clean(sp['tell'])} |
| 8 | 品质做工（只管表面与装饰） | {t.family[sp['family']]} |
| 9 | 光 | {_clean(sp['effect']) if sp.get('effect') else NO_GLOW} |
| 10 | 上身 | {_clean(sp.get('worn', '—'))} |
| 11 | **一句话锁定**（≤30 字 · byte-identical 进 shot `角色:` 行的装备段） | `{sp['lock']}` |

---

# 三视图 prompt — {r.name_zh}

> **正面纯文字自由生成、零参考图**（rule 4e ①）；侧 / 背只挂正面图作参考、钉死同一件东西只换机位
> （`python tools/gen_equipment.py images <本目录>`）。物品原名不进 prompt（C3），只写形制。

{FENCE}text
{front_prompt(d, r, sp)}
{FENCE}

{FENCE}text
{derived_prompt(d, r, sp, 1)}
{FENCE}

{FENCE}text
{derived_prompt(d, r, sp, 2)}
{FENCE}

## 负面词

{FENCE}text
{neg}
{FENCE}
"""


def _blocks(text: str) -> list[str]:
    return re.findall(FENCE + r"text\n(.*?)\n" + FENCE, text, re.S)


def card_errors(d: Drama, r: el.Row, body: str) -> list[str]:
    errs = []
    blocks = _blocks(body)[:3]
    heads = [b.split("\n")[0].strip() for b in blocks]
    if heads != [f"{r.key}-{v}" for v in VIEWS]:
        errs.append(f"{r.key} 三块 prompt 的首行应是 {r.key}-1_正面 / -2_侧面 / -3_背面，实为 {heads}")
    for b in blocks:
        n = len("\n".join(b.split("\n")[1:]).strip())
        if n > (EL_PROMPT_MAX if d.cfg.engine_for(r) == "elevenlabs" else dm.PROMPT_MAX):
            errs.append(f"{b.split(chr(10))[0]} prompt {n} 字 > {d.cfg.engine_for(r)} 上限")
        hit = d.banned(b)
        if hit:
            errs.append(f"{b.split(chr(10))[0]} prompt 含禁词：{'、'.join(sorted(set(hit))[:6])}")
        if r.name_zh in b:
            errs.append(f"{b.split(chr(10))[0]} prompt 里出现了物品原名「{r.name_zh}」（C3：只写形制）")
        leak = [w for w in GAME_IMAGE_SOURCES if w in b.lower()]
        if leak:
            errs.append(f"{b.split(chr(10))[0]} prompt 引到了游戏截图来源：{'、'.join(leak)}（concept C2：图只进人眼）")
        head = b.split(chr(10))[0]
        if head.endswith(("2_侧面", "3_背面")) and ABSOLUTE_POS.search(b):
            errs.append(f"{head} 写死了绝对方位「{ABSOLUTE_POS.search(b).group(0)}」——派生图会照抄正面；改成「与参考图左右对调」一类相对说法")
        if head.endswith("1_正面") and NAMED_ABSENCE.search(b):
            errs.append(f"{head} 点名了不该有的东西「{NAMED_ABSENCE.search(b).group(0)}」——即梦没有负向通道，会照画；改成正面写实际有什么，负向放负面词块")
        if el.HEX.search(b) or "**" in b:
            errs.append(f"{b.split(chr(10))[0]} prompt 含 hex 或 markdown 粗体")
    return errs


# ─────────────────────────── 装备表 / 索引 ───────────────────────────

def loadout_md(d: Drama, lo: el.Loadout) -> str:
    name = {r.key: r for r in d.rows}
    out = [f"# {lo.character} · 装备表", "",
           f"> **由 `{lo.path.name}` 经 `tools/gen_equipment.py` 生成，不要手改。**",
           f"> 便服底层（人物卡 #4）覆盖：{'、'.join(lo.base) or '无'}——{lo.base_note}",
           "> 分镜引擎按集取阶段、一集内按镜分段的按镜号取（`equipment_lib.wearing`）：装备段逐件贴一句话锁定，空槽反向声明原样进 `角色:` 行。", "",
           "| 阶段 | 等级 | 集 | 地点 | 身上 | 空槽反向声明 | 备注 |", "|---|---|---|---|---|---|---|"]
    for st in lo.stages:
        wear = "<br>".join(f"{name[k].slot}：`{k}` {name[k].name_zh}（{name[k].tier}）" for k in st.wear if k in name) or "只有便服"
        lv = f"{st.levels[0]}–{st.levels[1]}" if st.levels else "—"
        eps = '、'.join(st.episodes) or '—'
        if st.shots:
            eps += f" {st.shots[0]}–{st.shots[1]}"
        out.append(f"| {st.id} | {lv} | {eps} | {st.where} | {wear} | "
                   f"{el.empty_clause(d.root, lo, st) or '—'} | {st.note} |")
    return "\n".join(out) + "\n"


def index_md(d: Drama) -> str:
    out = ["# 装备索引", "", "> **由 `tools/gen_equipment.py` 生成，不要手改。** 编号出处 `registry.toml`，规则见 `ai_video.md` rule 4m。", ""]
    tiers = [t.name for t in d.cfg.tiers]
    groups = [(c.name, c.classes) for c in d.cfg.categories] or [("", "")]
    need = int(d.cfg.meta.get("min_per_tier", 0))
    capped = {t.name for t in d.cfg.tiers if t.rank == max(x.rank for x in d.cfg.tiers)}   # 最高档（橙）不设配额
    if d.cfg.categories:
        out += ["## 分类 × 品质" + (f"（每类每档目标 ≥{need}，不足的标 ▲缺口；{'、'.join(capped)}装不设配额）" if need else ""), "",
                "| 分类 | 谁用 | " + " | ".join(tiers) + " | 合计 |", "|---|---|" + "---|" * (len(tiers) + 1)]
        for name, cls in groups:
            n = [sum(1 for r in d.rows if r.category == name and r.tier == t) for t in tiers]
            cells = [f"{x} ▲{need - x}" if need and t not in capped and x < need else str(x or "") for x, t in zip(n, tiers)]
            out.append(f"| {name} | {cls} | " + " | ".join(cells) + f" | {sum(n)} |")
    out.append(f"| **合计** | | " + " | ".join(str(sum(1 for r in d.rows if r.tier == t) or "") for t in tiers) + f" | {len(d.rows)} |")
    # 号码怎么读（follow-up 028）：键的每一段就是一层目录，从左往右读就能一层层走到件
    nn = "N" * d.cfg.digits[-1]
    out += ["", "## 号码怎么读", "", f"键 ＝ 目录号拼起来：`e5103` → `5_近战武器/` → `51_主手/` → 第 03 件；同一槽内按品质灰→橙排号。", "",
            "| 目录 | 槽位目录（键段） |", "|---|---|"]
    for name, _ in groups:
        slots = d.cfg.category(name).slots if name else tuple(s.name for s in d.cfg.slots)
        out.append(f"| `{d.cfg.cat_dir(name) if name else '（根）'}` | "
                   + " · ".join(f"`{d.cfg.slot_dir(name, s)}` e{d.cfg.prefix(name, s)}{nn}" for s in slots) + " |")
    for name, cls in groups:
        in_cat = [r for r in d.rows if r.category == name]
        if name:
            out += ["", f"## {d.cfg.cat_dir(name)}（{cls}）"]
        for s in d.cfg.slots:
            rows = [r for r in in_cat if r.slot == s.name]
            if not rows:
                continue
            out += ["", f"### {d.cfg.slot_dir(name, s.name)}", "",
                    "| 键 | 品质 | 名称 | 原典 | 需求 | 谁穿 / 哪一段 | 图 |", "|---|---|---|---|---|---|---|"]
            for r in sorted(rows, key=lambda r: (d.cfg.tier(r.tier).rank, r.n)):
                sp = d.spec(r)
                dirp = el.find(d.root, r.key)
                imgs = sum(1 for v in VIEWS if dirp and (dirp / f"{r.key}-{v}.png").is_file())
                who = "；".join(d.wearers(r.key)) or sp.get("owner", "—")
                rel = el.item_dir(d.root, r, d.cfg).relative_to(d.root).as_posix()
                out.append(f"| `{r.key}` | {r.tier} | [{r.name_zh}]({rel}/{r.dir_name}.md) {sp.get('name_en', '')} | "
                           f"{sp.get('wow_id') or '原创'} | {sp.get('req_level', '—')} | {who} | {imgs}/3{' ⚠' if sp.get('known_issue') else ''} |")
    return chr(10).join(out) + chr(10)


# ─────────────────────────── 命令 ───────────────────────────

def place(d: Drama) -> None:
    """按 registry 建 / 搬目录：registry 是目录名的唯一出处（改档 / 改名 / 换槽位 → 这里搬）。"""
    for r in d.rows:
        want = el.item_dir(d.root, r, d.cfg)
        have = el.find(d.root, r.key)
        if have is None:
            want.mkdir(parents=True, exist_ok=True)
        elif have != want:
            want.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(have), str(want))
            stale = want / f"{have.name}.md"
            if stale.is_file():
                stale.unlink()
            print(f"  ↪ {have.relative_to(d.root)} → {want.relative_to(d.root)}")


def gates(d: Drama) -> list[str]:
    errs = el.check(d.root)
    if errs:
        return errs
    # 槽位陈列串逐字进每一张正面 prompt，点名的缺席物同样会被画出来（029 验图：「头模没有五官」长出鼻嘴、
    # 「没有手臂」长出木手、「没有手指」把露指手套画成五指）——配置里也只许写有什么
    for s in d.cfg.slots:
        hit = DISPLAY_ABSENCE.search(s.display)
        if hit:
            errs.append(f"equipment.toml 槽位「{s.name}」的 display 点名了「{hit.group(0)}」——即梦没有负向通道，只写实际有什么")
    # 做工串同理（029 验图：白档盾「铆钉规整，没有纹章」让素面钢盾满边长铆钉）：品质档的 positive 与各材质族串也逐字进正面
    for t in d.cfg.tiers:
        for label, text in [("positive", t.positive)] + [(f"family.{k}", v) for k, v in t.family.items()]:
            hit = DISPLAY_ABSENCE.search(text) or re.search(r"没有纹章|无纹章", text)
            if hit:
                errs.append(f"equipment.toml 品质「{t.name}」的 {label} 点名了「{hit.group(0)}」——做工串只写新旧与光洁，不点名缺席物")
    for r in d.rows:
        errs += card_errors(d, r, card(d, r, d.spec(r)))
    return errs


def lint(anywhere: str, toml_path: str, name: str, slot: str, tier: str, category: str) -> int:
    """暂存区里还没领号的 item.toml：按将来的名字 / 槽位 / 品质 / 分类拼出卡，跑条目契约与 prompt 闸门。"""
    import tomllib
    d = Drama(anywhere)
    r = el.Row("e0", name, slot, tier, (), category)
    spec = tomllib.loads(Path(toml_path).read_text(encoding="utf-8"))
    errs = el.check_spec(d.cfg, r, spec)
    if not errs:
        errs = card_errors(d, r, card(d, r, spec))
    for e in errs:
        print("  ❌", e)
    print(f"{toml_path}：" + ("过" if not errs else f"{len(errs)} 个 blocker"))
    return 1 if errs else 0


def check_only(anywhere: str, keys: set[str]) -> int:
    """只查这几件（item.toml 契约 + 拼出来的卡 prompt），不看装备表——并行写卡时各查各的。"""
    d = Drama(anywhere)
    errs: list[str] = []
    for r in d.rows:
        if r.key not in keys:
            continue
        item_errs = el.check_item(d.root, r, d.cfg)
        errs += item_errs or card_errors(d, r, card(d, r, d.spec(r)))
    for e in errs:
        print("  ❌", e)
    print(f"{'、'.join(sorted(keys, key=lambda k: int(k[1:])))}：" + ("过" if not errs else f"{len(errs)} 个 blocker"))
    return 1 if errs else 0


def build(anywhere: str, write: bool) -> int:
    d = Drama(anywhere)
    if write:
        place(d)
    errs = gates(d)
    for e in errs:
        print("  ❌", e)
    if errs:
        print(f"闸门：{len(errs)} 个 blocker，未写盘")
        return 1
    if not write:
        print(f"闸门过：{len(d.rows)} 件装备 · {len(d.loadouts)} 张装备表")
        return 0
    for r in d.rows:
        dirp = el.item_dir(d.root, r)
        body = card(d, r, d.spec(r))
        io.open(dirp / f"{r.dir_name}.md", "w", encoding="utf-8", newline="\n").write(body)
        back = (dirp / f"{r.dir_name}.md").read_text(encoding="utf-8")
        again = card_errors(d, r, back)
        if again:
            raise SystemExit(f"回读不过：{again}")
    for lo in d.loadouts:
        io.open(lo.path.with_suffix(".md"), "w", encoding="utf-8", newline="\n").write(loadout_md(d, lo))
    io.open(d.root / "equipment_index.md", "w", encoding="utf-8", newline="\n").write(index_md(d))
    by = {}
    for r in d.rows:
        by[r.tier] = by.get(r.tier, 0) + 1
    print(f"写出 {len(d.rows)} 张装备卡（" + " · ".join(f"{t.name} {by.get(t.name, 0)}" for t in d.cfg.tiers)
          + f"）+ {len(d.loadouts)} 张装备表 + equipment_index.md → {d.root}")
    return 0


# 三视图设定图（029 试验）：侧 / 背挂正面图作参考时，即梦照抄参考图构图（验图里一半以上的毛病）；
# 一张横幅里并排画正 / 侧 / 背，模型同时画三个角度，侧面才真的转过去，三格也天然是同一件。
# 试验三件里腰带、护肩有效、镐无效；但实战 18 件护甲第 3 次只过 1 件（成对装备只画一只——当时漏了陈列行，已补；
# 裁图偶尔带进分隔线；背面仍有照抄）——不是默认路线，只作参考图路线的备选。
SHEET_KEEP = ("主体", "尺寸", "配色", "材质", "纹饰", "使用痕迹", "辨识点", "光", "陈列", "渲染样式")
SHEET_HEAD = ("同一件物品的三视图设定图，横幅画面从左到右并排三个等大的区域，三个区域之间各有一条细细的竖直分隔线，"
              "三个区域里是同一件东西、同样的大小比例、配色、磨损与细节，成对的装备（靴、手套、护腕、护肩）每个区域都画完整的一对：\n"
              "左边是正面，四分之三俯视；中间是整件绕竖直轴转过 90° 的正侧面，只看到它的侧棱与厚度；"
              "右边是整件转过 180° 的背面，看到另一面的结构。三个视角的物件底边对齐、大小一致，彼此之间留出宽宽的灰色空隙；"
              "纯中性灰无缝背景，均匀柔和的散射光，物体下方没有投影；画面里只有这件物品的三个视角。")


def sheet_prompt(d: Drama, r: el.Row, sp: dict) -> str:
    rows = [x for x in front_prompt(d, r, sp).split("\n\n")[1:] if re.split(r"[:（]", x, 1)[0] in SHEET_KEEP]
    return SHEET_HEAD + "\n" + "\n".join(rows)


def split_sheet(sheet: Path, outs: list[Path]) -> None:
    """横幅设定图 → 三张方图：找两条竖分隔线（找不到按三等分），每格按背景色裁出物体、补成正方形。"""
    import numpy as np
    from PIL import Image
    im = Image.open(sheet).convert("RGB")
    a = np.asarray(im).astype(float)
    g = a.mean(axis=2)
    h, w = g.shape
    col, sd = g.mean(axis=0), g.std(axis=0)
    jump = np.zeros(w)
    jump[8:-8] = np.abs(col[8:-8] - (col[:-16] + col[16:]) / 2)
    jump[sd > 8] = 0
    cuts = []
    for lo, hi, dflt in ((0.2, 0.45, w / 3), (0.55, 0.8, 2 * w / 3)):
        s, e = int(lo * w), int(hi * w)
        c = s + int(np.argmax(jump[s:e]))
        cuts.append(c if jump[c] > 3 else int(dflt))
    edges = [0, *cuts, w]
    for i, out in enumerate(outs):
        x0, x1 = edges[i] + (50 if i else 0), edges[i + 1] - (50 if i < 2 else 0)   # 分隔带常有几十像素宽、带渐变
        p = a[:, x0:x1]
        mid = slice(p.shape[1] // 5, p.shape[1] * 4 // 5)          # 背景色取中段上下沿：两侧可能压着分隔带
        bg = np.median(np.concatenate([p[:12, mid].reshape(-1, 3), p[-12:, mid].reshape(-1, 3)]), axis=0)
        flat = p.mean(axis=2).std(axis=0) < 5                        # 整列一色的竖条＝分隔带或空背景，不是物体
        p = p.copy()
        p[:, flat & (np.abs(p.mean(axis=2).mean(axis=0) - bg.mean()) > 8)] = bg   # 分隔带涂成背景，免得裁进边上
        mask = np.abs(p - bg).max(axis=2) > 22
        mask[:, flat] = False
        ys, xs = np.nonzero(mask)
        if len(xs) == 0:
            raise RuntimeError(f"{sheet.name} 第 {i + 1} 格里找不到物体")
        pad = int(0.06 * max(ys.max() - ys.min(), xs.max() - xs.min()))
        box = (max(0, xs.min() - pad), max(0, ys.min() - pad), min(p.shape[1], xs.max() + pad), min(h, ys.max() + pad))
        crop = Image.fromarray(p.astype("uint8")).crop(box)
        side = max(crop.size)
        sq = Image.new("RGB", (side, side), tuple(int(v) for v in bg))
        sq.paste(crop, ((side - crop.size[0]) // 2, (side - crop.size[1]) // 2))
        sq.save(out)


def do_sheet(a, force: bool) -> None:
    """缺任何一张视图（或 --force）就出一张设定图、裁成三张，三张一起换——侧背与正面出自同一次生成，才是同一件。"""
    from tools import gen_bg_assets as ba
    views = [a.dir / f"{a.key}-{v}.png" for v in VIEWS]
    if all(v.is_file() for v in views) and not force:
        return
    prompt = sheet_prompt(a.drama, a.row, a.drama.spec(a.row))
    if len(prompt) > dm.PROMPT_MAX:
        raise RuntimeError(f"{a.key} 设定图 prompt {len(prompt)} 字 > 即梦 {dm.PROMPT_MAX}")
    t0 = time.time()
    url, cost = ba._dm_submit(prompt, [], ratio="21:9", wait_s=900)
    sheet = a.dir / f"{a.key}-0_三视图.png"
    dm.download(url, sheet)
    split_sheet(sheet, views)
    a.log(dreamina_sheet=cost)
    print(f"  ✓ {sheet.name} → 三张  {time.time() - t0:.0f}s", flush=True)


def images(paths: list[str], engine: str, force: bool, only: set[str], shard: tuple[int, int] = (0, 1), passes: int = 5,
           only_engine: str = "", sheet: bool = False) -> int:
    from tools import gen_bg_assets as ba   # 出图的唯一实现（即梦 / ElevenLabs、重试、日志）；这里只换「资产在哪」

    class Item(ba.Asset):
        def __init__(self, dirp: Path, key: str) -> None:   # noqa: D401 — 不读 asset.toml
            self.dir, self.key, self.spec = dirp, key, {}
            self.card = dirp / f"{dirp.name}.md"
            self.log_p = dirp / "gen_log.json"
            self.engine = ""
            self.row: el.Row | None = None
            self.drama: Drama | None = None

    todo: list[Item] = []
    for p in paths:
        root = el.equipment_root(p)
        cfg = el.config(root)
        drama = Drama(p) if sheet else None
        for r in el.registry(root):
            dirp = el.find(root, r.key)
            if dirp is None or (only and r.key not in only):
                continue
            eng = engine or cfg.engine_for(r)
            if only_engine and eng != only_engine:
                continue
            if Path(p).resolve() in (root, dirp, dirp.parent):
                it = Item(dirp, r.key)
                it.engine, it.row, it.drama = eng, r, drama
                todo.append(it)
    k, n = shard
    todo = [a for i, a in enumerate(sorted(todo, key=lambda a: int(a.key[1:]))) if i % n == k]
    # 一件失败（即梦 502 / 上传超时）只记下、接着出下一件；整轮出完隔一会儿再补跑失败的，已落盘的视图自动跳过
    for n_pass in range(passes):
        failed = []
        for a in todo:
            print(f"· {a.key} {a.dir.name}  [{a.engine}]", flush=True)
            try:
                if sheet and a.engine == ie.DREAMINA:
                    do_sheet(a, force if n_pass == 0 else False)
                else:
                    ba.do_images(a, a.engine, force if n_pass == 0 else False)
            except Exception as e:     # noqa: BLE001 — 服务端错误不该拖垮整个分片
                print(f"  ✗ {a.key}：{str(e)[:200]}", flush=True)
                failed.append(a)
        if not failed:
            return 0
        todo = failed
        print(f"— 第 {n_pass + 1} 轮后 {len(failed)} 件失败：{'、'.join(a.key for a in failed)}；90 秒后补跑", flush=True)
        time.sleep(90)
    return 1


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("build", "check", "images", "lint"))
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--engine", default="", choices=("",) + ie.CHOICES,
                    help="默认逐件定（follow-up 027 / 029：武器蓝档及以上 ElevenLabs、其余即梦）；显式点名则整批照它")
    ap.add_argument("--only-engine", default="", choices=("", ie.DREAMINA, ie.ELEVENLABS),
                    help="只出逐件判定为这一家的条目（两家分开并发时用）")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default="", help="只出这些键，逗号分隔")
    ap.add_argument("--shard", default="0/1", help="k/n：只做第 k 份（共 n 份），多进程并发时各拿不相交的一份")
    ap.add_argument("--passes", type=int, default=5, help="失败件最多补跑几轮")
    ap.add_argument("--sheet", action="store_true",
                    help="即梦件改走三视图设定图：一张横幅并排正 / 侧 / 背，裁成三张、三张一起换（029：护甲有效，扁长武器无效）")
    ap.add_argument("--item", default="", help="lint：暂存区 item.toml 路径")
    ap.add_argument("--name", default="")
    ap.add_argument("--slot", default="")
    ap.add_argument("--tier", default="")
    ap.add_argument("--category", default="")
    a = ap.parse_args()
    if a.step == "images":
        k, n = (int(x) for x in a.shard.split("/"))
        return images(a.paths, a.engine, a.force, {k for k in a.only.split(",") if k}, (k, n), a.passes, a.only_engine, a.sheet)
    if a.step == "lint":
        return lint(a.paths[0], a.item, a.name, a.slot, a.tier, a.category)
    only = {k for k in a.only.split(",") if k}
    if a.step == "check" and only:
        return max(check_only(p, only) for p in a.paths)
    return max(build(p, a.step == "build") for p in a.paths)


if __name__ == "__main__":
    raise SystemExit(main())
