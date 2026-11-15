# -*- coding: utf-8 -*-
"""t02 黄仁勋辞任英伟达 CEO：网页场景用的全部数据，写成 scenes/data.json。

    python edu_videos/redian_xiangying/t02_jensen_huang_resigns/scenes/data.py

画面上的每个数字、日期、引语都从 claims.json 取，并在这里断言：台账一改、和画面对不上，就在这里报错，先改画面再出片。
另外检查红线（research/dossier.md §6.1、§6.2）：data.json 与 scenes/web/ 下所有文件不得出现两位女性当事人的名字、
那家新加坡公司的名字，以及「女间谍」「美人计」「渗透」「intelligence asset」字样。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = HERE.parent
CLAIMS = {c["id"]: c for c in json.loads((TOPIC / "claims.json").read_text(encoding="utf-8"))["claims"]}
WEB = HERE / "web"

# 红线：屏幕与数据里一律不得出现（大小写不敏感）
BANNED = ["Alice", "黄乐", "Megaspeed", "女间谍", "美人计", "渗透", "intelligence asset", "色诱"]


def claim(cid: str, *needles: str, status: str | None = None, line: str | None = None) -> dict:
    """取一条台账，断言 claim / quote / note 里出现了画面要用的字样、性质和挂的句号。"""
    c = CLAIMS[cid]
    text = " ".join(str(c.get(k) or "") for k in ("claim", "quote", "note", "verified", "via", "source"))
    for n in needles:
        assert n in text, f"{cid} 里找不到画面要用的「{n}」"
    if status:
        assert c["status"] == status, f"{cid} 性质是 {c['status']}，画面按 {status} 标注"
    if line:
        assert line in (c.get("lines") or []), f"{cid} 没挂 {line}"
    return c


def quote_part(cid: str, part: str) -> str:
    """引语只截原话里连续的一段（逐字），断言它确实在台账 quote 里。"""
    q = CLAIMS[cid]["quote"]
    norm = lambda s: s.replace("“", "\"").replace("”", "\"").replace("’", "'")
    assert norm(part) in norm(q), f"{cid} 的 quote 里没有「{part}」"
    return part


def numbers() -> dict:
    c12 = claim("C12", "151.01", "148.80", "173.73", "166.19", "4.34%", status="已证实", line="l04")
    prev, opn, close = 173.73, 151.01, 166.19
    open_pct = (opn / prev - 1) * 100
    close_pct = (close / prev - 1) * 100
    assert round(close_pct, 2) == -4.34, close_pct
    # 讲稿：「一开盘就跌了十几个点」/ "opened down more than ten percent"
    assert -20 < open_pct < -10, open_pct
    assert round(open_pct) == -13
    claim("C06", "33 years", line="l03")
    claim("C07", status="已证实", line="l03")
    c118 = claim("C118", "77-20", "2025-10", status="已证实", line="l41")
    claim("C98", "2026-03-24", "Banks", "Warren", line="l42")
    claim("C08", "November 17", line="l68")
    claim("C10", "Filed 11/09/26", "5:26-cv-13448", line="l57")
    claim("C58", "non-fraternization policy", "2018-06-21", line="l61")
    claim("C101", "11-10", "R", line="l53")
    claim("C123", "11-12", "辞职之后", line="l55")
    claim("C100", "11-09", line="l44")
    claim("C82", "2025-08-11", line="l43")
    claim("C43", "negotiations", status="有争议", line="l69")
    claim("C131", "insufficient evidence", line="l22")
    claim("C132", "2025", "ongoing", line="l28")
    claim("C22", "ongoing", line="l28")
    claim("C23", "2026-02", "insufficient evidence", line="l21")
    claim("C72", "closed-door", line="l34")
    claim("C108", "top priority", "export control", line="l35")
    claim("C105", "Overwatch", "Mast", line="l47")
    claim("C107", "not to investigate", line="l45")
    claim("C120", "Lutnick", line="l46")
    claim("C122", "BIS", line="l46")
    claim("C110", "牺牲品", "11-10", status="有争议", line="l51")
    claim("C113", "民主党和美国建制派", "11-09", status="有争议", line="l50")
    claim("C20", "2026-10-29", status="指控未证实", line="l16")
    claim("C29", "11-11", "declined", status="指控未证实", line="l18")
    claim("C01", "November 11, 2026", "effective immediately", line="l60")
    return {
        "years": 33,
        "px": {"prev": prev, "open": opn, "close": close},
        "open_pct": round(open_pct), "close_pct": round(close_pct, 2),
        "senate": [77, 20],
    }


def quotes() -> dict:
    claim("C17", status="已证实", line="l05")
    claim("C19", status="已证实", line="l12")
    claim("C25", status="已证实", line="l19")
    claim("C26", status="已证实", line="l37")
    claim("C85", status="已证实", line="l26")
    claim("C23", status="已证实", line="l20")
    eightk = CLAIMS["C01"]["quote"]
    assert eightk.endswith("effective immediately.")
    return {
        "eightk": eightk,
        "letter": quote_part("C17", "I was unfaithful to my wife."),
        "board": quote_part("C19", "target of a foreign intelligence effort"),
        "board_no": quote_part("C19", "no reason to believe that either national security or NVIDIA secrets were compromised"),
        "mfa1": quote_part("C25", "纯属捕风捉影，污蔑抹黑。"),
        "mfa2": quote_part("C26", "美方应当停止编造所谓的“间谍叙事”，为实施科技封锁寻找借口。"),
        "tenk": quote_part("C85", "effectively foreclosed"),
        "mha": quote_part("C23", "not investigated for espionage"),
        "trump1": quote_part("C82", "pay us as a country something"),
        "trump2": quote_part("C100", "a very honorable man"),
        "jeffries": quote_part("C123", "was the right thing to do"),
        # 屏幕只列关键词（台词审 lines_r1 I37、I10）：外交部原话里截两段
        "mfa2_kw": quote_part("C26", "间谍叙事"),
        "mfa2_kw2": quote_part("C26", "科技封锁"),
    }


def chapters() -> dict:
    """页眉的章节叫法从 package.json 取，与目录、章节卡一致（design_system 7.5；讲稿作者改章名后重跑本脚本即可）。"""
    pk = json.loads((TOPIC / "package.json").read_text(encoding="utf-8"))
    out = {}
    for i, (cid, v) in enumerate(pk["chapters"].items(), 1):
        assert v.get("zh") and v.get("en"), f"package.json 章节 {cid} 缺中英标题"
        out[cid] = {"no": f"{i:02d}", "zh": v["zh"], "en": v["en"]}
    return out


def outro_quote() -> dict:
    """片尾点题句取 package.json quote（s6 l66 中文两行与片尾卡同一句；英文屏另用 ≤6 词的短写，见 s6）。"""
    q = json.loads((TOPIC / "package.json").read_text(encoding="utf-8"))["quote"]
    assert len(q["zh"]) == 2 and all(len(x) <= 12 for x in q["zh"]), q["zh"]
    return q


# 画面署名：默认取素材台账的 credit；这几张按要求改写成更短的写法
CREDIT_OVERRIDE = {
    "Official_Presidential_Portrait_of_President_Donald_J._Trump_(2025).jpg": {"zh": "图：白宫官方肖像（公共领域）", "en": "Photo: official White House portrait (public domain)"},
    "United_States_Capitol_west_front_edit2.jpg": {"zh": "图：Architect of the Capitol（公共领域）", "en": "Photo: Architect of the Capitol (public domain)"},
}


def credits() -> dict:
    """素材台账 → {场景里的 img/ 路径: 署名}。没有台账条目的图片，场景里的图片位不显示（系列 README §4）。"""
    ledger = json.loads((TOPIC / "media_ledger.json").read_text(encoding="utf-8"))["items"]
    out = {}
    for it in ledger:
        local = it.get("local") or ""
        if not local.startswith("assets/") or it.get("kind") not in (None, "image"):
            continue
        name = Path(local).name
        cr = CREDIT_OVERRIDE.get(name)
        if not cr and "/source/ai/" in local:
            cr = {"zh": "AI 生成", "en": "AI-generated"}
        if not cr:
            c = re.sub(r"\s+", " ", it.get("credit") or it.get("owner") or "").strip()
            cr = {"zh": f"图：{c}", "en": f"Photo: {c}"}
        out["img/" + local[len("assets/"):]] = cr
    # 场景里预留、但还没进台账的图片位（文件到了要先登记台账）
    used = set()
    for f in WEB.glob("*.html"):
        used |= set(re.findall(r'data-src="(img/[^"]+)"', f.read_text(encoding="utf-8")))
    missing = sorted(u for u in used if u not in out)
    if missing:
        print("图片位还没有台账条目（不显示）：" + "、".join(missing))
    return out


def redline_scan(out: dict) -> None:
    blob = json.dumps(out, ensure_ascii=False)
    files = sorted(WEB.glob("*.html")) + sorted(WEB.glob("*.js"))
    for name, text in [("data.json", blob)] + [(f.name, f.read_text(encoding="utf-8")) for f in files]:
        for b in BANNED:
            assert not re.search(re.escape(b), text, re.I), f"红线：{name} 里出现了「{b}」"


def main() -> None:
    out = {
        "note": "由 data.py 生成，勿手改；数字与引语对 claims.json 断言过",
        "as_of": "2026-11-14",
        "n": numbers(),
        "q": quotes(),
        "credits": credits(),
        "chapters": chapters(),
        "quote": outro_quote(),
    }
    redline_scan(out)
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = out["n"]
    print(f"data.json：开盘 {n['open_pct']}% · 收盘 {n['close_pct']}% · 参院 {n['senate'][0]}:{n['senate'][1]} · 引语 {len(out['q'])} 条 · 红线扫描通过")


if __name__ == "__main__":
    main()
