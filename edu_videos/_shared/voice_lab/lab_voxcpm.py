# -*- coding: utf-8 -*-
"""VoxCPM2（Apache-2.0；模型卡禁止冒充、欺诈、虚假信息，AI 生成内容须标注）选型实验：
括号描述设计音色 → 以设计出的参考音克隆，同一音色念中英文测试稿。

    .cache/venvs/voxcpm/Scripts/python edu_videos/_shared/voice_lab/lab_voxcpm.py
产物：voice_lab/voxcpm/{音色}_ref.wav、{音色}_{zh|en}.wav（本地运行，不收费、不走请求日志）。
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"
import soundfile as sf  # noqa: E402
import torch  # noqa: E402
from voxcpm import VoxCPM  # noqa: E402

LAB = Path(__file__).resolve().parent
MODEL = LAB.parents[2] / ".cache" / "models" / "voxcpm2"
OUT = LAB / "voxcpm"


def main() -> None:
    cfg = json.loads((LAB / "texts.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    torch.manual_seed(7)
    model = VoxCPM.from_pretrained(str(MODEL), load_denoiser=False)
    sr = model.tts_model.sample_rate
    for v, brief in cfg["voices"].items():
        t = time.time()
        ref = OUT / f"{v}_ref.wav"
        wav = model.generate(text=f"({brief['zh']}){cfg['ref_zh']}", cfg_value=2.0, inference_timesteps=10)
        sf.write(str(ref), wav, sr)
        print(f"设计 {v}：{len(wav) / sr:.1f}s，用时 {time.time() - t:.0f}s", flush=True)
        for lang, text in cfg["test"].items():
            t = time.time()
            wav = model.generate(text=text, prompt_wav_path=str(ref), prompt_text=cfg["ref_zh"],
                                 reference_wav_path=str(ref), cfg_value=2.0, inference_timesteps=10)
            sf.write(str(OUT / f"{v}_{lang}.wav"), wav, sr)
            print(f"克隆 {v}_{lang}：{len(wav) / sr:.1f}s，用时 {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
