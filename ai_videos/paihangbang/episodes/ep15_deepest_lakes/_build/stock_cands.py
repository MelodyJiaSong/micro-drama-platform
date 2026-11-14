# -*- coding: utf-8 -*-
"""follow-up 023：Claude 用 WebFetch 读 Pexels / Unsplash 站内搜索页挑出的候选 → reselect/claude_stock.json（同 codex schema）。
PX = (id, slug, author-handle, why)；US = (slug-id, images.unsplash.com 基址, 作者, why)。数据来自本会话 WebFetch 结果。"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).parent
def px(i, slug, author, why):
    return {"image_url": f"https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg", "page_url": f"https://www.pexels.com/photo/{i}/",
            "source": "Pexels", "author": author, "licence": "Pexels License", "why": why}
def us(sid, base, author, why):
    return {"image_url": f"https://{base}?fm=jpg&q=90&w=3000&fit=max", "page_url": f"https://unsplash.com/photos/{sid}",
            "source": "Unsplash", "author": author, "licence": "Unsplash License", "why": why}
C = {
 "01_02_lake_tanganyika": [
  px(30893780, "serene-boat-ride-on-lake-tanganyika", "Amani Allan", "Pexels search 'lake tanganyika': calm boat scene on the lake with distant hills"),
  px(35385931, "scenic-lakeside-view-with-lush-palm-trees", "Gwladys Nicimbikije", "lakeside with palm trees and mountains, Burundi"),
  px(5859993, "picture-taken-from-above-the-clouds-of-a-seashore-and-a-mountain-range", "Taty Lameck", "aerial view of mountains and the lake, Bujumbura"),
  px(30862105, "fisherman-working-on-traditional-boat-in-kigoma", "Amani Allan", "fisherman on a boat in Kigoma, Tanzania"),
  px(32806077, "small-boat-navigating-vibrant-turquoise-waters", "Edouard Mihigo", "wooden boat over turquoise water (Tanganyika search)"),
  px(27134437, "blue-sea-in-summer", "Chris Wade Ntezicimpa", "lake view with clear skies and greenery (Tanganyika search)"),
  px(35242823, "serene-lake-boat-near-tropical-beach-huts", "Isaac Naph", "boat near beach huts (Tanganyika search)"),
  px(37961021, "solitary-fisherman-in-wooden-boat-on-tranquil-lake", "Edouard Mihigo", "lone fisherman in wooden boat (Tanganyika search)")],
 "02_03_caspian_sea": [
  px(20591588, "cliffs-off-the-caspian-sea", "Radis B", "Pexels: dramatic rocky shoreline of Aktau, Kazakhstan (Caspian)"),
  px(20591589, "sun-ray-peeking-through-the-coast-of-the-caspian-sea", "Radis B", "Aktau rocky Caspian coastline with sun rays"),
  px(20048416, "wave-and-rocks-on-sea-shore", "Radis B", "waves on the rocky Caspian shore, Aktau"),
  px(20591584, "rocks-on-sea-shore", "Radis B", "rocky coastline of Aktau with waves"),
  px(17989624, "clear-sky-over-sea-coast", "Sultan Jafarov", "Caspian Sea under a clear blue sky")],
 "04_05_lago_viedma": [
  px(39277375, "stunning-view-of-mountains-over-lago-viedma-in-el-chalten", "Yani Martinez", "Pexels: mountains over Lago Viedma, El Chaltén, Santa Cruz")],
 "05_06_lake_malawi": [
  px(34504509, "colorful-sailboats-on-lake-malawi-beach", "Rosdel", "Pexels: sailboats on a Lake Malawi beach with mountains"),
  px(6509194, "docked-boats-on-sea", "Phiri Godfrey", "rowboats in Lake Malawi's waters"),
  px(36018012, "ducks-walking-by-lake-shore-in-malawi-village", "Joy Chisambo", "sandy shore of Lake Malawi with boats"),
  us("boulders-on-calm-lake-shore-3ZqcWC_HMM8", "images.unsplash.com/photo-1789587870068-bf23efb65498", "Omar Hakeem", "Unsplash tag 'lake malawi': boulders on calm shore with mountain (Cape Maclear style)"),
  us("rocky-shoreline-and-mountains-across-lake-FLqI1uJ7tto", "images.unsplash.com/photo-1789587869295-cb2dc5df032f", "Omar Hakeem", "Lake Malawi series: rocky shoreline and hazy mountains"),
  us("two-people-kayak-on-a-calm-blue-lake-near-mountains-Ca1VoEB8CMY", "images.unsplash.com/photo-1775123465209-68d1af71060d", "Omar Hakeem", "Lake Malawi series: calm blue lake near mountains"),
  us("a-body-of-water-surrounded-by-trees-and-rocks-28eycWOrkNU", "images.unsplash.com/photo-1715948887678-f33850e4ac50", "Omar Hakeem", "Lake Malawi series: water with trees and rocks"),
  us("motorboat-on-lake-malawi-0R6UXxGPg-8", "images.unsplash.com/photo-1789587871596-0b33af834b78", "Omar Hakeem", "motorboat moored on Lake Malawi")],
 "07_08_great_slave_lake": [
  us("boats-at-body-of-water-prUkJ3SEuWQ", "images.unsplash.com/photo-1528684012159-514fd1604514", "Ian Keefe", "Unsplash 'yellowknife': boats on Yellowknife Bay (Great Slave Lake)"),
  us("a-boat-sitting-on-top-of-a-lake-next-to-a-house-SJaLMYcH6So", "images.unsplash.com/photo-1634973304383-067216313633", "Ken Cheung", "Unsplash 'yellowknife': boat and house on the lake")],
 "26_27_lake_van": [
  px(37365340, "boat-lake-van", "Birkay Bolushikayesi", "Pexels: boat on Lake Van with snowy mountains, Van, Turkey"),
  px(21561934, "van-lake-snowcapped", "zlfdmr23", "Lake Van with snow-capped mountains and cloudy sky"),
  px(27065001, "lake-van-landscape", "Ensar", "Lake Van with rolling hills"),
  px(13024141, "lake-van-birds", "Leyla Helvaci", "Lake Van with birds and distant mountain")],
 "28_29_lake_manapouri": [
  px(17824119, "lake-manapouri-sunrise", "Donovan Kelly", "Pexels 'lake manapouri': Lake Manapouri at sunrise with misty mountains"),
  px(11819607, "fiordland-dawn", "Liisa Tervinen", "dawn in Fiordland, calm water and mountain reflections (lake not named)")],
 "30_30_lake_te_anau": [
  px(18531095, "pier-lake-te-anau", "Kari Kittlaus", "Pexels: pier stretching into Lake Te Anau, Southland")],
 "31_32_lake_tazawa": [
  px(31365953, "peaceful-winter-scene-of-a-traditional-japanese-shrine-by-a-lake-in-akita-prefecture", "alankrantas", "Pexels 'lake tazawa': shrine by the lake in Akita (Gozanoishi)"),
  px(19792304, "peaceful-winter-view-of-ukiki-shrine-in-akita-japan", "auspiciousajay", "Ukiki Shrine on Lake Tazawa shore, winter"),
  px(33651654, "peaceful-lakeside-scene-in-semboku-japan", "Ethan P", "lakeside in Semboku (Lake Tazawa's municipality)"),
  us("a-large-body-of-water-with-mountains-in-the-background-GRotN_yBHlk", "images.unsplash.com/photo-1740873690984-2c9a959505bf", "pen_ash", "Unsplash 'lake tazawa': lake with mountains"),
  us("snow-capped-mountains-reflected-in-a-calm-lake-Bk6yaDS-gX4", "images.unsplash.com/photo-1777500394141-1282a837b007", "Trac Vu", "Unsplash 'lake tazawa' series (golden statue set): snow-capped mountains reflected"),
  us("a-boat-is-docked-at-a-pier-on-a-lake-znuy79QN_rg", "images.unsplash.com/photo-1702529454259-a04cdf16c377", "Yu Gordon", "Unsplash 'lake tazawa': boat at pier")],
}
out = HERE / 'reselect' / 'claude_stock.json'
out.write_text(json.dumps({"items": [{"key": k, "images": v} for k, v in C.items()]}, ensure_ascii=False, indent=1), encoding='utf-8')
print(sum(len(v) for v in C.values()), 'candidates')
