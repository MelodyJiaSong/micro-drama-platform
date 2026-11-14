"""西幻新剧开发稿的形式检查（框架 v0.4，系列级试点）。

    python ai_videos/xihuan/framework/check.py ai_videos/xihuan/{剧}/0_开发 [--json]

--json 另把结果写进该目录的 _check.json（管理 UI 的开发稿预览页读取）。

必填小节从 templates/ 里各页「## 必填小节」下的 ### 标题读取（模板是唯一定义处）；开发稿里写成 ## 标题。
不通过：缺页、缺小节（只有表头也算缺）、篇幅超限、表格超过 12 行、库 ID 不存在、种族与势力某行没有库映射、
图里的名称或编号没在表里定义（关系图、人物关系图、矛盾图；矛盾图一端可以是力量源，如魔戒）、矛盾图没有主要矛盾、人物能力缺行或分数不是 1–5、出现季 / 集概念。
提示：秘密的「何时揭开」没写故事阶段。只查形式，不判断写得好不好。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parent
TEMPLATES = FRAMEWORK / "templates"
LIBRARY = FRAMEWORK.parents[1] / "_shared" / "xihuan" / "library.json"
REQUIRED_PAGES = ["01_主题", "02_世界", "03_力量", "04_人物", "05_矛盾"]
OPTIONAL_PAGES = ["06_秘密与伏笔", "07_观众与爽点"]
THEME_LIMITS = {"一句话": 40, "一段": 200, "一页": 1000}
LOGLINE_WORDS = 35
PAGE_PROSE_LIMIT = 300
TABLE_ROWS_LIMIT = 12
STAGES = ["开端", "大转折一", "中点", "大转折二", "高潮", "结局"]
UNMAPPED = ("原创", "库外")
# 汉字旁 \b 不生效（Python 把汉字算作单词字符），编号边界只看拉丁字母与数字。
EDGE_L, EDGE_R = r"(?<![A-Za-z0-9])", r"(?![A-Za-z0-9])"
LIB_ID = re.compile(EDGE_L + r"(?:PL|PS|SC|EL|HL|DK|PR|AU|GD|TR|PH|EV|FL|TL|CL|RC|RS|GF|GR|IR|CF|IT|MT|OR|BS)\d{2}" + EDGE_R)
PERSON = re.compile(EDGE_L + r"P\d+" + EDGE_R)
# 季与集是下一步（故事创作）的事，开发稿里出现就拦（用户 2026-11-08，xihuan follow-up 002）
SEASON_EPISODE = re.compile(r"第\s*[一二三四五六七八九十\d]+\s*[季集]|[每本上下前后首末]季|[每单本首末]集|集长|集数|季末|季初|季中|分集|"
                            r"S\d{1,2}E\d{1,2}|(?<![A-Za-z0-9])S\d{1,2}(?![A-Za-z0-9])|(?<![\d.])\d{1,2}-\d{2}(?!\d)")


def required_sections(page: str) -> list[str]:
    text = (TEMPLATES / f"{page}.md").read_text(encoding="utf-8")
    block = text.split("## 必填小节", 1)[1].split("\n## ", 1)[0]
    return re.findall(r"^### (.+?)\s*$", block, re.M)


def sections(text: str) -> dict[str, str]:
    parts = re.split(r"^## (.+?)\s*$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def prose_chars(text: str) -> int:
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith(("|", "#", "<!--", "```"))]
    return len(re.sub(r"[\s*_>`#\-]", "", "".join(lines)))


def table(section: str) -> list[list[str]]:
    """第一张表的数据行（去掉表头与分隔行），每行拆成单元格。"""
    rows = [ln for ln in section.splitlines() if ln.lstrip().startswith("|")]
    cells = [[c.strip().strip("*").strip() for c in r.strip().strip("|").split("|")] for r in rows]
    return [c for i, c in enumerate(cells) if i > 0 and not all(re.fullmatch(r":?-+:?", x or "-") for x in c)]


def filled(section: str) -> bool:
    prose = [ln for ln in section.splitlines() if ln.strip() and not ln.lstrip().startswith("|")]
    return bool(prose) or bool(table(section))


def check(folder: Path, warnings: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    warnings = [] if warnings is None else warnings
    library_ids = {a["id"] for a in json.loads(LIBRARY.read_text(encoding="utf-8"))["assets"]}
    texts = {p: (folder / f"{p}.md").read_text(encoding="utf-8") for p in REQUIRED_PAGES + OPTIONAL_PAGES if (folder / f"{p}.md").is_file()}
    errors += [f"缺页：{p}.md" for p in REQUIRED_PAGES if p not in texts]
    parsed = {p: sections(t) for p, t in texts.items()}
    for p, secs in parsed.items():
        for name in required_sections(p):
            if not filled(secs.get(name, "")):
                errors.append(f"{p}：缺小节或为空「## {name}」（只有表头也算空）")
        for name, sec in secs.items():
            if len(table(sec)) > TABLE_ROWS_LIMIT:
                errors.append(f"{p}「{name}」{len(table(sec))} 行，超过 {TABLE_ROWS_LIMIT}")
        unknown = sorted(set(LIB_ID.findall(texts[p])) - library_ids)
        if unknown:
            errors.append(f"{p}：库里没有这些 ID {unknown}")
        found = sorted({m.group(0) for m in SEASON_EPISODE.finditer(texts[p])})
        if found:
            errors.append(f"{p}：出现季 / 集概念 {found[:6]}——只用故事阶段（{'、'.join(STAGES)}）；若是数值范围请写成 5–10")
        if p == "01_主题":
            for name, limit in THEME_LIMITS.items():
                n = prose_chars(secs.get(name, ""))
                if n > limit:
                    errors.append(f"01_主题「{name}」{n} 字，超过 {limit}")
            words = len(re.findall(r"[A-Za-z']+", secs.get("英文 logline", "")))
            if words > LOGLINE_WORDS:
                errors.append(f"01_主题「英文 logline」{words} 词，超过 {LOGLINE_WORDS}")
        elif prose_chars(texts[p]) > PAGE_PROSE_LIMIT:
            errors.append(f"{p}：正文 {prose_chars(texts[p])} 字，超过 {PAGE_PROSE_LIMIT}（表格不计）")
    graphs(parsed, texts, errors, warnings)
    return errors


def graphs(parsed: dict[str, dict[str, str]], texts: dict[str, str], errors: list[str], warnings: list[str]) -> None:
    """图要画得出来：每条边的两端都在表里定义过。"""
    world = parsed.get("02_世界", {})
    groups = table(world.get("种族与势力", ""))
    names = {r[0] for r in groups if r and r[0]}
    for r in groups:
        if not LIB_ID.search(" ".join(r)) and not any(w in " ".join(r) for w in UNMAPPED):
            errors.append(f"02_世界「种族与势力」{r[0]} 没有库 ID，也没标「原创」")
    for r in table(world.get("关系", "")):
        for end in (r[0], r[2] if len(r) > 2 else ""):
            if end and end not in names:
                errors.append(f"02_世界「关系」里的「{end}」不在种族与势力表中")
    people = table(parsed.get("04_人物", {}).get("人物", ""))
    pids = {r[0] for r in people if r and PERSON.fullmatch(r[0])}
    if "04_人物" in parsed and people and "P01" not in pids:
        errors.append("04_人物「人物」第一列要用编号，P01 是主角")
    for r in table(parsed.get("04_人物", {}).get("关系", "")):
        for end in (r[0], r[2] if len(r) > 2 else ""):
            if end and end not in pids:
                errors.append(f"04_人物「关系」里的「{end}」不是人物表里的编号")
    abilities = table(parsed.get("04_人物", {}).get("能力", ""))
    for r in abilities:
        if r[0] not in pids:
            errors.append(f"04_人物「能力」里的「{r[0]}」不是人物表里的编号")
        for col, i in (("外", 2), ("内", 4)):
            if not re.fullmatch(r"[1-5]", r[i] if len(r) > i else ""):
                errors.append(f"04_人物「能力」{r[0]} 的「{col}」要打 1–5 的整数分")
    if abilities:
        lacking = sorted(pids - {r[0] for r in abilities})
        if lacking:
            errors.append(f"04_人物「能力」缺这些人物 {lacking}")
    powers = {r[0] for r in table(parsed.get("03_力量", {}).get("力量源", "")) if r and r[0]}
    conflicts = table(parsed.get("05_矛盾", {}).get("矛盾图", ""))
    for r in conflicts:
        for end in (r[0], r[2] if len(r) > 2 else ""):
            if end and end not in pids and end not in names and end not in powers:
                errors.append(f"05_矛盾「矛盾图」里的「{end}」不是人物编号、世界页的种族或势力，也不是力量页的力量源")
    if conflicts and not any(len(r) > 3 and r[3].startswith("主") for r in conflicts):
        errors.append("05_矛盾「矛盾图」至少一行的「主次」写「主」")
    for p, t in texts.items():
        missing = sorted(set(PERSON.findall(t)) - pids) if "04_人物" in parsed else []
        if missing:
            errors.append(f"{p}：引用了人物表里没有的编号 {missing}")
    for r in table(parsed.get("06_秘密与伏笔", {}).get("秘密", "")):
        if len(r) > 2 and not any(s in r[2] for s in STAGES):
            warnings.append(f"06_秘密与伏笔「{r[0]}」的「何时揭开」没写故事阶段（{'、'.join(STAGES)}）")


def metrics(folder: Path) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for p in REQUIRED_PAGES + OPTIONAL_PAGES:
        f = folder / f"{p}.md"
        if not f.is_file():
            out[p] = {"exists": False, "required": p in REQUIRED_PAGES}
            continue
        text = f.read_text(encoding="utf-8")
        secs = sections(text)
        entry: dict[str, object] = {"exists": True, "required": p in REQUIRED_PAGES, "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                                    "missing_sections": [n for n in required_sections(p) if not filled(secs.get(n, ""))]}
        if p == "01_主题":
            entry["limits"] = {n: {"chars": prose_chars(secs.get(n, "")), "limit": lim} for n, lim in THEME_LIMITS.items()}
        else:
            entry["limits"] = {"正文": {"chars": prose_chars(text), "limit": PAGE_PROSE_LIMIT}}
        out[p] = entry
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--json"]
    if len(args) != 1:
        raise SystemExit(__doc__)
    folder = Path(args[0])
    warnings: list[str] = []
    errors = check(folder, warnings)
    if "--json" in sys.argv:
        report = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "ok": not errors, "errors": errors,
                  "warnings": warnings, "pages": metrics(folder)}
        (folder / "_check.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\n".join(errors) if errors else f"{folder}：形式检查通过")
    if warnings:
        print("提示：\n" + "\n".join(warnings))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
