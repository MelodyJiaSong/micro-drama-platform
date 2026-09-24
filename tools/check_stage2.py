# -*- coding: utf-8 -*-
"""阶段 2 世界观人设的契约闸门（`ai_videos__格式契约` K7/K8/K9/K25 + rule 12.11 的可执行版）。

契约出处：`.claude/skills/ai_videos__全流程编排/playbooks/ai_videos__stage2_世界观人设.md` §5 ·
`.claude/agent_refs/project/ai_video.md` rule 1b / 12.1 / 12.9 / 12.11。

检查项
------
K9   零 hex —— 颜色一律自然中文色名；`#RRGGBB` 对生成模型不可解析、只是噪声
K8   角色识别标签 ≤30 字且存在 —— 它要被每个 shot **整段粘贴**，长了就撑爆 prompt
12.9 目录名 ＝ 内层 md 名 —— 否则 webapp 的树与导入器都找不到它
12.11 人物灵魂 12 维无留空 —— 写不出的要显式标 `待深化`，不得整行空白
K7   voice_id 存在且与 `casting.md` 一致
G1   零玩家概念（concept G1 推翻 divergence #9，不再有 `[玩家]` / `[NPC]` 之分）—— 本剧所有人都是世界里的人，
      「标志小动作」正面写了玩家三件套（无理由连跳 / 绕圈跑 / 挂机静止）或正文出现 `[玩家]` / `[NPC]` 标记即 blocker：
      那是把人演成游戏角色的出戏残留（**排除显式否定句**：「绝不做连跳」是做对了，不是违规）
G8   voice_id 以 `en-` 开头（卡片与 `casting.md`）—— 本剧面向英语观众、全员英文配音，残留的中文音色 id 会配出错的片
本剧  立绘 prompt 存在且首行路由键 ＝ 目录名（rule 4b-A：键不在首位，出的图就永远落不进这个文件夹）

用法：
    python tools/check_stage2.py ai_videos/shengji_zhilu
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
from dataclasses import dataclass

HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
# 每一维给一组同义写法——playbook 模板用的是「此刻怎么 make decision」（中英混排），
# 只认「决策」会把写对了的卡判成缺维度。**一个会误报的闸门比没有闸门更糟。**
SOUL_KEYS: tuple[tuple[str, ...], ...] = (
    ("年龄",), ("前史",), ("根因", "为什么在做"), ("目标",), ("需求", "needs"),
    ("欲望", "desire"), ("矛盾",), ("恐惧", "fear"), ("创伤", "wound"),
    ("决策", "decision"), ("性格",), ("成长", "变化轨迹"),
)
# G1：玩家三件套（① 无理由连跳 ② 绕圈跑 ③ 突然完全静止＝挂机，可选 ④ 战斗一结束蹲下翻尸体）。
# 「无理由…跳」单列——「无理由地连续原地起跳」里没有「连跳」两个字。
TRIO = re.compile(r"三件套|连跳|无理由[^，,。；;]{0,10}跳|绕圈|完全静止|翻尸体|蹲下翻")
# 否定词须在**同一句、命中之前**：「绝不做三件套——不做连跳」是否定，
# 「连跳两下（…铁律 I-7）」不是。旧版把「铁律」算否定词、且整行任何位置有否定就放行，
# 于是玩家卡只要句尾挂一句「铁律」就逃过了闸门。
_NEG = re.compile(r"不得|没有|禁止|严禁|不许|绝不|决不|从不|不会|不该|不出现|不做")
# 撤回词在同一句任何位置都算：「`[玩家]` 标记已作废」的否定落在命中之后。
_RETRACT = re.compile(r"作废|废除|取消|推翻|不再|删去|删掉|删除|去掉")
_SENT = re.compile(r"<br\s*/?>|[。；;！!？?\n]")
_PLAYER_TAG = re.compile(r"\[(?:玩家|NPC)\]")
# 按**标签**找锁定串，不按行号——具名角色卡是 8 字段表（#8 角色识别标签），
# 非人形图鉴是裁到 6 字段的精简表（#6 一句话锁定）。按行号找会把图鉴全判成缺失。
_LOCK_ROW = re.compile(r"^\|[^|]*\|[^|]*(?:角色识别标签|一句话锁定)[^|]*\|(.+?)\|\s*$", re.M)
_BACKTICK = re.compile(r"`([^`]+)`")
_PAREN = re.compile(r"[（(][^）)]*[）)]")
_DIM_HEAD = re.compile(r"^\s*-\s*\*\*[^*]+\*\*\s*[:：]\s*$")
# voice_id 必须与「voice_id」同行、且形如 en-m-szzl-name-01
_VOICE_ID = re.compile(r"voice_id[^`\n]{0,40}`([a-z0-9][a-z0-9_\-]{4,})`")
_VOICE_SHAPE = re.compile(r"`([a-z]{2}-[mfx]-[a-z0-9]+-[a-z0-9]+-\d{2})`")
# G8 扫的是**任何位置**的音色 id，不要求反引号——卡里有 `voice_id: zh-…` 整段包进一对反引号的写法，
# 按 _VOICE_ID 抓不到；turntable 表里「用 voice_id `zh-…` 的声线演绎」这类残留也要一并抓出来。
_VOICE_ANY = re.compile(r"(?<![a-z0-9-])([a-z]{2}-[mfx]-([a-z0-9]+)-[a-z0-9]+-\d{2})(?![a-z0-9-])")
# 残留扫描只认本剧域的 id：说明文字里引用外部声线表（`zh-m-wow-veteran-01`「不套用它」）不是本剧的声明。
# 本剧域以外的 id 若真被当成声明，会因「没有 en- id」被下面另一条拦住。
VOICE_DOMAIN = "szzl"
# 同行已有 en- id、或写明「作废 / 改为」的是迁移说明，不是声明
_VOICE_MIGRATE = re.compile(r"作废|废弃|弃用|改为|改成|替换|→|->")


@dataclass(frozen=True)
class Issue:
    card: str
    level: str
    code: str
    detail: str


def _lock_string(text: str) -> str | None:
    m = _LOCK_ROW.search(text)
    if not m:
        return None
    cell = m.group(1).strip()
    bt = _BACKTICK.findall(cell)
    raw = bt[0] if bt else _PAREN.sub("", cell)
    # `**` 是 markdown 强调记号、不是内容。不剥掉会把 30 字的串算成 34 字。
    return raw.replace("**", "").strip()


def _empty_dims(soul: str) -> list[str]:
    """只有「标题行后面紧跟的不是缩进子项」才算空维度——模板允许把内容写成嵌套子弹。"""
    lines = soul.split("\n")
    out: list[str] = []
    for i, ln in enumerate(lines):
        if not _DIM_HEAD.match(ln):
            continue
        nxt = next((x for x in lines[i + 1:] if x.strip()), "")
        if not nxt.startswith((" ", "\t")):
            out.append(ln.strip())
    return out


def _positive_hits(text: str, pat: re.Pattern[str]) -> list[str]:
    """`pat` 在**非否定语境**下命中的句子（每句至多记一次）。"""
    out: list[str] = []
    for sent in _SENT.split(text):
        if _RETRACT.search(sent):
            continue
        for m in pat.finditer(sent):
            if not _NEG.search(sent, 0, m.start()):
                out.append(sent.strip())
                break
    return out


def _check_g1(name: str, text: str) -> list[Issue]:
    out: list[Issue] = []
    act = _positive_hits(_row(text, "标志小动作"), TRIO)
    if act:
        out.append(Issue(name, "blocker", "G1",
                         "「标志小动作」正面写了玩家三件套——本剧没有玩家，这是出戏残留：%s" % act[0][:70]))
    tags = _positive_hits(text, _PLAYER_TAG)
    if tags:
        out.append(Issue(name, "blocker", "G1",
                         "正文 %d 处出现 `[玩家]` / `[NPC]` 标记（divergence #9 已作废），首处：%s" % (len(tags), tags[0][:60])))
    return out


def _stale_voice_ids(text: str) -> list[str]:
    """本剧域内不以 `en-` 开头、又不在迁移说明行里的音色 id（去重、保序）。"""
    out: list[str] = []
    for ln in text.split("\n"):
        ids = [i for i, dom in _VOICE_ANY.findall(ln) if dom == VOICE_DOMAIN]
        if not ids or any(i.startswith("en-") for i in ids) or _VOICE_MIGRATE.search(ln):
            continue
        out.extend(i for i in ids if not i.startswith("en-") and i not in out)
    return out


def _check_g8(name: str, text: str, is_mob: bool) -> list[Issue]:
    stale = _stale_voice_ids(text)
    if stale:
        return [Issue(name, "blocker", "G8",
                      "残留非英文 voice_id（本剧全员英文配音，须改 `en-…`）：%s" % "、".join(stale))]
    if not is_mob and "voice_id" in text and not any(
            i.startswith("en-") for i, _dom in _VOICE_ANY.findall(text)):
        return [Issue(name, "blocker", "G8", "没有声明 `en-` 开头的 voice_id")]
    return []


def _section(text: str, head: str) -> str:
    m = re.search(r"\n##+ *" + head + r"[^\n]*\n(.*?)(?=\n##+ |\Z)", text, re.S)
    return m.group(1) if m else ""


def _row(text: str, label: str) -> str:
    m = re.search(r"^\|[^|]*\|[^|]*" + label + r"[^|]*\|(.+?)\|\s*$", text, re.M)
    return m.group(1) if m else ""


# **只认真正的负向词声明行**：行首（可带 markdown 装饰）是「负向 / 负面词 / 译名负向」+ 冒号。
# 初版只要行里出现「负向」两个字就查，于是把「负向明列『穿衣服的两栖人』」这种正文说明
# 也判成违规——**会误报的闸门比没有闸门更糟**，这一课在本文件里已经交了三次学费。
_NEG_DECL = re.compile(r"^[\s>\*\-|]*\**\s*(?:译名负向|负向词?|负面词)\s*(?:（[^）]*）)?\s*[：:](.+)$")


def _check_self_negative(name: str, text: str) -> list[Issue]:
    """**卡片自己的正名绝不能出现在它的负向词里。**

    踩过的坑（2026-09-20）：对一批既要写正名、又要写错名的文件跑了一次**盲的全文替换**
    （麦克布莱德 → 玛克布莱德），把「错名」那一侧也换掉了，于是 c7 卡的译名负向行变成
    `治安官玛克布莱德，中士，…`——**等于在告诉下游把正确的名字挂进每个 shot 的负面词**。
    这种错不会报错，只会让每一张图都在被要求「不要画这个人」。
    """
    m = re.match(r"^#\s+([^\s·`]+)", text)
    if not m:
        return []
    canon = m.group(1).strip()
    if len(canon) < 2:
        return []
    out: list[Issue] = []
    for ln in text.split("\n"):
        m2 = _NEG_DECL.match(ln)
        if m2 and canon in m2.group(1):
            out.append(Issue(name, "blocker", "自负向",
                             "本卡的正名「%s」被列进了负向词——下游会把它挂进每个 shot 的负面词：%s"
                             % (canon, m2.group(1).strip()[:70])))
    return out


def check_card(path: str, is_mob: bool) -> list[Issue]:
    name = os.path.basename(os.path.dirname(path))
    text = io.open(path, encoding="utf-8").read()
    out: list[Issue] = []

    if os.path.basename(path)[:-3] != name:
        out.append(Issue(name, "blocker", "12.9", "目录名 ≠ 内层 md 名：%s" % os.path.basename(path)))

    for h in set(HEX.findall(text)):
        out.append(Issue(name, "blocker", "K9", "出现 hex 色值 %s —— 颜色须用自然中文色名" % h))

    lock = _lock_string(text)
    if not lock:
        out.append(Issue(name, "blocker", "K8", "锁定描述符第 8 行（角色识别标签 / 一句话锁定）缺失"))
    elif len(lock) > 30:
        out.append(Issue(name, "blocker", "K8", "锁定串 %d 字 > 30：%s" % (len(lock), lock[:40])))

    if "Seedream 立绘 prompt" not in text:
        out.append(Issue(name, "blocker", "4b-A", "缺 Seedream 立绘 prompt 段（本剧的脸由它承载）"))
    else:
        fences = re.findall(r"```(?:text)?\n(.*?)\n```", text, re.S)
        heads = [f.split("\n")[0].strip() for f in fences]
        if not any(h.startswith(name) for h in heads):
            out.append(Issue(name, "warning", "4b-A",
                             "没有任何可粘贴块以路由键 `%s` 开头——出的图会落不进本目录。首行实为：%s"
                             % (name, " / ".join(h[:26] for h in heads[:3]) or "（无围栏）")))

    if not is_mob:
        soul = _section(text, "人物灵魂")
        if not soul.strip():
            out.append(Issue(name, "blocker", "12.11", "缺 `## 人物灵魂` 段"))
        else:
            miss = [alts[0] for alts in SOUL_KEYS if not any(a in soul for a in alts)]
            if miss:
                out.append(Issue(name, "blocker", "12.11", "人物灵魂缺维度：%s" % "、".join(miss)))
            for ln in _empty_dims(soul):
                out.append(Issue(name, "blocker", "12.11", "人物灵魂有空维度（写不出须标 `待深化`）：%s" % ln))

        if "voice_id" not in text:
            out.append(Issue(name, "blocker", "K7", "缺 voice_id"))
        if "turntable" not in text:
            out.append(Issue(name, "warning", "12.5", "缺 turntable 建立视频块"))

    out.extend(_check_self_negative(name, text))
    out.extend(_check_g1(name, text))
    out.extend(_check_g8(name, text, is_mob))
    return out



# ── 场景档（rule 12.3 v3 + 4b-A 路由键 + 2026-06-21「当场建·禁待建」）─────────
SCENE_SECTIONS: tuple[tuple[str, str], ...] = (
    ("场景定位", "## 场景定位"),
    ("锁定描述符", "## 锁定描述符"),
    ("关键变化态", "## 关键变化态"),
    ("出现镜头", "## 出现镜头"),
    ("步骤一底图", "步骤一"),
    ("步骤二 walk-through", "步骤二"),
    ("背景图系统 index", "背景图系统"),
)
_PLATE_NAME = re.compile(r"^(bg\d+)-(\d+)_([^_]+)_(.+)$")
_BG_DIR = re.compile(r"^bg\d+_")
_SKIP_DIRS = frozenset({"_deleted", "renders", "previz", "frames", "__pycache__"})
# 「档级：锚点级」写在卡片抬头的引用块里（gen_world_scenes_szzl.py 的骨架就是这么写的）
_ANCHOR_LEVEL = re.compile(r"档级[:：]\s*\**锚点级")
# 只在**没有否定/引用语境**时才算违规——卡片正文常引用规则本身
# （「五个 plate 已全部当场建好（rule 12.3 …禁用「待建」）」），
# 把引用判成违规是上一版检查器反复犯的同一类错。**会误报的闸门比没有闸门更糟。**
_TODO = re.compile(r"待建|TODO|TBD")
_TODO_CITE = re.compile(r"(禁|不得|不可|已全部|已当场|已建|amendment|rule|规则|铁律)")


def _has_todo(text: str) -> bool:
    return any(_TODO.search(ln) and not _TODO_CITE.search(ln) for ln in text.split("\n"))


def check_scene(path: str, used_tokens: dict[str, str]) -> list[Issue]:
    """一个场景主体目录。`used_tokens` 累积全剧已用的方位 token，用于查子串撞车。"""
    name = os.path.basename(os.path.dirname(path))
    text = io.open(path, encoding="utf-8").read()
    out: list[Issue] = []

    if os.path.basename(path)[:-3] != name:
        out.append(Issue(name, "blocker", "12.9", "目录名 ≠ 主体 md 名"))

    for h in set(HEX.findall(text)):
        out.append(Issue(name, "blocker", "K9", "出现 hex 色值 %s" % h))

    # 锚点级档（stage2 playbook §3b ④ / rule 4f：必做只有锚点，plate 用到才建）：
    # 没有 walk-through 与五张 plate，只查锚点 prompt 那几节。
    anchor_only = _ANCHOR_LEVEL.search(text) is not None
    for label, marker in SCENE_SECTIONS:
        if anchor_only and label == "步骤二 walk-through":
            continue
        if marker not in text:
            out.append(Issue(name, "blocker", "12.3", "缺 v3 模板的「%s」节" % label))

    lock = _lock_string(text)
    if not lock:
        out.append(Issue(name, "blocker", "K8", "锁定描述符缺「一句话锁定」行"))
    elif len(lock) > 30:
        out.append(Issue(name, "blocker", "K8", "一句话锁定 %d 字 > 30：%s" % (len(lock), lock[:40])))

    if _has_todo(text):
        out.append(Issue(name, "blocker", "12.3", "主体 md 里出现「待建 / TODO」——plate 的 prompt 不可推迟（2026-06-21 amendment）"))

    # index 行 ↔ plate 目录 ↔ 首行 handle 三方一致（K23）
    root = os.path.dirname(path)
    # `planning/`（floor plan 的产物）不是 plate —— 它是 3D 链条的目录，不参与 K23 三方一致
    NOT_PLATE = {"planning", "_blender", "ref", "renders"}
    plates = sorted(d for d in os.listdir(root)
                    if os.path.isdir(os.path.join(root, d)) and d not in NOT_PLATE)
    if anchor_only:
        if plates:
            out.append(Issue(name, "warning", "K23", "锚点级档却有 %d 个 plate 目录——要么升成 v3 五 plate 档，要么删掉" % len(plates)))
        plates = []
    elif len(plates) != 5:
        out.append(Issue(name, "blocker", "K23", "plate 目录 %d 个，应为 5 个" % len(plates)))
    for pl in plates:
        md = os.path.join(root, pl, pl + ".md")
        if not os.path.exists(md):
            out.append(Issue(name, "blocker", "K23", "plate 目录 %s 里没有同名 md" % pl))
            continue
        body = io.open(md, encoding="utf-8").read()
        if _has_todo(body):
            out.append(Issue(name, "blocker", "12.3", "%s 里出现「待建」" % pl))
        heads = [f.split("\n")[0].strip() for f in re.findall(r"```(?:text)?\n(.*?)\n```", body, re.S)]
        if not any(h.startswith(pl) for h in heads):
            out.append(Issue(name, "blocker", "4b-A",
                             "%s 没有以路由键开头的可粘贴块——出的图会落不进本目录" % pl))
        if pl not in text:
            out.append(Issue(name, "blocker", "K23", "plate %s 不在主体 md 的 index 表里" % pl))
        m = _PLATE_NAME.match(pl)
        if not m:
            out.append(Issue(name, "blocker", "K23b", "plate 命名不是三段式 bgN-M_方位_描述：%s" % pl))
            continue
        token = m.group(3)
        for old, owner in used_tokens.items():
            if owner == name:
                continue
            if token in old or old in token:
                out.append(Issue(name, "blocker", "K23b",
                                 "方位 token「%s」与 %s 的「%s」互为子串——导入器按子串路由会撞车" % (token, owner, old)))
        used_tokens[token] = name
    return out


def check_casting(drama: str, cards: dict[str, str]) -> list[Issue]:
    path = os.path.join(drama, "2_世界观人设", "casting.md")
    if not os.path.exists(path):
        return [Issue("casting.md", "warning", "K7", "尚未生成（阶段 2 收尾时须建，与各角色卡双向一致）")]
    table = io.open(path, encoding="utf-8").read()
    out: list[Issue] = []
    for name, text in cards.items():
        # **同一行内**、且长得像 id 才算声明。跨行贪婪会把整段声线描述当成 id，
        # 而「不分配 voice_id」这种句子会让正则去抓后面第一个反引号里的任意内容。
        m = _VOICE_ID.search(_section(text, "配音参考") or text)
        if not m:
            continue
        vid = m.group(1)
        if vid not in table:
            out.append(Issue(name, "blocker", "K7", "voice_id `%s` 未登记进 casting.md" % vid))
    rows = [ln for ln in table.split("\n") if ln.startswith("|")]
    ids = [i for ln in rows for i in _VOICE_SHAPE.findall(ln)]
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        out.append(Issue("casting.md", "blocker", "K7", "voice_id `%s` 被两个角色共用——音色必串" % d))
    stale = _stale_voice_ids(table)
    if stale:
        out.append(Issue("casting.md", "blocker", "G8",
                         "%d 个 voice_id 不是 `en-` 开头（本剧全员英文配音）：%s"
                         % (len(stale), "、".join(stale[:6]) + (" …" if len(stale) > 6 else ""))))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("drama")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    cdir = os.path.join(args.drama, "2_世界观人设", "characters")
    if not os.path.isdir(cdir):
        print("没有 characters/ 目录")
        return 1

    issues: list[Issue] = []
    cards: dict[str, str] = {}
    for d in sorted(os.listdir(cdir)):
        p = os.path.join(cdir, d, d + ".md")
        if not os.path.exists(p):
            alt = [f for f in os.listdir(os.path.join(cdir, d)) if f.endswith(".md")]
            issues.append(Issue(d, "blocker", "12.9",
                                "目录里没有 %s.md（实有：%s）" % (d, "、".join(alt) or "空")))
            continue
        cards[d] = io.open(p, encoding="utf-8").read()
        issues.extend(check_card(p, is_mob=d.startswith("m")))
    issues.extend(check_casting(args.drama, cards))

    sdir = os.path.join(args.drama, "2_世界观人设", "scenes")
    scenes = 0
    if os.path.isdir(sdir):
        tokens: dict[str, str] = {}
        # 主体目录可以嵌在世界层级下面（`scenes/{大陆}/{区}/bg{N}_…`，follow-up 006）：
        # 判据不变——`bg{N}_` 开头 + 同名 md；层级目录（大陆 / 区）只是索引，不参与场景检查。
        for dp, dirs, _files in os.walk(sdir):
            dirs[:] = sorted(d for d in dirs if d not in _SKIP_DIRS and not d.startswith("."))
            base = os.path.basename(dp)
            if not _BG_DIR.match(base):
                continue
            dirs[:] = []      # 主体目录里面是 plate / planning / ref，不再往下找主体
            p = os.path.join(dp, base + ".md")
            if os.path.exists(p):
                scenes += 1
                issues.extend(check_scene(p, tokens))
            else:
                issues.append(Issue(base, "blocker", "12.9", "场景目录里没有同名主体 md"))

    b = [i for i in issues if i.level == "blocker"]
    w = [i for i in issues if i.level == "warning"]
    print("检查 %d 张角色卡 + %d 个场景主体 —— blocker %d · warning %d\n"
          % (len(cards), scenes, len(b), len(w)))
    for i in b:
        print("  ❌ [%s] %s: %s" % (i.code, i.card, i.detail))
    for i in w:
        print("  ⚠ [%s] %s: %s" % (i.code, i.card, i.detail))
    if not issues:
        print("  全部通过 ✔")
    return 1 if b else 0


if __name__ == "__main__":
    raise SystemExit(main())
