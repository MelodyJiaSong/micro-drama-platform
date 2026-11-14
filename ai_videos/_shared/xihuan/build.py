"""西幻资料库：校验 data/*.json，生成 library.json（管理 UI 契约）、条目卡片、prompt 文件、图鉴、STATUS 与图册。

只读写本地文件，不调用任何生成服务。出图用 gen_images.py（经 tools/codex_image.py 先记日志）。

    python ai_videos/_shared/xihuan/build.py          # 校验 + 重建派生文件
    python ai_videos/_shared/xihuan/build.py --check  # 只校验，派生文件过期也报错
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ENTRIES = ROOT / "entries"
CODEX = ROOT / "codex"
REVIEWS = ROOT / "qc" / "reviews.json"
VERSION = "1.2.0"

STYLE_FILE = ROOT / "prompt_styles.json"
FAMILIARITY = {"高", "中", "低"}
IP = {"generic": "通用类型词，可直接用", "inspired": "借鉴机制，名称与外观为本库原创", "public_domain": "神话/历史公有领域"}
REQUIRED = ["id", "name", "name_en", "summary", "xianxia", "visual", "familiarity", "ip"]
IMAGE_STATUS_ACCEPTED = {"reviewed", "reviewed_with_notes"}
BASIS = {"tradition": "欧洲传统", "genre": "现代类型（无传统原型）"}
FRANCHISE = re.compile(r"D&D|SRD|Pathfinder|魔兽|Warcraft|Dota|暗黑|英雄联盟|上古卷轴|猎魔人|龙腾|托尔金|指环王|冰与火|权力的游戏|时光之轮|战锤|魂系|艾尔登|万智牌|哈利|RPG|游戏|网文|网漫|短剧|现代奇幻|现代吸血鬼|现代女性向|IP 注意|日系|韩系|西幻通用|机制参考")
ADOPTION = {"locked": "锁定：跨剧一致，不改", "default": "默认：采用剧可改名改数值", "optional": "可选模块：采用剧可整块关闭"}
KIND = {"PL": "位面", "PS": "力量源", "SC": "魔法", "EL": "魔法", "HL": "魔法", "DK": "魔法", "PR": "魔法", "AU": "魔法",
        "EV": "事件", "FL": "事件", "TL": "头衔", "CL": "职业", "RC": "种族", "RS": "种族",
        "GF": "天赋", "GR": "成长", "IR": "道具", "CF": "工艺", "IT": "道具", "MT": "材料", "OR": "组织", "BS": "生物", "GD": "神祇"}


@dataclass(frozen=True)
class Group:
    order: int
    gid: str
    name: str
    intro: str
    subgroups: list[dict[str, Any]]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str, changed: list[str], check: bool) -> None:
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old == text:
        return
    changed.append(str(path.relative_to(ROOT)))
    if not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def png_size(path: Path) -> list[int] | None:
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return [int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")]


def load_groups() -> list[Group]:
    groups = []
    for path in sorted(DATA.glob("*.json")):
        raw = read_json(path)
        groups.append(Group(int(path.stem.split("_")[0]), raw["id"], raw["name"], raw.get("intro", ""), raw["subgroups"]))
    return groups


def validate(groups: list[Group], styles: dict[str, Any]) -> tuple[list[str], dict[str, dict[str, Any]]]:
    errors: list[str] = []
    entries: dict[str, dict[str, Any]] = {}
    for g in groups:
        for sub in g.subgroups:
            for e in sub["entries"]:
                missing = [k for k in REQUIRED if not e.get(k)]
                if missing:
                    errors.append(f"{e.get('id', '?')}: 缺字段 {missing}")
                if e.get("id") in entries:
                    errors.append(f"{e['id']}: ID 重复")
                if e.get("familiarity") not in FAMILIARITY:
                    errors.append(f"{e.get('id')}: familiarity 须为 高/中/低")
                if e.get("basis") not in BASIS:
                    errors.append(f"{e.get('id')}: basis 须为 {sorted(BASIS)}")
                elif e["basis"] == "tradition" and not any(not FRANCHISE.search(r["work"]) for r in e.get("references", [])):
                    errors.append(f"{e.get('id')}: 标为欧洲传统，但参考里没有非游戏/影视的传统来源")
                if e.get("adoption") not in ADOPTION:
                    errors.append(f"{e.get('id')}: adoption 须为 {sorted(ADOPTION)}")
                if e.get("adoption") == "optional" and not e.get("module"):
                    errors.append(f"{e.get('id')}: 可选条目须写 module")
                if e.get("id", "")[:2] not in KIND:
                    errors.append(f"{e.get('id')}: ID 前缀未登记")
                if e.get("ip") not in IP:
                    errors.append(f"{e.get('id')}: ip 须为 {sorted(IP)}")
                xx = e.get("xianxia") or {}
                if not isinstance(xx, dict) or not xx.get("concept"):
                    errors.append(f"{e.get('id')}: xianxia.concept 必填")
                img = e.get("image")
                if img and img.get("purpose") not in styles:
                    errors.append(f"{e.get('id')}: image.purpose 未在 prompt_styles.json 定义")
                if img and len(img.get("brief", "")) < 60:
                    errors.append(f"{e.get('id')}: image.brief 太短")
                e["_group"], e["_sub"] = g, sub
                entries[e["id"]] = e
    for e in entries.values():
        for r in e.get("relations", []):
            if r["target"] not in entries:
                errors.append(f"{e['id']}: 关系目标 {r['target']} 不存在")
    return errors, entries


def prompt_text(e: dict[str, Any], styles: dict[str, Any]) -> str:
    style = styles[e["image"]["purpose"]]
    return f"{style['prefix']}\n\n{e['image']['brief'].strip()}\n\n{style['suffix']}\n"


def image_state(e: dict[str, Any], reviews: dict[str, Any]) -> dict[str, Any]:
    v = e["image"].get("version", 1)
    folder = ENTRIES / e["id"].lower()
    anchor, prompt = folder / f"anchor_v{v}.png", folder / f"prompt_v{v}.txt"
    state: dict[str, Any] = {
        "anchor": str(anchor.relative_to(ROOT)).replace("\\", "/"),
        "prompt": str(prompt.relative_to(ROOT)).replace("\\", "/"),
        "purpose": e["image"]["purpose"], "sha256": None, "status": "planned",
    }
    if anchor.is_file():
        digest = sha256(anchor)
        state.update(sha256=digest, status="generated_unreviewed", actual_dimensions=png_size(anchor))
        review = reviews.get(e["id"])
        if review and review.get("sha256") == digest:
            state.update(status=review["status"], review_notes=review.get("notes", []), review_evidence=review.get("evidence"))
    return state


def backlinks(entries: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    back: dict[str, list[dict[str, str]]] = {k: [] for k in entries}
    for e in entries.values():
        for r in e.get("relations", []):
            back[r["target"]].append({"source": e["id"], "kind": KIND[e["id"][:2]], "role": r["role"]})
    return back


def ui_asset(e: dict[str, Any], state: dict[str, Any] | None, back: list[dict[str, str]]) -> dict[str, Any]:
    g, sub = e["_group"], e["_sub"]
    xx = e["xianxia"]
    return {
        "id": e["id"], "version": e.get("version", VERSION), "name": e["name"], "name_en": e["name_en"],
        "aliases": [e["name_en"], *e.get("aliases", [])], "category": f"{g.name}·{sub['name']}", "grade": e.get("tier"),
        "function": e["summary"], "cost_limit": e.get("cost", "见卡片"), "counter_failure": e.get("counter", "见卡片"),
        "visual_signature": e["visual"],
        "activation": {"trigger": e.get("trigger", "—"), "requirement": e.get("requirement", "—")},
        "parameters": "文中出现的数值都是默认值，采用剧可在自己的采用文件里改。",
        "relations": [{"target": r["target"], "kind": KIND[r["target"][:2]], "role": r["role"], "required": r.get("required", False), "note": r.get("note", "")} for r in e.get("relations", [])],
        "backlinks": back, "adoption": e["adoption"], "module": e.get("module"), "basis": e["basis"],
        "xianxia": xx, "familiarity": e["familiarity"], "ip": e["ip"], "references": e.get("references", []),
        "hooks": e.get("hooks", []), "details": e.get("details", {}),
        "image": state or {"anchor": f"entries/{e['id'].lower()}/anchor_v1.png", "prompt": "", "sha256": None, "status": "not_applicable", "purpose": "none"},
    }


def card(e: dict[str, Any], asset: dict[str, Any], names: dict[str, str]) -> str:
    adoption = ADOPTION[e["adoption"]] + (f"（模块：{e['module']}）" if e.get("module") else "")
    xx = e["xianxia"]
    lines = [f"# {e['id']} · {e['name']} / {e['name_en']}", "",
             f"> 由 `data/` 生成，勿手改。类别：{asset['category']}｜观众熟悉度：{e['familiarity']}｜{IP[e['ip']]}｜依据：{BASIS[e['basis']]}｜{adoption}", "",
             e["summary"], "", "| 项 | 内容 |", "|---|---|",
             f"| 仙侠参照 | **{xx['concept']}**{('：' + xx['note']) if xx.get('note') else ''} |"]
    for key, label in [("cost", "代价与限制"), ("counter", "克制与失效"), ("trigger", "触发"), ("requirement", "条件"), ("tier", "位阶")]:
        if e.get(key):
            lines.append(f"| {label} | {e[key]} |")
    for k, v in e.get("details", {}).items():
        lines.append(f"| {k} | {v if isinstance(v, str) else '；'.join(v)} |")
    lines.append(f"| 视觉 | {e['visual']} |")
    for k, v in e.get("screen", {}).items():
        lines.append(f"| 屏幕·{k} | {v} |")
    if e.get("hooks"):
        lines += ["", "## 剧作钩子", *[f"- {h}" for h in e["hooks"]]]
    if e.get("relations"):
        lines += ["", "## 关联", *[f"- {KIND[r['target'][:2]]} · {r['role']}：[{r['target']} {names[r['target']]}](../{r['target'].lower()}/card.md){(' — ' + r['note']) if r.get('note') else ''}" for r in e["relations"]]]
    if asset["backlinks"]:
        lines += ["", "## 被引用", *[f"- {b['kind']} [{b['source']} {names[b['source']]}](../{b['source'].lower()}/card.md)：{b['role']}" for b in asset["backlinks"]]]
    if e.get("references"):
        lines += ["", "## 参考作品（只借机制，不借专名）", *[f"- {r['work']}：{r['note']}" for r in e["references"]]]
    if asset["image"]["status"] != "not_applicable":
        img = asset["image"]
        lines += ["", "## 图像", f"状态：`{img['status']}`；用途：{img['purpose']}；prompt：[{Path(img['prompt']).name}]({Path(img['prompt']).name})"]
        if img.get("sha256"):
            lines += ["", f"![{e['name']}]({Path(img['anchor']).name})", "", f"SHA256 `{img['sha256']}`"]
        for n in img.get("review_notes", []):
            lines.append(f"- 审图：{n}")
    return "\n".join(lines) + "\n"


def codex_page(g: Group, assets: dict[str, dict[str, Any]]) -> str:
    lines = [f"# 图鉴 · {g.name}", "", "> 由 `data/` 生成，勿手改。点 ID 看完整卡片。", ""]
    if g.intro:
        lines += [g.intro, ""]
    for sub in g.subgroups:
        lines += [f"## {sub['name']}", ""]
        if sub.get("intro"):
            lines += [sub["intro"], ""]
        lines += ["| ID | 名称 | English | 一句话 | 仙侠参照 | 熟悉度 | 采用 |", "|---|---|---|---|---|---|---|"]
        for e in sub["entries"]:
            mode = {"locked": "锁定", "default": "默认", "optional": f"可选·{e.get('module', '')}"}[e["adoption"]]
            lines.append(f"| [{e['id']}](../entries/{e['id'].lower()}/card.md) | {e['name']} | {e['name_en']} | {e['summary']} | {e['xianxia']['concept']} | {e['familiarity']} | {mode} |")
        lines.append("")
    return "\n".join(lines)


def status_md(assets: list[dict[str, Any]], groups: list[Group]) -> str:
    imgs = [a for a in assets if a["image"]["status"] != "not_applicable"]
    counts: dict[str, int] = {}
    for a in imgs:
        counts[a["image"]["status"]] = counts.get(a["image"]["status"], 0) + 1
    lines = ["# 完成与验收状态", "", f"由 build.py 生成于 {datetime.now(timezone.utc).date().isoformat()}。条目 {len(assets)}；计划出图 {len(imgs)}；"
             f"已有图 {sum(1 for a in imgs if a['image']['sha256'])}；已验收 {sum(1 for a in imgs if a['image']['status'] in IMAGE_STATUS_ACCEPTED)}。", "",
             "验收绑定当前 PNG 的 SHA256；换图即回到待验收。", "", "| 图片状态 | 数量 |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    lines += ["", "| 大类 | 条目 | 计划图 | 有图 | 已验收 |", "|---|---:|---:|---:|---:|"]
    for g in groups:
        ga = [a for a in assets if a["category"].startswith(g.name + "·")]
        gi = [a for a in ga if a["image"]["status"] != "not_applicable"]
        lines.append(f"| {g.name} | {len(ga)} | {len(gi)} | {sum(1 for a in gi if a['image']['sha256'])} | {sum(1 for a in gi if a['image']['status'] in IMAGE_STATUS_ACCEPTED)} |")
    pending = [a for a in imgs if a["image"]["status"] not in IMAGE_STATUS_ACCEPTED]
    if pending:
        lines += ["", "## 待处理", "", *[f"- {a['id']} {a['name']}：`{a['image']['status']}`" for a in pending]]
    return "\n".join(lines) + "\n"


def gallery(lib: dict[str, Any]) -> str:
    data = json.dumps([{k: a[k] for k in ("id", "name", "name_en", "category", "function", "visual_signature", "xianxia", "familiarity")} | {"img": a["image"]["anchor"] if a["image"]["sha256"] else "", "status": a["image"]["status"]} for a in lib["assets"]], ensure_ascii=False)
    return f"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>西幻图册</title><style>
:root{{--bg:#f6f4ef;--fg:#1d1b18;--card:#fff;--mute:#6b665d;--line:#ddd6c8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16150f;--fg:#ece7dc;--card:#211f19;--mute:#a59e90;--line:#3a362c}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif}} header{{padding:16px;position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line)}}
input,select{{font:inherit;padding:6px 8px;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:6px;max-width:100%}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;padding:16px}}
.c{{background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}} .c img{{width:100%;aspect-ratio:1;object-fit:cover;background:#888;display:block}}
.ph{{aspect-ratio:1;display:grid;place-items:center;color:var(--mute)}} .b{{padding:8px 10px}} .b small{{color:var(--mute);display:block}}
</style></head><body><header><b>{html.escape(lib['title'])}</b> v{lib['version']} ·
<input id="q" placeholder="搜索名称/英文/仙侠对应"> <select id="cat"><option value="">全部类别</option></select> <span id="n"></span></header><main id="g"></main>
<script>const D={data};const g=document.getElementById('g'),q=document.getElementById('q'),cat=document.getElementById('cat'),n=document.getElementById('n');
[...new Set(D.map(a=>a.category))].forEach(c=>{{const o=document.createElement('option');o.value=o.textContent=c;cat.appendChild(o)}});
function esc(s){{return String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]))}}
function r(){{const t=q.value.toLowerCase();const L=D.filter(a=>(!cat.value||a.category===cat.value)&&(!t||[a.id,a.name,a.name_en,a.function,a.xianxia.concept].join(' ').toLowerCase().includes(t)));n.textContent=L.length+' 项';
g.innerHTML=L.map(a=>`<a class="c" href="entries/${{a.id.toLowerCase()}}/card.md" style="color:inherit;text-decoration:none">${{a.img?`<img loading="lazy" src="${{a.img}}" alt="">`:`<div class="ph">${{esc(a.status)}}</div>`}}<div class="b"><b>${{esc(a.name)}}</b> ${{esc(a.name_en)}}<small>${{esc(a.category)}} · 仙侠：${{esc(a.xianxia.concept)}}</small>${{esc(a.function)}}</div></a>`).join('')}}
q.oninput=cat.onchange=r;r();</script></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    styles = read_json(STYLE_FILE)
    groups = load_groups()
    errors, entries = validate(groups, styles)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    template = read_json(ROOT / "adoption_template.json")
    modules = {e["module"] for e in entries.values() if e.get("module")}
    bad = [f"{name}:{i}" for name, pack in template["presets"].items() for i in pack["entries"] if i not in entries]
    bad += [f"模块 {m} 未在模板 modules 中" for m in modules if m not in template["modules"]]
    if bad:
        print("adoption_template.json 有误：" + "，".join(bad), file=sys.stderr)
        return 1
    reviews = read_json(REVIEWS) if REVIEWS.is_file() else {}
    changed: list[str] = []
    names = {k: v["name"] for k, v in entries.items()}
    back = backlinks(entries)
    assets, by_id, stale = [], {}, []
    for e in entries.values():
        state = None
        if e.get("image"):
            folder = ENTRIES / e["id"].lower()
            v = e["image"].get("version", 1)
            prompt_file, text = folder / f"prompt_v{v}.txt", prompt_text(e, styles)
            if (folder / f"anchor_v{v}.png").is_file() and prompt_file.is_file():
                if e["image"]["brief"].strip() not in prompt_file.read_text(encoding="utf-8"):
                    stale.append(e["id"])  # 已出图的 prompt 是请求记录，不覆盖；改描述要升 image.version
            else:
                write_text(prompt_file, text, changed, args.check)
            state = image_state(e, reviews)
        a = ui_asset(e, state, back[e["id"]])
        assets.append(a)
        by_id[e["id"]] = a
        write_text(ENTRIES / e["id"].lower() / "card.md", card(e, a, names), changed, args.check)
    lib = {
        "schema_version": 1, "version": VERSION, "title": "西幻公共资料库", "generated_by": "build.py（源为 data/*.json，勿手改）",
        "scope": "欧美奇幻世界的力量源、魔法学派、头衔与威胁度、职业、种族、成长、道具、组织、位面与生物；每条附仙侠对应。不含剧情与具体人物。",
        "navigation": [{"id": g.gid, "name": g.name, "children": [{"id": s["id"], "name": s["name"], "asset_ids": [e["id"] for e in s["entries"]]} for s in g.subgroups]} for g in groups],
        "assets": assets,
    }
    write_text(ROOT / "library.json", json.dumps(lib, ensure_ascii=False, indent=1) + "\n", changed, args.check)
    for g in groups:
        write_text(CODEX / f"{g.order:02d}_{g.gid}.md", codex_page(g, by_id), changed, args.check)
    write_text(ROOT / "index.html", gallery(lib), changed, args.check)
    status = status_md(assets, groups)
    old_status = (ROOT / "STATUS.md").read_text(encoding="utf-8") if (ROOT / "STATUS.md").is_file() else ""
    if old_status.split("\n", 3)[3:] != status.split("\n", 3)[3:]:
        write_text(ROOT / "STATUS.md", status, changed, args.check)
    if stale:
        print(f"描述已改但图仍是旧版（升 image.version 重出，或改回描述）：{', '.join(stale)}", file=sys.stderr)
    print(f"条目 {len(assets)}；计划图 {sum(1 for a in assets if a['image']['status'] != 'not_applicable')}；{'过期' if args.check else '更新'} {len(changed)} 个文件")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
