# -*- coding: utf-8 -*-
"""教学视频（edu_videos）的配音、时间轴、字幕与合成。约定见 edu_videos/README.md。

    python tools/edu_video.py tts <知识点目录> [lNN ...]   讲稿 → 逐句克隆配音（本地 VoxCPM2，系列或频道 _shared/voice.json 定音色）
    python tools/edu_video.py qa <知识点目录> [lNN ...]     faster-whisper 回听：逐句错率（中文拼音音节 / 英文单词）、语速，存字级时间戳
    python tools/edu_video.py timeline <知识点目录>         去头尾静音、按段拼接 → audio/sN.wav 与 timeline.json（含包装卡）
                                       [--estimate]      配音没出时按语速估算时间轴，供画面草稿（不写音频）
    python tools/edu_video.py render <知识点目录> [SN ...]  跑 scenes/*.py 的 Manim 场景 → renders/[en/]sN.mp4（--draft 出 960×540）
    python tools/edu_video.py package <知识点目录>          按时间轴渲包装卡（片头、本期内容、章节转场、片尾）→ renders/package/
    python tools/edu_video.py sheet <知识点目录>            每句结尾抽帧拼总览图 → renders/sheets/（审片）
    python tools/edu_video.py preview <知识点目录>          生成 preview.json → 管理应用 /episode-preview?path=<知识点目录>
    python tools/edu_video.py mux <知识点目录> [--bgm x]    拼各段画面 + 配音（+配乐）+ 烧录字幕 → final/
每条命令都可加 `--lang en` 做英文版（缺省 zh）。

依赖：faster-whisper、pypinyin、soundfile、Pillow（系统 Python）；配音走 .cache/venvs/voxcpm（tools/edu_voxcpm.py），
voice.json 写 "engine": "moss" 的旧系列仍走 .cache/venvs/moss-voice（tools/local_voice_clone.py）。

讲稿格式：`## sN 标题` 为画面段，`- lNN: 文本` 为一句，句末可加 `[停N]`（英文稿 `[pause N]`）留 N 秒停顿。
字幕与念法不同时写 `{显示|念法}`，如 `{2011|二零一一}`、`{108|one hundred and eight}`：字幕显示前者，配音念后者。
段标题可带标签：`[冷开场]` 排在片头卡之前（先抛问题再出片名）；`[章:problem]` 段前插章节转场卡（章节 id 见系列 _shared/package.json）；`[包装:agenda]` / `[包装:outro]`
该段画面用包装卡（本期内容 / 片尾），卡上各项按该段每句开口时出场。系列有 _shared/package.json 时时间轴开头自动加片头卡。
双语：中文 `script.md`，英文 `script.en.md`，段号、句号与中文一一对应（动画按句号触发，两版共用一套场景）。
英文产物与中文并列：audio/en/、timeline.en.json、renders/en/、final/<知识点>.en.mp4、preview.en.json。
重出某句：在 <audio>/lines/takes.json 写 {"lNN": 种子}。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf

REPO = Path(__file__).resolve().parents[1]
ENGINES = {   # voice.json 的 engine → (环境里的 python, 生成脚本, 清单文件名)
    "voxcpm2": (REPO / ".cache" / "venvs" / "voxcpm" / "Scripts" / "python.exe", "edu_voxcpm.py", "gen_v2.json"),
    "moss": (REPO / ".cache" / "venvs" / "moss-voice" / "Scripts" / "python.exe", "local_voice_clone.py", "gen_v1.json"),
}
FPS = 30
SR = 48000
LEAD_IN = 0.6          # 每段开头留白（秒）
LINE_GAP = 0.35        # 句间停顿
TAIL = 0.9             # 每段结尾留白
SILENCE_DB = -42.0
CER_LIMIT = 0.12
WHISPER = "medium"     # 本机已缓存；large-v3 未下全
SUB_MAX = 20           # 字幕每屏最多字数（中文）
SUB_MAX_EN = 42        # 英文每屏最多字符
WER_LIMIT = 0.10
RATE = {"zh": (2.2, 7.0), "en": (1.4, 4.2)}   # 去头尾静音后的语速：中文字/秒，英文词/秒
EST_RATE = {"zh": 4.6, "en": 2.6}             # 估算时间轴用的典型语速（VoxCPM2 频道音色实测中文约 4.6 字/秒）
MANIM = REPO / ".cache" / "venvs" / "manim" / "Scripts" / "manim.exe"
SUB_FONT = "MiSans"                                    # 频道设计规范 v1（design_system.md §8）
SUB_FONTS_DIR = REPO / ".cache" / "fonts" / "misans"
PUNCT = "，。：；？！、“”‘’（）,.:;?!\"'()… 　"
LANGS = ("zh", "en")
LANG_LABEL = {"zh": "中文", "en": "English"}


SAY_RE = re.compile(r"\{([^|{}]*)\|([^{}]*)\}")      # `{显示|念法}`：字幕写 2011，配音念「二零一一」


@dataclass(frozen=True)
class Line:
    id: str
    raw: str                # 讲稿原文（可含 `{显示|念法}`）
    pause: float = 0.0      # 句后额外停顿，讲稿写 `[停N]`

    @property
    def text(self) -> str:
        """给人看的：字幕、预览、审片图。"""
        return SAY_RE.sub(r"\1", self.raw)

    @property
    def say(self) -> str:
        """给配音念的：TTS 与回听核对都用它。"""
        return SAY_RE.sub(r"\2", self.raw)


@dataclass(frozen=True)
class Segment:
    id: str
    title: str
    lines: tuple[Line, ...]
    chapter: str = ""       # 段前插章节转场卡
    card: str = ""          # 该段画面用包装卡（agenda / outro）
    cold: bool = False      # 冷开场：排在片头卡之前


SEG_RE = re.compile(r"##\s+(s\d+)\s*(.*)")
LINE_RE = re.compile(r"-\s+(l\d+):\s*(.+?)\s*(?:\[(?:停|pause)\s*(\d+(?:\.\d+)?)\])?$")
TAG_RE = re.compile(r"\[(章|chapter|包装|package)[:：]\s*([\w-]+)\]")
COLD_RE = re.compile(r"\[(冷开场|cold open)\]", re.I)


class Topic:
    def __init__(self, path: Path, lang: str = "zh") -> None:
        self.dir = path.resolve()
        if "edu_videos" not in self.dir.parts:
            raise SystemExit("知识点目录须在 edu_videos/<系列>/ 下")
        if lang not in LANGS:
            raise SystemExit(f"语言只支持 {LANGS}")
        self.lang = lang
        self.series = self.dir.parent
        sfx = "" if lang == "zh" else f".{lang}"
        self.script_path = self.dir / f"script{sfx}.md"
        self.audio_dir = self.dir / "audio" / ("" if lang == "zh" else lang)
        self.lines_dir = self.audio_dir / "lines"
        self.timeline_path = self.dir / f"timeline{sfx}.json"
        self.render_dir = self.dir / "renders" / ("" if lang == "zh" else lang)
        self.package_dir = self.dir / "renders" / "package" / lang
        self.stem = self.dir.name + sfx
        self.preview_path = self.dir / f"preview{sfx}.json"

    def segments(self) -> list[Segment]:
        if not self.script_path.exists():
            raise SystemExit(f"缺讲稿 {self.script_path.name}")
        segs: list[Segment] = []
        head, lines = None, []

        def close() -> None:
            if head:
                tags = {("chapter" if k in ("章", "chapter") else "card"): v for k, v in TAG_RE.findall(head[1])}
                title = COLD_RE.sub("", TAG_RE.sub("", head[1])).strip()
                segs.append(Segment(head[0], title, tuple(lines), **tags, cold=bool(COLD_RE.search(head[1]))))

        for raw in self.script_path.read_text(encoding="utf-8").splitlines():
            if m := SEG_RE.match(raw):
                close()
                head, lines = (m.group(1), m.group(2)), []
            elif m := LINE_RE.match(raw):
                if not head:
                    raise SystemExit(f"{m.group(1)} 不在任何 ## sN 段内")
                lines.append(Line(m.group(1), m.group(2).strip(), float(m.group(3) or 0)))
        close()
        ids = [ln.id for s in segs for ln in s.lines]
        if len(ids) != len(set(ids)):
            raise SystemExit("讲稿里有重复的句号 lNN")
        if self.lang != "zh":       # 英文稿与中文稿段、句一一对应，场景按句号触发才能两版共用
            zh = Topic(self.dir, "zh").segments()
            shape = lambda ss: [(s.id, s.chapter, s.card, s.cold, [ln.id for ln in s.lines]) for s in ss]
            if shape(segs) != shape(zh):
                raise SystemExit(f"{self.script_path.name} 的段 / 句号 / 标签与 script.md 不一致")
        return segs

    def package(self) -> dict | None:
        p = self.series / "_shared" / "package.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    def takes(self) -> dict[str, int]:
        p = self.lines_dir / "takes.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    def wav(self, line_id: str) -> Path:
        return self.lines_dir / f"{line_id}_s{self.takes().get(line_id, 1)}.wav"


def voice_config(topic: Topic) -> dict[str, str]:
    """系列 _shared/voice.json 优先，其次频道 edu_videos/_shared/voice.json。"""
    p = next((q for q in (topic.series / "_shared" / "voice.json", topic.series.parent / "_shared" / "voice.json")
              if q.exists()), None)
    if p is None:
        raise SystemExit("缺 voice.json：写 {\"engine\": \"voxcpm2\", \"reference\": \"<参考 wav，相对仓库根>\", "
                         "\"reference_text\": \"<参考音原文>\"}")
    return json.loads(p.read_text(encoding="utf-8"))


def cmd_tts(topic: Topic, only: list[str]) -> None:
    voice, takes = voice_config(topic), topic.takes()
    engine = voice.get("engine", "moss")
    if engine not in ENGINES:
        raise SystemExit(f"voice.json engine 未知：{engine}（可选 {', '.join(ENGINES)}）")
    py, script, name = ENGINES[engine]
    lines = [ln for s in topic.segments() for ln in s.lines]
    if engine == "moss":
        spec = {"items": [{"id": ln.id, "text": ln.say, "reference": [voice["reference"]],
                           "language": voice.get("language", "Chinese"), "seeds": [takes.get(ln.id, 1)]}
                          for ln in lines]}
    else:
        spec = {"voice": {"reference": voice["reference"], "reference_text": voice["reference_text"]},
                "items": [{"id": ln.id, "text": ln.say, "seeds": [takes.get(ln.id, 1)]} for ln in lines]}
    topic.lines_dir.mkdir(parents=True, exist_ok=True)
    manifest = topic.lines_dir / name
    manifest.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    subprocess.run([str(py), str(REPO / "tools" / script), str(manifest), *only], check=True)


HANZI_DIGITS = str.maketrans("零〇一二两三四五六七八九", "001223456789")
DIGIT_HANZI = str.maketrans("0123456789-", "零一二三四五六七八九负")
LETTER_READING = {"i": "ai", "j": "jie"}      # 配音把字母念成中文音节，识别常写成同音字


def normalize(text: str) -> str:
    text = text.lower().translate(HANZI_DIGITS)
    return "".join(ch for ch in text if ch not in PUNCT and not ch.isspace())


def syllables(text: str) -> list[str]:
    """按无声调拼音比对：识别把「矩阵」写成「举证」这类同音字不算念错，念错音才算。"""
    from pypinyin import lazy_pinyin
    text = re.sub(r"(?<=[零一二两三四五六七八九十\d])块(?=[零一二两三四五六七八九\d])", "点", text)   # 钱数：十块二 ↔ 识别的 10.2（t11，2026-11-10）
    text = re.sub(r"(?<=[零一二两三四五六七八九\d])毛(?=[零一二两三四五六七八九\d])", "", text)     # 两块五毛四 ↔ 2.54
    text = re.sub(r"[^一-鿿0-9a-z\-]", "", text.lower()).translate(DIGIT_HANZI)
    return [lazy_pinyin(ch)[0] if "一" <= ch <= "鿿" else LETTER_READING.get(ch, ch) for ch in text]


def place_reading(n: int) -> str:
    """阿拉伯数字按位值念：1797 → 一千七百九十七，10 → 十，300 → 三百（万以内）。"""
    if n == 0 or n >= 100000:
        return str(n).translate(DIGIT_HANZI)
    out, zero = "", False
    for unit, name in ((10000, "万"), (1000, "千"), (100, "百"), (10, "十"), (1, "")):
        q, n = divmod(n, unit)
        if q:
            if zero and out:
                out += "零"
            out += ("" if (q == 1 and name == "十" and not out) else "零一二三四五六七八九"[q]) + name
            zero = False
        elif out:
            zero = True
    return out


def number_variants(text: str, limit: int = 5) -> list[str]:
    """识别结果里的数字可能对应两种念法：逐位（年份 2024 → 二零二四）或位值（1797 → 一千七百九十七，37% → 百分之三十七）。
    每个数字两种都试，返回所有组合（数字多于 limit 个时只给逐位读法）。8×8 的 × 念「乘」。"""
    text = text.replace("×", "乘").replace("x", "乘") if re.search(r"\d\s*[×x]\s*\d", text) else text
    text = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: "百分之" + m.group(1), text)
    text = re.sub(r"(\d)\.(\d+)", lambda m: m.group(1) + "点" + m.group(2).translate(DIGIT_HANZI), text)   # 99.9 → 99点九（小数部分逐位念）
    nums = list(re.finditer(r"\d[\d,]*\d|\d", text))
    if not nums or len(nums) > limit:
        return [text]
    out = []
    for mask in range(1 << len(nums)):
        parts, last = [], 0
        for k, m in enumerate(nums):
            n = int(m.group().replace(",", ""))
            parts += [text[last:m.start()], place_reading(n) if mask >> k & 1 else m.group().replace(",", "")]
            last = m.end()
        out.append("".join(parts) + text[last:])
    return out


def _edit(a: list[str], b: list[str]) -> int:
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (ca != cb))
    return d[len(b)]


def cer(ref: str, hyp: str) -> float:
    a = syllables(ref)
    return min(_edit(a, syllables(h)) for h in number_variants(hyp)) / max(len(a), 1)


NUM_UNITS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                         "fourteen fifteen sixteen seventeen eighteen nineteen".split())}
NUM_TENS = {w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if w != "_"}


def spoken_numbers(words: list[str]) -> list[str]:
    """把念出来的数字词并成阿拉伯数字，和识别结果对齐：three hundred → 300，one hundred and eight → 108，
    twenty eleven → 2011（年份）。讲稿为了念对写成英文单词，识别常写成数字，不该算错。"""
    out: list[str] = []
    i = 0
    while i < len(words):
        w = words[i]
        if w not in NUM_UNITS and w not in NUM_TENS and not (w == "a" and i + 1 < len(words) and words[i + 1] == "hundred"):
            out.append(w); i += 1; continue
        total, cur, j, parts = 0, 0, i, []
        while j < len(words):
            x = words[j]
            if x in NUM_UNITS:
                cur += NUM_UNITS[x]
            elif x in NUM_TENS:
                if cur and cur % 100 and len(parts) == 1 and parts[0] in NUM_TENS:   # twenty eleven：年份
                    cur = cur * 100
                elif 0 < cur % 100 < 20:     # three fifty / ten twenty（钱数念法）是两个数，不是 53 / 30（t11，2026-11-10）
                    break
                cur += NUM_TENS[x]
            elif x == "a" and j + 1 < len(words) and words[j + 1] == "hundred":
                cur += 1
            elif x == "hundred" and cur:
                cur *= 100
            elif x == "thousand" and cur:
                total, cur = total + cur * 1000, 0
            elif x == "and" and parts and j + 1 < len(words) and (words[j + 1] in NUM_UNITS or words[j + 1] in NUM_TENS):
                pass
            else:
                break
            parts.append(x); j += 1
        if len(parts) >= 2 and parts[0] in NUM_TENS and parts[1] in NUM_UNITS and NUM_UNITS[parts[1]] >= 10:
            cur, total, j = NUM_TENS[parts[0]] * 100 + NUM_UNITS[parts[1]], 0, i + 2      # twenty thirteen：年份到此为止
        out.append(str(total + cur)); i = j
    return out


PLURAL_DIGITS = ["zeros", "ones", "twos", "threes", "fours", "fives", "sixes", "sevens", "eights", "nines"]


def words_en(text: str) -> list[str]:
    """英文词表：按标点分句各自并数字（逗号、句号两边的数字不连读）。"""
    import unicodedata
    text = unicodedata.normalize("NFKD", text.lower().replace("’", "'")).encode("ascii", "ignore").decode()  # résumé → resume
    text = re.sub(r"(?<=\d),(?=\d{3})", "", text)                                    # 1,500 → 1500
    text = re.sub(r"(\d)\s*[x×]\s*(\d)", r"\1 by \2", text)                           # 8x8 → 8 by 8
    text = re.sub(r"\b(\d)s\b", lambda m: PLURAL_DIGITS[int(m.group(1))], text)          # 3s → threes
    text = text.replace("%", " percent").replace("-", " ")         # 37% → 37 percent；ninety-seven 拆词
    text = re.sub(r"\$(\d+)\.(\d\d)\b", r"\1 \2", text).replace("$", " ")   # 钱数：$3.50 念 three fifty → 3 50；$5 → 5（dollar 词在下面去掉）（t11 回听误报，2026-11-10）
    text = re.sub(r"(\d+)\.(\d+)", lambda m: m.group(1) + " point " + " ".join(m.group(2)), text)   # 7.75 → 7 point 7 5（小数逐位念）
    dw = {"zero": "0", "oh": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    text = re.sub(r"\bpoint((?:\s+(?:zero|oh|one|two|three|four|five|six|seven|eight|nine)\b)+)",   # point seven five → point 7 5（逐位，不并成 12）
                  lambda m: "point " + " ".join(dw[w] for w in m.group(1).split()), text)
    out: list[str] = []
    for clause in re.split(r"[.,;:?!—]", text):
        toks = [t for t in spoken_numbers(re.findall(r"[a-z0-9]+(?:'[a-z]+)?", clause)) if t not in ("dollar", "dollars")]
        merged: list[str] = []                                                       # R L H F ↔ RLHF：连着的单字母并成一个词
        run = False
        for t in toks:
            letter = len(t) == 1 and t.isalpha() and t not in ("a", "i")
            if letter and run:
                merged[-1] += t
            else:
                merged.append(t)
            run = letter
        out += merged
    return out


def merge_compounds(toks: list[str], vocab: set[str]) -> list[str]:
    """相邻两词拼起来正好是对方的一个词就并成一个（hand written ↔ handwritten、every one ↔ everyone），不算念错。"""
    out: list[str] = []
    for t in toks:
        if out and out[-1] + t in vocab:
            out[-1] += t
        else:
            out.append(t)
    return out


def wer(ref: str, hyp: str) -> float:
    a, b = words_en(ref), words_en(hyp)
    a, b = merge_compounds(a, set(b)), merge_compounds(b, set(a))
    # 「6 x 6」words_en 记成 6 by 6，口播念「six times six」：两边 by / times 视为同一个词（t13 回听误报，2026-11-10）
    a, b = ["times" if w == "by" else w for w in a], ["times" if w == "by" else w for w in b]
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
    return d[len(b)] / max(len(a), 1)


def units(text: str, lang: str) -> int:
    """语速计数单位：中文字数，英文词数。"""
    return len(normalize(text)) if lang == "zh" else len(words_en(text))


def cmd_qa(topic: Topic, only: list[str]) -> None:
    from faster_whisper import WhisperModel
    model = WhisperModel(WHISPER, device="cpu", compute_type="int8")
    zh = topic.lang == "zh"
    prompt = "以下是普通话的科普讲解，使用简体中文。" if zh else None
    lo, hi = RATE[topic.lang]
    bad = 0
    for s in topic.segments():
        for ln in s.lines:
            if only and ln.id not in only:
                continue
            wav = topic.wav(ln.id)
            if not wav.exists():
                print(f"{ln.id} 缺配音 {wav.name}"); bad += 1; continue
            segs, _ = model.transcribe(str(wav), language=topic.lang, word_timestamps=True, initial_prompt=prompt)
            words = [{"w": w.word, "start": round(w.start, 3), "end": round(w.end, 3)} for sg in segs for w in sg.words]
            hyp = "".join(w["w"] for w in words)
            rate = units(ln.say, topic.lang) / max(len(trimmed(wav)) / SR, 0.1)     # 去头尾静音后的语速
            e = cer(ln.say, hyp) if zh else wer(ln.say, hyp)
            flag = "  <-- 重出" if e > (CER_LIMIT if zh else WER_LIMIT) or not lo <= rate <= hi else ""
            bad += bool(flag)
            print(f"{ln.id} {'音节' if zh else '单词'}错率 {e:.2f} 语速 {rate:.1f} {'字' if zh else '词'}/秒 | {hyp.strip()}{flag}")
            wav.with_suffix(".words.json").write_text(json.dumps({"text": ln.say, "hyp": hyp, "err": round(e, 3),
                                                                  "words": words}, ensure_ascii=False, indent=1),
                                                      encoding="utf-8")
    print(f"共 {bad} 句需重出" if bad else "全部通过")


def trimmed(path: Path) -> np.ndarray:
    x, sr = sf.read(str(path), dtype="float32", always_2d=True)
    if sr != SR:
        raise SystemExit(f"{path.name} 采样率 {sr}，期望 {SR}")
    mono = x.mean(axis=1)
    win = int(0.02 * SR)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(win) / win, mode="same"))
    loud = np.flatnonzero(env > 10 ** (SILENCE_DB / 20))
    if loud.size == 0:
        raise SystemExit(f"{path.name} 全是静音")
    a, b = max(loud[0] - int(0.05 * SR), 0), min(loud[-1] + int(0.12 * SR), len(mono))
    return mono[a:b]


def frames(sec: float) -> int:
    """段长对齐整帧（按采样数），拼接不漂移。"""
    return int(np.ceil(sec * FPS)) * SR // FPS


def cmd_timeline(topic: Topic, estimate: bool = False) -> None:
    pkg = topic.package()
    if pkg is None and any(s.chapter or s.card for s in topic.segments()):
        raise SystemExit("讲稿用了 [章:] / [包装:] 标签，但系列没有 _shared/package.json")
    out: dict[str, dict] = {}
    offset = 0.0
    topic.audio_dir.mkdir(parents=True, exist_ok=True)

    def card(sid: str, name: str, title: str, sec: float) -> None:      # 无配音的包装卡：静音占位
        nonlocal offset
        total = frames(sec)
        if not estimate:
            sf.write(str(topic.audio_dir / f"{sid}.wav"), np.zeros(total, np.float32), SR, subtype="PCM_24")
        out[sid] = {"title": title, "card": name, "offset": round(offset, 3), "duration": round(total / SR, 4), "lines": {}}
        offset += total / SR

    segs = topic.segments()
    cold = [s for s in segs if s.cold]
    if cold and segs[:len(cold)] != cold:
        raise SystemExit("[冷开场] 段必须排在讲稿最前面")
    for i, s in enumerate(segs):
        if pkg and i == len(cold):          # 片头卡排在冷开场之后
            card("intro", "intro", "片头" if topic.lang == "zh" else "Intro", pkg["durations"]["intro"])
        if s.chapter:
            rail = {c["id"]: c["rail"][topic.lang] for c in pkg["chapters"]}
            if s.chapter not in rail:
                raise SystemExit(f"{s.id} 的章节 {s.chapter} 不在系列章节里（{', '.join(rail)}）")
            card(f"c_{s.chapter}", f"chapter:{s.chapter}", rail[s.chapter], pkg["durations"]["chapter"])
        parts, cues, t = [np.zeros(int(LEAD_IN * SR), np.float32)], {}, LEAD_IN
        for ln in s.lines:
            if estimate:
                clip = np.zeros(int(units(ln.say, topic.lang) / EST_RATE[topic.lang] * SR), np.float32)
            else:
                clip = trimmed(topic.wav(ln.id))
            cues[ln.id] = [round(t, 3), round(t + len(clip) / SR, 3)]
            t += len(clip) / SR
            parts += [clip, np.zeros(int((LINE_GAP + ln.pause) * SR), np.float32)]
            t += LINE_GAP + ln.pause
        total = frames(t - LINE_GAP + TAIL)
        audio = np.concatenate(parts)[:total]
        audio = np.pad(audio, (0, total - len(audio)))
        if not estimate:
            sf.write(str(topic.audio_dir / f"{s.id}.wav"), audio, SR, subtype="PCM_24")
        out[s.id] = {"title": s.title, "offset": round(offset, 3), "duration": round(total / SR, 4), "lines": cues}
        if s.card:
            out[s.id]["card"] = s.card
        offset += total / SR
    doc = {"fps": FPS, "lang": topic.lang, "total": round(offset, 3), "segments": out} | ({"estimated": True} if estimate else {})
    topic.timeline_path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{topic.timeline_path.name}：{len(out)} 段，共 {offset:.1f} 秒" + ("（估算，配音出来后重跑）" if estimate else ""))


def cmd_render(topic: Topic, scenes: list[str], draft: bool) -> None:
    """跑 scenes/*.py 里与时间轴画面段同名的场景（sN → SN），输出拷到 renders/[en/]sN.mp4。
    有 scenes/web/（网页场景，设计规范 v1 起的默认做法）就交给 tools/edu_web.py 渲。"""
    import os
    import shutil
    if (topic.dir / "scenes" / "web").is_dir():
        import edu_web
        edu_web.cmd_render(topic, [x.lower() for x in scenes])
        return
    files = sorted((topic.dir / "scenes").glob("*.py"))
    if len(files) != 1:
        raise SystemExit(f"scenes/ 下应有且只有一个场景文件，现有 {[f.name for f in files]}")
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
    names = scenes or [sid.upper() for sid, seg in tl["segments"].items() if "card" not in seg and sid.startswith("s")]
    media = topic.render_dir / "media"
    res = "960,540" if draft else "1920,1080"
    env = os.environ | {"EDU_LANG": topic.lang, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([str(MANIM), "-r", res, "--fps", str(FPS), "--media_dir", str(media), "--disable_caching",
                        str(files[0]), *names], cwd=topic.dir, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    log = topic.render_dir / "render.log"
    log.write_text(r.stdout + r.stderr, encoding="utf-8")
    warn = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.startswith(("[cue]", "[layout]"))]
    if r.returncode != 0:
        raise SystemExit(f"Manim 失败（{log}）：\n" + (r.stdout + r.stderr)[-3000:])
    quality = f"{res.split(',')[1]}p{FPS}"
    for n in names:
        src = media / "videos" / files[0].stem / quality / f"{n}.mp4"
        if not src.exists():
            raise SystemExit(f"没找到 Manim 输出 {src}")
        shutil.copy2(src, topic.render_dir / f"{n.lower()}.mp4")
    print(f"渲好 {len(names)} 段 → {topic.render_dir}" + ("（草稿 960×540）" if draft else ""))
    for w in warn:
        print(w)


def cmd_package(topic: Topic) -> None:
    """按时间轴渲包装卡。本期内容卡：第 1 句出标题，第 2 句起每句出一行，最后一句出先修；
    片尾卡：第 1 句出眉题，之后每句出一行引语，最后一句出下一期。句子不够的项均匀铺到卡尾前。"""
    sys.path.insert(0, str(REPO / "tools"))
    import edu_package
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
    for sid, seg in tl["segments"].items():
        if "card" not in seg:
            continue
        cues = [round(a, 2) for a, _ in seg["lines"].values()] or None    # 第一句出标题 / 眉题，之后每句出一项
        if seg["card"] == "outro" and cues:
            # 片尾口播常是「一整句总结＋下一期」（台词审：引语要说成完整的一句，不拆成两句念）：
            # 句子不够一行引语一句时，引语各行铺在第一句里，下一期跟最后一句出（不再让引语跟着「下一期」那句出）。
            q = len(json.loads((topic.dir / "package.json").read_text(encoding="utf-8"))["quote"][topic.lang])
            spans = list(seg["lines"].values())
            if len(spans) < 2 + q:
                a, b = spans[0]
                cues = [round(a, 2)] + [round(a + (b - a) * f, 2) for f in [0.12 + 0.4 * i for i in range(q)]] \
                    + ([round(spans[-1][0], 2)] if len(spans) > 1 else [])
        edu_package.render(topic.dir, topic.lang, seg["card"], seg["duration"], cues, name=sid)


def chunks(text: str, lang: str = "zh") -> list[str]:
    """字幕断句：句号、问号、分号、冒号处必断；句内按逗号、冒号合并到 SUB_MAX；三字以内的碎片并入下一条。"""
    if lang != "zh":
        return chunks_en(text)
    out: list[str] = []
    for sent in (x for x in re.split(r"(?<=[。？！；：])", text) if x.strip()):
        cur: list[str] = []
        for p in (x for x in re.split(r"(?<=[，：])", sent) if x.strip()):
            if cur and len(cur[-1]) + len(p) <= SUB_MAX:
                cur[-1] += p
            else:
                cur.append(p)
        out += cur
    merged: list[str] = []
    for c in out:
        if merged and len(normalize(merged[-1])) <= 3:
            merged[-1] += c
        else:
            merged.append(c)
    return [c.strip().rstrip("，。；：") for c in merged]


WEAK_END = set("a an the to of and or but in on at for with from by as that which who his her its their our your "
               "is are was were be than more most very this these those it he she they we you i".split())


def wrap_en(c: str) -> list[str]:
    """一段英文切成 k = ⌈长度 / SUB_MAX_EN⌉ 行：动态规划挑断点，代价 = 行长偏离均值的平方 + 行尾是虚词的罚分。"""
    words = c.split()
    k = -(-len(c) // SUB_MAX_EN)
    if k <= 1 or len(words) < 2:
        return [c]
    target = len(c) / k
    n = len(words)
    best: dict[tuple[int, int], tuple[float, list[int]]] = {(0, 0): (0.0, [])}
    for parts in range(1, k + 1):
        for end in range(1, n + 1):
            for start in range(0, end):
                if (start, parts - 1) not in best:
                    continue
                line = " ".join(words[start:end])
                if len(line) > SUB_MAX_EN + 8:
                    continue
                cost = best[(start, parts - 1)][0] + (len(line) - target) ** 2
                if end < n and words[end - 1].lower().strip(",.;:") in WEAK_END:
                    cost += 400
                if (end, parts) not in best or cost < best[(end, parts)][0]:
                    best[(end, parts)] = (cost, best[(start, parts - 1)][1] + [end])
    if (n, k) not in best:
        return [c]
    cuts, prev, lines = best[(n, k)][1], 0, []
    for e in cuts:
        lines.append(" ".join(words[prev:e]))
        prev = e
    return lines


def chunks_en(text: str) -> list[str]:
    """英文字幕：句末标点必断，句内按逗号 / 破折号合并到 SUB_MAX_EN 字符，再长按词折；两词以内的碎片并入下一条。"""
    out: list[str] = []
    for sent in (x.strip() for x in re.split(r"(?<=[.?!;:])\s+", text) if x.strip()):
        cur: list[str] = []
        bits = re.split(r"(,(?!\d)[\"”’]?|—[\"”’]?)\s*", sent)      # 1,100 的逗号不断；逗号后的右引号跟着前半句，不甩到下一屏
        pieces = ["".join(bits[i:i + 2]) for i in range(0, len(bits), 2)]
        for part in (x.strip() for x in pieces if x.strip()):
            if cur and len(cur[-1]) + 1 + len(part) <= SUB_MAX_EN:
                cur[-1] += " " + part
            else:
                cur.append(part)
        for c in cur:                       # 单段仍超长：按词切成 k 行，行长均衡、不在虚词后断
            out += wrap_en(c)
    merged: list[str] = []
    for c in out:
        short = len(merged[-1].split()) <= 2 or len(c.split()) <= 2 if merged else False      # 两词以内的碎片并到相邻一条
        if short and len(merged[-1]) + 1 + len(c) <= SUB_MAX_EN + 10:
            merged[-1] += " " + c
        else:
            merged.append(c)
    return [c.rstrip(",;—") for c in merged]


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(topic: Topic, path: Path) -> None:
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))["segments"]
    rows, n = [], 0
    for s in topic.segments():
        for ln in s.lines:
            a, b = (tl[s.id]["offset"] + v for v in tl[s.id]["lines"][ln.id])
            parts = chunks(ln.text, topic.lang)
            size = (lambda x: len(normalize(x))) if topic.lang == "zh" else len
            weights = np.cumsum([0] + [size(p) for p in parts]) / max(sum(size(p) for p in parts), 1)
            for i, p in enumerate(parts):
                n += 1
                rows.append(f"{n}\n{srt_time(a + (b - a) * weights[i])} --> {srt_time(a + (b - a) * weights[i + 1])}\n{p}\n")
    path.write_text("\n".join(rows), encoding="utf-8")


def cmd_mux(topic: Topic, bgm: Path | None, bgm_db: float) -> None:
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
    final = topic.dir / "final"
    final.mkdir(exist_ok=True)
    work = topic.render_dir
    work.mkdir(parents=True, exist_ok=True)
    lst, alst = work / "concat.txt", work / "concat_audio.txt"
    lst.write_text("".join(f"file '{(work / f'{s}_fit.mp4').as_posix()}'\n" for s in tl["segments"]), encoding="utf-8")
    alst.write_text("".join(f"file '{(topic.audio_dir / f'{s}.wav').as_posix()}'\n" for s in tl["segments"]),
                    encoding="utf-8")
    for s, seg in tl["segments"].items():
        v = (topic.package_dir if "card" in seg else work) / f"{s}.mp4"     # 包装卡由 package 命令渲
        if not v.exists():
            raise SystemExit(f"缺 {v}" + ("（先跑 package）" if "card" in seg else ""))
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    str(v)], capture_output=True, text=True).stdout)
        if abs(dur - seg["duration"]) > 1.5 / FPS:
            raise SystemExit(f"{s}.mp4 时长 {dur:.3f} 与配音 {seg['duration']:.3f} 不符，重渲该段")
        pad = max(seg["duration"] - dur, 0)        # Manim 常少末帧；补齐到配音时长，拼接不累积漂移
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(v), "-vf",
                        f"scale=1920:1080,tpad=stop_mode=clone:stop_duration={pad:.4f},fps={FPS}", "-t", f"{seg['duration']:.4f}",
                        "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-pix_fmt", "yuv420p",
                        str(work / f"{s}_fit.mp4")], check=True)
    srt = final / f"{topic.stem}.srt"
    write_srt(topic, srt)
    # 浅色舞台：墨色字、不加底框、细白描边防压到深色画面；字高约 50px，落在底部 150px 字幕带内
    style = (f"FontName={SUB_FONT},FontSize=20,Bold=0,PrimaryColour=&H001F1D1D,OutlineColour=&H00FDFBFB,"
             "BorderStyle=1,Outline=1.2,Shadow=0,MarginV=22")
    sub = srt.as_posix().replace(":", r"\:")
    fonts = SUB_FONTS_DIR.as_posix().replace(":", r"\:")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
           "-f", "concat", "-safe", "0", "-i", str(alst)]
    voice = "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000"
    if bgm:
        cmd += ["-stream_loop", "-1", "-i", str(bgm)]
        fade = max(tl["total"] - 3, 0)
        mix = (f"{voice},asplit=2[v][key];"
               f"[2:a]aresample=48000,volume={bgm_db}dB,atrim=0:{tl['total']},afade=t=in:d=2,afade=t=out:st={fade}:d=3[m];"
               "[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=30:release=500[d];"
               "[v][d]amix=inputs=2:normalize=0:duration=first[a]")
    else:
        mix = f"{voice}[a]"
    out = final / f"{topic.stem}.mp4"
    cmd += ["-filter_complex", f"[0:v]subtitles='{sub}':fontsdir='{fonts}':force_style='{style}'[vo];{mix}",
            "-map", "[vo]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
    subprocess.run(cmd, check=True)
    print(f"成片 {out}（{tl['total']:.1f} 秒），字幕 {srt}")


def cmd_sheet(topic: Topic, video_dir: Path | None) -> None:
    """每句结尾抽一帧，按段拼成总览图（审片用）。"""
    from PIL import Image, ImageDraw, ImageFont
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))["segments"]
    src = video_dir or topic.render_dir
    out = topic.render_dir / "sheets"
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("C:/Windows/Fonts/NotoSansSC-VF.ttf", 22)
    texts = {ln.id: ln.text for s in topic.segments() for ln in s.lines}
    for sid, seg in tl.items():
        if not seg["lines"]:
            continue
        video = (topic.package_dir / f"{sid}.mp4" if "card" in seg else src / f"{sid}.mp4" if (src / f"{sid}.mp4").exists()
                 else next(iter(sorted(src.rglob(f"{sid.upper()}.mp4"))), src / f"{sid}.mp4"))
        if not video.exists():
            print(f"{sid}：没有画面 {video.name}，跳过" + ("（先跑 package）" if "card" in seg else ""))
            continue
        tiles = []
        for lid, (a, b) in seg["lines"].items():
            frame = out / f"_{sid}_{lid}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(b - 0.15, 0):.2f}", "-i", str(video),
                            "-frames:v", "1", "-vf", "scale=640:-1", str(frame)], check=True)
            im = Image.open(frame).convert("RGB")
            tile = Image.new("RGB", (im.width, im.height + 64), "white")
            tile.paste(im, (0, 0))
            ImageDraw.Draw(tile).text((8, im.height + 4), f"{lid} {texts[lid][:26]}", fill="black", font=font)
            tiles.append(tile)
            frame.unlink()
        cols = 3
        w, h = tiles[0].size
        sheet = Image.new("RGB", (w * cols, h * ((len(tiles) + cols - 1) // cols)), "white")
        for k, t in enumerate(tiles):
            sheet.paste(t, (k % cols * w, k // cols * h))
        sheet.save(out / f"{sid}.png")
        print(out / f"{sid}.png")


def cmd_preview(topic: Topic) -> None:
    """生成 `preview.json`，供管理应用单集预览页（成片模式）审片：章节 = 画面段，每句一段并截缩略图。"""
    rel = lambda p: p.relative_to(REPO).as_posix()
    tl = json.loads(topic.timeline_path.read_text(encoding="utf-8"))
    video = topic.dir / "final" / f"{topic.stem}.mp4"
    if not video.exists():
        raise SystemExit(f"缺成片 {video}，先跑 mux")
    script = topic.script_path.read_text(encoding="utf-8")
    heading = re.search(r"^#\s+(.+?)(?:\s+—\s+(?:讲稿|Script))?\s*$", script, re.M)
    tagline = re.search(r"^>\s*(?:一句话|In one sentence)[:：]\s*(.+)$", script, re.M)
    thumbs = topic.render_dir / "thumbs"
    thumbs.mkdir(parents=True, exist_ok=True)
    chapters, items = [], []
    for s in topic.segments():
        seg = tl["segments"][s.id]
        if s.chapter:          # 章节从转场卡开始
            chapters.append({"id": s.id, "title": s.title, "t": round(tl["segments"][f"c_{s.chapter}"]["offset"], 2)})
        else:
            chapters.append({"id": s.id, "title": s.title, "t": round(seg["offset"], 2)})
        for ln in s.lines:
            a, b = (seg["offset"] + v for v in seg["lines"][ln.id])
            thumb = thumbs / f"{ln.id}.jpg"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(b - 0.15, 0):.2f}", "-i", str(video),
                            "-frames:v", "1", "-vf", "scale=480:-1", "-q:v", "5", str(thumb)], check=True)
            items.append({"t": round(a, 2), "end": round(b, 2), "title": chunks(ln.text, topic.lang)[0], "subtitle": ln.text,
                          "badge": ln.id, "chapter": s.id, "image": rel(thumb)})
    links = [{"label": "讲稿", "path": rel(topic.script_path)}, {"label": "时间轴", "path": rel(topic.timeline_path)}]
    links += [{"label": "调研", "path": rel(p)} for p in [topic.dir / "research.md"] if p.exists()]
    links += [{"label": "字幕", "path": rel(p)} for p in [topic.dir / "final" / f"{topic.stem}.srt"] if p.exists()]
    langs = [{"lang": lg, "label": LANG_LABEL[lg], "preview": rel(Topic(topic.dir, lg).preview_path)}
             for lg in LANGS if Topic(topic.dir, lg).script_path.exists()]
    out = {"title": heading.group(1) if heading else topic.dir.name, "tagline": tagline.group(1) if tagline else "",
           "lang": topic.lang, "languages": langs if len(langs) > 1 else [],
           "video": rel(video), "duration": round(tl["total"], 2), "chapters": chapters, "items": items, "links": links}
    topic.preview_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    q = "" if topic.lang == "zh" else f"&lang={topic.lang}"
    print(f"{topic.preview_path.name}：{len(chapters)} 章 {len(items)} 段 → /episode-preview?path={rel(topic.dir)}{q}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    subs = {}
    for name in ("tts", "qa", "timeline", "package", "render", "sheet", "preview", "mux"):
        subs[name] = p = sub.add_parser(name)
        p.add_argument("topic", type=Path)
        p.add_argument("--lang", choices=LANGS, default="zh")
    for name in ("tts", "qa"):
        subs[name].add_argument("ids", nargs="*")
    subs["sheet"].add_argument("--video-dir", type=Path)
    subs["timeline"].add_argument("--estimate", action="store_true")
    subs["render"].add_argument("scenes", nargs="*")
    subs["render"].add_argument("--draft", action="store_true")
    subs["mux"].add_argument("--bgm", type=Path)
    subs["mux"].add_argument("--bgm-db", type=float, default=-24.0)
    a = ap.parse_args()
    topic = Topic(a.topic, a.lang)
    if a.cmd == "tts":
        cmd_tts(topic, a.ids)
    elif a.cmd == "qa":
        cmd_qa(topic, a.ids)
    elif a.cmd == "timeline":
        cmd_timeline(topic, a.estimate)
    elif a.cmd == "render":
        cmd_render(topic, a.scenes, a.draft)
    elif a.cmd == "package":
        cmd_package(topic)
    elif a.cmd == "sheet":
        cmd_sheet(topic, a.video_dir)
    elif a.cmd == "preview":
        cmd_preview(topic)
    else:
        cmd_mux(topic, a.bgm, a.bgm_db)


if __name__ == "__main__":
    sys.exit(main())
