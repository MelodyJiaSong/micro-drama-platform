"""选角候选出图：每位候选一张四视图（正面、四分之三、正侧、背面），再以四视图为参考出一张六格表情。
用法：python gen_casting.py [候选id …]；已存在的图跳过。出图走 tools/codex_image.py（先记请求日志）。"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
spec = json.loads((HERE / "candidates.json").read_text(encoding="utf-8"))
only = set(sys.argv[1:])

PHOTO = ("Photorealistic casting photo sheet for a live-action educational series, shot like a professional film casting session: "
         "real human photography, natural skin texture with pores and subtle imperfections, 85mm lens, soft large studio key light, "
         "neutral seamless light grey backdrop, natural color. A fictional person who must not resemble any real celebrity or public figure.")
TAIL = "No text, no labels, no numbers, no logos, no watermark. 16:9 landscape."


def run(out: Path, prompt: str, refs: list[Path]) -> str:
    if out.exists():
        return "exists"
    pf = HERE / "prompts" / (out.stem + ".txt")
    pf.parent.mkdir(exist_ok=True)
    pf.write_text(prompt, encoding="utf-8")
    cmd = [sys.executable, str(ROOT / "tools/codex_image.py"), "--out", str(out), "--prompt-file", str(pf)]
    for r in refs:
        cmd += ["--ref", str(r)]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (HERE / "prompts" / (out.stem + ".log")).write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    return "ok" if out.exists() else "FAIL: " + (r.stderr.strip().splitlines() or ["?"])[-1][:300]


def turnaround(c):
    role = spec["roles"][c["role"]]
    prompt = "\n\n".join([PHOTO,
        f"The person: {c['person']}. Wearing: {role['wardrobe']}.",
        "Layout: four full-body views of the same person side by side, same scale, standing relaxed neutral pose, arms at sides: "
        "1 front view facing camera, 2 three-quarter view, 3 exact side profile view facing right, 4 back view. Even lighting, soft floor shadows.",
        TAIL])
    refs = [ROOT / c["ref"]] if c.get("ref") else []
    return c["id"], "turnaround", run(HERE / f"{c['id']}_turnaround.png", prompt, refs)


def expressions(c):
    role = spec["roles"][c["role"]]
    ta = HERE / f"{c['id']}_turnaround.png"
    if not ta.exists():
        return c["id"], "expressions", "skip: no turnaround"
    prompt = "\n\n".join([PHOTO,
        f"The person: {c['person']}. Must be exactly the same person as in the reference image (same face, hair, age, skin tone). Wearing: {role['wardrobe']}.",
        "Layout: a 3 by 2 grid of six head-and-shoulders portraits of this one person, same framing and lighting in every cell, each with a different natural, "
        f"believable expression (subtle acting, not exaggerated): {role['expressions']}. Thin even gaps between cells.",
        TAIL])
    return c["id"], "expressions", run(HERE / f"{c['id']}_expressions.png", prompt, [ta])


cands = [c for c in spec["candidates"] if not only or c["id"] in only]
with ThreadPoolExecutor(6) as ex:
    for res in ex.map(turnaround, cands):
        print(*res, flush=True)
with ThreadPoolExecutor(6) as ex:
    for res in ex.map(expressions, cands):
        print(*res, flush=True)
