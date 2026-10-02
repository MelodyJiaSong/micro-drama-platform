# -*- coding: utf-8 -*-
"""英雄谷五尊雕像的「图先行」链路：三视图 → image-to-3D → 归一 → 场景可用的 .blend。

为什么不能 text-only 直接生成
-----------------------------
`ai_video.md` §28 实测：Rodin 的 text-only 做不了整身着装人像——
出来是**一具躺倒的光滑坨**，没有盔甲分片、没有披风，剑只剩一根棍。
判据不是「是不是人」，是「有没有大量需要语义理解才能生成的分件结构」。
工具自己的文档也写着「**image-to-3D 的正确用法是喂多视角参考图**」。

为什么三视图必须是我们**自己生成**的
------------------------------------
`divergence #108`：**权利人的官方图只进人眼、不进生成模型**。
所以喂进 Rodin 的三视图必须按锁定串纯文字自由生成、零参考图。
这恰好就是 rule 4d 「图先行、锚点图纯文字自由生成」的原意——
**那条规矩不只是为了质量，在 IP 衍生项目里它同时是合规屏障。**

为什么三视图要阴天均匀光
------------------------
rule 4d / `divergence #18`：烘进纹理的方向光会被重建**当成几何**，
在模型上留下假的凹凸。所以三视图一律阴天散射光、无投影、无戏剧光。

形制唯一出处
------------
`scenes/stormwind/_gate_research/gate_spec.md` §4 雕像清单 + §5 配色表。
**最重要的一条**：它们**不是素灰石像，是带金饰的彩石像**——
石材冷月白灰，但盔甲边饰、纹章、腰扣、袍纹一律以暗金/土金勾出（五图一致 ✅）。

用法（仓库根目录，分段跑，互不阻塞）：
    python tools/gen_statues_sk2.py --cards            # 只写卡与 prompt
    python tools/gen_statues_sk2.py --images           # 出三视图（纯网络）
    python tools/gen_statues_sk2.py --mesh             # 三视图 → Rodin GLB（纯网络）
    python tools/gen_statues_sk2.py --gate             # 归一成 .blend（开 Blender）
    python tools/gen_statues_sk2.py --only p23,p25
**`--gate` 会开 Blender，不要与别的 Blender 批次重叠**（rule 4h ⑥）。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
# 与 bg* 主体目录并列：`image_fetch.py` 只在 `scenes/*/{键}_*/` 这一层找卡，
# 放更深会找不到；而且按仓库惯例「一个目录 ＝ 一个主体」，雕像本来就是主体。
# 走**物件**链路：`image_fetch --object` 会把 `-1` 钉死、`-2/-3` 挂着它只换机位
# （该文件自述：三张正交图各自独立生成时不会互相同意，形制比例各漂各的）。
# 雕像功能上就是待建的三维物件，复用那条已验证的链路，不另起一套。
ROOT = (REPO / "ai_videos" / "shikong_lvxing" / "sk2" / "2_世界观人设" / "props")
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from blender_exe import BLENDER as _BLENDER_EXE  # noqa: E402  Blender 路径唯一出处
BLENDER = _BLENDER_EXE

# 全片共用的造型语汇与出图纪律（逐字进每条 prompt，改这里等于全改）
COMMON = (
    "一尊巨型石雕人像，立在一座八角低石台上，整体作为一件雕塑存在。"
    "石材是**冷调的月白灰**——比暖白墙石更冷更浅，表面有石灰岩的细孔与极轻的风化；"
    "**盔甲边饰、纹章、腰扣、袍纹一律以暗金／土金色勾出**——"
    "这尊像**不是素灰石像，是带金饰的彩石像**，金饰只在边线与纹样上，不是整块镀金。"
    "姿态端正、重心稳、**竖直站立**，不倾斜不躺卧。"
)
SHOOT = (
    "中性浅灰摄影棚背景，**阴天式的均匀散射光**——没有方向性硬阴影、没有戏剧光、"
    "没有轮廓光、没有彩色光，受光均匀；这是一张供三维重建使用的工装图，"
    "光影不能被烘进材质。全身入画、人像居中、底座完整可见、头顶与台下各留一点余量。"
)
NEG = (
    "任何文字, 字母, 汉字, 数字, 铭文, 碑文, logo, 水印, "
    "躺卧, 倾斜, 悬浮, 缺基座, 多个雕像, 背景建筑, 实景背景, 草地, 天空, "
    "戏剧性侧逆光, 硬投影, 彩色滤镜, 发光特效, 魔法光效, 金光, 圣光, "
    "整体镀金, 纯金像, 青铜像, 大理石抛光, 素灰无金饰, "
    "真人, 活人, 皮肤质感, 布料飘动, 动态模糊, "
    "低多边形, 卡通渲染, 塑料高光, 过饱和, 白模, 灰模, 3D 建模预览"
)

# (键, 目录名, 一句话身份, 姿态与持物, 三视图各自的机位说明)
STATUES = {
    "p23": ("p23_库德兰像", "一位矮人族长的巨型石雕",
           "双腿开立，**右臂高举过头**、手握一柄巨型风暴战锤（矩形锤头，锤面铸着族纹），"
           "锤柄斜向后下；左臂向前下方平伸、拳握。胸前一枚**圆形锤纹护章**，"
           "短裙上勾一道**闪电纹**；**长须及腹**，头盔或发冠简朴。"
           "身形矮壮：**头相对身体偏大、肩极宽、四肢短粗**，不是缩小的人类。"),
    "p24": ("p24_卡德加像", "一位大法师的巨型石雕",
           "直立，**右臂上举、手握一根极长的法杖**——杖身带数道金箍，"
           "**杖头是宽扁的斜刃／铲状**，不是球不是水晶；左臂垂于体侧。"
           "**长袍及地**，前襟一道**金色绳结纹**，束腰；身形清瘦挺拔。"),
    "p25": ("p25_图拉扬像", "一位高阶将军骑士的巨型石雕",
           "重甲直立，**双手交握于胸前、握着一柄大剑的剑柄，剑尖朝下**抵在身前。"
           "肩甲与膝甲带**羽翼形饰片**，甲面以金线勾边；披风垂于身后。"
           "身形高大端正，是全段唯一正面朝前的一尊。"),
    "p26": ("p26_丹娜斯像", "一位民兵指挥官的巨型石雕",
           "**光头、短须**，双臂弯曲，**一柄长柄战锤扛在右肩上**。"
           "腰带正中一枚**大型 H 形扣**，甲面以金线勾边；身形壮实。"),
    "p27": ("p27_奥蕾莉亚像", "一位精灵游侠队长的巨型石雕",
           "**前弓步**——左腿前屈、右腿后展；**左臂高举并向侧伸展，手上停着一只展翅猛禽**；"
           "右手持一张**长弓**、斜垂向前下方；**背后箭袋露出箭羽**。"
           "战袍上勾金色卷草纹；身形修长，**耳朵细长**。"),
}

VIEWS = [
    ("1", "正面", "正对雕像的正面，视线与雕像腰部同高，无仰角无俯角"),
    ("2", "侧面", "严格的正侧面（相机绕到雕像左手边 90 度），视线与腰部同高"),
    ("3", "背面", "严格的背面（相机绕到雕像正后方 180 度），视线与腰部同高"),
]


def prompt(key, view_no, view_name, view_cam):
    _dir, ident, pose = STATUES[key]
    return "\n".join([
        f"{key}-{view_no}_{_dir.split(chr(95))[1]}{view_name}",
        "参考: 无（纯文字自由生成）",
        f"{ident}，{view_cam}。{COMMON}",
        f"姿态与持物：{pose}",
        f"摄影：{SHOOT}",
        "比例: 画幅 1:1。",
        f"负面词: {NEG}",
    ])


def write_cards(keys):
    n = 0
    for k in keys:
        d, ident, pose = STATUES[k]
        p = ROOT / d
        p.mkdir(parents=True, exist_ok=True)
        lines = [f"# {d.split('_')[1]} · 英雄谷雕像 {k.upper()}", "",
                 f"> 形制出处：`_gate_research/gate_spec.md` §4 雕像清单 + §5 配色表。",
                 "> **参考图只进人眼、不进生成模型**（`divergence #108`）——",
                 "> 下面三条 prompt 一律**纯文字自由生成、零参考图**。", "",
                 f"- **身份**：{ident}", f"- **姿态与持物**：{pose}", ""]
        for vno, vname, vcam in VIEWS:
            lines += [f"## 视图 {vno} · {vname}", "",
                      f"- **路由键**：`{k}-{vno}`　**落盘**：`{k}-{vno}.png`", "",
                      "```text", prompt(k, vno, vname, vcam), "```", ""]
        lines += ["## 下游", "",
                  "```",
                  f"python tools/gen_statues_sk2.py --mesh --only {k}   # 三视图 → Rodin GLB",
                  f"python tools/gen_statues_sk2.py --gate --only {k}   # 归一成 .blend",
                  "```", "",
                  "归一后的 `.blend` 填进 `tools/build_gate_scene.py` 的 `STATUES` 表即可入场景。"]
        (p / f"{d}.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
        print(f"✓ {d}/{d}.md（3 条 prompt）")
        n += 1
    return n


def run(cmd, timeout=1800):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def gen_images(keys, force):
    ok = fail = 0
    for k in keys:
        d = STATUES[k][0]
        p = ROOT / d
        for vno, vname, vcam in VIEWS:
            dst = p / f"{k}-{vno}.png"
            if dst.exists() and not force:
                print(f"· {k}-{vno} 已存在，跳过")
                continue
            txt = p / f".prompt_{vno}.txt"
            txt.write_text(prompt(k, vno, vname, vcam), encoding="utf-8", newline="\n")
            rc, log = run([sys.executable, str(REPO / "tools" / "image_fetch.py"),
                           "--drama", "shikong_lvxing/sk2", "--scene", f"{k}-{vno}",
                           "--force"], timeout=900)
            if dst.exists():
                print(f"✓ {k}-{vno} {dst.stat().st_size // 1024} KB")
                ok += 1
            else:
                print(f"✗ {k}-{vno} {log.strip().splitlines()[-1][:150] if log.strip() else rc}")
                fail += 1
    return ok, fail


def gen_mesh(keys, force):
    ok = fail = 0
    for k in keys:
        d = STATUES[k][0]
        p = ROOT / d
        imgs = [p / f"{k}-{v}.png" for v, _, _ in VIEWS]
        have = [i for i in imgs if i.exists()]
        if len(have) < 2:
            print(f"· {k} 只有 {len(have)} 张视图，至少要 2 张才喂 image-to-3D，跳过")
            continue
        # 落点必须是 `{物件目录}/whitemodel/raw.glb` —— `build_sk2_whitemodels.py`
        # 的闸门只认这个位置（2026-09-21 放在 `{物件目录}/raw.glb` 导致闸门跑了 0 个）
        (p / "whitemodel").mkdir(exist_ok=True)
        raw = p / "whitemodel" / "raw.glb"
        if raw.exists() and not force:
            print(f"· {k} raw.glb 已存在，跳过")
            continue
        cmd = [sys.executable, str(REPO / "tools" / "hyper3d_fetch.py"),
               "--prompt", f"A monumental carved stone statue of {k}, standing upright on an "
                           "octagonal plinth, pale limestone with dark gold trim on the armour "
                           "edges and heraldry, museum sculpture, single figure",
               "--bbox", "1", "1", "2.6", "--tier", "Regular", "--mesh-mode", "Quad",
               "--out", str(raw)]
        for i in have:
            cmd += ["--image", str(i)]
        rc, log = run(cmd)
        if raw.exists():
            print(f"✓ {k} raw.glb {raw.stat().st_size // 1024} KB（喂了 {len(have)} 视图）")
            ok += 1
        else:
            print(f"✗ {k} Rodin 失败：{log.strip().splitlines()[-1][:160] if log.strip() else rc}")
            fail += 1
    return ok, fail


def gate(keys):
    """归一 + **先渲一眼**（rule 4h §G：没看过的网格不许往下用）。"""
    ok = 0
    for k in keys:
        d = STATUES[k][0]
        p = ROOT / d
        # 落点必须是 `{物件目录}/whitemodel/raw.glb` —— `build_sk2_whitemodels.py`
        # 的闸门只认这个位置（2026-09-21 放在 `{物件目录}/raw.glb` 导致闸门跑了 0 个）
        (p / "whitemodel").mkdir(exist_ok=True)
        raw = p / "whitemodel" / "raw.glb"
        if not raw.exists():
            print(f"· {k} 没有 raw.glb，跳过")
            continue
        rc, log = run([BLENDER, "-b", "--factory-startup", "--python",
                       str(REPO / "tools" / "glb_preview.py"), "--",
                       "--src", str(raw), "--out", str(p / f"{k}_preview.png")], timeout=900)
        print(f"{'✓' if rc == 0 else '✗'} {k} 四视图预览 -> {p.name}/{k}_preview_*.png")
        ok += rc == 0
    return ok


def main():
    ap = argparse.ArgumentParser()
    for f in ("cards", "images", "mesh", "gate", "force"):
        ap.add_argument(f"--{f}", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    keys = [x.strip().lower() for x in a.only.split(",") if x.strip()] or list(STATUES)
    keys = [k for k in keys if k in STATUES]
    if not (a.cards or a.images or a.mesh or a.gate):
        a.cards = True
    if a.cards:
        print(f"— 写卡 —\n共 {write_cards(keys)} 张")
    if a.images:
        print("— 出三视图 —")
        ok, fail = gen_images(keys, a.force)
        print(f"图：成功 {ok} 失败 {fail}")
    if a.mesh:
        print("— image-to-3D —")
        ok, fail = gen_mesh(keys, a.force)
        print(f"网格：成功 {ok} 失败 {fail}")
    if a.gate:
        print("— 预览（先看一眼再用）—")
        print(f"预览：{gate(keys)} 个")


main()
