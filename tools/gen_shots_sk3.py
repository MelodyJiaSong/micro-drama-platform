# -*- coding: utf-8 -*-
"""Build every sk3 shot card (stage 5 + 6 combined) from the shot tables.

Same contract as `gen_shots_sk1.py`, but the 49-shot content lives in
`tools/sk3_data/shots_*.toml` so several authors can work at once without
fighting over one file. This module owns the **engine and the gates** — a card
that violates a mechanical contract cannot be written at all:

  · prompt ≤ 5000 中文字符 (CLAUDE.md 全局硬顶)
  · 相邻镜景别跳档: 人占画高比值 ≥2.0 或 ≤0.5 **且机位标签不同** (K31)
    唯一豁免是 shot01→shot02 的航拍承接对 (I-14)
  · 共用串不得点名光源 → tools/prompt_light.py (K32)，legacy 为空
  · 台词语速 ≤ 2.4 words/s，且占镜长 ≤ 80%（留呼吸）
  · **非旅行者的台词必须带 fact_id 或标「虚构人物·现代英语」**（sk3 D2 闸门）
  · prompt 内零 hex、零字幕字样
  · 裸 `=>@` 占位，不得代填槽位号

Run (repo root):
    python tools/gen_shots_sk3.py
    python tools/gen_shots_sk3.py --check
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompt_light  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
DRAMA = REPO / "ai_videos" / "shikong_lvxing" / "sk3"
A = DRAMA / "2_世界观人设"
OUT = DRAMA / "5_6_分镜与prompt"
SHOTS_DIR = OUT / "shots"
STYLE_GUIDE = A / "style_guide.md"
DATA = REPO / "tools" / "sk3_data"

FENCE = chr(96) * 3
NL = "\n"
MAX_PROMPT = 5000
MAX_WPS = 2.4
BREATH = 0.8
HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
SLOT_RE = re.compile(r"=>@\s*[0-9A-Za-z一-鿿]")
SUBTITLE_RE = re.compile(r"字幕|caption|subtitle", re.I)

EN_OPENING = ("It's Saturday, the first of September, 1666. You're in London, three hundred and sixty "
              "years ago. Everything is as it was that day — except I'm here.")
EN_CLOSER = ("I changed nothing. I was just there.",
             "History doesn't do refunds. See you at the next stop.")

# 两个装束态各一个 entity handle —— 初版只有 1666 那个、且写死在 refs_line()，
# 于是 shot03–12 的 `参考:` 说 1666 装、`角色:` 说现代装，同一张卡两行打架。
TR_TOKEN = "c5_妮娅(Seedance 人物 entity·1666 装态)"
TR_TOKEN_MODERN = "c5_妮娅(Seedance 人物 entity·现代装态)"
TR_VOICE = ("妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，"
            "语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔")
TR_LOCK = ("妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、"
           "戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；"
           "不是全黑清教徒装、帽上没有方形金属扣")
TR_MODERN = ("妮娅（Seedance 人物 entity · 现代装态）— 深色运动上衣与工装裤、低帮徒步鞋，"
             "素色布质胸牌别在左胸；短话筒与麻布采访本随身")

# 她不入画的镜（`onscreen = false`）。**这一句必须由生成器写，不能指望作者记得**：
# emit() 无条件写她的锁定串、refs_line() 无条件挂她的 entity 图，模型看到这两样就会把她画进去。
# 实测四位并行作者里只有一位在自己那段写了禁令；漏掉的镜里 shot16 一旦画出她，
# shot17「她站在门口没说出口」整场戏就没了。
TR_ABSENT = ("**本镜画面里不出现旅行者妮娅**——她只有画外声。"
             "不得依据任何锁定描述符把她画进画面；画面里没有任何现代装或 1666 装的年轻女性主体。")

PHOTO = "35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角"
AGING = ("木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；"
         "砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。"
         "所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫")

USAGE = ("白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。"
         "场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，"
         "以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。"
         "物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；"
         "画面里不出现任何文字。")

# 不入画的镜要换一套用法说明——原样板写着「她的脸由 entity 承载」，
# 对一个她根本不该出现的镜来说是自相矛盾的，等于在暗示模型把她画出来。
USAGE_ABSENT = ("白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。"
                "场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，"
                "以本镜 `光线:` 为准。**本镜没有挂旅行者的人物参考图，因为她不入画**——"
                "只挂了她的声样，用于生成画外音。物件锚点锁形制，入画时照搬。"
                "台词由视频直接出声：妮娅的句子全部是画外音，画面里没有她、也没有任何人对这些话做口型；"
                "画面里不出现任何文字。")


# ══════════════════════════════════════════════════════════════════════════════
# 载入
# ══════════════════════════════════════════════════════════════════════════════

def load_shared() -> tuple[str, str]:
    body = STYLE_GUIDE.read_text(encoding="utf-8")
    f = re.findall(r"```text\n(.*?)\n```", body, flags=re.S)
    neg = next((x.strip() for x in f if "thatched roof" in x), None)
    style = next((x.strip() for x in f if "写实纪录片影像" in x), None)
    if not neg or not style:
        raise SystemExit("style_guide.md 缺负向块或 STYLE_BASE")
    return neg, style


def load_shots() -> list[dict]:
    shots: list[dict] = []
    for p in sorted(DATA.glob("shots_*.toml")):
        shots += tomllib.loads(p.read_text(encoding="utf-8")).get("shot", [])
    shots.sort(key=lambda s: s["n"])
    return shots


def scene_oneline(bg_dir: str) -> str:
    """该 bg 的「一句话锁定」——从场景卡里读，保证 shot 与卡逐字一致。"""
    card = A / "scenes" / "london" / bg_dir / ("%s.md" % bg_dir)
    if not card.exists():
        return ""
    m = re.search(r"\|\s*8\s*\|\s*一句话锁定\s*\|\s*(.+?)\s*\|", card.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


# ══════════════════════════════════════════════════════════════════════════════
# 渲染
# ══════════════════════════════════════════════════════════════════════════════

def words(s: str) -> int:
    return len([w for w in re.split(r"\s+", s.strip()) if w])


_VIEW_RE = re.compile(r"^((?:bg|[cp])\d+-\d+)")


def view_key(raw: str) -> str:
    """`bg2-1_布丁巷锚点` → `bg2-1`。

    路由键之后的中文视图名是给人看的，盘上的文件只叫 `bg2-1.png`，而 `参考:` handle
    的机检口径是「handle ⊆ 产物路径」。作者各写各的（有人写短 stem、有人抄 prompt 首行），
    所以**在这里归一**，不靠约定。
    """
    m = _VIEW_RE.match(raw.strip())
    if m is None:
        raise SystemExit("view 不是合法路由键：%r" % raw)
    return m.group(1)


def refs_line(s: dict) -> str:
    """`参考:` 行。装束态必须与 `角色:` 行取同一个 —— 两者都读 `modern_dress`。"""
    out = []
    if s.get("previz"):
        out.append("`shot%02d_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`" % s["n"])
    if s.get("handoff_from"):
        out.insert(0, "`本镜首帧(上一镜末帧)=>@`")
    out.append("`%s(场景主体·%s)=>@`" % (view_key(s["view"]), s["bg"]))
    if "c5" in s.get("chars", ["c5"]):
        # 不入画的镜**不挂她的 entity 参考图**——挂了就是在请模型把她画出来；
        # 声音样本照挂，她仍然在说话。
        if s.get("onscreen", True):
            out.append("`%s=>@`" % (TR_TOKEN_MODERN if s.get("modern_dress") else TR_TOKEN))
        out.append("`妮娅声音(c5-2 声样)=>@`")
    for c in s.get("chars", []):
        if c != "c5":
            out.append("`%s(人物锚点)=>@`" % c)
    for p in s.get("props", []):
        out.append("`%s-1(物件锚点)=>@`" % p)
    return "，".join(out)


def emit(s: dict, neg: str, style: str, seam: str) -> str:
    n = s["n"]
    modern = s.get("modern_dress")
    lock = (TR_MODERN if modern else TR_LOCK) if s.get("onscreen", True) else TR_ABSENT
    o = [
        "---",
        "segment: %s" % s["segment"],
        "section: %s" % s["section"],
        "duration: %ds" % s["dur"],
        "scene: %s" % s["bg"],
        "view: %s" % view_key(s["view"]),
        "characters: [%s]" % ", ".join(s.get("chars", ["c5"])),
        "props: [%s]" % ", ".join(s.get("props", [])),
        "dialogue: %s" % ("yes" if s.get("lines") else "no"),
        "status: 已出prompt",
        "---",
        "",
        "# shot%02d · %s" % (n, s["title"]),
        "",
        "## Shot context",
        "",
        "- 景别档: %s%.2f → %s%.2f（机位 `%s` → `%s`）。**与前一镜的切口**：%s" % (
            s["jb"][1], s["jb"][0], s["jb"][3], s["jb"][2], s["jbcam"][0], s["jbcam"][1], seam),
        "- 衔接: %s" % ("承接 shot%02d 末帧（首帧＝上一镜末帧）" % s["handoff_from"]
                        if s.get("handoff_from") else "硬切（独立首帧）"),
    ]
    if s.get("handoff_to"):
        o.append("- 尾帧锁定: 本镜末帧是 shot%02d 的交接源；**重生时须用 `shot%02d_lastframe.png` 钉住末帧**"
                 % (s["handoff_to"], n))
    if s.get("facts"):
        o.append("- 史实: %s" % "、".join("`%s`" % f for f in s["facts"]))
    if s.get("note"):
        o.append("- 判断: %s" % s["note"])
    o += ["", "## 视频 prompt", "",
          FENCE + "text",
          "参考: " + refs_line(s),
          "参考用法: " + (USAGE if s.get("onscreen", True) else USAGE_ABSENT),
          "情节: `%s`" % s["plot"],
          "场景: `%s — %s`" % (s["bg"], scene_oneline(s["bg"])),
          "角色: `%s`" % lock,
          ]
    if s.get("props_lock"):
        o.append("道具: `%s`" % s["props_lock"])
    o += [
        "镜头: `%s`" % s["lens"],
        "走位: `%s`" % s["blocking"],
        "动作: `%s`" % s["action"],
    ]
    if s.get("lines"):
        o.append("台词:")
        for ln in s["lines"]:
            who = ln.get("speaker") or "妮娅"
            kind = ln["kind"]
            tail = "（对口型）" if kind == "对镜" else "（画外，嘴唇不动）" if kind == "画外" else "（对口型）"
            o.append("  - %s · %s%s: %s" % (who, kind, tail, ln["en"]))
    o += [
        "声音: `%s`；本镜人声由视频直接生成" % TR_VOICE,
        "摄影: `%s`" % PHOTO,
        "做旧: `%s`" % AGING,
        "光线: `%s`" % s["light"],
        "节奏: %s" % s["tempo"],
        "渲染样式: %s" % style,
        "比例: 16:9",
        "时长: %d秒" % s["dur"],
        "负面词: %s" % neg,
        FENCE,
        "",
    ]
    if s.get("lines"):
        o += ["## 台词配音 prompt", ""]
        for ln in s["lines"]:
            who = ln.get("speaker") or "妮娅"
            vid = ln.get("voice_id") or "c5 视频原声（补录 en-f-vlogger-nia-01）"
            o += [
                FENCE + "text",
                "角色: %s ｜ 音色(锁定·全站复用): `%s`" % (who, vid),
                "情绪: %s ｜ 语速: 中" % s.get("mood", "平稳"),
                "类型: %s%s ｜ 时间窗: %s" % (
                    ln["kind"], "（画外，嘴唇不动）" if ln["kind"] == "画外" else "",
                    ln.get("window", "全镜")),
                "台词: %s" % ln["en"],
                "时长目标: %.1fs" % (words(ln["en"]) / MAX_WPS),
                FENCE,
                "",
            ]
        if any(l.get("speaker") for l in s["lines"]):
            o += ["> **非旅行者台词的合法性**：" +
                  "；".join("%s ← %s" % (l["speaker"], l["source"])
                            for l in s["lines"] if l.get("speaker")), ""]
    return NL.join(o)


# ══════════════════════════════════════════════════════════════════════════════
# 闸门
# ══════════════════════════════════════════════════════════════════════════════

def seam_of(prev: dict | None, cur: dict) -> tuple[str, str | None]:
    """返回 (人读的切口说明, 违规原因或 None)。"""
    if prev is None:
        return "全片首镜", None
    if cur.get("handoff_from"):
        if prev["jbcam"][1] != cur["jbcam"][0] or tuple(prev["jb"][2:4]) != tuple(cur["jb"][0:2]):
            return "", "承接对 shot%02d→shot%02d 两端机位标签或景别档不一致" % (prev["n"], cur["n"])
        return "🔗 承接（I-14 豁免跳档）", None
    a, b = prev["jb"][2], cur["jb"][0]
    cam_differs = prev["jbcam"][1] != cur["jbcam"][0]
    if not cam_differs:
        return "", ("shot%02d→shot%02d 机位标签相同（`%s`）——切口不成立，不看比值（16.5 ①）"
                    % (prev["n"], cur["n"], prev["jbcam"][1]))
    if a <= 0.001 and b <= 0.001:
        return "✅ 两端皆无人（航拍/空镜），靠机位方位差成立", None
    if a <= 0.001 or b <= 0.001:
        return "✅ 一端无人一端有人，天然跳档", None
    r = max(a, b) / min(a, b)
    if r >= 2.0:
        return "✅ 比值 %.2f ≥ 2.0，机位亦不同" % r, None
    return "", ("shot%02d→shot%02d 人占画高比值 %.2f < 2.0（%.2f→%.2f），景别未跳档"
                % (prev["n"], cur["n"], r, a, b))


def gate(shots: list[dict], cards: dict[Path, str]) -> list[str]:
    bad: list[str] = []
    ns = [s["n"] for s in shots]
    if len(set(ns)) != len(ns):
        bad.append("镜号重复：%s" % [n for n in ns if ns.count(n) > 1])

    prev = None
    for s in shots:
        _, err = seam_of(prev, s)
        if err:
            bad.append(err)
        prev = s

    for path, text in cards.items():
        m = re.search(r"```text\n(.*?)\n```", text, flags=re.S)
        if m and len(m.group(1)) > MAX_PROMPT:
            bad.append("%s: 视频 prompt %d 字 > %d 硬顶" % (path.stem, len(m.group(1)), MAX_PROMPT))
        if HEX_RE.search(text):
            bad.append("%s: 出现 hex 颜色" % path.stem)
        for mm in SLOT_RE.finditer(text):
            bad.append("%s: `=>@` 后代填了槽位号 %r" % (path.stem, mm.group(0)))
        body = m.group(1) if m else ""
        if SUBTITLE_RE.search(body) and "无字幕" not in body:
            bad.append("%s: prompt 里出现字幕字样" % path.stem)

    for s in shots:
        budget = s["dur"] * BREATH
        used = sum(words(l["en"]) for l in s.get("lines", [])) / MAX_WPS
        if used > budget:
            bad.append("shot%02d: 台词需时 %.1fs > 镜长 %ds 的 80%%（%.1fs）——拆镜或精简"
                       % (s["n"], used, s["dur"], budget))
        for l in s.get("lines", []):
            if l.get("speaker") and not l.get("source"):
                bad.append("shot%02d: 非旅行者台词「%s」缺 fact_id 或「虚构人物·现代英语」标注（D2 闸门）"
                           % (s["n"], l["en"][:24]))

    by_shot = {p.stem: t for p, t in cards.items()}
    for i in prompt_light.check_drama(by_shot):
        if i.level == "blocker":
            bad.append("%s [%s] %s" % (i.shot, i.code, i.detail))
    return bad


# ══════════════════════════════════════════════════════════════════════════════

def build_shotlist(shots: list[dict]) -> str:
    o = ["# 分镜表 · 时空旅行 · 伦敦大火前一夜（sk3）", "",
         "> 由 `tools/gen_shots_sk3.py` 生成——**改表＝改 `tools/sk3_data/shots_*.toml` 重跑**。", "",
         "| # | 段 | 时长 | bg | 景别档 | 切口 | 标题 |", "|---|---|---|---|---|---|---|"]
    prev = None
    total = 0
    for s in shots:
        seam, _ = seam_of(prev, s)
        o.append("| %02d | %s | %ds | %s | %s%.2f→%s%.2f | %s | %s |" % (
            s["n"], s["segment"], s["dur"], s["view"],
            s["jb"][1], s["jb"][0], s["jb"][3], s["jb"][2], seam, s["title"]))
        total += s["dur"]
        prev = s
    o += ["", "**合计 %d 镜 · %d 秒（%.1f 分钟）**" % (len(shots), total, total / 60.0), ""]
    return NL.join(o)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    neg, style = load_shared()
    shots = load_shots()
    if not shots:
        print("没有镜表数据（tools/sk3_data/shots_*.toml），什么都没做")
        return 0

    cards: dict[Path, str] = {}
    prev = None
    for s in shots:
        seam, _ = seam_of(prev, s)
        cards[SHOTS_DIR / ("shot%02d" % s["n"]) / ("shot%02d.md" % s["n"])] = emit(s, neg, style, seam)
        prev = s

    problems = gate(shots, cards)
    if problems:
        for p in problems:
            print("BLOCKER", p)
        return 1

    if args.check:
        drift = [p.name for p, t in cards.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != t]
        if drift:
            print("DRIFT:", ", ".join(drift))
            return 1
        print("check ok — %d 镜与生成器一致" % len(cards))
        return 0

    for path, text in cards.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline=NL)
    (OUT).mkdir(parents=True, exist_ok=True)
    (OUT / "shotlist.md").write_text(build_shotlist(shots), encoding="utf-8", newline=NL)
    allp = ["# 全部分镜 prompt · sk3", "",
            "> 由 `tools/gen_shots_sk3.py` 生成，逐镜 `## 视频 prompt` 的 text 围栏原样汇总。", ""]
    for s in shots:
        t = cards[SHOTS_DIR / ("shot%02d" % s["n"]) / ("shot%02d.md" % s["n"])]
        m = re.search(r"```text\n(.*?)\n```", t, flags=re.S)
        allp += ["## shot%02d · %s" % (s["n"], s["title"]), "", FENCE + "text", m.group(1), FENCE, ""]
    (OUT / "all_shot_prompts.md").write_text(NL.join(allp), encoding="utf-8", newline=NL)

    total = sum(s["dur"] for s in shots)
    print("%d 镜 · %d 秒（%.1f 分钟）；shotlist.md 与 all_shot_prompts.md 已更新"
          % (len(shots), total, total / 60.0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
