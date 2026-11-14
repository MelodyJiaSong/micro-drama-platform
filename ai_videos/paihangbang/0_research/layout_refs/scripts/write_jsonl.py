"""Merge measured metrics with per-video layout observations -> data/layout_refs_2026-11-06.jsonl"""
import glob, json, sys
from pathlib import Path
root = Path(sys.argv[1])
dur = {}
for f in glob.glob(str(root / 'data/search_*.jsonl')):
    for l in open(f, encoding='utf-8'):
        d = json.loads(l); dur[d['id']] = d.get('duration')
meta = {}
for l in open(root / 'data/meta_watchpage_2026-11-06.jsonl', encoding='utf-8'):
    d = json.loads(l); meta[d['requested_id']] = d
OBS = [
 ("01","A","country_cassette_car_brands","YzRCcFx3XME","白底；车型侧视抠图；国旗做成车门贴膜","黑底白字国家横幅在顶→抠图→灰色药丸品牌名→柱状图标+Units Sold+数值→Rank N","国旗贴膜在主体上 + 顶部国名横幅","同屏约 2.5 列匀速左移（见 reference_analysis）；不同车型/颜色"),
 ("02","A","worldtv_population_cubes","wma5fLfVYF0","3D 国旗方块，体积≈数值；沙漠/棋盘场景","悬浮深色信息牌：国名 / 大号数值+单位 / World Share + Rank","国旗即主体","镜头沿队列推进；场景换底色"),
 ("03","A","worldtv_national_fruits","q6iNqx8nUnI","3D 实物：整果+剖开同框，统一木桌","左下紫色大字名称 + 红字国家列表","国旗插杆在主体后方（多国共享一果）","每条换摆盘（碗/散放/切面）"),
 ("04","A","dastatistics_phone_brands","OhvO854SS8c","产品抠图在粉彩渐变底","列头：盾形国旗+国名（蓝条）→ 品牌 logo → 品牌名（紫条）→ 产品图","盾形国旗列头；同国连排共用","按国家分组，换组才换列头内容"),
 ("05","A","worlddata3d_oldest_countries","p3E5Y5AyBYg","3D 柱体高≈数值，柱面嵌历史图片窗","柱面：国名 / 黄色数值 / years / 朝代名","柱顶旗杆","镜头环绕、柱高变化"),
 ("06","A","realdata_tallest_statues","YEPJDkZRdJU","3D 实物模型并排站一条线","深色半透明标签：名称小 / 数值巨 / 城市,国家 + 小国旗","标签内小国旗 + 地名","开头先放「平均人 176 cm」作比例参照；镜头平移"),
 ("07","A","mostdata_country_size","BuN8c74BKdM","卫星影像抠出国土，浅灰底，大量留白","插旗针旁细体：国名 / km²(mi²)","国旗插在国土上","形状本身每条都不同"),
 ("08","A","globalrank_rice_own_vs_import","3FEoOFsZ-8w","无实物图；只有圆形国旗徽章","#名次左上 + 原因小签右上 → 国名条 → 绿/红双值格","圆形国旗","原因小签每条不同；数值有明显错误（110%/00%）"),
 ("09","A","dataanalyst_rice_export_race","LMEgQRxehlc","条形赛跑；右侧手绘插画（牛车米袋）","左国名 / 条 / 国旗圆章 / 数值；大号年份","条端国旗圆章","年份推进；9:16 画面加黑边放在 16:9"),
 ("10","A","ranktheworld_rice_export_race","tu54enkhyiE","同 09（同类模板）","同 09","同 09","同 09"),
 ("11","A","dataworldplus_bread_by_country","fYv2NP-71HA","食物抠图在白/灰绿渐变底","主图 → 名称条（蓝/红）→ 黄色国名签 → 透视国旗「底座」","国旗做成卡片下半部的底座","几乎无变化；连续 3 张 White Bread 图也相似"),
 ("12","A","rmrs_top30_fragrances","rYTs0xE6YAY","主持人手持产品；封面瓶身大小≈销量","口播为主","无","主持人表演；封面用尺寸编码数值"),
 ("13","B","bonappetit_12_rice_microscope","ZDYg9SQthas","生米小木碗 → 显微镜 → 成品菜满版微距","左下细线框编号标签「5 | BOMBA」，全片不变","无国旗（口播讲产地）","生→显微→熟三段；每种配一道菜"),
 ("14","B","foodexplained_every_rice","1X5g92z_OUU","白底抠图：熟米一碗 + 前景撒生米；碗和点缀各不同","名称在图下居中，黑色粗体","无（口播）","每种换器皿和点缀（茉莉花、肉桂、芭蕉叶）；插入等式图「白+黑=紫」"),
 ("15","B","epicurious_rice_10_countries","pFgndOFYmys","俯拍成品菜在木桌；4 宫格","左上：圆形国旗 + 红色国名药丸","圆形国旗 + 国名","主持人轮换；国家开场卡（大国旗圆章+粗体国名）"),
 ("16","B","insider_16_rice_dishes","qb-gcaO_UIg","满版视频，人物试吃+食物特写","左侧转盘：顶部编号 16，中间高亮当前国，上下列前后国家","转盘里写国家/地区","转盘给进度感；每国一位当地人"),
 ("17","B","insider_29_breads","C8U23AS1irY","满版食物特写/剖面（芝士拉丝、玉米面包切面）","系列角标 + 同款转盘","同上","每条一个动作镜头（撕开、拉丝）"),
 ("18","B","insider_cheese_around_world","2NutfCHAyNM","满版制作过程 + 切面特写","同 17","同上","同 17"),
 ("19","B","bonappetit_every_egg_59","qWAagS_MANg","满版俯拍/平拍，同一大理石台面","封面大白字名称；片中左下线描小图标表示做法","无","每条换图标与器具；统一台面保持系列感"),
 ("20","B","epicurious_every_mushroom","wnCCdpt8y6w","封面：实物抠图在暖色条纹底；片中主持人","橙色名称条；事实卡：圆形小图+名称+AKA 别名+3 条要点","无","事实卡固定格式，内容每条不同"),
 ("21","B","tasty_party_rice_africa","F1ku3Rljj1c","黑底人物 + 成品菜","左上「Ghanaian Jollof Rice / as made by」+ 人名 + 左下圆形国旗","圆形国旗","每国一位厨师"),
 ("22","B","greatbigstory_7_rice_dishes","ihWdzgsIAIM","纪录片满版，人物与家庭场景","角标品牌","口播/字幕","人物故事驱动"),
]
out = open(root / 'data/layout_refs_2026-11-06.jsonl', 'w', encoding='utf-8')
for nn, grp, slug, vid, img, label, origin, variety in OBS:
    m = meta[vid]
    rec = {"no": nn, "group": grp, "id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
           "channel": m.get('initialdata_channel') or 'Country Cassette', "title": m.get('initialdata_title'),
           "views": int(m['initialdata_views_text'].split()[0].replace(',', '')), "likes": m.get('like_count'),
           "duration_s": dur.get(vid), "date_text": m.get('initialdata_date_text'),
           "measured_at": "2026-11-06", "frames_dir": f"frames/{nn}_{slug}/",
           "image_treatment": img, "label_layout": label, "origin": origin, "variety_and_motion": variety}
    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("ok")
