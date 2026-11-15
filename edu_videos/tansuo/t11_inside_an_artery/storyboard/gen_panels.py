"""Build prompt files from panels.json and generate via tools/codex_image.py."""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(r"C:\workspace\micro-drama-platform")
SB = ROOT / "edu_videos/tansuo/t11_inside_an_artery/storyboard"
spec = json.loads((SB / "panels.json").read_text(encoding="utf-8"))
only = set(sys.argv[1:])

HEAD = ("Cinematic film still, storyboard keyframe for a live-action-style educational short about blood lipids and arterial disease, matching the supplied cinematic style reference. "
        "Photorealistic fictional human presenters with natural skin texture, physically plausible tissue and molecular materials, cinematic soft key light, gentle rim light, subtle atmospheric haze, shallow depth of field. "
        "Spectacular but scientifically accountable science-documentary effects: volumetric light, particles and scale-change ripples only where they explain a real structure or process. "
        "Not cartoon, not fantasy, not a medical horror image. Molecular colors are explicitly explanatory coding rather than literal visible color. Composition must leave room for post-production labels.")
CHARS = ("The two people must match the photographic character reference sheets exactly: same faces, hair and clothing. They are fictional and must not resemble any real public figure. "
         "Lin: East Asian Chinese woman in her early thirties, long straight black hair in a neat low bun, no glasses, light grey zip work jacket with a thin amber stripe at each cuff, white tee, dark charcoal trousers, grey sneakers, one round black watch with an amber dial ring on her LEFT wrist only. "
         "Kai: young adult man of mixed Chinese and European heritage, wavy dark-brown hair, hazel eyes, tall and lanky, plain navy hoodie, khaki cargo pants, white sneakers, sand-colored canvas crossbody bag. "
         "Exactly these two presenters and no additional person anywhere in the image.")
TAIL = "No text, no letters, no numbers, no labels, no logos, no UI, no watermark. 16:9 landscape."


def job(p):
    if p.get('legacy_image'):
        return p['id'], '已改为功能分镜；用 render_diagrams.py 构建，旧图不再生成'
    out = SB / p.get('image', f"{p['id']}.png")
    if out.exists():
        return p["id"], "exists"
    (SB / "prompts").mkdir(exist_ok=True)
    pf = SB / "prompts" / f"{p['id']}.txt"
    pf.write_text("\n\n".join([HEAD, p["prompt"], CHARS, TAIL]), encoding="utf-8")
    cmd = [sys.executable, str(ROOT / "tools/codex_image.py"), "--out", str(out), "--prompt-file", str(pf)]
    refs = [ROOT / r for r in spec["char_refs"]]
    refs.append(ROOT / spec["style_ref"])
    for ref in refs:
        cmd += ["--ref", str(ref)]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (SB / "prompts" / f"{p['id']}.log").write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
    return p["id"], "ok" if out.exists() else "FAIL: " + (result.stderr.strip().splitlines() or ["?"])[-1][:300]


panels = [p for p in spec["panels"] if not only or p["id"] in only]
with ThreadPoolExecutor(1) as pool:
    for pid, status in pool.map(job, panels):
        print(pid, status, flush=True)
