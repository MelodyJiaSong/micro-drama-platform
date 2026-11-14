"""ep01 licenses.csv（bible §4.2）与 sources.md（bible §6 ②）。

    python ai_videos/zhenshi_chidu/_tools/make_ep01_meta.py

licenses.csv：场景里每个外部素材一行（主体模型、人体参照）。天空为 Blender 内置程序天空、地面为程序棋盘格，无外部素材。
sources.md：按名次列肩高、体长与出处（标题、链接、读取日期），供审片追溯与描述框引用。
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
EP = ROOT / "episodes" / "ep01_largest_land_animals"
FIELDS = ["item_rank", "item_name", "role", "source", "asset_id", "url", "title", "author", "license", "license_url",
          "attribution_text", "modified", "downloaded_at", "sha256"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    dims = {d["name"]: d for d in json.loads((ROOT / "0_research/ep01_animal_dimensions.json").read_text(encoding="utf-8"))}
    rows = []
    cut_mode = all(it.get("cutout") for it in data["items"])
    if cut_mode:   # 第 2 版 2.5D：主体是 Codex 侧面参考图的抠像（_tools/cutouts.py）
        cuts = json.loads((EP / "assets/cutouts/cutouts.json").read_text(encoding="utf-8"))
        for it in data["items"]:
            p = REPO / it["cutout"]["png"]
            rows.append({
                "item_rank": it["rank"], "item_name": it["name"], "role": "subject",
                "source": "AI-generated in-house: Codex image_gen side-view image (OpenAI terms: output owned by user), "
                          "background removed with rembg isnet-general-use (Apache-2.0)",
                "asset_id": it["model"]["key"], "url": "", "title": f"{it['name']} (AI IMAGE)", "author": "zhenshi_chidu (generated)",
                "license": "own-generated", "license_url": "https://openai.com/policies/terms-of-use",
                "attribution_text": "", "modified": True, "downloaded_at": "2026-11-07", "sha256": sha(p),
            })
        hp = REPO / cuts["human"]["png"]
        rows.append({
            "item_rank": "", "item_name": "1.75 m man", "role": "human",
            "source": "AI-generated in-house: Codex image_gen full-body image (fictional person), background removed with rembg isnet-general-use",
            "asset_id": "human_man_v1", "url": "", "title": "1.75 m man (AI IMAGE)", "author": "zhenshi_chidu (generated)",
            "license": "own-generated", "license_url": "https://openai.com/policies/terms-of-use",
            "attribution_text": "", "modified": True, "downloaded_at": "2026-11-07", "sha256": sha(hp),
        })
        for key, title in [("env_plate_v1", "Savanna horizon backdrop (AI IMAGE)"), ("env_acacia_a", "Umbrella acacia (AI IMAGE)"),
                           ("env_acacia_b", "Young acacia (AI IMAGE)"), ("env_bush_a", "Thorn bush (AI IMAGE)")]:
            src = EP / "assets" / "ref_images" / f"{key}.png"
            if src.exists():
                rows.append({
                    "item_rank": "", "item_name": title, "role": "environment",
                    "source": "AI-generated in-house: Codex image_gen (OpenAI terms: output owned by user)" + ("" if key == "env_plate_v1" else "; background removed with rembg isnet-general-use"),
                    "asset_id": key, "url": "", "title": title, "author": "zhenshi_chidu (generated)", "license": "own-generated",
                    "license_url": "https://openai.com/policies/terms-of-use", "attribution_text": "", "modified": key != "env_plate_v1",
                    "downloaded_at": "2026-11-08", "sha256": sha(src),
                })
        shared = ROOT / "_shared"
        for f, title, author, url in [
            ("hdri/mpumalanga_veld_8k.hdr", "Mpumalanga Veld (HDRI)", "Greg Zaal", "https://polyhaven.com/a/mpumalanga_veld"),
            ("hdri/plains_sunset_4k.hdr", "Plains Sunset (HDRI)", "Dimitrios Savva, Jarod Guest", "https://polyhaven.com/a/plains_sunset"),
            ("tex/grass_ground/grass_ground_diff_2k.jpg", "Grass Ground (texture set)", "Charlotte Baglioni", "https://polyhaven.com/a/grass_ground"),
            ("models/grass_medium_01/grass_medium_01.gltf", "Grass Medium 01 (3D model)", "Rob Tuytel, Rico Cilliers", "https://polyhaven.com/a/grass_medium_01"),
            ("models/grass_medium_02/grass_medium_02.gltf", "Grass Medium 02 (3D model)", "Rico Cilliers", "https://polyhaven.com/a/grass_medium_02"),
            ("models/grass_bermuda_01/grass_bermuda_01.gltf", "Grass Bermuda 01 (3D model)", "Rico Cilliers", "https://polyhaven.com/a/grass_bermuda_01"),
            ("models/moon_rock_02/moon_rock_02.gltf", "Moon Rock 02 (3D model)", "Rico Cilliers, Greg Zaal, Jenelle van Heerden", "https://polyhaven.com/a/moon_rock_02"),
        ]:
            rows.append({
                "item_rank": "", "item_name": title, "role": "environment", "source": "Poly Haven", "asset_id": url.rsplit("/", 1)[1],
                "url": url, "title": title, "author": author, "license": "CC0-1.0",
                "license_url": "https://polyhaven.com/license", "attribution_text": f"{title} by {author}, Poly Haven (CC0)",
                "modified": False, "downloaded_at": "2026-11-07", "sha256": sha(shared / f),
            })
    for it in ([] if cut_mode else data["items"]):
        m = it["model"]
        p = REPO / m["path"]
        rows.append({
            "item_rank": it["rank"], "item_name": it["name"], "role": "subject",
            "source": "AI-generated in-house: Codex image_gen reference (OpenAI terms: output owned by user) + local TripoSR (MIT)",
            "asset_id": m["key"], "url": "", "title": f"{it['name']} (AI MODEL)", "author": "zhenshi_chidu (generated)",
            "license": "own-generated", "license_url": "https://github.com/VAST-AI-Research/TripoSR/blob/main/LICENSE",
            "attribution_text": "", "modified": True, "downloaded_at": "2026-11-07", "sha256": sha(p),
        })
        if sha(p) != m["sha256"]:
            raise SystemExit(f"模型 sha256 与 models_ai.json 不符：{p}")
    if not cut_mode:
      rows.append({
        "item_rank": "", "item_name": "1.75 m man", "role": "human",
        "source": "MPFB 2.0.18 (MakeHuman for Blender) bundled base mesh, baked to static mesh",
        "asset_id": "mpfb_base_male", "url": "https://extensions.blender.org/add-ons/mpfb/",
        "title": "MakeHuman base mesh", "author": "MakeHuman community", "license": "CC0-1.0",
        "license_url": "https://raw.githubusercontent.com/makehumancommunity/mpfb2/master/LICENSE.md",
        "attribution_text": "", "modified": True, "downloaded_at": "2026-11-06", "sha256": "",
    })
    with (EP / "licenses.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    lines = ["# ep01 · 出处（肩高排名）", "",
             "> 由 `_tools/make_ep01_meta.py` 从 `0_research/ep01_animal_dimensions.json` 生成；取值说明与分歧取舍见该目录的 `.md`。",
             f"> 口径：{data['metric_label']}。所有链接读取于 2026-11-06。", ""]
    for it in data["items"]:
        d = dims[it["name"]]
        lines.append(f"## {'=' if it['tied'] else '#'}{it['rank']} {it['name']} — {it['value_display']}（卡上出处：{it['source_short']}）")
        lines.append(f"- 肩高 {d['shoulder_height_m']} m，头体长 {d['head_body_length_m']} m；取值方式 {d['value_kind']}；性别口径 {d['sex_basis']}")
        for s in d["sources"]:
            lines.append(f"- {s['name']} — <{s['url']}>")
        cc = d.get("cross_check") or {}
        if cc:
            lines.append(f"- 交叉核对：{cc.get('source', '')}：{cc.get('value', '')} — <{cc.get('url', '')}>")
        lines.append("")
    (EP / "sources.md").write_text("\n".join(lines), encoding="utf-8")

    # YouTube 置顶评论：每条名次、物种、肩高、主出处与链接（publish.md 引用此文件）
    # 出处与卡上简称对应：按简称关键词挑 sources 里的那一条，找不到才用第一条；超 5000 字拆成置顶 + 回复
    keys = {"Handbook": ("Handbook", "HMW"), "Animal": ("ADW", "Animal Diversity"), "ADW": ("ADW",),
            "San": ("San Diego", "SDZWA"), "IUCN": ("IUCN",), "Halloran": ("Halloran", "Krasi")}
    pc_rows = []
    for it in data["items"]:
        srcs = dims[it["name"]]["sources"]
        first = it["source_short"].split()[0]
        kw = keys.get(first, (first,))
        s0 = next((s for s in srcs if any(k in s["name"] for k in kw)), srcs[0])
        cite = f"{s0['name']} — {s0['url']}"
        if "/" in it["source_short"]:          # 卡上并列两个出处（如 ADW / ADF&G）：两条都列
            second = it["source_short"].split("/")[1].split()[0]
            s1 = next((s for s in srcs if second in s["name"] and s is not s0), None)
            if s1:
                cite += f" ; {s1['name']} — {s1['url']}"
        pc_rows.append(f"{'=' if it['tied'] else '#'}{it['rank']} {it['name']} {it['value_display']}: {cite}")
    head = "Shoulder-height sources (typical adults; males where data allow). Rank · animal · value: source — link"
    parts = [[head + " (1/2)"] + pc_rows[:15], ["(2/2)"] + pc_rows[15:]]
    text = "\n\n".join("\n".join(p) for p in parts)
    for p in parts:
        assert len("\n".join(p)) <= 5000, "单条评论超过 5000 字"
    (EP / "_build" / "pinned_comment.txt").write_text(text + "\n", encoding="utf-8")
    print(len(rows), "license rows; sources.md written")


if __name__ == "__main__":
    main()
