# -*- coding: utf-8 -*-
"""后期试做（声音、字幕、地名字卡，ai_video_management follow-up 283）：在集级剪辑成片上叠后期，出一版看效果。

    python tools/episode_post.py <后期决定.json>        # 出成片、.srt 与回读报告

声音与音乐、成片交付两个模块还是待设计（.agents/skills/ai-videos-pipeline/modules/sound.md），本工具只是用户要求的
best-effort 试做，不是锁片后的正式后期；做法随模块设计再定。

后期决定 `{集}/post/trial/post_v{N}.json`：
    source_cut   集级剪辑决定（相对集目录），用它的成片与各场 / 各条的入出点算时间
    sound        dialogue_pad（台词前后各留几秒）、dialogue_ramp（淡入淡出）、original_outside_dialogue_db（每场台词之外的原声增益）、
                 dialogue_db（台词区间内原声再加几 dB，默认 0）、dialogue_comp {threshold_db, ratio, makeup}（原声压缩，默认 -24 / 2.5 / 1）、
                 beds（每场环境声：rain / wind / river → dB，ffmpeg 合成；键以 .wav 结尾的是音频文件，路径相对本决定，
                 不够长就循环）、bed_crossfade
                 music[]（配乐，follow-up 289）{path, scene, offset, db, duck_db, fade_in, fade_out, skip?, length?}：从该场开头 + offset
                 进来，文件从 skip 秒处开始放，长度默认到文件结尾；台词区间内再压低 duck_db
    subtitles[]  {scene, shot, from, to, en, zh}：from / to 是这一条台词首尾的词，按条目录 annotation.json 的逐词时间对上
    titles[]     {scene, offset, duration, kicker, zh, en}：到达大场景时的地名字卡，offset 从该场开头算
    spec         loudness_lufs / true_peak_db（两遍 loudnorm）、audio_rate
产物同目录 `{集}_post_v{N}.mp4`、`.srt`（中英双语）与回读写回决定的 output 段（不进 git 的只有 mp4）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.scene_cut import ff, probe, sha256

FONT_ZH_TITLE = "C:/Windows/Fonts/NotoSerifSC-VF.ttf"
FONT_EN_TITLE = "C:/Windows/Fonts/PERTILI.TTF"
FONT_SUB = "C:/Windows/Fonts/msyh.ttc"
GOLD = (226, 196, 138)
BEDS = {   # 合成环境声：lavfi 片段（{seed} 左右声道不同，听起来有宽度）
    "rain": "anoisesrc=c=pink:a=0.5:seed={seed},highpass=f=500,lowpass=f=7000",
    "wind": "anoisesrc=c=brown:a=0.7:seed={seed},lowpass=f=450,tremolo=f=0.13:d=0.6",
    "river": "anoisesrc=c=white:a=0.4:seed={seed},bandpass=f=900:width_type=h:w=1500,tremolo=f=0.7:d=0.35,lowpass=f=3200",
}


def norm(w: str) -> str:
    return re.sub(r"[^a-z']", "", w.lower().replace("’", "'"))


# ---------- 时间线 ----------

def timeline(ep: Path, cut: dict) -> tuple[dict, list[dict]]:
    """(场 → {start, dur}, 镜头事件[{scene, shot, take_dir, in, out, start}])；场间转场按集级决定扣掉重叠。"""
    from tools.episode_cut import MENU
    scenes, events, t = {}, [], 0.0
    for k, item in enumerate(cut["scenes"]):
        if k:
            tr = cut["transitions"][k - 1]
            t -= tr.get("duration", 0) if MENU[tr["type"]][1] else 0
        sc = json.loads((ep / "scenes" / item["scene"] / "edit" / cut["stage"] / ("cut_v%s.json" % item["cut_version"])).read_text(encoding="utf-8"))
        x = t
        for ev in sc["events"]:
            d = ev["duration"] if ev.get("placeholder") else ev["out"] - ev["in"]
            if not ev.get("placeholder"):
                events.append({"scene": item["scene"], "shot": ev["shot"], "in": ev["in"], "out": ev["out"], "start": x,
                               "take_dir": ep / "scenes" / item["scene"] / "shots" / ev["shot"] / "renders" / ev["take"]})
            x += d
        scenes[item["scene"]] = {"start": t, "dur": x - t}
        t = x
    return scenes, events


def subtitle_times(subs: list[dict], events: list[dict]) -> list[dict]:
    """每条字幕按首尾词在条里的逐词时间对上，换算到成片时间；同一镜里按顺序往后找。"""
    out, cursor = [], {}
    for s in subs:
        ev = next((e for e in events if e["scene"] == s["scene"] and e["shot"] == s["shot"]), None)
        if not ev:
            raise SystemExit("字幕「%s」：剪辑里没有 %s %s" % (s["en"], s["scene"], s["shot"]))
        words = [w for w in json.loads((ev["take_dir"] / "annotation.json").read_text(encoding="utf-8"))["words"]
                 if w["s"] >= ev["in"] - 0.05 and w["e"] <= ev["out"] + 0.05]
        key = (s["scene"], s["shot"])
        i = cursor.get(key, 0)
        a = next((j for j in range(i, len(words)) if norm(words[j]["w"]) == norm(s["from"])), None)
        b = next((j for j in range(a, len(words)) if norm(words[j]["w"]) == norm(s["to"])), None) if a is not None else None
        if a is None or b is None:
            raise SystemExit("字幕「%s」：在 %s %s 的逐词时间里找不到 %s…%s" % (s["en"], s["scene"], s["shot"], s["from"], s["to"]))
        cursor[key] = b + 1
        off = ev["start"] - ev["in"]
        out.append(dict(s, start=round(words[a]["s"] + off, 3), end=round(words[b]["e"] + off, 3)))
    # 最短 1.2 秒、不和下一条重叠（留 0.08 秒）
    for k, s in enumerate(out):
        nxt = out[k + 1]["start"] - 0.08 if k + 1 < len(out) else s["end"] + 2
        s["show_start"] = s["start"]
        s["show_end"] = round(min(max(s["end"] + 0.3, s["start"] + 1.2), nxt), 3)
    return out


# ---------- 画面：字幕与字卡（PIL 出透明 PNG，ffmpeg 叠上去）----------

def _spaced(d, xy, text, font, fill, spacing, anchor_center_w=None):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (anchor_center_w - total) / 2 if anchor_center_w else xy[0]
    for ch, w in zip(text, widths):
        d.text((x, xy[1]), ch, font=font, fill=fill)
        x += w + spacing
    return total


def title_png_zone(t: dict, W: int, H: int, out: Path) -> None:
    """英文版地名字卡（style＝zone）：像游戏里进入新区域时的地名提示——金黄大写地名、下面一行较小的上一级地区，
    深色描边加柔和投影，画面中上方。font / sub_font 可在决定里换（默认本机 Perpetua Titling Bold / Regular）。"""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    scale = t.get("scale", 1.0)
    main = ImageFont.truetype(t.get("font", "C:/Windows/Fonts/PERTIBD.TTF"), int(54 * scale))
    sub = ImageFont.truetype(t.get("sub_font", FONT_EN_TITLE), int(26 * scale))
    gold, pale = (255, 209, 64), (238, 222, 170)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    rows = [(t["en"], main, int(4 * scale), gold, int(3 * scale))]
    if t.get("en_sub"):
        rows.append((t["en_sub"], sub, int(5 * scale), pale, int(2 * scale)))
    def width(text, font, sp):
        return sum(tmp.textlength(c, font=font) for c in text) + sp * (len(text) - 1)
    hs = [r[1].getbbox(r[0])[3] - r[1].getbbox(r[0])[1] for r in rows]
    gap = int(16 * scale)
    cx, cy = t.get("pos", [0.5, 0.2])
    y = cy * H - (sum(hs) + gap * (len(rows) - 1)) / 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for (text, font, sp, col, stroke), h in zip(rows, hs):
        top = font.getbbox(text)[1]
        x = cx * W - width(text, font, sp) / 2
        for ch in text:
            sd.text((x + 2, y - top + 3), ch, font=font, fill=(0, 0, 0, 170), stroke_width=stroke + 2, stroke_fill=(0, 0, 0, 170))
            d.text((x, y - top), ch, font=font, fill=col + (255,), stroke_width=stroke, stroke_fill=(28, 18, 6, 235))
            x += tmp.textlength(ch, font=font) + sp
        y += h + gap
    im = Image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4 * scale)), im)
    im.save(out)


def title_png(t: dict, W: int, H: int, out: Path) -> None:
    if t.get("style") == "zone":
        return title_png_zone(t, W, H, out)
    """地名字卡：小字副题（上一级地名）→ 中文地名（思源宋体、金色、宽字距）→ 两端渐隐的细线 → 英文（Perpetua Titling 罗马大写）。
    pos＝字卡中心在画面里的位置（宽、高的比例），按每场画面里空着的地方定；行距按实际字高排，不会叠字。"""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    scale = t.get("scale", 1.0)
    zh = ImageFont.truetype(FONT_ZH_TITLE, int(62 * scale))
    try:
        zh.set_variation_by_name("SemiBold")
    except Exception:
        pass
    kick = ImageFont.truetype(FONT_ZH_TITLE, int(26 * scale))
    en = ImageFont.truetype(FONT_EN_TITLE, int(22 * scale))
    rows = [(t.get("kicker", ""), kick, int(9 * scale), 235), (t["zh"], zh, int(18 * scale), 255), (t["en"], en, int(8 * scale), 240)]
    gaps = [int(12 * scale), int(30 * scale)]          # 副题↔地名，地名↔英文（中间放细线）
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    def size(text, font, sp):
        if not text:
            return 0, 0, 0
        top, bot = font.getbbox(text)[1], font.getbbox(text)[3]
        return sum(tmp.textlength(c, font=font) for c in text) + sp * (len(text) - 1), top, bot
    dims = [size(r[0], r[1], r[2]) for r in rows]
    heights = [d[2] - d[1] for d in dims]
    block_h = sum(heights) + sum(gaps)
    cx, cy = t.get("pos", [0.5, 0.4])
    y = cy * H - block_h / 2
    ys = []
    for k, h in enumerate(heights):
        ys.append(y); y += h + (gaps[k] if k < len(gaps) else 0)
    def draw(d, alpha_mul, fill_rgb):
        for (text, font, sp, a), (w, top, _), yy in zip(rows, dims, ys):
            if not text:
                continue
            x = cx * W - w / 2
            for ch in text:
                d.text((x, yy - top), ch, font=font, fill=fill_rgb + (int(a * alpha_mul),))
                x += tmp.textlength(ch, font=font) + sp
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw(ImageDraw.Draw(shadow), 0.8, (0, 0, 0))
    im = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), shadow.filter(ImageFilter.GaussianBlur(5 * scale)))
    d = ImageDraw.Draw(im)
    draw(d, 1.0, GOLD)
    lw, ly = int(max(dims[1][0], dims[2][0]) * 0.9), int(ys[1] + heights[1] + gaps[1] / 2)
    for i in range(lw):
        a = int(210 * (1 - abs(i - lw / 2) / (lw / 2)))
        d.point((int(cx * W - lw / 2) + i, ly), fill=GOLD + (a,))
    im.save(out)


def subtitle_png(s: dict, W: int, H: int, out: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fz, fe = ImageFont.truetype(FONT_SUB, 34), ImageFont.truetype(FONT_SUB, 22)
    lines = ((s["zh"], fz, H - 112), (s["en"], fe, H - 64)) if s.get("zh") else ((s["en"], ImageFont.truetype(FONT_SUB, 32), H - 82),)
    for text, font, y in lines:
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, y), text, font=font, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 200))
    im.save(out)


def srt(subs: list[dict]) -> str:
    def ts(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
        return "%02d:%02d:%02d,%03d" % (h, m, s, ms)
    return "".join("%d\n%s --> %s\n%s\n\n" % (i + 1, ts(s["show_start"]), ts(s["show_end"]),
                   "\n".join(x for x in (s.get("zh"), s["en"]) if x)) for i, s in enumerate(subs))


# ---------- 声音 ----------

def gain_expr(spans: list[tuple[float, float]], scene_gain: list[tuple[float, float, float]], ramp: float, inside: float = 1.0) -> str:
    """volume 表达式：台词区间内 inside（默认 1），区间外按场的增益；区间两端 ramp 秒线性过渡。"""
    on = "+".join("clip(min((t-%.3f)/%.3f\\,(%.3f-t)/%.3f)\\,0\\,1)" % (a - ramp, ramp, b + ramp, ramp) for a, b in spans) or "0"
    base = "+".join("between(t\\,%.3f\\,%.3f)*%.5f" % (a, b, g) for a, b, g in scene_gain) or "1"
    head = "min(1\\,(%s))" % on if inside == 1 else "%.5f*min(1\\,(%s))" % (inside, on)
    return "%s+(1-min(1\\,(%s)))*(%s)" % (head, on, base)


def duck_expr(spans: list[tuple[float, float]], duck_db: float, ramp: float) -> str:
    """volume 表达式：台词区间内压低 duck_db，区间外 1；两端 ramp 秒过渡（配乐给台词让路）。"""
    on = "+".join("clip(min((t-%.3f)/%.3f\\,(%.3f-t)/%.3f)\\,0\\,1)" % (a - ramp, ramp, b + ramp, ramp) for a, b in spans) or "0"
    return "1-%.5f*min(1\\,(%s))" % (1 - 10 ** (duck_db / 20), on)


def run(path: Path) -> None:
    post = json.loads(path.read_text(encoding="utf-8"))
    ep = path.parent.parent.parent
    cut_path = ep / post["source_cut"]
    cut = json.loads(cut_path.read_text(encoding="utf-8"))
    src = cut_path.parent / cut["output"]["path"]
    if sha256(src) != cut["output"]["sha256"]:
        raise SystemExit("集级剪辑成片与决定里记的 sha256 不一致：先重跑 episode_cut.py join")
    pr = probe(src); v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    W, H, total = v["width"], v["height"], float(pr["format"]["duration"])
    sp, snd = post["spec"], post["sound"]
    scenes, events = timeline(ep, cut)
    subs = subtitle_times(post["subtitles"], events)
    if post.get("subtitle_lang") == "en":          # 英文版：只出英文字幕
        subs = [dict(s, zh="") for s in subs]
    tmp = Path(tempfile.mkdtemp(prefix="post_"))
    # 声音 1：原声（台词保留，台词外按场压低），清理
    pad0, pad1 = snd["dialogue_pad"]
    spans = []
    for s in subs:
        a, b = s["start"] - pad0, s["end"] + pad1
        if spans and a <= spans[-1][1]:
            spans[-1] = (spans[-1][0], max(spans[-1][1], b))
        else:
            spans.append((a, b))
    # 场间 J 剪辑：下一场的原声提前 j 秒进来，那几秒按下一场的增益算（例如 s2 原声整段静音，提前进来的部分也静音）
    lead = {tr["to"]: (tr.get("audio") or {}).get("j", 0) for tr in cut.get("transitions", [])}
    sg = []
    for k in scenes:
        a, b = scenes[k]["start"] - lead.get(k, 0), scenes[k]["start"] + scenes[k]["dur"]
        if sg and a < sg[-1][1]:
            sg[-1] = (sg[-1][0], a, sg[-1][2])
        sg.append((a, b, 10 ** (snd["original_outside_dialogue_db"].get(k, 0) / 20)))
    orig = tmp / "orig.wav"
    comp = snd.get("dialogue_comp", {})
    (tmp / "orig.txt").write_text(
        "[0:a]aresample=%d,highpass=f=80,afftdn=nf=-28,acompressor=threshold=%sdB:ratio=%s:attack=8:release=120:makeup=%s,"
        "volume=eval=frame:volume='%s'[o]" % (sp["audio_rate"], comp.get("threshold_db", -24), comp.get("ratio", 2.5), comp.get("makeup", 1),
                                              gain_expr(spans, sg, snd["dialogue_ramp"], 10 ** (snd.get("dialogue_db", 0) / 20))), encoding="utf-8")
    ff(["-i", str(src), "-/filter_complex", str(tmp / "orig.txt"), "-map", "[o]", "-ac", "2", "-c:a", "pcm_s16le", str(orig), "-y"])
    # 声音 2：每场环境声床，场与场之间交叉淡化
    xf = snd["bed_crossfade"]
    bed_inputs, fc, labels = ["-i", str(orig)], [], ["[0:a]"]
    n = 1
    for k, rec in snd["beds"].items():
        if k not in scenes:
            continue
        a = max(0.0, scenes[k]["start"] - xf / 2); b = min(total, scenes[k]["start"] + scenes[k]["dur"] + xf / 2)
        for kind, db in rec.items():
            if kind.endswith(".wav"):      # 生成或录制的环境声文件：不够长就循环
                bed_inputs += ["-stream_loop", "-1", "-t", "%.3f" % (b - a), "-i", str((path.parent / kind).resolve())]
                fc.append("[%d:a]aresample=%d,aformat=channel_layouts=stereo,volume=%.1fdB,afade=t=in:d=%.2f,afade=t=out:st=%.3f:d=%.2f,adelay=%d|%d[b%d]"
                          % (n, sp["audio_rate"], db, xf, b - a - xf, xf, int(a * 1000), int(a * 1000), n))
                labels.append("[b%d]" % n); n += 1
                continue
            for ch, seed in (("L", n * 7 + 1), ("R", n * 7 + 3)):
                bed_inputs += ["-f", "lavfi", "-t", "%.3f" % (b - a), "-i", BEDS[kind].format(seed=seed) + ",aresample=%d" % sp["audio_rate"]]
            fc.append("[%d:a][%d:a]join=inputs=2:channel_layout=stereo,volume=%.1fdB,afade=t=in:d=%.2f,afade=t=out:st=%.3f:d=%.2f,adelay=%d|%d[b%d]"
                      % (n, n + 1, db, xf, b - a - xf, xf, int(a * 1000), int(a * 1000), n))
            labels.append("[b%d]" % n); n += 2
    # 声音 2b：配乐，台词区间内再压低
    for mu in snd.get("music", []):
        f = (path.parent / mu["path"]).resolve()
        a = max(0.0, scenes[mu["scene"]]["start"] + mu.get("offset", 0))
        sk = mu.get("skip", 0)
        du = min(mu.get("length") or float(probe(f)["format"]["duration"]) - sk, total - a)
        bed_inputs += ["-ss", "%.3f" % sk, "-t", "%.3f" % du, "-i", str(f)]
        fc.append("[%d:a]aresample=%d,aformat=channel_layouts=stereo,volume=%.1fdB,afade=t=in:d=%.2f,afade=t=out:st=%.3f:d=%.2f,adelay=%d|%d,"
                  "volume=eval=frame:volume='%s'[b%d]"
                  % (n, sp["audio_rate"], mu["db"], mu.get("fade_in", 1.0), du - mu.get("fade_out", 1.5), mu.get("fade_out", 1.5),
                     int(a * 1000), int(a * 1000), duck_expr(spans, mu.get("duck_db", 0), snd["dialogue_ramp"] * 2), n))
        labels.append("[b%d]" % n); n += 1
    fc.append("".join(labels) + "amix=inputs=%d:normalize=0:duration=first[m]" % len(labels))
    (tmp / "mix.txt").write_text(";".join(fc), encoding="utf-8")
    mix = tmp / "mix.wav"
    ff([*bed_inputs, "-/filter_complex", str(tmp / "mix.txt"), "-map", "[m]", "-c:a", "pcm_s16le", str(mix), "-y"])
    # 声音 3：两遍 loudnorm 到目标响度与真峰值
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", ff(["-i", str(mix), "-af", "loudnorm=I=%s:TP=%s:LRA=11:print_format=json"
                                                     % (sp["loudness_lufs"], sp["true_peak_db"]), "-f", "null", "-"]), re.S)
    meas = json.loads(m.group(0))
    final_a = tmp / "final.wav"
    ff(["-i", str(mix), "-af", "loudnorm=I=%s:TP=%s:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true,aresample=%d"
        % (sp["loudness_lufs"], sp["true_peak_db"], meas["input_i"], meas["input_tp"], meas["input_lra"], meas["input_thresh"],
           meas["target_offset"], sp["audio_rate"]), "-c:a", "pcm_s16le", str(final_a), "-y"])
    # 画面：字卡与字幕 PNG 叠加（字卡淡入淡出，字幕硬进硬出）
    ins, vf, k = ["-i", str(src), "-i", str(final_a)], [], 2
    cur = "[0:v]"
    for i, t in enumerate(post["titles"]):
        png = tmp / ("title%d.png" % i); title_png(t, W, H, png)
        st = scenes[t["scene"]]["start"] + t["offset"]; du = t["duration"]
        ins += ["-loop", "1", "-t", "%.3f" % du, "-i", str(png)]
        vf.append("[%d:v]format=rgba,fade=t=in:st=0:d=0.9:alpha=1,fade=t=out:st=%.3f:d=1.1:alpha=1,setpts=PTS+%.3f/TB[t%d]" % (k, du - 1.1, st, i))
        vf.append("%s[t%d]overlay=0:0:enable='between(t,%.3f,%.3f)'[v%d]" % (cur, i, st, st + du, k)); cur = "[v%d]" % k; k += 1
    for i, s in enumerate(subs):
        png = tmp / ("sub%02d.png" % i); subtitle_png(s, W, H, png)
        du = s["show_end"] - s["show_start"]
        ins += ["-loop", "1", "-t", "%.3f" % du, "-i", str(png)]
        vf.append("[%d:v]format=rgba,setpts=PTS+%.3f/TB[s%d]" % (k, s["show_start"], i))
        vf.append("%s[s%d]overlay=0:0:enable='between(t,%.3f,%.3f)'[v%d]" % (cur, i, s["show_start"], s["show_end"], k)); cur = "[v%d]" % k; k += 1
    (tmp / "v.txt").write_text(";".join(vf), encoding="utf-8")
    out = path.parent / ("%s_post_v%s.mp4" % (ep.name, post["version"]))
    ff([*ins, "-/filter_complex", str(tmp / "v.txt"), "-map", cur, "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out), "-y"])
    srt_path = out.with_suffix(".srt"); srt_path.write_text(srt(subs), encoding="utf-8")
    # 回读
    pr2 = probe(out); dur = float(pr2["format"]["duration"])
    lu = ff(["-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"])
    post["output"] = {"rendered_at": datetime.now().isoformat(timespec="seconds"), "path": out.name, "sha256": sha256(out),
                      "srt": srt_path.name, "source_sha256": cut["output"]["sha256"], "duration_s": round(dur, 3),
                      "duration_ok": abs(dur - total) < 0.25,
                      "loudness_lufs": float(re.findall(r"I:\s+(-?[\d.]+) LUFS", lu)[-1]),
                      "true_peak_db": float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lu)[-1]),
                      "subtitles": [{"start": s["show_start"], "end": s["show_end"], "text": s.get("zh") or s["en"]} for s in subs]}
    path.write_text(json.dumps(post, ensure_ascii=False, indent=1), encoding="utf-8")
    o = post["output"]
    print(out, o["duration_s"], "s", "时长对" if o["duration_ok"] else "时长不对", "响度", o["loudness_lufs"], "LUFS 真峰值", o["true_peak_db"], "dBFS")
    print("字幕 %d 条，字卡 %d 张" % (len(subs), len(post["titles"])))


def main() -> None:
    ap = argparse.ArgumentParser(description="后期试做：声音、字幕、地名字卡")
    ap.add_argument("post")
    run(Path(ap.parse_args().post))


if __name__ == "__main__":
    main()
