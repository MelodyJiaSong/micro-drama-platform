# -*- coding: utf-8 -*-
"""follow-up 016 第一步：每项内容落盘 _build/content/NN_<key>.md（Britannica 原文摘句 + Wikipedia 导语 + 找图要点）。
只读已下载的 raw/brit/*.html 与 raw/wp_articles/*.txt，不联网。"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from img_hints import H  # noqa: E402
from items_def import ITEMS  # noqa: E402

B = Path(__file__).parent / "raw" / "brit"
W = Path(__file__).parent / "raw" / "wp_articles"
OUT = Path(__file__).parent / "content"
OUT.mkdir(exist_ok=True)
EP = Path(__file__).resolve().parents[1]
WPT = {"nile": "Nile", "amazon": "Amazon_River", "yangtze": "Yangtze", "mississippi_missouri": "Mississippi_River", "yenisey": "Yenisey",
       "yellow": "Yellow_River", "ob_irtysh": "Ob_(river)", "parana": "Paraná_River", "congo": "Congo_River", "amur": "Amur_River",
       "lena": "Lena_(river)", "mekong": "Mekong", "mackenzie": "Mackenzie_River", "niger": "Niger_River", "murray_darling": "Murray_River",
       "zambezi": "Zambezi", "volga": "Volga", "madeira": "Madeira_River", "jurua": "Juruá_River", "purus": "Purus_River", "indus": "Indus_River",
       "yukon": "Yukon_River", "rio_grande": "Rio_Grande", "syr_darya": "Syr_Darya", "lower_tunguska": "Lower_Tunguska",
       "sao_francisco": "São_Francisco_River", "brahmaputra": "Brahmaputra_River", "danube": "Danube", "japura": "Japurá_River",
       "euphrates": "Euphrates", "orinoco": "Orinoco", "tocantins": "Tocantins_River", "vilyuy": "Vilyuy", "nelson": "Nelson_River",
       "paraguay": "Paraguay_River", "amu_darya": "Amu_Darya", "ganges": "Ganges", "pilcomayo": "Pilcomayo_River", "ishim": "Ishim_(river)",
       "ural": "Ural_(river)", "salween": "Salween", "arkansas": "Arkansas_River", "colorado": "Colorado_River", "olenyok": "Olenyok_(river)",
       "aldan": "Aldan_(river)", "negro": "Rio_Negro_(Amazon)", "ubangi": "Ubangi_River", "dnieper": "Dnieper", "irrawaddy": "Irrawaddy_River",
       "kasai": "Kasai_River", "araguaia": "Araguaia_River"}


QUOTE = [""]


def brit_text(url):
    slug = url.rsplit("/", 1)[-1]
    f = B / f"{slug}.html"
    if not f.exists():
        return ""
    t = f.read_text(encoding="utf-8", errors="replace")
    s = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", t))))
    nums = re.findall(r"\d,\d\d\d", QUOTE[0])
    i = s.find(nums[-1]) if nums and nums[-1] in s else -1
    if i < 0:
        return ""
    return "…" + s[max(0, i - 700):i + 1100] + "…"


def main():
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    by_key = {it["key"]: it for it in data["items"]}
    for d in ITEMS:
        it = by_key[d["key"]]
        wp = W / f"{WPT[d['key']]}.txt"
        wtxt = wp.read_text(encoding="utf-8") if wp.exists() else "(Wikipedia 文本未取到：429 限流)"
        head, _, body = wtxt.partition("\n\n")
        intro = body.split("\n\n")[0][:1500] if body else ""
        course = ""
        m = re.search(r"\n== ?(Course|Geography|Description|Course and features|Physical geography) ?==\n(.{0,1500})", body, re.S)
        if m:
            course = m.group(2).strip()
        QUOTE[0] = d['quote']
        view, avoid = H[d["key"]]
        md = f"""# #{it['rank']} {d['name']}（{d['country']} · {d['continent']}）

- 长度：{d['km']:,} km（{d['src'][0]}；{d['src'][1]}）
- 原文：“{d['quote']}”
- 走向：{d['subtitle']}；{d['tag'][1]}
- 备注：{d.get('notes','')}

## 它是什么、在哪、长什么样（Britannica 摘录，存档于 raw/brit/）
{brit_text(d['src'][1]) or '(Britannica 正文未取到)'}

## Wikipedia 导语（只作文字参考；{head.replace(chr(10), ' ')}）
{intro}

{('### 河道 / 地理' + chr(10) + course) if course else ''}

## 找图要点（浓缩进 data.json image_hint）
- 标志性视角 / 最佳拍摄点：{view}
- 易混对象（排除）：{avoid}
- 要求：真实照片，河本身是主体，横幅风景，适合 720×800 满版卡居中裁切；不要地图、卫星假彩色、AI 图。
"""
        (OUT / f"{it['rank']:02d}_{d['key']}.md").write_text(md, encoding="utf-8")
    print(len(list(OUT.glob("*.md"))), "files")


if __name__ == "__main__":
    main()
