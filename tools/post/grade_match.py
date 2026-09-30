# -*- coding: utf-8 -*-
"""全集分组调色：同一场景的各镜向组内参考镜的色彩统计量靠拢，出片前把同场景各镜的色调拉齐。

    python tools/post/grade_match.py <剧> <ep> [--shots 1-7] [--ref shot02 ...] [--strength 0.7] [--samples 24]

- 场景键：shot md「参考:」行里第一个 bg 主体（`bg175_武器大厅`、路由键 `bg1-2_谷口_…` 都归到主体 bg{N}）；取不到就单独成组。
- 每组参考镜默认组内第一镜，`--ref shotNN` 覆盖它所在的组（可给多次）；参考镜与单镜组不调色、直接用原片。
- 色彩数学复用 tools/seam_color.py：抽样帧 Lab 均值 / 标准差（`_lab_stats`）＋ Reinhard 迁移（`_transfer`，强度即 s），
  烘成 33³ `.cube`，ffmpeg `lut3d`（16 位中转）出 `shotNN_graded.mp4`（CRF 16，音轨原样拷贝）。对比度倍数限在 1/MAX_GAIN–MAX_GAIN。
- 产物在 `{ep}/post/grade/`；grade.json 记每镜用哪条、离参考镜的 Lab 距离（调前 / 调后，调后从成片回读）。
- 逐镜落盘：源、参考、强度都没变的镜跳过。需要 opencv + numpy（默认后期解释器 index-tts/.venv 里有）。
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import post_common as pc

try:
    import numpy as np
    import seam_color
except ImportError as e:
    raise SystemExit(f"grade_match 需要 opencv-python 与 numpy（{e}）：换装了它们的解释器跑，如\n"
                     f"  \"{pc.POST_PYTHON}\" tools/post/grade_match.py …") from e

LUT = 33
MAX_GAIN = 2.0
CRF = "16"
# 8 位 RGB 中转 + 默认截断取整会让整条片子暗约 1.5 L（单位 LUT 实测）；16 位中转 + 精确取整把往返误差压到 ~0.2
SWS = "accurate_rnd+full_chroma_int+full_chroma_inp"


def lab_stats(src: Path, samples: int, cache: Path) -> tuple[np.ndarray, np.ndarray]:
    """整镜均匀抽 `samples` 帧的 Lab 统计量（按源文件缓存）。"""
    sig = pc.signature([src], samples=samples)
    if pc.fresh(cache, sig):
        j = json.loads(cache.read_text(encoding="utf-8"))
        return np.array(j["mean"]), np.array(j["std"])
    dur = pc.probe(src).v_dur
    with tempfile.TemporaryDirectory() as td:
        pc.run([pc.FFMPEG, "-y", "-i", src, "-vf", f"fps={samples / dur:.6f},scale=360:-2", "-frames:v", str(samples),
                "-q:v", "2", Path(td) / "f_%03d.png"])
        st = seam_color._lab_stats(sorted(Path(td).glob("f_*.png")))
    if st is None:
        raise SystemExit(f"{src.name}：抽不出帧")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"mean": st[0].tolist(), "std": st[1].tolist()}), encoding="utf-8")
    pc.stamp(cache, sig)
    return st


def cube_text(mu_b: np.ndarray, sd_b: np.ndarray, mu_a: np.ndarray, sd_a: np.ndarray, s: float, title: str) -> str:
    """把「本镜 → 参考镜」的 Reinhard 迁移烘成 33³ 3D LUT（.cube：R 变化最快，其次 G，最后 B）。"""
    sd_a = np.clip(sd_a, sd_b / MAX_GAIN, sd_b * MAX_GAIN)
    lv = np.round(np.arange(LUT) * 255 / (LUT - 1)).astype(np.uint8)
    b, g, r = np.meshgrid(lv, lv, lv, indexing="ij")
    grid = np.stack([b, g, r], axis=-1).reshape(-1, 1, 3)
    rgb = seam_color._transfer(grid, mu_b, sd_b, mu_a, sd_a, s).reshape(-1, 3)[:, ::-1] / 255.0
    rows = "\n".join(f"{x:.6f} {y:.6f} {z:.6f}" for x, y, z in rgb)
    return f'TITLE "{title}"\nLUT_3D_SIZE {LUT}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n{rows}\n'


def groups_of(dirs: list[Path], refs: list[str]) -> dict[str, list[Path]]:
    """场景键 → 组内各镜（参考镜排第一）。"""
    groups: dict[str, list[Path]] = {}
    for d in dirs:
        k = pc.scene_key(pc.shot_md(d))
        groups.setdefault(k[0] if k else f"solo:{d.name}", []).append(d)
    chosen: dict[str, str] = {}
    for ref in refs:
        name = "shot%02d" % min(pc.parse_shots(ref))
        key = next((k for k, v in groups.items() if any(d.name == name for d in v)), None)
        if key is None:
            raise SystemExit(f"--ref {ref}：不在这次调色的镜里")
        if key in chosen:
            raise SystemExit(f"--ref：{key} 组给了两个参考镜（{chosen[key]}、{name}）")
        chosen[key] = name
        groups[key].sort(key=lambda d: d.name != name)
    return groups


def dist(a: np.ndarray, b: np.ndarray) -> float:
    return round(float(np.linalg.norm(a - b)), 2)


def grade_episode(epd: Path, dirs: list[Path], refs: list[str], strength: float, samples: int) -> dict[str, Path]:
    out_dir = epd / pc.POST_DIR / "grade"
    stats_dir = out_dir / "stats"
    out_dir.mkdir(parents=True, exist_ok=True)
    groups = groups_of(dirs, refs)
    report: dict = {"strength": strength, "groups": {}, "shots": {}}
    use: dict[str, Path] = {}
    for key, members in groups.items():
        ref = members[0]
        mu_a, sd_a = lab_stats(pc.shot_mp4(ref), samples, stats_dir / f"{ref.name}.json")
        report["groups"][key] = {"ref": ref.name, "shots": [d.name for d in members],
                                 "scene": (pc.scene_key(pc.shot_md(ref)) or ("", ""))[1]}
        use[ref.name] = pc.shot_mp4(ref)
        report["shots"][ref.name] = {"group": key, "ref": ref.name, "file": pc.shot_mp4(ref).as_posix()}
        for d in members[1:]:
            src = pc.shot_mp4(d)
            mu_b, sd_b = lab_stats(src, samples, stats_dir / f"{d.name}.json")
            cube = out_dir / f"{d.name}.cube"
            text = cube_text(mu_b, sd_b, mu_a, sd_a, strength, f"{d.name} -> {ref.name} s={strength}")
            if not cube.is_file() or cube.read_text(encoding="utf-8") != text:
                cube.write_text(text, encoding="utf-8")
            graded = out_dir / f"{d.name}_graded.mp4"
            vf = f"format=gbrp16le,lut3d=file={cube.name}:interp=tetrahedral,format=yuv420p"
            sig = pc.signature([src], cube=pc.sha256(cube), vf=vf, sws=SWS, crf=CRF)
            done = pc.fresh(graded, sig)
            if done:
                after = done["dist_after"]
                print(f"  {d.name} → {ref.name}：已是最新，跳过")
            else:
                part = out_dir / f"{d.name}_graded.part.mp4"
                pc.run([pc.FFMPEG, "-y", "-sws_flags", SWS, "-i", src.resolve(),
                        "-vf", vf,
                        "-map", "0:v:0", "-map", "0:a?", "-c:v", "libx264", "-crf", CRF, "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", part.name], cwd=out_dir)
                part.replace(graded)
                with tempfile.TemporaryDirectory() as td:
                    after = dist(lab_stats(graded, samples, Path(td) / "g.json")[0], mu_a)
                pc.stamp(graded, sig, dist_after=after)
                print(f"  {d.name} → {ref.name}：Lab 距离 {dist(mu_b, mu_a)} → {after}")
            use[d.name] = graded
            report["shots"][d.name] = {"group": key, "ref": ref.name, "file": graded.as_posix(),
                                       "dist_before": dist(mu_b, mu_a), "dist_after": after}
    (out_dir / "grade.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    worse = [k for k, v in report["shots"].items() if "dist_after" in v and v["dist_after"] > v["dist_before"]]
    if worse:
        raise SystemExit(f"调色后反而离参考镜更远（从成片回读）：{worse}——查 LUT 与色彩矩阵，别拿这版拼片")
    n_multi = sum(len(v) > 1 for v in groups.values())
    print(f"调色：{len(dirs)} 镜，{len(groups)} 组（{n_multi} 组有多镜），调了 {len(dirs) - len(groups)} 镜 → {out_dir}")
    return use


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="全集分组调色（Reinhard → 3D LUT）")
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--shots", default=None, help="如 1-7,9；默认从第一镜起连续有出片的镜")
    ap.add_argument("--ref", action="append", default=[], help="shotNN：它所在组的参考镜（可多次）")
    ap.add_argument("--strength", type=float, default=0.7)
    ap.add_argument("--samples", type=int, default=24, help="每镜抽几帧算统计量")
    a = ap.parse_args()
    if not 0.0 <= a.strength <= 1.0:
        raise SystemExit("--strength 要在 0–1")
    epd = pc.ep_dir(pc.drama_root(a.drama), a.ep)
    grade_episode(epd, pc.cut_shots(epd, a.shots), a.ref, a.strength, a.samples)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
