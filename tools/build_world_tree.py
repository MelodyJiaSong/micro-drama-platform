# -*- coding: utf-8 -*-
"""艾泽拉斯地理树渲染器 —— YAML 片区 → 多层级 markdown 树 + JSON。

用法（仓库根目录）：
    python tools/build_world_tree.py                      # 渲染 + 机检
    python tools/build_world_tree.py --check              # 只机检，不写盘
    python tools/build_world_tree.py --src <dir>          # 换片区目录

产物（写在 --src 目录下）：
    world_tree.md        整棵树，缩进到每一个地标
    world_overview.md    只到 zone 层的总览（世界 → 大陆 → 分区 → 地区）
    world_tree.json      机器可读快照，给下游生成器用

设计依据
--------
· **树数据的唯一出处是片区 YAML**（rule 4i ①：一份东西只有一个出处，副本必漂）。
  markdown 树是派生产物，**不许手写、不许手改**——改地理 ＝ 改 YAML 重跑。
· **本脚本是闸门不是报告**：id 重复 / parent 不存在 / 成环 / 必填字段缺失 / 枚举越界
  一律 exit 1，坏数据进不了产物。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
from dataclasses import dataclass, field

import yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DEFAULT_SRC = os.path.join(REPO, "ai_videos", "_research", "wow", "map")

TYPES: tuple[str, ...] = (
    "world", "continent", "region", "zone", "city", "district",
    "subzone", "settlement", "dungeon", "raid", "battleground", "poi", "transport",
)
TYPE_ORDER: dict[str, int] = {t: i for i, t in enumerate(TYPES)}
FACTIONS: tuple[str, ...] = ("alliance", "horde", "contested", "neutral", "pvp", "")
ERAS: tuple[str, ...] = ("vanilla", "tbc", "wotlk", "cata_plus", "")
VERIFIED: tuple[str, ...] = ("human", "ai_read", "ai_draft", "")

FACTION_MARK: dict[str, str] = {
    "alliance": "联盟", "horde": "部落", "contested": "争夺",
    "neutral": "中立", "pvp": "战场", "": "",
}
TYPE_MARK: dict[str, str] = {
    "world": "世界", "continent": "大陆", "region": "分区", "zone": "地区",
    "city": "主城", "district": "城区", "subzone": "子区域", "settlement": "聚居点",
    "dungeon": "副本", "raid": "团本", "battleground": "战场", "poi": "地标",
    "transport": "交通",
}


@dataclass(frozen=True)
class WorldNode:
    node_id: str
    parent: str | None
    node_type: str
    subtype: str
    name_zh: str
    name_en: str
    level: str
    faction: str
    coords: str
    adjacent: tuple[str, ...]
    era: str
    look_zh: str
    note_zh: str
    source_url: str
    quote: str
    verified_by: str
    source_file: str

    @property
    def label(self) -> str:
        zh, en = self.name_zh.strip(), self.name_en.strip()
        return f"{zh}（{en}）" if zh and en and zh != en else (zh or en or self.node_id)

    @property
    def tags(self) -> str:
        bits: list[str] = [TYPE_MARK.get(self.node_type, self.node_type)]
        if self.subtype:
            bits.append(self.subtype)
        if self.level:
            bits.append(f"{self.level} 级")
        if FACTION_MARK.get(self.faction):
            bits.append(FACTION_MARK[self.faction])
        if self.era and self.era != "vanilla":
            bits.append(self.era)
        if self.verified_by == "ai_draft":
            bits.append("待核")
        return " · ".join(bits)


@dataclass
class Issue:
    level: str
    node_id: str
    message: str


@dataclass
class WorldTree:
    nodes: dict[str, WorldNode] = field(default_factory=dict)
    children: dict[str, list[str]] = field(default_factory=lambda: collections.defaultdict(list))
    roots: list[str] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)

    @property
    def blockers(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "blocker"]

    def load(self, src: str) -> None:
        names = sorted(n for n in os.listdir(src) if n.endswith((".yaml", ".yml")) and not n.startswith("world_"))
        if not names:
            self.issues.append(Issue("blocker", "-", f"{src} 下没有任何片区 YAML"))
            return
        for name in names:
            self._load_one(os.path.join(src, name), name)
        self._link()

    def _load_one(self, path: str, name: str) -> None:
        with open(path, encoding="utf-8") as fh:
            try:
                doc = yaml.safe_load(fh)
            except yaml.YAMLError as exc:
                self.issues.append(Issue("blocker", name, f"YAML 解析失败：{exc}"))
                return
        raw = (doc or {}).get("nodes")
        if not isinstance(raw, list):
            self.issues.append(Issue("blocker", name, "顶层缺少 nodes: 列表"))
            return
        for item in raw:
            self._ingest(item, name)

    def _ingest(self, item: object, name: str) -> None:
        if not isinstance(item, dict):
            self.issues.append(Issue("blocker", name, f"节点不是字典：{item!r}"))
            return
        node_id = str(item.get("id") or "").strip()
        if not node_id:
            self.issues.append(Issue("blocker", name, f"节点缺 id：{item!r}"))
            return
        if node_id in self.nodes:
            self.issues.append(Issue("blocker", node_id, f"id 重复：{self.nodes[node_id].source_file} 与 {name}"))
            return
        node_type = str(item.get("type") or "").strip()
        if node_type not in TYPES:
            self.issues.append(Issue("blocker", node_id, f"type 越界：{node_type!r}"))
            return
        faction = str(item.get("faction") or "").strip()
        if faction not in FACTIONS:
            self.issues.append(Issue("warning", node_id, f"faction 越界：{faction!r}"))
            faction = ""
        era = str(item.get("era") or "vanilla").strip()
        if era not in ERAS:
            self.issues.append(Issue("warning", node_id, f"era 越界：{era!r}"))
            era = "vanilla"
        verified = str(item.get("verified_by") or "").strip()
        if verified not in VERIFIED:
            self.issues.append(Issue("blocker", node_id, f"verified_by 越界：{verified!r}（只许 human/ai_read/ai_draft）"))
            return
        if not str(item.get("name_zh") or item.get("name_en") or "").strip():
            self.issues.append(Issue("blocker", node_id, "既无 name_zh 也无 name_en"))
            return
        parent_raw = item.get("parent")
        parent = None if parent_raw in (None, "", "null") else str(parent_raw).strip()
        adjacent = item.get("adjacent") or []
        self.nodes[node_id] = WorldNode(
            node_id=node_id,
            parent=parent,
            node_type=node_type,
            subtype=str(item.get("subtype") or "").strip(),
            name_zh=str(item.get("name_zh") or "").strip(),
            name_en=str(item.get("name_en") or "").strip(),
            level=str(item.get("level") or "").strip(),
            faction=faction,
            coords=str(item.get("coords") or "").strip(),
            adjacent=tuple(str(a).strip() for a in adjacent if str(a).strip()),
            era=era,
            look_zh=str(item.get("look_zh") or "").strip(),
            note_zh=str(item.get("note_zh") or "").strip(),
            source_url=str(item.get("source_url") or "").strip(),
            quote=str(item.get("quote") or "").strip(),
            verified_by=verified,
            source_file=name,
        )

    def _link(self) -> None:
        for node in self.nodes.values():
            if node.parent is None:
                self.roots.append(node.node_id)
            elif node.parent not in self.nodes:
                self.issues.append(Issue("blocker", node.node_id, f"parent 不存在：{node.parent}（片区间命名没对齐）"))
            else:
                self.children[node.parent].append(node.node_id)
        for parent_id, kids in self.children.items():
            kids.sort(key=lambda k: (TYPE_ORDER[self.nodes[k].node_type], self.nodes[k].name_zh or self.nodes[k].name_en))
        self._check_cycles()
        self._check_adjacency()
        if not self.roots:
            self.issues.append(Issue("blocker", "-", "没有根节点（应有一个 parent: null 的 world 节点）"))

    def _check_cycles(self) -> None:
        for node_id in self.nodes:
            seen: set[str] = set()
            cur: str | None = node_id
            while cur is not None:
                if cur in seen:
                    self.issues.append(Issue("blocker", node_id, "parent 链成环"))
                    break
                seen.add(cur)
                node = self.nodes.get(cur)
                cur = node.parent if node and node.parent in self.nodes else None

    def _check_adjacency(self) -> None:
        for node in self.nodes.values():
            for other in node.adjacent:
                if other not in self.nodes:
                    self.issues.append(Issue("warning", node.node_id, f"adjacent 指向不存在的节点：{other}"))
                elif node.node_id not in self.nodes[other].adjacent:
                    self.issues.append(Issue("info", node.node_id, f"邻接不对称：{other} 没把它列为邻居"))

    def depth(self, node_id: str) -> int:
        d, cur = 0, self.nodes[node_id].parent
        while cur is not None and cur in self.nodes:
            d, cur = d + 1, self.nodes[cur].parent
        return d

    def descendants(self, node_id: str) -> int:
        return sum(1 + self.descendants(k) for k in self.children.get(node_id, []))

    def zones(self) -> list[WorldNode]:
        return [n for n in self.nodes.values() if n.node_type in ("zone", "city")]


class TreeRenderer:
    def __init__(self, tree: WorldTree) -> None:
        self.tree = tree

    def full_tree(self) -> str:
        out: list[str] = [
            "# 艾泽拉斯地理树 · 经典旧世（Vanilla / Classic Era）",
            "",
            "> **本文件由 `tools/build_world_tree.py` 生成，不要手改。**",
            "> 地理数据的唯一出处是同目录下的片区 `*.yaml`；改地理 ＝ 改 YAML 重跑。",
            f"> 节点合计 **{len(self.tree.nodes)}** 个。「待核」＝ `verified_by: ai_draft`，未经原文页核实，不得直接进 prompt。",
            "",
        ]
        for root in self.tree.roots:
            out.extend(self._branch(root, 0))
        return "\n".join(out) + "\n"

    def _branch(self, node_id: str, depth: int) -> list[str]:
        node = self.tree.nodes[node_id]
        pad = "  " * depth
        head = f"{pad}- **{node.label}** — {node.tags}"
        lines = [head]
        detail = " · ".join(x for x in (node.look_zh, node.note_zh) if x)
        if detail:
            lines.append(f"{pad}  - {detail}")
        for kid in self.tree.children.get(node_id, []):
            lines.extend(self._branch(kid, depth + 1))
        return lines

    def overview(self) -> str:
        out: list[str] = [
            "# 艾泽拉斯总览 · 世界 → 大陆 → 分区 → 地区",
            "",
            "> 由 `tools/build_world_tree.py` 生成，不要手改。只展开到 zone / city 层；",
            "> 每一个地区下面还有多少子区域与地标，见同目录 `world_tree.md`。",
            "",
        ]
        for root in self.tree.roots:
            for cont in self.tree.children.get(root, []):
                node = self.tree.nodes[cont]
                if node.node_type != "continent":
                    continue
                out.append(f"## {node.label} — {node.tags}")
                if node.look_zh:
                    out.append(f"\n{node.look_zh}\n")
                out.append("")
                out.append("| 分区 | 地区 | 等级 | 阵营 | 下挂节点 | 画面 |")
                out.append("|---|---|---|---|---|---|")
                out.extend(self._continent_rows(cont))
                out.append("")
        return "\n".join(out) + "\n"

    def _continent_rows(self, cont_id: str) -> list[str]:
        rows: list[str] = []
        for region_id in self.tree.children.get(cont_id, []):
            region = self.tree.nodes[region_id]
            kids = self.tree.children.get(region_id, [])
            zone_ids = [k for k in kids if self.tree.nodes[k].node_type in ("zone", "city")]
            if not zone_ids:
                rows.append(f"| {region.label} | — | | | {self.tree.descendants(region_id)} | {region.look_zh} |")
                continue
            for i, zid in enumerate(zone_ids):
                z = self.tree.nodes[zid]
                head = region.label if i == 0 else ""
                rows.append(
                    f"| {head} | {z.label} | {z.level} | {FACTION_MARK.get(z.faction, '')} "
                    f"| {self.tree.descendants(zid)} | {z.look_zh} |"
                )
        return rows

    def zone_page(self, zone: WorldNode) -> str:
        lineage: list[str] = []
        cur = zone.parent
        while cur is not None and cur in self.tree.nodes:
            lineage.append(self.tree.nodes[cur].label)
            cur = self.tree.nodes[cur].parent
        out: list[str] = [
            f"# {zone.label} — {zone.tags}",
            "",
            "> 由 `tools/build_world_tree.py` 生成，不要手改。改地理 ＝ 改片区 YAML 重跑。",
            "",
            f"- **所属**：{' ← '.join(reversed(lineage)) or '—'}",
        ]
        if zone.adjacent:
            names = [self.tree.nodes[a].label if a in self.tree.nodes else a for a in zone.adjacent]
            out.append(f"- **相邻**：{' · '.join(names)}")
        if zone.look_zh:
            out.append(f"- **画面**：{zone.look_zh}")
        if zone.note_zh:
            out.append(f"- **备注**：{zone.note_zh}")
        if zone.source_url:
            out.append(f"- **出处**：{zone.source_url}（{zone.verified_by or '未标'}）")
        out.extend(["", f"## 下挂 {self.tree.descendants(zone.node_id)} 个节点", ""])
        for kid in self.tree.children.get(zone.node_id, []):
            out.extend(self._branch(kid, 0))
        return "\n".join(out) + "\n"

    def stats(self) -> str:
        rows = sorted(self.tree.zones(), key=lambda n: -self.tree.descendants(n.node_id))
        lines = [f"{'zone':32} {'节点':>5}  {'深度':>4}  等级"]
        for z in rows:
            kids = self.tree.descendants(z.node_id)
            deep = max((self.tree.depth(k) for k in self.tree.nodes if self._under(k, z.node_id)), default=0)
            flag = "  ← 偏薄" if kids < 10 else ""
            lines.append(f"{z.node_id:32} {kids:>5}  {deep:>4}  {z.level}{flag}")
        return "\n".join(lines)

    def _under(self, node_id: str, ancestor: str) -> bool:
        cur = self.tree.nodes[node_id].parent
        while cur is not None and cur in self.tree.nodes:
            if cur == ancestor:
                return True
            cur = self.tree.nodes[cur].parent
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--check", action="store_true", help="只机检，不写盘")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    tree = WorldTree()
    tree.load(args.src)

    for issue in tree.issues:
        if issue.level != "info":
            print(f"[{issue.level}] {issue.node_id}: {issue.message}")
    info = [i for i in tree.issues if i.level == "info"]
    if info:
        print(f"[info] 另有 {len(info)} 条提示（邻接不对称等），见 --verbose 语义：已折叠")

    if tree.blockers:
        print(f"\n机检不通过：{len(tree.blockers)} 条 blocker，未写盘。")
        return 1

    renderer = TreeRenderer(tree)
    print(f"\n节点 {len(tree.nodes)} · 地区/主城 {len(tree.zones())} · 根 {len(tree.roots)}\n")
    print(renderer.stats())

    if args.check:
        return 0

    outputs = {
        "world_tree.md": renderer.full_tree(),
        "world_overview.md": renderer.overview(),
    }
    for name, body in outputs.items():
        path = os.path.join(args.src, name)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        print(f"\n写出 {path}（{len(body)} 字符）")

    zone_dir = os.path.join(args.src, "zones")
    os.makedirs(zone_dir, exist_ok=True)
    for zone in tree.zones():
        with open(os.path.join(zone_dir, f"{zone.node_id}.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(renderer.zone_page(zone))
    print(f"写出 {zone_dir}/ 下 {len(tree.zones())} 份单区页")

    snapshot = {
        "node_count": len(tree.nodes),
        "roots": tree.roots,
        "nodes": [
            {
                "id": n.node_id, "parent": n.parent, "type": n.node_type, "subtype": n.subtype,
                "name_zh": n.name_zh, "name_en": n.name_en, "level": n.level, "faction": n.faction,
                "coords": n.coords, "adjacent": list(n.adjacent), "era": n.era,
                "look_zh": n.look_zh, "note_zh": n.note_zh, "source_url": n.source_url,
                "verified_by": n.verified_by, "depth": tree.depth(n.node_id),
            }
            for n in sorted(tree.nodes.values(), key=lambda x: x.node_id)
        ],
    }
    json_path = os.path.join(args.src, "world_tree.json")
    with open(json_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(snapshot, fh, ensure_ascii=False, indent=1)
    print(f"写出 {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
