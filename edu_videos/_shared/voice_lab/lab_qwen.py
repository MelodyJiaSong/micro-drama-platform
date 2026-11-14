# -*- coding: utf-8 -*-
"""Qwen3-TTS（Apache-2.0）选型实验：VoiceDesign 设计音色 → Base 克隆，同一音色念中英文测试稿。

    .cache/venvs/qwen3-tts/Scripts/python edu_videos/_shared/voice_lab/lab_qwen.py
产物：voice_lab/qwen/{音色}_ref.wav、{音色}_{zh|en}.wav（本地运行，不收费、不走请求日志）。
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"
import soundfile as sf  # noqa: E402
import torch  # noqa: E402
from qwen_tts import Qwen3TTSModel  # noqa: E402

LAB = Path(__file__).resolve().parent
MODELS = LAB.parents[2] / ".cache" / "models"
OUT = LAB / "qwen"
LANG = {"zh": "Chinese", "en": "English"}


def load(name: str) -> Qwen3TTSModel:
    return Qwen3TTSModel.from_pretrained(str(MODELS / name), device_map="cuda:0", dtype=torch.bfloat16,
                                         attn_implementation="sdpa")


def main() -> None:
    cfg = json.loads((LAB / "texts.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    torch.manual_seed(7)
    design = load("qwen3-tts-voicedesign")
    refs = {}
    for v, brief in cfg["voices"].items():
        t = time.time()
        wavs, sr = design.generate_voice_design(text=cfg["ref_zh"], language="Chinese", instruct=brief["zh"])
        sf.write(str(OUT / f"{v}_ref.wav"), wavs[0], sr)
        refs[v] = (wavs[0], sr)
        print(f"设计 {v}：{len(wavs[0]) / sr:.1f}s，用时 {time.time() - t:.0f}s", flush=True)
    del design
    torch.cuda.empty_cache()
    clone = load("qwen3-tts-base")
    for v, ref in refs.items():
        prompt = clone.create_voice_clone_prompt(ref_audio=ref, ref_text=cfg["ref_zh"], x_vector_only_mode=False)
        for lang, text in cfg["test"].items():
            t = time.time()
            wavs, sr = clone.generate_voice_clone(text=text, language=LANG[lang], voice_clone_prompt=prompt)
            sf.write(str(OUT / f"{v}_{lang}.wav"), wavs[0], sr)
            print(f"克隆 {v}_{lang}：{len(wavs[0]) / sr:.1f}s，用时 {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
