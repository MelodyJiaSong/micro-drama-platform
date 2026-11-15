"""Build storyboard prompts and generate via codex_image.py. Set PANEL_SPEC for additions."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(r"C:\workspace\micro-drama-platform")
SB = ROOT / "edu_videos/tansuo/t01_inside_a_chip/storyboard"
spec = json.loads((SB / os.environ.get("PANEL_SPEC", "panels.json")).read_text(encoding="utf-8"))
only = set(sys.argv[1:])

HEAD = ("Cinematic film still, storyboard keyframe for a live-action-style educational short about microchips (match the style reference image). "
        "Photorealistic: real human actors with natural skin texture, physically plausible materials, cinematic lighting with soft key, gentle rim light and subtle atmospheric haze, "
        "shallow depth of field, anamorphic film look. Spectacular, imaginative visual effects like a big-budget science documentary feature: volumetric light, particles, light trails, bloom; the effects depict real phenomena (light, electric signals, electrons, change of scale, structures splitting apart). Not cartoon, not 3D animation style. Structures stay physically plausible: no decorative fake circuit patterns, no floating UI, no holographic text.")
CHARS = ("The two people must match the photographic character reference sheets exactly (same faces, hair, clothing); they are fictional and must not resemble any real public figure. "
         "Lin: strikingly beautiful East Asian (Chinese) woman in her early thirties with elegant intellectual beauty, long straight black hair in a neat low bun with a few soft face-framing strands, no glasses, "
         "light grey zip work jacket with a thin amber stripe at each cuff, white tee, dark charcoal trousers, grey sneakers, round black watch with an amber dial ring on her left wrist. "
         "Lin wears her single round black watch on her LEFT wrist only, nothing on her right wrist, and never wears glasses. "
         "Kai: young man of mixed Chinese and European heritage in his early twenties, wavy dark-brown hair, hazel eyes, tall and lanky, plain navy blue hoodie, khaki cargo pants, white sneakers, sand-colored canvas crossbody bag.")
MAT = ("Chip structures with physically plausible materials (match the style reference image): polished copper wires with warm reflections, grey silicon, "
       "clear glassy insulating material with subtle refraction, contacts and gate metal dark steel grey. Vias are short square plugs no wider than the wires, connecting only adjacent layers; no tall round copper columns, no flanges, no glass rings around vias; clear glassy insulation fills the space between wires.")
TAIL = "No text, no letters, no numbers, no labels, no logos, no UI, no watermark. 16:9 landscape."


def job(p):
    out = SB / f"{p['id']}.png"
    if out.exists():
        return p["id"], "exists"
    parts = [HEAD, p["prompt"], CHARS]
    refs = [ROOT / r for r in spec["char_refs"]]
    if p.get("style_ref"):
        refs.append(ROOT / spec["style_ref"])
    if p.get("materials", p["id"] not in ("P01", "P02", "P11", "P12", "P14")):
        parts.append(MAT)
    parts.append(TAIL)
    pf = SB / "prompts" / f"{p['id']}.txt"
    pf.write_text("\n\n".join(parts), encoding="utf-8")
    cmd = [sys.executable, str(ROOT / "tools/codex_image.py"), "--out", str(out), "--prompt-file", str(pf)]
    for r in refs:
        cmd += ["--ref", str(r)]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (SB / "prompts" / f"{p['id']}.log").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    return p["id"], "ok" if out.exists() else "FAIL: " + (r.stderr.strip().splitlines() or ["?"])[-1][:300]


panels = [p for p in spec["panels"] if not only or p["id"] in only]
with ThreadPoolExecutor(6) as ex:
    for pid, st in ex.map(job, panels):
        print(pid, st, flush=True)
