"""Build captioned contact sheets from frames/ (internal research only).

usage: python -I build_sheets.py <layout_refs dir>
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(sys.argv[1])
FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"
CW, CH, CAP, PAD, COLS = 640, 360, 78, 14, 4

# (frame path relative to frames/, optional crop box as fractions, title, note)
SHEETS = {
    "contact_sheet_A_food_items.jpg": (
        "A · 食物「每种 X」：单个条目怎么呈现（对应大米期）",
        [
            ("14_foodexplained_every_rice/thumb.jpg", None, "14 Food Explained · 5.1万", "熟米一碗 + 前景撒一小撮生米：生熟同框抠图，白底统一"),
            ("14_foodexplained_every_rice/f75.jpg", None, "14 Food Explained", "白米 + 黑米 = 紫米：用等式解释混合/颜色来源"),
            ("13_bonappetit_12_rice_microscope/f25.jpg", None, "13 Bon Appétit 米显微镜 · 92万", "生米装小木碗，左下编号细框「1 | BLACK」"),
            ("13_bonappetit_12_rice_microscope/f50.jpg", None, "13 Bon Appétit", "成品菜满版微距（Bomba→西班牙饭），标签不变"),
            ("11_dataworldplus_bread_by_country/thumb.jpg", None, "11 Data World Plus 面包 · 8.3万", "抠图面包在白/灰底 + 名称条 + 黄色国名签 + 透视国旗底座"),
            ("11_dataworldplus_bread_by_country/f75.jpg", None, "11 Data World Plus（反例）", "连续 3 张都叫 White Bread、图也像：重复感最强处"),
            ("03_worldtv_national_fruits/f25.jpg", None, "03 WorldTV 国果 · 200万", "整果 + 剖开：内外同框；国旗插杆在背后，统一木桌"),
            ("20_epicurious_every_mushroom/thumb.jpg", None, "20 Epicurious 蘑菇 · 398万", "统一暖色条纹底 + 实物抠图 + 橙色名称条"),
            ("20_epicurious_every_mushroom/f25.jpg", None, "20 Epicurious", "条目事实卡：圆形小图 + 名称 + AKA 别名 + 3 条要点"),
            ("15_epicurious_rice_10_countries/thumb.jpg", None, "15 Epicurious 10 国米饭 · 49万", "俯拍成品 + 圆形国旗 + 红色国名药丸（左上）"),
            ("16_insider_16_rice_dishes/f75.jpg", None, "16 Insider 16 种米饭 · 168万", "转盘式进度：第 16 道，上下列出前后国家"),
            ("19_bonappetit_every_egg_59/f50.jpg", None, "19 Bon Appétit 59 种蛋 · 4026万", "左下线描小图标表示做法（微波炉），每条换图标"),
        ],
    ),
    "contact_sheet_B_data_cards.jpg": (
        "B · 数据排行/对比卡：数值、产地、比例怎么放（对照我们 ep04）",
        [
            ("00_ours_ep04_t120.jpg", None, "00 我们 ep04（现状）", "满版照片 + 左上国旗 + 右上名次 + 底部数值块"),
            ("01_country_cassette_car_brands/f25.jpg", None, "01 Country Cassette · 53万", "白底抠图车身 + 国旗贴在车门：一图同时给出物和国"),
            ("01_country_cassette_car_brands/thumb.jpg", None, "01 Country Cassette 封面", "正面抠图 + 国旗块 + 巨号数值 + 宽字距单位"),
            ("04_dastatistics_phone_brands/thumb.jpg", None, "04 Dastatistics · 573万", "盾形国旗 + 国名做列头，产品抠图在彩色底"),
            ("04_dastatistics_phone_brands/f75.jpg", None, "04 Dastatistics", "同国连排共用列头（分组），换国才换颜色"),
            ("06_realdata_tallest_statues/f75.jpg", None, "06 Real Data 雕像 · 5829万", "半透明标签：名称小 / 数值巨 / 地点 + 小国旗"),
            ("06_realdata_tallest_statues/f25.jpg", None, "06 Real Data", "比例参照：先放「平均人 176 cm」再比"),
            ("07_mostdata_country_size/f25.jpg", None, "07 Most Data 国土 · 397万", "卫星抠图 + 插旗针 + 细字数值，大量留白"),
            ("08_globalrank_rice_own_vs_import/f25.jpg", None, "08 Global Rank 自产/进口米 · 20万", "圆形国旗 + #名次 + 原因小签（Water scarcity）"),
            ("02_worldtv_population_cubes/f50.jpg", None, "02 WorldTV 人口 · 1028万", "3D 国旗方块 + 悬浮信息牌（份额、名次）"),
            ("05_worlddata3d_oldest_countries/f25.jpg", None, "05 World Data 3D · 667万", "柱顶旗杆 + 柱面历史图窗 + 名称/数值/朝代"),
            ("09_dataanalyst_rice_export_race/f75.jpg", None, "09 Data Analyst 大米出口 · 692万", "条形赛跑 + 国旗圆章；竖版加黑边（反例）"),
        ],
    ),
}


def load(rel: str, crop):
    im = Image.open(ROOT / "frames" / rel).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im.thumbnail((CW, CH))
    cell = Image.new("RGB", (CW, CH), (20, 20, 20))
    cell.paste(im, ((CW - im.width) // 2, (CH - im.height) // 2))
    return cell


def build(name: str, title: str, items) -> None:
    rows = (len(items) + COLS - 1) // COLS
    head = 70
    W = COLS * CW + (COLS + 1) * PAD
    H = head + rows * (CH + CAP) + (rows + 1) * PAD
    sheet = Image.new("RGB", (W, H), (245, 243, 238))
    d = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(FONT_B, 34)
    fb = ImageFont.truetype(FONT_B, 22)
    fn = ImageFont.truetype(FONT, 20)
    d.text((PAD, 16), title, font=ft, fill=(20, 20, 20))
    d.text((W - 640, 26), "内部调研用，截图版权归原频道，勿外传", font=fn, fill=(150, 60, 60))
    for i, (rel, crop, cap1, cap2) in enumerate(items):
        r, c = divmod(i, COLS)
        x = PAD + c * (CW + PAD)
        y = head + PAD + r * (CH + CAP + PAD)
        sheet.paste(load(rel, crop), (x, y))
        d.text((x + 2, y + CH + 6), cap1, font=fb, fill=(30, 30, 30))
        d.text((x + 2, y + CH + 38), cap2, font=fn, fill=(70, 70, 70))
    out = ROOT / name
    sheet.save(out, quality=88)
    print(out, sheet.size)


for fname, (title, items) in SHEETS.items():
    build(fname, title, items)
