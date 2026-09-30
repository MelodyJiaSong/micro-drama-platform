# -*- coding: utf-8 -*-
"""align.py 的纯函数自测（不加载模型、不读媒体）：python tools/post/tests/test_align.py
norm_words 用 whisper 的 EnglishTextNormalizer：当前解释器没有 whisper 就换 pc.ALIGN_PYTHON 重跑本文件。"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import align  # noqa: E402
import post_common as pc  # noqa: E402


def _line(kind: str = "正常台词", t0: float = 0.0, t1: float = 2.0, text: str = "Thank you, Eagan.") -> pc.Line:
    return pc.Line("Aaron", kind, text, "谢谢你，伊根。", t0, t1, None)


def _w(w: str, s: float, e: float) -> dict:
    return {"w": w, "s": s, "e": e, "p": 0.9}


def test_wer() -> None:
    assert align.norm_words("Duke! Duke the Unbre— ow!") == ["duke", "duke", "the", "unbre", "ow"]
    assert align.norm_words("Oof. It didn't even feel that.") == ["oof", "it", "did", "not", "even", "feel", "that"]
    ref = align.norm_words("Kobolds first. Then wolves!")
    assert align.wer(ref, ref) == 0.0
    assert align.wer(ref, align.norm_words("Cobbles first, then wolves.")) == 0.25
    assert align.wer(ref, align.norm_words("Kobolds first, then the wolves")) == 0.25
    assert align.wer(ref, []) == 1.0
    assert align.wer([], []) == 0.0
    assert align.wer([], ["thank", "you"]) == 2.0
    # EnglishTextNormalizer：数词写成数字、缩写拆开都不算错
    assert align.wer(align.norm_words("Twelve bandanas. Easy."), align.norm_words("12 bandanas, easy.")) == 0.0
    assert align.wer(align.norm_words("Oof. It didn't even feel that."), align.norm_words("Oof, it did not even feel that.")) == 0.0
    # 逐词归一：整句归一会把数数并成一个数（台词 '1234567 8 9 10 11'、ASR '1234567891011'，整句算错）
    count = "One, two, three, four, five, six, seven... eight... nine... ten... ...eleven."
    assert align.norm_words(count) == ["one", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    assert align.wer(align.norm_words(count), align.norm_words("One, two, three, four, five, six, seven, eight, nine, ten, eleven.")) == 0.0
    assert align.norm_words("... — Hmm.") == []


def test_line_status() -> None:
    ok = align.line_record(1, _line(), [(" Thank", 1.0, 1.2, 0.9), (" you,", 1.2, 1.4, 0.8), (" Eagan.", 1.5, 1.9, 0.7)])
    assert (ok["status"], ok["start"], ok["end"], ok["conf"]) == ("ok", 1.0, 1.9, 0.8)
    assert [w["w"] for w in ok["words"]] == ["Thank", "you,", "Eagan."]
    low = align.line_record(2, _line(), [(" Thank", 1.0, 1.2, 0.3), (" you,", 1.2, 1.4, 0.4), (" Eagan.", 1.5, 1.9, 0.5)])
    assert low["status"] == "low_conf"
    # shot05 实测：被挪了语序的一句挤在 40 ms 里，概率却高——按零时长词过半判 missing
    moved = align.line_record(8, _line(t0=24.6, t1=26.0, text="Dad's boots are fine."),
                              [(" Dad's", 27.30, 27.34, 0.49), (" boots", 27.34, 27.34, 1.0),
                               (" are", 27.34, 27.34, 0.99), (" fine.", 27.34, 27.34, 0.98)])
    assert (moved["status"], moved["start"], moved["end"], moved["words"]) == ("missing", 24.6, 26.0, [])
    # 同镜「It」没说（ASR：Oof, didn't even feel that.）：6 词 1 个零时长，仍是 ok，起止取有时长的词
    part = align.line_record(4, _line(text="Oof. It didn't even feel that."),
                             [(" Oof.", 12.72, 12.82, 0.54), (" It", 13.14, 13.14, 0.0), (" didn't", 13.14, 13.28, 1.0),
                              (" even", 13.28, 13.44, 1.0), (" feel", 13.44, 13.68, 0.99), (" that.", 13.68, 14.68, 0.92)])
    assert (part["status"], part["start"], part["end"], len(part["words"])) == ("ok", 12.72, 14.68, 6)
    off = align.line_record(4, _line(kind="画外", t0=3.0, t1=5.0), None)
    assert (off["status"], off["start"], off["end"], off["conf"], off["words"]) == ("offscreen", 3.0, 5.0, None, [])
    punct = align.line_record(5, _line(), [(" Meat", 1.0, 1.3, 0.9), (" —", 1.3, 1.4, 0.0), (" fair's", 1.4, 1.7, 0.9)])
    assert punct["conf"] == 0.9 and [w["w"] for w in punct["words"]] == ["Meat", "fair's"]
    assert align.line_record(6, _line(), [])["status"] == "missing"


def test_onscreen() -> None:
    # 画内 / 不动嘴只在 pc.onscreen 判：括注不影响（shikong_lvxing / wushen_juexing 的写法），没写类型按正常台词
    assert pc.onscreen("正常台词") and pc.onscreen("正常台词（对镜说话，口型对林问）") and pc.onscreen("正常台词(对口型)")
    assert pc.onscreen("")
    for k in ("内心独白", "画外", "系统提示音", "内心独白（画外，嘴唇不动）", "画外（画外，嘴唇不动）", "系统提示音(嘴唇不动)"):
        assert not pc.onscreen(k), k
    assert not pc.onscreen("对镜")          # 不认识的类型按不动嘴（要后期配，缺 TTS 时 finish_ep 报错）并警告
    assert pc.base_kind("内心独白（OS·嘴唇不动）") == "内心独白" and pc.base_kind("  ") == "正常台词"


def test_silences() -> None:
    err = "\n".join(["[silencedetect @ 0] silence_start: -2.08333e-05",
                     "[silencedetect @ 0] silence_end: 0.8 | silence_duration: 0.8",
                     "[silencedetect @ 0] silence_start: 2.5",
                     "[silencedetect @ 0] silence_end: 3.25 | silence_duration: 0.75",
                     "[silencedetect @ 0] silence_start: 5.9"])
    assert pc.silences(err, 6.0) == [(0.0, 0.8), (2.5, 3.25), (5.9, 6.0)]
    assert pc.silences("", 6.0) == []


def test_trim_edges() -> None:
    # shot01 #4 实测：句尾「one.」被对齐拖到 17.82，ASR 听到的同一个词止于 15.46
    words = [_w("...I", 14.52, 14.62), _w("want", 14.62, 14.76), _w("be", 15.16, 15.28), _w("one.", 15.28, 17.82)]
    heard = [("I", 14.5, 14.6), ("want", 14.6, 14.8), ("be", 15.1, 15.3), ("one.", 15.3, 15.46)]
    got = align.trim_edges(words, heard)
    assert (got[0]["s"], got[-1]["s"], got[-1]["e"]) == (14.52, 15.28, 15.46)   # 只缩不扩；句中的边不动
    assert words[-1]["e"] == 17.82                                                # 不改入参
    # 句首被拖长（shot05「I」8.56–10.32）：收到 ASR 的起
    got = align.trim_edges([_w("I", 8.56, 10.32), _w("hate", 10.32, 10.5)], [("I", 10.1, 10.3), ("hate", 10.3, 10.5)])
    assert (got[0]["s"], got[0]["e"]) == (10.1, 10.32)
    # 不是同一个词（Kobolds / Cobbles）、时间不交叠、ASR 词零时长、ASR 的词更宽：都不动
    base = [_w("Kobolds", 22.74, 24.5), _w("path.", 24.86, 25.14)]
    assert align.trim_edges(base, [("Cobbles", 24.2, 24.5), ("path.", 26.0, 26.3)]) == base
    assert align.trim_edges(base, [("path.", 25.0, 25.0)]) == base
    assert align.trim_edges(base, [("Kobolds", 22.0, 24.9), ("path", 24.5, 25.9)]) == base
    # 一词句两头都收
    assert align.trim_edges([_w("Hey!", 3.0, 5.0)], [("hey", 3.2, 3.6)]) == [_w("Hey!", 3.2, 3.6)]
    # shot05 #9 实测：句首「Thank」被挤成零时长（ASR 听到它在 27.26–27.40）——不去收「you,」，否则把 Thank 切掉
    thank = [_w("Thank", 27.34, 27.34), _w("you,", 27.34, 27.66), _w("Eagan.", 27.66, 27.86)]
    assert align.trim_edges(thank, [("Thank", 27.26, 27.4), ("you,", 27.4, 27.5), ("Egan.", 27.64, 27.8)]) == thank
    got = align.trim_edges([_w("I", 11.7, 11.7), _w("want", 11.7, 12.3)], [("I", 11.5, 11.6), ("want", 11.9, 12.1)])
    assert [(w["s"], w["e"]) for w in got] == [(11.7, 11.7), (11.7, 12.1)]
    # 同词多处交叠：取交叠最长的；数词按归一口径算同词
    got = align.trim_edges([_w("go", 4.0, 4.5), _w("to", 5.0, 6.0)], [("to", 4.0, 5.1), ("to", 5.2, 5.5)])
    assert got[-1]["e"] == 5.5
    assert align.trim_edges([_w("Twelve.", 1.0, 3.0)], [("12.", 1.1, 1.6)]) == [_w("Twelve.", 1.1, 1.6)]


def test_coverage() -> None:
    # shot01 #2 实测：台词 Aaron, sir. From Stormwind.，ASR 听成 Hi, I'm Arran from Stormhawk. → 只有 from 对上
    heard = [("Hi,", 7.9, 8.1), ("I'm", 8.2, 8.4), ("Arran", 8.5, 8.9), ("from", 9.9, 10.0), ("Stormhawk.", 10.0, 10.4)]
    assert align.coverage("Aaron, sir. From Stormwind.", 7.86, 10.32, heard) == 0.25
    # ±COVER_WIN：窗外听到的不算
    assert align.coverage("Thank you.", 5.0, 6.0, [("Thank", 3.8, 3.95), ("you.", 7.05, 7.4)]) == 0.0
    assert align.coverage("Thank you.", 5.0, 6.0, [("Thank", 3.9, 4.1), ("you.", 6.9, 7.2)]) == 1.0
    # 听到的每个词只抵一次；数词、缩写按归一口径比
    assert align.coverage("to be or not to be", 0.0, 2.0, [("to", 0.1, 0.2), ("be", 0.2, 0.3)]) == 0.333
    assert align.coverage("Twelve people. Can't stop!", 0.0, 2.0,
                          [("12", 0.1, 0.4), ("people.", 0.4, 0.8), ("Can", 0.9, 1.0), ("not", 1.0, 1.1), ("stop!", 1.1, 1.5)]) == 1.0
    assert align.coverage("Hmm...", 0.0, 1.0, []) is None


def test_settle() -> None:
    rec = align.line_record(4, _line(t0=14.0, t1=17.0, text="...I want to learn to be one."),
                            [(" ...I", 14.52, 14.62, 0.098), (" want", 14.62, 14.76, 0.85), (" to", 14.76, 14.86, 0.945),
                             (" learn", 14.86, 15.02, 0.66), (" to", 15.02, 15.16, 0.661), (" be", 15.16, 15.28, 0.984),
                             (" one.", 15.28, 17.82, 0.976)])
    assert (rec["status"], rec["end"]) == ("ok", 17.82)
    heard = [("I", 14.5, 14.6), ("want", 14.6, 14.76), ("to", 14.76, 14.86), ("learn", 14.86, 15.0),
             ("to", 15.0, 15.16), ("be", 15.16, 15.28), ("one.", 15.28, 15.46)]
    got = align.settle(rec, heard)
    assert (got["status"], got["start"], got["end"], got["cover"]) == ("ok", 14.52, 15.46, 1.0)
    assert align.speech_spans([got]) == [[14.52, 15.46]]
    # conf 过了、ASR 却几乎没听到 → low_conf（起止照对齐）
    rec2 = align.line_record(2, _line(t0=7.5, t1=10.5, text="Aaron, sir. From Stormwind."),
                             [(" Aaron,", 7.86, 8.84, 0.9), (" sir.", 8.84, 9.92, 0.9), (" From", 9.92, 10.0, 0.9),
                              (" Stormwind.", 10.0, 10.32, 0.9)])
    got2 = align.settle(rec2, [("Hi,", 7.9, 8.1), ("Arran", 8.5, 8.9), ("from", 9.9, 10.0), ("Stormhawk.", 10.0, 10.4)])
    assert (rec2["status"], got2["status"], got2["cover"], got2["start"], got2["end"]) == ("ok", "low_conf", 0.25, 7.86, 10.32)
    # 刚好 0.6 不降
    rec3 = align.line_record(3, _line(text="a b c d e"), [(f" {c}", i, i + 0.5, 0.9) for i, c in enumerate("abcde")])
    assert align.settle(rec3, [(c, i, i + 0.5) for i, c in enumerate("abc")])["status"] == "ok"
    # missing / offscreen 原样，cover 记 None
    off = align.line_record(5, _line(kind="画外", t0=3.0, t1=5.0), None)
    assert align.settle(off, heard) == off | {"cover": None}
    moved = align.line_record(8, _line(t0=24.6, t1=26.0, text="Dad's boots are fine."),
                              [(" Dad's", 27.30, 27.34, 0.49), (" boots", 27.34, 27.34, 1.0),
                               (" are", 27.34, 27.34, 0.99), (" fine.", 27.34, 27.34, 0.98)])
    assert align.settle(moved, [("Dad's", 25.0, 25.3)]) == moved | {"cover": None}


def test_speech_spans() -> None:
    recs = [{"status": "ok", "words": [{"s": 0.5, "e": 0.8}, {"s": 0.9, "e": 1.2}, {"s": 1.5, "e": 1.8}]},
            {"status": "offscreen", "words": []},
            {"status": "low_conf", "words": [{"s": 1.84, "e": 2.0}, {"s": 3.0, "e": 3.0}]}]
    assert align.speech_spans(recs) == [[0.5, 1.2], [1.5, 2.0]]


def test_pick_cuts() -> None:
    # shot06 实测（scdet 分）：5.800 真切 11.5 + 次帧余波 6.2；11.633 打斗 5.6；16.5 真切 7.0；21.25 计划外硬切 11.9
    hits = [(5.8, 11.49), (5.833, 6.2), (11.633, 5.609), (16.5, 6.956), (21.25, 11.915)]
    assert align.pick_cuts(hits, [6.0, 17.0]) == [5.8, 16.5, 21.25]
    assert align.pick_cuts(hits, []) == [5.8, 21.25]
    assert align.pick_cuts([(9.0, 7.0)], [10.0]) == []
    assert align.pick_cuts([(9.5, 7.0)], [10.0]) == [9.5]


def test_planned_cuts() -> None:
    md = "---\nshot: 05\n---\n```text\n镜头: 远景\n分镜: 0–7s 林缘远景推近，连续运镜｜7–18s【切】正面全景轻跟｜18–28s【切】树桩旁中景推成特写，" \
         "连续运镜。镜内硬切不加任何转场效果\n```\n\n```text\n分镜: 0–3s 不是设计稿｜3–5s【切】\n```\n"
    assert align.planned_cuts(md, 28.0) == [7.0, 18.0]
    assert align.planned_cuts("```text\n镜头: 中景\n```\n", 10.0) == []
    assert align.planned_cuts("```text\n分镜: 0–11.2s 甲｜11.2–17s【切】乙\n```\n", 17.0) == [11.0]


def test_stale() -> None:
    lines = [_line()]
    want = align.inputs(lines)
    rec = {"version": align.VERSION, "model": "medium.en", "lines": [align.line_record(1, lines[0], None)],
           "cuts": {"planned": [7.0]}}
    assert align.stale(rec, "medium.en", want, [7.0]) is None
    assert align.stale(None, "medium.en", want, [7.0])
    assert align.stale(rec | {"version": 1}, "medium.en", want, [7.0])        # v1 缓存没收首尾、没覆盖率：重算
    assert align.stale(rec, "large-v3", want, [7.0])
    assert align.stale(rec, "medium.en", want, [7.0, 18.0])
    assert align.stale(rec, "medium.en", align.inputs([_line(text="Thanks, Eagan.")]), [7.0])
    assert align.stale(rec, "medium.en", align.inputs([_line(t1=2.5)]), [7.0])


def test_cache_path() -> None:
    assert align.cache_path(Path("E"), "shot05", "9f3c2a1b7d4e" + "0" * 52).as_posix() == "E/post/align/shot05.9f3c2a1b7d4e.json"


if __name__ == "__main__":
    if importlib.util.find_spec("whisper") is None:
        raise SystemExit(subprocess.run([str(pc.ALIGN_PYTHON), __file__]).returncode)
    pc.utf8_console()
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for n, f in tests:
        f()
        print(f"✓ {n}")
    print(f"{len(tests)} 项全过")
