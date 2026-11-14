# follow-up 016/024：Codex 只做生成。python -I gen_run.py <worker> <nworkers> → 依次跑 gen_prompts/*.txt（已有输出跳过）
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).parent; EP = HERE.parent; REPO = HERE.parents[4]
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
w, n = int(sys.argv[1]), int(sys.argv[2])
extra = sys.argv[3:]
todo = sorted(HERE.glob("gen_prompts/*.txt"))
for k, pf in enumerate(todo):
    if k % n != w:
        continue
    i = int(pf.stem[:2]); suffix = pf.stem[2:]            # 02.txt 或 02b.txt（重出）
    stem = Path(d["items"][i]["image"]).stem
    out = EP / "assets" / "img" / f"{stem}_gen{suffix}.png"
    if out.exists():
        print("skip", out.name, flush=True); continue
    r = subprocess.run([sys.executable, str(REPO / "tools" / "codex_image.py"), "--out", str(out), "--prompt-file", str(pf), "--timeout", "600"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(REPO))
    print(i, out.name, "rc", r.returncode, (r.stdout + r.stderr)[-300:].replace("\n", " "), flush=True)
