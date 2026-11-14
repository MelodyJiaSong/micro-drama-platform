"""真实尺度 · 中文版叠加层：版式与 cards.py 一致，文字换成中文，写 <集目录>/_build/cards_zh/（文件名与英文版相同）。

    python ai_videos/zhenshi_chidu/_tools/cards_zh.py <集目录>
    python ai_videos/zhenshi_chidu/_tools/compose.py <集目录> --cards _build/cards_zh --music <配乐> --out render/ep_master_zh.mp4

字体 Noto Sans SC（可变字重，SIL OFL 1.1，projects/rank_scroll/assets/fonts/）。片中无旁白，中英两版只差叠加文字。
英寸换算（ft/in）对中文观众无意义，副数值改为「人高的 N 倍」（参照人 1.75 m）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cards import ACCENT, GREY, H, W, WHITE, _canvas, _shadowed_panel  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
NOTO = REPO / "projects" / "rank_scroll" / "assets" / "fonts" / "NotoSansSC-Variable.ttf"
WEIGHT = {"Black": 900, "ExtraBold": 800, "Bold": 700, "Medium": 500, "Regular": 400}
DIM = (160, 166, 175, 255)

# 卡上用的中文名（短名；审片页 make_preview.ZH 可带括注）
NAME = {
    "Giraffe": "长颈鹿", "African Bush Elephant": "非洲草原象", "Asian Elephant": "亚洲象", "African Forest Elephant": "非洲森林象",
    "Moose": "驼鹿", "Wild Yak": "野牦牛", "Gaur": "印度野牛", "White Rhinoceros": "白犀", "Indian Rhinoceros": "印度犀",
    "Wild Water Buffalo": "野水牛", "American Bison": "美洲野牛", "European Bison": "欧洲野牛", "Giant Eland": "德氏大羚羊",
    "African Buffalo": "非洲水牛", "Javan Rhinoceros": "爪哇犀", "Banteng": "爪哇野牛", "Common Eland": "普通大羚羊",
    "Hippopotamus": "河马", "Black Rhinoceros": "黑犀", "Elk (Wapiti)": "北美马鹿", "Grévy's Zebra": "细纹斑马",
    "Polar Bear": "北极熊", "Muskox": "麝牛", "Mountain Zebra": "山斑马", "Kiang": "藏野驴", "Brown Bear": "棕熊",
    "Plains Zebra": "平原斑马", "Sumatran Rhinoceros": "苏门答腊犀", "Bongo": "紫羚", "Takin": "扭角羚",
}
REGION = {
    "Arctic Canada & Greenland": "加拿大北极地区与格陵兰", "Central & West Africa": "中非与西非",
    "East & Southern Africa": "东非与南部非洲", "Eastern Himalaya & China": "喜马拉雅东部与中国",
    "India & Nepal": "印度与尼泊尔", "India, Nepal & Thailand": "印度、尼泊尔与泰国", "Kenya & Ethiopia": "肯尼亚与埃塞俄比亚",
    "Namibia & South Africa": "纳米比亚与南非", "North America": "北美洲", "North America & East Asia": "北美与东亚",
    "Northern Eurasia & N. America": "欧亚大陆北部与北美", "Northern forests worldwide": "北半球的北方森林",
    "Poland, Belarus & Russia": "波兰、白俄罗斯与俄罗斯", "South & Southeast Asia": "南亚与东南亚", "Southeast Asia": "东南亚",
    "Southern & East Africa": "南部与东部非洲", "Sub-Saharan Africa": "撒哈拉以南非洲", "Sumatra & Borneo": "苏门答腊与婆罗洲",
    "The Arctic": "北极地区", "Tibetan Plateau": "青藏高原", "Ujung Kulon, Indonesia": "印度尼西亚乌戎库隆",
}
BASIS = {"shoulder height · adult male": "肩高 · 成年雄性", "shoulder height · adults, both sexes": "肩高 · 成年个体（雌雄合计）"}
INSIGHT = [   # 与 data.json insights 同序
    "为什么量肩高？头和脖子会动，肩膀不会。\n黄线标出的就是每只动物量肩高的位置。",
    "从下一只开始，每一只的肩高都不低于我们 1.75 m 的参照人。",
]
MAN = "1.75 m 的人"
MUSIC = "配乐：本频道用 Suno 生成的原创纯音乐（job b60957b7）。字体：Noto Sans SC（SIL OFL 1.1）。"


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(NOTO), size)
    f.set_variation_by_axes([WEIGHT[weight]])
    return f


def _tw(d, text, f) -> int:
    return int(d.textlength(text, font=f))


def _center(d, text, f, y, fill=WHITE):
    d.text(((W - _tw(d, text, f)) // 2, y), text, font=f, fill=fill)


def wrap(d, text: str, f, width: int, indent: str = "") -> list[str]:
    """中英混排折行：英文按词、中文按字；行首不放中文标点；文本里的换行符是指定断行。"""
    if "\n" in text:
        return [ln for part in text.split("\n") for ln in wrap(d, part, f, width, indent)]
    toks, buf = [], ""
    for ch in text:
        if ch.isascii() and ch != " ":
            buf += ch
            continue
        if buf:
            toks.append(buf)
            buf = ""
        toks.append(ch)
    if buf:
        toks.append(buf)
    lines, cur = [], ""
    for t in toks:
        nxt = cur + t
        if _tw(d, nxt, f) > width and cur.strip() and t not in "，。、；：）」？！":
            lines.append(cur.rstrip())
            cur = indent + t.lstrip()
        else:
            cur = nxt
    lines.append(cur.rstrip())
    return lines


def times_man(it: dict, man_m: float) -> str:
    k = it["dims"]["height_m"] / man_m
    return "和参照人一样高" if abs(k - 1) < 0.005 else f"人高的 {k:.2f} 倍"


def label_card(it: dict, man_m: float) -> Image.Image:
    im, d = _canvas()
    x0, y0 = 60, 770
    f_rank, f_name, f_sci = font("Black", 60), font("Black", 56), font("Medium", 28)
    f_val, f_imp, f_meta, f_src = font("Black", 70), font("Bold", 34), font("Medium", 29), font("Medium", 25)
    rank = f"{'=' if it['tied'] else '#'}{it['rank']}"
    name = NAME[it["name"]]
    sec = times_man(it, man_m)
    meta = f"{BASIS[it['basis']]}{' · 并列' if it['tied'] else ''}  ·  {REGION[it['region']]}"
    src = "来源：" + it["source_short"]
    rank_w = max(_tw(d, rank, f_rank), 120)
    tag_w = 170
    sci_w = _tw(d, it["scientific_name"], f_sci)
    val_w = _tw(d, it["value_display"], f_val) + 24 + _tw(d, sec, f_imp)
    inner = max(rank_w + 28 + _tw(d, name, f_name) + 24 + sci_w + tag_w, val_w, _tw(d, meta, f_meta), _tw(d, src, f_src), 560)
    box = (x0, y0, x0 + inner + 76, y0 + 286)
    _shadowed_panel(im, box)
    cx, cy = x0 + 38, y0 + 26
    d.text((cx, cy - 8), rank, font=f_rank, fill=ACCENT)
    d.text((cx + rank_w + 28, cy - 10), name, font=f_name, fill=WHITE)
    d.text((cx + rank_w + 28 + _tw(d, name, f_name) + 24, cy + 18), it["scientific_name"], font=f_sci, fill=GREY)
    d.text((cx, cy + 74), it["value_display"], font=f_val, fill=WHITE)
    d.text((cx + _tw(d, it["value_display"], f_val) + 24, cy + 110), sec, font=f_imp, fill=GREY)
    d.text((cx, cy + 170), meta, font=f_meta, fill=GREY)
    d.text((cx, cy + 212), src, font=f_src, fill=DIM)
    if it.get("model") and it["model"].get("ai_model"):
        tag, f_tag = "AI 生成图", font("Black", 24)
        tw = _tw(d, tag, f_tag)
        bx1 = box[2] - 22
        d.rounded_rectangle((bx1 - tw - 28, y0 + 22, bx1, y0 + 60), 8, fill=ACCENT)
        d.text((bx1 - tw - 14, y0 + 23), tag, font=f_tag, fill=(20, 20, 20, 255))
    return im


def man_label() -> Image.Image:
    f = font("Bold", 27)
    tw = _tw(ImageDraw.Draw(Image.new("RGBA", (1, 1))), MAN, f)
    im = Image.new("RGBA", (tw + 36, 62), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw + 36, 44), 10, fill=(16, 20, 26, 200))
    d.text((18, 2), MAN, font=f, fill=WHITE)
    cx = (tw + 36) // 2
    d.polygon([(cx - 10, 44), (cx + 10, 44), (cx, 60)], fill=(16, 20, 26, 200))
    return im


def hook_card() -> Image.Image:
    im, d = _canvas()
    _shadowed_panel(im, (W // 2 - 820, 50, W // 2 + 820, 270), 28)
    _center(d, "谁才是最高的巨兽？", font("Black", 96), 56)
    _center(d, "30 种最大的陆地动物  ·  真实比例  ·  和一个 1.75 m 的人站在一起", font("Bold", 36), 196)
    return im


def title_card() -> Image.Image:
    im, d = _canvas()
    _shadowed_panel(im, (300, 772, 1620, 1050), 28)
    _center(d, "真实尺度  ·  TRUE SCALE", font("ExtraBold", 32), 784, ACCENT)
    _center(d, "最大的 30 种陆地动物", font("Black", 72), 822)
    _center(d, "按肩高排名  ·  每只旁边站一个 1.75 m 的人", font("Bold", 38), 920)
    _center(d, "数据截至 2026 年 11 月", font("Medium", 28), 984, DIM)
    return im


def group_card() -> Image.Image:
    im, d = _canvas()
    _shadowed_panel(im, (W // 2 - 760, 30, W // 2 + 760, 190), 24)
    _center(d, "30 种全体合影，真实比例", font("Black", 64), 40)
    _center(d, "小的在前、高的在后  ·  1.75 m 的人在最左", font("Bold", 30), 128)
    return im


def insight_card(text: str) -> Image.Image:
    im, d = _canvas()
    f = font("ExtraBold", 46)
    lines = wrap(d, text, f, 1480)
    h = 76 + 62 * len(lines) + 56
    y0 = H - h - 24
    _shadowed_panel(im, (180, y0, W - 180, y0 + h), 28)
    _center(d, "你知道吗？", font("Black", 32), y0 + 22, ACCENT)
    for i, ln in enumerate(lines):
        _center(d, ln, f, y0 + 72 + 62 * i)
    return im


def sources_card(data: dict) -> Image.Image:
    im = Image.new("RGBA", (W, H), (14, 17, 22, 255))
    d = ImageDraw.Draw(im)
    d.text((110, 60), "资料来源与署名", font=font("Black", 50), fill=ACCENT)
    f, fb = font("Medium", 24), font("Bold", 26)
    srcs: dict[str, list[str]] = {}
    for it in data["items"]:
        srcs.setdefault(it["source_short"], []).append(NAME[it["name"]])
    col_x, y, x = [110, 1000], 160, 0
    d.text((col_x[0], y), "肩高（典型成年个体，有数据时取雄性；完整出处与链接见置顶评论）：", font=fb, fill=WHITE)
    y += 46
    y_start = y
    for s, names in sorted(srcs.items(), key=lambda kv: -len(kv[1])):
        wrapped = wrap(d, f"{s}：" + "、".join(names), f, 830, "    ")
        if y + 33 * len(wrapped) > 700 and x == 0:
            x, y = 1, y_start
        for ln in wrapped:
            d.text((col_x[x], y), ln, font=f, fill=GREY)
            y += 33
        y += 8
    y = 790
    for ln in [
        "动物与 1.75 m 的人：为本片 AI 生成的图像，抠像后由脚本按卡上的肩高缩放。",
        "远景与金合欢：为本片 AI 生成。Poly Haven（CC0）：HDRI Mpumalanga Veld（G. Zaal）、Plains Sunset（D. Savva & J. Guest）；",
        "地面贴图 Grass Ground（C. Baglioni）；草与石块模型：R. Cilliers、R. Tuytel、G. Zaal、J. van Heerden。",
        MUSIC,
        "名单：30 种最重的野生陆地动物（与我们的体重排行同一份名单），按典型肩高重新排名；资料给出范围时取中值。",
    ]:
        d.text((110, y), ln, font=f, fill=GREY)
        y += 36
    return im


def pinned_comment_zh(ep: Path, data: dict) -> None:
    """中文置顶评论（国内平台）：不放外链（平台会屏蔽或限流），每只写名次、中文名、肩高与卡上出处简称；
    完整引文与链接在英文版（YouTube）置顶评论与 sources.md。B站单条评论 ≤ 1000 字，超了拆成置顶 + 回复。"""
    rows = [f"{'=' if it['tied'] else '#'}{it['rank']} {NAME[it['name']]} {it['value_display']}：{it['source_short']}"
            for it in data["items"]]
    head = "肩高出处（典型成年个体，有数据时取雄性；资料给出范围时取中值）。名次 · 动物 · 肩高：出处"
    parts, cur = [], [head]
    for r in rows:
        if len("\n".join(cur + [r])) > 980:
            parts.append(cur)
            cur = []
        cur.append(r)
    parts.append(cur)
    if len(parts) > 1:
        parts = [p + [f"（{i + 1}/{len(parts)}）"] for i, p in enumerate(parts)]
    (ep / "_build" / "pinned_comment_zh.txt").write_text("\n\n".join("\n".join(p) for p in parts) + "\n", encoding="utf-8")


def main() -> None:
    ep = Path(sys.argv[1]).resolve()
    data = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    pinned_comment_zh(ep, data)
    assert len(INSIGHT) == len(data["insights"])
    man_m = data["human_reference_m"]
    out = ep / "_build" / "cards_zh"
    out.mkdir(parents=True, exist_ok=True)
    for i, it in enumerate(data["items"]):
        label_card(it, man_m).save(out / f"label_{i:02d}.png")
    man_label().save(out / "man_label.png")
    hook_card().save(out / "hook.png")
    title_card().save(out / "title.png")
    group_card().save(out / "group.png")
    for i, t in enumerate(INSIGHT):
        insight_card(t).save(out / f"insight_{i}.png")
    sources_card(data).save(out / "sources.png")
    print("cards_zh ->", out)


if __name__ == "__main__":
    main()
