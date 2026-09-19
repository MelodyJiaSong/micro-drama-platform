# -*- coding: utf-8 -*-
"""把 sk2 的 **look 层** 盖进每一张阶段 2 图 prompt（follow-up 010）。

为什么有这个文件
----------------
rule 4i ①「一份东西只有一个出处，副本必漂」。13 张场景卡 / 27 张视图里重复着同一套
「这张图长什么样」的东西——媒介声明、摄影器材与景深纪律、做旧通则、渲染样式串、负向块。
手改 27 处必漂，所以它们从此只有一个出处：本文件。

本文件**只拥有 look 层**，不碰内容层：
  拥有  媒介 / 摄影 / 渲染样式 / 做旧通则 / 负向成因块
  不碰  场景 / 构图与视角 / 建筑形制 / 街具 / 地面 / 人物 / 光线与时段的**时辰与光源**

2026-09-19 用户定调「画面太像劣质游戏 CG，我们要真实感」。复盘出三个病灶：

1. **`渲染样式:` 以「半写实」开头，且写着「忠于原作」——而原作是一款游戏。**
   正面在说「照着游戏画」，负面挂着「游戏引擎渲染」。正面永远赢负面
   （同侏儒五指、同东亚脸，这是同一失效模式的第三次）。
   根子是把两个**互相独立的轴**混成了一个：
     轴一 形制/比例/配色 → 按暴风城设定（该保）
     轴二 影像真实度     → 被一起降成了「半写实」（不该降）
   「半写实」形容的是**世界的设计**，不是**画面的渲染**。

2. **`材质与做旧:` 在主动要求「石面干净、缝口整齐、几乎没有风化」**——那正是游戏资产的样子。
   设定上暴风城是战后重建的新城没错，但真实照片里再新的城也有积灰、水渍、色差、歪瓦。

3. **`瓦色是饱和的中蓝`——「饱和」这个词本身就是反写实的。** 蓝顶要保，但实拍影调下
   它是偏灰的中蓝，不是纯色块。

第四条是**位置**：`渲染样式:` 原先排在 prompt 第 12 行，前面 11 行全在讲暴风城的内容，
模型早已建立游戏美术的先验。与先验对抗的约束**必须放最前面**——所以本文件把
`媒介:` 插到 `参考用法:` 之后、一切内容之前。

口径直接继承 `ai_video.md` §18（sk1 2026-09-16「太像动画，全部重来」的产物），
不另起炉灶——那一套已经出过可验收的图（见 `sk1/.../bg4-1.png`）。

Run（repo root）：
    python tools/gen_scene_prompts_sk2.py            # 写盘
    python tools/gen_scene_prompts_sk2.py --check    # 只校验不写盘
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SCENES = REPO / "ai_videos" / "shikong_lvxing" / "sk2" / "2_世界观人设" / "scenes" / "stormwind"

# 上限由**在用的模型**定，不由一个启发值定。
# 实测（2026-09-19，同一批 prompt）：
#   gpt-image-2（在用）  收下 2500+ 无问题；外景最好的一张 bg2-1 v3 就是 2500 字
#   ElevenLabs-seedream  硬限 2000（400 invalid_parameters）
#   即梦-seedream 5.0    硬限 1600（ret=1046 prompt len is larger than limited len）
# rule 4d ⑤ 的「硬顶 2000」写于 prompt ＝ 纯形制描述的年代；sk2 每张卡多背两层**强制**内容
# （rule 16.9 的逐镜反向声明 + 本文件的 look 层）。取舍：不删有设定背书的建筑形制去迁就启发值。
# **若将来换 seedream，必须先跑一轮压缩**——那两个硬限是真的会 4xx 的。
MAX_CN = 2300
MIN_CN = 1200   # 室内小景放宽（rule 4d ⑤ 原文是 ≥1500）

# ── look 层的五个串 ────────────────────────────────────────────────────────────

MEDIA_BODY = (
    "**实拍电影剧照，不是渲染图、不是游戏截图、不是概念原画。**"
    "拍的是按下文设定搭出来的实景与真人演员：设定管「长什么样」，"
    "真实光学与真实材料管「拍出来什么样」，后者不因前者打折。"
)

STYLE = (
    "ARRI ALEXA + Cooke S4/i 定焦实拍，1/48 秒自然运动模糊；"
    "《权力的游戏》那一路的影调：高光柔滚不死白，暗部厚实该黑就黑，不抬亮不补蓝；"
    "颜色压过、偏灰偏实，不是纯色块；边缘略松、淡暗角、轻微色散与柔光晕，"
    "细腻不匀的胶片颗粒；画面内无任何文字"
)

# 景深与大气——这两条是「像 CG」与「像照片」最大的分水岭（§18 ②）
OPTICS = (
    "**不是全景深**：最近的主体最实，每往深一层软一档，最远的那一层只剩一个偏蓝灰的轮廓；"
    "**空气看得见**——越远越淡、越软、越偏蓝灰，这不是雾，是距离；"
    "受光面与阴影差三档，**阴影里只留很少细节**，不抬亮、不补蓝"
)

SKY = "天空有云与层次、近地平线一圈淡蓝灰的霾，不是纯渐变；天上没有飞行物"

WEAR = (
    "做旧按材质写死——"
    "石：踩踏面磨出凹坑、边棱磨圆，缝里积灰生草、墙根一圈返潮的深色水渍，"
    "**每块的色差与缺角各不相同，不是切割整齐的新石材、不是重复贴图**；"
    "木：向阳面晒白起毛刺、背阴发灰长霉斑，接缝开裂翘边，手常握处磨出油亮包浆，**没有刨光的新板**；"
    "铁：氧化起麻点、流痕挂在下方，手常碰的地方磨出亮，**不是均匀的哑黑漆面**；"
    "布：洗到发白、有补丁与污渍、垂坠不挺，**不是崭新的整匹布**；"
    "瓦：个别缺角与歪斜，哑光不反光。"
    "重建不久所以没有百年风化，但**天天有人走的城不可能干净整齐**"
)

# 负向要挡**成因**不挡症状（§18 结论）
NEG_CAUSE = (
    "游戏截图, 游戏引擎画面, 虚幻引擎, 3D 渲染, CG, 概念原画, 建筑效果图, 沙盘模型, "
    "全景深, 边到边一样锐, 均匀布光, 正面平光, 环境光遮蔽, 抬亮的暗部, 补蓝的暗部, "
    "重复贴图, 一尘不染, 崭新的木头, 没有污渍的墙, 纯渐变天空, 奶白色地平线雾, "
    "站桩不动的人, 低多边形, 卡通渲染, 插画风, 塑料高光, 过饱和, 白模, 灰模"
)

# 旧串（要被换掉的）
OLD_STYLE_RE = re.compile(r"半写实电影质感[^\n]*?画面内不出现任何文字[。．]?")
OLD_NEG_RE = re.compile(
    r"游戏截图, (?:游戏引擎渲染, )?UI 界面, 低多边形, 卡通渲染, 塑料高光, 过饱和, 白模, 灰模")

# 「饱和」是反写实词——蓝顶要保，但实拍影调下它偏灰
SAT_FIX = [
    ("瓦色是饱和的中蓝", "瓦色是中蓝（实拍影调下偏灰、不是纯色块）"),
    ("饱和的中蓝", "中蓝（实拍影调下偏灰）"),
    ("屋顶以饱和的中蓝为主", "屋顶以中蓝为主（实拍影调下偏灰）"),
    ("饱和的钴蓝色", "钴蓝色（实拍影调下偏灰）"),
]


def has_sky(block: str) -> bool:
    """这一块有没有天空。rule 16.9：只属于部分镜的设定不许写进共用串。

    地下（bg5-2 / bg6）与室内（bg10 / bg12）的卡明写「没有任何天空」，
    往它们头上盖一句「天空有真实的云」就是直接自相矛盾。
    """
    for k in ("没有任何天空", "全封闭地下", "无天空", "厅内", "堂屋", "室内"):
        if k in block:
            return False
    return "天空" in block or "日光" in block or "天光" in block


# 内容层里与「空气看得见」直接打架的天空写法。
# 注意「空无一物」指的是**没有飞行坐骑**（Vanilla 不能飞），不是没有云——
# 所以只改「干净/通透」这类反大气的措辞，飞行坐骑那层语义原样保留。
SKY_FIX = [
    ("天空是明亮通透的蓝，空无一物。",
     "天空是明亮的蓝，两三缕真实的云与层次、近地平线一圈淡蓝灰的霾；天上没有任何飞行物。"),
    ("天空自地平线的浅金过渡到高处干净通透的蓝，最多两三缕淡高云；",
     "天空自地平线的浅金过渡到高处的蓝，近地平线一圈淡蓝灰的霾、高处两三缕淡云；"),
    ("天空自地平线的浅金过渡到高处干净通透的蓝，天空里空无一物。",
     "天空自地平线的浅金过渡到高处的蓝，近地平线一圈淡蓝灰的霾、高处两三缕淡云；天空里没有任何飞行物。"),
    ("天空自地平线的浅金过渡到高处干净通透的蓝；",
     "天空自地平线的浅金过渡到高处的蓝，近地平线一圈淡蓝灰的霾；"),
    ("天空自地平线的浅金过渡到高处通透的蓝，空无一物。",
     "天空自地平线的浅金过渡到高处的蓝，近地平线一圈淡蓝灰的霾；天上没有任何飞行物。"),
    ("天空是明亮的蓝、只有两三缕淡高云；",
     "天空是明亮的蓝、两三缕淡高云、近地平线一圈淡蓝灰的霾；"),
    ("天空是干净的深蓝、还留一线极淡的余晖；",
     "天空是深蓝、还留一线极淡的余晖，近地平线一层淡霾；"),
]


def strip_look(b: str) -> str:
    """剥掉本文件此前盖过的 look 层，让每次跑都能换成最新口径。

    幂等不等于不可更新：口径改了就要能覆盖旧的，否则「已是最新」会把改进吞掉。
    只删本文件自己加的那几段，作者手写的部分一律不动。

    **不用正则反向引用**——`` 在本文件里被转义吃掉过两次（写进去成了 ，
    替换串于是变成空串，整行被删光，10 张卡差点被写坏）。
    改成「按标记切、留前缀」的明码写法，没有可被吃掉的东西。
    """
    MARKS = (
        (("摄影: ", "【摄影】"), ("；景深是实拍的", "；**不是全景深**")),
        (("材质与做旧: ", "【材质与做旧】"), ("。做旧通则", "。做旧按材质写死")),
    )
    out = []
    for line in b.split("\n"):
        if line.startswith(("媒介: ", "【媒介】")):
            continue                                   # 媒介整行重盖
        for heads, marks in MARKS:
            if line.startswith(heads):
                for m in marks:                        # 两代口径都认
                    i = line.find(m)
                    if i > 0:
                        line = line[:i].rstrip("。．") + "。"
                        break
                break
        out.append(line)
    return "\n".join(out)


def stamp_block(b: str) -> tuple[str, list[str]]:
    """把 look 层盖进**一个 prompt 块**。幂等。"""
    log: list[str] = []
    b = strip_look(b)
    tag = (lambda k: f"【{k}】") if "【摄影】" in b else (lambda k: f"{k}: ")

    # ① 媒介声明紧跟 参考用法 —— 位置就是效力（见模块 docstring 第四条）
    if True:
        out = []
        for line in b.split("\n"):
            out.append(line)
            if line.startswith("参考用法:") or line.startswith("【参考用法】"):
                out.append(tag("媒介") + MEDIA_BODY)
                log.append("媒介")
        b = "\n".join(out)

    # ② 渲染样式整串替换
    if OLD_STYLE_RE.search(b):
        b = OLD_STYLE_RE.sub(STYLE, b)
        log.append("渲染样式")

    # ③ 摄影行追加景深与大气；天空子句**按块条件化**（rule 16.9）
    def optics(mo):
        line = mo.group(0)
        add = OPTICS + ("；" + SKY if has_sky(b) else "")
        return line.rstrip("。．") + "；" + add + "。"

    before = b
    b = re.sub(r"^(?:摄影: |【摄影】)[^\n]*", optics, b, flags=re.M)
    if b != before:
        log.append("摄影+景深" + ("+天空" if has_sky(b) else ""))

    # ④ 做旧通则
    def wear(mo):
        line = mo.group(0)
        line = line.replace("石面干净、缝口整齐、几乎没有风化，只有踩踏面磨出一点包浆；", "")
        return line.rstrip("。．") + "。" + WEAR + "。"

    before = b
    b = re.sub(r"^(?:材质与做旧: |【材质与做旧】)[^\n]*", wear, b, flags=re.M)
    if b != before:
        log.append("做旧")

    # ⑤ 负向换成成因词
    if OLD_NEG_RE.search(b):
        b = OLD_NEG_RE.sub(NEG_CAUSE, b)
        log.append("负向")

    # ⑥ 天空的反大气措辞（是替换不是追加：既消矛盾又不涨长度）
    for a, c in SKY_FIX:
        if a in b:
            b = b.replace(a, c)
            log.append("天空")

    # ⑦ 负向逐词去重（保序）
    def dedup(mo):
        line = mo.group(0)
        sep = "】" if line.startswith("【") else ": "
        head, _, body = line.partition(sep)
        seen, out = set(), []
        for w in (x.strip() for x in body.split(",")):
            if w and w not in seen:
                seen.add(w)
                out.append(w)
        return head + sep + ", ".join(out)

    b = re.sub(r"^(?:负面词: |【负面词】)[^\n]*", dedup, b, flags=re.M)

    # ⑧ 「饱和」是反写实词
    for a, c in SAT_FIX:
        if a in b:
            b = b.replace(a, c)
            log.append("去饱和")
            break
    return b, log


def stamp(text: str) -> tuple[str, list[str]]:
    """只改 bg 的 prompt 块，卡里的散文与对账表一概不碰。"""
    logs: list[str] = []

    def one(mo):
        body = mo.group(1)
        if not re.match(r"^bg\d+-\d+", body.split("\n", 1)[0].strip()):
            return mo.group(0)
        new, log = stamp_block(body)
        logs.extend(log)
        return "```text\n" + new + "```"

    text = re.sub(r"```text\n(.*?)```", one, text, flags=re.S)
    seen = []
    for x in logs:
        if x not in seen:
            seen.append(x)
    return text, seen


def prompts(text: str) -> list[tuple[str, int]]:
    out = []
    for mo in re.finditer(r"```text\n(.*?)```", text, re.S):
        body = mo.group(1)
        head = body.split("\n", 1)[0].strip()
        if not re.match(r"^bg\d+-\d+", head):
            continue
        cn = len(re.findall(r"[一-鿿　-〿＀-￯]", body))
        out.append((head, cn))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校验不写盘")
    args = ap.parse_args()

    errs: list[str] = []
    touched = 0
    for d in sorted(SCENES.iterdir()):
        if not d.is_dir():
            continue
        f = d / (d.name + ".md")
        if not f.exists():
            continue
        src = f.read_text(encoding="utf-8")
        new, log = stamp(src)
        for head, cn in prompts(new):
            if cn > MAX_CN:
                errs.append(f"{head} {cn} 字 > {MAX_CN}")
            elif cn < MIN_CN:
                errs.append(f"{head} {cn} 字 < {MIN_CN}")
        if re.search(r"#[0-9A-Fa-f]{6}", new):
            errs.append(f"{d.name} 含 hex 色值")
        if "半写实电影质感" in new:
            errs.append(f"{d.name} 仍有「半写实电影质感」残留")
        # 反做旧指令的**措辞变体**：只匹配某一张卡的原句会让变体活下来，
        # 而「正面互相打架」的 prompt 里先出现的那条赢（2026-09-19 bg0/bg1 实测）。
        for bad in ("石面干净", "缝口整齐", "几乎没有风化", "一尘不染的", "崭新的城"):
            if bad in new.split("负面词")[0]:
                errs.append(f"{d.name} 正文仍有反做旧措辞「{bad}」")
        counts = " ".join(f"{h.split('_')[0]}:{c}" for h, c in prompts(new))
        mark = "·" if not log else "OK"
        print(f"{mark} {d.name:<24}{'，'.join(log) or '已是最新':<28}{counts}")
        # 防呆：strip→重盖 这条路径出过一次「剥掉了却没盖回去」（ 反向引用被转义吃掉，
        # 结果每块净减约 370 字）。look 层只会让 prompt 变长，**变短一定是盖章失败**——
        # 与其相信它，不如让它自己证明：短了就拒写，把卡留在原样。
        if len(new) < len(src) * 0.92:
            errs.append(f"{d.name} 盖章后反而短了 {len(src)-len(new)} 字——疑似 strip 成功但重盖失败，已拒写")
            continue
        if new != src and not args.check:
            f.write_text(new, encoding="utf-8", newline="\n")
            touched += 1

    if errs:
        print(f"\n闸门未过 {len(errs)} 条：")
        for e in errs:
            print("  x", e)
        raise SystemExit(1)
    print(f"\n{'（--check，未写盘）' if args.check else f'已更新 {touched} 张卡'}")


if __name__ == "__main__":
    main()
