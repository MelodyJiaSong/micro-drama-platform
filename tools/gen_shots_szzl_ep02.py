# -*- coding: utf-8 -*-
"""《圣光刚好够用》ep02 *Acting* —— 分镜 + prompt 数据（阶段 5/6）。

镜表分五段放在 `tools/szzl_ep02/shots_{a..e}.py`（S01–S11 / S12–S19 / S20–S28 / S29–S43 / S44–S49），各段的
`SHOTS` 按镜号顺序拼起来就是本集；还没写的镜列在各段的 `PENDING`。共用的键与措辞在 `szzl_ep02/common.py`。
版式、闸门、回读校验全在 `tools/szzl_shot_engine.py`（不改它）；台词、锁定串、voice_id 都在构建时从剧本 / 卡 / casting 读。

    python tools/gen_shots_szzl_ep02.py --only S01          # 只查这几镜（逗号分隔）：本镜闸门全跑，不写盘
    python tools/gen_shots_szzl_ep02.py --only S01 --print  # 同上，并把渲染出的 shot md 打到屏幕上
    python tools/gen_shots_szzl_ep02.py --only S01 --write  # 闸门全过才写这几镜的 shotNN.md（给 shot_overhead.py 出审阅图用）
    python tools/gen_shots_szzl_ep02.py                     # 整集：闸门 + 写盘 + 回读（PENDING 清空之后才放行）
    python tools/gen_shots_szzl_ep02.py --check / --verify / --materials 1,2 / --previz-config 1,2
    python tools/gen_shots_szzl_ep02.py --dialogue-stamp "…" / --viewer-stamp "…"   # 通读过后盖章（同样要写完全集）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prompt_light  # noqa: E402
import seedance_kit  # noqa: E402
import shot_logic  # noqa: E402
import szzl_shot_engine as engine  # noqa: E402
import wow_version_gate  # noqa: E402
from szzl_ep02 import shots_a, shots_b, shots_c, shots_d, shots_e  # noqa: E402

EP, GENERATOR = "ep02", "tools/gen_shots_szzl_ep02.py"

# ── ep 级表：引擎里这几张表只有 ep01 的内容，本集在这里追加（不改引擎文件）──
# 剧本说话人 → (人物卡目录 | None, casting.md 里的名字)；None ＝ 无卡、只在画外出声，不挂 entity
engine.SPEAKERS.update({
    "Dughan": ("c8_Marshal_Dughan", "Marshal Dughan"),
    "Wilhelm": ("c19_Brother_Wilhelm", "Brother Wilhelm"),
    "Lyria": ("c20_Lyria_DuLac", "Lyria Du Lac"),
    "Walt": ("c21_Walt", "Walt"),
    "Nell": ("c22_Nell", "Nell"),
    "Ben": ("c23_Ben", "Ben"),
    "Grandad": ("c24_Grandad", "Grandad"),
    "Ma Stonefield": ("c25_Ma_Stonefield", "Ma Stonefield"),
    "Bernice": ("c26_Bernice_Stonefield", '"Auntie" Bernice Stonefield'),
    "Maybell": ("c27_Maybell_Maclure", "Maybell Maclure"),
    "Tommy Joe": ("c28_Tommy_Joe_Stonefield", "Tommy Joe Stonefield"),
    "Billy": ("c29_Billy_Maclure", "Billy Maclure"),
    "Pestle": ("c30_William_Pestle", "William Pestle"),
    "Surena": ("c33_Surena_Caledon", "Surena Caledon"),
    "Gramma": (None, "Gramma Stonefield / Mildred"),      # S12 屋里画外一句，无卡
})
# 叙事字段（情节 / 动作 / 走位）点名的生物 → 必须挂的卡（rule 29）；狗头人、豺狼人按黄级规则在叙事里写描述
engine.CREATURES.update({
    "m1_Kobold": re.compile(r"鼠面"),
    "m2_Gnoll": re.compile(r"豺狼人|鬣狗"),
    "m3_Murloc": re.compile(r"鱼人"),
    "m9_Princess": re.compile(r"母猪|野猪"),
})
# previz 色块：公主是四足（PROXY 身高读作肩高，卡：肩高到成年人腰上）；鱼人一米二
engine.PROXY.update({"m9_Princess": ("粉", 1.0), "m3_Murloc": ("黄", 1.2)})
engine.QUADRUPED.add("m9_Princess")
# 引擎里按镜号记的遗留清单都是 ep01 的镜（规则变更不回溯旧剧）；ep02 全是新镜，一条也不继承
for _legacy in ("SPEAK_WINDOW_LEGACY", "DENSITY_LEGACY", "PREVIZ_ENGINE_LEGACY", "CASCADEUR_LEGACY"):
    setattr(engine, _legacy, frozenset())

MODULES = (shots_a, shots_b, shots_c, shots_d, shots_e)
SHOTS: tuple[engine.Shot, ...] = tuple(s for m in MODULES for s in m.SHOTS)
PENDING: tuple[tuple[str, float, str], ...] = tuple(p for m in MODULES for p in m.PENDING)


def coverage() -> list[str]:
    """已写 + 待写按镜号顺序恰好铺满剧本，待写的镜长逐镜等于剧本（已写的镜长由引擎闸门从剧本读）。"""
    src = engine.script_lines(EP)
    keys = [k for m in MODULES for k in [s.key for s in m.SHOTS] + [p[0] for p in m.PENDING]]
    bad = []
    if sorted(keys, key=lambda k: int(k[1:])) != list(src):
        bad.append("已写 + 待写的镜号与剧本对不上：%s / 剧本 %s" % (keys, list(src)))
    bad += ["%s 待写镜长 %gs，剧本是 %gs" % (k, secs, src[k][0]) for k, secs, _ in PENDING if k in src and secs != src[k][0]]
    return bad


def check_only(keys: list[str], show: bool, write: bool) -> int:
    """只查点名的几镜：引擎的逐镜闸门 + 产物闸门全跑。整集级的（镜号齐不齐、对白通读章、目标账本、
    状态账本、跨镜轴线与切口里涉及没点名的镜）另列，等全集写完由整集构建判。
    write：闸门全过才只写这几镜的 shotNN.md；「与前一镜的切口」只认同一次点名的上一镜（整集构建时全部重写）。"""
    subset = tuple(s for s in SHOTS if s.key in keys)
    miss = [k for k in keys if k not in {s.key for s in subset}]
    if miss:
        print("还没写（在 PENDING 里）：%s" % "、".join(miss))
        return 1
    no_ov = [s.key for s in subset if not (engine._shot_dir(EP, s) / "planning" / "overhead.toml").is_file()]
    if no_ov:
        print("没有镜头平面图（shots/shotNN/planning/overhead.toml，每镜先写它）：%s" % "、".join(no_ov))
        return 1
    mine = tuple("shot%02d" % s.n for s in subset) + tuple(s.key + " " for s in subset)
    bad, ctx = engine.gate(EP, subset)
    own = [b for b in bad if b.startswith(mine)]
    rest = [b for b in bad if not b.startswith(mine)]
    mds: dict[str, str] = {}
    try:
        mds = engine._md_by_shot(EP, subset, ctx["src"], ctx["seams"], ctx["scen"])   # 精简稿 > 2000 字在这里 raise
    except SystemExit as e:
        own.append(str(e))
    if mds:
        for g in (prompt_light.gate, engine.carry_gate, shot_logic.gate,
                  lambda m: engine.product_gates(EP, subset, m, ctx["src"]), wow_version_gate.gate):
            try:
                g(mds)
            except SystemExit as e:
                own.append(str(e))
    for b in own:
        print("  ✗ " + b)
    if rest:
        print("  （整集级 %d 条，等全集写完再判：%s）" % (len(rest), "；".join(r[:60] for r in rest)))
    for s in subset:
        md = mds.get("shot%02d" % s.n, "")
        seed = engine.seedance_block(md) or ""
        print("  shot%02d %-8s %4gs  设计稿 %4d 字  精简稿 %4d 字  previz %s" % (
            s.n, s.title, ctx["src"][s.key][0], len(prompt_light.positive(md) or ""), len(seed),
            "要" if engine.previz_needed(EP, s, ctx["src"][s.key][0])[0] else "免"))
        if show and md:
            print(md)
    print("%s %s 闸门：%s" % (EP, "、".join(keys), "不通过（%d 条）" % len(own) if own else "全过"))
    if own:
        return 1
    if write:
        paths = [engine._shot_dir(EP, s) / ("shot%02d.md" % s.n) for s in subset]
        before = {p: (p.read_bytes() if p.is_file() else None) for p in paths}
        for s, p in zip(subset, paths):
            p.write_text(mds["shot%02d" % s.n], encoding="utf-8", newline="\n")
        print("已写出 %s（shotlist.md / all_shot_prompts.md 等整集构建再写）" % "、".join(p.name for p in paths))
        ready = {}
        for s, p in zip(subset, paths):     # 资料包只给上传源文件齐了的镜建（缺平面图 ref 时 seedance_kit 建不起来）
            secs, lines = ctx["src"][s.key]
            if all(f is None or f.is_file() for _, f in engine.upload_files(EP, s, lines, engine.previz_needed(EP, s, secs)[0], secs)):
                ready[p] = before[p]
            else:
                print("  %s 资料包先不建：上传源文件不齐（--materials %d 看缺哪份；平面图 ref 由 tools/shot_overhead.py 出）" % (p.stem, s.n))
        if ready:
            seedance_kit.after_write(ready)
    return 0


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--only", default="", help="逗号分隔的剧本镜号（S01,S02）：只查这几镜")
    ap.add_argument("--print", action="store_true", dest="show", help="配合 --only：打印渲染出的 shot md")
    ap.add_argument("--write", action="store_true", help="配合 --only：闸门全过就写这几镜的 shotNN.md")
    args, rest = ap.parse_known_args(argv)
    bad = coverage()
    if bad:
        print("\n".join("  ✗ " + b for b in bad))
        return 1
    if args.only:
        return check_only([k.strip() for k in args.only.split(",") if k.strip()], args.show, args.write)
    per_shot = any(a.startswith(("--materials", "--previz-config")) for a in rest)
    if PENDING and not per_shot:
        print("还有 %d 镜待写（%s…）：整集构建 / 盖章要等全部写完；已写的镜用 --only 查" % (
            len(PENDING), "、".join(p[0] for p in PENDING[:5])))
        return 1
    return engine.run(EP, SHOTS, GENERATOR, rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
