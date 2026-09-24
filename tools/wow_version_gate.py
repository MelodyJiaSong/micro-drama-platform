# -*- coding: utf-8 -*-
"""经典旧世版本红线闸门 —— 把「版本错置」这一整类错误挡在 build 之前。

契约出处：`ai_videos/shengji_zhilu/1_立项/concept.md` A1 / F6 ·
`0_research/blacklist.md` A 类 · `CLAUDE.md`「能量化的反馈必须落成可机检的闸门」。

## 为什么需要它

本剧锚定**经典旧世 Vanilla 1.12**，而**大地的裂变 4.0.3a 把人族 1–30 级区域整体重写过**。
网上能搜到的图文**大多数是大灾变之后的版本**，生成模型的默认输出因此天然偏向错误的那一版。
这不是"写 prompt 时记得注意"能解决的——一条写进 playbook 的叮嘱，靠的是下一次有人记得读它；
一个闸门，是下一次**做不出违规产物**。

## 两级判据（精度取舍，照抄 prompt_light 的教训）

**HARD —— 在经典旧世里全局不成立的专名，判得准，所以是 blocker。**
「凡妮莎·范克里夫」在 1.12 的艾泽拉斯不存在，不管这一镜拍的是哪里。

**SCOPED —— 只在特定地区错的，判不准，所以只报 warning 并附正解。**
「黑石兽人」出现在燃烧平原是对的，出现在北郡新手谷是 4.0.3a 的剧情。
本闸门不知道这一镜拍的是哪里（那要解析场景卡），所以交人判断。
**宁可少报、报准**——一个在全语料上大面积报警的检查，等于没有检查。

## 只扫正向，不扫负向

`负面词:` 行里**本来就应该**写满这些词（那正是黑名单的用途）。
扫描前剔掉负向行与含否定词的分句，否则闸门会把"做对了"判成"做错了"。

用法：
    import wow_version_gate
    wow_version_gate.gate(md_by_shot, legacy={"shot07"})   # 生成器构建闸门

    python tools/wow_version_gate.py                        # 全仓巡检
    python tools/wow_version_gate.py ai_videos/shengji_zhilu
"""
import io
import os
import re
import sys
from dataclasses import dataclass

# ── HARD：经典旧世全局不成立。命中即 blocker ────────────────────────────
HARD: dict[str, str] = {
    "凡妮莎": "Vanilla 的迪菲亚首领是**埃德温·范克里夫**（她父亲）；凡妮莎是大地的裂变才登场的",
    "西部荒野旅": "25 ADP 时叫**人民军（People's Militia）**；改名发生在 27 ADP 天灾战争期",
    "Westfall Brigade": "同上，25 ADP 是人民军",
    "训练假人": "修道院内院的训练假人是 **4.0.3a 加的**，旧世没有",
    "木桩靶": "同上，4.0.3a 才有",
    "瓦里安": "Vanilla 的暴风城是**十岁的安杜因**戴冠、**伯瓦尔·弗塔根**摄政；瓦里安当时失踪在外",
    "暴风城港口": "港口是 **3.0.2 巫妖王之怒**才开的，旧世没有",
    "斯托姆温德港": "同上",
    "死亡之翼": "大地的裂变的事，旧世不存在",
    "哈蒙德·克雷": "旧世霍格是**可杀的 11 级精英**，不是被将军逮捕押走的事件 boss（那是 4.0.3a）",
    "库尔托克": "4.0.3a 北郡剧情的 NPC，旧世不存在",
    "专精": "旧世是**天赋树**（三系自由加点），没有「专精三选一」——那是 5.0 之后的形态",
    "三选一卡片": "同上，旧世无专精选择界面",
    "飞行坐骑": "旧世的天空**不能飞**，飞行坐骑是燃烧的远征才有的",
    "Bravo Company": "赤脊山的 B 连剧情是 **4.0.3a** 加的戏仿线",
    "B连": "同上",
}

# ── SCOPED：只在特定地区/语境错。报 warning 并附范围 ────────────────────
SCOPED: dict[str, str] = {
    "狮鹫栖木": "**旧世艾尔文森林全境零飞行点**——闪金镇/东谷的狮鹫都是 4.0.3a 加的。若本镜在哨兵岭或暴风城则合法",
    "飞行管理员": "同上，艾尔文森林内一律非法；哨兵岭（10 级，人类第一次坐狮鹫）合法",
    "巴特莱特": "闪金镇的狮鹫管理员，4.0.3a 新增",
    "燃烧的葡萄园": "**北郡是安宁的**——葡萄园在烧、兽人进攻新手村是 4.0.3a 的开场",
    "黑石兽人": "出现在燃烧平原/赤脊山合法；出现在**北郡新手谷**是 4.0.3a 剧情",
    "地精刺客": "北郡的地精刺客是 4.0.3a；别处的地精合法",
    "焦黑哨塔": "**哨兵岭在旧世是完好的**木制哨塔与营地，没被烧毁",
    "在建石墙": "同上，哨兵岭没有在建石墙与脚手架",
    "塌陷巨坑": "西部荒野的 Raging Chasm 是 4.0.3a 加的",
    "乌瑟尔": "**教堂广场喷泉上的雕像，旧世是阿隆索斯·法奥**，乌瑟尔像是大灾变才换上去的。作为 lore 人物被提及则合法",
    "完整的木桥": "**湖畔镇大桥在旧世没修好**——断桥是赤脊山的标志性景观",
    "红色蜘蛛": "艾尔文森林的母牙在旧世是**绿色、10 级**；红色是 4.0.3a 改的",
    "20级坐骑": "旧世坐骑门槛是 **40 级**（圣骑士军马）/ 60 级战马",
    "10级坐骑": "同上，旧世 40 级才有坐骑",
}

_NEGATION = re.compile(r"(没有|不许|不出现|绝不|不会|无任何|禁止|不存在|不得|非法)")
_CLAUSE = re.compile(r"[；;。，,\n]")
_NEG_LINE = re.compile(r"^(负面词|负向|负向词)\s*[:：]")
SKIP_DIRS: tuple[str, ...] = ("_deleted", "previz", "renders")


@dataclass(frozen=True)
class Issue:
    shot: str
    level: str      # blocker | warning
    token: str
    detail: str


def positive(md: str) -> str | None:
    """取 prompt 正文（第一个 ```text 块）。"""
    b = re.findall(r"```text\n(.*?)\n```", md, re.S)
    return b[0] if b else None


def _scannable(pos: str) -> str:
    """剔掉负向行与含否定词的分句——写在负向里是**做对了**，不该被判违规。"""
    kept = [ln for ln in pos.split("\n") if not _NEG_LINE.match(ln.strip())]
    return "；".join(c for c in _CLAUSE.split("\n".join(kept)) if not _NEGATION.search(c))


def check(shot: str, md: str) -> list[Issue]:
    pos = positive(md)
    if not pos:
        return []
    scan = _scannable(pos)
    out: list[Issue] = []
    for tok, fix in HARD.items():
        if tok in scan:
            out.append(Issue(shot, "blocker", tok, fix))
    for tok, fix in SCOPED.items():
        if tok in scan:
            out.append(Issue(shot, "warning", tok, fix))
    return out


def gate(md_by_shot: dict[str, str], legacy: set[str] | None = None) -> list[Issue]:
    """生成器的构建闸门。

    `legacy` ＝ 显式技术债清单（已按旧串出过渲染、暂不改的镜号）。
    **只减不增**：新镜不在里面，一旦犯同样的错就直接终止生成。
    """
    legacy = legacy or set()
    issues = [i for s, md in sorted(md_by_shot.items()) for i in check(s, md)]
    hard = [i for i in issues if i.level == "blocker" and i.shot not in legacy]
    if hard:
        raise SystemExit(
            "版本错置 %d 处（经典旧世 1.12 红线）：\n" % len(hard)
            + "\n".join("  %s 「%s」 → %s" % (i.shot, i.token, i.detail) for i in hard))
    return issues


def _load(root: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not (fn.startswith("shot") and fn.endswith(".md")) or fn == "shotlist.md":
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            out[rel] = io.open(p, encoding="utf-8").read()
    return out


def _scan(root: str) -> int:
    shots = _load(root)
    print("扫描 %d 个 shot md（已跳过 %s）" % (len(shots), "、".join(SKIP_DIRS)))
    issues = [i for s, md in sorted(shots.items()) for i in check(s, md)]
    b = [i for i in issues if i.level == "blocker"]
    w = [i for i in issues if i.level == "warning"]
    for i in b:
        print("  ❌ %s 「%s」 → %s" % (i.shot, i.token, i.detail))
    for i in w:
        print("  ⚠ %s 「%s」 → %s" % (i.shot, i.token, i.detail))
    if not issues:
        print("无版本错置 ✔")
    else:
        print("\nblocker %d · warning %d" % (len(b), len(w)))
    return len(b)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(1 if _scan(sys.argv[1] if len(sys.argv) > 1 else "ai_videos") else 0)
