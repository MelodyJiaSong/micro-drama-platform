# -*- coding: utf-8 -*-
"""物件流水线驱动：三视图齐了就立刻转 3D，不等全部出完。

为什么要单独一个驱动
------------------
出图是**网络等待**（每张约 50 s），Hyper3D 生成也是网络等待，白模闸门是**本地 CPU**。
让它们串成一条队列，等于把三段互不相干的等待加起来。本文件做的事只有一件：
**盯着 `props/`，谁的三视图齐了就立刻推它往下走**，与出图进程并行。

为什么闸门走 `--fit stretch`（2026-09-17 sk1 实测定的）
----------------------------------------------------
`whitemodel_normalize` 默认等比缩放，为的是让「生成网格的比例对不对」仍然能被验收发现。
但实测下来，Rodin 对**高长径比**物体是**系统性地压方**的：漕船声明 18 × 4.5（4:1），
三张正交视图都正确，出来的网格仍是 1.25:1；表木（0.6 × 0.6 × 7.5）同理。
换句话说这不是「这一版没掷好、重掷一次」，是 vendor 的固有行为，等比缩放只会让每个
细长物件永远卡在闸门上。而白模的唯一消费者是 previz —— 它要的是**真实世界尺寸下的
体量与轮廓**，不是舱门窗格的比例。所以逐轴贴合到声明包围盒是对的取舍；
代价（比例读数）没有被藏起来：闸门改报 `来源比例漂移` 这一条 warning，
且每个白模自动出三张 `peek_*.png` 快照（rule 4h §G 那一眼）。

每个物件的四步（都幂等，产物在就跳过）：
    1. `hyper3d_fetch` 拿 `pN-1/-2/-3.png` + 英文 prompt + bbox → `whitemodel/raw.glb`
    2. `whitemodel_normalize`（Blender）按 `object.toml` 归一化 + 验收 → `whitemodel/pN_{名}.blend`
    3. `mesh_peek`（Blender）出 `whitemodel/peek_{iso,top,side}.png` —— 给人看的那一眼
    4. 白模落盘后，`build_bianjing.py` 的 `resolve_asset` 下次重建就自动把同尺寸替身换成它

用法（仓库根目录）：
    python tools/build_objects.py            # 把当前已就绪的都推一遍，然后退出
    python tools/build_objects.py --watch    # 常驻，边出图边转（与 image_fetch 并行跑）
    python tools/build_objects.py --only p12,p14
    python tools/build_objects.py --tier Regular   # 默认 Regular；探形状可用 Sketch

**Blender 调用天然串行**（本文件一个循环里顺序跑），不会出现 rule 4h ⑥ 说的 previz 批量重叠。
"""
from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
import time
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import view_check

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SK1 = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "2_世界观人设"
PROPS = SK1 / "props"
BLENDER = Path(r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe")


def inventory() -> list[dict]:
    return tomllib.loads((SK1 / "object_inventory.toml").read_text(encoding="utf-8"))["object"]


# 超过这个长径比就不送 image-to-3D（2026-09-17 sk1 实测定的，rule 4g ② 的机械化）
#
# 生成式重建给不出高长径比：漕船声明 18 × 4.5 × 3（6.0），三张正交视图都正确，
# Rodin 出来仍是 1.25:1 的一坨；等比缩放过不了包围盒，逐轴拉伸又会把斜放的桅杆
# 抻成一根穿出画面的长刺，白模比替身盒还糟。表木（12.5）、青布幌（36）同理。
#
# 关键是**这些东西本来就不该走生成**：幌子/立招/窗扇/闸门/木桥/表木是近平面或近线性的，
# 对它们来说 `resolve_asset` 的同尺寸替身盒**不是近似、就是正确形状**——一块板就是一块板。
# 所以跳过它们不是降级，是把 rule 4g ②「平直重复的走脚本、有机繁复的小件走生成」
# 从人眼判断变成一条可执行的判据。真要精修，写 builder 脚本，不要掷 Rodin。
SKIP_ASPECT = 6.0

# 白模闸门报出的「来源比例漂移」上限；超了就不要这个网格（见 process() 里的实测依据）
DRIFT_MAX = 2.0


def aspect(size: list[float]) -> float:
    return max(size) / max(min(size), 1e-9)


def folder_of(key: str) -> Path | None:
    hits = sorted(PROPS.glob(f"{key}_*"))
    return hits[0] if len(hits) == 1 else None


def views_ready(fold: Path, key: str) -> list[Path]:
    got = [fold / f"{key}-{n}.png" for n in (1, 2, 3)]
    return got if all(p.is_file() and p.stat().st_size > 10000 for p in got) else []


def run(cmd: list[str], log: Path) -> bool:
    with log.open("w", encoding="utf-8") as fh:
        r = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, text=True)
    return r.returncode == 0



AXES = ("X", "Y", "Z")
# 置换要比"不转"好这么多才采纳（log 比例和；0.35 ≈ 某一轴差 1.4 倍）
SWITCH_MARGIN = 0.35


def probe_bbox(mesh: Path, logs: Path) -> tuple[float, float, float] | None:
    """量 raw 网格的包围盒。image-to-3D 的输出朝向是随机的，不量就只能猜。"""
    log = logs / (mesh.parent.parent.name + "_bbox.log")
    run([str(BLENDER), "-b", "--factory-startup", "--python",
         str(REPO / "tools" / "mesh_bbox.py"), "--", str(mesh)], log)
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("BBOX "):
            return tuple(float(v) for v in line.split()[1:4])
    return None


def detect_orientation(dims: tuple[float, float, float], size: list[float]) -> tuple[str, str]:
    """由「实测包围盒」与「声明尺寸」的长宽高比例，反推源朝向的 前 / 上。

    为什么要自动判：`object.toml` 的 `源朝向` 是生成器写的默认猜测（`前 -Y / 上 +Z`），
    而 Rodin 每次输出的朝向是随机的。p13 实测踩到过——杆子躺在 Y 上，按默认值旋转之后
    包围盒变成 7 × 93 × 7.5 m，闸门直接判死。比例匹配是机械的，比人逐个渲图去看快得多。

    只判轴、不判正负：包围盒对 180° 掉头是瞎的，那一类要靠 `object.toml` 里的截面对比探针抓。

    **证据不够强就不转**（2026-09-17 sk1，油纸伞踩到）：伞声明 2.4 × 2.4 × 2.6、
    实测 1.739 × 1.892 × 1.745 —— 近乎立方，三个轴的比例几乎一样，谁当"上"都差不多，
    于是最优解挑了最长的 Y，把伞整个放倒了。近立方物件的包围盒**本来就不含朝向信息**，
    这时候该信的是 glTF 导入器：它已经把 Y-up 转成了 Blender 的 Z-up，恒等映射
    （前+Y 上+Z）通常就是对的。所以只有当某个置换**明显**比恒等映射更贴合时才换。
    """
    import math
    want = [float(v) for v in size]                 # [X宽, Y长, Z高]，目标朝向 上=+Z 前=+Y

    def score_of(fwd: int, up: int) -> float:
        side = 3 - up - fwd
        got = [dims[side], dims[fwd], dims[up]]      # 摆成 宽 / 长 / 高
        if min(got) <= 1e-9:
            return math.inf
        gm, wm = max(got), max(want)
        return sum(abs(math.log((g / gm) / (w / wm))) for g, w in zip(got, want))

    ident = score_of(1, 2)                           # 前+Y 上+Z ＝ 不转
    best, best_score = ("+Y", "+Z"), ident
    for up in range(3):
        for fwd in range(3):
            if fwd == up:
                continue
            s = score_of(fwd, up)
            # 只有明显更好才换；差不多好就留在恒等映射上（见 docstring）
            if s < best_score - SWITCH_MARGIN:
                best_score, best = s, ("+" + AXES[fwd], "+" + AXES[up])
    return best


def rodin_prompt(o: dict) -> str:
    """Rodin 只吃英文。三张参考图已经把形状钉死了，文字只用来定题材与材质大方向。"""
    return (f"{o['en']}. Northern Song dynasty Chinese, historically accurate, "
            f"plain weathered materials, no text, no signage, no people, no ground plane, no background. "
            f"Single object only, matching the three orthographic reference views exactly.")


def process(o: dict, tier: str, logs: Path) -> str:
    key = o["key"]
    fold = folder_of(key)
    if fold is None:
        return "no-folder"
    if aspect(o["size"]) >= SKIP_ASPECT:
        return "proxy-box"
    # 清单里挂了 `skip3d = "理由"` 的，直接判替身盒，一次 Rodin 也不掷。
    #
    # 为什么需要它（2026-09-18 p22 素木床榻踩出来的）：此前「这个物件不走生成」这件事只能靠
    # **whitemodel/ 里有没有 raw.glb** 来表达，而那个状态是本文件自己会改写的 —— 删掉 blend 想让它
    # 退回替身盒，下一次全量跑又拿留着的 raw.glb 重新过一遍闸门、把同一个坏网格重新放行；
    # 连 raw.glb 一起删，则每跑一次全量就重掷一次 Rodin。两头都不对。判据属于清单，不属于产物目录。
    if o.get("skip3d"):
        return "proxy-box"
    imgs = views_ready(fold, key)
    if not imgs:
        return "waiting"
    # 三视图塌成一个轴 → 走替身盒，不送 Rodin。
    #
    # 试过一版「降级成单视图」（只留画对了的那张，方向交给 prompt 与 bbox_condition），
    # 实测出来的 p27 挑担货筐是坏网格：扁担穿过筐身、一只筐塌成一张片。
    # 两张重复方向的图固然没用，可**一张图本来就重建不出第二个方向**——
    # 生成式不会凭空补出它没看见的那一维。所以这一档只能退回替身盒。
    #
    # 为什么用机检结果路由、而不是用长径比去预测：长径比只是个相关量。
    # p12 漕船(6.0) 与 p27 挑担(4.0) 都塌了，可 p18 杈子(4.8)、p22 床榻(3.3) 不一定
    # ——那要看这一面在现实里是不是一个"人会去拍的角度"，不是看数字。
    # 既然已经有机检能**直接量**到底塌没塌，就不该再退回去猜。
    vc = view_check.check(o)
    if vc["problems"]:
        (logs / f"{key}_views.log").write_text(
            chr(10).join(vc["problems"] + vc["warnings"]), encoding="utf-8")
        return "proxy-box"
    wm = fold / "whitemodel"
    wm.mkdir(exist_ok=True)
    blend = wm / f"{fold.name}.blend"
    if blend.is_file():
        return "done"
    raw = wm / "raw.glb"
    if not raw.is_file():
        print(f"  → {fold.name}：三视图齐，送 Hyper3D…", flush=True)
        cmd = [sys.executable, "-u", str(REPO / "tools" / "hyper3d_fetch.py"),
               "--tier", tier, "--prompt", rodin_prompt(o),
               "--bbox", *[str(v) for v in o["size"]], "--out", str(raw)]
        for p in imgs:
            cmd += ["--image", str(p)]
        if not run(cmd, logs / f"{key}_rodin.log"):
            return "rodin-failed"
    if not raw.is_file():
        return "rodin-no-output"
    dims = probe_bbox(raw, logs)
    fwd, up = detect_orientation(dims, o["size"]) if dims else ("-Y", "+Z")
    print(f"  → {fold.name}：实测包围盒 {tuple(round(v, 3) for v in dims) if dims else '?'}"
          f" → 源朝向 前{fwd} 上{up}；过白模闸门…", flush=True)
    cmd = [str(BLENDER), "-b", "--factory-startup", "--python",
           str(REPO / "tools" / "whitemodel_normalize.py"), "--",
           "--src", str(raw), "--spec", str(fold / "object.toml"), "--out", str(blend),
           "--src-forward", fwd, "--src-up", up, "--fit", "stretch"]
    if not run(cmd, logs / f"{key}_gate.log"):
        return "gate-failed"
    if not blend.is_file():
        return "gate-no-output"
    # 漂移过大 ＝ 生成网格的形状离声明太远，出来的东西比同尺寸替身盒还糟 —— 退回替身盒。
    # 阈值 2.0 由实测卡出来：p37 石门枕 1.47 形态对（略钝但认得出）、p21 辘轳 1.43 对；
    # p44 长条木凳 2.84 出来是一堆带尖刺的框、p22 素木床榻 3.37 是一块带枕头疙瘩的板、四条腿没了。
    # 白模的唯一消费者是 previz，替身盒至少体量与轮廓是准的；坏网格连这个都不保。
    m = re.search(r"最大÷最小 = ([0-9.]+)", (logs / f"{key}_gate.log").read_text(encoding="utf-8", errors="replace"))
    if m and float(m.group(1)) > DRIFT_MAX:
        print(f"  ! {fold.name}：来源比例漂移 {m.group(1)} > {DRIFT_MAX}，网格形状离声明太远，退回替身盒", flush=True)
        blend.unlink()
        return "proxy-box"
    # rule 4h §G：出了模型必须先渲一眼。闸门量不出「长得像不像」，这三张快照量得出。
    run([str(BLENDER), "-b", "--factory-startup", "--python", str(REPO / "tools" / "mesh_peek.py"),
         "--", str(blend.resolve()), str((wm / "peek.png").resolve())], logs / f"{key}_peek.log")
    return "done"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true", help="常驻，边出图边转")
    ap.add_argument("--only", default="")
    ap.add_argument("--tier", default="Regular", choices=("Sketch", "Regular"))
    ap.add_argument("--interval", type=int, default=60)
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    logs = REPO / ".audit" / "objects"
    logs.mkdir(parents=True, exist_ok=True)

    seen: dict[str, str] = {}
    while True:
        objs = [o for o in inventory() if not only or o["key"] in only]
        pend = 0
        for o in objs:
            # 不缓存 "done"：状态每轮都从盘上重新推（CLAUDE.md §State surfaces 第 1 条）。
            # 缓存过一次，代价是删掉白模后 watcher 再也不重建它 —— 2026-09-17 踩到。
            # process() 自己就是一次 stat，便宜得很。
            st = process(o, a.tier, logs)
            if st != seen.get(o["key"]):
                if st not in ("waiting",):
                    print(f"{o['key']}_{o['name']}: {st}", flush=True)
                seen[o["key"]] = st
            if st in ("waiting",):
                pend += 1
        done = sum(1 for v in seen.values() if v == "done")
        skip = sum(1 for v in seen.values() if v == "proxy-box")
        bad = {k: v for k, v in seen.items() if v not in ("done", "waiting", "proxy-box")}
        print(f"[{time.strftime('%H:%M:%S')}] 白模 {done}/{len(objs) - skip}"
              f"　替身盒 {skip}　等图 {pend}"
              + (f"　异常 {bad}" if bad else ""), flush=True)
        if not a.watch or (pend == 0 and not bad):
            break
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
