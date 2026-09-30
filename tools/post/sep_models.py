# -*- coding: utf-8 -*-
"""分离模型（P2 试验，tools/post/stems_trial.py 调）：一条音轨 wav → 分轨 wav，逐单元落盘，源与参数没变就跳过。在 pc.ALIGN_PYTHON（.venv-post）里跑。
输入不限于原片：stems_trial 也拿一个模型的输出轨喂给另一个（级联），两个函数对输入一视同仁。

· roformer：python-audio-separator 的 BS-RoFormer（viperx ep368），vocals / instrumental 两轨（instrumental＝原片减 vocals，相加即原片）。
· bandit：Bandit v2（Watcharasupat、Wu、Orife 2024，DnR v3 英语权重），speech / music / sfx 三轨。audio-separator 0.47.0 的模型表里
  没有影视三分轨（对白 / 音乐 / 音效），所以直接用作者仓库的模型类（BANDIT_SRC，钉 BANDIT_COMMIT）。模型是单声道：左右声道各当一条过；
  48 kHz 训练：进出各用 soxr VHQ 重采样一次，落盘回源片采样率、与源片等长。
权重在 MODEL_DIR（与 audio-separator 同一规则：AUDIO_SEPARATOR_MODEL_DIR，没设就 /tmp/audio-separator-models），本机缓存、不进 git；
缺了报出下载命令，本工具不替你下（同 stems.py 对 demucs 的做法）。
*(judgment call — 切块照作者 configs/inference/chunked-tensor.yaml 的 8 s 块、1 s 跳、Hann 窗；叠加按实际窗和归一、前后各反射垫一个重叠长，
  不照抄作者前后各垫 2 倍重叠的写法：22–28 s 的短片上它退成常数垫，结果等价、代码短一半。batch 从 10 降到 8 省显存，结果不变。)*
"""
from __future__ import annotations

import hashlib
import logging
import math
import os
import sys
import time
import types
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr
import torch
from torch import nn
from torch.nn import functional as F

import post_common as pc

MODEL_DIR = Path(os.environ.get("AUDIO_SEPARATOR_MODEL_DIR", "/tmp/audio-separator-models")).resolve()

ROFORMER = "bs_roformer_ep368"
ROFORMER_FILE = "model_bs_roformer_ep_368_sdr_12.9628.ckpt"
ROFORMER_STEMS = ("vocals", "instrumental")

BANDIT = "bandit_v2_eng"
BANDIT_SRC = pc.REPO / ".venv-post" / "src" / "bandit-v2"
BANDIT_REPO = "https://github.com/kwatcharasupat/bandit-v2.git"
BANDIT_COMMIT = "d5563d9031e95fdaa3e5a73d5020b9a0df61adb6"
BANDIT_CKPT = MODEL_DIR / "bandit_v2" / "checkpoint-eng.ckpt"
BANDIT_URL = "https://zenodo.org/records/12701995/files/checkpoint-eng.ckpt?download=1"
BANDIT_MD5 = "9b74787e7f752709ce986ba1b1ac29a9"
BANDIT_STEMS = ("speech", "music", "sfx")
BANDIT_FS = 48000
BANDIT_KW = {  # 作者 configs/models/bandit-mus64.yaml 原样
    "in_channels": 1, "band_type": "musical", "n_bands": 64, "normalize_channel_independently": False,
    "treat_channel_as_feature": True, "n_sqm_modules": 8, "emb_dim": 128, "rnn_dim": 256, "bidirectional": True,
    "rnn_type": "GRU", "mlp_dim": 512, "hidden_activation": "Tanh", "hidden_activation_kwargs": None, "complex_mask": True,
    "use_freq_weights": True, "n_fft": 2048, "win_length": 2048, "hop_length": 512, "window_fn": "hann_window",
    "wkwargs": None, "power": None, "center": True, "normalized": True, "pad_mode": "reflect", "onesided": True,
}
CHUNK_S, HOP_S, BATCH = 8.0, 1.0, 8

CARDS = {        # 写进 metrics.json 的模型卡：文件名、出处、许可
    ROFORMER: {
        "file": ROFORMER_FILE,
        "listed_as": "Roformer Model: BS-Roformer-Viperx-1296（audio-separator 0.47.0 --list_models）",
        "stems": list(ROFORMER_STEMS),
        "source": "github.com/TRvlvr/model_repo 的 release all_public_uvr_models（audio-separator 首次用时自动下，连同 model_bs_roformer_ep_368_sdr_12.9628.yaml）",
        "bytes": 639317465,
        "licence": "权重未声明许可（TRvlvr/model_repo 无 LICENSE，训练者 viperx 未给条款）；audio-separator 代码 MIT。本剧是爱好者不变现（concept E6），自用可以，商用前要重新确认",
        "published_scores": "audio-separator models-scores.json 中位数：vocals SDR 12.10 / SIR 28.16 / SAR 12.98；instrumental SDR 16.31",
        "why": "RoFormer 两轨模型里 vocals SIR（其余声源串进人声的程度，越高越干净）最高：28.16，比默认的 ep317 高 0.8 dB、比 vocals SDR 第一的 Kim MelBand（12.60 / SIR 25.58）高 2.6 dB；去音乐要紧的是对白里不带配乐，所以按 SIR 挑"
               "（SIR 更高的两个是 Karaoke 模型——分主唱与和声，不是分人声与伴奏，不算）",
        "observed": "人声（含吼叫、尖叫、狗头人叫）都归 vocals，这是 Bandit 做不到的；但 shot06 19–22 s 的乌鸦叫和一段配乐也被当成 vocals，"
                    "shot03 开头 7 s 的脚步、碎响也有一部分进 vocals",
    },
    BANDIT: {
        "file": BANDIT_CKPT.name,
        "listed_as": "不在 audio-separator 表里（0.47.0 共 169 个模型，没有一个出对白 / 音乐 / 音效三轨）",
        "stems": list(BANDIT_STEMS),
        "source": f"Zenodo doi:10.5281/zenodo.12701995（Bandit v2，Watcharasupat、Wu、Orife 2024《Remastering Divide and Remaster》，DnR v3 英语子集训练，48 kHz）；md5 {BANDIT_MD5}；代码 github.com/kwatcharasupat/bandit-v2 @ {BANDIT_COMMIT[:7]}",
        "bytes": 446680129,
        "licence": "权重 CC BY-SA 4.0（Zenodo 记录）；代码 Apache-2.0。可商用，署名 + 相同方式共享",
        "published_scores": "论文报 DnR v3 测试集上 speech / music / sfx 的 SNR，未在本机复核",
        "why": "影视三分轨（对白 / 音乐 / 音效）现成权重里最新的一代、许可最宽；同类的 BandIt Plus（DnR v2，MSST release v.1.0.3 的 model_bandit_plus_dnr_sdr_11.47.chpt ＝ Zenodo 10160698 的 dnr-3s-mus64-l1snr-plus.ckpt）是 CC BY-NC 4.0、训练数据旧一代，没跑。"
               "本剧对白是英语（align.py 用 medium.en），所以取 eng 权重",
        "tested_alternatives": "同一 Zenodo 记录的 checkpoint-multi.ckpt（多语种，md5 fea2868787551b0cff36cfcf7c3622a3）在 shot03 / 05 / 06 上试过："
                               "三轨逐秒电平与 eng 相差 < 1 dB（音效轨略多），同样把吼叫、狗头人叽喳、乌鸦叫分进音乐轨、同样丢 shot05 第二声「Ugh!」——没换；"
                               "记录里还有 cmn / deu / fra / spa / fao 单语种权重，对白是英语，没试",
        "observed": "DnR 的对白轨只含朗读式说话：吼叫、尖叫、喘、怪物叫声不算对白，实测多数被分进音乐轨（shot05 7–15 s 的吼与打斗声、shot06 0–21 s 的狗头人叽喳与尖叫）。"
                    "所以「只用 Bandit 去音乐」会把打戏里的人声一起去掉，要配 RoFormer 级联（stems_trial.RECIPES）",
    },
}


@dataclass(frozen=True)
class Run:
    model: str                  # 目录名：stems_test/{shot}/{model}/
    stems: dict[str, Path]      # 轨名 → wav（float32、源片采样率、与源片等长）
    load_s: float               # 载模型（含权重读盘）秒数
    sep_s: float                # 分离本身秒数（含重采样与写盘）
    device: str
    reused: bool                # True＝这次没算、沿用上次落盘的（秒数是上次的）


def device_name() -> str:
    return f"cuda:0 {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "cpu"


def _reuse(model: str, stems: dict[str, Path], sig: dict) -> Run | None:
    first = next(iter(stems.values()))
    st = pc.fresh(first, sig)
    if st is None or not all(p.is_file() for p in stems.values()):
        return None
    return Run(model, stems, float(st["load_s"]), float(st["sep_s"]), str(st["device"]), True)


def write_wav(path: Path, x: np.ndarray, sr: int) -> None:
    """x：(n, ch) float32 → path（先写 .part 再换名）。"""
    part = path.with_name(path.stem + ".part.wav")
    sf.write(part, x, sr, subtype="FLOAT")
    part.replace(path)


# ─────────────────────────── BS-RoFormer（audio-separator）───────────────────────────

def roformer(src: Path, out: Path) -> Run:
    stems = {s: out / f"{s}.wav" for s in ROFORMER_STEMS}
    sr = sf.info(src).samplerate
    sig = pc.signature([src], model=ROFORMER_FILE, sr=sr)
    if (hit := _reuse(ROFORMER, stems, sig)) is not None:
        return hit
    from audio_separator.separator import Separator     # 只在要算时导入：慢，且会配置 logging
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    # normalization_threshold=1.0：只在峰值超满刻度时才缩（默认 0.9 会把各轨各自缩放，轨相加就不等于原片了）
    sep = Separator(log_level=logging.WARNING, model_file_dir=str(MODEL_DIR), output_dir=str(out), output_format="WAV",
                    use_soundfile=True, normalization_threshold=1.0, sample_rate=sr)
    sep.load_model(ROFORMER_FILE)
    t1 = time.perf_counter()
    got = sep.separate(str(src), custom_output_names={"vocals": "vocals", "instrumental": "instrumental", "other": "instrumental"})
    t2 = time.perf_counter()
    missing = [p.name for p in stems.values() if not p.is_file()]
    if missing:
        raise SystemExit(f"audio-separator 没写出 {missing}（它写了 {got}）")
    dev = device_name() if str(sep.torch_device).startswith("cuda") else str(sep.torch_device)
    del sep
    torch.cuda.empty_cache()
    pc.stamp(stems["vocals"], sig, load_s=round(t1 - t0, 2), sep_s=round(t2 - t1, 2), device=dev)
    return Run(ROFORMER, stems, round(t1 - t0, 2), round(t2 - t1, 2), dev, False)


# ─────────────────────────── Bandit v2（作者模型类）───────────────────────────

def md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def check_bandit() -> None:
    """代码与权重都在、权重 md5 对得上 Zenodo 登记的；缺了报出取回命令。"""
    why = []
    if not (BANDIT_SRC / "src" / "models" / "bandit" / "bandit.py").is_file():
        why.append(f"缺作者代码：git clone {BANDIT_REPO} \"{BANDIT_SRC}\" && git -C \"{BANDIT_SRC}\" checkout {BANDIT_COMMIT}")
    if not BANDIT_CKPT.is_file():
        why.append(f"缺权重：curl -L -C - -o \"{BANDIT_CKPT}\" \"{BANDIT_URL}\"（446,680,129 字节）")
    elif md5(BANDIT_CKPT) != BANDIT_MD5:
        why.append(f"{BANDIT_CKPT} md5 ≠ {BANDIT_MD5}（没下完或坏了）：删掉重下")
    if why:
        raise SystemExit("Bandit v2 不齐，本工具不替你下：\n  " + "\n  ".join(why))


def load_bandit(dev: torch.device) -> nn.Module:
    if "pytorch_lightning" not in sys.modules:      # 作者的基类是 LightningModule，推理只用到 nn.Module 那一层
        stub = types.ModuleType("pytorch_lightning")
        stub.LightningModule = nn.Module
        sys.modules["pytorch_lightning"] = stub
    if str(BANDIT_SRC) not in sys.path:
        sys.path.insert(0, str(BANDIT_SRC))
    from src.models.bandit.bandit import Bandit     # noqa: E402  作者仓库的模块
    model = Bandit(stems=list(BANDIT_STEMS), fs=BANDIT_FS, **BANDIT_KW)
    sd = torch.load(BANDIT_CKPT, map_location="cpu", weights_only=True)["state_dict"]
    model.load_state_dict({k.removeprefix("model."): v for k, v in sd.items() if k.startswith("model.")}, strict=True)
    return model.to(dev).eval()


def _overlap_add(model: nn.Module, x: torch.Tensor) -> dict[str, torch.Tensor]:
    """x：(ch, n) 48 kHz → {轨: (ch, n)}。每声道当一条单声道切 CHUNK_S 块、HOP_S 跳，Hann 窗叠加、按窗和归一。"""
    ch, n = x.shape
    chunk, hop = int(CHUNK_S * BANDIT_FS), int(HOP_S * BANDIT_FS)
    pad = chunk - hop                                          # 前后各垫一个重叠长：每个原样本都落在满窗叠加区
    n_chunks = math.ceil((n + 2 * pad - chunk) / hop) + 1
    total = (n_chunks - 1) * hop + chunk
    refl = min(pad, n - 1)
    xp = F.pad(x[None], (refl, refl), mode="reflect")[0]
    xp = F.pad(xp, (pad - refl, total - xp.shape[1] - (pad - refl)))
    frames = xp.unfold(1, chunk, hop)                          # (ch, n_chunks, chunk)
    flat = frames.reshape(-1, 1, chunk)
    win = torch.hann_window(chunk, device=x.device)
    outs: dict[str, list[torch.Tensor]] = {s: [] for s in BANDIT_STEMS}
    for i in range(0, flat.shape[0], BATCH):
        est = model({"mixture": {"audio": flat[i:i + BATCH]}})["estimates"]
        for s in BANDIT_STEMS:
            outs[s].append(est[s]["audio"].reshape(-1, chunk) * win)
    norm = F.fold(win.repeat(n_chunks, 1).T[None], (1, total), (1, chunk), stride=(1, hop))[0, 0, 0]
    res: dict[str, torch.Tensor] = {}
    for s in BANDIT_STEMS:
        y = torch.cat(outs[s]).reshape(ch, n_chunks, chunk).permute(0, 2, 1)       # (ch, chunk, n_chunks)
        y = F.fold(y, (1, total), (1, chunk), stride=(1, hop))[:, 0, 0]              # (ch, total)
        res[s] = (y / norm.clamp_min(1e-8))[:, pad:pad + n]
    return res


def bandit(src: Path, out: Path) -> Run:
    stems = {s: out / f"{s}.wav" for s in BANDIT_STEMS}
    x, sr = sf.read(src, dtype="float32", always_2d=True)
    sig = pc.signature([src], model=BANDIT_CKPT.name, md5=BANDIT_MD5, commit=BANDIT_COMMIT, chunk=CHUNK_S, hop=HOP_S, sr=sr)
    if (hit := _reuse(BANDIT, stems, sig)) is not None:
        return hit
    check_bandit()
    out.mkdir(parents=True, exist_ok=True)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    t0 = time.perf_counter()
    model = load_bandit(dev)
    t1 = time.perf_counter()
    x48 = soxr.resample(x, sr, BANDIT_FS, quality="VHQ")                            # (n48, ch)
    with torch.inference_mode():
        est = _overlap_add(model, torch.from_numpy(np.ascontiguousarray(x48.T)).to(dev))
    for s, y in est.items():
        back = soxr.resample(y.T.contiguous().cpu().numpy(), BANDIT_FS, sr, quality="VHQ")
        fit = np.zeros_like(x)
        fit[:min(len(back), len(x))] = back[:len(x)]
        write_wav(stems[s], fit, sr)
    t2 = time.perf_counter()
    name = device_name() if dev.type == "cuda" else "cpu"
    del model
    torch.cuda.empty_cache()
    pc.stamp(stems[BANDIT_STEMS[0]], sig, load_s=round(t1 - t0, 2), sep_s=round(t2 - t1, 2), device=name)
    return Run(BANDIT, stems, round(t1 - t0, 2), round(t2 - t1, 2), name, False)
