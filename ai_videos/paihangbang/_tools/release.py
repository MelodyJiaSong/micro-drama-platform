"""把每期的正式版（英文 + 中文）收进 `release/`，并生成预览页。

    python ai_videos/paihangbang/_tools/release.py           # 收录 / 刷新，生成预览页
    python ai_videos/paihangbang/_tools/release.py --check   # 只报告：缺片、与 render 不同步、渲染中

- 正式版默认是「稳妥版」`render/<期>_master.mp4` / `_master_zh.mp4`（README：推荐发布默认版）。
  某期改发风险版时，在系列根 `release_choices.json` 写 {"<期目录名>": "risk"}，再跑本脚本。
- 视频和封面用硬链接放进 `release/<期>/`，不占额外空间；render 下的文件不动，审片页、补配乐等工具照旧可用。
  render 里的文件被重渲（换了新文件）后，硬链接会指向旧内容，`--check` 会报「不同步」，再跑一次即刷新。
- 刚改过（2 分钟内）或 ffprobe 读不出时长的视频视为「渲染中」，本次不收录。
- **配图硬闸门**（follow-up 054，bible §4）：要发的版本过不了 `tile_gate.py`（有卡缺图 / 不合格 / 未经独立逐卡审图）的期不收录，
  已收录的视频与封面链接撤掉（render 下原文件不动），预览页标「⛔ 配图闸门未过」并列原因。
- 预览页：`release/index.html`（总览）与 `release/<期>/index.html`（单期：双语播放器、封面、发布稿、审片结论、待定事项），
  每次运行按当时的 publish.md / publish.zh.md / qc.md / README 重新生成。
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SERIES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tile_gate import gate  # noqa: E402
EPS = SERIES / "episodes"
OUT = SERIES / "release"
CHOICES = SERIES / "release_choices.json"
SETTLE_S = 120
COVER_FORMATS = {"": "16:9 横屏（随片）", "_4x3": "4:3 横屏", "_3x4": "3:4 竖屏"}   # 抖音上传页要横 4:3、竖 3:4 两张
COVER_STYLES = {1: "① 冠军大图", 2: "② 柱状对比", 3: "③ 悬念大字"}


# ---------- 收录 ----------

def sources(ep: Path, variant: str) -> dict[str, Path]:
    tag = "_with-risk-images" if variant == "risk" else ""
    r = ep / "render"
    # ep03：thumbnail.png 是稳妥版、另有 _with-risk-images；ep06：thumbnail.png 是带图版、稳妥版另存 _default
    special = r / ("thumbnail_with-risk-images.png" if variant == "risk" else "thumbnail_default.png")
    thumb_en = special if special.is_file() else r / "thumbnail.png"
    return {
        f"{ep.name}_en.mp4": r / f"{ep.name}_master{tag}.mp4",
        f"{ep.name}_zh.mp4": r / f"{ep.name}_master{tag}_zh.mp4",
        "thumbnail_en.png": thumb_en,
        "thumbnail_zh.png": r / "thumbnail_zh.png",
        **{f"covers_zh/cover_zh_{k}{s}.png": r / "covers_zh" / f"cover_zh_{k}{s}.png"
           for k in (1, 2, 3) for s in COVER_FORMATS},                                           # _tools/zh_covers.py
    }


def probe_duration(p: Path) -> float | None:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                             capture_output=True, text=True, timeout=60).stdout.strip()
        return float(out)
    except (ValueError, subprocess.SubprocessError, OSError):
        return None


def same_file(a: Path, b: Path) -> bool:
    try:
        sa, sb = a.stat(), b.stat()
    except OSError:
        return False
    return (sa.st_ino, sa.st_dev) == (sb.st_ino, sb.st_dev) and sa.st_ino != 0


def state(src: Path, dst: Path) -> str:
    if not src.is_file():
        return "missing"
    if src.suffix == ".mp4" and (time.time() - src.stat().st_mtime < SETTLE_S or probe_duration(src) is None):
        return "rendering"
    if same_file(src, dst):
        return "ok"
    return "stale" if dst.exists() else "new"


def link(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".tmp")
    tmp.unlink(missing_ok=True)
    try:
        os.link(src, tmp)
        how = "hardlink"
    except OSError:
        shutil.copy2(src, tmp)
        how = "copy"
    try:
        tmp.replace(dst)
    except PermissionError:          # 预览页正在播放旧链接：先删再放
        dst.unlink()
        tmp.replace(dst)
    return how


# ---------- 读资料 ----------

def md_sections(text: str) -> list[tuple[str, str]]:
    out, head, buf = [], "", []
    for ln in text.splitlines():
        if ln.startswith("## "):
            if head or any(x.strip() for x in buf):
                out.append((head, "\n".join(buf).strip()))
            head, buf = ln[3:].strip(), []
        else:
            buf.append(ln)
    out.append((head, "\n".join(buf).strip()))
    return out


def first_code(body: str) -> str:
    m = re.search(r"```[a-z]*\n(.*?)\n```", body, re.S)
    return m.group(1) if m else ""


def en_title(pub: str) -> str:
    for head, body in md_sections(pub):
        if head == "Title":
            return next((x for x in body.splitlines() if x.strip() and not x.startswith("（")), "")
    return ""


def zh_title(pubzh: str) -> str:
    for head, body in md_sections(pubzh):
        if head.startswith("抖音"):
            return first_code(body).strip()
    return ""


def readme_notes(ep_id: str) -> dict[str, str | list[str]]:
    readme = (SERIES / "README.md").read_text(encoding="utf-8")
    short = ep_id.split("_")[0]
    notes: dict[str, str | list[str]] = {"pending": [], "status": ""}
    for ln in readme.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if ln.lstrip().startswith(f"| {short} |") and len(cells) >= 7:     # ep11–ep20 状态表
            notes["status"] = f"图片：{cells[5]}；配乐：{cells[4]}"
            notes["pending"].append(cells[6])
        elif ln.startswith("| ") and len(cells) >= 3 and cells[0].isdigit() and short in cells[1]:   # 发布前待定表
            notes["pending"].append(f"{cells[1]} —— 代理默认：{cells[2]}")
        elif ln.startswith("- ") and f" {short} " in ln[:12]:               # ep01–ep06 状态条目
            notes["status"] = re.sub(r"\*\*|`", "", ln[2:])
    return notes


def qc_summary(ep: Path) -> list[tuple[str, str]]:
    p = ep / "qc.md"
    if not p.is_file():
        return []
    secs = [s for s in md_sections(p.read_text(encoding="utf-8")) if s[0]]
    return secs[:3]


def facts(ep: Path) -> dict:
    d = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    items = d.get("items", [])
    champ = min(items, key=lambda r: r.get("rank", 999)) if items and d.get("mode") != "list" else None
    return {
        "kicker": d.get("kicker", ""), "metric": d.get("metric_label", ""), "period": d.get("period_label", ""),
        "n": len(items), "mode": d.get("mode", "rank"),
        "champion": f"{champ['name']}（{champ.get('value_display') or champ.get('value')}{'' if champ.get('value_display') else ' ' + d.get('unit', '')}）" if champ else "",
    }


# ---------- 页面 ----------

CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#16181d;--mute:#5d6470;--line:#e2e5ea;--acc:#2f6fed;--ok:#1d8a4e;--warn:#b26a00;--bad:#c4372f;--code:#f1f3f6}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--card:#1b1e23;--ink:#e8eaee;--mute:#9aa1ad;--line:#2b2f36;--acc:#6c9bff;--ok:#4cc483;--warn:#f0a73a;--bad:#ff6b61;--code:#23272e}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
main{max-width:1240px;margin:0 auto;padding:24px 16px 64px}a{color:var(--acc)}h1{font-size:24px;margin:0 0 4px}h2{font-size:18px;margin:28px 0 10px}h3{font-size:15px;margin:18px 0 6px}
.sub{color:var(--mute)}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:820px){.two{grid-template-columns:1fr}}
video,img.thumb{width:100%;border-radius:8px;background:#000;display:block}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}.chip{border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:13px;color:var(--mute)}
.ok{color:var(--ok)}.warn{color:var(--warn)}.bad{color:var(--bad)}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{color:var(--mute);font-weight:500;white-space:nowrap}
pre{background:var(--code);border-radius:8px;padding:12px;white-space:pre-wrap;word-break:break-word;font:13px/1.55 ui-monospace,Consolas,monospace;margin:0}
.code{position:relative;margin:8px 0}.copy{position:absolute;top:6px;right:6px;font-size:12px;padding:2px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink);cursor:pointer}
details{margin:8px 0}summary{cursor:pointer;font-weight:600}code{background:var(--code);padding:0 4px;border-radius:4px;font-size:13px}
.tabs{display:flex;gap:8px;margin:20px 0 0;flex-wrap:wrap}.tabs button{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:6px 14px;cursor:pointer}.tabs button.on{border-color:var(--acc);color:var(--acc)}
.pane{display:none}.pane.on{display:block}ul{padding-left:20px;margin:6px 0}
"""

JS = """
function cp(b){const t=b.nextElementSibling.innerText;const done=()=>{b.textContent='已复制';setTimeout(()=>b.textContent='复制',1200)};
if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,()=>fb(t,done))}else fb(t,done)}
function fb(t,done){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();done()}
function tab(id){document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('on',p.id===id));document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.t===id))}
"""

e = html.escape


def inline(s: str) -> str:
    s = e(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def md(text: str) -> str:
    out, lst, para = [], False, []

    def flush():
        nonlocal lst
        if para:
            out.append("<p>" + "<br>".join(inline(x) for x in para) + "</p>")
            para.clear()
        if lst:
            out.append("</ul>")
            lst = False

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append('<div class="code"><button class="copy" onclick="cp(this)">复制</button><pre>'
                       + e("\n".join(lines[i + 1:j])) + "</pre></div>")
            i = j + 1
            continue
        if ln.startswith("#"):
            flush()
            out.append(f"<h3>{inline(ln.lstrip('#').strip())}</h3>")
        elif re.match(r"\s*[-*] ", ln):
            if para:
                flush()
            if not lst:
                out.append("<ul>")
                lst = True
            item = re.sub(r"^\s*[-*] ", "", ln)
            out.append(f"<li>{inline(item)}</li>")
        elif ln.startswith(">"):
            flush()
            out.append(f'<p class="sub">{inline(ln.lstrip("> "))}</p>')
        elif ln.startswith("|"):
            flush()
            out.append(f"<p><code>{e(ln)}</code></p>")
        elif not ln.strip():
            flush()
        else:
            if lst:
                flush()
            para.append(ln)
        i += 1
    flush()
    return "\n".join(out)


def page(title: str, body: str) -> str:
    return (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{e(title)}</title><style>{CSS}</style></head><body><main>{body}</main><script>{JS}</script></body></html>")


def fmt_dur(s: float | None) -> str:
    return "—" if s is None else f"{int(s) // 60}:{int(s) % 60:02d}"


def mark(st: str) -> str:
    return {"ok": '<span class="ok">✅ 已收录</span>', "missing": '<span class="bad">⛔ 尚未生成</span>',
            "rendering": '<span class="warn">⏳ 渲染中，下次运行再收录</span>',
            "stale": '<span class="warn">⚠ 与 render 不同步</span>', "new": '<span class="warn">⚠ 未收录</span>',
            "blocked": '<span class="warn">⛔ 配图闸门未过，不发</span>'}.get(st, st)


def episode_page(ep: Path, info: dict) -> str:
    pub = (ep / "publish.md").read_text(encoding="utf-8") if (ep / "publish.md").is_file() else ""
    pubzh = (ep / "publish.zh.md").read_text(encoding="utf-8") if (ep / "publish.zh.md").is_file() else ""
    f, notes, rel = info["facts"], info["notes"], f"../../episodes/{ep.name}"
    synth = re.search(r"Altered or synthetic content」：(.*?)→ 选 (Yes|No)", pub)
    music = next((ln for ln in first_code(next((b for h, b in md_sections(pub) if h.startswith("Description")), "")).splitlines()
                  if ln.startswith("Music:")), "")
    if not music:
        man = ep / "render" / f"{ep.name}_master{'_with-risk-images' if info['variant'] == 'risk' else ''}.manifest.json"
        tracks = json.loads(man.read_text(encoding="utf-8")).get("inputs", {}).get("music") if man.is_file() else None
        music = (f"母版已配乐（{len(tracks)} 段，见 manifest）；⚠ publish.md 描述框缺配乐署名，上传前补一行" if tracks
                 else "⚠ manifest 没有配乐记录（可能是静音版）")
    variant = "带风险图版（release_choices.json 指定）" if info["variant"] == "risk" else "稳妥版（默认）"
    risk_alt = ep / "render" / f"{ep.name}_master_with-risk-images.mp4"

    def player(lang: str, label: str) -> str:
        v = info["files"][f"{ep.name}_{lang}.mp4"]
        poster = f"thumbnail_{lang}.png" if info["files"][f"thumbnail_{lang}.png"]["state"] == "ok" else ""
        vid = (f'<video controls preload="metadata" src="{ep.name}_{lang}.mp4" poster="{poster}"></video>' if v["state"] == "ok"
               else f'<div class="card sub" style="aspect-ratio:16/9;display:grid;place-items:center">{mark(v["state"])}</div>')
        return (f'<div class="card"><h3 style="margin-top:0">{label}</h3>{vid}<table style="margin-top:8px">'
                f'<tr><th>文件</th><td><code>{ep.name}_{lang}.mp4</code> {mark(v["state"])}</td></tr>'
                f'<tr><th>时长 / 大小</th><td>{fmt_dur(v["duration"])} · {v["size_mb"]} MB</td></tr>'
                f'<tr><th>来源</th><td><code>render/{e(v["src"])}</code></td></tr>'
                f'<tr><th>封面</th><td>{"<a href=thumbnail_" + lang + ".png>thumbnail_" + lang + ".png</a>" if poster else mark(info["files"]["thumbnail_" + lang + ".png"]["state"])}</td></tr></table></div>')

    covers = cover_rows(info, "")
    g = info.get("gate") or {}
    gate_html = "" if g.get("ok", True) else (
        '<div class="card"><h3 style="margin-top:0">⛔ 配图闸门未过：本期不发</h3><ul>'
        + "".join(f"<li>#{r} {e(n)}：{e(w)}</li>" for r, n, w in sorted(g["fails"]))
        + "".join(f"<li>合同错误：{e(m)}</li>" for m in g["errors"])
        + (f"<li>{len(g['pending'])} 张图待独立逐卡审图（<code>tile_gate.py sheet</code> → 独立审图人 <code>record</code>）</li>" if g["pending"] else "")
        + "</ul>" + (f"<p>可从榜尾截短到 Top {g['cut']} 后重渲。</p>" if g.get("cut") else "")
        + f"<p class=\"sub\"><code>python ai_videos/paihangbang/_tools/tile_gate.py check {e(ep.name)}</code></p></div>")
    chips = [f["kicker"], f"{f['n']} 条", f["metric"], f["period"], variant]
    if f["champion"]:
        chips.insert(1, "冠军 " + f["champion"])
    pend = "".join(f"<li>{inline(x)}</li>" for x in notes["pending"]) or "<li class='sub'>README 里没有列待定事项</li>"
    qc = "".join(f"<details{' open' if k == 0 else ''}><summary>{inline(h)}</summary>{md(b)}</details>" for k, (h, b) in enumerate(info["qc"]))
    body = f"""
<p class="sub"><a href="../index.html">← 全部正式版</a></p>
<h1>{e(ep.name)}</h1>
<div style="font-size:18px">{e(info['en_title'])}</div><div style="font-size:18px">{e(info['zh_title'])}</div>
<div class="chips">{''.join(f'<span class="chip">{inline(c)}</span>' for c in chips if c)}</div>
{gate_html}<div class="two">{player('en', '英文 · YouTube')}{player('zh', '中文 · 抖音 / B站 / 视频号等')}</div>
<h2>中文封面候选</h2>
{covers}
<h2>上传前要点</h2>
<div class="card"><table>
<tr><th>AI 合成内容声明</th><td>{('YouTube 选 <b>' + synth.group(2) + '</b>：' + inline(synth.group(1))) if synth else '见发布稿清单'}</td></tr>
<tr><th>配乐</th><td>{inline(music) or '—'}</td></tr>
<tr><th>状态</th><td>{inline(str(notes['status'])) or '—'}</td></tr>
<tr><th>待你决定</th><td><ul>{pend}</ul></td></tr>
<tr><th>风险版</th><td>{('另有 <code>render/' + risk_alt.name + '</code>，未收录（含授权不明或全景自由风险图，签字前不发）') if risk_alt.is_file() and info['variant'] != 'risk' else '—'}</td></tr>
<tr><th>源文件</th><td><a href="{rel}/publish.md">publish.md</a> · <a href="{rel}/publish.zh.md">publish.zh.md</a> · <a href="{rel}/qc.md">qc.md</a> · <a href="{rel}/sources.md">sources.md</a> · <a href="{rel}/render/">render/</a></td></tr>
</table></div>
<div class="tabs"><button data-t="yt" class="on" onclick="tab('yt')">YouTube 发布稿</button><button data-t="cn" onclick="tab('cn')">国内平台发布稿</button><button data-t="qc" onclick="tab('qc')">审片结论</button></div>
<div class="pane on card" id="yt">{md(pub) if pub else '<p class="sub">没有 publish.md</p>'}</div>
<div class="pane card" id="cn">{md(pubzh) if pubzh else '<p class="sub">没有 publish.zh.md</p>'}</div>
<div class="pane card" id="qc"><p class="sub">qc.md 最新三节（全文见 <a href="{rel}/qc.md">qc.md</a>）</p>{qc or '<p class="sub">没有 qc.md</p>'}</div>
<p class="sub" style="margin-top:24px">生成于 {info['generated']} · <code>python ai_videos/paihangbang/_tools/release.py</code> 重新生成</p>"""
    return page(f"{ep.name.split('_')[0]} 正式版", body)


def index_page(rows: list[dict], generated: str) -> str:
    cards = []
    for r in rows:
        st = {k: v["state"] for k, v in r["files"].items()}
        en, zh = st[f"{r['ep']}_en.mp4"], st[f"{r['ep']}_zh.mp4"]
        thumb = "<img class='thumb' src='" + r["ep"] + "/thumbnail_en.png' alt=''>" if st["thumbnail_en.png"] == "ok" else ""
        cards.append(f"""<a class="card" href="{r['ep']}/index.html" style="text-decoration:none;color:inherit">{thumb}
<div style="margin-top:8px;font-weight:600">{e(r['ep'].split('_')[0])} · {e(r['en_title'])}</div>
<div class="sub">{e(r['zh_title'])}</div>
<div class="chips"><span class="chip">英文 {mark(en)}</span><span class="chip">中文 {mark(zh)}</span>
<span class="chip">{fmt_dur(r['files'][r['ep'] + '_en.mp4']['duration'])}</span>{'<span class="chip">风险版</span>' if r['variant'] == 'risk' else ''}</div></a>""")
    ok = sum(1 for r in rows for k, v in r["files"].items() if k.endswith(".mp4") and v["state"] == "ok")
    body = (f"<h1>排行榜 · 正式版</h1><p class='sub'>{len(rows)} 期，已收录视频 {ok} / {len(rows) * 2}（英文 + 中文）。"
            "正式版 = 稳妥版（默认母版）；视频是 render 里的硬链接，不占额外空间。点卡片看单期预览与发布稿。"
            "<a href='covers_zh.html'>中文封面一页挑选 →</a></p>"
            f"<div class='grid'>{''.join(cards)}</div><p class='sub' style='margin-top:24px'>生成于 {generated}</p>")
    return page("排行榜正式版", body)


def cover_rows(info: dict, prefix: str, formats=tuple(COVER_FORMATS)) -> str:
    """一期的封面候选：每种尺寸一行（16:9 行带随片的现用封面）。prefix 是相对 release/ 的路径前缀。"""
    out = []
    for s in formats:
        cells = [("thumbnail_zh.png", "现用（随片渲染）")] if s == "" else []
        cells += [(f"covers_zh/cover_zh_{k}{s}.png", lab) for k, lab in COVER_STYLES.items()]
        html_cells = "".join(
            f'<a class="card" style="padding:8px" href="{prefix}{fn}" target="_blank"><img class="thumb" loading="lazy" src="{prefix}{fn}" alt="">'
            f'<div class="sub" style="margin-top:6px">{lab} · <code>{fn.split("/")[-1]}</code></div></a>'
            for fn, lab in cells if info["files"].get(fn, {}).get("state") == "ok")
        col = "minmax(0,1fr)"
        n = 4 if s == "" else 3
        width = "max-width:780px;" if s == "_3x4" else ""
        out.append(f'<h3>{COVER_FORMATS[s]}</h3><div class="grid" style="{width}grid-template-columns:repeat({n},{col})">{html_cells}</div>')
    return "".join(out)


def covers_page(rows: list[dict], generated: str) -> str:
    tabs, panes = [], []
    for s, lab in COVER_FORMATS.items():
        pid, on = "f" + (s or "169"), " on" if s == "" else ""
        tabs.append(f"<button data-t=\"{pid}\" class=\"{on.strip()}\" onclick=\"tab('{pid}')\">{lab}</button>")
        blocks = "".join(f'<h2><a href="{r["ep"]}/index.html">{e(r["ep"].split("_")[0])}</a> · {e(r["zh_title"])}</h2>'
                         + cover_rows(r, f'{r["ep"]}/', (s,)) for r in rows)
        panes.append(f'<div class="pane{on}" id="{pid}">{blocks}</div>')
    tabs = "".join(tabs)
    body = ("<p class='sub'><a href='index.html'>← 全部正式版</a></p><h1>中文封面挑选</h1>"
            "<p class='sub'>每期三款（① 冠军大图 ② 柱状对比 ③ 悬念大字），各出三种尺寸：16:9（1920×1080，和视频一样）、"
            "4:3 横屏（1440×1080）、3:4 竖屏（1080×1440）。抖音上传页的横封面用 4:3、竖封面用 3:4。点图看原尺寸；原图在 "
            "<code>episodes/&lt;期&gt;/render/covers_zh/</code>，用 <code>_tools/zh_covers.py</code> 重新生成。</p>"
            f"<div class='tabs'>{tabs}</div>" + "".join(panes)
            + f"<p class='sub' style='margin-top:24px'>生成于 {generated}</p>")
    return page("中文封面挑选", body)


# ---------- 主流程 ----------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只报告，不改 release/")
    a = ap.parse_args()
    choices = json.loads(CHOICES.read_text(encoding="utf-8")) if CHOICES.is_file() else {}
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    rows, problems = [], []
    episodes = sorted(p for p in EPS.iterdir() if (p / "data.json").is_file())
    for ep in episodes:
        variant = choices.get(ep.name, "default")
        g = gate(ep, variant)
        files = {}
        for name, src in sources(ep, variant).items():
            dst = OUT / ep.name / name
            st = state(src, dst) if g["ok"] else "blocked"
            if st == "blocked" and not a.check and dst.exists() and src.is_file():
                dst.unlink()                   # 闸门未过：撤掉收录（render 下原文件还在）
            if not a.check and st in ("new", "stale"):
                link(src, dst)
                st = "ok"
            if not a.check and st in ("missing", "rendering") and dst.exists() and not same_file(src, dst):
                dst.unlink()                   # 不留指向旧内容的链接
            if st != "ok":
                problems.append(f"{ep.name}/{name}: {st}")
            files[name] = {"src": src.name, "state": st,
                           "duration": probe_duration(dst) if st == "ok" and name.endswith(".mp4") else None,
                           "size_mb": round(src.stat().st_size / 1e6, 1) if src.is_file() else 0}
        pub = (ep / "publish.md").read_text(encoding="utf-8") if (ep / "publish.md").is_file() else ""
        pubzh = (ep / "publish.zh.md").read_text(encoding="utf-8") if (ep / "publish.zh.md").is_file() else ""
        info = {"ep": ep.name, "variant": variant, "files": files, "facts": facts(ep), "notes": readme_notes(ep.name),
                "gate": g, "qc": qc_summary(ep), "en_title": en_title(pub), "zh_title": zh_title(pubzh), "generated": generated}
        rows.append(info)
        if not a.check:
            (OUT / ep.name).mkdir(parents=True, exist_ok=True)
            (OUT / ep.name / "index.html").write_text(episode_page(ep, info), encoding="utf-8")
    if not a.check:
        known = {ep.name for ep in episodes}
        for d in OUT.iterdir():
            if d.is_dir() and d.name not in known:      # 已删的期
                shutil.rmtree(d)
        (OUT / "index.html").write_text(index_page(rows, generated), encoding="utf-8")
        (OUT / "covers_zh.html").write_text(covers_page(rows, generated), encoding="utf-8")
        (OUT / "release.json").write_text(json.dumps(
            [{"episode": r["ep"], "variant": r["variant"], "files": {k: {"src": v["src"], "state": v["state"]} for k, v in r["files"].items()}}
             for r in rows], indent=2, ensure_ascii=False), encoding="utf-8")
    ok = sum(1 for r in rows for k, v in r["files"].items() if k.endswith(".mp4") and v["state"] == "ok")
    print(f"{len(rows)} 期，视频 {ok}/{len(rows) * 2} 已{'同步' if a.check else '收录'}" + ("" if a.check else f" → {OUT / 'index.html'}"))
    for p in problems:
        print("  " + p)
    return 1 if a.check and problems else 0


if __name__ == "__main__":
    sys.exit(main())
