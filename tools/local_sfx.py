# -*- coding: utf-8 -*-
"""本地音效生成（MOSS-SoundEffect-v2.0：音效、生物叫声、环境声，48 kHz 单声道，每条最长 30 秒；Apache-2.0）。

只用完全开源的本地模型（paid_services.md 商业用途一节）。独立环境跑（Python 3.12，torch 2.9.0+cu128）：
    .cache/venvs/moss-soundeffect/Scripts/python tools/local_sfx.py <生成清单.json> [条目 id ...]
代码检出 .cache/src/MOSS-TTS（moss_soundeffect_v2 以 -e 装进环境），权重 .cache/models/moss-soundeffect-v2/，只读本地、不连 Hugging Face。

生成清单（放在产物要落的目录，如资产的 voice/sfx_NN/gen_v1.json、集的 post/audio/gen_vN.json）：
    items[]  {id, prompt, negative?, duration（秒，≤30）, seeds[], steps?（默认 100）, cfg?（默认 4.0）, shift?（默认 5.0）, note?}
产物同目录 `{id}_s{seed}.wav`（48 kHz 单声道）与 `{id}_s{seed}.json`（模型、prompt、种子、wav sha256、逐秒响度）。
prompt / 种子 / 参数都没变且 wav 还在的跳过。本地运行不收费、不走请求日志。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MODEL = REPO / ".cache" / "models" / "moss-soundeffect-v2"
KEYS = ("prompt", "negative", "duration", "steps", "cfg", "shift")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def levels(audio, sr: int) -> dict:
    """峰值与逐秒 RMS（dBFS），用来挑掉静音、削波或忽大忽小的结果。"""
    import torch
    x = audio.float()
    sec = [float(torch.sqrt((x[:, i:i + sr] ** 2).mean() + 1e-12)) for i in range(0, x.shape[1], sr)]
    db = lambda v: round(20 * math.log10(max(v, 1e-9)), 1)
    return {"peak_db": db(float(x.abs().max())), "rms_db_per_s": [db(v) for v in sec]}


def run(path: Path, only: list[str]) -> None:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")   # Windows 没有 Triton，关掉 torch.compile
    import soundfile as sf
    import torch
    spec = json.loads(path.read_text(encoding="utf-8"))
    out_dir = path.parent
    pipe = None
    for it in (i for i in spec["items"] if not only or i["id"] in only):
        for seed in it["seeds"]:
            wav, meta = out_dir / ("%s_s%d.wav" % (it["id"], seed)), out_dir / ("%s_s%d.json" % (it["id"], seed))
            want = {k: it.get(k) for k in KEYS} | {"seed": seed}
            if wav.exists() and meta.exists():
                old = json.loads(meta.read_text(encoding="utf-8"))
                if {k: old.get(k) for k in want} == want and old.get("wav_sha256") == sha256(wav):
                    print("跳过（未变）", wav.name); continue
            if pipe is None:
                from moss_soundeffect_v2 import MossSoundEffectPipeline
                print("装模型", MODEL.name)
                pipe = MossSoundEffectPipeline.from_pretrained(str(MODEL), torch_dtype=torch.bfloat16, device="cuda")
            audio = pipe(prompt=it["prompt"], negative_prompt=it.get("negative") or "", seconds=it["duration"],
                         num_inference_steps=it.get("steps", 100), cfg_scale=it.get("cfg", 4.0),
                         sigma_shift=it.get("shift", 5.0), seed=seed)[0].float().cpu()
            sr = pipe.sample_rate
            sf.write(str(wav), audio.numpy().T, sr, subtype="PCM_24")   # torchaudio 2.9 存盘要 FFmpeg 动态库，改用 soundfile
            meta.write_text(json.dumps(want | {
                "id": it["id"], "weights": MODEL.name, "license": "Apache-2.0",
                "sample_rate": sr, "seconds": round(audio.shape[1] / sr, 3), "wav": wav.name, "wav_sha256": sha256(wav),
                **levels(audio, sr), "note": it.get("note")}, ensure_ascii=False, indent=1), encoding="utf-8")
            print("出了", wav.name, "%.1fs" % (audio.shape[1] / sr), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="本地音效生成（MOSS-SoundEffect-v2.0）")
    ap.add_argument("spec"); ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    run(Path(a.spec).resolve(), a.ids)


if __name__ == "__main__":
    sys.exit(main())
