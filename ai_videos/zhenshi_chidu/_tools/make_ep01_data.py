"""ep01 data.json：按肩高重排名（bible §3），并接上 AI 模型标定（models_ai.json）。

    python ai_videos/zhenshi_chidu/_tools/make_ep01_data.py

输入：0_research/ep01_animal_dimensions.json（30 条尺寸与出处）、paihangbang ep04 data.json（地区、体重排名）、
      episodes/ep01_largest_land_animals/assets/models_ai/models_ai.json（模型与标定）。
输出：episodes/ep01_largest_land_animals/data.json。肩高相同并列同名次，名次内按体重排（体重排名小的在前）。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
EP = ROOT / "episodes" / "ep01_largest_land_animals"

# 卡片上的出处简称（肩高的主出处；全称与链接在 sources.md）
SOURCE_SHORT = {
    "African Bush Elephant": "Larramendi 2016",
    "Asian Elephant": "Larramendi 2016",
    "White Rhinoceros": "Handbook of the Mammals of the World",
    "Indian Rhinoceros": "Laurie, Lang & Groves 1983",
    "African Forest Elephant": "Larramendi 2016",
    "Hippopotamus": "San Diego Zoo Wildlife Alliance",
    "Javan Rhinoceros": "Handbook of the Mammals of the World",
    "Giraffe": "Ciofolo & Le Pendu 2013 (via SDZWA)",
    "Black Rhinoceros": "Hillman-Smith & Groves 1994",
    "Gaur": "Nowak 1999",
    "Wild Yak": "Leslie & Schaller 2009",
    "Wild Water Buffalo": "IUCN SSC Asian Wild Cattle SG",
    "American Bison": "Halloran 1960 (via Krasińska 2002)",
    "Sumatran Rhinoceros": "Handbook of the Mammals of the World",
    "African Buffalo": "Handbook of the Mammals of the World",
    "Banteng": "Handbook of the Mammals of the World",
    "Giant Eland": "Handbook of the Mammals of the World",
    "European Bison": "Krasińska & Krasiński 2002",
    "Common Eland": "Handbook of the Mammals of the World",
    "Moose": "Handbook of the Mammals of the World",
    "Polar Bear": "DeMaster & Stirling 1981",
    "Grévy's Zebra": "Handbook of the Mammals of the World",
    "Kiang": "Animal Diversity Web",
    "Brown Bear": "Seryodkin et al. 2016",
    "Elk (Wapiti)": "Handbook of the Mammals of the World",
    "Takin": "Animal Diversity Web",
    "Muskox": "ADW / Alaska Dept. of Fish & Game",
    "Bongo": "Handbook of the Mammals of the World",
    "Mountain Zebra": "Penzhorn 1988 (via ADW)",
    "Plains Zebra": "San Diego Zoo Wildlife Alliance",
}


# 肩高本身是推算值（来源冲突后的判断或按体重缩放）的条目，卡上加 ≈
SH_EST = {"Muskox", "Brown Bear"}


def _pooled_sh(sex_basis: str) -> bool:
    """肩高只有雌雄混合数据（卡上写 adults, both sexes）。"""
    sb = sex_basis.lower()
    return sb.startswith("sexes pooled") or "sh sexes pooled" in sb or "shoulder height adults" in sb


def ft_in(m: float) -> str:
    inches = round(m / 0.0254)
    return f"{inches // 12} ft {inches % 12} in"


def main() -> None:
    dims = json.loads((ROOT / "0_research" / "ep01_animal_dimensions.json").read_text(encoding="utf-8"))
    ep04 = json.loads((REPO / "ai_videos/paihangbang/episodes/ep04_largest_land_animals/data.json").read_text(encoding="utf-8"))
    region = {i["name"]: i["subtitle"] for i in ep04["items"]}
    region_iso = {i["name"]: i.get("country_iso2") for i in ep04["items"]}
    models = json.loads((EP / "assets/models_ai/models_ai.json").read_text(encoding="utf-8"))["models"]
    cut_path = EP / "assets/cutouts/cutouts.json"     # 第 2 版（2.5D 抠像，_tools/cutouts.py）
    cuts = json.loads(cut_path.read_text(encoding="utf-8")) if cut_path.exists() else {}
    by_rank_name = {(m["rank"], m["name"]): (k, m) for k, m in models.items()}

    rows = sorted(dims, key=lambda d: (-d["shoulder_height_m"], d["rank"]))
    items = []
    for d in rows:
        sh = d["shoulder_height_m"]
        rank = 1 + sum(1 for o in dims if o["shoulder_height_m"] > sh)
        tied = sum(1 for o in dims if o["shoulder_height_m"] == sh) > 1
        key, m = by_rank_name.get((d["rank"], d["name"]), (None, None))
        est = d["name"] in SH_EST
        items.append({
            "rank": rank, "tied": tied, "weight_rank": d["rank"], "name": d["name"],
            "scientific_name": d["scientific_name"], "region": region.get(d["name"]),
            "flag_iso2": region_iso.get(d["name"]), "mass_kg": d["mass_kg"],
            "value_display": f"{'≈' if est else ''}{sh:.2f} m", "secondary_display": ft_in(sh),
            "basis": "shoulder height · adults, both sexes" if _pooled_sh(d["sex_basis"]) else "shoulder height · adult male",
            "source_short": SOURCE_SHORT[d["name"]],
            "dims": {"height_m": sh, "length_m": d["head_body_length_m"], "basis": "shoulder_height"},
            "model": None if m is None else {
                "key": key, "path": m["model_path"], "sha256": m["model_sha256"], "ai_model": True,
                "import": m["import"], "landmark_ratio": m["landmark_ratio"],
                "landmark_x_frac": m.get("landmark_x_frac"),
            },
            "cutout": None if m is None or key not in cuts else {
                "png": cuts[key]["png"], "size": cuts[key]["size"], "shoulder_col": cuts[key]["shoulder_col"],
                "shoulder_top": cuts[key]["shoulder_top"], "bottom": cuts[key]["bottom"],
                "method": cuts[key]["method"], "note": cuts[key].get("note", ""),
            },
        })
    out = {
        "episode": "ep01_largest_land_animals",
        "title": "The 30 Largest Land Animals, Ranked by Height",
        "kicker": "TRUE SCALE",
        "metric_label": "Shoulder height · typical adult (male where data allow)",
        "scope_note": "The 30 heaviest wild land animals (same list as our weight ranking), re-ranked by typical "
                      "shoulder height; where sources give a range we use its midpoint. Ties share a rank. "
                      + ("All animal images are AI-generated for this video and scaled by script to the shoulder height shown."
                         if cuts else "All 3D models are AI-generated (reference image + TripoSR) and scaled by script to the shoulder height shown."),
        "period_label": "Data as of Nov 2026",
        "human_reference_m": 1.75,
        "insights": [
            {"after_rank": 21, "text": "Why shoulder height? Heads and necks move; the shoulder doesn't. The yellow line marks where each animal is measured."},
            {"after_rank": 11, "text": "From the next animal on, every one stands at least as tall at the shoulder as our 1.75 m man."},
        ],
        "items": items,
    }
    missing = [i["name"] for i in items if i["model"] is None]
    (EP / "data.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(len(items), "items; missing models:", missing)
    for i in items:
        print(("=" if i["tied"] else " ") + str(i["rank"]), i["name"], i["value_display"])


if __name__ == "__main__":
    main()
