# -*- coding: utf-8 -*-
"""follow-up 023：Claude 自己用 WebFetch（Pexels / Unsplash 站内搜索页、Flickr 照片页）找到的候选，写 reselect/claude_<批>.json。
Pexels 直链按 images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg 构造；Unsplash 用 /photos/<id>/download?force=true；
写入前逐个 GET 验证能下到图片本身（Content-Type image/*，> 50 KB）。

    python claude_cands.py <批号>      # 例：python claude_cands.py 01
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}

# 批次 → {data.json 下标: [(source, page_url, author, licence, why), ...]}
BATCHES = {
 "01": {
  15: [("Pexels", "https://www.pexels.com/photo/scenic-aerial-view-of-desert-oasis-and-sand-dunes-36885274/", "Mohammed Alnaily", "Pexels License", "Aerial oasis among dunes, Libya (location stated on page)"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-oasis-in-vast-desert-landscape-36885275/", "Mohammed Alnaily", "Pexels License", "Same series, Libya"),
       ("Pexels", "https://www.pexels.com/photo/stunning-oasis-in-the-expansive-sahara-desert-36885278/", "Mohammed Alnaily", "Pexels License", "Same series, Libya"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-sand-dunes-and-oasis-in-libya-39223094/", "bubaker-lfkeeh", "Pexels License", "Dunes meeting an oasis, Kufra, Libya"),
       ("Pexels", "https://www.pexels.com/photo/historic-arch-at-leptis-magna-libya-38076912/", "montaha", "Pexels License", "Leptis Magna Roman arch (fallback subject)"),
       ("Pexels", "https://www.pexels.com/photo/majestic-desert-arch-in-sahara-landscape-36885280/", "Mohammed Alnaily", "Pexels License", "Stone arch in the Sahara, same Libyan series")],
  21: [("Pexels", "https://www.pexels.com/photo/man-standing-by-majestic-kalandula-falls-angola-29932465/", "Cardoso Lopes", "Pexels License", "Kalandula Falls, Malanje, Angola"),
       ("Pexels", "https://www.pexels.com/photo/adventurer-at-majestic-waterfall-in-malanje-29932468/", "Cardoso Lopes", "Pexels License", "Kalandula Falls, Malanje")],
  25: [("Pexels", "https://www.pexels.com/photo/brown-monkey-on-gray-rock-7002325/", "atypeek", "Pexels License", "Gelada against Ethiopian highlands (Simien)"),
       ("Pexels", "https://www.pexels.com/photo/a-gelada-on-a-rock-25853766/", "atypeek", "Pexels License", "Gelada on rock, Ethiopian highlands"),
       ("Pexels", "https://www.pexels.com/photo/a-close-up-shot-of-a-gelada-monkey-sitting-on-a-rock-7002321/", "atypeek", "Pexels License", "Gelada, Simien Mountains"),
       ("Pexels", "https://www.pexels.com/photo/majestic-gelada-baboon-in-simien-mountains-39056951/", "atypeek", "Pexels License", "Gelada, Simien Mountains")],
  30: [("Pexels", "https://www.pexels.com/photo/scenic-panorama-with-river-cascade-and-a-distant-tepui-mountain-canaima-national-park-venezuela-7360544/", "Ederik Palencia Ferreira", "Pexels License", "Canaima NP cascade with tepui"),
       ("Pexels", "https://www.pexels.com/photo/mountain-under-cloudy-sky-12693427/", "Frank Araujo", "Pexels License", "Cerro Autana tepui, Venezuela")],
  31: [("Pexels", "https://www.pexels.com/photo/zuma-rock-in-nigeria-under-clear-blue-sky-29560016/", "solomon-onyeagoro", "Pexels License", "Zuma Rock, blue sky, greenery"),
       ("Pexels", "https://www.pexels.com/photo/zuma-rock-in-abuja-nigeria-majestic-landmark-31800347/", "felix-olojede", "Pexels License", "Zuma Rock, clear sky"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-zuma-rock-in-nigeria-32413269/", "harrun-muhammad", "Pexels License", "Aerial Zuma Rock"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-iconic-zuma-rock-in-nigeria-32413125/", "harrun-muhammad", "Pexels License", "Aerial Zuma Rock"),
       ("Pexels", "https://www.pexels.com/photo/view-of-the-zuma-rock-in-niger-state-nigeria-21715785/", "akoonie", "Pexels License", "Zuma Rock above village"),
       ("Pexels", "https://www.pexels.com/photo/zuma-rock-monolith-in-nigeria-seen-from-a-car-9593297/", "planeteelevene", "Pexels License", "Zuma Rock near Suleja")],
  32: [("Pexels", "https://www.pexels.com/photo/dead-trees-in-deadvlei-namibia-26968203/", "Bruno Almeida", "Pexels License", "Deadvlei dead trees"),
       ("Pexels", "https://www.pexels.com/photo/two-dead-trees-in-the-desert-with-sand-dunes-in-the-background-27441219/", "Hans Lutjes", "Pexels License", "Deadvlei trees + dunes"),
       ("Pexels", "https://www.pexels.com/photo/dry-bare-trees-on-desert-18616976/", "Kallie Calitz", "Pexels License", "Deadvlei camel thorn trees"),
       ("Pexels", "https://www.pexels.com/photo/stunning-sossusvlei-desert-landscape-in-namibia-35043952/", "hub-jacqu", "Pexels License", "Sossusvlei dead trees and red dunes"),
       ("Pexels", "https://www.pexels.com/photo/majestic-dead-trees-in-sossusvlei-desert-landscape-35043955/", "hub-jacqu", "Pexels License", "Deadvlei dead trees"),
       ("Pexels", "https://www.pexels.com/photo/leafless-trees-near-a-desert-10259907/", "Wendy R", "Pexels License", "Deadvlei with dunes"),
       ("Pexels", "https://www.pexels.com/photo/bare-tree-in-desert-5125151/", "Roger Brown", "Pexels License", "Deadvlei dead tree")],
  33: [("Pexels", "https://www.pexels.com/photo/beach-along-turquoise-sea-12437389/", "carlos-jamaica", "Pexels License", "Aerial Mozambique coastline, turquoise water"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-coastal-island-with-blue-waters-34109834/", "droneafrica", "Pexels License", "Aerial island, turquoise (location to verify)"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-pristine-island-and-blue-waters-34109835/", "droneafrica", "Pexels License", "Aerial island (location to verify)"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-tropical-island-coastline-34109832/", "droneafrica", "Pexels License", "Aerial island (location to verify)")],
  40: [("Pexels", "https://www.pexels.com/photo/stunning-view-of-band-e-amir-lake-in-afghanistan-28889933/", "Wasim Mirzaie", "Pexels License", "Band-e Amir lake and cliffs"),
       ("Pexels", "https://www.pexels.com/photo/stunning-view-of-band-e-amir-national-park-lake-31736016/", "Mahdi Ansel", "Pexels License", "Band-e Amir cliffs"),
       ("Pexels", "https://www.pexels.com/photo/band-e-amir-national-park-afghanistan-11854377/", "azadphotos", "Pexels License", "Band-e Amir with boats"),
       ("Pexels", "https://www.pexels.com/photo/rock-formation-surrounded-by-a-lake-12821744/", "sulimansallehi", "Pexels License", "Cliff reflected in lake (likely Band-e Amir)"),
       ("Pexels", "https://www.pexels.com/photo/eroded-sandstone-vertical-wall-along-river-12821773/", "sulimansallehi", "Pexels License", "Cliffs by water (likely Band-e Amir)"),
       ("Pexels", "https://www.pexels.com/photo/brown-rock-formations-beside-the-blue-sea-12821775/", "sulimansallehi", "Pexels License", "Cliffs over blue lake (likely Band-e Amir)")],
  41: [("Pexels", "https://www.pexels.com/photo/aerial-view-of-mogadishu-overlooking-the-indian-ocean-40163418/", "Ibrahim Halil Degerli", "Pexels License", "Mogadishu coast and Indian Ocean"),
       ("Pexels", "https://www.pexels.com/photo/fishing-boats-and-old-ruin-in-mogadishu-somalia-5702144/", "yahyesomali", "Pexels License", "Mogadishu old ruin and fishing boats")],
 },
 "02": {
  15: [("Pexels", "https://www.pexels.com/photo/scenic-aerial-view-of-desert-oasis-and-sand-dunes-36885274/", "Mohammed Alnaily", "Pexels License", "Aerial oasis among dunes, Libya (location stated on page)"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-oasis-in-vast-desert-landscape-36885275/", "Mohammed Alnaily", "Pexels License", "Same series, Libya"),
       ("Pexels", "https://www.pexels.com/photo/stunning-oasis-in-the-expansive-sahara-desert-36885278/", "Mohammed Alnaily", "Pexels License", "Same series, Libya"),
       ("Pexels", "https://www.pexels.com/photo/majestic-desert-arch-in-sahara-landscape-36885280/", "Mohammed Alnaily", "Pexels License", "Stone arch in the Sahara, same series")],
  16: [("Pexels", "https://www.pexels.com/photo/damavand-27459097/", "Sinna Nazari", "Pexels License", "Snow-capped Mount Damavand, Iran"),
       ("Unsplash", "https://unsplash.com/photos/a-mountain-with-snow-wGRY6UEYJMc", "arshia jafari", "Unsplash License", "Mount Damavand (used in ep02)",
        "https://images.unsplash.com/photo-1661334836702-7a332fb15dc5?fm=jpg&q=95")],
  19: [("Flickr", "https://www.flickr.com/photos/davidstanleytravel/23532185684/", "David Stanley", "CC BY 2.0", "Aloba Arch, Ennedi (original 1024x768)",
        "https://live.staticflickr.com/1529/23532185684_397657036b_o.jpg"),
       ("Flickr", "https://www.flickr.com/photos/davidstanleytravel/24105901212/", "David Stanley", "CC BY 2.0", "Ennedi hoodoos (original 1024x768)",
        "https://live.staticflickr.com/1529/24105901212_7e89dac165_o.jpg"),
       ("Flickr", "https://www.flickr.com/photos/davidstanleytravel/23509788093/", "David Stanley", "CC BY 2.0", "Ennedi Mountains (original 1024x768)",
        "https://live.staticflickr.com/1441/23509788093_16a6b12fa5_o.jpg")],
  20: [("Pexels", "https://www.pexels.com/photo/agadez-grand-mosque-in-the-sun-38108932/", "sanimaikatanga", "Pexels License", "Agadez Grand Mosque (16th c. mud-brick, UNESCO)"),
       ("Pexels", "https://www.pexels.com/photo/ancient-ruins-on-desert-8236033/", "andre", "Pexels License", "Agadez mosque amid desert sand"),
       ("Pexels", "https://www.pexels.com/photo/people-on-camels-13851626/", "andre", "Pexels License", "Camels at Cure Salee, Ingall, Niger"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-brown-field-8236054/", "andre", "Pexels License", "Aerial desert near Niamey")],
  22: [("Pexels", "https://www.pexels.com/photo/boats-on-a-river-17676145/", "Fatih Turan", "Pexels License", "Niger River boats, Bamako, Mali"),
       ("Pexels", "https://www.pexels.com/photo/view-of-a-riverbank-17676147/", "Fatih Turan", "Pexels License", "Niger River, Bamako"),
       ("Pexels", "https://www.pexels.com/photo/aerial-view-of-boats-on-a-river-17676148/", "Fatih Turan", "Pexels License", "Niger River, Bamako")],
  29: [("Unsplash", "https://unsplash.com/photos/a-giraffe-standing-in-a-field-with-a-mountain-in-the-background-1ZfMAnL4ubE", "Stephan Bechert", "Unsplash License",
        "Kilimanjaro with giraffe (used in ep02)", "https://images.unsplash.com/photo-1631646109248-a7264aae1790?fm=jpg&q=90&w=3000&fit=max")],
  39: [("EGU Imaggeo / INPE via Flickr", "https://www.egu.eu/medialibrary/image/4254/aerial-image-of-the-sudd-wetlands-in-south-sudan/",
        "Coordenação-Geral de Observação da Terra/INPE", "CC BY-SA 2.0", "Sudd wetlands, South Sudan (satellite/aerial)",
        "https://www.egu.eu/media/filer_public/da/31/da31732f-5e60-4959-9081-f4f6a2511855/45666872191_44e388ee1f_o.jpg")],
 },
}


def direct(source: str, page: str) -> str:
    if source == "Pexels":
        pid = re.search(r"-(\d+)/?$", page).group(1)
        return f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg"
    if source == "Unsplash":
        uid = page.rstrip("/").split("-")[-1].split("/")[-1]
        return f"https://unsplash.com/photos/{uid}/download?force=true"
    return page


def ok(url: str) -> tuple[bool, str]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
        ct = r.headers.get("Content-Type", "")
        n = len(r.read())
        return ct.startswith("image/") and n > 50_000, f"{ct} {n}"
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def main(tag: str) -> None:
    data = json.load(open(EP / "data.json", encoding="utf-8"))
    items = []
    for idx, cands in BATCHES[tag].items():
        it = data["items"][idx]
        key = f"{idx:02d}_{Path(it['image']).stem}"
        imgs = []
        for source, page, author, lic, why, *explicit in cands:
            url = explicit[0] if explicit else direct(source, page)
            good, info = ok(url)
            if not good and source == "Pexels":          # 新近上传的 Pexels 原图是 PNG：同 id 换 .png?fm=jpg
                url = url.replace(".jpeg", ".png?cs=srgb&fm=jpg")
                good, info = ok(url)
            print(key, "OK " if good else "BAD", url, info)
            if good:
                imgs.append({"image_url": url, "page_url": page, "source": source, "author": author, "licence": lic, "why": why})
        items.append({"key": key, "images": imgs})
    out = EP / "_build" / "reselect" / f"claude_{tag}.json"
    out.write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1])
