# -*- coding: utf-8 -*-
"""教学视频配音（本地 VoxCPM2，Apache-2.0，48 kHz）：按频道音色逐句克隆。由 `tools/edu_video.py tts` 调用：
    .cache/venvs/voxcpm/Scripts/python tools/edu_voxcpm.py <生成清单.json> [条目 id ...]

生成清单（放在产物目录，如 <知识点>/audio/lines/gen_v2.json）：
    voice  {reference（相对仓库根的 wav）, reference_text（参考音的原文）}
    items[] {id, text, seeds[], cfg?（2.0）, steps?（10）}
产物同目录 `{id}_s{seed}.wav` 与 `{id}_s{seed}.json`（参数、参考 sha256、wav sha256、时长）。参数没变且 wav 还在的跳过。
模型卡要求：不得冒充真人，AI 生成内容须标注——频道只用自设计音色，成片注明「AI 配音」。本地运行不收费、不走请求日志。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MODEL = REPO / ".cache" / "models" / "voxcpm2"
DEFAULTS = {"cfg": 2.0, "steps": 10}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def run(spec_path: Path, only: list[str]) -> None:
    os.environ["HF_HUB_OFFLINE"] = "1"
    import numpy as np
    import soundfile as sf
    import torch
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out = spec_path.parent
    ref = (REPO / spec["voice"]["reference"]).resolve()
    if not ref.is_file():
        raise SystemExit(f"参考音不存在：{spec['voice']['reference']}")
    ref_text, ref_sha = spec["voice"]["reference_text"], sha256(ref)[:12]
    model = None
    for it in (i for i in spec["items"] if not only or i["id"] in only):
        params = {k: it.get(k, v) for k, v in DEFAULTS.items()}
        for seed in it["seeds"]:
            wav, meta = out / f"{it['id']}_s{seed}.wav", out / f"{it['id']}_s{seed}.json"
            want = {"engine": "voxcpm2", "text": it["text"], "reference": spec["voice"]["reference"],
                    "reference_sha256_12": ref_sha, **params, "seed": seed}
            if wav.exists() and meta.exists():
                old = json.loads(meta.read_text(encoding="utf-8"))
                if {k: old.get(k) for k in want} == want and old.get("wav_sha256") == sha256(wav):
                    print("跳过（未变）", wav.name); continue
            if model is None:
                from voxcpm import VoxCPM
                print("装模型", MODEL.name, flush=True)
                model = VoxCPM.from_pretrained(str(MODEL), load_denoiser=False)
            random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
            y = model.generate(text=it["text"], prompt_wav_path=str(ref), prompt_text=ref_text,
                               reference_wav_path=str(ref), cfg_value=params["cfg"],
                               inference_timesteps=params["steps"])
            sr = model.tts_model.sample_rate
            sf.write(str(wav), y, sr, subtype="PCM_24")
            meta.write_text(json.dumps(want | {
                "id": it["id"], "weights": MODEL.name, "license": "Apache-2.0", "sample_rate": sr,
                "seconds": round(len(y) / sr, 3), "wav": wav.name, "wav_sha256": sha256(wav)},
                ensure_ascii=False, indent=1), encoding="utf-8")
            print("出了", wav.name, f"{len(y) / sr:.1f}s", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="教学视频配音（本地 VoxCPM2）")
    ap.add_argument("spec"); ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    run(Path(a.spec).resolve(), a.ids)


if __name__ == "__main__":
    sys.exit(main())
