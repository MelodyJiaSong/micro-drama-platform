"""K8/K18 机械校验：shot prompt 的 `角色:` 行造型段是否与角色卡锁定描述符 byte-identical。

来源：2026-07-28 follow-up 124 —— EP8 整集把锁定串写成自由发挥的简写
（裴霆「玄黑铠甲常服」实为苍青襕袍、云鹤「灰白道袍拂尘」实为玄青鎏金道袍佩剑…），
成片服装与前 7 集不一致。K8 一直是 blocker，但靠人眼比对必然漏；本脚本让它可执行。

用法:
    python tools/check_locked_descriptors.py <drama>            # 全剧
    python tools/check_locked_descriptors.py <drama> ep08       # 单集
退出码 1 = 存在漂移。
"""

import glob
import io
import os
import re
import sys

CARD_ROOT = "2_世界观人设/characters"
SHOT_ROOT = "5_6_分镜与prompt/episodes"
# 锁定描述符在角色卡 rule-10 表格行内；取该行最后一个表格单元
LOCK_ROW = re.compile(r"\|\s*10\s*\|.*?\|\s*([^|]+?)\s*\|\s*$", re.M)
ROLE_LINE = re.compile(r"^角色: `")


def load_locks(drama_dir: str) -> dict[str, str]:
    locks: dict[str, str] = {}
    for card in glob.glob(os.path.join(drama_dir, CARD_ROOT, "*", "*.md")):
        folder = os.path.basename(os.path.dirname(card))
        if os.path.splitext(os.path.basename(card))[0] != folder:
            continue
        m = LOCK_ROW.search(io.open(card, encoding="utf-8").read())
        if not m:
            continue
        value = m.group(1).strip()
        if " — " not in value:
            continue
        name, descriptor = value.split(" — ", 1)
        locks[name.strip()] = descriptor.strip()
    return locks


def scan(drama_dir: str, locks: dict[str, str], ep: str | None) -> list[tuple[str, int, str, str]]:
    pattern = os.path.join(drama_dir, SHOT_ROOT, ep or "ep*", "shots", "*", "shot*.md")
    drifts: list[tuple[str, int, str, str]] = []
    for shot in sorted(glob.glob(pattern)):
        for lineno, line in enumerate(io.open(shot, encoding="utf-8").read().splitlines(), 1):
            if not ROLE_LINE.match(line):
                continue
            for name, lock in locks.items():
                for m in re.finditer(re.escape(name) + r" — ([^、；`／]+)", line):
                    got = m.group(1).strip()
                    if not got.startswith(lock):
                        drifts.append((os.path.relpath(shot, drama_dir), lineno, name, got))
    return drifts


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    drama_dir = os.path.join("ai_videos", argv[0])
    ep = argv[1] if len(argv) > 1 else None
    locks = load_locks(drama_dir)
    if not locks:
        print(f"no locked descriptors found under {drama_dir}/{CARD_ROOT}")
        return 2
    drifts = scan(drama_dir, locks, ep)
    for path, lineno, name, got in drifts:
        print(f"DRIFT {path}:{lineno} | {name}")
        print(f"      want: {locks[name]}")
        print(f"      got : {got}")
    scope = ep or "all eps"
    print(f"\n{len(locks)} locked characters | {scope} | drift: {len(drifts)}")
    return 1 if drifts else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
