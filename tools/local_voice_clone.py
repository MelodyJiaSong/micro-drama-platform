# -*- coding: utf-8 -*-
"""本地声音克隆配音（MOSS-TTS-Local-Transformer-v1.5：给参考录音，按它的音色念台词；48 kHz；Apache-2.0）。

只用本地模型，参考录音不出本机。第三方原版语音作参考须有用户书面决定并记在该卡 refs.md（如 dota_yingxiong `m4`，follow-up 044）；
没有这样的决定，参考只能是本剧自有声音。独立环境与 `tools/local_voice.py` 共用：
    .cache/venvs/moss-voice/Scripts/python tools/local_voice_clone.py <生成清单.json> [条目 id ...]
权重 .cache/models/moss-tts-local-v1.5/，编解码器 .cache/models/moss-audio-tokenizer-v2/；只读本地、不连 Hugging Face。

生成清单（放在产物要落的目录，如资产的 voice/clone_NN/gen_v1.json）：
    items[]  {id, text, reference[]（相对清单目录或仓库根的音频路径）, language?（默认 English）, seeds[],
              temperature?（1.7）, top_p?（0.8）, top_k?（25）, repetition_penalty?（1.0）, note?}
产物同目录 `{id}_s{seed}.wav`（48 kHz）与 `{id}_s{seed}.json`（参数、参考文件 sha256、wav sha256、时长、峰值）。参数都没变且 wav 还在的跳过。
本地运行不收费、不走请求日志。
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
MODEL = REPO / ".cache" / "models" / "moss-tts-local-v1.5"
CODEC = REPO / ".cache" / "models" / "moss-audio-tokenizer-v2"
DEFAULTS = {"temperature": 1.7, "top_p": 0.8, "top_k": 25, "repetition_penalty": 1.0}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def resolve(base: Path, rel: str) -> Path:
    for p in (base / rel, REPO / rel):
        if p.is_file():
            return p.resolve()
    raise SystemExit(f"参考录音不存在：{rel}")


def run(path: Path, only: list[str]) -> None:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")
    import soundfile as sf
    import torch
    from transformers import AutoModel, AutoProcessor
    torch.backends.cuda.enable_cudnn_sdp(False)          # 官方 README：cuDNN SDPA 后端有问题
    spec = json.loads(path.read_text(encoding="utf-8"))
    out_dir = path.parent
    processor = model = None
    for it in (i for i in spec["items"] if not only or i["id"] in only):
        params = {k: it.get(k, v) for k, v in DEFAULTS.items()}
        refs = [resolve(out_dir, r) for r in it["reference"]]
        ref_sha = [sha256(r)[:12] for r in refs]
        for seed in it["seeds"]:
            wav, meta = out_dir / ("%s_s%d.wav" % (it["id"], seed)), out_dir / ("%s_s%d.json" % (it["id"], seed))
            want = {"text": it["text"], "reference": it["reference"], "reference_sha256_12": ref_sha,
                    "language": it.get("language", "English"), **params, "seed": seed}
            if wav.exists() and meta.exists():
                old = json.loads(meta.read_text(encoding="utf-8"))
                if {k: old.get(k) for k in want} == want and old.get("wav_sha256") == sha256(wav):
                    print("跳过（未变）", wav.name); continue
            if model is None:
                print("装模型", MODEL.name, flush=True)
                processor = AutoProcessor.from_pretrained(str(MODEL), trust_remote_code=True, codec_path=str(CODEC))
                processor.audio_tokenizer = processor.audio_tokenizer.to("cuda")
                model = AutoModel.from_pretrained(str(MODEL), trust_remote_code=True, attn_implementation="sdpa",
                                                  torch_dtype=torch.bfloat16).to("cuda").eval()
            torch.manual_seed(seed)
            # 自己读参考再编码：模型代码的 torchaudio.load 要 torchcodec（Windows 上缺 FFmpeg 动态库）
            import torchaudio.functional as taf
            target_sr = int(processor.model_config.sampling_rate)
            wavs = []
            for r in refs:
                y, ysr = sf.read(str(r), dtype="float32", always_2d=True)
                w = torch.from_numpy(y.T.copy())
                wavs.append(taf.resample(w, ysr, target_sr) if ysr != target_sr else w)
            codes = processor.encode_audios_from_wav(wavs, target_sr, n_vq=int(processor.model_config.n_vq))
            msg = processor.build_user_message(text=it["text"], reference=list(codes), language=want["language"])
            batch = processor([[msg]], mode="generation")
            with torch.no_grad():
                out = model.generate(input_ids=batch["input_ids"].to("cuda"), attention_mask=batch["attention_mask"].to("cuda"),
                                     max_new_tokens=1024, do_sample=True, audio_temperature=params["temperature"],
                                     audio_top_p=params["top_p"], audio_top_k=params["top_k"],
                                     audio_repetition_penalty=params["repetition_penalty"])
            msgs = [m for m in processor.decode(out) if m is not None]
            if not msgs:
                print("没出声音", wav.name); continue
            audio = msgs[0].audio_codes_list[0].float().cpu()          # [声道, 采样]
            sr = processor.model_config.sampling_rate
            x = audio.T if audio.dim() == 2 else audio.reshape(-1, 1)
            sf.write(str(wav), x.numpy(), sr, subtype="PCM_24")
            peak = float(audio.abs().max())
            meta.write_text(json.dumps(want | {
                "id": it["id"], "weights": MODEL.name, "codec": CODEC.name, "license": "Apache-2.0", "sample_rate": sr,
                "seconds": round(x.shape[0] / sr, 3), "wav": wav.name, "wav_sha256": sha256(wav),
                "peak_db": round(20 * math.log10(max(peak, 1e-9)), 1), "note": it.get("note")},
                ensure_ascii=False, indent=1), encoding="utf-8")
            print("出了", wav.name, "%.1fs" % (x.shape[0] / sr), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="本地声音克隆配音（MOSS-TTS-Local-Transformer-v1.5）")
    ap.add_argument("spec"); ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    run(Path(a.spec).resolve(), a.ids)


if __name__ == "__main__":
    sys.exit(main())
