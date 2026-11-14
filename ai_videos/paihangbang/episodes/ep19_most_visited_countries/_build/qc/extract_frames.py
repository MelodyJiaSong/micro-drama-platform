"""QC: extract frames from the master at given times (independent QC, 2026-11-04)."""
import subprocess, sys, pathlib
ep = pathlib.Path(__file__).resolve().parents[2]
mp4 = ep / "render" / "ep19_most_visited_countries_master.mp4"
out = ep / "_build" / "qc" / "frames"
out.mkdir(parents=True, exist_ok=True)
times = [float(t) for t in sys.argv[1:]]
for t in times:
    f = out / f"t{t:07.2f}.png"
    if f.exists():
        continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", str(f)], check=True)
    print(f.name)
