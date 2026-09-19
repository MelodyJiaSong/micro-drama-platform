# -*- coding: utf-8 -*-
"""Emit one `previz_config.toml` per sk3 shot that needs geometry.

Driven straight off `tools/sk3_data/shots_*.toml`, so the previz and the shot
card cannot drift: the camera's `占画高` **is** the shot's `jb` 起幅 value, which
is the same number `gen_shots_sk3.py` uses for the 景别档 gate. Two files, one
number (`ai_video.md` rule 4h ②: previz_config 是 3D 层唯一真相, 关键帧 t 与 shot md
`动作:` 时间轴逐拍对齐).

Nia starts at a per-bg anchor in `london.blend` and walks in a straight line
along that bg's axis at a real pace (1.33 m/s, the 80 m/min the route table
uses), so **how far she gets is decided by the shot's duration, not by the bg**.
The first cut hard-coded an endpoint per bg, which turned a 100 m stretch in a
20 s shot into an 18 km/h sprint — she left frame after a few frames and the
rest of the previz was an empty street. Framing itself was never the problem
(shot19 frame 2 measured her at the requested 75%); the displacement was.

That is still deliberately coarse — previz exists to solve camera path,
occlusion, scale and timing, not performance.

Run (repo root):
    python tools/gen_previz_sk3.py              # 写配置
    python tools/gen_previz_sk3.py --render     # 写配置并逐镜调 blender 渲 mp4
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "tools" / "sk3_data"
SHOTS_DIR = REPO / "ai_videos" / "shikong_lvxing" / "sk3" / "5_6_分镜与prompt" / "shots"
BLENDER = Path(r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe")
ENGINE = REPO / "tools" / "previz" / "build_previz.py"

# previz 是给人看运动/遮挡/尺度/时刻表的灰模动画，不是成片 —— 按 previz 规格给。
# 初版用 24fps + 1920×1080，单镜 27 s ＝ 648 帧，实测一镜十几分钟，38 镜要几小时。
# 实测三档：24fps/1920×1080 ＝ 23 s/帧（对象合并前）；12fps/960×540 ＝ 5.4 s/帧；
# 8fps/640×360 ＝ 下表。previz 要的是运动、遮挡、尺度、时刻表，这三样在 8fps 640p 全读得出来。
# 实测（同一场景、10 个合并对象、场景级关阴影）：约 3.1 s/帧 @640×360。
# previz 要的是运动、遮挡、尺度、时刻表 —— 6 fps 的 animatic 全读得出来，
# 而它把一个 22 s 的镜从 176 帧降到 132 帧。
FPS = 6
RES = [640, 360]
Z_STREET = 3.0          # 与 build_london.py 的 BANK_Z 一致
Z_DECK = 3.6            # 桥面顶

# 步速：w2 的路线表用的是 80 m/min ＝ 1.33 m/s（拥挤街道实际更慢）。
# **走多远由时长决定，不由 bg 决定** —— 初版给每个 bg 钉死一对端点，于是 bg6 的
# 100 m 在一个 20 s 的镜里变成 5 m/s（18 km/h 狂奔），她几帧就跑出画外，
# 后面的 previz 全是空街。起幅取景是准的（实测 shot19 第 2 帧她正好占 75%），
# 坏的是位移。
WALK_MPS = 1.33

# bg → (妮娅起点, 行走方向(单位向量前两轴), 默认焦距, 默认俯角)
# 坐标取自 build_london.py，原点＝Monument 现址；改几何就要回来改这里。
ANCHOR: dict[str, tuple[tuple[float, float, float], tuple[float, float, float], float, float]] = {
    "bg0_伦敦全城":        ((0, -140, 120), (-1.0, 0.1, 0.0), 28.0, 38.0),
    "bg1_旧伦敦桥":        ((-80, -250, Z_DECK), (0.0, 1.0, 0.0), 35.0, 2.0),
    # 起点往巷内挪 13 m：巷子跨 y −100…−40，而 `占画高 0.15` 的 24mm 要相机退到
    # 她身后约 11.5 m。从 −98 起步，相机就落在 −109.5 —— 退出了巷口、埋进泰晤士街的
    # 房子里，单帧从 3 s 涨到 30 s，整镜撞超时。从 −85 起步，相机落在 −96.5，仍在巷腔内。
    "bg2_布丁巷":          ((61.6, -85, Z_STREET), (0.0, 1.0, 0.0), 24.0, 0.0),
    "bg13_布丁巷傍晚":     ((61.6, -70, Z_STREET), (0.0, -1.0, 0.0), 35.0, 0.0),
    "bg3_客栈":            ((-6, -74, Z_STREET), (0.0, 1.0, 0.0), 28.0, 3.0),
    "bg4_泰晤士街与码头":  ((30, -100, Z_STREET), (-1.0, 0.0, 0.0), 35.0, 2.0),
    "bg5_皇家交易所内院":  ((150, 150, Z_STREET), (0.0, 1.0, 0.0), 24.0, 4.0),
    "bg6_Cheapside":       ((-60, 120, Z_STREET), (1.0, 0.0, 0.0), 35.0, 2.0),
    "bg7_旧圣保罗":        ((-320, 150, Z_STREET), (-1.0, 0.0, 0.0), 24.0, 22.0),
    "bg8_Moorfields木偶戏棚": ((0, 372, Z_STREET), (0.0, 1.0, 0.0), 35.0, 2.0),
    "bg10_伦敦全城燃烧":   ((0, -120, 90), (-1.0, 0.1, 0.0), 28.0, 32.0),
    "bg11_坎宁街":         ((20, -20, Z_STREET), (-1.0, 0.0, 0.0), 35.0, 2.0),
    "bg12_河上搬家的船":   ((-60, -190, 1.2), (-1.0, 0.1, 0.0), 32.0, 3.0),
}

# 机位标签里的方位词 → 方位角（0 正前 / 90 正侧 / 180 正后）
AZIM_HINT = (
    ("正面", 0.0), ("侧后", 140.0), ("后方", 165.0), ("斜侧", 45.0),
    ("侧", 90.0), ("低角度", 15.0), ("仰", 10.0), ("俯", 20.0),
)


def _kill_orphan_blender() -> None:
    """超时后清掉还活着的 blender。

    `subprocess.run(timeout=...)` 只杀直接子进程；blender 常常继续跑，
    然后和下一镜抢 CPU、把好镜也拖成假失败。
    """
    subprocess.run(["taskkill", "/IM", "blender.exe", "/F"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")


def load_shots() -> list[dict]:
    out: list[dict] = []
    for p in sorted(DATA.glob("shots_*.toml")):
        out += tomllib.loads(p.read_text(encoding="utf-8")).get("shot", [])
    out.sort(key=lambda s: s["n"])
    return out


# 走廊型地点：桥上房屋隧道、布丁巷。这些地方**只有沿轴的机位成立**——
# 侧向机位会被两侧的墙挡死，或者干脆把相机放到墙外（实测 shot06/09 的 30° 方位角
# 把相机摆到了桥侧面的河上，于是拍到的是对岸而不是沿桥纵深）。
# 关键词猜方位角对开阔地够用，对走廊不够；这里按 bg 直接钉死在「她背后、沿轴」。
# 真·航拍/漂流的 bg。**必须按 bg 判，不能按「占画高很小」判**——
# 初版用 `占画高 ≤ 0.03` 当航拍判据，于是 bg8 木偶戏棚、bg7 圣保罗这些
# 只是「远景」的地面镜也被加上了 120 m 的升降运镜，把人直接抬出画框，
# 引擎自检报「落幅基准主体整个在画框外」。远景 ≠ 航拍。
AERIAL_BG = {"bg0_伦敦全城", "bg10_伦敦全城燃烧", "bg12_河上搬家的船"}

CORRIDOR_BG = {"bg1_旧伦敦桥", "bg2_布丁巷", "bg13_布丁巷傍晚"}
# **必须是正后方 180°，不能"偏一点"。** 初版取 170°，想着偏 10° 免得与她共线；
# 但布丁巷只有 4 m 宽（半宽 2 m），而 `占画高 0.15` 的 24mm 广角把相机推到她身后
# 约 11.5 m —— 11.5 × sin(10°) ≈ 2.0 m，相机正好嵌进墙里。
# 后果不是穿帮而是**渲染爆炸**：shot15 变成 28 s/帧（其余镜 3.1 s/帧），
# 跑到第 11 帧撞上 30 分钟超时被杀。桥面宽 8 m 所以 06/07/09 侥幸没事。
# 跟拍镜本来就该在正后方，共线不是问题——她就在画面正中。
CORRIDOR_AZIM = 180.0


def azim_for(label: str, bg: str = "") -> float:
    if bg in CORRIDOR_BG:
        return CORRIDOR_AZIM
    for token, deg in AZIM_HINT:
        if token in label:
            return deg
    return 30.0


def config_for(s: dict) -> str:
    bg = s["bg"]
    if bg not in ANCHOR:
        return ""
    (ax, ay, az), (dx, dy, _dz), lens, tilt = ANCHOR[bg]
    dur = float(s["dur"])
    # 航拍/河上镜是飞行与漂流，不是走路——给它 8× 步速，其余按真实步速。
    speed = WALK_MPS * (8.0 if bg in AERIAL_BG else 1.0)
    frac = max(0.02, float(s["jb"][0]))
    aerial = bg in AERIAL_BG
    # **走不走、走多远，由这一镜是什么镜决定，不由 bg 决定。**
    # 第二版按时长算位移（1.33 m/s）仍然错：它给每一镜都套了「走路」，
    # 而 shot19「面包摊三档」是她站在摊前说话的 0.75 近景，却被安排走了 26.6 m，
    # 静止机位当然跟丢。景别越紧 ＝ 她越不动：
    #   占画高 ≥ 0.70（近景/特写）→ 原地，只留一点重心移动
    #   0.40–0.70（中景）        → 走三成
    #   < 0.40（全景/远景）      → 真在穿行，走满
    #   航拍（占画高 ≤ 0.03）    → **完全不动**：飞的是相机（`运镜` 的升降段），不是她；
    #     她在这些镜里其实根本不入画，留在原地只是给机位一个稳定的基准主体。
    #     让她跟着"飞" 319 m 的后果是引擎自检直接拦下：「落幅基准主体整个在画框外」。
    mobility = 0.0 if aerial else (0.05 if frac >= 0.70 else (0.30 if frac >= 0.40 else 1.0))
    reach = speed * dur * mobility
    norm = (dx * dx + dy * dy) ** 0.5 or 1.0
    bx, by, bz = ax + dx / norm * reach, ay + dy / norm * reach, az
    L = [
        "# shot%02d previz · %s" % (s["n"], s["title"]),
        "# 由 tools/gen_previz_sk3.py 从 tools/sk3_data/shots_*.toml 生成——**改镜表重跑，别手改本文件**",
        "# 占画高 ＝ 该镜 jb 起幅值（与 gen_shots_sk3.py 的景别档闸门同一个数）",
        "# ⚠️ 关键帧 t 必须与 shot%02d.md 的 `动作:` 时间轴逐拍对齐（rule 4h ②）" % s["n"],
        "# ⚠️ **本文件是骨架**：`占画高` 与时长由镜表算准，但**方位角、道具坐标、关键帧时刻仍需按镜手调**。"
        "走廊型地点（桥 / 布丁巷）的方位角已按 bg 钉死在沿轴，其余仍是按机位标签关键词猜的。",
        "",
        '["全局"]',
        'shot = "shot%02d"' % s["n"],
        '"项目" = "shikong_lvxing/sk3"',
        '"场景" = "london"',
        "fps = %d" % FPS,
        "total_sec = %.1f" % dur,
        '"地面" = false',
        '"分辨率" = [%d, %d]' % (RES[0], RES[1]),
        "",
        '["机位"]',
        '"焦距" = %.1f' % lens,
        '"俯角" = %.1f' % (tilt if not aerial else max(tilt, 30.0)),
        '"方位角" = %.1f' % azim_for(s["jbcam"][0], bg),
        '"基准主体" = "nia"',
        '"占画高" = %.3f' % frac,
        '"横向偏移" = 0.0',
        "",
        '[["角色"]]',
        '"名" = "nia"',
        '"色" = "绿"',
        '"身高" = 1.72',
        '  [["角色"."关键帧"]]',
        "  t = 0.0",
        '  "位置" = [%.2f, %.2f, %.2f]' % (ax, ay, az),
        '  [["角色"."关键帧"]]',
        "  t = %.1f" % dur,
        '  "位置" = [%.2f, %.2f, %.2f]' % (bx, by, bz),
        "",
    ]
    if aerial:
        L += ['[["运镜"]]', '"类型" = "升降"', '"起" = 0.0', '"止" = %.1f' % dur, '"量" = 120.0', ""]
    elif "推" in s.get("lens", "") or "推近" in s.get("lens", ""):
        L += ['[["运镜"]]', '"类型" = "推近"', '"起" = 0.0', '"止" = %.1f' % dur, '"量" = 8.0', ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true", help="写完配置后逐镜调 blender 渲 mp4")
    ap.add_argument("--blend-only", action="store_true",
                    help="只出每镜的 previz .blend（机位/角色/道具都已摆好），不渲 mp4。"
                         "渲染是分钟级的，建 blend 是秒级的——先把 38 个 blend 全出来，"
                         "mp4 留给一次无人值守的长跑。")
    ap.add_argument("--only", type=int, nargs="*", help="只处理这些镜号")
    args = ap.parse_args()

    shots = [s for s in load_shots() if s.get("previz")]
    if args.only:
        shots = [s for s in shots if s["n"] in args.only]
    if not shots:
        print("没有标了 previz 的镜")
        return 0

    written: list[Path] = []
    for s in shots:
        body = config_for(s)
        if not body:
            print("skip shot%02d：bg %s 没有 ANCHOR（室内镜不建几何）" % (s["n"], s["bg"]))
            continue
        d = SHOTS_DIR / ("shot%02d" % s["n"])
        d.mkdir(parents=True, exist_ok=True)
        p = d / "previz_config.toml"
        p.write_text(body, encoding="utf-8", newline="\n")
        written.append(p)
        print("wrote", p.relative_to(REPO))

    if not args.render and not args.blend_only:
        print("%d 份配置；加 --render 出 mp4，或 --blend-only 只出 blend" % len(written))
        return 0

    # 串行 —— rule 4h ⑥：previz 批量任务不许重叠跑（TaskStop 杀 shell 不杀 blender.exe）。
    # 实测这条是真的：一个以为已经停掉的旧批量仍在跑，与新批量抢同一批文件，
    # 结果是两边都在写、镜号乱序完成。开跑前先确认 blender 进程数为 0。
    ok = 0
    failed: list[str] = []
    for p in written:
        # 断点续跑：已经有完整 mp4 的镜跳过。48 字节 ＝ 只有容器头的半成品，要重渲。
        done = p.parent / ("%s_previz.mp4" % p.parent.name)
        if done.exists() and done.stat().st_size > 10_000:
            print("skip %s（已完成 %d KB）" % (p.parent.name, done.stat().st_size // 1024))
            ok += 1
            continue
        cmd = [str(BLENDER), "-b", "--factory-startup", "--python", str(ENGINE), "--", str(p)]
        if args.blend_only:
            cmd.append("--no-render")
        # encoding/errors 必须显式给：默认 text=True 用系统代码页（Windows 上是 cp1252）解码，
        # blender 的输出里有非 cp1252 字节，读取线程会抛 UnicodeDecodeError，
        # 结果 returncode 变成 1、把成功的渲染误报成失败（shot01/02 就是这么"失败"的）。
        #
        # **超时必须接住。** subprocess.run 超时是抛异常不是返回非零——没有这个 try，
        # 一个慢镜就把整批打掉：实测 shot16 卡在 1800 s 上，后面 22 个镜一个都没跑。
        # 而且超时只杀直接子进程，blender 常常还活着，必须显式清掉，
        # 否则它会和下一镜抢 CPU、制造假失败（rule 4h ⑥ 说的就是这个）。
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=1800)
        except subprocess.TimeoutExpired:
            failed.append(p.parent.name)
            print("✗ %s  超时 1800 s —— 跳过，继续下一镜" % p.parent.name)
            print("    该镜多半是机位嵌进了几何里（窄处的广角镜最常见），单帧会从 3 s 涨到 30 s")
            _kill_orphan_blender()
            continue
        tail = (r.stdout or "")[-300:].replace("\n", " ")
        if r.returncode == 0:
            ok += 1
            print("✓ %s  %s" % (p.parent.name, tail[-120:]))
        else:
            # 真正的错误常被十万行网格警告淹没——先把噪声滤掉再报最后几行
            noise = ("Warning: edge", "appears twice")
            blob = (r.stderr or "") + (r.stdout or "")
            lines = [x for x in blob.splitlines()
                     if x.strip() and not any(n in x for n in noise)]
            failed.append(p.parent.name)
            print("✗ %s  rc=%d" % (p.parent.name, r.returncode))
            for x in lines[-6:]:
                print("    " + x)
    print("previz 渲毕 %d/%d" % (ok, len(written)))
    if failed:
        print("失败 %d 个：%s" % (len(failed), ", ".join(failed)))
        print("重跑同一条命令即可续——已完成的会跳过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
