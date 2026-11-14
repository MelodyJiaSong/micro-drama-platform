# -*- coding: utf-8 -*-
"""复核小修：按名称重出生成图（去掉村庄 / 教堂等可识别建筑；外形按真实火山特征写）。
输出 assets/img/<stem>_gen2.png（旧 _gen.png 保留，换用后由 swap 写回 data / assets）。经 tools/codex_image.py（先记请求日志）。

    python _build/gen_ai2.py <name> [<name> ...]
"""
import json
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
EP = H.parent
REPO = EP.parents[3]

LOOK = {
    "Isluga": "Isluga volcano in the Chilean altiplano: a broad snow-dusted stratovolcano with a wide flat-topped summit and a thin fumarole plume, dark lava flows on its flanks, empty high-altitude plain with golden paja brava grass and a small wetland stream in the foreground; no buildings, no animals",
    "Taapaca": "Taapaca volcanic complex in northern Chile: a cluster of steep snow-capped lava-dome summits with grey and ochre rocky slopes, rising above an empty high Andean valley with golden grass and scattered rocks; no village, no buildings, no fields, no walls",
    "Llullaillaco": "Llullaillaco volcano: a massive, very tall stratovolcano with a rugged, craggy rocky summit ridge (not a smooth cone), long streaks of snow and ice running down steep dark-brown gullies, wide lava flows on its lower flanks, rising alone above the bone-dry reddish Atacama Desert plateau; no lake, no people",
    "Incahuasi": "Nevado de Incahuasi: a huge broad volcanic massif with a wide rounded summit plateau and a small summit crater, patchy snow on the upper slopes, reddish-brown and grey lava flows, seen across the empty high Puna desert near the Chile–Argentina border; no lake, no people",
    "Ojos del Salado": "Ojos del Salado, the highest volcano on Earth: a vast, broad desert massif with a jagged rocky summit crater rim and several craters, thin snow and ice patches on its upper slopes, ochre, rust and grey volcanic slopes, seen from a pale high-altitude desert plain; no lake, no people",
    "Coropuna": "Nevado Coropuna in southern Peru: a broad elongated volcanic massif covered by a wide white ice cap with several rounded snowy summits, dark rock below the ice, golden puna grassland in the foreground; no buildings, no walls",
}
TEMPLATE = ("Photorealistic landscape photograph, portrait orientation, aspect ratio 9:10. {look}. "
            "The whole volcano is clearly visible, seen from ground level several kilometres away. Natural light, crisp detail, "
            "realistic colours, clear high-altitude sky. No people, no buildings, no text, no logos, no watermark, no frame.")


def main() -> None:
    d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    (H / "gen_prompts").mkdir(exist_ok=True)
    for name in sys.argv[1:]:
        it = next(i for i in d["items"] if i["name"] == name)
        stem = Path(it["image"]).stem.replace("_gen", "").replace("_nasa", "")
        out = EP / "assets" / "img" / f"{stem}_gen2.png"
        if out.exists():
            print("skip", out.name); continue
        pf = H / "gen_prompts" / f"{stem}_gen2.txt"
        pf.write_text(TEMPLATE.format(look=LOOK[name]), encoding="utf-8")
        r = subprocess.run([sys.executable, str(REPO / "tools" / "codex_image.py"), "--out", str(out), "--prompt-file", str(pf)],
                           cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(name, out.name, "rc", r.returncode, (r.stdout + r.stderr)[-200:].replace("\n", " "), flush=True)


if __name__ == "__main__":
    main()
