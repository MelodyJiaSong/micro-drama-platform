# -*- coding: utf-8 -*-
"""教学视频审查：第一层「程序检验」。约定见 edu_videos/README.md「审查」。

    python tools/edu_review.py validate <知识点目录> [--lang zh|en|all]   程序检验 → reviews/validate.md（全绿才往下审）
    python tools/edu_review.py brief <知识点目录> --stage script|cut      开一轮审稿：材料 + 每个角色的任务书 → reviews/<阶段>_rN/
    python tools/edu_review.py merge <审稿目录>                          汇总各角色报告 → issues.md（按句号排，标出多人同指的问题）
    python tools/edu_review.py new <知识点目录> [--after <上一轮>]       台词审 v2：口播＋屏幕文字 × 中英，各两位独立审（Claude＋Codex）→ reviews/lines_rN/
    python tools/edu_review.py check <lines_rN>                          校验报告格式与证据、对比两位评分、出裁决任务书
    python tools/edu_review.py issues <lines_rN>                         汇总 → issues.json / issues.md（编号 I1…、各项最终分、通过与否）
    python tools/edu_review.py fix <lines_rN> (--ids I3,I7 | --item screen_zh --where l47,agenda) --status implemented|wontfix --solution "…" [--reason …] [--file …]
    python tools/edu_review.py conclude <lines_rN> [--note …]          收轮 → 结果.md、状态「已收轮」；下一轮 new 自动带上一轮的处理复核

审稿角色与必查项：edu_videos/_shared/review/roles.json；流程：edu_videos/README.md「审查」。

查什么（每条都能机器判，不靠人看）：
  配音    每句回听错率、语速在范围内（读 tools/edu_video.py qa 存的 .words.json）
  字幕    每屏字数、停留时间、阅读速度、短碎片
  节奏    全片与各段的语速（中文字/分、英文词/分）；开口前的空白；首个问题出现的时刻
  画面    渲染日志里的 [layout]（出画面、压字幕带、文字重叠）与 [cue]（动画迟到 / 超出配音）
  事实    讲稿里带数字、百分比、引号的句子，都要在 claims.json 里登记出处（实验算出的写 source: "experiment"）
  成片    时长与时间轴一致、整体响度 −18～−14 LUFS
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import edu_video as ev  # noqa: E402

# 阈值：中文参考 B 站科普 ≈220–280 字/分；英文参考 StatQuest / 3B1B 140–190 词/分（benchmark 2026-11-08）
PACE = {"zh": (200, 300), "en": (130, 185)}
SUB_SPEED = {"zh": 9.0, "en": 21.0}          # 字幕阅读上限：中文字/秒，英文字符/秒
SUB_MIN_DUR = 0.9
SUB_MAX = {"zh": ev.SUB_MAX + 2, "en": ev.SUB_MAX_EN + 10}
HOOK_BY = 20.0                                # 开片多少秒内要抛出问题
LUFS = (-18.0, -14.0)
FACT_RE = re.compile(r"\d|%|％|百分之|倍|“|\"|[零一二三四五六七八九十百千万亿]{2,}(?:年|周|次|个|万|亿|倍)")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []      # (级别, 类, 位置, 说明)

    def add(self, level: str, kind: str, where: str, msg: str) -> None:
        self.rows.append((level, kind, where, msg))

    @property
    def blockers(self) -> int:
        return sum(r[0] == "必改" for r in self.rows)


def srt_rows(path: Path) -> list[tuple[float, float, str]]:
    out = []
    for block in path.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        a, b = (sum(float(x) * m for x, m in zip(re.split(r"[:,]", t.strip())[:3], (3600, 60, 1))) +
                int(re.split(r"[:,]", t.strip())[3]) / 1000 for t in lines[1].split("-->"))
        out.append((a, b, " ".join(lines[2:])))
    return out


def check_lang(topic_dir: Path, lang: str, R: Report) -> None:
    t = ev.Topic(topic_dir, lang)
    tag = lang.upper()
    segs = t.segments()
    lo, hi = ev.RATE[lang]
    # 配音
    for s in segs:
        for ln in s.lines:
            w = t.wav(ln.id)
            j = w.with_suffix(".words.json")
            if not w.exists():
                R.add("必改", "配音", f"{tag} {ln.id}", "缺配音"); continue
            if not j.exists():
                R.add("必改", "配音", f"{tag} {ln.id}", "没跑 qa"); continue
            d = json.loads(j.read_text(encoding="utf-8"))
            if d.get("text") != ln.say:
                R.add("必改", "配音", f"{tag} {ln.id}", "讲稿改过，配音或回听是旧的（重跑 tts / qa）")
            hyp = d.get("hyp", "")
            err = ev.cer(ln.say, hyp) if lang == "zh" else ev.wer(ln.say, hyp)     # 用当前评分规则重算，不信旧值
            if err > (ev.CER_LIMIT if lang == "zh" else ev.WER_LIMIT):
                R.add("必改", "配音", f"{tag} {ln.id}", f"回听错率 {err:.0%}：{d.get('hyp', '')[:40]}")
    # 时间轴、节奏
    if not t.timeline_path.exists():
        R.add("必改", "节奏", tag, "缺时间轴"); return
    tl = json.loads(t.timeline_path.read_text(encoding="utf-8"))
    if tl.get("estimated"):
        R.add("必改", "节奏", tag, "时间轴还是估算的（配音出来后重跑 timeline）")
    by_id = {ln.id: ln for s in segs for ln in s.lines}
    speak = sum(b - a for seg in tl["segments"].values() for a, b in seg["lines"].values())
    units = sum(ev.units(ln.say, lang) for ln in by_id.values())
    total = tl["total"]
    pace = units / (total / 60)
    unit = "字/分" if lang == "zh" else "词/分"
    lo_p, hi_p = PACE[lang]
    R.add("信息" if lo_p <= pace <= hi_p else "建议", "节奏", tag,
          f"全片 {pace:.0f} {unit}（含停顿；纯说话 {units / (speak / 60):.0f}）；参考 {lo_p}–{hi_p}；总长 {total:.0f} 秒")
    first_q = None
    for sid, seg in tl["segments"].items():
        for lid, (a, b) in seg["lines"].items():
            if first_q is None and re.search(r"[？?]|怎么回事|为什么|Why|What", by_id[lid].text):
                first_q = seg["offset"] + a
    if first_q is None or first_q > HOOK_BY:
        R.add("建议", "节奏", tag, f"开片 {HOOK_BY:.0f} 秒内没有抛出问题（第一个问句在 {first_q or 0:.0f} 秒）")
    # 字幕
    srt = topic_dir / "final" / f"{t.stem}.srt"
    if srt.exists():
        for a, b, txt in srt_rows(srt):
            n = len(ev.normalize(txt)) if lang == "zh" else len(txt)
            dur = b - a
            where = f"{tag} 字幕 {a:.1f}s"
            if n > SUB_MAX[lang]:
                R.add("必改", "字幕", where, f"一屏 {n} 字：{txt}")
            if dur < SUB_MIN_DUR:
                R.add("建议", "字幕", where, f"只停 {dur:.2f} 秒：{txt}")
            elif n / dur > SUB_SPEED[lang]:
                R.add("建议", "字幕", where, f"读速 {n / dur:.1f}/秒偏快：{txt}")
            if lang == "en" and len(txt.split()) <= 2 and not re.search(r"[.?!]$", txt):
                R.add("建议", "字幕", where, f"碎片：{txt}")
    else:
        R.add("必改", "字幕", tag, "缺成片字幕（先跑 mux）")
    # 画面日志
    log = t.render_dir / "render.log"
    if log.exists():
        for ln in log.read_text(encoding="utf-8", errors="replace").splitlines():
            if ln.startswith("[layout]"):
                R.add("必改", "画面", tag, ln[9:])
            elif ln.startswith("[cue]"):
                R.add("必改" if "超出" in ln else "建议", "画面", tag, ln[6:])
    else:
        R.add("建议", "画面", tag, "没有渲染日志（用 edu_video.py render 出画面才有自检）")
    # 成片
    final = topic_dir / "final" / f"{t.stem}.mp4"
    if final.exists():
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(final)],
                                   capture_output=True, text=True).stdout or 0)
        if abs(dur - total) > 0.2:
            R.add("必改", "成片", tag, f"成片 {dur:.1f} 秒与时间轴 {total:.1f} 秒不符（时间轴改过没重合成）")
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(final), "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.findall(r"I:\s+(-?\d+\.\d) LUFS", r.stderr)
        if m:
            lufs = float(m[-1])
            R.add("信息" if LUFS[0] <= lufs <= LUFS[1] else "必改", "成片", tag, f"响度 {lufs} LUFS")
    else:
        R.add("必改", "成片", tag, "缺成片")


def check_claims(topic_dir: Path, R: Report) -> None:
    """讲稿里像事实的句子（数字、百分比、引号）都要在 claims.json 登记。"""
    p = topic_dir / "claims.json"
    claims = json.loads(p.read_text(encoding="utf-8"))["claims"] if p.exists() else []
    covered = {lid for c in claims for lid in c.get("lines", [])}
    for c in claims:
        if not c.get("source"):
            R.add("必改", "事实", c.get("id", "?"), "台账条目缺出处")
        elif c["source"] not in ("experiment", "analogy", "judgment") and not c.get("quote"):   # analogy：比方里的虚构情节，不是事实；judgment：我们的判断（热点相迎立场规则），依据写在 basis
            R.add("必改", "事实", c.get("id", "?"), "外部出处缺原文原话（quote）")
    for lang in ev.LANGS:
        t = ev.Topic(topic_dir, lang)
        if not t.script_path.exists():
            continue
        for s in t.segments():
            if s.card:
                continue
            for ln in s.lines:
                if FACT_RE.search(ln.text) and ln.id not in covered:
                    R.add("必改", "事实", f"{lang.upper()} {ln.id}", f"像事实的句子没登记出处：{ln.text[:40]}")
    if not p.exists():
        R.add("必改", "事实", "claims.json", "缺事实台账")


def cmd_validate(topic_dir: Path, langs: list[str]) -> int:
    R = Report()
    for lang in langs:
        check_lang(topic_dir, lang, R)
    check_claims(topic_dir, R)
    order = {"必改": 0, "建议": 1, "信息": 2}
    rows = sorted(R.rows, key=lambda r: (order[r[0]], r[1], r[2]))
    out = topic_dir / "reviews" / "validate.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# 程序检验：{topic_dir.name}", "", f"必改 {R.blockers} · 建议 {sum(r[0] == '建议' for r in rows)}", "",
             "| 级别 | 类 | 位置 | 说明 |", "|---|---|---|---|"]
    lines += [f"| {a} | {b} | {c} | {d.replace('|', '｜')} |" for a, b, c, d in rows]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for a, b, c, d in rows:
        if a != "信息" or b in ("节奏", "成片"):
            print(f"{a}  {b}  {c}  {d}")
    print(f"→ {out.relative_to(REPO).as_posix()}：必改 {R.blockers} 条" + ("" if R.blockers else "，程序检验通过"))
    return 1 if R.blockers else 0


ROLES = REPO / "edu_videos" / "_shared" / "review" / "roles.json"
DESIGN_DOCS = [REPO / "edu_videos" / "_shared" / "design" / "design_system.md", REPO / "edu_videos" / "_shared" / "design" / "tokens.json"]
BENCH = REPO / "edu_videos" / "_shared" / "research" / "explainer_benchmark.md"


def lines_table(topic_dir: Path, langs: tuple[str, ...]) -> str:
    """讲稿按段列成表；包装卡段注明「画面：包装卡」。"""
    tops = {lg: ev.Topic(topic_dir, lg) for lg in langs}
    segs = {lg: t.segments() for lg, t in tops.items()}
    out = []
    for i, s in enumerate(segs[langs[0]]):
        kind = "冷开场" if s.cold else (f"包装卡 {s.card}" if s.card else (f"章节 {s.chapter}" if s.chapter else ""))
        out.append(f"\n### {s.id} {s.title}" + (f"（{kind}）" if kind else ""))
        out.append("| 句号 | " + " | ".join({"zh": "中文", "en": "English"}[lg] for lg in langs) + " |")
        out.append("|---|" + "---|" * len(langs))
        for j, ln in enumerate(s.lines):
            cells = [segs[lg][i].lines[j].text.replace("|", "｜") for lg in langs]
            out.append(f"| {ln.id} | " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def cmd_brief(topic_dir: Path, stage: str, after: Path | None = None) -> Path:
    roles = [r for r in json.loads(ROLES.read_text(encoding="utf-8"))["roles"] if stage in r["stages"]]
    base = topic_dir / "reviews"
    n = 1 + max([int(m.group(1)) for d in base.glob(f"{stage}_r*") if (m := re.match(rf"{stage}_r(\d+)$", d.name))] or [0])
    run = base / f"{stage}_r{n}"
    mat = run / "materials"
    (run / "tasks").mkdir(parents=True)
    (run / "reports").mkdir()
    mat.mkdir()
    (mat / "lines.md").write_text("# 讲稿（中英对照）\n" + lines_table(topic_dir, ("zh", "en")), encoding="utf-8")
    (mat / "lines_zh.md").write_text("# 讲稿（中文）\n" + lines_table(topic_dir, ("zh",)), encoding="utf-8")
    (mat / "lines_en.md").write_text("# Script (English)\n" + lines_table(topic_dir, ("en",)), encoding="utf-8")
    learn = json.loads((topic_dir / "learning.json").read_text(encoding="utf-8")) if (topic_dir / "learning.json").exists() else {}
    quiz = ["# 测验（不含答案）", ""]
    for q in learn.get("quiz", []):
        quiz.append(f"**{q['id']}** {q['zh']}  \n{q['en']}")
        for c_zh, c_en in zip(q.get("choices", {}).get("zh", []), q.get("choices", {}).get("en", [])):
            quiz.append(f"- {c_zh} / {c_en}")
        quiz.append("")
    if learn.get("explain_back"):
        quiz.append(f"**讲回来**：{learn['explain_back']['prompt']['zh']} / {learn['explain_back']['prompt']['en']}")
    (mat / "quiz.md").write_text("\n".join(quiz) + "\n", encoding="utf-8")
    rel = lambda q: q.relative_to(REPO).as_posix()
    paths = {
        "lines_bilingual": [mat / "lines.md"], "lines_zh": [mat / "lines_zh.md"], "lines_en": [mat / "lines_en.md"],
        "learning": [topic_dir / "learning.json"], "research_summary": [BENCH],
        "claims": [topic_dir / "claims.json"], "research": [topic_dir / "research.md"],
        "quiz_only": [mat / "quiz.md"], "design_system": DESIGN_DOCS,
        "frames_and_subs": [topic_dir / "renders" / "sheets", topic_dir / "renders" / "en" / "sheets",
                            topic_dir / "final" / f"{topic_dir.name}.srt", topic_dir / "final" / f"{topic_dir.name}.en.srt"],
    }
    out_rule = json.loads(ROLES.read_text(encoding="utf-8"))["output"]
    for r in roles:
        mats = [q for k in r["materials"] for q in paths.get(k, [])]
        lines = [f"# 审稿任务：{r['name']}（{topic_dir.parent.name} / {topic_dir.name} · {stage} 第 {n} 轮）", "",
                 "你是一位独立审稿人，用全新的视角审这一期中英双语科普短视频（AI 高频词系列，面向没有机器学习背景的普通观众）。",
                 "", "## 规则",
                 "- **只读**：不要修改仓库里的任何文件；只读下面列出的材料" + ("（盲审：不要读讲稿以外的任何文件，包括另一种语言的版本与别的审稿报告）" if r.get("blind") else "，不要读别的审稿报告") + "。",
                 "- 只管你这一角色的必查项；顺手看到的其他问题放在最后「其他」，一句话。",
                 "- 拿不准写「存疑」并说明怎么核实。", "", "## 材料（路径相对仓库根 " + REPO.as_posix() + "）"]
        lines += [f"- `{rel(q)}`" for q in mats]
        checks = list(r["checks"])
        if after and not r.get("blind"):
            lines.append(f"- `{rel(after / 'issues.md')}`（上一轮问题与作者处理结论）")
            checks.append("R：复核上一轮你这一角色指出的问题（见上一轮 issues.md）：逐条写「已解决 / 未解决 / 改出了新问题」；作者「不采纳」的，判断理由是否成立")
        lines += ["", "## 必查项"] + [f"{i}. {c}" for i, c in enumerate(checks, 1)]
        if r.get("examples"):
            lines += ["", "## 以前抓到过的同类问题（照这个水平找）"] + [f"- {e}" for e in r["examples"]]
        if r["runner"] == "codex":
            tail = "最终回复就是完整报告（Markdown），不要写文件。"
        else:
            tail = (f"把完整报告写到 `{rel(run / 'reports' / (r['id'] + '.md'))}`（这是你唯一可以写的文件），"
                    "然后只回复 200 字以内的摘要：最严重的 3 条与报告路径。")
        lines += ["", "## 输出", out_rule, "", tail]
        (run / "tasks" / f"{r['id']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (run / "roster.json").write_text(json.dumps({"stage": stage, "round": n, "roles": [{"id": r["id"], "name": r["name"], "runner": r["runner"]} for r in roles]},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{rel(run)}：{len(roles)} 个角色 → " + "、".join(f"{r['id']}（{r['runner']}）" for r in roles))
    return run


ROW = re.compile(r"^\|\s*(l\d+|s\d+|全片)[^|]*\|\s*([^|]*)\|\s*(必改|建议|记录|存疑)\s*\|\s*([^|]*)\|\s*([^|]*)\|", re.M)


def cmd_merge(run: Path) -> Path:
    roster = json.loads((run / "roster.json").read_text(encoding="utf-8"))
    rows = []
    for r in roster["roles"]:
        p = run / "reports" / f"{r['id']}.md"
        if not p.exists():
            print(f"缺报告：{r['id']}"); continue
        for m in ROW.finditer(p.read_text(encoding="utf-8")):
            rows.append({"line": m.group(1), "lang": m.group(2).strip(), "level": m.group(3), "issue": m.group(4).strip(),
                         "fix": m.group(5).strip(), "role": r["id"]})
    key = lambda x: (int(x["line"][1:]) if x["line"][0] in "ls" and x["line"][1:].isdigit() else 9999, {"必改": 0, "存疑": 1, "建议": 2, "记录": 3}[x["level"]])
    rows.sort(key=key)
    by_line: dict[str, set] = {}
    for x in rows:
        by_line.setdefault(x["line"], set()).add(x["role"])
    out = [f"# 审稿汇总：{run.name}", "", f"必改 {sum(x['level'] == '必改' for x in rows)} · 存疑 {sum(x['level'] == '存疑' for x in rows)} · "
           f"建议 {sum(x['level'] == '建议' for x in rows)} · 记录 {sum(x['level'] == '记录' for x in rows)}；"
           "「多人」= 两个以上角色指到同一句。处理结论写在最后一列（改 / 不改＋理由）。", "",
           "| 句号 | 语言 | 级别 | 角色 | 多人 | 问题 | 建议改法 | 处理 |", "|---|---|---|---|---|---|---|---|"]
    for x in rows:
        multi = "★" if len(by_line[x["line"]]) > 1 else ""
        out.append(f"| {x['line']} | {x['lang']} | {x['level']} | {x['role']} | {multi} | {x['issue']} | {x['fix']} |  |")
    p = run / "issues.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{p.relative_to(REPO).as_posix()}：{len(rows)} 条")
    return p


# ───────────────────────── 台词审 v2（口播＋屏幕文字；双审＋裁决） ─────────────────────────
LINE_REVIEW = REPO / "edu_videos" / "_shared" / "review" / "line_review.json"
LEVELS = ("必改", "存疑", "建议", "记录")
SCORE_RE = re.compile(r"^\s*-\s*\**\s*(V\d|P\d|R)\s*\**\s*[:：]?\s*([0-3])\s*分?\s*(证据|原因|理由)\s*[:：]\s*(.+?)\s*$", re.M)
TABLE_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*(必改|存疑|建议|记录)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|", re.M)
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9'’.%,\-–]*")   # 带重音的拉丁字母（résumé）算同一个词


def rel(p: Path) -> str:
    return p.resolve().relative_to(REPO).as_posix()


def count_text(s: str, lang: str) -> int:
    """中文数汉字＋数字串（一个数字串算 1 字）；英文数词。"""
    if lang == "en":
        return len(WORD_RE.findall(s))
    return len(re.findall(r"[一-鿿]", s)) + len(re.findall(r"[0-9][0-9.,%]*|[A-Za-z]+", s))


def seg_label(s, lang: str) -> str:
    zh = lang == "zh"
    if s.cold:
        return "开场（片头之前）" if zh else "Cold open (before the title card)"
    if s.card == "agenda":
        return "本期内容（画面：目录卡）" if zh else "What's coming (on screen: agenda card)"
    if s.card == "outro":
        return "片尾（画面：片尾卡）" if zh else "Outro (on screen: end card)"
    return s.title


# 口语黑名单（用户每抓到一句别扭话就加一条，附出处）。命中只是「可疑」，交审稿人逐条判；validate 里记为建议。
LINT = {
    "zh": [
        (r"的(祸|代价|局限|弊端|危害|意义)[，,]\s*(和|以及|与)", "名词短语后硬接「和…」（「现实里的祸，和怎么防」，用户 2026-11-09）"),
        (r"[，,]\s*(和|以及)(怎么|如何|为什么|为何)", "名词短语加「和」再接问句，口语不这么并列（用户 2026-11-09）"),
        (r"以及|进行|予以|加以|从而|因而|诸如|鉴于|之所以|亦", "书面词"),
        (r"[；;]", "分号：口播里像在念清单"),
        (r"(讲|说|聊)(几|两|三|四|五)件事", "目录腔（用户 2026-11-08）"),
        (r"^(它是|为什么|怎么|如何)[^，。？]{0,10}[；。]$", "标题式短句单独成句（目录腔）"),
    ],
    "en": [
        (r"\b(failures?|costs?|problems?|limits?),? and how to\b", "noun phrase + 'and how to…' (TOC style, user 2026-11-09)"),
        (r"\bIn this episode\b|\bFirstly\b|\bfurthermore\b|\bmoreover\b|\bthus\b|\bhence\b|\bwhereby\b", "written / TOC style"),
        (r";", "semicolon: sounds like reading a list"),
    ],
}
LINT_TITLE_ZH = [(r"^[^，。]{1,6}的(祸|代价|局限)$", "章名是生造的名词短语（「现实里的祸」，用户 2026-11-09）"),
                 (r"^怎么\S+，怎么\S+$", "章名两个「怎么」并列，读着像目录（用户 2026-11-09）")]


def lint_hits(topic_dir: Path, lang: str) -> list[str]:
    out = []
    for s in ev.Topic(topic_dir, lang).segments():
        for ln in s.lines:
            for pat, why in LINT[lang]:
                if re.search(pat, ln.say, re.I | re.M):
                    out.append(f"{ln.id}「{ln.say}」：{why}")
    pk = topic_dir / "package.json"
    if pk.exists():
        E = json.loads(pk.read_text(encoding="utf-8"))
        for cid, t in (E.get("chapters") or {}).items():
            text = t.get(lang, "")
            for pat, why in (LINT_TITLE_ZH if lang == "zh" else []):
                if re.search(pat, text):
                    out.append(f"[屏幕] 章节卡 {cid}「{text}」：{why}")
    return out


def picture_note(info: dict | None, lang: str) -> str:
    """一句画面说明（盲审也要知道「这十个点」指着什么）：屏幕上最大的两块字，有图表就说有图。"""
    if not info:
        return ""
    blocks = info["blocks"]
    main = sorted([b for b in blocks if b["cls"] not in ("eyebrow", "chart")], key=lambda b: -b["px"])[:2]
    chart = any(b["cls"] == "chart" for b in blocks)
    parts = [f"「{b['text'][:24]}」" for b in main] + (["图表" if lang == "zh" else "a chart"] if chart else [])
    if not parts:
        return ""
    return ("　〔画面：" + "、".join(parts) + "〕") if lang == "zh" else ("  [On screen: " + ", ".join(parts) + "]")


def voice_md(topic_dir: Path, lang: str, shots: dict | None = None) -> str:
    """盲审材料：只有口播（按播放顺序，配音实际念法），附时长与停顿、一句画面说明；包装卡、章节卡只写一行提示。"""
    t = ev.Topic(topic_dir, lang)
    tl = json.loads(t.timeline_path.read_text(encoding="utf-8"))["segments"]
    pk = json.loads((topic_dir / "package.json").read_text(encoding="utf-8"))
    zh = lang == "zh"
    out = ["# 口播（按播放顺序）" if zh else "# Narration (in playback order)", "",
           ("每行：句号（念多长 / 句后停多久）：配音念的原文；〔画面：…〕是这句说完时屏幕上最显眼的字，只用来判断「这个」「左边」之类指得到指不到，画面本身另有人审。章节卡、片头卡不念，只提示画面切换。" if zh else
            "Each line: id (spoken duration / pause after): exactly what the narrator says. [On screen: …] lists the most prominent on-screen text when the line ends, only so you can tell whether words like 'this' or 'on the left' point at something; the visuals are reviewed separately. Title and chapter cards are silent; they only mark scene changes."), ""]
    for s in t.segments():
        if s.chapter:
            out.append(f"> 〔画面：章节卡「{pk['chapters'][s.chapter][lang]}」〕\n" if zh else f"> [On screen: chapter card “{pk['chapters'][s.chapter][lang]}”]\n")
        out.append(f"## {seg_label(s, lang)}")
        cues = tl.get(s.id, {}).get("lines", {})
        lids = [ln.id for ln in s.lines]
        for k, ln in enumerate(s.lines):
            a, b = cues.get(ln.id, (0, 0))
            nxt = cues.get(lids[k + 1], (b, b))[0] if k + 1 < len(lids) else None
            gap = f" / {'停' if zh else 'pause'} {nxt - b:.1f}s" if nxt is not None else ""
            out.append(f"- {ln.id}（{b - a:.1f}s{gap}）：{ln.say}{picture_note((shots or {}).get(ln.id), lang)}")
        out.append("")
        if s.cold:
            out.append("> 〔画面：片头卡（节目名＋本期标题）〕\n" if zh else "> [On screen: title card (series + episode title)]\n")
    return "\n".join(out) + "\n"


def card_frames(topic_dir: Path, lang: str, out_dir: Path) -> dict[str, str]:
    """包装卡（片头、本期内容、章节卡、片尾）末尾一帧。"""
    t = ev.Topic(topic_dir, lang)
    tl = json.loads(t.timeline_path.read_text(encoding="utf-8"))["segments"]
    out_dir.mkdir(parents=True, exist_ok=True)
    res = {}
    for sid, seg in tl.items():
        if "card" not in seg:
            continue
        src = t.render_dir / f"{sid}_fit.mp4"
        if not src.exists() or src.stat().st_mtime < (t.package_dir / f"{sid}.mp4").stat().st_mtime if (t.package_dir / f"{sid}.mp4").exists() else False:
            src = t.package_dir / f"{sid}.mp4"      # 还没整片渲染时，用包装卡本身
        if not src.exists():
            continue
        dst = out_dir / f"card_{sid}.png"
        at = seg["duration"] - (1.3 if seg.get("card") == "outro" else 0.4)   # 片尾卡最后 0.9 秒淡到黑，截在淡出前
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(at, 0):.2f}", "-i", str(src),
                        "-frames:v", "1", str(dst)], check=True)
        res[sid] = rel(dst)
    return res


def card_texts(pk: dict, sid: str, card: str, lang: str) -> list[str]:
    if card == "agenda":
        ag = pk.get("agenda", [])
        rows = ([f"{k:02d} · {v[lang]}" for k, v in enumerate(pk["chapters"].values(), 1)] if ag == "chapters"   # 目录 = 章节卡标题
                else [f"{r['tag'][lang]} · {r['text'][lang]}" for r in ag])
        pre = [r["text"][lang] for r in pk.get("prereq", [])]
        return rows + ([("先修：" if lang == "zh" else "Prereqs: ") + " / ".join(pre)] if pre else [])
    if card.startswith("chapter:"):
        return [pk["chapters"][card.split(":", 1)[1]][lang]]
    if card == "intro":
        return [pk["title"][lang]]
    if card == "outro":
        return [" ".join(pk.get("quote", {}).get(lang, [])), pk.get("next", {}).get(lang, [""])[0]]   # 卡上只放本语言
    return []


def screen_md(topic_dir: Path, lang: str, mat: Path, shots: dict | None = None) -> str:
    """屏幕文字材料：逐句列口播、该句说完时屏幕上看得见的文字块（层级、字号、字数）、截图；包装卡列文字＋末帧。"""
    import edu_web
    t = ev.Topic(topic_dir, lang)
    tl = json.loads(t.timeline_path.read_text(encoding="utf-8"))["segments"]
    pk = json.loads((topic_dir / "package.json").read_text(encoding="utf-8"))
    shots = shots if shots is not None else edu_web.screen_dump(t, mat / "screen" / lang)
    frames = card_frames(topic_dir, lang, mat / "screen" / lang)
    zh = lang == "zh"
    unit = "字" if zh else "words"
    out = ["# 屏幕文字（逐屏）" if zh else "# On-screen text (screen by screen)", "",
           ("每句口播说完前一刻，屏幕上看得见的文字块：`[层级 字号px]` 文字（字数）。层级：eyebrow 小标签、display 大数字、h1 标题、h2 小标题、body 正文、caption 注释、chart 图表文字。"
            "截图是 1920×1080 的那一刻（字幕在成片里另外压在底部，截图里没有）。" if zh else
            "For each narration line, the text blocks visible just before it ends: `[level size px]` text (word count). Levels: eyebrow label, display big number, h1 title, h2 subtitle, body, caption, chart text. "
            "Screenshots are 1920×1080 at that moment (narration subtitles are burned in at the bottom of the final cut, not shown here)."), ""]
    segs = t.segments()
    for s in segs:
        seg = tl.get(s.id, {})
        if s.chapter:
            cid = f"c_{s.chapter}"
            out += [f"## {cid}（{'章节卡' if zh else 'chapter card'}）", f"- {card_texts(pk, cid, 'chapter:' + s.chapter, lang)[0]}",
                    f"- {'截图' if zh else 'screenshot'}：`{frames.get(cid, '')}`", ""]
        out.append(f"## {s.id} {seg_label(s, lang)}")
        if s.card:
            out += [f"### {s.card}（{'包装卡，整段' if zh else 'package card, whole segment'} {seg.get('duration', 0):.1f}s）"]
            out += [f"- 口播 {ln.id}：{ln.text}" if zh else f"- narration {ln.id}: {ln.text}" for ln in s.lines]
            out += [f"- {'屏幕' if zh else 'screen'}：{x}（{count_text(x, lang)} {unit}）" for x in card_texts(pk, s.id, s.card, lang)]
            out += [f"- {'截图' if zh else 'screenshot'}：`{frames.get(s.id, '')}`", ""]
            continue
        cues = seg.get("lines", {})
        prev = None
        for ln in s.lines:
            info = shots.get(ln.id)
            a, b = cues.get(ln.id, (0, 0))
            out.append(f"### {ln.id}（{b - a:.1f}s）")
            out.append(f"- {'口播' if zh else 'narration'}：{ln.text}")
            if not info:
                out.append(f"- （{'无截图' if zh else 'no screenshot'}）"); continue
            blocks = info["blocks"]
            sig = [x["text"] for x in blocks]
            if sig == prev:
                out.append(f"- {'屏幕同上一句' if zh else 'screen unchanged from previous line'}")
            else:
                main = [x for x in blocks if x["cls"] not in ("eyebrow", "chart")]
                total = sum(count_text(x["text"], lang) for x in main)
                for x in blocks:
                    out.append(f"- [{x['cls']} {x['px']}px] {x['text']}（{count_text(x['text'], lang)} {unit}）")
                out.append(f"- {'合计' if zh else 'total'}（{'不含小标签、图表' if zh else 'excl. eyebrow & chart'}）：{len(main)} {'块' if zh else 'blocks'}，{total} {unit}")
            out.append(f"- {'截图' if zh else 'screenshot'}：`{info['shot']}`")
            prev = sig
        out.append("")
    return "\n".join(out) + "\n"


def slot_prompt(it: dict, slot: str, run: Path, cfg: dict, loop: int, topic_dir: Path) -> str:
    zh = it["lang"] == "zh"
    model = cfg["models"][slot]
    mat = run / "materials"
    rp = run / "reports" / f"{it['id']}__{slot}.md"
    L = [f"你是独立审稿人 **{it['id']}__{slot}**（{slot} 位 · {model}），只管「{it['name']}」这一项。第 {loop} 轮（最多 {cfg['max_rounds']} 轮）。", "",
         it["who"], "", f"## 这一项查什么\n{it['what']}", "", f"为什么要查：{it['why']}", "",
         "## 规则",
         "- **只读**：不要修改仓库里的任何文件（你自己的报告除外）；不调用任何收费服务。",
         "- 同一项还有另一位审稿人（另一个模型）独立审；**不要读它的报告**，也不要读 `reconcile/` 与 `reports/` 下别人的文件。"]
    if it["material"] == "voice":
        L += [f"- **盲审：只读 `{rel(mat / ('voice_' + it['lang'] + '.md'))}`**。不要读讲稿、画面、另一种语言的版本或任何别的文件——观众只能听。",
              "- 每句都出声在心里念一遍，用耳朵判断。"]
    else:
        L += [f"- 材料：`{rel(mat / ('screen_' + it['lang'] + '.md'))}`（逐屏文字、字数、对应口播）与截图目录 `{rel(mat / 'screen' / it['lang'])}/`（需要看排版、层级时打开截图）。",
              "- 只评屏幕上的文字；口播文字只用来判断分工与一致，口播本身另有审稿人。",
              f"- {it['limits']}"]
    if loop > 1:
        L.append(f"- 上一轮问题与作者处理：`{rel(run / 'previous.md')}`（只看本项的条目）；评分表另写 `- R` 一行逐条复核：已解决 / 未解决 / 改出新问题；作者「不采纳」的判断理由是否成立。")
    lang = it["lang"]
    if cfg.get("strict"):
        L += ["", "## 从严条目" if zh else "## Strict items", cfg["strict"][lang]]
    if it["material"] == "voice" and cfg.get("retell"):
        L += ["", "## 逐句复述" if zh else "## Line-by-line retell", cfg["retell"][lang]]
    hits = lint_hits(topic_dir, lang)
    if hits:
        L += ["", "## 程序标出的可疑句（逐条判：成立就进问题表，不成立在整体观察里说一句）" if zh else
              "## Lines flagged by the lint (rule on each: add to the issue table if it holds, otherwise say why in 整体观察)"]
        L += [f"- {h}" for h in hits if (it["material"] == "voice") == (not h.startswith("[屏幕]"))] or ["- （无）"]
    L += ["", "## 评分维度（「## 评分表」里每维一行）"] + [f"- **{d[0]}** {d[1]}：{d[2]}" for d in it["dims"]]
    if loop > 1:
        L.append("- **R** 复核上一轮")
    L += ["", "## 评分规则"] + [f"- {x}" for x in cfg["scoring"]]
    if it.get("examples"):
        L += ["", "## 以前抓到过的同类问题（照这个水平找，别放过同类）"] + [f"- {e}" for e in it["examples"]]
    L += ["", "## 输出", cfg["output"]["zh" if zh else "en"], ""]
    if slot == "b":
        L.append("最终回复就是完整报告（Markdown），不要写文件。")
    else:
        L.append(f"把完整报告写到 `{rel(rp)}`（你唯一可以写的文件），然后只回复 200 字以内的摘要：最低分维度、最严重的 3 条。")
    return "\n".join(L) + "\n"


def next_round(topic_dir: Path, chain: str = "lines") -> int:
    base = topic_dir / "reviews"
    return 1 + max([int(m.group(1)) for d in base.glob(f"{chain}_r*") if (m := re.match(rf"{re.escape(chain)}_r(\d+)$", d.name))] or [0])


def cmd_new(topic_dir: Path, after: Path | None, chain: str = "lines") -> Path:
    cfg = json.loads(LINE_REVIEW.read_text(encoding="utf-8"))
    n = next_round(topic_dir, chain)
    if n > cfg["max_rounds"]:
        raise SystemExit(f"台词审已到第 {cfg['max_rounds']} 轮上限")
    if n > 1 and not after:
        after = topic_dir / "reviews" / f"{chain}_r{n - 1}"
    run = topic_dir / "reviews" / f"{chain}_r{n}"
    mat = run / "materials"
    for d in (mat, run / "items", run / "reports", run / "reconcile"):
        d.mkdir(parents=True, exist_ok=True)
    import edu_web
    for lg in ("zh", "en"):
        shots = edu_web.screen_dump(ev.Topic(topic_dir, lg), mat / "screen" / lg)
        (mat / f"voice_{lg}.md").write_text(voice_md(topic_dir, lg, shots), encoding="utf-8")
        (mat / f"screen_{lg}.md").write_text(screen_md(topic_dir, lg, mat, shots), encoding="utf-8")
    if after:
        (run / "previous.md").write_text((after / "issues.md").read_text(encoding="utf-8"), encoding="utf-8")
    items = []
    for it in cfg["items"]:
        for slot in ("a", "b"):
            (run / "items" / f"{it['id']}__{slot}.md").write_text(slot_prompt(it, slot, run, cfg, n, topic_dir), encoding="utf-8")
        n_lines = sum(len(s.lines) for s in ev.Topic(topic_dir, it["lang"]).segments())
        items.append({"id": it["id"], "name": it["name"], "dims": [d[0] for d in it["dims"]] + (["R"] if n > 1 else []),
                      "retell_min": int(n_lines * 0.8) if it["material"] == "voice" and cfg.get("retell") else 0})
    (run / "roster.json").write_text(json.dumps({"kind": "lines", "round": n, "after": rel(after) if after else None, "created_at": now_iso(), "state": "进行中",
                                                "models": cfg["models"], "items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    write_checklist(run)
    print(f"{rel(run)}：{len(items)} 项 × 2 位审稿 → items/<项>__a.md（Claude，自己写报告）/ __b.md（Codex，codex exec -o reports/<项>__b.md）")
    return run


def parse_report(text: str, dims: list[str], judge: bool = False, retell_min: int = 0) -> tuple[dict, list[dict], list[str]]:
    """返回（分数 {维: (分, 证据)}，问题行，格式错误）。"""
    errs, scores = [], {}
    for m in SCORE_RE.finditer(text):
        scores[m.group(1)] = (int(m.group(2)), m.group(4).strip(), m.group(3))
    rows = [{"where": m.group(1), "dim": m.group(2), "level": m.group(3), "orig": m.group(4), "issue": m.group(5), "fix": m.group(6)}
            for m in TABLE_ROW.finditer(text) if not m.group(1).startswith("位置") and not set(m.group(1)) <= set("-: ")]
    if judge:
        return scores, rows, errs
    for d in dims:
        if d not in scores:
            errs.append(f"缺维度 {d}")
            continue
        sc, ev_, kind = scores[d]
        if sc >= 2 and (kind != "证据" or len(ev_) < 8):
            errs.append(f"{d} 打 {sc} 分但证据不足 8 字")
        if sc == 0 and kind != "原因":
            errs.append(f"{d} 打 0 分要写原因")
        if sc == 1 and not any(d in r["dim"] for r in rows) and not (d in ("R", "V6", "P6") and rows):   # 复核、改写质量的问题常归到原维度的条目下
            errs.append(f"{d} 打 1 分但问题表里没有对应条目")
    if "结论：无问题" not in text and not rows:
        errs.append("没有问题表，也没写「结论：无问题」")
    if retell_min:
        body = text.split("## 逐句复述", 1)[1].split("\n## ", 1)[0] if "## 逐句复述" in text else ""
        n = len(re.findall(r"^\|\s*l\d+", body, re.M))
        if n < retell_min:
            errs.append(f"「## 逐句复述」只有 {n} 句，至少要 {retell_min} 句（每句都要写跟朋友会怎么说）")
    return scores, rows, errs


def audit_pick(run: Path, iid: str, cands: list[str], k: int = 2) -> list[str]:
    import hashlib
    return sorted(cands, key=lambda d: hashlib.sha1(f"{run.name}/{iid}/{d}".encode()).hexdigest())[:k]


def judge_prompt(run: Path, it: dict, cfg_it: dict, a_rep: Path, b_rep: Path, disagree: list[str], audit: list[str],
                 sa: dict, sb: dict, topic_dir: Path) -> str:
    mat = run / "materials"
    fmt = lambda s, d: f"{s[d][0]} 分（{s[d][1][:300]}）" if d in s else "缺"
    L = [f"你是裁决人 **{it['id']}__judge**（claude-opus-5-5），裁「{it['name']}」这一项两位审稿人的分歧，并抽查两人都判通过的维度。", "",
         "## 材料",
         f"- a 位报告：`{rel(a_rep)}`；b 位报告：`{rel(b_rep)}`",
         f"- 被审材料：`{rel(mat / ('voice_' + cfg_it['lang'] + '.md' if cfg_it['material'] == 'voice' else 'screen_' + cfg_it['lang'] + '.md'))}`"
         + (f"，截图 `{rel(mat / 'screen' / cfg_it['lang'])}/`" if cfg_it["material"] == "screen" else ""),
         f"- 你可以另读讲稿 `{rel(topic_dir / ('script.md' if cfg_it['lang'] == 'zh' else 'script.en.md'))}` 与场景源文件 `{rel(topic_dir / 'scenes' / 'web')}/` 核对。",
         f"- 本项标准：`{rel(run / 'items' / (it['id'] + '__a.md'))}`（评分维度、硬上限、示例）。", "",
         "## 要裁的维度"]
    for d in disagree:
        L.append(f"- **{d}**（分歧）a {fmt(sa, d)}；b {fmt(sb, d)}")
    for d in audit:
        L.append(f"- **{d}**（抽查）a {fmt(sa, d)}；b {fmt(sb, d)}")
    cfg = json.loads(LINE_REVIEW.read_text(encoding="utf-8"))
    L += ["", "## 规则",
          "- " + cfg.get("strict", {}).get(cfg_it["lang"], ""),
          "- 分歧维度：回到材料本身核两人的证据，谁站得住；抽查维度：专找两个模型**共同**漏掉的问题，不因两人都给高分就放过。",
          "- 两人的问题表里，你认为不成立或改写反而更差的条目，在「## 驳回」里列出位置和理由。",
          "- 只读，不改被审材料。", "",
          "## 输出（写到 `" + rel(run / 'reports' / (it['id'] + '__judge.md')) + "`）",
          "1. `## 裁决`：每个要裁的维度一行 `- <编号> <0–3> 理由：…`（理由至少 8 字，引用句号或屏号）。",
          "2. `## 补充问题`（两人都漏的，可空）：同审稿报告的表头 `| 位置 | 维度 | 级别 | 原文 | 问题 | 改写 |`。",
          "3. `## 驳回`：`- <位置>：<理由>`（可空）。",
          "然后只回复 150 字以内的摘要。"]
    return "\n".join(L) + "\n"


def cmd_check(run: Path) -> int:
    cfg = json.loads(LINE_REVIEW.read_text(encoding="utf-8"))
    by_id = {x["id"]: x for x in cfg["items"]}
    ros = json.loads((run / "roster.json").read_text(encoding="utf-8"))
    topic_dir = run.parent.parent
    todo = 0
    for it in ros["items"]:
        reps = {s: run / "reports" / f"{it['id']}__{s}.md" for s in ("a", "b")}
        parsed = {}
        for s, p in reps.items():
            if not p.exists():
                print(f"[待审] {it['id']}__{s}"); todo += 1; continue
            sc, rows, errs = parse_report(p.read_text(encoding="utf-8"), it["dims"], retell_min=it.get("retell_min", 0))
            if errs:
                print(f"[格式不合格] {it['id']}__{s}：" + "；".join(errs)); todo += 1; continue
            parsed[s] = sc
        if len(parsed) < 2:
            continue
        sa, sb = parsed["a"], parsed["b"]
        dis = [d for d in it["dims"] if abs(sa[d][0] - sb[d][0]) >= 2 or (min(sa[d][0], sb[d][0]) <= 1 < max(sa[d][0], sb[d][0]))]
        both_ok = [d for d in it["dims"] if sa[d][0] >= 2 and sb[d][0] >= 2]
        aud = audit_pick(run, it["id"], both_ok)
        it["disagree"], it["audit"] = dis, aud
        rec = [f"# 对比：{it['id']}", "", "| 维度 | a | b | 处理 |", "|---|---|---|---|"]
        rec += [f"| {d} | {sa[d][0]} | {sb[d][0]} | {'分歧→裁决' if d in dis else ('抽查→裁决' if d in aud else ('都 ≥2' if d in both_ok else '都 ≤1'))} |" for d in it["dims"]]
        (run / "reconcile" / f"{it['id']}.md").write_text("\n".join(rec) + "\n", encoding="utf-8")
        jp = run / "items" / f"{it['id']}__judge.md"
        if not jp.exists():
            jp.write_text(judge_prompt(run, it, by_id[it["id"]], reps["a"], reps["b"], dis, aud, sa, sb, topic_dir), encoding="utf-8")
        jr = run / "reports" / f"{it['id']}__judge.md"
        if not jr.exists():
            print(f"[待裁决] {it['id']}：分歧 {dis or '无'}，抽查 {aud}"); todo += 1; continue
        js, _, _ = parse_report(jr.read_text(encoding="utf-8"), [], judge=True)
        miss = [d for d in dis + aud if d not in js]
        if miss:
            print(f"[裁决不全] {it['id']}：缺 {miss}"); todo += 1; continue
        print(f"[完成] {it['id']}")
    (run / "roster.json").write_text(json.dumps(ros, ensure_ascii=False, indent=1), encoding="utf-8")
    write_checklist(run)
    print("全部审完，可以运行 issues" if not todo else f"还有 {todo} 处没完成")
    return todo


STATUS = {"open": "待处理", "implemented": "已改", "wontfix": "不改", "rejected": "驳回"}
UI_LEVEL = {"必改": "critical", "存疑": "verify", "建议": "minor", "记录": "minor"}
ITEM_NAME = {"voice_zh": "中文口播", "voice_en": "英文口播", "screen_zh": "中文屏幕文字", "screen_en": "英文屏幕文字"}
ITEM_COLOR = {"voice_zh": "#c0502e", "voice_en": "#2e6fc0", "screen_zh": "#b8860b", "screen_en": "#6b4fc0"}


def write_checklist(run: Path) -> None:
    """把审查单写成管理站 /review-run 读的 checklist.json（与 Portal Travel v5 审查单同形），
    审稿任务、两位审稿人的评分与证据、裁决、最终分、收轮结论都在站上看；问题清单页读 issues.json。"""
    cfg = json.loads(LINE_REVIEW.read_text(encoding="utf-8"))
    by_id = {x["id"]: x for x in cfg["items"]}
    ros = json.loads((run / "roster.json").read_text(encoding="utf-8"))
    topic_dir = run.parent.parent
    issues = json.loads((run / "issues.json").read_text(encoding="utf-8")) if (run / "issues.json").exists() else None
    items = []
    for it in ros["items"]:
        c = by_id[it["id"]]
        slots, parsed = {}, {}
        for sl in ("a", "b"):
            rp = run / "reports" / f"{it['id']}__{sl}.md"
            sc = parse_report(rp.read_text(encoding="utf-8"), it["dims"])[0] if rp.exists() else {}
            parsed[sl] = sc
            slots[sl] = {"slot": sl, "runner": "claude" if sl == "a" else "codex", "model": cfg["models"][sl],
                         "status": "done" if rp.exists() else "pending", "report": f"reports/{it['id']}__{sl}.md",
                         "prompt": f"items/{it['id']}__{sl}.md",
                         "scores": {d: {"score": v[0], "evidence": v[1]} for d, v in sc.items()}}
        jr = run / "reports" / f"{it['id']}__judge.md"
        js = parse_report(jr.read_text(encoding="utf-8"), [], judge=True)[0] if jr.exists() else {}
        dims = it["dims"]
        dis, aud = it.get("disagree", []), it.get("audit", [])
        scores, final = {}, {}
        for d in dims:
            a, b = parsed["a"].get(d), parsed["b"].get(d)
            name = next((x[1] for x in c["dims"] if x[0] == d), "复核上一轮" if d == "R" else d)
            fin = js[d][0] if d in js else (min(a[0], b[0]) if a and b else None)
            final[d] = fin
            scores[d] = {"name": name, "a": a[0] if a else -1, "a_ev": a[1] if a else "", "b": b[0] if b else -1, "b_ev": b[1] if b else "",
                         "verdict": "分歧" if d in dis else ("抽查" if d in aud else "一致"), "agreed": None if d in dis else fin,
                         "final": fin, "judge_reason": js[d][1] if d in js else ""}
        cnt = {}
        if issues:
            for i in issues["issues"]:
                if i["item"] == it["id"]:
                    cnt[i["level_zh"]] = cnt.get(i["level_zh"], 0) + 1
        done = all(sv["status"] == "done" for sv in slots.values()) and (jr.exists() or not (dis or aud))
        items.append({
            "id": it["id"], "law": "lines", "law_name": c["name"], "color": ITEM_COLOR.get(it["id"], "#888"),
            "scope": [], "checks": c["what"], "how": c.get("limits", "") or ("盲审：只听口播（按播放顺序）" if c.get("blind") else ""),
            "blind": bool(c.get("blind")), "status": "done" if done else ("adjudicating" if all(sv["status"] == "done" for sv in slots.values()) else "pending"),
            "report": f"reconcile/{it['id']}.md", "prompt": f"items/{it['id']}__a.md",
            "what": c["what"], "problem": c["why"], "model_why": "a 位 Claude、b 位 Codex 各自独立审；分歧与抽查交 Claude Opus 裁决",
            "rubric": [{"id": x[0], "name": x[1], "question": x[2]} for x in c["dims"]] + ([{"id": "R", "name": "复核上一轮", "question": "上一轮本项的问题逐条复核"}] if "R" in dims else []),
            "slots": slots, "scores": scores, "disputes": dis, "audits": aud, "final_scores": final,
            "judge": {"runner": "claude", "model": cfg["models"]["judge"], "status": "done" if jr.exists() else "pending",
                      "dims": dis + aud, "prompt": f"items/{it['id']}__judge.md", "report": f"reports/{it['id']}__judge.md",
                      "ruling": {d: {"score": v[0], "evidence": v[1]} for d, v in js.items()}},
            "findings": {}, "rows": sum(cnt.values()), "ticked_by_list": [f"{cfg['models']['a']}/{it['id']}__a", f"{cfg['models']['b']}/{it['id']}__b"],
        })
    verdict = ros.get("verdict", "")
    data = {
        "version": 5, "kind": "edu_lines",
        "scoring": {"scale": {str(k): v.split("：", 1)[1] for k, v in enumerate(cfg["scoring"][:4])},
                    "evidence_rule": cfg["scoring"][4], "disagreement": cfg["scoring"][5]},
        "adjudicator": {"runner": "claude", "model": cfg["models"]["judge"]},
        "id": run.name, "chain": f"{topic_dir.name}/lines", "loop": ros["round"], "max_loops": cfg["max_rounds"],
        "parent": ros.get("after") or "", "title": f"{topic_dir.name} · 台词审（口播＋屏幕文字）第 {ros['round']} 轮",
        "target": rel(topic_dir), "episode": topic_dir.name, "stage": "lines", "stage_name": "台词审（口播＋屏幕文字 × 中英）",
        "scenes": [], "created_at": ros.get("created_at", ""), "author": "Claude Code", "known": "",
        "changes": (run / "previous.md").read_text(encoding="utf-8")[:4000] if (run / "previous.md").exists() else "",
        "items": items, "state": ros.get("state", "进行中"), "concluded_at": ros.get("concluded_at", ""),
        "result": "结果.md" if (run / "结果.md").exists() else "",
        "verdict": {"result": "可以配音、渲染" if verdict.startswith("通过") else ("不通过" if verdict else ""), "text": verdict},
        "log": ros.get("log", []),
    }
    nxt = run.parent / re.sub(r"_r\d+$", f"_r{ros['round'] + 1}", run.name)
    if nxt.exists():
        data["child"] = rel(nxt)
    (run / "checklist.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def issue_key(r: dict) -> str:
    import hashlib
    return hashlib.sha1("|".join([r["item"], r["src"], r["where"], r["dim"], r["issue"]]).encode()).hexdigest()[:12]


def now_iso() -> str:
    import datetime as dt
    return dt.datetime.now().isoformat(timespec="seconds")


def cmd_issues(run: Path) -> Path:
    """汇总三份报告 → issues.json（每条问题编号 I1…，带处理状态）＋ issues.md。已登记的处理按 key 保留。"""
    ros = json.loads((run / "roster.json").read_text(encoding="utf-8"))
    rows, summary = [], []
    lvl = {k: i for i, k in enumerate(LEVELS)}
    for it in ros["items"]:
        sc = {}
        for s in ("a", "b"):
            t = (run / "reports" / f"{it['id']}__{s}.md").read_text(encoding="utf-8")
            sc[s], rr, _ = parse_report(t, it["dims"])
            rows += [dict(r, item=it["id"], src=s) for r in rr]
        jt = run / "reports" / f"{it['id']}__judge.md"
        js, rejected = {}, set()
        if jt.exists():
            text = jt.read_text(encoding="utf-8")
            js, jrows, _ = parse_report(text, [], judge=True)
            rows += [dict(r, item=it["id"], src="judge") for r in jrows]
            rej = text.split("## 驳回", 1)[1] if "## 驳回" in text else ""
            # 驳回行如「- a · l39（…）：理由」「- b l03-l07 …：理由」：取开头的审稿位与位置
            # 驳回行如「- a · l39（…）：理由」：可能驳回问题本身，也可能只驳回某个改写——不自动判驳回，
            # 只把裁决人的话挂到对应条目上，由作者处理时决定（status=rejected 要用 fix 显式登记）
            rejected = []
            for m in re.finditer(r"^-\s*(?:\*\*)?\s*(?:([ab])\s*[·:]?\s*)?([^：:（(「]+)(.*)$", rej, re.M):
                for tok in re.findall(r"l\d+(?:\s*[-–～~]\s*l?\d+)?|agenda|outro|c_\w+|s\d+", m.group(2)):
                    rejected.append((m.group(1), tok.replace(" ", ""), (m.group(2) + m.group(3)).strip()))
        final = {d: (js[d][0] if d in js else min(sc["a"][d][0], sc["b"][d][0])) for d in it["dims"]}
        for r in rows:
            if r["item"] == it["id"] and r["src"] != "judge":
                notes = [txt for slot, tok, txt in rejected
                         if slot in (None, r["src"]) and (tok == r["where"].replace(" ", "") or r["where"].startswith(tok))]
                if notes:
                    r["judge_note"] = "；".join(dict.fromkeys(notes))
        summary.append({"item": it["id"], "name": it["name"], "final": final,
                        "scores": {"a": {d: sc["a"][d][0] for d in it["dims"]}, "b": {d: sc["b"][d][0] for d in it["dims"]},
                                   "judge": {d: v[0] for d, v in js.items()}}})
    num = lambda w: int(m.group(1)) if (m := re.search(r"l(\d+)", w)) else -1
    rows.sort(key=lambda r: (r["item"], num(r["where"]), lvl[r["level"]]))
    jp = run / "issues.json"
    old = {x["key"]: x for x in json.loads(jp.read_text(encoding="utf-8"))["issues"]} if jp.exists() else {}
    issues = []
    for i, r in enumerate(rows, 1):
        k = issue_key(r)
        prev = old.get(k, {})
        issues.append({"id": f"I{i}", "key": k, "item": r["item"], "where": r["where"], "dim": r["dim"], "level_zh": r["level"],
                       "level": UI_LEVEL[r["level"]], "law": "lines", "category": ITEM_NAME.get(r["item"], r["item"]),
                       "dimension": r["dim"], "shots": [r["where"]], "evidence": [r["orig"]] if r["orig"] else [],
                       "sources": [{"a": "a 位（Claude）", "b": "b 位（Codex）", "judge": "裁决人"}[r["src"]]],
                       "fix": r["fix"], "cost": "便宜",
                       "src": r["src"], "orig": r["orig"], "problem": r["issue"], "suggest": r["fix"],
                       "judge_note": r.get("judge_note", ""),
                       "status": prev.get("status") or "open", "solution": prev.get("solution", ""),
                       "reason": prev.get("reason", ""), "files": prev.get("files", []), "history": prev.get("history", [])})
    data = {"run": run.name, "round": ros["round"], "generated_at": now_iso(), "items": summary, "issues": issues}
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    p = write_issues_md(run, data)
    write_checklist(run)
    for x in summary:
        print(x["item"], " ".join(f"{d}={v}" for d, v in x["final"].items()), "通过" if item_ok(x, issues) else "不通过")
    print(f"{rel(p)}：{len(issues)} 条")
    return p


def item_ok(x: dict, issues: list[dict]) -> bool:
    must = [i for i in issues if i["item"] == x["item"] and i["level_zh"] == "必改" and i["status"] == "open"]
    return all(v >= 2 for v in x["final"].values()) and not must


def write_issues_md(run: Path, data: dict) -> Path:
    esc = lambda s: str(s).replace("|", "｜").replace("\n", " ")
    issues = data["issues"]
    cnt = {k: sum(i["status"] == k for i in issues) for k in STATUS}
    out = [f"# 台词审汇总：{run.name}", "",
           "处理状态：" + " · ".join(f"{STATUS[k]} {v}" for k, v in cnt.items())
           + "（`python tools/edu_review.py fix` 登记；下一轮审稿人按「处理」列逐条复核）", "",
           "## 各项结论（最终分：裁决过的维度用裁决分，其余取两人较低分）", "",
           "| 项 | 最终分 | 未处理的必改 | 结论 |", "|---|---|---|---|"]
    for x in data["items"]:
        must = sum(1 for i in issues if i["item"] == x["item"] and i["level_zh"] == "必改" and i["status"] == "open")
        out.append(f"| {x['item']} | " + " ".join(f"{d}={v}" for d, v in x["final"].items())
                   + f" | {must} | {'通过' if item_ok(x, issues) else '不通过'} |")
    out += ["", "## 问题（来源 a = Claude、b = Codex、judge = 裁决补充）", "",
            "| 编号 | 项 | 位置 | 维度 | 级别 | 来源 | 原文 | 问题 | 建议改写 | 裁决人意见 | 处理 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i in issues:
        h = STATUS[i["status"]] + (f"：{i['solution']}" if i["solution"] else "") + (f"（理由：{i['reason']}）" if i["reason"] else "")
        out.append(f"| {i['id']} | {i['item']} | {i['where']} | {i['dim']} | {i['level_zh']} | {i['src']} | {esc(i['orig'])} | "
                   f"{esc(i['problem'])} | {esc(i['suggest'])} | {esc(i.get('judge_note', ''))} | {esc(h)} |")
    p = run / "issues.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    return p


def cmd_fix(run: Path, ids: list[str], item: str | None, where: list[str], status: str, solution: str, reason: str,
            files: list[str]) -> None:
    """登记处理：按编号（--ids I3,I7）或按「项＋位置」（--item screen_zh --where l47）批量登记；驳回的条目只按编号改。"""
    jp = run / "issues.json"
    data = json.loads(jp.read_text(encoding="utf-8"))
    hit = []
    for i in data["issues"]:
        by_id = i["id"] in ids
        by_where = bool(where) and item in (None, "*", i["item"]) and any(
            w == i["where"] or re.match(rf"{re.escape(w)}(?!\d)", i["where"]) for w in where)
        if by_id or (by_where and i["status"] != "rejected"):
            i["history"].append({"at": now_iso(), "status": i["status"], "solution": i["solution"]})
            i.update(status=status, solution=solution, reason=reason, files=sorted(set(i["files"]) | set(files)))
            hit.append(i["id"])
    if not hit:
        raise SystemExit("没有匹配的问题")
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    write_issues_md(run, data)
    write_checklist(run)
    print(f"登记 {len(hit)} 条：{', '.join(hit[:40])}{' …' if len(hit) > 40 else ''}")


def cmd_conclude(run: Path, note: str) -> Path:
    """收轮：结果.md（各项最终分、处理统计、还没处理的问题、结论）＋ roster 状态「已收轮」。"""
    data = json.loads((run / "issues.json").read_text(encoding="utf-8"))
    ros = json.loads((run / "roster.json").read_text(encoding="utf-8"))
    issues = data["issues"]
    open_ = [i for i in issues if i["status"] == "open"]
    passed = [x["item"] for x in data["items"] if item_ok(x, issues) and all(v >= 2 for v in x["final"].values())]
    if len(passed) == len(data["items"]):
        verdict = "通过：可以配音、渲染"
    else:
        last = ros["round"] >= json.loads(LINE_REVIEW.read_text(encoding="utf-8"))["max_rounds"]
        verdict = f"不通过：{len(data['items']) - len(passed)} 项未过" + (
            f"；还有 {len(open_)} 条没处理" if open_ else
            ("；已到轮数上限，余下问题已按问题清单修改，由程序检验复核成片" if last else "；已按问题清单修改，开下一轮复核"))
    cnt = {k: sum(i["status"] == k for i in issues) for k in STATUS}
    out = [f"# 结果：{run.name}（第 {ros['round']} 轮）", "", f"**结论**：{verdict}", ""] + ([note, ""] if note else []) + [
        "## 各项最终分", "", "| 项 | 名称 | 最终分 | 结论 |", "|---|---|---|---|"]
    out += [f"| {x['item']} | {x['name']} | " + " ".join(f"{d}={v}" for d, v in x["final"].items())
            + f" | {'通过' if x['item'] in passed else '不通过'} |" for x in data["items"]]
    out += ["", "## 处理统计", "", " · ".join(f"{STATUS[k]} {v}" for k, v in cnt.items()), ""]
    if open_:
        out += ["## 还没处理的问题", ""] + [f"- {i['id']} {i['item']} {i['where']}（{i['level_zh']}）：{i['problem']}" for i in open_]
    p = run / "结果.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    ros.update(state="已收轮", concluded_at=now_iso(), verdict=verdict)
    (run / "roster.json").write_text(json.dumps(ros, ensure_ascii=False, indent=1), encoding="utf-8")
    write_checklist(run)
    print(f"{rel(p)}：{verdict}")
    return p


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate"); p.add_argument("topic", type=Path); p.add_argument("--lang", default="all")
    p = sub.add_parser("brief"); p.add_argument("topic", type=Path); p.add_argument("--stage", choices=("script", "cut"), required=True)
    p.add_argument("--after", type=Path, help="上一轮审稿目录：任务书带上它的 issues.md，加复核项")
    p = sub.add_parser("merge"); p.add_argument("run", type=Path)
    p = sub.add_parser("new", help="台词审 v2：口播＋屏幕文字，中英分审，双审＋裁决")
    p.add_argument("topic", type=Path); p.add_argument("--after", type=Path)
    p.add_argument("--chain", default="lines", help="审查链名：讲稿大改（如重写结构）后另起一条，轮数从 1 计，如 lines5")
    p = sub.add_parser("lint", help="口语黑名单：讲稿与章节标题里的书面腔、名词硬拼、目录腔"); p.add_argument("topic", type=Path)
    p = sub.add_parser("check"); p.add_argument("run", type=Path)
    p = sub.add_parser("issues"); p.add_argument("run", type=Path)
    p = sub.add_parser("fix", help="登记问题的处理（写进审查单 issues.json / issues.md）")
    p.add_argument("run", type=Path); p.add_argument("--ids", default="", help="I3,I7")
    p.add_argument("--item", help="voice_zh / voice_en / screen_zh / screen_en / *")
    p.add_argument("--where", default="", help="位置，逗号分隔，如 l47,agenda")
    p.add_argument("--status", choices=list(STATUS), default="implemented"); p.add_argument("--solution", default="")
    p.add_argument("--reason", default=""); p.add_argument("--file", action="append", default=[])
    p = sub.add_parser("conclude", help="收轮：结果.md＋状态「已收轮」"); p.add_argument("run", type=Path); p.add_argument("--note", default="")
    a = ap.parse_args()
    if a.cmd == "fix":
        cmd_fix(a.run.resolve(), [x for x in a.ids.split(",") if x], a.item, [x for x in a.where.split(",") if x], a.status,
                a.solution, a.reason, a.file); return
    if a.cmd == "conclude":
        cmd_conclude(a.run.resolve(), a.note); return
    if a.cmd == "merge":
        cmd_merge(a.run.resolve()); return
    if a.cmd == "check":
        sys.exit(1 if cmd_check(a.run.resolve()) else 0)
    if a.cmd == "issues":
        cmd_issues(a.run.resolve()); return
    if a.cmd == "new":
        cmd_new(a.topic.resolve(), a.after.resolve() if a.after else None, a.chain); return
    if a.cmd == "lint":
        hits = lint_hits(a.topic.resolve(), "zh") + lint_hits(a.topic.resolve(), "en")
        print("\n".join(hits) or "口语黑名单：无可疑句"); return
    topic = a.topic.resolve()
    if a.cmd == "brief":
        cmd_brief(topic, a.stage, a.after.resolve() if a.after else None); return
    langs = list(ev.LANGS) if a.lang == "all" else [a.lang]
    sys.exit(cmd_validate(topic, langs))


if __name__ == "__main__":
    main()
