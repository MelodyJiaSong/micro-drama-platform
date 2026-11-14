# -*- coding: utf-8 -*-
"""补图后就地更新发布稿里的图片署名（paihangbang follow-up 058）。

    python ai_videos/paihangbang/_tools/regate_publish.py <ep_dir> <key> [<key> ...]

发布稿生成后有人工润色（finish_publish.py 等），不整篇重生成：只改这些卡在署名段里的行（保留行首原有的
「#R Name (…): 」前缀，只换冒号后的正文），并按署名段实际 AI 行数改「N images marked AI-generated」/
「片中有N张标注」，重算各节字符数。
publish.md：Description 的短署名与 Comment 里的完整署名；publish.zh.md：「图片署名（作者，授权）」段。
合成内容声明（Yes / No）若因此变化，打印提示，由人改清单那一行。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from regate_apply import tile_key  # noqa: E402

AI_SHORT = "AI-generated illustration (Codex image_gen)"
AI_ZH = "AI-generated（AI生成插画，非实拍）"
SHORT_HEAD = re.compile(r"^Image credits \(")
FULL_HEAD = re.compile(r"^Full (?:image|photo) credits \(")
ZH_HEAD = re.compile(r"^图片署名（作者，授权）")
AI_COUNT = re.compile(r"\b\d+ images? marked AI-generated (?:are illustrations|is an illustration)")


def default_image(it: dict) -> str:
    return it["image_alt"] if it.get("image_risk") and it.get("image_alt") else it["image"]


def lines_for(ep: Path, keys: list[str]) -> list[tuple[str, str, str, str, str]]:
    """(英文键「#R Name」, 中文键「第R名 名称」, 短署名正文, 完整署名正文, 中文署名正文)。"""
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    zh = json.loads((ep / "data.zh.json").read_text(encoding="utf-8")) if (ep / "data.zh.json").is_file() else None
    ledger = {a["file"]: a for a in json.loads((ep / "assets.json").read_text(encoding="utf-8"))}
    out = []
    for i, it in enumerate(data["items"]):
        if tile_key(i, it) not in keys:
            continue
        a = ledger[default_image(it)]
        en = f"#{it['rank']} {it['name']}"
        zp = f"第{it['rank']}名 {zh['items'][i]['name'] if zh else it['name']}"
        if a["licence"].lower().startswith("ai-generated"):
            out.append((en, zp, AI_SHORT, AI_SHORT + ", not a photo", AI_ZH))
        else:
            link = f" {a['licence_url']}" if a.get("licence_url") else ""
            out.append((en, zp, f"{a['author']} ({a['licence']})", f"{a['author']}, {a['licence']}{link} — {a['source_page']}",
                        f"{a['author']}（{a['licence']}）"))
    return out


def section(text: str, header: re.Pattern) -> list[tuple[int, str]]:
    """header 行之后、到空行或代码块结束为止的行（行号, 内容）。"""
    lines, out, inside = text.split("\n"), [], False
    for i, line in enumerate(lines):
        if header.search(line):
            inside = True
            continue
        if inside and (not line.strip() or line.startswith("```")):
            inside = False
        if inside:
            out.append((i, line))
    return out


RANK = re.compile(r"^(?:#|第)(\d+)")


def patch(text: str, bodies: dict[str, str], header: re.Pattern, sep: str) -> tuple[str, int]:
    """署名段里以「键:」或「键 (…):」开头的行：保留原前缀，换正文。
    段里没有这张卡的行（原来是无图卡）就按名次插到对应位置。"""
    lines, n = text.split("\n"), 0
    sec = section(text, header)
    found: set[str] = set()
    for i, line in sec:
        for key, body in bodies.items():
            rest = line[len(key):]
            if line.startswith(key) and sep in rest and (rest.startswith(sep) or rest.startswith(" (") or rest.startswith("（")):
                found.add(key)
                new = line[:len(key) + rest.index(sep) + len(sep)] + body
                if new != line:
                    lines[i], n = new, n + 1
    if not sec:
        return "\n".join(lines), n
    inserts: list[tuple[int, str]] = []
    for key, body in bodies.items():
        if key in found:
            continue
        rank = int(RANK.match(key).group(1))
        at = sec[0][0]                                   # 默认插在段首
        for i, line in sec:
            m = RANK.match(line)
            if m and int(m.group(1)) <= rank:
                at = i + 1
        inserts.append((at, key + sep + body))
    for at, new in sorted(inserts, key=lambda x: -x[0]):
        lines.insert(at, new)
        n += 1
    return "\n".join(lines), n


def recount(text: str) -> str:
    def fix(m: re.Match) -> str:
        return f"{m.group(1)}{len(m.group(3))}{m.group(2)}{m.group(3)}"
    return re.sub(r"(## [^\n]*?（(?:置顶）（)?)\d+( 字符）\n\n```text\n)(.*?)(?=\n```)", fix, text, flags=re.S)


def main() -> None:
    ep, keys = Path(sys.argv[1]).resolve(), sys.argv[2:]
    rows = lines_for(ep, keys)
    p = ep / "publish.md"
    t = p.read_text(encoding="utf-8")
    t, a = patch(t, {r[0]: r[2] for r in rows}, SHORT_HEAD, ": ")
    t, b = patch(t, {r[0]: r[3] for r in rows}, FULL_HEAD, ": ")
    ai = sum("AI-generated" in line for _, line in section(t, SHORT_HEAD))
    t = AI_COUNT.sub(f"{ai} image{'' if ai == 1 else 's'} marked AI-generated {'is an illustration' if ai == 1 else 'are illustrations'}", t)
    desc = re.search(r"## Description（(\d+) / 5000 字符）\n\n```text\n(.*?)\n```", t, flags=re.S)
    if desc:
        t = t.replace(desc.group(0), desc.group(0).replace(f"（{desc.group(1)} / 5000", f"（{len(desc.group(2))} / 5000", 1))
    t = recount(t)
    p.write_text(t, encoding="utf-8")
    print(f"publish.md：短署名 {a} 行、完整署名 {b} 行；描述里 AI 图 {ai} 张")
    zp = ep / "publish.zh.md"
    if zp.is_file():
        z = zp.read_text(encoding="utf-8")
        z, c = patch(z, {r[1]: r[4] for r in rows}, ZH_HEAD, "：")
        zai = sum("AI生成插画" in line for _, line in section(z, ZH_HEAD))
        z = re.sub(r"片中有\d+张标注", f"片中有{zai}张标注", z)
        zp.write_text(z, encoding="utf-8")
        print(f"publish.zh.md：署名 {c} 行；AI 图 {zai} 张")
    yes = re.search(r"synthetic content[^\n]*选 \**Yes", t)
    if ai and not yes:
        print("⚠ 现在有 AI 图，但 publish.md 的合成内容声明不是「选 Yes」：改清单那一行")
    if not ai and yes:
        print("⚠ 现在没有 AI 图，但 publish.md 的合成内容声明是「选 Yes」：改成 No，并删描述里的 AI 说明")


if __name__ == "__main__":
    main()
