# -*- coding: utf-8 -*-
"""排行榜大陆中文版（paihangbang follow-up 046）。每步落盘、可续跑：

    python ai_videos/paihangbang/_tools/zh_edition.py translate <ep_dir>     # Codex 联网翻译（标准中文译名）
    python ai_videos/paihangbang/_tools/zh_edition.py merge     <ep_dir>     # 合成 data.zh.json + 确定性合规处理
    python ai_videos/paihangbang/_tools/zh_edition.py gate      <ep_dir>     # 合规闸门，不过就不许渲染

合规（台湾 / 香港 / 澳门）**不交给翻译**，由 merge 写死、gate 复查：
- 国家代码 TW / HK / MO 一律改 CN（五星红旗、计分板计入「中国」），显示名固定「中国台湾 / 中国香港 / 中国澳门」；
- 「一国一张」的榜单（ep02 各国最高峰）删去台湾条目，名次重排，补下一个主权国家；
- 列有地区的「国家」榜单标题必须写「国家和地区」；
- 画面文字里不得出现「中华民国 / 台湾国 / ROC」，不得出现不带「中国」前缀的「台湾」作国家名。
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from tools.service_request import RequestLog  # noqa: E402

REGION = {"TW": "中国台湾", "HK": "中国香港", "MO": "中国澳门"}
REGION_EN = {"Taiwan": "TW", "Hong Kong": "HK", "Macao": "MO", "Macau": "MO",
             "Taiwan, China": "TW", "Hong Kong, China": "HK", "Macao, China": "MO"}   # 英文版已按 follow-up 047 改写，新旧两种都认
CONTINENT = {"Asia": "亚洲", "Europe": "欧洲", "Africa": "非洲", "North America": "北美洲", "South America": "南美洲",
             "Oceania": "大洋洲", "Antarctica": "南极洲", "Australia": "大洋洲"}
# 计分板按自定义分类（ep05 传播途径、ep06 出版社）分组时的中文显示名；与卡面译名一致
CATEGORY = {"Airborne": "空气传播", "Blood & sex": "血液和性传播", "Food & water": "食物和水", "Contact": "接触传播",
            "Mosquito & tick": "蚊虫叮咬", "Animals": "动物传播",
            "Shueisha": "集英社", "Shogakukan": "小学馆", "Leed Publishing": "LEED出版社", "Kodansha": "讲谈社",
            "Akita Shoten": "秋田书店", "Square Enix": "史克威尔艾尼克斯", "Shimaisha": "姊妹社", "Ushio Shuppan": "潮出版社"}
# 外交部口径（不含中印边境印占区与克什米尔印控区）；只改大陆版显示，英文版不动
OFFICIAL_AREA = {"IN": (2980000, "约298万平方公里")}

ITEM_KEYS = ("name", "subtitle", "country_name", "continent", "value_display", "secondary_display", "badge",
             "tag1", "tag2", "image_note", "corner", "person_name", "person_role")
TOP_KEYS = ("title", "metric_label", "period_label", "source_line", "tally_title", "unit", "scope_note")

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["top", "items", "insights"], "properties": {
    "top": {"type": "object", "additionalProperties": False, "required": list(TOP_KEYS), "properties": {k: {"type": "string"} for k in TOP_KEYS}},
    "items": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["i", *ITEM_KEYS],
              "properties": {"i": {"type": "integer"}, **{k: {"type": "string"} for k in ITEM_KEYS}}}},
    "insights": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["i", "text"],
                 "properties": {"i": {"type": "integer"}, "text": {"type": "string"}}}}}}

PROMPT = """把下面这一期排行榜视频的屏幕文字翻译成**简体中文**，给中国大陆观众看（发布在抖音 / B 站）。可以联网核对专名的标准中文译名。

硬性要求：
1. 专名（建筑、山峰、河湖、动物、病毒、漫画、公司、人名、船名、体育场、城市、国家）一律用中国大陆媒体通行的标准译名；没有通行译名的音译或意译，必要时保留原文（如 ONE PIECE、ChatGPT）。拿不准就联网查。
2. 涉及台湾、香港、澳门：只能称「中国台湾」「中国香港」「中国澳门」或其下的地名（如「中国台湾新竹县」），**绝不能**把它们称作国家，不得出现「台湾国」「中华民国」「ROC」。country_name 若是 Taiwan / Hong Kong / Macao，就译成「中国台湾」等。榜单标题若是「国家」而条目里有这些地区，标题改成「国家和地区」。
3. 单位与数字按大陆习惯：高度、深度用「米」；长度、距离用「公里」；面积用「平方公里」；速度用「公里/小时」；大数用「万」「亿」（如 9360万人次、960万平方公里、6亿册）；四位数不加千分位逗号。value_display 只写一个数值加单位。
4. secondary_display 若是英制换算（ft、mi、mph、sq mi、°F 等）一律留空字符串；若是别的说明（如 est.、since 2014）就译成中文（估计、2014年起）。
5. kicker 不在这里翻译。title 简洁有力（如「全球最高建筑」），不要写「TOP 50」。metric_label、period_label、source_line、tally_title 都译成中文，机构名可保留缩写（如「数据：世界高层建筑与都市人居学会（CTBUH）、Wikidata」）。
6. badge、tag1、tag2、corner 要短（badge ≤ 10 个汉字，tag ≤ 12 个汉字）；如 NEW 2025→「2025新建」，SHARED WITH NEPAL→「与尼泊尔共有」，EST. 2010→「成立于2010」。
7. insights 是「你知道吗？」卡上的一句话，译成自然口语的中文，≤ 40 个汉字，数字与事实不得改动；若原句把台湾当国家，改写成地区的说法。
8. 原文为空的字段输出空字符串；i 原样照抄；数组顺序与条数不变。只输出 JSON。

原文：
{payload}"""


def paths(ep: Path) -> dict[str, Path]:
    b = ep / "_build" / "zh"
    return {"build": b, "src": b / "src.json", "tr": b / "translation.json", "data": ep / "data.json", "zh": ep / "data.zh.json"}


def extract(d: dict) -> dict:
    items = []
    for i, it in enumerate(d["items"]):
        tags = [t.get("text", "") for t in it.get("tags") or []] + ["", ""]
        person = it.get("person") or {}
        items.append({"i": i, "name": it.get("name", ""), "subtitle": it.get("subtitle", ""), "country_name": it.get("country_name", ""),
                      "continent": it.get("continent", ""), "value_display": it.get("value_display", ""),
                      "secondary_display": it.get("secondary_display", ""), "badge": it.get("badge", "") or "",
                      "tag1": tags[0], "tag2": tags[1], "image_note": it.get("image_note", "") or "", "corner": it.get("corner", "") or "",
                      "person_name": person.get("name", "") if isinstance(person, dict) else "",
                      "person_role": person.get("role", "") if isinstance(person, dict) else ""})
    top = {k: str(d.get(k, "")) for k in TOP_KEYS if k != "tally_title"}
    top["tally_title"] = (d.get("tally") or {}).get("title", "")
    return {"top": top, "items": items, "insights": [{"i": i, "text": x["text"]} for i, x in enumerate(d.get("insights", []))]}


def cmd_translate(ep: Path) -> None:
    p = paths(ep)
    p["build"].mkdir(parents=True, exist_ok=True)
    if p["tr"].exists():
        print("已有 translation.json，跳过"); return
    d = json.loads(p["data"].read_text(encoding="utf-8"))
    src = extract(d)
    p["src"].write_text(json.dumps(src, ensure_ascii=False, indent=1), encoding="utf-8")
    schema = p["build"] / "schema.json"
    schema.write_text(json.dumps(SCHEMA), encoding="utf-8")
    prompt = PROMPT.replace("{payload}", json.dumps(src, ensure_ascii=False))
    argv = [shutil.which("codex") or "codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
            "--output-schema", str(schema), "-o", str(p["tr"]), "-"]
    req = {"argv": argv, "prompt": prompt, "purpose": "排行榜大陆中文版：屏幕文字翻译（只翻译，不生成图）", "output": str(p["tr"]), "cost": "ChatGPT 订阅额度，未知"}
    r = RequestLog(ep).invoke("codex_cli", "translate", req, lambda: subprocess.run(
        argv, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800))
    print(ep.name, "rc", r.returncode, "ok" if p["tr"].exists() else "NO OUTPUT " + r.stderr[-300:])


LINK_PAREN = re.compile(r"[（(][^（）()]*\]\([^)]*\)[^（）()]*[）)]")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
NOTE_TAIL = re.compile(r"[；;，,]?\s*(译名参考|参考|来源说明)[:：].*$")


def clean(s: str) -> str:
    """Codex 有时把查证引用塞进译文（Markdown 链接、网址、「译名参考：…」）；画面上只留译文本身。"""
    s = LINK_PAREN.sub("", s)
    s = MD_LINK.sub("", s)
    s = URL.sub("", s)
    s = NOTE_TAIL.sub("", s)
    return re.sub(r"[（(]\s*[）)]", "", s).strip(" ；;，,、")


def clean_tree(x):
    if isinstance(x, str):
        return clean(x)
    if isinstance(x, list):
        return [clean_tree(v) for v in x]
    if isinstance(x, dict):
        return {k: (v if k == "i" else clean_tree(v)) for k, v in x.items()}
    return x


def zh_tags(orig: list, t1: str, t2: str) -> list:
    out = []
    for k, t in enumerate(orig or []):
        out.append({**t, "text": [t1, t2][k] if k < 2 and [t1, t2][k] else t.get("text", "")})
    return out


def cmd_merge(ep: Path) -> None:
    p = paths(ep)
    d = base_data(ep)
    tr = clean_tree(json.loads(p["tr"].read_text(encoding="utf-8")))
    z = copy.deepcopy(d)
    z["lang"] = "zh"
    for k in ("title", "metric_label", "period_label", "source_line", "unit", "scope_note"):
        if tr["top"].get(k):
            z[k] = tr["top"][k]
    z.setdefault("tally", {})["title"] = tr["top"].get("tally_title") or z["tally"].get("title", "")
    m = re.fullmatch(r"(\d+) AI COMPANIES", z.get("kicker", ""))      # 角标：「TOP N」中文观众通用，保留；其余英文改中文
    if m:
        z["kicker"] = f"{m.group(1)}家AI公司"
    by_i = {x["i"]: x for x in tr["items"]}
    labels: dict[str, str] = {}
    drop = []
    for i, it in enumerate(z["items"]):
        t = by_i.get(i, {})
        iso0 = str(it.get("country_iso2", "")).upper()
        for k in ("name", "subtitle", "country_name", "value_display", "secondary_display", "badge", "image_note", "corner"):
            if k in it or t.get(k):
                it[k] = t.get(k, it.get(k, "")) if t.get(k) is not None else it.get(k, "")
        it["tags"] = zh_tags(it.get("tags"), t.get("tag1", ""), t.get("tag2", ""))
        if isinstance(it.get("person"), dict):
            it["person"] = {**it["person"], "name": t.get("person_name") or it["person"].get("name", ""),
                            "role": t.get("person_role") or it["person"].get("role", "")}
        # ── 合规：台湾 / 香港 / 澳门是中国的地区 ───────────────────────────
        orig = d["items"][i]
        region = REGION.get(iso0) or REGION.get(REGION_EN.get(orig.get("country_name", ""), "")) or REGION.get(REGION_EN.get(orig.get("name", ""), ""))
        if region:
            if iso0 in REGION:
                it["country_iso2"] = "CN"
            if orig.get("country_name") in REGION_EN or (iso0 in REGION and z.get("tally", {}).get("by") == "country"):
                it["country_name"] = region
            if orig.get("name") in REGION_EN:          # 榜单条目本身就是这个地区（ep19）
                it["name"] = region
        if iso0 == "IN" and ep.name.startswith("ep12_"):
            v, disp = OFFICIAL_AREA["IN"]
            it["value"], it["value_display"] = v, disp
            it["notes"] = (it.get("notes", "") + " | 大陆版按外交部口径：约298万平方公里（不含中印边境印占区与克什米尔印控区）").strip(" |")
        # 「一国一张」的榜：台湾不是国家，整张删去
        if z.get("one_per_country") or ep.name.startswith("ep02_"):
            if iso0 == "TW" or "Yushan" in orig.get("name", ""):
                drop.append(i)
        if str(it.get("country_iso2", "")).upper() == "CN":
            labels["CN"] = "中国"
        elif it.get("country_iso2"):
            labels.setdefault(str(it["country_iso2"]), it.get("country_name", ""))
        if it.get("continent"):
            k0 = orig.get("continent", "")
            labels.setdefault(k0, CONTINENT.get(k0) or CATEGORY.get(k0) or it.get("continent", ""))
        it["continent"] = orig.get("continent", "")            # 计分板分组键保持英文（tally.icons 以它为键），显示名走 labels
    for k in sorted(drop, reverse=True):
        del z["items"][k]
    extra = p["build"] / "extra_items.json"          # 删条目后补位（如 ep02 补第 51 个主权国家），已是中文
    if extra.exists() and not any(abs(float(it["value"]) - float(x["value"])) < 1e-6 and it.get("country_iso2") == x.get("country_iso2")
                                  for x in json.loads(extra.read_text(encoding="utf-8")) for it in z["items"]):
        z["items"] += json.loads(extra.read_text(encoding="utf-8"))
        z["items"].sort(key=lambda x: -float(x["value"]))
    if drop or extra.exists():
        renumber(z)
    for x in tr["insights"]:
        if x["i"] < len(z.get("insights", [])) and x["text"]:
            z["insights"][x["i"]]["text"] = x["text"]
    if not any(it.get("name") in REGION.values() for it in z["items"]) and "国家和地区" in z.get("title", ""):
        z["title"] = z["title"].replace("各国家和地区", "各国").replace("国家和地区", "国家")   # 台湾已删、只剩主权国家（ep02）
    if len(z.get("source_line", "")) > 70:                 # 机构列太长：截到 70 字内最后一个顿号，补「等」
        s = z["source_line"][:68]
        z["source_line"] = (s[:s.rfind("、")] if "、" in s else s) + "等"
    for it in z["items"]:                                   # 数值与单位之间不留空格，全片一致
        it["value_display"] = re.sub(r"(?<=\d)\s+(?=[一-鿿])", "", str(it.get("value_display", "")))
    if z.get("tally", {}).get("by") == "country":
        z["tally"]["labels"] = {k: v for k, v in labels.items() if len(k) == 2}
    else:
        z["tally"]["labels"] = {k: v for k, v in labels.items() if len(k) > 2}
    p["zh"].write_text(json.dumps(z, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(ep.name, "data.zh.json 写好", f"（删去 {len(drop)} 条）" if drop else "")


def base_data(ep: Path) -> dict:
    """译文是照哪一版 data.json 翻的，就以哪一版为底稿（英文版 follow-up 047 改过条目顺序，按序号对会错位）。"""
    src = json.loads(paths(ep)["src"].read_text(encoding="utf-8"))
    names = [x["name"] for x in src["items"]]
    for cand in (ep / "data.json", ep / "_build" / "data.before_region_fix.json"):
        if cand.exists():
            d = json.loads(cand.read_text(encoding="utf-8"))
            if [it.get("name", "") for it in d["items"]] == names:
                return d
    raise SystemExit(f"{ep.name}：找不到与译文逐条对应的 data.json（译文过期，需重译）")


def renumber(z: dict) -> None:
    """删条目后重排名次：值相同的同名次（1,1,3 式跳号），按值降序。"""
    rank = 0
    for n, it in enumerate(z["items"]):
        if n == 0 or it["value"] != z["items"][n - 1]["value"]:
            rank = n + 1
        it["rank"] = rank


# ── 闸门 ──────────────────────────────────────────────────────────────────
BANNED = ("中华民国", "中華民國", "台湾国", "臺灣國", "ROC", "Republic of China", "青天白日")
TW_BARE = re.compile(r"(?<!中国)(台湾|臺灣)(?!省|海峡|地区)")


def screen_texts(z: dict) -> list[tuple[str, str]]:
    out = [(k, str(z.get(k, ""))) for k in ("title", "kicker", "metric_label", "period_label", "source_line")]
    out.append(("tally.title", str(z.get("tally", {}).get("title", ""))))
    out += [(f"tally.labels.{k}", v) for k, v in (z.get("tally", {}).get("labels") or {}).items()]
    for it in z["items"]:
        w = f"#{it['rank']} {it.get('name','')}"
        for k in ("name", "subtitle", "country_name", "value_display", "secondary_display", "badge", "image_note", "corner"):
            out.append((f"{w}.{k}", str(it.get(k) or "")))
        out += [(f"{w}.tag", str(t.get("text", ""))) for t in it.get("tags") or []]
        if isinstance(it.get("person"), dict):
            out += [(f"{w}.person", str(it["person"].get("name", "")) + " " + str(it["person"].get("role", "")))]
    out += [(f"insight{i}", x["text"]) for i, x in enumerate(z.get("insights", []))]
    return out


def cmd_gate(ep: Path) -> int:
    p = paths(ep)
    z = json.loads(p["zh"].read_text(encoding="utf-8"))
    errs = []
    for it in z["items"]:
        iso = str(it.get("country_iso2", "")).upper()
        if iso in REGION:
            errs.append(f"#{it['rank']} {it['name']}：国家代码仍是 {iso}（须为 CN）")
    for where, s in screen_texts(z):
        for b in BANNED:
            if b in s:
                errs.append(f"{where}：出现禁用词「{b}」：{s}")
        if URL.search(s) or MD_LINK.search(s):
            errs.append(f"{where}：画面文字里不能有链接：{s[:60]}")
        if TW_BARE.search(s):
            errs.append(f"{where}：「台湾」前须加「中国」：{s}")
        if re.search(r"[A-Za-z]{4,}", s) and where.endswith((".country_name", "title", "metric_label", ".value_display")) and not re.search(r"[一-鿿]", s):
            errs.append(f"{where}：没有译成中文：{s}")
    if len(z.get("source_line", "")) > 70:
        errs.append(f"source_line 超过 70 字：{z['source_line']}")
    labels = z.get("tally", {}).get("labels") or {}
    if z.get("tally", {}).get("by") == "country" and any(str(it.get("country_iso2", "")).upper() == "CN" for it in z["items"]) and labels.get("CN") != "中国":
        errs.append(f"计分板 CN 的显示名须为「中国」，现在是「{labels.get('CN')}」")
    for k, v in labels.items():                       # 计分板显示名必须是中文（ep05/ep06 自定义分类曾漏译）
        if not re.search(r"[一-鿿]", str(v)) and not re.fullmatch(r"[A-Z0-9]{2,6}", str(v)):
            errs.append(f"计分板分组「{k}」显示名没有译成中文：{v}")
    regions_listed = any(it.get("name") in REGION.values() for it in z["items"])
    if regions_listed and "地区" not in z.get("title", ""):
        errs.append(f"榜单条目里有地区，标题须写「国家和地区」：{z.get('title')}")
    if ep.name.startswith("ep02_") and any("玉山" in it.get("name", "") for it in z["items"]):
        errs.append("ep02 是一国一张的榜单，不得有玉山（台湾）条目")
    for e in errs:
        print("  ✗", e)
    print(f"{ep.name}：{'闸门通过' if not errs else f'{len(errs)} 处不合规'}")
    return 1 if errs else 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("translate", "merge", "gate"))
    ap.add_argument("ep", nargs="+")
    a = ap.parse_args()
    rc = 0
    for e in a.ep:
        ep = Path(e).resolve()
        if a.step == "translate":
            cmd_translate(ep)
        elif a.step == "merge":
            cmd_merge(ep)
        else:
            rc |= cmd_gate(ep)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
