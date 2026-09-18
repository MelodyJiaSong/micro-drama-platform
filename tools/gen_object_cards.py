# -*- coding: utf-8 -*-
"""把「场景里有哪些物件」的清单，摊成可以开工的物件文件夹（用户 2026-09-17 定的流程）。

流程（五步，每一步的产出都是下一步的输入）
------------------------------------------
  1. **拆解**（Claude）  读各 bg / p 卡，把场景拆成一个个**有界的物件**，写进
     `2_世界观人设/object_inventory.toml`。本文件读它，生成：
         props/p{N}_{名}/{名}.md      —— 三张图的 prompt：正面（参考）+ 侧面 + 背面
         props/p{N}_{名}/object.toml  —— 归一化 + 验收规格（白模闸门的输入）
  2. **出图**（用户）    按 md 出图、导入；导入器按 prompt 首行的路由键落位。
  3. **生成**（Claude）  `tools/hyper3d_fetch.py --image 正 --image 侧 --image 背` → raw.glb
  4. **闸门**（Claude）  `tools/whitemodel_normalize.py --src raw.glb --spec object.toml`
                         → `whitemodel/{名}.blend`
  5. **组装**（Claude）  重跑 `tools/build_bianjing.py`：`resolve_asset` 看见白模就把
                         同尺寸替身换成真网格，shot previz 跟着变。**布局代码一个字都不用改。**

为什么正面先出、当参考
--------------------------
用户 2026-09-17 定的次序：**先出正面，再拿正面当参考出侧面与背面**。这样 `-1` 就是那张参考，
读起来不用解释。理由是**三张正交图各自独立生成时不会互相同意**——形制、比例、部件位置会各漂各的；
有一张钉死的参考，后两张只换机位。
锚点（四分之三视角）不再默认出——它只对人眼验收有用，对重建没用，省一张就是省一张。

为什么正交三视图必须**阴天均匀光**
--------------------------------
它们是喂 image-to-3D 的，不是给人看的画面。烘进纹理的方向光与投影会被重建当成几何，
出来就是一身假凹凸（sk1 divergence #18）。**这条与 follow-up 014 的 GoT 实拍画风不冲突**：
画风管的是入画的镜头，这三张是工装图，没有一张会进片子。

用法（仓库根目录）：
    python tools/gen_object_cards.py                 # 写盘
    python tools/gen_object_cards.py --check         # 只校验
    python tools/gen_object_cards.py --only p12,p13  # 只生成这几个
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
A = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "2_世界观人设"
INVENTORY = A / "object_inventory.toml"
PROPS = A / "props"

# 三视图的共用工装串：正交、阴天均匀光、纯背景、零文字。**不是 GoT 画风**（见抬头）
ORTHO = ("正交视图（无透视、无近大远小），纯中性浅灰背景，阴天一样的均匀散射光、没有方向性阴影、"
         "没有投影、没有高光；主体完整入画、居中、不被裁切，四周留约百分之八的边；"
         "画面里只有这一件东西，没有地面、没有背景物、没有人、没有文字、没有水印")
ORTHO_NEG = ("透视畸变, 广角变形, 方向光, 硬阴影, 投影, 高光, 反光, 环境反射, 地面, 背景物, 人, 手, "
             "文字, 水印, logo, 裁切, 多个物体, 爆炸图, 拆解图, 尺寸标注, 箭头, 网格底纹, 渐变背景, "
             "卡通渲染, 插画风, 线稿, 白模, 灰模, 三维渲染感, 塑料质感")
# 每个视图除了写「从哪看」，还必须写死「这一面该看到多大」，**而且要放在 prompt 的高权重位置**。
# 2026-09-17 两次实测踩到的坑：
#   一、床榻（宽1.1 × 长2.0 × 高0.6）没有天然的「正面」，模型把 2.0 m 的长边当成了正面；
#   二、漕船（宽4.5 × 长18 × 高3）把「正面」画成了和侧面一模一样的舷侧视图。
# 第二次失败证明：光把尺寸写进中段的 `画面尺寸:` 挡不住模型对「船＝侧视图」这类强先验——
# 它读到 `主体: 漕船` + `形体规格: 长 18 米` 就已经锁死了构图，后面再说什么都晚了。
# 所以现在：约束提到 `参考用法:` 之后、`主体:` 之前的 `视图:` 行，`主体:` 本身带上朝向前缀，
# 并把**另外两个视图写进负向词**（「本图不是侧视图」正向说一遍、负向再挡一遍）。
# 末位两项 = (水平方向取 size 的哪一项, 垂直方向取哪一项)、(本图要挡掉的另外两个视图名)
VIEWS = [("1", "正面", "正视图", "主体的**正面**正对镜头",
          "正前方平视，视线与主体正面垂直", (0, 2), ("侧视图", "背视图")),
         ("2", "侧面", "侧视图", "主体的**左侧面**正对镜头（相对正视图绕竖直轴转了 90°）",
          "正左侧平视，视线与主体侧面垂直", (1, 2), ("正视图", "背视图")),
         ("3", "背面", "背视图", "主体的**背面**正对镜头（相对正视图绕竖直轴转了 180°）",
          "正后方平视，视线与主体背面垂直", (0, 2), ("正视图", "侧视图"))]

# 第三视图换成俯视的那一档（清单里 `view3 = "俯视"`）。
# 2026-09-17 实测定的：**背面与正面是同一根轴**，对 image-to-3D 不贡献新方向，
# 三张图实际只覆盖两个轴。而对「没人会去拍那个窄面」的物件（床榻端面、扁担端面、
# 长凳端面），无论 prompt 怎么写模型都画成长边——p22 用最终版卡仍然塌陷。
# 俯视两头都占：补上第三个轴，且它不是「经典产品视角」，塌不到侧视图上。
VIEW3_TOP = ("3", "俯视", "俯视图", "**从正上方垂直向下看**主体的顶面",
             "正上方垂直俯视，相机光轴垂直于地面、正对主体顶面", (0, 1), ("正视图", "侧视图"))


# 第二视图换成四分之三视角的那一档（清单里 `view2 = "四分之三"`）。
# 2026-09-17 实测定的：**又宽又薄**的物件（杈子 2.4×0.5×1.3、床榻、长凳）那个窄端
# 现实里没人拍，模型无论如何都画成长边——p18 换了俯视之后第三张对了，第二张仍然塌。
# 四分之三视角两头都占：**一张图同时给出三个轴**，而且它是模型最愿意画的角度。
# 代价是它不是正交图（带轻微透视），所以场景串要换一版，机检也量不了它的宽高比。
VIEW2_ISO = ("2", "四分之三", "四分之三视角图",
             "从主体的**右前上方**看过去，同一张里同时看得到正面、右侧面与顶面",
             "右前上方四分之三视角：与主体正面约 45°、俯角约 20°", (0, 2), ("正视图", "俯视图"))

# 四分之三视角专用场景串：允许轻微透视，其余（阴天均匀光、纯背景、零文字）与正交图一致
ISO_NEG = ("广角变形, 鱼眼, 方向光, 硬阴影, 投影, 高光, 反光, 环境反射, 地面, 背景物, 人, 手, "
           "文字, 水印, logo, 裁切, 多个物体, 爆炸图, 拆解图, 尺寸标注, 箭头, 网格底纹, 渐变背景, "
           "卡通渲染, 插画风, 线稿, 白模, 灰模, 三维渲染感, 塑料质感")
ISO_SCENE = ("轻微透视的四分之三视角（不是正交图，但焦段偏长、变形很小），纯中性浅灰背景，"
             "阴天一样的均匀散射光、没有方向性阴影、没有投影、没有高光；主体完整入画、居中、"
             "不被裁切，四周留约百分之八的边；画面里只有这一件东西，没有地面、没有背景物、"
             "没有人、没有文字、没有水印")


def load() -> list[dict]:
    if not INVENTORY.is_file():
        raise SystemExit(f"没有清单：{INVENTORY.relative_to(REPO)}")
    data = tomllib.loads(INVENTORY.read_text(encoding="utf-8"))
    objs = data.get("object", [])
    seen: set[str] = set()
    for o in objs:
        for field in ("key", "name", "en", "size", "front", "desc", "scene", "parts"):
            if field not in o:
                raise SystemExit(f"{o.get('key', '?')} 缺字段 {field}")
        if not re.fullmatch(r"p\d+", o["key"]):
            raise SystemExit(f"资产键「{o['key']}」不是 pN（build_bianjing.resolve_asset 只认这个）")
        if o["key"] in seen:
            raise SystemExit(f"资产键重复：{o['key']}")
        seen.add(o["key"])
        if len(o["size"]) != 3:
            raise SystemExit(f"{o['key']} 尺寸要三个数（X宽 Y长 Z高，米）")
    return objs


def _shape(h: float, v: float) -> str:
    r = h / v if v else 1.0
    if r >= 1.6:
        return f"是一个明显横向的长方形（宽高比约 {r:.1f}:1）"
    if r <= 0.62:
        return f"是一个明显竖向的长方形（高宽比约 {1 / r:.1f}:1）"
    return "接近方形"


def _depth(n: str, size: list[float], top: bool = False) -> float:
    if top:
        return size[2]          # 俯视：看不见的是高度
    return size[1] if n in ("1", "3") else size[0]



FACE = {"1": "正面", "2": "左侧面", "3": "背面", "T": "顶面"}


def _face(n: str) -> str:
    return FACE[n]


def _depth_axis(n: str, top: bool = False) -> str:
    if top:
        return "高度方向"
    return "长度方向" if n in ("1", "3") else "宽度方向"


def _silhouette(hw: float, dp: float) -> str:
    """把「看不见的那一轴比看得见的宽」说成剪影后果——探针里真正起作用的就是这一句。"""
    if dp >= hw * 1.5:
        return "；它看起来是矮而方的一块，**不是细长的一条**"
    if dp * 1.5 <= hw:
        return "；它看起来比另两张都宽"
    return ""

def card_md(o: dict) -> str:
    key, name, size = o["key"], o["name"], o["size"]
    folder = f"{key}_{name}"
    dims = "宽 %g × 长 %g × 高 %g 米" % tuple(size)
    out = [f"# {name} · {key}（物件白模源）", "",
           f"> **它是什么**：{o['desc']}", ">",
           f"> **出现在**：{'、'.join(o['scene'])}",
           f"> **真实尺寸**：{dims}（`object.toml` 的 `尺寸`，白模闸门按它等比缩放）",
           f"> **朝向**：正面朝 `{o['front']}`（归一化目标；`object.toml` 的 `目标朝向`）", "",
           "本卡是**工装卡**，不是入画的画面卡：这三张图是喂 image-to-3D 的原料，",
           "按 sk1 divergence #18 一律**正交 + 阴天均匀光**，与 follow-up 014 的 GoT 实拍画风无关。", "",
           "---", "", "## 开工顺序", "",
           f"1. 先出 **`{key}-1` 正面**（纯文字生成）——**它就是那张参考**，形制、比例、部件位置由它定死。",
           f"2. 再出 **`{key}-2` 侧面 / `{key}-3` 背面**，两张都把 `{key}-1` 放进参考槽、**只换机位**。",
           f"3. 三张齐了（自动出图：`python tools/image_fetch.py --object {key}`），跑：", "",
           "```bash",
           f"python tools/hyper3d_fetch.py --tier Regular --bbox %g %g %g \\" % tuple(size),
           f"  --image ai_videos/shikong_lvxing/sk1/2_世界观人设/props/{folder}/{key}-1.png \\",
           f"  --image ai_videos/shikong_lvxing/sk1/2_世界观人设/props/{folder}/{key}-2.png \\",
           f"  --image ai_videos/shikong_lvxing/sk1/2_世界观人设/props/{folder}/{key}-3.png \\",
           f"  --out ai_videos/shikong_lvxing/sk1/2_世界观人设/props/{folder}/whitemodel/raw.glb",
           "",
           "blender -b --factory-startup --python tools/whitemodel_normalize.py -- \\",
           f"  --src ai_videos/shikong_lvxing/sk1/2_世界观人设/props/{folder}/whitemodel/raw.glb \\",
           f"  --spec ai_videos/shikong_lvxing/sk1/2_世界观人设/props/{folder}/object.toml \\",
           f"  --out ai_videos/shikong_lvxing/sk1/2_世界观人设/props/{folder}/whitemodel/{folder}.blend",
           "```", "",
           f"4. 白模落盘后重跑 `tools/build_bianjing.py`——`resolve_asset` 会自动把 `{key}` 的同尺寸替身",
           "   换成真网格，shot previz 跟着变，**布局代码一个字都不用改**。", "",
           "---", ""]
    v2 = VIEW2_ISO if o.get("view2") == "四分之三" else VIEWS[1]
    views = [VIEWS[0], v2, VIEW3_TOP if o.get("view3") == "俯视" else VIEWS[2]]
    for n, vname, vlabel, facing, cam, (hi_, vi_), block in views:
        rk = f"{key}-{n}"
        is_top = vlabel == "俯视图"
        is_iso = vlabel == "四分之三视角图"
        hw, vh, dp = size[hi_], size[vi_], _depth(n, size, is_top)
        view_line = ((
            f"视图: {vlabel}——{facing}。主体的三个方向"
            f"（宽 {size[0]:g} × 长 {size[1]:g} × 高 {size[2]:g} 米）"
            f"**在这一张里都看得见**，比例要对得上；"
            f"这是三张里唯一带透视的一张。"
            f"**本图不是{block[0]}、也不是{block[1]}。**") if is_iso else
            f"视图: 正交{vlabel}——{name}的{_face('T' if is_top else n)}**笔直正对镜头**，"
                     f"画面里只看得到{_face('T' if is_top else n)}这一面。"
                     f"主体{_depth_axis(n, is_top)}上的 {dp:g} 米完全朝着镜头、一点也看不见；"
                     f"所以画面里主体的外轮廓是 **{hw:g} 米（左右）× {vh:g} 米（上下）**、{_shape(hw, vh)}"
                     f"{'' if is_top else _silhouette(hw, dp)}。**本图不是{block[0]}、也不是{block[1]}。**")
        out += [f"## 视图 {n} · {vname}（{vlabel}）", "",
                f"**路由键**：`{rk}`（prompt 首行就是它，导入器按它落位）　**落盘**：`{folder}/{rk}.png`",
                "**上传**：" + ("无（纯文字自由生成 —— 本图就是那张参考）" if n == "1"
                              else f"`{folder}/{key}-1.png`（本物件正视图·定形制与比例）"), "",
                "```text",
                f"{rk}_{name}{vname}",
                view_line,
                ("参考: 无" if n == "1" else f"参考: `{folder}/{key}-1.png(本物件正视图·形制与比例)=>@`"),
                ("参考用法: 本图不挂参考图，形制全部由下面的文字定；它是后两张的唯一参考。" if n == "1"
                 else f"参考用法: 参考图是本物件的正视图，定形制、比例与各部件位置；本图**只把相机挪到{vlabel}的位置**{'（抬到主体正上方、垂直向下看）' if is_top else ('（挪到右前上方，不是正侧面）' if is_iso else '（绕竖直轴）')}，"
                      f"其余一律照它；冲突时以参考图为准。**不要复制参考图的取景**——照抄参考图的外轮廓就是这张图做废了。"),
                f"主体: 【{vlabel}·{facing}】{name}——{o['desc']}",
                f"形体规格: 整体约{dims}；{o.get('spec', '各部件比例照参考图')}",
                f"识别特征: {o.get('id', '、'.join(o['parts']))}",
                f"材质细节: {o.get('mat', '素木灰褐、不上漆；铁件发黑；麻绳捆扎处留绳头')}",
                f"机位: {cam}（正交，相机光轴严格垂直于该面）",
                f"场景: {ISO_SCENE if is_iso else ORTHO}",
                "比例: 1:1（正方形画幅，主体居中）",
                "```", "",
                "**反向提示词**（粘进平台的负向框，不要并进正向）：", "",
                "```text", (ISO_NEG if is_iso else ORTHO_NEG) + f", {block[0]}, {block[1]}, 四分之三视角, 斜角透视, "
                f"把看不见的进深画成左右方向的宽度, 外轮廓比 {hw:g}:{vh:g} 更细长的剪影"
                + ("" if n == "1" else ", 与参考图相同的取景"),
                "```", ""]
    out += ["---", "", "## 验收（`object.toml` 的探针只测体量，这几条要人眼看）", ""]
    for part in o["parts"]:
        out += [f"- [ ] **{part}** 在，且不是糊成一坨"]
    out += ["- [ ] 整体比例与 `形体规格` 对得上（不是被拉长或压扁的）",
            "- [ ] 没有多生出来的部件、没有把背景当成几何吸进来",
            "- [ ] 薄件（辕、杆、栏、绳）没有被甩成碎渣——这是 image-to-3D 最不稳的地方，挂了就重掷", ""]
    return "\n".join(out)


def spec_toml(o: dict) -> str:
    key, name, size = o["key"], o["name"], o["size"]
    lines = [f"# {key}_{name} 白模规格 + 验收清单（`tools/whitemodel_normalize.py` 的输入）。",
             "#",
             "# 写一次，之后**每一次重生成**都过同一套验收——换 Rodin、换 Hunyuan3D、换买来的模型，",
             "# 验收标准不变（vendor 无关，闸门才是质量的出处）。",
             "# 区域坐标一律归一化到包围盒 0..1。", "",
             '["对象"]',
             f'"名称" = "{key}_{name}"',
             f'"中文名" = "{name}"', "",
             '["几何"]',
             '"尺寸" = [%g, %g, %g]        # X宽 × Y长 × Z高，米' % tuple(size),
             '"容差" = 0.08',
             '"最多松散块" = 60000    # 生成网格每条缝都是独立壳，几万块是常态；这条抓的是「薄件被甩成碎渣」',
             "",
             "# image-to-3D 的输出朝向是随机的；**拿到网格先渲一眼再改这里**（rule 4h §G）。",
             '"源朝向" = { "前" = "-Y", "上" = "+Z" }   # Rodin GLB 常见值，实测后按需改',
             '"目标朝向" = { "前" = "%s", "上" = "+Z" }' % o["front"], ""]
    lines += ["# ---- 占位探针：只判定「这个部件在不在」，判定不了表面质量与拓扑。",
              "# 阈值先给下限占位值；首个被人眼接受的网格落地后，按那一版实测收紧，那一版即回归基线。"]
    for part in o["parts"]:
        lines += ["", "[[\"验收\"]]", f'"名称" = "{part}"', '"类型" = "占位"',
                  '"区域" = { z = [0.00, 1.00] }   # ⚠ 待收紧：按该部件在包围盒里的实际位置改',
                  '"最少顶点" = 3', '"最少面积占比" = 0.004']
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", default="", help="逗号分隔的 pN，只处理这几个")
    args = ap.parse_args()
    only = {s.strip() for s in args.only.split(",") if s.strip()}
    made = []
    for o in load():
        if only and o["key"] not in only:
            continue
        folder = PROPS / f"{o['key']}_{o['name']}"
        md, spec = folder / f"{o['key']}_{o['name']}.md", folder / "object.toml"
        made.append(f"{o['key']}_{o['name']}")
        if args.check:
            continue
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "whitemodel").mkdir(exist_ok=True)
        md.write_text(card_md(o), encoding="utf-8")
        if not spec.is_file():          # 已存在就不覆盖：阈值是人调过的，重跑不该抹掉
            spec.write_text(spec_toml(o), encoding="utf-8")
    print(f"{'校验' if args.check else '生成'} {len(made)} 个物件文件夹：")
    for m in made:
        print("  props/" + m)


if __name__ == "__main__":
    main()
