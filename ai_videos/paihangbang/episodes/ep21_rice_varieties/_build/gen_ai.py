# -*- coding: utf-8 -*-
"""ep21：为品种出 AI 写实米粒图（follow-up 057：找不到合格真实照片就直接 Codex 出图）。
图存 _build/tiles/<key>/ai/ai1.png，不碰找图代理写的 cand/ 与 candidates.json；选图时再并入。经 tools/codex_image.py（先记 request_log）。
每种米配一个与产地相关的容器 / 台面（只有米，没有别的食物），避免 30 张卡都是「石板上一堆白米」。

    python ai_videos/paihangbang/episodes/ep21_rice_varieties/_build/gen_ai.py [--all | key ...] [--workers 3]
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
REPO = EP.parents[3]
sys.path.insert(0, str(EP / "_build"))
from make_data import LOOK, tile_key  # noqa: E402

SKIP = {1, 3, 7, 8, 9, 16, 20, 22, 30}   # 常见品种，先等真实照片（--all 或点名时也出）
SETTING = {
    1: "heaped in a small square wooden rice-measuring box (masu) on pale hinoki wood",
    2: "a small mound of highly polished, almost round grains on a dark indigo cloth beside a tiny white ceramic sake cup that is empty",
    3: "in a pale handmade wooden bowl on beige linen",
    4: "heaped on a red lacquer tray",
    5: "spread on a round woven bamboo sieve",
    6: "heaped on a fresh green banana leaf",
    7: "in a round woven bamboo winnowing tray, the broken fragments clearly visible",
    8: "plain steamed glutinous rice in a small woven bamboo basket (tip khao), lid open",
    9: "heaped on a woven rattan mat",
    10: "in a plain white ceramic dish on light wood, the purple grains contrasting with the white",
    11: "in a dark red-and-black Burmese lacquerware bowl",
    12: "in a polished brass bowl on dark wood",
    13: "a small mound on a green banana leaf beside a tiny brass bowl that is empty",
    14: "in a rough terracotta clay bowl",
    15: "in a hand-woven straw basket on rough stone, cool mountain daylight",
    16: "spilling from a hammered copper scoop onto a copper plate",
    17: "in a hand-painted blue-and-white Uzbek ceramic dish (lyagan)",
    18: "on a turquoise Persian glazed ceramic plate",
    19: "in a hammered copper bowl on a wooden table",
    20: "heaped on white Carrara marble",
    21: "in a rustic Provençal ceramic bowl on weathered grey wood",
    22: "in a terracotta cazuela dish",
    23: "heaped on blue-and-white Portuguese azulejo tiles",
    24: "in a wooden scoop resting on a burlap sack",
    25: "in a polished calabash bowl",
    26: "on a woven grass mat beside a small calabash",
    27: "in a white enamel cup lying on its side, grains spilling onto light wood",
    28: "in a dark Mexican clay bowl (barro negro)",
    29: "in a coiled sweetgrass basket",
    30: "on a piece of birch bark",
}


def prompt(it: dict) -> str:
    r = it["rank"]
    if r == 8:
        subject = SETTING[8]
    else:
        subject = f"raw grains {SETTING[r]}"
    return (f"Photorealistic close-up food photograph of {it['name']} rice ({it['subtitle']}). The rice: {LOOK[r]}. "
            f"Scene: {subject}. Show ONLY the rice itself; the rice fills most of the frame and a few loose grains in the "
            "foreground are in razor-sharp focus so the grain shape, size and colour are clearly readable. Soft natural "
            "window light from the side, shallow depth of field, true-to-life colours. Vertical 3:4 composition. "
            "No other food, no garnish, no sauces, no packaging, no labels, no text, no hands or people, no watermark.")


def run(it: dict) -> tuple[str, str]:
    key = tile_key(it["rank"] - 1, it["name"])
    d = EP / "_build/tiles" / key / "ai"
    d.mkdir(parents=True, exist_ok=True)
    out = d / "ai1.png"
    if out.exists():
        return key, "exists"
    pf = d / "prompt.txt"
    pf.write_text(prompt(it), encoding="utf-8")
    r = subprocess.run([sys.executable, str(REPO / "tools/codex_image.py"), "--out", out.relative_to(REPO).as_posix(),
                        "--prompt-file", str(pf)], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=REPO)
    return key, f"rc={r.returncode} {(r.stdout or r.stderr)[-200:].strip()}"


if __name__ == "__main__":
    argv = sys.argv[1:]
    w = int(argv[argv.index("--workers") + 1]) if "--workers" in argv else 3
    keys = [a for a in argv if not a.startswith("--") and not a.isdigit()]
    items = json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]
    if "--all" in argv:
        todo = items
    elif keys:
        todo = [it for it in items if tile_key(it["rank"] - 1, it["name"]) in keys]
    else:
        todo = [it for it in items if it["rank"] not in SKIP]
    with ThreadPoolExecutor(w) as ex:
        for key, msg in ex.map(run, todo):
            print(key, msg, flush=True)
