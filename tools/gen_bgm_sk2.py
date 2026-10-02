# -*- coding: utf-8 -*-
"""按 `casting.md` §6.2 的分段编制表出 sk2 的 12 段 BGM。

为什么不用 `tools/stableaudio_gen.py`
------------------------------------
它走 `stabilityai/stable-audio-open-1.0` 本地权重，要 **torch**（本机未装，~2.5 GB）
**且权重在 HuggingFace 上是 gated 的**——必须本人去网页接受许可才能下载。
这两条都不是能自动化绕过的。

而 **ElevenLabs 有 `POST /v1/music`**（2026-09-20 查 openapi 实证），本账号是 Pro、
图片链路一直在用同一个 key，不需要任何额外授权。参数正好对得上 §6 的纪律：
`force_instrumental=true` ⇔ §6.3「无词：不出现任何语种的可辨歌词」；
`music_length_ms` 3 s–600 s ⇔ 每段按实际镜段时长给。

`stableaudio_gen.py` 保留不动——它是 webapp 的 BGM 库在用的，与本片无关。

用法（仓库根目录）：
    python tools/gen_bgm_sk2.py                 # 全部 12 段（跳过已存在）
    python tools/gen_bgm_sk2.py --only 5,9
    python tools/gen_bgm_sk2.py --force
    python tools/gen_bgm_sk2.py --dry-run       # 只打印 prompt 与时长，不调用

纪律（来自 `casting.md` §6）
---------------------------
· **英语系（西欧/不列颠）语汇**，不用东亚音阶、不用中式乐器。
· **无词**：`force_instrumental=True`，prompt 里也写死 no vocals / no lyrics。
· **绝不使用暴雪原声音乐**——全片原创；prompt 里不出现任何作品名与曲名。
· **S20–S22 王座厅近乎无乐**是设计不是遗漏，所以那一段的 prompt 只要一层极弱持续音。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "ai_videos" / "shikong_lvxing" / "sk2" / "7_bgm"
API = "https://api.elevenlabs.io/v1/music"

# (序号, 起镜, 止镜, 文件名 stem, 英文 prompt)
# prompt 逐条对应 casting.md §6.2 的「情绪 + 编制」，调式按 §6.1
# （自然小调与多利亚为主，教堂段转利底亚/混合利底亚）。
SEGMENTS = [
    (1, 1, 2, "01_opening_aerial",
     "Cinematic orchestral opening for an aerial approach to a walled stone city at dawn. "
     "Sustained string bed, a single French horn stating a noble main theme, harp arpeggios "
     "underneath. Wide, open, with a held breath of first sight. Natural minor, slow build, "
     "no percussion. Fully instrumental, no vocals, no lyrics, no choir."),
    (2, 3, 7, "02_valley_of_heroes",
     "Solemn but not heavy orchestral cue. The main theme restated on low strings, soft timpani, "
     "restrained brass. A procession past colossal statues. Dorian mode, steady pulse, dignified. "
     "Fully instrumental, no vocals, no lyrics."),
    (3, 8, 13, "03_trade_district",
     "Bright British folk dance in a busy market square. Tin whistle lead, fiddle, cittern, "
     "bodhran driving a light jig. The most alive cue of the piece. Dorian mode, up-tempo, "
     "warm and unpolished, played by real people in a square. "
     "Fully instrumental, no vocals, no lyrics."),
    (4, 14, 19, "04_canal_to_oldtown",
     "Relaxed turning pensive. Solo fiddle over plucked strings, then the drum drops out entirely "
     "and only the fiddle and a sparse pizzicato remain as the streets narrow. Natural minor, "
     "slow, intimate, slightly melancholy. Fully instrumental, no vocals, no lyrics."),
    (5, 20, 22, "05_throne_room",
     "Almost no music. One extremely quiet sustained string pad, barely above silence, no melody, "
     "no movement, no resolution. Nothing should tell the listener how to feel. "
     "Fully instrumental, no vocals, no lyrics, no percussion, no swell."),
    (6, 23, 24, "06_dwarven_forges",
     "Heavy working cue. Low percussion and struck anvil on the beat, bass strings underneath, "
     "the rhythm of hammer on iron. Industrious, weighty, unhurried. Natural minor. "
     "Fully instrumental, no vocals, no lyrics."),
    (7, 25, 29, "07_tram_mechanical",
     "Mechanical wonder. A regular low-frequency pulse standing in for wheel rhythm, metallic "
     "textures, widening sense of scale as the tunnel opens. Minimal, hypnotic, building. "
     "Fully instrumental, no vocals, no lyrics."),
    (8, 30, 31, "08_underwater",
     "All percussion drops away. Only a diffuse glockenspiel shimmer and a deep low drone remain, "
     "as if the air had been replaced by water: long reverb, high frequencies eaten away. "
     "Awe, suspension, no pulse. Fully instrumental, no vocals, no lyrics."),
    (9, 32, 34, "09_cathedral",
     "Reverent cathedral cue. Pipe organ and wordless choir on open vowels only, no intelligible "
     "words in any language. Lydian colour, broad and slow, deep stone reverb. "
     "Instrumental with wordless vowel choir only, no lyrics, no words."),
    (10, 35, 36, "10_moonwell",
     "The most beautiful cue of the piece. No rhythm at all: an ambient bed, a wordless female "
     "vowel hum, harp harmonics, and a slow bloom at sunset backlight. Mixolydian, weightless, "
     "luminous. Instrumental with wordless vowel humming only, no lyrics, no words."),
    (11, 37, 39, "11_mage_quarter",
     "Unresolved and waiting. High sustained strings holding a suspension that never lands, sparse "
     "celesta points, then everything strips back to a bare low drone for the cellar. "
     "Quiet unease, no resolution. Fully instrumental, no vocals, no lyrics."),
    (12, 40, 44, "12_night_and_return",
     "Winding down, then the opening theme returns. Double bass pizzicato and solo fiddle for the "
     "night canal; the music finishes cleanly before the candle is blown out. Then one full "
     "statement of the main theme on French horn at first light, ending on harp alone. "
     "Natural minor to major, unhurried. Fully instrumental, no vocals, no lyrics."),
]


def shot_durations() -> dict[int, int]:
    spec = importlib.util.spec_from_file_location("g", REPO / "tools" / "gen_shots_sk2.py")
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return {int(s["id"][1:]): int(s["d"]) for s in g.SHOTS}


def api_key() -> str:
    env = REPO / ".env"
    for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("ELEVENLABS_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("没在根 .env 找到 ELEVENLABS_API_KEY")


def compose(key: str, prompt: str, ms: int, dst: Path) -> str:
    # 实测 2026-09-20：`seed` **不能与 `prompt` 同用**（422 `seed` cannot be used with `prompt`）——
    # 它只服务于 `composition_plan` 那条路。所以走简单 prompt 时**没有可复现的种子**，
    # 不满意只能重跑碰运气；真要可复现就得改走 composition_plan。
    body = json.dumps({
        "prompt": prompt,
        "music_length_ms": ms,
        "force_instrumental": True,   # casting.md §6.3「无词」
    }).encode()
    req = urllib.request.Request(
        API + "?output_format=mp3_44100_128", data=body, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}：{e.read()[:220].decode('utf-8', 'replace')}"
    if len(data) < 10_000:
        return f"返回过小（{len(data)} B），疑似不是音频：{data[:160]!r}"
    dst.write_bytes(data)
    return f"OK {len(data)//1024} KB"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="逗号分隔的段号，如 5,9")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    dur = shot_durations()
    keep = {int(x) for x in args.only.split(",") if x.strip().isdigit()}
    key = "DRY" if args.dry_run else api_key()

    ok = fail = 0
    for idx, a, b, stem, prompt in SEGMENTS:
        if keep and idx not in keep:
            continue
        dst = OUT / f"{stem}.mp3"
        if dst.exists() and not args.force:
            print(f"· {stem} 已存在，跳过")
            continue
        secs = sum(dur.get(n, 0) for n in range(a, b + 1))
        # 留 2 s 余量给淡入淡出；API 的下限是 3 s、上限 600 s
        ms = max(3000, min(600_000, (secs + 2) * 1000))
        if args.dry_run:
            print(f"[dry] {stem}  S{a:02d}–S{b:02d}  {secs}s → {ms} ms\n      {prompt[:110]}…")
            ok += 1
            continue
        print(f"→ {stem}  S{a:02d}–S{b:02d}  {secs}s", flush=True)
        res = compose(key, prompt, ms, dst=dst)
        print(f"  {res}", flush=True)
        ok += res.startswith("OK")
        fail += not res.startswith("OK")

    print(f"\n合计：成功 {ok} · 失败 {fail}　落点 {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
