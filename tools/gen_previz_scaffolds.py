"""从 arc_outline.md 的分镜总表生成每镜的 previz_config.toml 骨架。

用法（仓库根目录）：
    python tools/gen_previz_scaffolds.py duikang_shangzeng
    python tools/gen_previz_scaffolds.py duikang_shangzeng --force   # 覆盖已手改的配置

契约（follow-up duikang_shangzeng/001 — previz 覆盖率 100%）：
    每一个镜头都必须有一份 previz，用途是**指导动作细节**——
    previz 的 `[["道具"."关键帧"]].t` / `[["角色"."关键帧"]].t` 就是 shot prompt 里
    `动作:` 字段时间轴的来源，两处必须一致。

四步工序：
    ① previz_config.toml → ② build_previz.py 出 .blend + 帧序列
    → ③ whitemodel_to_mp4.py 出 MP4 → ④ 上传 Seedance 的 reference_video 位
    previz 管主干动作与人物物品位置；Seedance 管全部细节渲染与特效。

设计边界（沿用 build_previz.py 的既定分工）：
    3D 只承担「机位几何 / 构图占比 / 站位朝向 / 尺度 / 遮挡 / 轨迹 / 时刻表」；
    长相、材质、光色、表演质感、次级运动、特效形态一律不碰，交 Seedance。
    唯一例外＝本片的 F80 车体几何（产品即长相），走 `形 = "模型"` 挂真实白模。

TOML 注意：中文键**必须加引号**（TOML 1.0 裸键只允许 ASCII 字母数字/下划线/连字符）。
本生成器输出的所有中文键与表头都是带引号的；`shot`/`fps`/`total_sec`/`t` 是 ASCII 键，裸写。

生成的是**骨架不是成品**：方位角、道具坐标、关键帧时刻都需要按镜手调。
骨架保证的是：合法（过 tomllib + build_previz.py 的 SCHEMA）、参数自洽
（fps/时长/焦距/分辨率/占画高与分镜表一致）、且带着本镜该有的主体与档位注释。
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

FPS = 25
RES = [2560, 1090]               # 2.35:1
# 尺寸＝[X 宽, Y 纵深, Z 高]。车头朝 +Y（画深处），故车长 4.84 落在 Y 轴。
CAR_SIZE = [2.06, 4.84, 1.14]    # Ferrari F80 实车：宽 2.06 × 长 4.84 × 高 1.14
HORSE_SIZE = [0.80, 2.40, 1.75]  # 马 proxy：宽 0.80 × 体长 2.40 × 肩高 1.75

MOVE_KINDS = ("推近", "后拉", "横移", "升降", "上摇", "下摇", "环绕")

# 景别/运镜文本 → 运镜类型。顺序敏感：先长后短。
# 注意：「跟随」不在此表——跟随镜是机位锁主体、靠主体关键帧走，不打 rig 运镜。
MOVE_MAP = [
    ("反拉", "后拉"), ("拉开", "后拉"), ("后拉", "后拉"),
    ("升高", "升降"), ("升降", "升降"),
    ("下摇", "下摇"), ("上摇", "上摇"), ("环绕", "环绕"),
    ("甩镜", "横移"), ("横移", "横移"),
    ("极缓推", "推近"), ("缓推", "推近"), ("推", "推近"),
]

PITCH_MAP = [
    ("无人机", 45.0), ("高位反拉", 22.0), ("高位俯拍", 22.0),
    ("低位仰拍", -12.0), ("贴地", -5.0), ("低位", -8.0),
]

# 景别 → 占画高（主体占画面高度的比例）
FRAME_HEIGHT = [
    ("大全景", 0.15), ("全景", 0.35), ("中近景", 0.50), ("中景", 0.55),
    ("近景", 0.70), ("大特写", 0.90), ("特写", 0.85),
]

SCENE_MAP = {
    "bg1 广场": "entropy_city", "bg2 主街": "entropy_city",
    "bg3 高架": "entropy_city", "bg4 隧道": "entropy_city",
    "bg1→bg2": "entropy_city", "bg4→bg2": "entropy_city",
    "medieval": "medieval_road", "ice_plain": "ice_plain",
    "车内": None, "转场": None, "图形层": None,
}

# 人工核定的主体在场表——inferred 之外的唯一真相
HORSE_SHOTS = {8, 19, 20, 25, 26, 27, 28, 30, 32, 34, 35, 37, 38, 41, 46, 47, 48, 49}
DRIVER_SHOTS = {9, 11, 12, 36, 43, 44, 45, 58}
NO_CAR_SHOTS = {2, 3, 4, 5, 6, 19, 53, 55, 57, 61}
# 车在本镜【静止不动】的镜：产品镜、点火前、停稳后。骨架不得给它们过画轨迹。
STATIC_CAR_SHOTS = {7, 8, 10, 13, 14, 15, 50, 58, 59, 60}


def tier_of(num: int, scene: str, focal: str, framing: str) -> tuple[str, str]:
    """返回 (档位, 档位说明)。微距标在【焦段列】，判档必须一起看。"""
    if scene == "图形层":
        return "D", "落版图形层——previz 只解版式与文字动画时刻表"
    if "微距" in focal or "微距" in framing or scene == "车内":
        return "C", "时刻表档——单主体 proxy + 动作关键帧，不建环境；previz 只解「这个动作分几拍、每拍几秒」"
    if "固定" in framing and "跟随" not in framing:
        return "B", "简化建场档——主体 proxy + 机位，无机位动画；previz 解构图占比与站位朝向"
    return "A", "完整建场档——车/马/环境体块 + 机位动画；previz 解轨迹、遮挡、尺度与时刻表"


def parse_outline(path: Path) -> list[dict]:
    rows = []
    pat = re.compile(
        r"^\|\s*(\d{2})\s*\|\s*([\d:.]+)\s*\|\s*\*{0,2}([\d.]+)\*{0,2}\s*\|"
        r"\s*([\d—-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        m = pat.match(line)
        if not m:
            continue
        num, start, fin, gen, scene, focal, framing, content = m.groups()
        rows.append({
            "num": int(num), "start": start, "fin": float(fin), "gen": gen.strip(),
            "scene": scene.strip(), "focal": focal.strip(),
            "framing": framing.strip(), "content": content.strip(),
        })
    rows.sort(key=lambda r: r["num"])
    return rows


def focal_of(text: str) -> int:
    m = re.search(r"(\d+)", text)
    return int(m.group(1)) if m else 24


def height_of(framing: str) -> float:
    for token, h in FRAME_HEIGHT:
        if token in framing:
            return h
    return 0.55


# 平移类运镜（推近/后拉/横移/升降）的默认幅度，按景别定——单位米。
# 微距镜用 8m 会直接穿过主体：85mm 特写的合理推进量是几十厘米，不是几米。
DOLLY_AMOUNT = [
    ("大全景", 12.0), ("全景", 8.0), ("中近景", 3.0), ("中景", 3.0),
    ("近景", 1.5), ("大特写", 0.3), ("特写", 0.4),
]


def moves_of(framing: str, focal: str, total: float) -> list[tuple[str, float, float, float]]:
    # 跟随镜：机位锁主体、随主体关键帧走，不打 rig 运镜（否则与主体位移双重叠加）
    if "跟随" in framing:
        return []
    for token, kind in MOVE_MAP:
        if token not in framing:
            continue
        if "甩镜" in framing:
            amt = 25.0
        elif kind in ("上摇", "下摇", "环绕"):
            amt = 30.0
        else:
            amt = next((a for tok, a in DOLLY_AMOUNT if tok in framing), 3.0)
            if "微距" in focal:
                amt = min(amt, 0.4)
        return [(kind, 0.0, total, amt)]
    return []


def pitch_of(framing: str) -> float:
    for token, deg in PITCH_MAP:
        if token in framing:
            return deg
    return 0.0


def render(row: dict, project: str, car_blend_exists: bool) -> str:
    n = row["num"]
    total = float(row["gen"]) if row["gen"].isdigit() else row["fin"]
    scene_key = SCENE_MAP.get(row["scene"])
    tier, tier_note = tier_of(n, row["scene"], row["focal"], row["framing"])
    has_car = n not in NO_CAR_SHOTS
    has_horse = n in HORSE_SHOTS
    has_driver = n in DRIVER_SHOTS
    tracking = "跟随" in row["framing"]
    static_car = n in STATIC_CAR_SHOTS
    moves = moves_of(row["framing"], row["focal"], total)

    L: list[str] = []
    L.append(f"# shot{n:02d} previz —— {row['content'][:60]}")
    L.append(f"# 成片 {row['fin']}s ／ 生成 {total}s ／ 入点 {row['start']} ／ "
             f"{row['scene']} ／ {row['focal']} ／ {row['framing']}")
    L.append(f"# 档位 {tier}：{tier_note}")
    L.append("#")
    L.append("# 坐标：+X 画右，-X 画左，+Y 画深处，Z 高度。朝向：0 面朝镜头，90 面朝画右，-90 面朝画左。")
    L.append("# ⚠ 本文件是【骨架】：方位角、道具坐标、关键帧时刻均需按镜手调（标了 TODO 的三类值）。")
    L.append("# ⚠ 关键帧的 t 必须与 shotNN.md 的 `动作:` 时间轴逐拍对齐（follow-up 001）。")
    L.append("# 重跑：blender -b --factory-startup --python tools/previz/build_previz.py -- <本文件>")
    L.append("")
    L.append('["全局"]')
    L.append(f'shot = "shot{n:02d}"')
    L.append(f'"项目" = "{project}"')
    L.append(f"fps = {FPS}")
    L.append(f"total_sec = {total}")
    if scene_key:
        L.append(f'"场景" = "{scene_key}"')
        L.append('"地面" = false')
    else:
        L.append(f'# 不挂场景主档（{row["scene"]}）：空间信息由下面的灰模摆件自己承载')
        L.append('"地面" = true')
    L.append(f'"分辨率" = [{RES[0]}, {RES[1]}]')
    L.append("")

    base = "f80" if has_car else ("horse" if has_horse else "subject")
    L.append('["机位"]')
    L.append(f'"焦距" = {float(focal_of(row["focal"]))}')
    L.append(f'"俯角" = {pitch_of(row["framing"])}')
    L.append(f'"基准主体" = "{base}"')
    L.append(f'"占画高" = {height_of(row["framing"])}')
    L.append('"横向偏移" = 0.0')
    L.append('"距离倍数" = 1.0')
    L.append('"方位角" = 25.0        # TODO 按镜调：0=正前 90=正侧 180=正后')
    if tracking or has_horse:
        L.append(f'"锁定主体" = "{base}"    # 跟随/并驾镜：机位锁主体，不打 rig 运镜')
    L.append("")

    for kind, t0, t1, amt in moves:
        L.append('[["运镜"]]')
        L.append(f'"类型" = "{kind}"        # 合法值＝{"/".join(MOVE_KINDS)}')
        L.append(f'"起" = {t0}')
        L.append(f'"止" = {t1}')
        L.append(f'"量" = {amt}            # TODO 按运镜幅度调（横移/推拉＝米，摇/环绕＝度）；已按景别给合理初值')
        L.append("")
    if not moves:
        why = "跟随镜——机位锁主体，靠主体关键帧走" if tracking else "本镜机位固定"
        L.append(f"# 无 [[\"运镜\"]]：{why}")
        L.append("")

    if has_car:
        L.append('[["道具"]]')
        L.append('"名" = "f80"')
        if car_blend_exists:
            L.append('"形" = "模型"')
            L.append(f'"档" = "ai_videos/{project}/2_世界观人设/props/f80_ferrari/f80_ferrari.blend"')
        else:
            L.append('"形" = "box"           # ← 白模就位后跑 --force，自动升级为 "模型"')
        L.append(f'"尺寸" = [{CAR_SIZE[0]}, {CAR_SIZE[1]}, {CAR_SIZE[2]}]   # 宽×长×高，车头朝 +Y，勿改')
        L.append('"色" = "红"')
        L.append('"位置" = [0.0, 0.0, 0.0]')
        L.append('"朝向" = 0.0')
        if static_car:
            pass
        if tier == "A" and tracking and not static_car:
            L.append('  # 跟随镜：车＝画框锚点，previz 里【保持原点不动】。')
            L.append('  # 机位与车同速平移时，车在画面里的位置不变——真正要 previz 定的是')
            L.append('  # 「其它主体相对车怎么动」，那部分写在马/角色的关键帧上。')
            L.append('  # 向前的绝对位移交给 Seedance（路面流动、环境掠过）。')
            L.append('  [["道具"."关键帧"]]')
            L.append("  t = 0.0")
            L.append('  "位置" = [0.0, 0.0, 0.0]')
            L.append('  [["道具"."关键帧"]]')
            L.append(f"  t = {total}")
            L.append('  "位置" = [0.0, 0.0, 0.0]   # TODO 若本镜车相对机位有进退，改这里')
        elif static_car:
            L.append('  # 本镜车【静止不动】：产品镜/点火前/停稳后。位置与角度全程零变化。')
            L.append('  [["道具"."关键帧"]]')
            L.append("  t = 0.0")
            L.append('  "位置" = [0.0, 0.0, 0.0]')
            L.append('  [["道具"."关键帧"]]')
            L.append(f"  t = {total}")
            L.append('  "位置" = [0.0, 0.0, 0.0]')
        elif tier == "A":
            L.append('  # 固定机位过画镜：车的轨迹＝本镜动作时间轴。')
            L.append('  # t 必须与 shotNN.md `动作:` 的分拍一致。')
            L.append('  [["道具"."关键帧"]]')
            L.append("  t = 0.0")
            L.append('  "位置" = [0.0, -25.0, 0.0]   # TODO 起幅：车在画外多远')
            L.append('  [["道具"."关键帧"]]')
            L.append(f"  t = {total}")
            L.append('  "位置" = [0.0, 25.0, 0.0]    # TODO 落幅：车出画多远')
        L.append("")

    if has_horse:
        L.append('[["道具"]]')
        L.append('"名" = "horse"')
        L.append('"形" = "box"')
        L.append(f'"尺寸" = [{HORSE_SIZE[0]}, {HORSE_SIZE[1]}, {HORSE_SIZE[2]}]   # 宽×体长×肩高，马头朝 +Y')
        # 素模化会把场景整体刷成中性灰——马若也用灰，在灰模视频里与建筑无法分辨。
        # previz 的全部意义是「一眼看清谁在哪」，主体必须用高对比色块。
        L.append('"色" = "绿"')
        L.append('"位置" = [-4.0, 0.0, 0.0]   # 铁律：马恒在画面左（-X）、不超越车（world.md §五）')
        L.append('"朝向" = 0.0')
        if tier == "A" and tracking:
            L.append('  # 跟随镜：车锚定在原点，马也必须锚定——只写【相对车】的位移。')
            L.append('  # 若马也向前跑 40m，它会几帧内冲出画面（车不动、马狂奔）。')
            L.append('  [["道具"."关键帧"]]')
            L.append("  t = 0.0")
            L.append('  "位置" = [-4.0, -3.0, 0.0]   # 起幅：略落后于车半个身位')
            L.append('  [["道具"."关键帧"]]')
            L.append(f"  t = {total}")
            L.append('  "位置" = [-4.0, 0.0, 0.0]    # 落幅：追平并驾。Y 不得为正（不超越车）')
        elif tier == "A":
            L.append('  [["道具"."关键帧"]]')
            L.append("  t = 0.0")
            L.append('  "位置" = [-4.0, -25.0, 0.0]')
            L.append('  [["道具"."关键帧"]]')
            L.append(f"  t = {total}")
            L.append('  "位置" = [-4.0, 25.0, 0.0]   # TODO 与车同速：并驾不超越')
        L.append("")

    if has_driver:
        L.append('[["角色"]]')
        L.append('"名" = "driver"')
        L.append('"色" = "青"')
        L.append('"身高" = 1.68')
        L.append('  [["角色"."关键帧"]]')
        L.append("  t = 0.0")
        L.append('  "位置" = [0.0, 0.0, 0.0]   # TODO 车内镜＝坐姿基准点；车外镜＝站位')
        L.append('  "朝向" = 0.0')
        L.append('  "姿态" = "坐"')
        L.append("")

    if not (has_car or has_horse or has_driver):
        L.append('[["道具"]]')
        L.append('"名" = "subject"')
        L.append('"形" = "box"')
        L.append('"尺寸" = [0.4, 0.4, 0.4]   # TODO 换成本镜主体的真实包围盒')
        L.append('"色" = "白"')
        L.append('"位置" = [0.0, 0.0, 0.0]')
        L.append('  # 时刻表：本镜动作分几拍、每拍几秒。t 必须与 shotNN.md `动作:` 一致。')
        L.append('  [["道具"."关键帧"]]')
        L.append("  t = 0.0")
        L.append('  "位置" = [0.0, 0.0, 0.0]')
        L.append('  [["道具"."关键帧"]]')
        L.append(f"  t = {total}")
        L.append('  "位置" = [0.0, 0.0, 0.0]   # TODO 按动作拍点补中间关键帧')
        L.append("")

    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", help="ai_videos/ 下的项目名，例如 duikang_shangzeng")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的 previz_config.toml")
    args = ap.parse_args()

    root = REPO / "ai_videos" / args.project
    outline = root / "3_大纲" / "arc_outline.md"
    if not outline.is_file():
        raise SystemExit(f"找不到分镜总表：{outline}")
    shots_root = root / "5_6_分镜与prompt" / "shots"
    car_blend = root / "2_世界观人设" / "props" / "f80_ferrari" / "f80_ferrari.blend"

    rows = parse_outline(outline)
    if not rows:
        raise SystemExit("分镜总表里没解析出任何镜头行")

    # 自检：生成的 TOML 必须能被 tomllib 解析（中文裸键会在这里当场炸）
    import tomllib
    written = skipped = 0
    tiers: dict[str, int] = {}
    for row in rows:
        d = shots_root / f"shot{row['num']:02d}"
        d.mkdir(parents=True, exist_ok=True)
        dst = d / "previz_config.toml"
        tier, _ = tier_of(row["num"], row["scene"], row["focal"], row["framing"])
        tiers[tier] = tiers.get(tier, 0) + 1
        text = render(row, args.project, car_blend.is_file())
        try:
            tomllib.loads(text)
        except tomllib.TOMLDecodeError as e:
            raise SystemExit(f"shot{row['num']:02d} 生成的 TOML 非法：{e}")
        if dst.exists() and not args.force:
            skipped += 1
            continue
        dst.write_text(text, encoding="utf-8")
        written += 1

    print(f"解析 {len(rows)} 镜 | 写入 {written} | 跳过已存在 {skipped} | TOML 自检全过")
    print("档位分布：" + "  ".join(f"{k}={v}" for k, v in sorted(tiers.items())))
    print("F80 白模 " + ("已就位（形=模型）" if car_blend.is_file()
                       else "尚未就位（形=box；白模到位后跑 --force 重生即自动升级）"))


if __name__ == "__main__":
    main()
