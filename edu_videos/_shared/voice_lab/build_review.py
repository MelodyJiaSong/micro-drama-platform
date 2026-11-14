# -*- coding: utf-8 -*-
"""把各引擎样音汇成 review.json（管理应用 /character-review?path=edu_videos/_shared/voice_lab），并回听核对念得对不对。

    python edu_videos/_shared/voice_lab/build_review.py
中文按拼音比对音节错率（tools/edu_video.py 同一套），英文按单词错率；结果写进每项说明，供挑音色时参考。
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

import soundfile as sf

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[2]
sys.path.insert(0, str(REPO / "tools"))
import edu_video  # noqa: E402

ENGINES = {
    "qwen": ("Qwen3-TTS 1.7B", "Apache-2.0；文字描述设计音色 → Base 克隆"),
    "voxcpm": ("VoxCPM2", "Apache-2.0（模型卡禁止冒充、欺诈，AI 内容须标注）；括号描述设计 → 参考音克隆"),
    "moss": ("MOSS（现用）", "Apache-2.0；t01 / t03 现用音色克隆"),
}
VOICE = {"m": "男声 · 沉稳温暖的发布会主讲", "f": "女声 · 清亮知性的纪录片旁白"}
LANG = {"ref": "设计参考（中文）", "zh": "中文测试稿", "en": "英文测试稿"}


def wer(ref: str, hyp: str) -> float:
    a, b = re.findall(r"[a-z']+", ref.lower()), re.findall(r"[a-z']+", hyp.lower())
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
    return d[len(b)] / max(len(a), 1)


def main() -> None:
    from faster_whisper import WhisperModel
    asr = WhisperModel(edu_video.WHISPER, device="cpu", compute_type="int8")
    cfg = json.loads((LAB / "texts.json").read_text(encoding="utf-8"))
    texts = {"ref": cfg["ref_zh"], **cfg["test"]}
    sections, n = [], 0
    for eng, (name, how) in ENGINES.items():
        for v, vname in VOICE.items():
            items = []
            for kind in ("ref", "zh", "en"):
                wav = LAB / eng / f"{v}_{kind}.wav"
                if not wav.exists():
                    continue
                n += 1
                lang = "en" if kind == "en" else "zh"
                segs, _ = asr.transcribe(str(wav), language=lang)
                hyp = "".join(s.text for s in segs)
                err = wer(texts[kind], hyp) if lang == "en" else edu_video.cer(texts[kind], hyp)
                secs = sf.info(str(wav)).duration
                items.append({"id": f"{eng[0].upper()}{v.upper()}{'R' if kind == 'ref' else kind.upper()}",
                              "label": LANG[kind], "path": wav.relative_to(REPO).as_posix(), "kind": "audio",
                              "desc": f"{secs:.1f} 秒 · {'单词' if lang == 'en' else '音节'}错率 {err:.0%} · 识别：{hyp.strip()[:80]}"})
            if items:
                sections.append({"id": f"{eng}_{v}", "title": f"{name} · {vname}", "hint": how, "items": items})
    out = {"title": "配音选型试听", "character": "edu_videos 频道配音", "updated": date.today().isoformat(),
           "notes": ["同一段中英文讲稿，各引擎、各音色都念一遍。挑的时候说编号，例如「QM 男声不错，英文再自然些」。",
                     "错率由本地语音识别回听得出，只说明念得对不对，不代表好不好听。"],
           "sections": sections}
    (LAB / "review.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"review.json：{len(sections)} 组 {n} 条 → /character-review?path={LAB.relative_to(REPO).as_posix()}")


if __name__ == "__main__":
    main()
