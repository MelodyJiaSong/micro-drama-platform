"""探索 t01：按实际场景与视觉镜头生成故事板和整集音频预览（edu_videos follow-up 054）。

    python edu_videos/tansuo/t01_inside_a_chip/storyboard/build_preview.py
    python tools/audio_preview.py build edu_videos/tansuo/t01_inside_a_chip/audio/preview_manifest.json
    python tools/audio_preview.py build edu_videos/tansuo/t01_inside_a_chip/audio/preview_manifest.en.json --lang en
    python edu_videos/tansuo/t01_inside_a_chip/storyboard/build_preview.py

讲稿段落只表示教学节拍，不表示影视场景。SCENE_PLAN 按地点组织，每个视觉镜头独立登记机位、动作和首帧。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\workspace\micro-drama-platform")
sys.path.insert(0, str(ROOT / "tools"))
import edu_video  # noqa: E402

TOPIC = ROOT / "edu_videos/tansuo/t01_inside_a_chip"
SB = TOPIC / "storyboard"
rel = lambda p: p.relative_to(ROOT).as_posix()


def S(sid, lines, visual):
    return {"id": sid, "lines": lines, "visual": visual}


def V(title, action, camera, source, image=None, note=""):
    return {"title": title, "action": action, "camera": camera, "source": source, "image": image, "note": note}


VISUALS = {
    "city_reveal": V("城市错觉拉远", "发光街区拉远成台灯下的芯片", "俯瞰大全景→桌面全景", "Blender 城市错觉 + Seedance 拉远"),
    "chip_close": V("芯片特写", "凯用镊子夹着独立展示样品贴近观察；旁边完整手机用于后续点击", "芯片特写→凯反应", "Seedance", "P01"),
    "transistor_answer": V("晶体管定义", "林接过话，凯半信半疑", "双人中近景", "Seedance"),
    "tap_close": V("点击手机", "凯点屏，蓝白信号钻入手机", "指尖与屏幕特写", "Seedance + 网页信号光迹"),
    "watch_rule": V("缩小规则", "林抬左腕，探索表刻度涟漪启动", "表的特写→双人", "Seedance + 网页比例尺"),
    "shrink_travel": V("米粒与头发", "米粒成山、头发成崖，两人跟信号下降", "连续下降旅行镜头", "Seedance + 网页比例尺", "P02"),
    "black_package": V("黑色封装", "凯把黑壳当成芯片，林纠正", "主板低机位全景→黑壳特写", "Blender 结构 + Seedance 人物"),
    "solder_hall": V("焊球大厅", "两人钻到封装下，焊球像柱厅", "低机位广角", "Blender 结构 + Seedance 人物", "P03"),
    "solder_detail": V("焊球连接", "供电、接地和数据分别通过不同焊球", "焊球与接触点特写", "Blender + 网页信号叠加"),
    "package_exploded": V("封装爆炸分解", "塑封、重布线层和薄硅片分层展开", "侧向爆炸图", "Blender（3D 示意）", "P04"),
    "die_flip": V("硅片翻转", "硅片从倒扣转为正面朝上", "环绕翻转镜头", "Blender（3D 示意）"),
    "die_city": V("硅片城市", "正面分区像夜景城市，凯寻找 CPU", "高空俯瞰→分区推进", "Blender + 网页色块", "P05"),
    "die_colors": V("颜色是后加的", "分区色光亮起又褪去，说明这是示意", "同一机位的对照演示", "Blender + 网页色块"),
    "die_bottom": V("开关在最底下", "视线穿过表面，底层开关被导线遮住", "表面推近→向下转场", "Blender（3D 示意）"),
    "wiring_city": V("导线城市", "凯误把层叠导线当开关", "广角看十几层互连", "Blender（3D 示意）", "P06"),
    "wiring_layers": V("上粗下细", "上层远路与底层近连接做上下对照", "垂直剖面升降", "Blender（3D 示意）"),
    "vias_close": V("层间绝缘与通孔", "先显出层间绝缘材料，交叉线路互不接触；再示相邻层换向便于布线，通孔只在选定位置连接上下层", "绝缘剖面→通孔微距", "Blender + 网页标注"),
    "signal_electrons": V("信号与电子", "蓝白信号飞驰，琥珀电子只在局部移动", "两种运动同框", "Blender（3D 示意）", "P07"),
    "electron_drift": V("电子只挪一点", "电子在导线内缓慢漂移，电场变化向前传", "电子微距→信号接续", "Blender（3D 示意）"),
    "subway_analogy": V("挤地铁类比", "人物只用小幅挪动解释个体与整体响应", "双人反应＋网页短类比", "Seedance + 网页示意"),
    "phone_blur": V("拍糊了", "凯拿手机拍导线，画面无法合焦", "过肩拍手机→屏幕糊图", "Seedance + 网页叠加", "P08"),
    "wavelength": V("光的波长太粗", "彩虹光波与纳米结构同尺度比较", "光波扫过结构的比例演示", "Blender + 网页比例尺"),
    "microscope_gray": V("电子显微镜灰图示意", "同一结构模型从灰度切为伪彩；标明这是电镜成像示意，不能冒充真实显微照片", "灰度→伪彩切换", "Blender + 网页叠加"),
    "gray_reaction": V("全灰了", "画面褪灰，凯理解照片与实物颜色的区别", "凯反应近景", "Seedance"),
    "gate_array": V("抵达栅极阵列", "一排排栅极横跨硅条，凯寻找三纳米", "阵列大全景", "Blender（3D 示意）", "P09"),
    "gate_pitch": V("栅极中心间距", "标记相邻栅极中心，和头发宽度对照", "测量特写", "Blender + 网页尺寸叠加"),
    "process_name": V("工艺代号", "在实物上找不到三纳米，转车型号类比", "实物量尺→车型短类比", "Blender + 网页示意"),
    "transistor_wide": V("发现一个开关", "凯围着静止晶体管寻找把手", "晶体管全景→凯反应", "Blender + Seedance 人物", "P10"),
    "nanosheet": V("纳米片结构", "三四片硅片连接两头，栅极四面包围", "剖视推近纳米片", "Blender（3D 示意）"),
    "relay_compare": V("继电器对比", "继电器铁片咔哒吸合，再切回静止晶体管", "机械特写↔纳米片静止", "Blender + 继电器网页示意"),
    "off_state": V("关态", "硅材料仍在，但电子没有连成通道", "关态剖视全景", "Blender（3D 示意）"),
    "channel_material": V("断的是通道不是材料", "硅片保持完整，断续电子路径被强调", "材料与电子通道分层特写", "Blender（3D 示意）"),
    "insulator": V("极薄绝缘层", "栅极与硅片之间显示绝缘层，说明漏电并非绝对零", "绝缘层微距剖面", "Blender（3D 示意）"),
    "electrons_gather": V("加电形成通道", "电场把电子聚到绝缘层附近并连成通道", "电子聚集延时", "Blender（3D 示意）"),
    "electrons_disperse": V("撤电通道消失", "电子散开，通道断开，机械结构始终不动", "开→关循环对照", "Blender（3D 示意）"),
    "field_force": V("隔空施力", "绝缘层不阻挡电场作用，磁铁只作隔空类比", "绝缘层微距＋磁铁短类比", "Blender + 网页示意"),
    "switch_realization": V("看懂了", "凯发现没有小机关，林用通断短句收束", "双人近景→通道轻演示", "Seedance + Blender 背景"),
    "wrap_question": V("为什么四面包住", "凯绕晶体管观察栅极包围", "环绕机位", "Blender + Seedance 人物"),
    "leakage": V("包围与漏电", "包围程度与关态漏电做定性对照", "控制通道特写", "Blender + 网页曲线"),
    "evolution": V("平面到全包", "平面器件、鳍式沟道、环绕栅依次变形", "三结构并列演变", "Blender（3D 示意）"),
    "tap_arrival": V("点击到了", "凯看到代表自己点击的信号抵达", "信号跟拍→凯反应", "Seedance + 网页信号光迹"),
    "voltage_01": V("高低电压与零一", "高低电压和 1/0 对应，开关产生并传递信号", "网页信息图＋晶体管背景", "网页 0/1 示意"),
    "inverter": V("反相器", "两个不同类型开关组成反相器，输入输出反转", "电路连接动画", "网页反相器示意"),
    "array_signal": V("信号传向下一开关", "通道导通，相邻晶体管依次传递信号", "阵列拉远", "Blender + 网页电路叠加", "V18C"),
    "atom_count": V("数原子", "镜头推入纳米片的局部放大窗；凯在窗外点数放大的原子层，人物不再次缩小、不接触真实原子", "人物过肩→晶格局部放大窗", "Blender 晶格 + Seedance 人物", note="旧 P11 右腕表错误且原子层数不足，已退出当前首帧；原图保留供审计。新图须左腕表、硅金刚石结构，不用旧图作视频首帧。"),
    "atom_thickness": V("四十几层与并行制造", "厚度比例拉开，再切整片硅上器件一起制造", "切面→整片硅拉远", "Blender + 网页尺度叠加"),
    "scale_guess": V("猜缩小倍数", "两人坐在晶体管顶，凯先猜一万倍", "双人中景", "Seedance + 网页数字", "P12"),
    "scale_answer": V("一千七百万倍", "探索表七格多与 100 纳米人体同时呈现", "表盘特写→人体比例", "Seedance + 网页数字揭晓"),
    "reverse_zoom": V("反向放大提问", "凯提出把芯片也放大同一倍数", "人物近景→阵列待拉远", "Seedance + Blender 背景"),
    "beijing_area": V("两个北京的面积", "阵列铺向地平线，面积换算覆盖视野", "超大拉远＋面积信息图", "Blender 拉远 + 网页面积换算"),
    "return": V("回程", "刻度涟漪倒放，两人一路返回桌面", "快速回程隧道", "Seedance + Blender 倒放", "P13"),
    "desk_recap": V("凯讲回来", "凯按开关、导线、倒扣封装自己总结", "台灯下双人中景", "Seedance", "P14"),
    "next_episode": V("下一期问题", "凯再点屏幕，追问开关怎么学会加法", "屏幕特写→凯好奇表情", "Seedance + 片尾卡"),
    "solder_power": V("供电接地与数据", "不同焊球分别承担供电、接地和数据连接", "焊球阵列俯视→接触点分组特写", "Blender + 网页连接叠加"),
    "region_switch_question": V("开关在哪个区", "凯追问开关位置，林说明各区都靠晶体管工作", "人物近景→功能分区俯视", "Seedance + Blender 色块"),
    "static_transistor_reaction": V("没有机械零件", "静止纳米片与凯的疑惑交替，确认没有会动的把手", "静止结构特写→凯反应", "Blender + Seedance 人物"),
    "channel_not_road": V("不是铺实体路", "虚拟道路示意散去，电子聚成真实导电通道", "概念道路淡出→电子通道微距", "Blender + 网页示意"),
    "magnet_analogy": V("磁铁隔空类比", "磁铁隔桌移动铁屑，随即切回绝缘层两侧的电场", "桌面类比→绝缘层微距", "网页类比 + Blender 剖面"),
    "pocket_beijing": V("两个北京揣兜里", "凯看着手机，想象两个北京的面积藏在日常设备里", "凯反应近景→手机与面积图同框", "Seedance + 网页面积图"),
}

SCENE_PLAN = [
    {"id": "c01", "location": "暖光书桌", "scale": "俯拍 → 1 cm", "purpose": "用城市错觉和一下点击提出寻找开关的任务", "segments": ["s1", "s2", "s3"], "shots": [
        S("s1", ["l01", "l02"], "city_reveal"), S("s2-1", ["l03"], "chip_close"), S("s2-2", ["l04", "l05"], "transistor_answer"),
        S("s3-1", ["l06", "l07"], "tap_close"), S("s3-2", ["l08", "l09"], "watch_rule")]},
    {"id": "c02", "location": "缩小途中", "scale": "1 cm → 100 µm", "purpose": "用米粒和头发建立第一层尺度", "segments": ["s4"], "shots": [
        S("s4", ["l10", "l11"], "shrink_travel")]},
    {"id": "c03", "location": "封装与焊球", "scale": "1 mm → 100 µm", "purpose": "分清封装、焊球和真正干活的薄硅片", "segments": ["s5", "s6", "s7"], "shots": [
        S("s5", ["l12", "l13"], "black_package"), S("s6-1", ["l14", "l15"], "solder_hall"), S("s6-2", ["l16"], "solder_power"),
        S("s7-1", ["l18", "l20"], "package_exploded"), S("s7-2", ["l21", "l22"], "die_flip")],
     "en_shots": [S("s5", ["l12", "l13"], "black_package"), S("s6-1", ["l14"], "solder_hall"), S("s6-2", ["l15"], "solder_detail"),
                  S("s6-3", ["l16"], "solder_power"), S("s7-1", ["l18", "l20"], "package_exploded"), S("s7-2", ["l21", "l22"], "die_flip")]},
    {"id": "c04", "location": "硅片正面", "scale": "1 mm", "purpose": "看清功能分区只是俯视示意，开关还在最底下", "segments": ["s8", "s9"], "shots": [
        S("s8-1", ["l23", "l24"], "die_city"), S("s8-2", ["l25", "l26"], "die_colors"), S("s9", ["l27", "l28", "l29", "l30"], "die_bottom")],
     "en_shots": [S("s8-1", ["l23", "l24"], "die_city"), S("s8-2", ["l25", "l26"], "die_colors"),
                  S("s9-1", ["l27", "l28", "l29"], "region_switch_question"), S("s9-2", ["l30"], "die_bottom")]},
    {"id": "c05", "location": "金属互连层", "scale": "10 µm → 100 nm", "purpose": "穿过导线城市，分清电子、信号与光学成像限制", "segments": ["s10", "s11", "s12"], "shots": [
        S("s10-1", ["l31", "l32"], "wiring_city"), S("s10-2", ["l33"], "wiring_layers"), S("s10-3", ["l34"], "vias_close"),
        S("s11-1", ["l35", "l36"], "signal_electrons"), S("s11-2", ["l37"], "electron_drift"), S("s11-3", ["l39"], "subway_analogy"),
        S("s12-1", ["l40", "l41"], "phone_blur"), S("s12-2", ["l42"], "wavelength"), S("s12-3", ["l43"], "microscope_gray"), S("s12-4", ["l44"], "gray_reaction")],
     "en_shots": [S("s10-1", ["l31", "l32"], "wiring_city"), S("s10-2", ["l33"], "wiring_layers"), S("s10-3", ["l34"], "vias_close"),
                  S("s11-1", ["l35", "l36"], "signal_electrons"), S("s11-2", ["l37", "l39"], "electron_drift"),
                  S("s12-1", ["l40", "l41"], "phone_blur"), S("s12-2", ["l42"], "wavelength"), S("s12-3", ["l43"], "microscope_gray"), S("s12-4", ["l44"], "gray_reaction")]},
    {"id": "c06", "location": "晶体管与栅极", "scale": "100 nm → 10 nm", "purpose": "找到开关并讲透电场如何让它通断", "segments": ["s13", "s14", "s15", "s16", "s17", "s18"], "shots": [
        S("s13-1", ["l45"], "gate_array"), S("s13-2", ["l46"], "gate_pitch"), S("s13-3", ["l47"], "process_name"),
        S("s14-1", ["l49"], "transistor_wide"), S("s14-2", ["l50"], "nanosheet"), S("s14-3", ["l51", "l52", "l53"], "relay_compare"),
        S("s15-1", ["l54", "l55", "l56"], "off_state"), S("s15-2", ["l57", "l58"], "channel_material"),
        S("s16-1", ["l59"], "insulator"), S("s16-2", ["l60", "l61"], "electrons_gather"), S("s16-3", ["l62", "l63"], "electrons_disperse"),
        S("s16-4", ["l64", "l65"], "field_force"), S("s16-5", ["l66", "l67"], "switch_realization"),
        S("s17-1", ["l68"], "wrap_question"), S("s17-2", ["l69"], "leakage"), S("s17-3", ["l70"], "evolution"),
        S("s18-1", ["l71"], "tap_arrival"), S("s18-2", ["l72"], "voltage_01"), S("s18-3", ["l73"], "inverter"), S("s18-4", ["l74", "l75"], "array_signal")],
     "en_shots": [S("s13-1", ["l45"], "gate_array"), S("s13-2", ["l46"], "gate_pitch"), S("s13-3", ["l47"], "process_name"),
                  S("s14-1", ["l49"], "transistor_wide"), S("s14-2", ["l50"], "nanosheet"), S("s14-3", ["l51"], "relay_compare"), S("s14-4", ["l52", "l53"], "static_transistor_reaction"),
                  S("s15-1", ["l54", "l55"], "off_state"), S("s15-2", ["l56", "l57"], "channel_material"), S("s15-3", ["l58"], "channel_not_road"),
                  S("s16-1", ["l59"], "insulator"), S("s16-2", ["l60"], "electrons_gather"), S("s16-3", ["l61", "l62"], "electrons_disperse"),
                  S("s16-4", ["l63", "l64"], "field_force"), S("s16-5", ["l65"], "magnet_analogy"), S("s16-6", ["l66", "l67"], "switch_realization"),
                  S("s17-1", ["l68"], "wrap_question"), S("s17-2", ["l69"], "leakage"), S("s17-3", ["l70"], "evolution"),
                  S("s18-1", ["l71"], "tap_arrival"), S("s18-2", ["l72"], "voltage_01"), S("s18-3", ["l73"], "inverter"), S("s18-4", ["l74", "l75"], "array_signal")]},
    {"id": "c07", "location": "纳米片原子切面", "scale": "1 nm", "purpose": "用四十几层原子落到制造精度与并行制造", "segments": ["s19"], "shots": [
        S("s19-1", ["l76"], "atom_count"), S("s19-2", ["l77", "l78"], "atom_thickness")],
     "en_shots": [S("s19-1", ["l76", "l77"], "atom_count"), S("s19-2", ["l78"], "atom_thickness")]},
    {"id": "c08", "location": "晶体管阵列顶部", "scale": "100 nm", "purpose": "用反向放大回答指甲盖如何放下一两百亿个开关", "segments": ["s20", "s21"], "shots": [
        S("s20-1", ["l79", "l80"], "scale_guess"), S("s20-2", ["l81", "l82"], "scale_answer"),
        S("s21-1", ["l83"], "reverse_zoom"), S("s21-2", ["l84", "l85"], "beijing_area")],
     "en_shots": [S("s20-1", ["l79", "l80"], "scale_guess"), S("s20-2", ["l81", "l82"], "scale_answer"),
                  S("s21-1", ["l83"], "reverse_zoom"), S("s21-2", ["l84"], "beijing_area"), S("s21-3", ["l85"], "pocket_beijing")]},
    {"id": "c09", "location": "回程与暖光书桌", "scale": "100 nm → 1 cm", "purpose": "回到桌面，让凯讲回来并引出下一期", "segments": ["s22", "s23"], "shots": [
        S("s22", ["l86", "l87"], "return"), S("s23-1", ["l88"], "desk_recap"), S("s23-2", ["l89", "l90", "l91"], "next_episode")]},
]

VISUALS["channel_cycle"] = V("成通道再撤电", "先保持正栅压，让电子聚成通道；直到 l62 说撤电才降压、散开；不得在 l61 提前演关态", "同一剖面固定机位，开态→关态", "Blender（3D 示意）")
VISUALS["field_question"] = V("结构不动与隔层追问", "保持关态展示机械结构未动；凯追问隔着绝缘层如何拉电子，镜头移到栅极和绝缘层", "静止剖面→凯反应→绝缘层近景", "Blender + Seedance 人物")
for scene in SCENE_PLAN:
    for shot in scene.get("en_shots", []):
        if shot["id"] == "s16-3":
            shot["visual"] = "channel_cycle"
        elif shot["id"] == "s16-4":
            shot["visual"] = "field_question"

OVERLAYS = {
    "chip_close": "后期小字：数量举例：2023 年 A17 Pro，190 亿晶体管；不是画中无品牌样品的实测。",
    "watch_rule": "后期标注：缩小旅行／信号放慢为叙事示意；一次点击涉及许多器件，并非只拨动一个开关。",
    "wiring_city": "首次进结构层上屏：多种先进工艺的结构示例，非同一型号复刻 / Examples from different processes; not one chip teardown。",
    "gate_pitch": "标尺：栅极中心距约 50 nm，仅为一种工艺示例；线宽、缝宽不能代替中心距。",
    "process_name": "短字卡：工艺代号 ≠ 单一尺寸 / Process name ≠ one dimension。",
    "nanosheet": "模型切换卡：纳米片晶体管示意 / Nanosheet transistor example；不宣称开场 A17 Pro 使用环绕栅。",
    "off_state": "角标：增强型 N 沟道示例 / Enhancement-mode nMOS；这里的栅压均相对源极。",
    "insulator": "用不同材质明确区分灰色硅、薄绝缘层、栅金属；切面描白边，不画成栅极开窗。",
    "inverter": "画出电源、地、互补 P/N 两管、共用输入与输出；高输入时 N 通 P 断、输出低，低输入相反。",
    "atom_count": "常驻：局部放大示意 / Magnified inset；沿 [001] 约 44 原子层、厚约 6 nm，以晶格计算渲染，不拿 AI 点阵计数。",
    "atom_thickness": "原子层统计沿 [001]，间距约 0.136 nm；不是原子直径。拉远回器件时关闭局部放大窗。",
    "scale_guess": "人物仍约 100 nm 高；叠层高度须由模型决定，不再要求叠层与人同高。",
    "scale_answer": "后期：1.7 m ÷ 100 nm ≈ 1700 万；7.23 格（每格十倍）。镜头放大不改变人物尺寸。",
    "beijing_area": "后期：比较的是面积；约 3.0–3.3 万 km² ≈ 1.8–2.0 个北京市行政区。平均地盘包含布线等面积，不是晶体管实体面积。",
    "next_episode": "片尾补 AI 生成画面／AI 配音标注及来源卡；下一期：开关怎么组成加法。",
}
COMMON_VISUAL_RULES = "真人写实；林 G9 低发髻、左腕唯一探索表，凯 K1 卷发与固定服装。结构按模型，硅为灰色、铜导线为铜色、绝缘层独立可辨；结构剖切面描白边。蓝白只表示信号、电场变化，琥珀点表示电子；它们不是实际发光。比例尺由后期按模型与机位计算，非人物身高。进入芯片常驻‘结构／颜色／信号示意’，不要等到拍糊才揭示。进入晶体管后人物约 100 nm 高，原子层仅用局部放大窗。所有中文、英文文字和读数后期叠加，AI 图不画字。"


def frame_prompt(key):
    visual = VISUALS[key]
    path = SB / "prompts" / "current" / f"{key}.txt"
    path.parent.mkdir(exist_ok=True)
    text = f"当前分镜首帧制作说明（follow-up 056，待独立复审）\n{COMMON_VISUAL_RULES}\n镜头：{visual['title']}\n镜头内动作：{visual['action']}\n机位：{visual['camera']}\n画面来源：{visual['source']}\n只画动作开始前的一个瞬间，不把整段动作拼成多格图。人物参考：_shared/cast/lin/turnaround.png 与 _shared/cast/kai/turnaround.png。\n{OVERLAYS.get(key, '')}\n{visual['note']}\n旧图片仅作构图参考；本说明不是旧图的历史生成请求。未生成、未独立审图不得记已完成。\n"
    path.write_text(text, encoding="utf-8")
    return rel(path)

beats = {}
for row in (TOPIC / "beats.md").read_text(encoding="utf-8").splitlines():
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    match = re.match(r"^(\d+)\s+(.+)$", cells[0]) if len(cells) >= 6 else None
    if match:
        beats[int(match.group(1))] = {"question": cells[3]}


def spoken_line(ln):
    match = re.match(r"^\[(凯|林|Kai|Lin)\]\s*(.+)$", ln.raw, re.S)
    if not match:
        raise ValueError(f"{ln.id} 缺说话人：{ln.raw}")
    return {"id": ln.id, "speaker": "阿凯" if match.group(1) in ("凯", "Kai") else "林工", "text": match.group(2), "pause": ln.pause}


def voice(character, lang):
    data = json.loads((ROOT / f"edu_videos/tansuo/_shared/cast/{character}/voice.json").read_text(encoding="utf-8"))
    return data["voices"][lang]


def scene_shots(scene, lang):
    return scene.get("en_shots", scene["shots"]) if lang == "en" else scene["shots"]


def validate_plan():
    assert len(SCENE_PLAN) == 9
    for lang, expected_lines, expected_shots in (("zh", 87, 53), ("en", 87, 58)):
        segments = edu_video.Topic(TOPIC, lang).segments()
        expected = [ln.id for seg in segments for ln in seg.lines]
        used = [line for scene in SCENE_PLAN for shot in scene_shots(scene, lang) for line in shot["lines"]]
        shot_ids = [shot["id"] for scene in SCENE_PLAN for shot in scene_shots(scene, lang)]
        visual_keys = [shot["visual"] for scene in SCENE_PLAN for shot in scene_shots(scene, lang)]
        assert len(expected) == expected_lines
        assert used == expected, f"{lang} 镜头台词覆盖不等于讲稿：{len(used)} / {len(expected)}"
        assert len(shot_ids) == expected_shots, f"{lang} 镜头数变化未登记：{len(shot_ids)}"
        assert len(shot_ids) == len(set(shot_ids)), f"{lang} 镜头 ID 重复"
        assert len(visual_keys) == len(set(visual_keys)), f"{lang} 不同镜头复用了同一视觉登记"
        assert all(visual in VISUALS for visual in visual_keys)
        for scene in SCENE_PLAN:
            assert len(scene_shots(scene, lang)) >= len(scene["segments"]), f"{scene['id']} 又退化成段落单镜"


def image_info(visual):
    image_id = visual["image"]
    if not image_id:
        return None, "首帧待出：本镜有独立机位，不再套用无关旧图"
    path = SB / f"{image_id}.png"
    if not path.exists():
        return None, f"首帧待出：登记的 {image_id} 文件不存在"
    if image_id == "V18C":
        note = "V18C 已通过独立故事板审查"
    elif image_id == "P11":
        note = "旧 P11 仅临时参考；右腕表未过审，正式首帧必须修正"
    else:
        note = f"临时沿用 {image_id} 作构图参考，不代表本镜已审通过"
    return {"path": rel(path), "mtime": int(path.stat().st_mtime)}, note


def build(lang):
    segments = edu_video.Topic(TOPIC, lang).segments()
    line_map = {ln.id: spoken_line(ln) for seg in segments for ln in seg.lines}
    timeline_path = TOPIC / "audio/preview" / ("" if lang == "zh" else "en") / "timeline.json"
    old_timeline = json.loads(timeline_path.read_text(encoding="utf-8"))["shots"] if timeline_path.exists() else []
    old_by_id = {shot["id"]: shot for shot in old_timeline}
    board_scenes, manifest_scenes = [], []
    for scene in SCENE_PLAN:
        board_shots, manifest_shots = [], []
        for planned in scene_shots(scene, lang):
            visual = VISUALS[planned["visual"]]
            lines = [line_map[line_id] for line_id in planned["lines"]]
            old = old_by_id.get(planned["id"], {})
            old_lines = old.get("lines", [])
            lead = old_lines[0]["start"] if old_lines else (0.4 if lang == "en" else 0.6)
            tail = round(old.get("speech_need", old_lines[-1]["end"] + 0.8) - old_lines[-1]["end"] - lines[-1]["pause"], 2) if old_lines else 0.8
            image, note = image_info(visual)
            if visual["note"]:
                note = f"{note}；{visual['note']}"
            if planned["visual"] in OVERLAYS:
                note += "；" + OVERLAYS[planned["visual"]]
            duration = old.get("duration", 0)
            board_shots.append({
                "id": planned["id"], "key": planned["id"], "title": visual["title"], "duration": duration,
                "cast": ["林", "凯"],
                "dialogue": [{"speaker": line["speaker"], "direction": "", "text": edu_video.Line(line["id"], line["text"]).text} for line in lines],
                "action": visual["action"], "blocking": "讲机制时人物退到画面边上，让结构与特效讲。",
                "beats": f"{scene['purpose']}；{visual['action']}", "camera": f"{visual['camera']}；画面来源：{visual['source']}",
                "image": image, "framePrompt": frame_prompt(planned["visual"]),
                "packPrompt": "", "shotDir": rel(SB), "note": note,
            })
            manifest_shots.append({
                "id": planned["id"], "title": visual["title"], "image": image["path"] if image else None,
                "note": note, "lines": lines, "lead": lead, "tail": tail,
            })
        questions = "；".join(dict.fromkeys(beats[int(seg[1:])]["question"] for seg in scene["segments"]))
        board_scenes.append({
            "id": scene["id"], "location": scene["location"], "time": f"比例尺 {scene['scale']}", "purpose": scene["purpose"],
            "question": questions, "shots": board_shots, "total": sum(shot["duration"] for shot in board_shots),
        })
        manifest_scenes.append({
            "id": scene["id"], "title": f"{scene['id']} {scene['location']}", "subtitle": f"比例尺 {scene['scale']}", "shots": manifest_shots,
        })
    return board_scenes, manifest_scenes


validate_plan()
zh_scenes, zh_manifest = build("zh")
board = {
    "title": "探索 · 芯片 t01：跟着一下点击，找到那个开关", "eyebrow": "教学视频 · 探索 · t01 故事板 V5.1 修补版",
    "lang": "zh", "version": "v5.1-review-repair", "updated": "2026-11-15",
    "notes": [
        COMMON_VISUAL_RULES,
        "本轮已修文字、动作时序与制作说明；Kimi 额度限制，本轮独立复审未完成。当前仍是制作中的故事板，不是可直接出片的完成版。",
        "P11 错腕表原图已退出当前首帧；38 个原缺图镜头加该镜，共 39 个中文镜头待首帧。现有 14 图仅作构图参考。",
        "首帧提示统一来自当前分镜；旧 P/V 提示和旧审稿保留为历史，不再用于直接生成。每镜补有真实性、尺度和电路机制制作约束。",
        "已按实际地点重组为 9 个场景、53 个中文视觉镜头；不再把 23 个讲稿段落各自当成单镜场景。",
        "每镜都有独立机位和动作；没有对应首帧就明确显示“首帧待出”，不再用同一张旧图冒充不同镜头。",
        "英文为 58 镜，因语速不同而对少数镜头作语言版拆分；时长与台词起点以对应语言 timeline.json 为准。",
    ],
    "links": [{"label": "音频预览", "href": f"/episode-preview?path={rel(TOPIC)}&audio=1"},
              {"label": "中文讲稿", "path": rel(TOPIC / "script.md")}, {"label": "节拍", "path": rel(TOPIC / "beats.md")},
              {"label": "事实台账", "path": rel(TOPIC / "claims.json")}, {"label": "旧故事板数据", "path": rel(SB / "panels.json")}],
    "scenes": zh_scenes,
}
(SB / "storyboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")

manifest = {
    "title": "探索 · 芯片 t01：跟着一下点击，找到那个开关", "path": rel(TOPIC), "lang": "zh",
    "defaults": {"split": True, "max": 15},
    "voices": {"林工": {k: voice("lin", "zh")[k] for k in ("reference", "reference_text")},
               "阿凯": {k: voice("kai", "zh")[k] for k in ("reference", "reference_text")}},
    "scenes": zh_manifest,
    "links": [{"label": "故事板", "path": rel(SB / "storyboard.json")}, {"label": "中文讲稿", "path": rel(TOPIC / "script.md")},
              {"label": "事实台账", "path": rel(TOPIC / "claims.json")}],
    "notes": [{"title": "V5 视觉分镜", "items": [
        "9 个实际场景、53 个中文镜头；同地点的教学节拍已合并为多镜场景。",
        "首帧待出表示该机位尚无图，不是漏数据；旧图只在构图匹配时作临时参考。",
        "本地配音只作听感与时长预览；用户听审前不提交 Seedance。"]}],
}
(TOPIC / "audio").mkdir(exist_ok=True)
(TOPIC / "audio/preview_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

en_scenes, en_manifest = build("en")
en_manifest = manifest | {
    "title": "Tansuo t01: Follow a Tap into a Chip", "lang": "en",
    "defaults": manifest["defaults"] | {"lead": 0.4},
    "voices": {"林工": {k: voice("lin", "en")[k] for k in ("reference", "reference_text")},
               "阿凯": {k: voice("kai", "en")[k] for k in ("reference", "reference_text")}},
    "scenes": en_manifest,
    "links": [{"label": "Storyboard", "path": rel(SB / "storyboard.json")}, {"label": "English script", "path": rel(TOPIC / "script.en.md")}],
    "notes": [{"title": "V5 visual shot plan", "items": [
        "Nine physical scenes and 58 English shots. Missing frames are marked instead of reusing unrelated panels.",
        "Local cloned voices are for timing and listening review only."]}],
}
(TOPIC / "audio/preview_manifest.en.json").write_text(json.dumps(en_manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"9 个实际场景；中文 {len(zh_scenes and [shot for scene in zh_scenes for shot in scene['shots']])} 镜；英文 {len([shot for scene in en_scenes for shot in scene['shots']])} 镜")
