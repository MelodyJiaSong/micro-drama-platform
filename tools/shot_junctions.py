# -*- coding: utf-8 -*-
"""镜间接点表与机检（chuanyue_yiri follow-up 056，filming.md「镜与镜接得上」）：只读 filming.json，不调用任何服务。

    python tools/shot_junctions.py <集目录> [--scene s1] [--out junctions.md] [--before <旧 filming.json>]

按播放顺序列出每个接点（同场相邻两镜，以及上一场最后一镜 → 下一场第一镜）：
上一镜的视角来源、最后一拍、最后一句台词 ↔ 下一镜的视角来源、第 0 秒、第一拍、第一句台词。审稿人逐个接点判，
写分镜的人保存前自己连起来读一遍。

机检（同场接点；场间接点只列表不报，场间转场归 edit.scene_joins）。⚠＝「同一刻里重新开场」类疑点，计入退出码：
1. 重新打招呼：同一个人上一镜已经在说话，下一镜第一句又是 Hi / Hello / Good morning / Welcome 之类的开场问候。
2. 重复信息：下一镜第一句重复上一镜最后两句里的专名（地点、人名），同一个说话人。
3. 情绪跳变：同一个说话人，上一镜的说话方式是小声 / 惊叹 / 发喘 / 哽咽一类，下一镜第一句是兴奋 / 欢快 / 大声一类，
   而接点两侧都没写转变的动作或台词（喘口气、笑出来、定定神、清清嗓子……）。
上一镜结尾写明「重新开录」（台词里 do this right / start over，或 beats 里「重新开录」）时 1、2 不报——那是有意的重开。
ℹ＝视角来源切换（自拍 ↔ 他拍 / 架着的相机），两侧都没写交代（拿起、放下、架好、递给相机……）：只提示，审稿人按本剧视角约定判；
和 ⚠ 同时出现时最可疑（EP1 s1 st1→st2：他拍全景里低声惊叹 → 自拍里欢快地重新开场）。
报出的接点不一定都错——是戏就在下一镜开头写明理由；有 ⚠ 时退出码 1。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEG = re.compile(r"(?:^|(?<=[；;。\n]))\s*(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*秒")
SELFIE = re.compile(r"自拍|举着(?:相机|手机|镜头)|伸直[左右]?臂持镜|手持自拍")
OTHER = re.compile(r"他拍|架(?:在|着|好)[^。；]{0,8}(?:相机|镜头)|三脚架|别人(?:拿着|举着)|有人(?:拿着|举着)?拍|客观镜头|固定机位")
HANDOFF = re.compile(r"(?:拿起|拿过|抓起|抓向镜头|接过|递给|递过|放下|架(?:在|好|上)|立在|搁在|举起)[^。；]{0,10}(?:相机|镜头|手机)|手掌挡满画面|(?:相机|镜头|手机)[^。；]{0,6}(?:被拿起|拿起来|放下|架好)")
GREET = re.compile(r"^\W*(hi|hey|hello|good (?:morning|afternoon|evening)|welcome|what'?s up)\b", re.I)
SOFT = re.compile(r"小声|低声|悄悄|轻声|发喘|半喘|喘|惊叹|不敢相信|哽咽|愣|发抖|颤")
LOUD = re.compile(r"兴奋|欢快|大声|热情|元气|活泼|主持")
SHIFT = re.compile(r"喘(?:口|出一口)气|笑出来|笑出声|定定神|深吸一口气|清清嗓|整理一下|回过神|重新开录|调整一下情绪|镇定下来")
SENT = re.compile(r"[^.?!…]+[.?!…]+[\"”’']?")
PROPER = re.compile(r"\b[A-Z][a-z]{3,}\b")
COMMON = {"Okay", "Yeah", "Like", "That", "This", "There", "Those", "These", "What", "When", "Where", "Good", "Well",
          "Wait", "Look", "Just", "Really", "Right", "Sorry", "Thanks", "Thank", "Here", "Hello", "Morning", "Also", "Actually",
          "Literally", "Seriously", "Anyway", "Maybe", "Could", "Would", "Should", "They", "Then", "Yes", "Nope", "Gonna"}


def segments(beats: str) -> list[tuple[float, float, str]]:
    ms = list(SEG.finditer(beats or ""))
    return [(float(m.group(1)), float(m.group(2)), beats[m.end():(ms[i + 1].start() if i + 1 < len(ms) else len(beats))].strip(" ；;。"))
            for i, m in enumerate(ms)]


def speech(dialogue: str) -> list[tuple[str, str, str]]:
    """「Riley（说法）：台词」→ [(说话人, 说法, 台词)]；台词里括号内的舞台说明去掉。"""
    out = []
    for ln in (dialogue or "").splitlines():
        m = re.match(r"\s*([^（(：:]{1,20})\s*[（(](.*?)[）)]\s*[：:]\s*(.+)", ln) or re.match(r"\s*([^：:]{1,20})\s*[：:]\s*(.+)", ln)
        if not m:
            continue
        who, how, text = (m.group(1), m.group(2), m.group(3)) if m.lastindex == 3 else (m.group(1), "", m.group(2))
        out.append((who.strip(), how, re.sub(r"[（(][^）)]*[）)]", " ", text).strip()))
    return out


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENT.findall(text)] or ([text.strip()] if text.strip() else [])


def source(spec: dict) -> str:
    cam = str(spec.get("camera", ""))
    head = re.split(r"[。；]", cam, maxsplit=1)[0] + str(spec.get("action", ""))[:12]
    if SELFIE.search(head):
        return "自拍"
    if OTHER.search(head):
        return "他拍"
    return "他拍" if OTHER.search(cam) else ("自拍" if SELFIE.search(cam) else "未写")


def ends(spec: dict) -> dict:
    segs = segments(str(spec.get("beats", "")))
    action = str(spec.get("action", ""))
    m = re.search(r"第\s*0\s*秒[：:](.+)$", action)
    said = speech(str(spec.get("dialogue", "")))
    first_who, first_how, first_text = said[0] if said else ("", "", "")
    last_who, last_how, last_text = said[-1] if said else ("", "", "")
    return {"source": source(spec), "start": (m.group(1).strip() if m else ""), "first_beat": segs[0][2] if segs else "",
            "last_beat": segs[-1][2] if segs else "", "first_who": first_who, "first_how": first_how,
            "first_line": (sentences(first_text) or [""])[0], "last_who": last_who, "last_how": last_how,
            "last_lines": sentences(last_text)[-2:], "action": action, "camera": str(spec.get("camera", "")),
            "said_tail": str(spec.get("dialogue", ""))[-160:], "said_head": str(spec.get("dialogue", ""))[:160]}


RESTART = re.compile(r"重新开录|重新开始|do (?:this|it) right|start over|from the top|take two", re.I)


def check(a: dict, b: dict) -> tuple[list[str], list[str]]:
    flags, notes = [], []
    tail = a["last_beat"] + a["action"][-200:] + a["said_tail"]    # 台词里的括号舞台说明（笑出来、边走边说）也算交代
    head = b["start"] + b["first_beat"] + b["action"][:200] + b["camera"][:120] + b["said_head"]
    if {a["source"], b["source"]} == {"自拍", "他拍"} and not (HANDOFF.search(tail) or HANDOFF.search(head)):
        notes.append(f"视角来源切换（{a['source']} → {b['source']}），两侧没写谁拿起 / 放下 / 架好相机——按本剧视角约定判")
    same = a["last_who"] and a["last_who"] == b["first_who"]
    restart = bool(RESTART.search(tail + b["first_how"] + " ".join(a["last_lines"])))
    if same and not restart and GREET.search(b["first_line"]):
        flags.append(f"重新打招呼：{b['first_who']} 上一镜已经在说话，下一镜第一句又是开场问候「{b['first_line']}」")
    if same and not restart:
        prev = {w for s in a["last_lines"] for w in PROPER.findall(s)} - COMMON
        rep = sorted(w for w in set(PROPER.findall(b["first_line"])) - COMMON if w in prev)
        if rep:
            flags.append(f"重复信息：下一镜第一句又说 {'、'.join(rep)}（上一镜最后两句刚说过）")
    if same:
        if SOFT.search(a["last_how"]) and LOUD.search(b["first_how"]) and not (SHIFT.search(tail) or SHIFT.search(head)):
            flags.append(f"情绪跳变：「{a['last_how'][:24]}」→「{b['first_how'][:24]}」，接点两侧没写转变的动作或台词")
    if flags and notes:
        flags.append("同时视角来源也切换了：像换了一台相机重新开场")
    return flags, notes


def junctions(ep: Path, only: str | None = None, filming: Path | None = None) -> tuple[list[str], int]:
    return table(json.loads((filming or ep / "filming.json").read_text(encoding="utf-8"))["content"]["scenes"], only)


def table(scenes: list[dict], only: str | None = None) -> tuple[list[str], int]:
    """scenes＝filming.json content.scenes（或审查单快照里同样结构的场列表，按播放顺序）。"""
    order = [(sc["id"], sh) for sc in scenes for sh in sc["shots"]]
    rows = ["# 镜间接点表", "",
            "按播放顺序：上一镜结尾 ↔ 下一镜开头。逐个接点判：位置朝向、手里的东西、视角来源（谁在拍）、表演与情绪、台词是不是同一个人接着说。",
            "⚠ 是机检报出的「重新开场」类疑点、ℹ 是视角来源切换提示（`tools/shot_junctions.py`），审稿人复核；没有标记的接点也要看。", ""]
    bad = 0
    for (sa, a), (sb, b) in zip(order, order[1:]):
        if only and only not in (sa, sb):
            continue
        ea, eb = ends(a), ends(b)
        cross = sa != sb
        flags, notes = ([], []) if cross else check(ea, eb)
        bad += bool(flags)
        rows += [f"## {sa}_{a['id']} → {sb}_{b['id']}" + ("（场间接点，转场另审）" if cross else ""), "",
                 f"- 上一镜结尾：视角 **{ea['source']}**；最后一拍：{ea['last_beat'] or '（beats 没分拍）'}",
                 f"  - 最后的台词：{(ea['last_who'] + '（' + ea['last_how'][:40] + '）：' + ' '.join(ea['last_lines'])) if ea['last_lines'] else '（无）'}",
                 f"- 下一镜开头：视角 **{eb['source']}**；第 0 秒：{eb['start'] or '（action 没写第 0 秒）'}",
                 f"  - 第一拍：{eb['first_beat'] or '（beats 没分拍）'}",
                 f"  - 第一句台词：{(eb['first_who'] + '（' + eb['first_how'][:40] + '）：' + eb['first_line']) if eb['first_line'] else '（无）'}",
                 *[f"- ⚠ {f}" for f in flags], *[f"- ℹ {n}" for n in notes], ""]
    return rows, bad


def main() -> int:
    ap = argparse.ArgumentParser(description="镜间接点表与机检")
    ap.add_argument("episode")
    ap.add_argument("--scene")
    ap.add_argument("--out")
    ap.add_argument("--filming", help="用另一份 filming.json（比如改前备份）跑")
    a = ap.parse_args()
    ep = Path(a.episode)
    rows, bad = junctions(ep, a.scene, Path(a.filming) if a.filming else None)
    text = "\n".join(rows)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    flagged = [r for r in rows if r.startswith("## ") or r.startswith("- ⚠")]
    show = [r for i, r in enumerate(flagged) if r.startswith("- ⚠") or (i + 1 < len(flagged) and flagged[i + 1].startswith("- ⚠"))]
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(show) if show else "接点机检：没有疑点")
    info = sum(r.startswith("- ℹ") for r in rows)
    print(f"{ep}：{sum(r.startswith('## ') for r in rows)} 个接点，{bad} 个有 ⚠ 疑点，{info} 个视角切换提示（见全表）" + (f"；全表 → {a.out}" if a.out else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
