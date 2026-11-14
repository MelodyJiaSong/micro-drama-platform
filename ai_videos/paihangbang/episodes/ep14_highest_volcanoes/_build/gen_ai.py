# -*- coding: utf-8 -*-
"""follow-up 016：两轮搜索仍无可商用图的项，默认母版用 Codex 生成图（tools/codex_image.py，脚本先记请求日志）。
画面按 content/ 里的 GVP 描述写，求真实可信，但不冒充任何一张真实照片；不生成人物、logo、文字。

    python _build/gen_ai.py <rank> [<rank> ...] [--try N]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
EP = H.parent
REPO = EP.parents[3]

LOOK = {
    1: "Ojos del Salado, a vast desert stratovolcano in the Puna de Atacama: a broad massif with a jagged rocky summit crater rim, thin snow streaks on its upper slopes, ochre, rust and grey volcanic slopes, a turquoise salt lagoon (Laguna Verde) and pale desert plain in the foreground",
    2: "Llullaillaco, an isolated steep symmetric stratovolcano rising alone above the bone-dry Atacama Desert, upper third streaked with snow and ice, dark brown lava flows on its flanks, a white salt flat and sparse golden grass tufts in the foreground",
    3: "the Tipas volcanic complex in the Argentine Puna: a huge rounded massif of reddish-brown and dark grey lava domes and thick lava flows with scattered snow patches, a rocky desert valley with yellow paja brava grass in the foreground",
    4: "Nevado de Incahuasi, a massive desert stratovolcano with a broad snow-dusted summit and a small summit crater, long brown lava flows on its flanks, high Puna plateau with a small blue lagoon in front",
    5: "Nevado Coropuna in southern Peru: a broad elongated volcanic massif covered by a wide white ice cap with several rounded snowy summits, dark rock below the ice, golden puna grassland and a few stone walls in the foreground",
    6: "Cerro El Cóndor, a dark brown and grey stratovolcano with a symmetric cone and a small snow cap, in the empty high desert of the Catamarca Puna, a pale salt-crusted basin and low dunes in front",
    7: "Parinacota, a perfectly symmetric snow-capped stratovolcano reflected in the calm water of a high-altitude lake (Lago Chungará), its twin Pomerape partly visible behind on the left, green bofedal wetland grass on the shore",
    9: "Pular, a long volcanic ridge with several snow-streaked summits in the Atacama, reddish-brown and grey slopes, a white salt flat (Salar de Pular) with a thin blue lagoon in the foreground",
    10: "Cerro El Solo, a steep, isolated rocky volcanic cone with snow patches, standing alone in a vast reddish Puna desert, distant larger volcanoes faint on the horizon",
    11: "Sierra Nevada de Lagunas Bravas, a long ridge of several snow-dusted volcanic summits above high-desert salt lagoons with pale turquoise water and white salt rims",
    12: "Aracar, an isolated almost perfectly conical stratovolcano with a thin snow cap, rising above the white Salar de Arizaro salt flat in the Argentine Puna, brown desert plain in front",
    13: "Guallatiri, a snow-capped stratovolcano with a thin white fumarole plume drifting from its summit, golden altiplano grassland with a few grazing vicuñas and a small wetland stream in the foreground",
    14: "San José, a large glacier-covered volcanic massif at the head of a deep Andean valley in central Chile, white glaciers above dark rock walls, a grey river bed and green scrub in the foreground",
    15: "Socompa, a broad brown stratovolcano with snow patches near the summit and a huge horseshoe-shaped collapse scar, a turquoise lagoon with pink flamingos far away in the foreground and dry desert plain",
    16: "Acamarachi, a very steep, perfectly conical stratovolcano with snow streaks near its pointed summit, standing above the Atacama altiplano with golden paja brava grass and a deep-blue lagoon in front",
    17: "Sairecabur, a broad volcanic massif with several snow-dusted summits seen across the Atacama altiplano, brown and violet slopes, dry grassland in front",
    21: "Miñiques, a broad brown volcanic massif with light snow, rising behind a deep-blue high-altitude lagoon (Laguna Miñiques) bordered by white salt and golden grass",
    22: "Falso Azufre, a broad reddish volcanic massif with several craters and snow streaks on the Chile–Argentina border, high desert with a pale lagoon",
    23: "Putana, a snow-capped stratovolcano with yellow sulphur deposits and a faint steam plume at its summit, a high-altitude river wetland with green grass and grazing vicuñas in front",
    24: "Taapaca (Nevados de Putre), a snowy volcanic dome complex rising above terraced green fields and stone walls of an Andean village area in northern Chile",
    25: "Cordón de Puntas Negras, a chain of dark volcanic cones with snow patches above red and white salt flats and a turquoise lagoon in the Atacama",
    26: "Tutupaca, a snow-capped volcano with two summits and a large collapse scar, steaming fumaroles, puna grassland and a small lake in the foreground, southern Peru",
    28: "Cayambe, a broad heavily glaciated volcano in Ecuador with wide white glaciers and blue ice cliffs, green páramo grassland in the foreground",
    29: "Chiliques, a symmetric snow-capped stratovolcano rising behind a calm blue altiplano lagoon with white salt edges and golden grass",
    30: "Antisana, a massive glaciated volcano with several white summits above green páramo grassland and a small lagoon, Ecuador",
    31: "Cerro Peinado, a very symmetrical dark volcanic cone with a light snow cap, a turquoise lagoon with pink flamingos at its foot, Argentine Puna",
    32: "Lastarria, a brown volcano with bright yellow sulphur deposits and several white steam plumes rising from fumaroles near its summit, high desert",
    33: "the Olca–Paruma volcanic chain, an east–west ridge of brown and ochre volcanic summits with snow streaks above a white salt flat on the Chile–Bolivia altiplano",
    34: "the Purico volcanic complex, broad brown volcanic summits and a rounded dome on a high Atacama plateau with sparse yellow grass, very clear dark-blue sky",
    36: "Tupungatito, an active volcano with a glacier-filled summit crater and white steam rising from it, below the much larger snowy mass of Tupungato, central Andes",
    38: "Colachi, a snow-streaked brown volcanic cone next to a steeper cone, above the Atacama altiplano with a dark-blue lagoon",
    39: "Nevados Casiri, a group of snow-capped volcanic peaks above high puna lakes and golden grassland in southern Peru",
    40: "Ubinas, a truncated volcanic cone with a wide summit crater emitting a grey ash plume, terraced fields and a small Andean village in the valley below",
    41: "Guayaques, rounded brown lava-dome summits with light snow on the Chile–Bolivia altiplano, salt flat and lagoon in the foreground",
    42: "Láscar, a brown truncated stratovolcano with a white steam and gas plume rising from its summit crater, Atacama altiplano with golden grass in front",
    44: "Isluga, a snow-dusted volcanic cone with a small fumarole plume, a white adobe Andean church and green wetland with grazing llamas in the foreground",
    45: "Yucamane, a steep snow-capped symmetric stratovolcano above a blue high-Andean lake and golden puna grassland, southern Peru",
    46: "Cordón del Azufre, a row of brown, ochre and pale yellow volcanic vents and lava flows with sulphur stains in the high Puna desert",
    47: "Corrida de Cori, a group of small brown and black volcanic cones and dark lava flows in a high desert near a white salt flat, a large snowy volcano far in the background",
    48: "Tata Sabaya, a snow-capped stratovolcano rising above the brilliant white Salar de Coipasa salt flat in Bolivia",
    49: "Cerro Bayo, pale yellowish-brown volcanic peaks and domes in the high Puna desert on the Chile–Argentina border, rocky foreground",
}

TEMPLATE = ("Photorealistic landscape photograph, portrait orientation, aspect ratio 9:10. {look}. "
            "The whole volcano is clearly visible, seen from ground level a few kilometres away. Natural midday or "
            "golden-hour light, crisp detail, clear deep-blue high-altitude sky, rich but realistic colours. "
            "No people, no text, no logos, no watermark, no frame, no border.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ranks", nargs="+", type=int)
    ap.add_argument("--try", dest="tr", type=int, default=1)
    a = ap.parse_args()
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    (H / "gen_prompts").mkdir(exist_ok=True)
    for r in a.ranks:
        it = next(i for i in data["items"] if i["rank"] == r)
        stem = Path(it["image"]).stem
        suffix = "_gen" if a.tr == 1 else f"_gen{a.tr}"
        out = EP / "assets" / "img" / f"{stem}{suffix}.png"
        if out.exists():
            print("skip", out.name, flush=True)
            continue
        pf = H / "gen_prompts" / f"{stem}{suffix}.txt"
        pf.write_text(TEMPLATE.format(look=LOOK[r]), encoding="utf-8")
        rc = subprocess.run([sys.executable, str(REPO / "tools" / "codex_image.py"), "--out", str(out), "--prompt-file", str(pf)],
                            cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(r, out.name, "rc", rc.returncode, (rc.stdout + rc.stderr)[-300:].replace("\n", " "), flush=True)


if __name__ == "__main__":
    main()
