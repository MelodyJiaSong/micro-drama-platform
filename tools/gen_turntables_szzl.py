# -*- coding: utf-8 -*-
"""《圣光刚好够用》人物卡的 4 秒建立视频（turntable）prompt（ai_video.md rule 12.5 / 22.2）。

每张人物卡都要有**一张立绘 prompt + 一条 4 秒建立视频 prompt**：立绘定脸，turntable 定体型、服装、随身物、站姿与声音，
两者一起建 Seedance 角色资产包 entity（shot 的 `参考:` 直接 @ 它，rule 23 2026-09-25 修订）。

单一出处（rule 4i ①）——本工具不写任何角色内容，一律在构建时读：
  · 长相 / 装束 / 随身物 ← 本卡 `# Seedream 立绘 prompt` 下首行 ＝ 目录名的 text 块（去掉取景、光线、背景、风格、画幅行）
  · 负向               ← 同一块的 `负面词` 行，没有就读卡里 `## 负向` 节（与 gen_char_images 同一套取法）
  · 声线 / voice_id    ← `casting.md`；casting 里没有这张卡的 → 本条建立视频不出声（rule 22.2 零台词角色）
写进卡里 `## turntable 说明` 一节（在立绘标题之前；已有就整节替换）。
**已有手写视频 prompt 的卡（节里有 text 块、却没有本工具的生成标记：c1 / c2 / c6 / c10）一律不动**——它们写得比模板细
（c10 的圣光光环、c6 的腰后双匕），模板覆盖只会变差。旧卡里手写、但没写成 prompt 的要点（声样怎么演、侧面 / 背面必须看见什么）
收在下面的 `NOTES` 表，拼进 prompt。

用法（仓库根目录）：
    python tools/gen_turntables_szzl.py            # 写卡
    python tools/gen_turntables_szzl.py --check    # 只核对：每张卡都有首行 `{目录名}_turntable` 的视频块
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import gen_char_images as gci  # noqa: E402
from tools.gen_turntable_videos import CRY, creature_sound  # noqa: E402  叫声一节的读法只在那里定义

CHARS = REPO / "ai_videos" / "shengji_zhilu" / "2_世界观人设" / "characters"
CASTING = CHARS.parent / "casting.md"
MARK = "由 `tools/gen_turntables_szzl.py`"
# 旧卡 turntable 节里手写的要点（2026-09-25 从 git 旧版找回）：voice ＝ 声样怎么演，side / back ＝ 那一秒必须看得见什么
NOTES: dict[str, dict[str, str]] = {
    "c3_Owen": {"voice": "快、亮、平，像随口交代一句就要接着说下一句",
                "back": "后背完全空着（无披风、无战袍、无背挂武器），腰间织带绕到背后的两圈与那本小册子挂在侧后方的垂感清楚"},
    "c4_Maren": {"voice": "语速比别的角色慢一档，句尾不上扬",
                 "side": "软帽轮廓、罩衫的无袖肩线、麻绳束带的系结、两手空空垂在身侧",
                 "back": "低束发的发尾与长袍后摆垂坠自然，背上没有任何金属"},
    "c5_Rook": {"side": "腰后那串细铁签清楚可见，它被软皮裹着、彼此不相碰",
                "back": "墨绿软皮兜帽后翻搭在肩背上的形状与内衬清楚，后背完全空着（无披风、无战袍、无背挂武器）"},
    "c7_Marshal_McBride": {"voice": "公事公办"},
    "c8_Marshal_Dughan": {"back": "是站着的静定，肩膀有呼吸起伏"},
    "c9_Duthorian_Rall": {"voice": "慢，不抬音量"},
    "c11_Edwin_VanCleef": {"voice": "慢，压着嗓子，不抬音量"},
    "c12_Hogger": {"voice": "极低喉音、含混、字间拖喘（这句只是音色采样，剧中他从不说完整复句）"},
}
HEAD = re.compile(r"^# Seedream 立绘 prompt.*$", re.M)
SECTION = "## turntable 说明"
FENCE = "`" * 3
PROMPT_MAX = 5000
VOICE_LINE = "Hello. It's quiet out today, and the weather's not bad."   # 跨角色 byte-identical（与 c1 / c2 同一句）

LABEL = re.compile(r"^([^：:，。]{1,20})[：:]")
DROP_LABELS = ("光线", "光源", "背景", "风格", "比例", "画幅", "负面词", "构图", "镜头", "验收", "用途", "视角", "参考", "上传", "出图", "摄影")
# 立绘的取景 / 布光 / 画幅子句——建立视频有自己的一套，照抄会打架
FRAMING = re.compile(r"立绘|竖幅|竖屏|画幅|占画面|画面高度|画面中央|平视镜头|正面平视|人物居中|正面站定|正面站立|单体|中性站姿"
                     r"|背景|透视线|4K|9:16|无环境|布光|影棚光|参考图|侧身站姿|头转向镜头|脚下留白|无地平线|无投影|无墓碑|无地面"
                     r"|全身站姿|并排|等距|单个主体|单主体|居中站立")
DROP_CLAUSE = ("", "人物", "正面")
GROUP = re.compile(r"[三两]名|[三两]具|[三两]只|[三两]人")          # 立绘是一组并排的群体怪
FLOAT = re.compile(r"悬浮|悬在")
TT_NEG = ("机位移动", "镜头推拉", "背景变化", "人物位移", "换脸", "面部与参考图不一致", "多余装备", "背景音乐", "旁白", "第二个人")
SILENT_NEG = ("人声", "说话", "台词", "口型")


def casting_voice(key: str) -> tuple[str, str] | None:
    """(voice_id, 声线)；casting 表里按「· c13）」这类卡号认行。"""
    no = key.split("_", 1)[0]
    for ln in CASTING.read_text(encoding="utf-8").split("\n"):
        if not ln.startswith("| **"):
            continue
        cells = [c.strip() for c in ln.split("|")]
        if re.search(r"[（(][^）)]*(?<![A-Za-z0-9])%s(?![0-9])" % re.escape(no), cells[1]):
            vid = re.search(r"`(en-[^`]+)`", ln)
            return (vid.group(1), cells[3].replace("**", "")) if vid else None
    return None


CRY_MUTE = ("m5", "m6")        # 机器与灵体：「人声 / 说话 / 台词 / 口型」四个照留（w24 §2）
CRY_USAGE = "声音参考只借音色与质感，不照搬它的节奏、内容与环境底噪；画面里不出现参考录音里的动物或器物。"


def portrait_lines(body: str) -> list[str]:
    """立绘块 → 只留「这个角色长什么样、穿什么、带什么」的行。"""
    out: list[str] = []
    dropping = False
    for raw in body.split("\n")[1:]:
        ln = raw.strip()
        if not ln or ln.startswith("本图"):
            continue
        m = LABEL.match(ln)
        if m:
            dropping = m.group(1).startswith(DROP_LABELS)
        if dropping:
            continue
        # 句内的取景 / 画幅子句（「一名…的全身立绘，9:16 竖幅，人物居中…」）去掉，身份与姿态子句留下
        ln = ln.replace("的全身立绘", "").replace("人物全身立绘", "").replace("全身立绘", "")
        parts = [p for p in re.split(r"(?<=[，。])", ln) if p.strip()]
        kept = "".join(p for p in parts if not FRAMING.search(p) and p.strip("，。 ") not in DROP_CLAUSE)
        if kept.strip("，。"):
            out.append((kept, bool(m)))
    # 原卡里一句话折成几行时行尾是逗号，照留；只有下一行另起一个标签（或到头了）才收成句号
    lines: list[str] = []
    for i, (ln, _) in enumerate(out):
        nxt_label = i + 1 == len(out) or out[i + 1][1]
        if nxt_label and ln.endswith("，"):
            ln = ln[:-1] + "。"
        elif not ln.endswith(("，", "。", "；", "：", ":")):
            ln += "。" if nxt_label else "，"
        lines.append(ln)
    return lines


def build(d: Path) -> tuple[str, str]:
    """(整节 markdown, 视频 prompt)。"""
    key = d.name
    job = gci.Job(d, HEAD, gci.KINDS["characters"][1])
    ratio = job.aspect             # 建立视频跟立绘同画幅：人物竖幅、四足兽横幅（follow-up 055）
    body = next(m.group(1) for m in gci.BLOCK.finditer(d.joinpath(key + ".md").read_text(encoding="utf-8")[
        HEAD.search(d.joinpath(key + ".md").read_text(encoding="utf-8")).end():])
                if m.group(1).split("\n")[0].strip() == key)
    look = portrait_lines(body)
    floating = any(FLOAT.search(l) for l in look)
    group = any(GROUP.search(l) for l in look[:3])
    neg_src = re.split(r"负面词[：:]", job.prompt, maxsplit=1)
    negs = [n.strip() for n in re.split(r"[，,、]\s*", neg_src[1] if len(neg_src) > 1 else "") if n.strip()]
    voice = casting_voice(key)
    cry = creature_sound(d)
    if cry:
        mute = (list(SILENT_NEG) if key.split("_")[0] in CRY_MUTE else
                [] if cry["speaks"] else ["人类说话声", "说话", "台词"])     # 叫、咕噜、低吼要张嘴：不挂「口型」
        negs = list(dict.fromkeys(negs + list(TT_NEG) + mute + cry["neg"]))
    else:
        negs = list(dict.fromkeys(negs + list(TT_NEG) + ([] if voice else list(SILENT_NEG))))
    if cry:
        sound = "声音：" + cry["sound"]
        if cry["speaks"]:
            say, turn, done = "，开口出声", "一边接着出声，一边", "，声音在 3.5 秒前收住"
        else:
            say, turn, done = "，开始发出叫声", "叫声不停，一边", "，声音在 3.5 秒前收住"
    elif voice:
        how = NOTES.get(key, {}).get("voice")
        sound = ("声音：从 0 秒开口，角色用英语说一句——%s 声线：%s。%s约 3.5 秒说完，之后闭嘴，不再出声；"
                 "没有旁白、没有背景音乐，只有摄影棚的安静底噪。" % (
                     VOICE_LINE, voice[1].rstrip("。"), ("演法：%s。" % how) if how else ""))
        say, turn, done = "，开口说那一句话", "一边接着说，一边", "，那句话在 3.5 秒前说完"
    else:
        sound = "声音：角色全程不出声、不张嘴说话；没有旁白、没有背景音乐，只有摄影棚的安静底噪。"
        say, turn, done = "", "", ""
    audio = ["`%s声音(%s·只借音色)=>@`" % (key, p.stem.replace("_", " ", 1)) for p in (cry["refs"] if cry else [])]
    prompt = "\n".join([
        key + "_turntable",
        "参考: " + "、".join(["`%s(立绘·脸的唯一标准)=>@`" % key] + audio),
        "参考用法: 参考图定这个角色的长相、这一身行头与随身物件的形制和颜色，一律照搬，不得重新设计、不得美化，"
        "不得添加参考图里没有的装备。本视频负责把体型、衣着、随身物件与站姿在正、侧、背三个朝向上交代清楚。"
        + (CRY_USAGE if audio else ""),
        "角色建立视频：参考图里的这个角色%s中性浅灰色摄影棚背景正中，阴天正午式的均匀柔和散射光，"
        "机位固定不动、焦距不变，角色原地缓慢自转，全身入画、%s，两侧留出均匀的灰背景。" % (
            "悬在" if floating else "站在", "保持参考图里离地悬浮的高度" if floating else "双脚踩实地面"),
        *(["参考图是同一类的几个并排站着；本视频只要其中最左边的那一个，单独一个在画面正中，其余的都不出现。"] if group else []),
        *look,
        "光与特效：除上文写明的角色自带光源外，本视频没有任何发光特效，角色不自发光，瞳孔不发光，武器不发光，脚下没有光环。",
        sound,
        "镜头时间轴：",
        "0-1 秒 正面站定，脸清晰可见、平视镜头%s。" % say,
        "1-1.5 秒 %s开始向左缓慢转动，姿态与身上、手里的东西保持不变。" % turn,
        "1.5-2.5 秒 转到左侧身静止：侧脸轮廓、体型侧影、随身物件的厚度与全长，全部完整可见%s。" % (
            "；" + NOTES[key]["side"] if "side" in NOTES.get(key, {}) else ""),
        "2.5-3 秒 继续向左转动到背面。",
        "3-4 秒 背面静止%s：背后的装束与随身物件清楚可见，背上没有参考图里没有的东西%s。" % (
            done, "；" + NOTES[key]["back"] if "back" in NOTES.get(key, {}) else ""),
        "风格：影视级实拍质感，35mm 胶片颗粒，浅景深，真实皮肤纹理与布料纤维，物理正确的材质反射，"
        "真人正常比例不做英雄化夸张；画面不烧字幕、不出现任何文字。",
        "比例：画幅 %s，时长 4 秒。" % ratio,
        "负面词: " + ", ".join(negs),
    ])
    if len(prompt) > PROMPT_MAX:
        raise SystemExit("%s turntable prompt %d 字 > %d" % (key, len(prompt), PROMPT_MAX))
    if not look:
        raise SystemExit("%s：立绘块里抽不出任何长相 / 装束行" % key)
    if cry:
        voice_row = ("- **叫声**（0–3.5 s）：见本卡 `%s`（出处 w24）%s；参考录音：%s（真实录音，只借音色，许可见 `ref/audio/refs.md`）" % (
            CRY, "；人声走 `%s`" % voice[0] if (voice and cry["speaks"]) else "",
            "、".join("`ref/audio/%s`" % p.name for p in cry["refs"]) or "无"))
    else:
        voice_row = ("- **声样**（0–3.5 s · 跨角色同一句）：`%s`，用 `%s` 的声线" % (VOICE_LINE, voice[0]) if voice else
                     "- **声样**：无——`casting.md` 里没有这张卡的 voice_id，建立视频全程不出声（rule 22.2 零台词角色）；"
                     "要让它在资产包里带声音，先在 casting 补一行再重跑")
    ok6 = ("叫声按 `%s` 的时间轴走完，3.5 s 后静音；画面里没有参考录音里的动物或器物" % CRY if cry else
           "那一句英文逐字说完，3.5 s 后静音" if voice else "全程不出声")
    uploads = "、".join(["`` `%s(立绘·脸的唯一标准)=>@` ``" % key] + ["`` %s `` ← `ref/audio/%s`" % (h, p.name) for h, p in zip(audio, cry["refs"] if cry else [])])
    section = f"""{SECTION}（4 s 建立视频 reference · rule 12.5 / 22.2）

> 由 `tools/gen_turntables_szzl.py` 从本卡立绘 prompt 与 `casting.md` 生成，**勿手改**——改立绘 prompt 或 casting 后重跑。
> 立绘定**脸**，turntable 定**体型 + 服装 + 随身物 + 站姿 + 声音**；两者一起建 Seedance 角色资产包 entity。
> 画幅 **{ratio}**｜时长 **4 s**｜5-phase locked-framing single-take｜抽帧 front 0.5 s / side 2.0 s / back 3.5 s。

- **路由键 / prompt 首行**：`{key}_turntable`　**落盘**：`characters/{key}/{key}_turntable.mp4`
- **上传**：{uploads}
{voice_row}
- **验收**：① 4 秒内完成正→侧→背；② 机位、焦距与角色中心全程不动；③ 正面与 `{key}.png` 是同一个角色；
  ④ 侧、背两面的装束与随身物件与立绘一致，没有多出来的东西；⑤ 全程无字幕、无文字、无 UI；⑥ {ok6}。

{FENCE}text
{prompt}
{FENCE}

"""
    return section, prompt


def splice(text: str, section: str) -> str:
    """整节替换；没有就插在立绘标题之前。"""
    i = text.find(SECTION)
    if i >= 0:
        j = min([k for k in (text.find("\n## ", i + 1), text.find("\n# ", i + 1)) if k >= 0] or [len(text)])
        return text[:i] + section.rstrip("\n") + "\n" + text[j:]
    h = HEAD.search(text)
    return text[:h.start()] + section + text[h.start():]


def hand_written(text: str) -> bool:
    """节里已有 text 块、又不是本工具写的 ＝ 手写 prompt，不动。"""
    i = text.find(SECTION)
    if i < 0:
        return False
    j = min([k for k in (text.find("\n## ", i + 1), text.find("\n# ", i + 1)) if k >= 0] or [len(text)])
    sec = text[i:j]
    return FENCE + "text" in sec and MARK not in sec


def has_video(d: Path) -> bool:
    text = (d / (d.name + ".md")).read_text(encoding="utf-8")
    return any(m.group(1).split("\n")[0].strip() == d.name + "_turntable" for m in gci.BLOCK.finditer(text))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", default="", help="逗号分隔的卡号，如 c13,m1")
    args = ap.parse_args()
    only = [s for s in args.only.split(",") if s]
    dirs = sorted(d for d in CHARS.iterdir() if d.is_dir() and (d / (d.name + ".md")).is_file()
                  and (not only or d.name.split("_")[0] in only))
    if args.check:
        miss = [d.name for d in dirs if not has_video(d)]
        for m in miss:
            print("  ✗ %s：没有首行为 `%s_turntable` 的建立视频块" % (m, m))
        print("%d 张卡 · 缺 %d" % (len(dirs), len(miss)))
        return 1 if miss else 0
    for d in dirs:
        p = d / (d.name + ".md")
        if hand_written(p.read_text(encoding="utf-8")):
            print("  %-24s 手写，不动" % d.name)
            continue
        section, prompt = build(d)
        p.write_text(splice(p.read_text(encoding="utf-8"), section), encoding="utf-8", newline="\n")
        cry = creature_sound(d)
        print("  %-24s %4d 字  %s" % (d.name, len(prompt), ("叫声（参考录音 %d 段）" % len(cry["refs"])) if cry else
                                        "有声" if casting_voice(d.name) else "无声"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
