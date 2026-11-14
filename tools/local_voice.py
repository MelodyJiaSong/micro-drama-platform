# -*- coding: utf-8 -*-
"""本地声音设计配音（MOSS-VoiceGenerator：按文字描述设计音色并念台词，不用参考音频；中英文；Apache-2.0）。

只用完全开源的本地模型（paid_services.md 商业用途一节）。独立环境（Python 3.12，torch 2.9.0+cu128，transformers 5.0.0——
模型自带代码要 5.x，MOSS-SoundEffect 的环境是 4.57，不共用）：
    .cache/venvs/moss-voice/Scripts/python tools/local_voice.py <生成清单.json> [条目 id ...]
权重 .cache/models/moss-voicegenerator/（含模型自带的 remote code），音频编解码器 .cache/models/moss-audio-tokenizer/；只读本地、不连 Hugging Face。

生成清单（放在产物要落的目录，如资产的 voice/vg_NN/gen_v1.json）：
    items[]  {id, text, instruction, seeds[], temperature?（默认 1.5）, top_p?（0.6）, top_k?（50）, repetition_penalty?（1.1）, note?}
产物同目录 `{id}_s{seed}.wav` 与 `{id}_s{seed}.json`（模型、文本、描述、种子、wav sha256、时长、峰值）。
参数都没变且 wav 还在的跳过。本地运行不收费、不走请求日志。原版第三方语音不能作输入（本工具也不收参考音频）。
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
MODEL = REPO / ".cache" / "models" / "moss-voicegenerator"
CODEC = REPO / ".cache" / "models" / "moss-audio-tokenizer"
DEFAULTS = {"temperature": 1.5, "top_p": 0.6, "top_k": 50, "repetition_penalty": 1.1}
KEYS = ("text", "instruction", *DEFAULTS)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def run(path: Path, only: list[str]) -> None:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")
    import soundfile as sf
    import torch
    from transformers import AutoModel, AutoProcessor
    torch.backends.cuda.enable_cudnn_sdp(False)          # 官方模型卡：cuDNN SDPA 后端有问题
    spec = json.loads(path.read_text(encoding="utf-8"))
    out_dir = path.parent
    processor = model = None
    for it in (i for i in spec["items"] if not only or i["id"] in only):
        params = {k: it.get(k, v) for k, v in DEFAULTS.items()}
        for seed in it["seeds"]:
            wav, meta = out_dir / ("%s_s%d.wav" % (it["id"], seed)), out_dir / ("%s_s%d.json" % (it["id"], seed))
            want = {"text": it["text"], "instruction": it["instruction"], **params, "seed": seed}
            if wav.exists() and meta.exists():
                old = json.loads(meta.read_text(encoding="utf-8"))
                if {k: old.get(k) for k in want} == want and old.get("wav_sha256") == sha256(wav):
                    print("跳过（未变）", wav.name); continue
            if model is None:
                print("装模型", MODEL.name, flush=True)
                processor = AutoProcessor.from_pretrained(str(MODEL), trust_remote_code=True, normalize_inputs=True,
                                                          codec_path=str(CODEC))
                processor.audio_tokenizer = processor.audio_tokenizer.to("cuda")
                model = AutoModel.from_pretrained(str(MODEL), trust_remote_code=True, attn_implementation="sdpa",
                                                  torch_dtype=torch.bfloat16).to("cuda").eval()
            torch.manual_seed(seed)
            batch = processor([[processor.build_user_message(text=it["text"], instruction=it["instruction"])]],
                              mode="generation")
            with torch.no_grad():
                out = model.generate(input_ids=batch["input_ids"].to("cuda"), attention_mask=batch["attention_mask"].to("cuda"),
                                     audio_temperature=params["temperature"], audio_top_p=params["top_p"],
                                     audio_top_k=params["top_k"], audio_repetition_penalty=params["repetition_penalty"])
            audio = next(iter(processor.decode(out))).audio_codes_list[0].float().cpu()
            sr = processor.model_config.sampling_rate
            x = audio.reshape(-1) if audio.dim() == 1 or audio.shape[0] == 1 else audio.T
            sf.write(str(wav), x.numpy(), sr, subtype="PCM_24")
            peak = float(audio.abs().max())
            meta.write_text(json.dumps(want | {
                "id": it["id"], "weights": MODEL.name, "codec": CODEC.name, "license": "Apache-2.0", "sample_rate": sr,
                "seconds": round(x.shape[0] / sr, 3), "wav": wav.name, "wav_sha256": sha256(wav),
                "peak_db": round(20 * math.log10(max(peak, 1e-9)), 1), "note": it.get("note")},
                ensure_ascii=False, indent=1), encoding="utf-8")
            print("出了", wav.name, "%.1fs" % (x.shape[0] / sr), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="本地声音设计配音（MOSS-VoiceGenerator）")
    ap.add_argument("spec"); ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    run(Path(a.spec).resolve(), a.ids)


if __name__ == "__main__":
    sys.exit(main())
