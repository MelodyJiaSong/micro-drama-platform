# -*- coding: utf-8 -*-
"""follow-up 016 第一步：每项内容落盘 _build/content/NN_<slug>.md（来自本地已抓的 Wikipedia wikitext、ILEC 与调研笔记）。"""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).parent; EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import ITEMS
ART = {"lake_baikal": "Lake_Baikal", "lake_tanganyika": "Lake_Tanganyika", "caspian_sea": "Caspian_Sea", "lago_ohiggins": "O_Higgins_San_Martín_Lake",
       "lago_viedma": "Viedma_Lake", "lake_malawi": "Lake_Malawi", "issyk_kul": "Issyk_Kul", "great_slave_lake": "Great_Slave_Lake",
       "lago_argentino": "Lake_Argentino", "crater_lake": "Crater_Lake", "lake_matano": "Lake_Matano", "lago_general_carrera": "Lake_General_Carrera_Buenos_Aires",
       "hornindalsvatnet": "Hornindalsvatnet", "quesnel_lake": "Quesnel_Lake", "sarez_lake": "Sarez_Lake", "lake_toba": "Lake_Toba", "lake_tahoe": "Lake_Tahoe",
       "salvatnet": "Salvatnet", "lake_kivu": "Lake_Kivu", "nahuel_huapi": "Nahuel_Huapi_Lake", "lake_hauroko": "Lake_Hauroko", "lago_cochrane": "Cochrane_Pueyrredón_Lake",
       "tinnsjoen": "Lake_Tinn", "adams_lake": "Adams_Lake", "lake_chelan": "Lake_Chelan", "mjosa": "Mjøsa", "lake_van": "Lake_Van", "great_bear_lake": "Great_Bear_Lake",
       "lake_manapouri": "Lake_Manapouri", "lake_como": "Lake_Como", "lake_te_anau": "Lake_Te_Anau", "lake_tazawa": "Lake_Tazawa", "lake_khantayskoye": "Lake_Khantayskoye",
       "lake_wakatipu": "Lake_Wakatipu", "lago_grey": "Grey_Lake", "lake_superior": "Lake_Superior"}

def plain(w: str) -> str:
    w = re.sub(r'<!--.*?-->', '', w, flags=re.S)
    w = re.sub(r'<ref[^>]*/>|<ref[^>]*>.*?</ref>', '', w, flags=re.S)
    for _ in range(4):
        w = re.sub(r'\{\{(?:convert|cvt)\|([^|}]+)\|([^|}]+)[^{}]*\}\}', r'\1 \2', w)
        w = re.sub(r'\{\{[^{}]*\}\}', '', w)
    w = re.sub(r'\[\[(?:File|Image):[^\]]*(\[\[[^\]]*\]\][^\]]*)*\]\]', '', w)
    w = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', w)
    w = re.sub(r'\[https?://\S+ ([^\]]*)\]', r'\1', w)
    w = re.sub(r"'{2,}", '', w); w = re.sub(r'<[^>]+>', '', w)
    w = re.sub(r'\{\|.*?\|\}', '', w, flags=re.S)
    return re.sub(r'\n{3,}', '\n\n', w).strip()

data = json.loads((EP / 'data.json').read_text(encoding='utf-8'))
by = {d['name']: d for d in ITEMS}
out = HERE / 'content'; out.mkdir(exist_ok=True)
for it in data['items']:
    d = by[it['name']]
    wt = (HERE / 'raw' / 'articles' / f"{ART[d['key']]}.wikitext").read_text(encoding='utf-8')
    rev = re.search(r'revid (\d+) title (.*?)-->', wt)
    p = plain(wt)
    lead = p.split('\n==')[0].strip()[:1800]
    secs = re.findall(r'\n==+\s*([^=\n]+?)\s*==+\n(.*?)(?=\n==)', '\n' + p + '\n==', flags=re.S)
    geo = [f"### {h}\n{b.strip()[:1200]}" for h, b in secs if re.search(r'geograph|descri|physical|hydrolog|geolog|bathym|landscape|setting|overview', h, re.I)][:2]
    md = f"""# {it['rank']:02d} · {it['name']}（{it['country_name']}，{it['continent']}）

来源：Wikipedia 「{rev.group(2)}」rev {rev.group(1)}（2026-11-03 经 API 取 wikitext，只作文字与交叉核对）；数值出处见 sources.md。

## 它是什么、在哪
{lead}

{chr(10).join(geo)}

## 本期数据
- 最大水深 {it['value_display']}（{it['source']['name']}）；湖面海拔 {d['surface']} m（{d['surface_src']}）→ {it['tags'][0]['text']}
- 备注：{d['notes']}

## 找图要点（写入 image_hint）
- {d['hint']}
- 横幅风景（卡 720×800 满版，焦点居中）；真实照片；色彩好、天气晴；不要人物为主体、不要建筑压过湖面。
"""
    f = out / f"{it['rank']:02d}_{d['key']}.md"
    f.write_text(md, encoding='utf-8')
print(len(list(out.glob('*.md'))), 'files')
