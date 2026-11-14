# -*- coding: utf-8 -*-
"""分镜表演机检（chuanyue_yiri follow-up 054，filming.md「画面里的人不定格」）：只读 filming.json，报两类问题。

    python tools/filming_lint.py <集目录> [--scene s3]

1. 定格词：action / beats / blocking 里写了「一动不动」「愣住」「就那样盯着/看着」「僵住/僵在」「定住」「呆住」
   （前面有「不/不会/没有/别」的否定说法不算；「愣一下」这种瞬间反应不算）。
2. 听者空白：beats 里某一拍（「A–B秒 …」）超过 3 秒且有人说话，同一镜的其他有卡人物在这一拍里没被写到——
   模型会让他站成摆件（EP1 s3 st4 Felix）。
3. 缺看点（chuanyue_yiri follow-up 058）：每镜要有 point——这一镜要观众看懂或感到什么。
4. [动机] 对话里写了避而不看（头也不抬、眼睛只看手里、没有任何手势）：多半是为情节需要硬写的，抛开剧情人物为什么这么做？
5. [过演] 配角的反应写成大表情（张大嘴、瞪大眼、笑出声、鼓起腮帮、目瞪口呆…）：视频模型会演得更夸张，写成「微微 / 一下」或删掉这一拍。
7. [跨镜] 正文里提到别的镜头（接上一镜、下一镜她…、交给 st10）：模型看不到别的镜头，只会困惑（follow-up 067）。
6. [跨语言] Riley 对只说拉丁语的人只说一个词的问句（如 Garum?）：对方和观众都不知道她要什么——说完整意图并配手势。
（4–6 来自 chuanyue_yiri follow-up 062：EP1 s3 面包师头也不抬说 dextram、「Garum?」问得不明、面包师张嘴吸气的惊讶脸很傻。）
有问题时退出码 1。不调用任何服务。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FREEZE = re.compile(r"(?<![不别没])(?<!不会)(?<!没有)(一动不动|愣住|就那样(?:盯着|看着|站着)|僵住|僵在|(?<![不])定住|呆住|木在那)(?!不超过|一下|片刻)")
SEG = re.compile(r"(?:^|(?<=[；;。\n]))\s*(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*秒")   # 只认拍的开头，不认括号里的台词时间
SPEAK = re.compile(r"(说|问|喊|念|嘟囔|[A-Za-z]{3,}[^。；]*[.?!…])")


def cast_names(ep: Path) -> dict[str, list[str]]:
    chars = ep.parents[1] / "2_世界观人设" / "characters"
    out: dict[str, list[str]] = {}
    for d in chars.iterdir() if chars.is_dir() else []:
        m = re.match(r"(c\d+)_(.+)", d.name)
        if m and d.is_dir():
            out[m.group(1)] = [m.group(2)]
            card = d / f"{d.name}.md"             # 卡标题「# Vibia · 喷泉边接水的女人」：分镜里常用身份词（女人、面包师）指人
            if card.is_file():
                title = card.read_text(encoding="utf-8").splitlines()[0]
                role = title.split("·")[-1].strip() if "·" in title else ""
                for alias in (role, role[-2:] if len(role) > 2 else ""):
                    if alias and alias not in out[m.group(1)]:
                        out[m.group(1)].append(alias)
    out.setdefault("c1", ["Riley"])
    return out


def segments(beats: str) -> list[tuple[float, float, str]]:
    ms = list(SEG.finditer(beats))
    segs = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(beats)
        segs.append((float(m.group(1)), float(m.group(2)), beats[m.end():end]))
    return segs


CROSS_REF = re.compile(r"(接上一镜|上一镜|下一镜|前一镜|后一镜|交给\s*st\d+|st\d+\s*的(?:台词|动作|画面)|（接[^）]{0,6}镜）)")
AVOID = re.compile(r"(头也不抬|头一直低着|眼睛只看(?:着)?(?:托板|面包|手里|罐子|活)|看也不看|没有任何手势|没有任何朝向|不抬头)")
OVERACT = re.compile(r"(?<![不别没])(张大嘴|张嘴吸一口气|瞪大(?:了)?眼|大吃一惊|惊得|笑出声|捧腹|拍大腿|鼓起腮帮|目瞪口呆|笑弯了腰|使劲摇头|夸张地)")
ONE_WORD_Q = re.compile(r"Riley[^：:\n]*[：:]\s*([A-Za-z\-']+)\?\s*(?:$|/)", re.M)


def lint(ep: Path, only: str | None) -> list[str]:
    F = json.loads((ep / "filming.json").read_text(encoding="utf-8"))["content"]["scenes"]
    names = cast_names(ep)
    probs: list[str] = []
    for sc in F:
        if only and sc["id"] != only:
            continue
        for sh in sc["shots"]:
            key = f"{sc['id']} {sh['id']}"
            if not str(sh.get("point") or "").strip():      # follow-up 058：每镜写看点，审片拿它对照
                probs.append(f"{key} 没写看点（point）：一句话写这一镜要观众看懂或感到什么，画面里靠什么让人看懂")
            for field in ("action", "beats", "camera", "lighting", "blocking"):     # follow-up 067（审查 I54）：prompt 只写这一镜
                for m in CROSS_REF.finditer(sh.get(field) or ""):
                    probs.append(f"{key} [跨镜] [{field}] 「{m.group(1)}」：送给模型的正文只描述这一镜，别的镜头的事写进首帧和接点表，不进 prompt")
            dlg = sh.get("dialogue") or ""
            talk = len(set(re.findall(r"^\s*([^（(：:/\n]{1,20})[（(]", dlg, re.M) + re.findall(r"/\s*([^（(：:/]{1,20})[（(]", dlg))) >= 2
            for field in ("action", "beats"):
                text = sh.get(field) or ""
                if talk:
                    for m in AVOID.finditer(text):
                        probs.append(f"{key} [动机] [{field}] 对话里写了「{m.group(1)}」：抛开剧情，他为什么这么做？动机要来自人物"
                                     f"（手上真有急活、指的方向含糊、误会），不能只为让情节成立")
                others = [n for c in (sh.get("cast") or []) if c != "c1" for n in names.get(c, [])]
                for m in OVERACT.finditer(text):
                    before = text[max(0, m.start() - 20): m.start()]
                    near = text[max(0, m.start() - 8): m.end() + 10]
                    if re.search(r"喊|大声|说|念|叫|唱", near):
                        continue            # 喊话、说话时张嘴是台词的一部分
                    if not ("他" in before or any(n in before for n in others)):
                        continue            # 只管配角的反应；主持人对镜头笑、惊讶是 vlog 的表达
                    ctx = text[max(0, m.start() - 10): m.end() + 8].replace("\n", " ")
                    probs.append(f"{key} [过演] [{field}] 「{m.group(1)}」：模型会演得更夸张——写成「微微 / 一下」或删掉这一拍：…{ctx}…")
            gesture = re.search(r"(举着|举起|指着|指向|朝[^。；]{0,6}一指|比划|递给|递过去|摊开手)[^。；]{0,30}(问|说)|(问|说)[^。；]{0,12}(举着|举起|指着|指向|一指|比划)",
                                (sh.get("action") or "") + (sh.get("beats") or ""))
            if "拉丁语" in dlg and not gesture:             # 一个词加上手势（举着面包问）意思是清楚的
                for m in ONE_WORD_Q.finditer(dlg):
                    probs.append(f"{key} [跨语言] Riley 对只说拉丁语的人只问一个词「{m.group(1)}?」：对方和观众都不知道她要什么——"
                                 f"说出完整意图并配手势（指、比划），回答也要让观众看懂")
            for field in ("action", "beats", "blocking"):
                for m in FREEZE.finditer(sh.get(field) or ""):
                    ctx = (sh[field][max(0, m.start() - 14): m.end() + 10]).replace("\n", " ")
                    probs.append(f"{key} [{field}] 定格词「{m.group(1)}」：…{ctx}…")
            cast = [c for c in (sh.get("cast") or []) if c in names]
            spoken = {}                                    # 台词行「Riley（…）：Okay… I …」→ {Riley: 前 10 个字}
            for m in re.finditer(r"([A-Za-z]+)（[^）]*）：\s*([^/]+)", sh.get("dialogue") or ""):
                spoken[m.group(1)] = m.group(2).strip()[:10]
            if len(cast) < 2:
                continue
            for a, b, text in segments(sh.get("beats") or ""):
                if b - a <= 3 or not SPEAK.search(text):
                    continue
                speakers = [c for c in cast if any(spoken.get(n, "") and spoken[n] in text for n in names[c])]
                if not speakers and "说" in text:          # 「她说…」「他说…」：说话人用代词指，按台词行里第一个说话人算
                    speakers = [c for c in cast if any(n in spoken for n in names[c])][:1]
                for c in cast:
                    if c in speakers:
                        continue
                    if not any(n in text for n in names[c]):
                        probs.append(f"{key} {a:g}–{b:g} 秒（{b - a:g} 秒有人说话）：{names[c][0]}（{c}）在这一拍没写动作——听的人要有手上的活和钉在词上的反应")
    return probs


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", type=Path)
    ap.add_argument("--scene")
    a = ap.parse_args()
    probs = lint(a.episode.resolve(), a.scene)
    for p in probs:
        print("  ✗", p)
    print(f"{a.episode.as_posix()}：{'分镜表演机检通过' if not probs else f'{len(probs)} 处要看'}")
    return 1 if probs else 0


if __name__ == "__main__":
    raise SystemExit(main())
