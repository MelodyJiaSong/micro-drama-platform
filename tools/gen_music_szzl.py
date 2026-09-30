# -*- coding: utf-8 -*-
"""《圣光刚好够用》（shengji_zhilu）主题曲草稿：ElevenLabs Music（music_v2_5 + composition_plan），一首一个请求。

    python tools/gen_music_szzl.py               # 缺哪首出哪首；mp3 已在就跳过（不重复计费）
    python tools/gen_music_szzl.py --dry-run     # 只过闸门、打印请求体，不调用
    python tools/gen_music_szzl.py --only t02

落点 `ai_videos/shengji_zhilu/2_世界观人设/music/drafts/{stem}/`：`{stem}.mp3` + 卡 `{stem}.md`（生成回执）
+ `{stem}.response.json`（API 原样返回的响应头与 JSON 部分）。
build 时闸门（命中即 raise，不发请求）：
· 禁用名单：prompt 只写风格，不点任何游戏 / 影视 / 作曲家 / 厂商（concept F5；Eleven Music Terms 也禁艺人名、曲名、厂牌名）；
· 无词：唱的行只许元音音节（Aah / Ooh），一个真词都不许；
· 单首 75–90 s、合计 ≤ 180 s；段长、行数、行长守 API 上限。
回读（从 mp3 量）：时长、积分响度、真峰值；时长出界即非零退出。
不自动重试：失败原样报出，要不要再发一次由人定。
续跑：mp3 与卡都在就跳过；只删卡再跑＝从 response.json 重写卡（不调 API），但会丢掉卡尾手工追加的「机检回读」段。

*(judgment call — 走 composition_plan 不走单句 prompt：v2.5 的段长是硬执行的，动机落在已知秒数上，日后截 sting 才有准；
而且 seed 只能配 plan 用，单句 prompt 没有可复现的种子，见 gen_bgm_sk2.py 的实测注。)*
*(judgment call — 走 /v1/music/detailed：同价多拿回 JSON 部分。实测 2026-09-30：给了 plan 时 song_metadata 全空（languages []），
返回的 composition_plan 与所发一致——核不了「无词」，只当回执存；无词靠上面的闸门 + 听。响应头没有 request-id，只有 song-id 与 x-trace-id。)*
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools" / "post"))
import post_common as pc  # noqa: E402  它再把 tools/ 加进 sys.path
import loudness  # noqa: E402
from image_fetch import api_key  # noqa: E402  ELEVENLABS_API_KEY 的唯一读法

DRAFTS = REPO / "ai_videos" / "shengji_zhilu" / "2_世界观人设" / "music" / "drafts"
API = "https://api.elevenlabs.io/v1/music/detailed"
MODEL_ID = "music_v2_5"
OUTPUT_FORMAT = "mp3_44100_192"   # 试听用；成片混音时 finish_ep 反正重采样到 48 kHz
PLAN = "Pro"
USD_PER_MIN = 0.15                # elevenlabs.io/pricing/api「Eleven Music $0.15 per minute」（2026-09-30 取）
LEN_S = (75, 90)                  # 单首时长区间（本批任务单）
TOTAL_MAX_S = 180                 # 本批合计上限（≈ $0.45）
API_CHUNK_MS = (3000, 120000)
API_MAX_CHUNKS = 30
API_MAX_LINES = 30
API_MAX_LINE = 200
API_MAX_STYLES = 50

# *(judgment call — 84 BPM：7/4 一小节正好 7 × 60/84 = 5.000 s，段界全落在小节线上，试听时对着秒表就能数小节。)*
BPM = 84
BEATS_PER_BAR = 7
BAR_MS = round(60_000 * BEATS_PER_BAR / BPM)
METER = f"{BEATS_PER_BAR}/4 time signature"
TEMPO = f"{BPM} BPM"
# *(judgment call — D 大调：哨笛 / 小提琴 / 竖琴的顺手调，两首同调，日后能互相拼接。)*
KEY = "D major"
GROUPING = f"{BEATS_PER_BAR}/4 meter, each bar grouped 2+2+3"

BANNED = re.compile(r"\b(" + "|".join([
    "blizzard", "warcraft", "wow", "azeroth", "stormwind", "elwynn", "northshire", "lordaeron", "hearthstone",
    "diablo", "starcraft", "overwatch", r"video ?games?", r"mmo(?:rpg)?", "rpg", "soundtrack of", "in the style of",
    "jason hayes", "russell brower", "derek duke", "glenn stafford", r"tracy w\.? bush", "neal acree",
    "david arkenstone", "howard shore", "hans zimmer", "john williams", "james horner", "enya",
    "loreena mckennitt", "clannad", "bill whelan", "riverdance", "jeremy soule", "nobuo uematsu", "koji kondo",
    "ramin djawadi", "lord of the rings", "braveheart", "titanic", "skyrim", "zelda", "final fantasy",
    "game of thrones",
]) + r")\b", re.I)
VOWEL_TOKEN = re.compile(r"(?:a+h*|o+h*|u+h*|m+)", re.I)

NEG = (
    "lyrics with words", "spoken word", "rap", "male vocals", "choir", "operatic vibrato",
    "epic trailer music", "heavy percussion", "drum kit", "electronic beats", "synthesizer", "electric guitar",
    "bagpipes", "East Asian instruments", "brass fanfare", "4/4 time signature",
)


@dataclass(frozen=True)
class Chunk:
    section: str
    bars: int
    directions: tuple[str, ...]     # 每条包进 {}，是给模型的段内指示
    sung: tuple[str, ...]           # 无词吟唱的音节行，模型当「歌词」唱；闸门只放元音
    styles: tuple[str, ...]

    @property
    def ms(self) -> int:
        return self.bars * BAR_MS

    def text(self) -> str:
        return "\n".join([f"[{self.section}]", *(f"{{{d}}}" for d in self.directions), *self.sung])

    def body(self) -> dict[str, object]:
        return {"text": self.text(), "duration_ms": self.ms, "positive_styles": list(self.styles),
                "negative_styles": list(NEG)}


@dataclass(frozen=True)
class Sketch:
    stem: str
    title: str
    seed: int
    chunks: tuple[Chunk, ...]
    concept: tuple[str, ...]        # 与 concept / style_guide 的对应，进卡
    listen: tuple[str, ...]         # 试听要点，进卡

    @property
    def ms(self) -> int:
        return sum(c.ms for c in self.chunks)

    def body(self) -> dict[str, object]:
        return {"composition_plan": {"chunks": [c.body() for c in self.chunks]}, "model_id": MODEL_ID,
                "seed": self.seed}

    def starts(self) -> list[tuple[float, Chunk]]:
        t, out = 0.0, []
        for c in self.chunks:
            out.append((t, c))
            t += c.ms / 1000
        return out


# *(judgment call — 动机取 1–2–5（D–E–A，末音延长）而不是大三和弦琶音 1–3–5：琶音是最通用的「升级」形状，
#  1–2–5 保住上行轮廓、又是五声音阶里的开放音程，贴凯尔特语汇，也离任何现成音效更远。)*
MOTIF = "a short rising three-note motif: D, then E, then a long held A"

SKETCHES: tuple[Sketch, ...] = (
    Sketch(
        stem="t01_main_theme",
        title="主题曲 · 7/4（凯尔特民谣 + 小编制管弦 + 无词女声）",
        seed=20260930,
        chunks=(
            Chunk("Intro", 2,
                  (f"solo Celtic harp alone, a gentle fingerpicked ostinato in {GROUPING}",
                   "a soft low string drone underneath, quiet early-morning stillness"),
                  (),
                  ("Celtic folk", "small chamber orchestra", "gentle main title theme", METER, TEMPO, KEY,
                   "hopeful", "understated", "Celtic harp", "warm intimate acoustic recording",
                   "great production quality")),
            Chunk("Theme A - low whistle", 4,
                  ("low whistle states the main melody: simple, singable, mostly stepwise, gently arching",
                   "harp ostinato continues, lightly strummed bouzouki, very soft bodhran on the first beat of each bar"),
                  (),
                  ("Celtic folk", METER, "low whistle melody", "bouzouki", "soft bodhran", "hopeful", "understated")),
            Chunk("Theme A - wordless voice", 4,
                  ("a soft, breathy solo female voice sings the melody without words, open vowels only",
                   "fiddle adds a gentle countermelody, warm chamber strings enter underneath"),
                  ("Aah... aah... aah...", "Ooh... ooh... aah..."),
                  ("wordless female vocalise", "soft breathy solo female voice", "fiddle countermelody",
                   "warm chamber strings", METER, "hopeful")),
            Chunk("Lift - small orchestra", 4,
                  ("the small orchestra lifts the theme: solo French horn and warm strings join the voice and the whistle",
                   "fuller and hopeful, but restrained, no big drums, no epic climax"),
                  ("Aah... aah... aah...",),
                  ("small chamber orchestra", "solo French horn", "warm strings", "wordless female vocalise",
                   "hopeful swell", "restrained", METER)),
            Chunk("Outro", 3,
                  ("the texture thins back to Celtic harp and the wordless voice",
                   f"the last phrase settles on {KEY} and rings out, quiet clean ending"),
                  ("Ooh... aah...",),
                  ("Celtic harp", "wordless female vocalise", "gentle ending", "ring out", "understated", METER)),
        ),
        concept=(
            "**E3 片头曲试 7/4**：本稿就是这次尝试——按 2+2+3 分组、84 BPM，一小节正好 5 s。"
            "耳听若数不齐 7 拍，按 E3 退 4/4、改下一稿的 plan，不在本稿上修。",
            "**F5 配乐语汇**：凯尔特民谣（竖琴 / 低音哨笛 / 小提琴 / 布祖基 / 宝思兰鼓）+ 小编制管弦（弦乐 + 圆号）+ 无词女声；"
            "请求里零作品名、零作曲家名（生成器禁用名单闸门）。",
            "**G9②**：本稿**不含**上行三音动机——动机只留给「学会新本事」那一刻（t02 供料），主题里先用掉就不稀罕了。",
            "**E5 BGM 走生成**：本稿即生成件。用途候选：S01 冷开场切黑后的片名卡 *JUST ENOUGH LIGHT*（style_guide §8）与片尾卡。",
        ),
        listen=(
            "段落起点 0 / 10 / 30 / 50 / 70 s（v2.5 硬执行段长）。数拍：跟着听到的拍子数，数到 7 回到强拍＝7/4，数到 4 或 8＝4/4。",
            "听三件事：① 是不是 7 拍一循环（E3 成败）② 女声只有 a / u 元音、没有吐字 ③ 克制，不是史诗。",
        ),
    ),
    Sketch(
        stem="t02_skill_motif",
        title="变奏 · 上行三音动机（「学会新本事」sting 取材）",
        seed=20260931,
        chunks=(
            Chunk("Motif - harp", 2,
                  ("near silence over a soft held low string note",
                   f"solo Celtic harp doubled by glockenspiel plays {MOTIF}",
                   "a soft string chord answers, then stillness"),
                  (),
                  ("Celtic folk", "small chamber orchestra", "rising three-note motif", "clear exposed melodic statement",
                   METER, TEMPO, KEY, "hopeful", "understated", "Celtic harp", "glockenspiel",
                   "warm intimate acoustic recording", "great production quality")),
            Chunk("Theme variation - fiddle", 4,
                  (f"a gentle groove begins in {GROUPING}: harp ostinato, lightly strummed bouzouki, very soft bodhran",
                   "fiddle plays a variation of the main theme that opens with the same rising three-note motif"),
                  (),
                  ("Celtic folk", METER, "fiddle melody", "bouzouki", "soft bodhran", "rising three-note motif",
                   "hopeful")),
            Chunk("Motif - wordless voice", 2,
                  ("everything drops out except one held string chord",
                   "a soft solo female voice sings the rising three-note motif without words, "
                   "doubled by harp and celesta, the last note held"),
                  ("Ah... ah... aah...",),
                  ("exposed rising three-note motif", "wordless female vocalise", "Celtic harp", "celesta",
                   "held string chord", "hushed", METER)),
            Chunk("Development - French horn", 4,
                  ("solo French horn states the rising three-note motif, then warm strings and low whistle develop the theme",
                   "hopeful and warm, restrained, no big drums"),
                  (),
                  ("solo French horn", "rising three-note motif", "warm strings", "low whistle",
                   "small chamber orchestra", "hopeful", "restrained", METER)),
            Chunk("Motif - final statement", 4,
                  ("the texture thins; low whistle plays the rising three-note motif one last time, answered by harp",
                   f"the last note is held over a soft {KEY} chord and rings out, quiet clean ending"),
                  ("Aah...",),
                  ("low whistle", "Celtic harp", "rising three-note motif", "wordless female vocalise", "gentle ending",
                   "ring out", METER)),
        ),
        concept=(
            "**G9② 上行三音动机**：D–E–A（1–2–5），末音延长；只进配乐层、只在「学会新本事」那一刻响（style_guide §9：ep01 S08、S14 各一次）。",
            "计划中五次陈述：0 s 竖琴 + 钢片琴（裸奏）· 10 s 小提琴起句 · 30 s 无词女声 + 竖琴 + 钢片琴（裸奏）· 40 s 圆号 · 60 s 低音哨笛；"
            "截 sting 首选 0–4 s 与 30–34 s 两处裸奏。",
            "**E7 → G9②**：旧「升级音做成上行三音和弦」已改为配乐层动机、没有升级音效——本稿只作配乐素材，不当音效用。",
            "当垫乐用时必须剪掉动机段（动机只在学会新本事时响）；计划与 t01 同调同速（D 大调 · 84 BPM · 7/4）以便互拼——模型实际给的速度见「机检回读」。",
        ),
        listen=(
            "听 0 / 10 / 30 / 40 / 60 s 五处有没有清楚的上行三音（任务单要求 ≥ 2 次清楚陈述）；记下最干净的一处，截 sting 用。",
            "同样核：7 拍一循环、女声无吐字、克制。",
        ),
    ),
)


def check(sketches: tuple[Sketch, ...]) -> None:
    errs: list[str] = []
    for sk in sketches:
        if not LEN_S[0] * 1000 <= sk.ms <= LEN_S[1] * 1000:
            errs.append(f"{sk.stem}：计划 {sk.ms / 1000:g} s，不在 {LEN_S[0]}–{LEN_S[1]} s")
        if len(sk.chunks) > API_MAX_CHUNKS:
            errs.append(f"{sk.stem}：{len(sk.chunks)} 段 > {API_MAX_CHUNKS}")
        for c in sk.chunks:
            where = f"{sk.stem}/[{c.section}]"
            if not API_CHUNK_MS[0] <= c.ms <= API_CHUNK_MS[1]:
                errs.append(f"{where}：段长 {c.ms} ms 越界")
            if not 1 <= len(c.section) <= 100:
                errs.append(f"{where}：段名长度越界")
            lines = c.text().splitlines()
            if len(lines) > API_MAX_LINES:
                errs.append(f"{where}：{len(lines)} 行 > {API_MAX_LINES}")
            errs += [f"{where}：行长 {len(x)} > {API_MAX_LINE}：{x[:60]}…" for x in lines if len(x) > API_MAX_LINE]
            if max(len(c.styles), len(NEG)) > API_MAX_STYLES:
                errs.append(f"{where}：style 超 {API_MAX_STYLES} 条")
            for s in c.sung:
                bad = [w for w in re.findall(r"[A-Za-z]+", s) if not VOWEL_TOKEN.fullmatch(w)]
                if bad:
                    errs.append(f"{where}：唱的行里有真词 {bad}（只许元音音节）")
        for s in json.dumps(sk.body(), ensure_ascii=False).splitlines():
            errs += [f"{sk.stem}：禁用名「{m.group(0)}」" for m in BANNED.finditer(s)]
    total = sum(sk.ms for sk in sketches) / 1000
    if total > TOTAL_MAX_S:
        errs.append(f"合计 {total:g} s > {TOTAL_MAX_S} s")
    if errs:
        raise SystemExit("闸门拦下，未发请求：\n  " + "\n  ".join(errs))


def split_multipart(ctype: str, data: bytes) -> list[tuple[dict[str, str], bytes]]:
    m = re.search(r'boundary="?([^";]+)"?', ctype)
    if not m:
        raise ValueError(f"multipart 没有 boundary：{ctype}")
    parts: list[tuple[dict[str, str], bytes]] = []
    for seg in data.split(b"--" + m.group(1).encode())[1:]:
        if seg.startswith(b"--"):
            break
        seg = seg[2:] if seg.startswith(b"\r\n") else seg.lstrip(b"\n")
        sep = b"\r\n\r\n" if b"\r\n\r\n" in seg else b"\n\n"
        head, _, payload = seg.partition(sep)
        if payload.endswith(b"\r\n"):
            payload = payload[:-2]
        hdrs: dict[str, str] = {}
        for line in head.decode("latin-1").splitlines():
            k, _, v = line.partition(":")
            if k.strip():
                hdrs[k.strip().lower()] = v.strip()
        parts.append((hdrs, payload))
    return parts


def looks_mp3(b: bytes) -> bool:
    return len(b) > 10_000 and (b[:3] == b"ID3" or (b[0] == 0xFF and b[1] & 0xE0 == 0xE0))


def unpack(raw: Path, mp3: Path, resp: Path) -> None:
    """raw（响应头 JSON 一行 + 空行 + 原始字节）→ mp3 + response.json；解不开就留着 raw 报错，不重发请求。"""
    head, _, data = raw.read_bytes().partition(b"\n\n")
    meta = json.loads(head)
    ctype = meta["headers"].get("content-type", "")
    json_part: object = None
    audio: bytes | None = None
    if ctype.startswith("multipart/"):
        for hdrs, payload in split_multipart(ctype, data):
            pct = hdrs.get("content-type", "")
            if pct.startswith("application/json"):
                json_part = json.loads(payload.decode("utf-8"))
            elif pct.startswith("audio/") or looks_mp3(payload):
                audio = payload
    elif looks_mp3(data):
        audio = data
    if audio is None or not looks_mp3(audio):
        raise SystemExit(f"{raw.name}：响应里找不到 mp3（content-type {ctype!r}）——raw 留在原地，手工解，不要重发")
    mp3.write_bytes(audio)
    resp.write_text(json.dumps({**meta, "json_part": json_part}, ensure_ascii=False, indent=1), encoding="utf-8")
    raw.unlink()


def compose(key: str, sk: Sketch, raw: Path) -> str | None:
    req = urllib.request.Request(f"{API}?output_format={OUTPUT_FORMAT}", data=json.dumps(sk.body()).encode(),
                                 method="POST", headers={"xi-api-key": key, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            data = r.read()
            hdrs = {k.lower(): v for k, v in r.headers.items() if k.lower() != "set-cookie"}
            status = r.status
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}：{e.read()[:1200].decode('utf-8', 'replace')}"
    except (urllib.error.URLError, TimeoutError) as e:
        return f"网络错误：{e}"
    meta = {"status": status, "elapsed_s": round(time.time() - t0, 1),
            "requested_at": datetime.fromtimestamp(t0).astimezone().isoformat(timespec="seconds"), "headers": hdrs}
    raw.write_bytes(json.dumps(meta, ensure_ascii=False).encode() + b"\n\n" + data)
    return None


def stream_info(mp3: Path) -> str:
    r = subprocess.run([pc.FFPROBE, "-v", "error", "-select_streams", "a:0", "-show_entries",
                        "stream=sample_rate,channels,bit_rate", "-of", "json", str(mp3)], capture_output=True)
    s = json.loads(r.stdout)["streams"][0]
    return f"{int(s['sample_rate']) / 1000:g} kHz · {s['channels']} ch · {round(int(s['bit_rate']) / 1000)} kbps"


def card(sk: Sketch, d: Path, mp3: Path, resp: Path) -> bool:
    meta = json.loads(resp.read_text(encoding="utf-8"))
    hdrs: dict[str, str] = meta["headers"]
    lp = loudness.measure(mp3)
    dur = pc.probe(mp3).a_dur
    ok = LEN_S[0] <= dur <= LEN_S[1]
    sha = hashlib.sha256(mp3.read_bytes()).hexdigest()
    rid = next((f"`{hdrs[k]}`（{k}）" for k in ("request-id", "x-request-id", "x-trace-id") if k in hdrs), None)
    status = "draft（未批准）" if ok else f"draft（未批准）· ⚠ 时长 {dur:.2f} s 出了 {LEN_S[0]}–{LEN_S[1]} s"
    plan_rows = "\n".join(f"| {t:g}–{t + c.ms / 1000:g} s | {c.section} | {c.bars} |" for t, c in sk.starts())
    song_meta = (meta.get("json_part") or {}).get("song_metadata") if isinstance(meta.get("json_part"), dict) else None
    body = json.dumps(sk.body(), ensure_ascii=False, indent=1)
    md = f"""# {sk.stem} · {sk.title}

> **status: {status}**——供试听；批准前不进 `finish_ep --bgm`、不进任何成片。**本卡即生成回执**（授权凭证），删卡＝丢证据；
> API 原样返回的响应头与 JSON 部分在 `{resp.name}`。生成器 `tools/gen_music_szzl.py`（请求体由它产出，本卡由它写）。

| 字段 | 值 |
|---|---|
| status | {status} |
| provider | ElevenLabs · Eleven Music API（`POST /v1/music/detailed?output_format={OUTPUT_FORMAT}`） |
| model_id | `{MODEL_ID}` |
| plan | {PLAN} |
| date | {meta['requested_at'][:10]}（请求 {meta['requested_at']}，耗时 {meta['elapsed_s']} s） |
| seed | {sk.seed} |
| song-id | `{hdrs.get('song-id', '未返回')}` |
| request-id | {rid or '未返回（响应头里没有 request-id 类字段；song-id 即唯一标识）'} |
| 音频 | `{mp3.name}` · {stream_info(mp3)} · sha256 `{sha}`（mp3 全局 gitignore，备份走 R2） |
| 时长 | 实测 **{dur:.2f} s**（计划 {sk.ms / 1000:g} s = {sum(c.bars for c in sk.chunks)} 小节 × {BAR_MS / 1000:g} s） |
| 响度（原始，未归一） | 积分 **{float(lp['input_i']):.1f} LUFS** · 真峰值 **{float(lp['input_tp']):.1f} dBTP** · LRA {float(lp['input_lra']):.1f} LU |
| 成本估算 | {dur / 60:.2f} min × ${USD_PER_MIN}/min = **${dur / 60 * USD_PER_MIN:.2f}**（list 价；Pro 月包 660 min 内扣） |
| 请求的速度 / 拍号 / 调 | {TEMPO} · {METER.split()[0]}（2+2+3）· {KEY}（模型是否照做见「机检回读」） |

## 与立项的对应

{chr(10).join(f'- {x}' for x in sk.concept)}

## 试听要点

{chr(10).join(f'- {x}' for x in sk.listen)}

| 段 | section | 计划小节（按 {TEMPO}） |
|---|---|---|
{plan_rows}

## 许可（Eleven Music · self-serve 计划，2026-09-30 取原文）

- Eleven Music Model-Specific Terms：Starter / Creator / **Pro** / Scale ＝ "All online and offline commercial use permitted, except film, TV, radio, & Studio Games"；Pro 有 streaming rights；付费档不要求署名。本剧主平台 YouTube 长视频属在线使用 ✅；将来上电视 / 电台 / 院线 / 游戏须另谈 Enterprise。
- 输出**不独占**（ToS："the Output … may not be unique across users"）→ **永不登记 YouTube Content ID 或任何指纹认领系统**。
- Music Terms 禁在 prompt 里写艺人 / 作曲家名、曲名、专辑名、厂牌名：生成器禁用名单闸门已拦（另加游戏 / 影视 / 厂商名，concept F5）。
- 与 concept F2（前 10–20 集非商业）/ E6（同人姿态）不冲突；本曲全原创、零魔兽原声（F5）。

## 生成请求（原样，不含 key）

*(judgment call — 不开 `force_instrumental`：它会连无词女声一起去掉（F5 要女声）；「无词」改由生成器闸门保证——唱的行只许元音音节。
不开 `store_for_inpainting` / `sign_with_c2pa`：计划档限制不明，一次失败就吃掉仅有的一次重试额度。)*

```json
{body}
```

## 模型返回的 song_metadata

```json
{json.dumps(song_meta, ensure_ascii=False, indent=1) if song_meta is not None else 'null（响应里没有 JSON 部分）'}
```
"""
    (d / f"{sk.stem}.md").write_text(md, encoding="utf-8")
    print(f"  卡 → {pc.rel(d / (sk.stem + '.md'))}：{dur:.2f} s · {float(lp['input_i']):.1f} LUFS · "
          f"{float(lp['input_tp']):.1f} dBTP · ${dur / 60 * USD_PER_MIN:.2f}" + ("" if ok else "  ⚠ 时长出界"))
    return ok


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser(description="shengji_zhilu 主题曲草稿（ElevenLabs Music）")
    ap.add_argument("--only", default="", help="逗号分隔的 stem 前缀，如 t02")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    check(SKETCHES)
    want = [x.strip() for x in a.only.split(",") if x.strip()]
    todo = [sk for sk in SKETCHES if not want or any(sk.stem.startswith(w) for w in want)]
    if a.dry_run:
        for sk in todo:
            print(f"[dry] {sk.stem}  {sk.ms / 1000:g} s  seed {sk.seed}\n{json.dumps(sk.body(), ensure_ascii=False, indent=1)}")
        return 0
    key: str | None = None
    bad = 0
    for sk in todo:
        d = DRAFTS / sk.stem
        d.mkdir(parents=True, exist_ok=True)
        mp3, resp, raw = d / f"{sk.stem}.mp3", d / f"{sk.stem}.response.json", d / f"{sk.stem}.raw"
        if (d / f"{sk.stem}.md").is_file() and mp3.is_file():
            print(f"· {sk.stem}：mp3 与卡都在，跳过")
            continue
        if not mp3.is_file() and not raw.is_file():
            key = key or api_key()
            print(f"→ {sk.stem}  {sk.ms / 1000:g} s  {MODEL_ID}  seed {sk.seed}", flush=True)
            err = compose(key, sk, raw)
            if err:
                print(f"  ✗ {err}\n  （不自动重试）", flush=True)
                bad += 1
                continue
        if raw.is_file():
            unpack(raw, mp3, resp)
        bad += not card(sk, d, mp3, resp)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
