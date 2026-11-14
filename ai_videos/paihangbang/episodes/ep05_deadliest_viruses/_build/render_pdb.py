# -*- coding: utf-8 -*-
"""Claude 自己做的科学插画（follow-up 024）：用 RCSB PDB 的真实病毒衣壳原子坐标（PDB 数据 CC0）渲染高清结构图。

    python render_pdb.py <virus_key> <PDB_ID> [--size 3000] [--view 0.3 0.5 0] [--palette ...]

做法：取 Cα 原子 → 按 mmCIF 里的生物组装体（assembly 1，二十面体对称操作）铺满整个衣壳 → 正交投影，
每个 Cα 画成小球（z-buffer），按实体（蛋白种类）上色、每条链轻微变色，加球面光照、屏幕空间环境光遮蔽与
轮廓线（Goodsell 风格），深色背景。输出写进该卡候选目录 r<id>.jpg，并在 meta.json 记来源与方法。
这不是电镜照片：账本许可记「Claude-rendered from PDB <id> (CC0 data)」，屏上署名写清是结构渲染。
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import urllib.request
from pathlib import Path

import gemmi
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

BUILD = Path(__file__).resolve().parent
EP = BUILD.parent
PDB_DIR = BUILD / "pdb"
PALETTES = {   # 每个实体一个颜色（按 entity 出现顺序）
    "warm": ["#f4b942", "#e8607a", "#6cc6e8", "#9be07a", "#c792ea"],
    "cool": ["#56c2e6", "#7be08a", "#f06d8c", "#f5c451", "#b48cf2"],
    "coral": ["#ff8a65", "#ffd166", "#4dd0e1", "#ba68c8", "#81c784"],
    "violet": ["#b388ff", "#64ffda", "#ff80ab", "#ffd54f", "#4fc3f7"],
}


def hexrgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255


def fetch(pid: str) -> Path:
    PDB_DIR.mkdir(exist_ok=True)
    f = PDB_DIR / f"{pid.lower()}.cif.gz"
    if not f.exists():
        f.write_bytes(urllib.request.urlopen(f"https://files.rcsb.org/download/{pid.upper()}.cif.gz", timeout=300).read())
    return f


def beads(pid: str):
    st = gemmi.read_structure(str(fetch(pid)))
    st.setup_entities()
    model = st[0]
    sub_ent: dict[str, int] = {}
    ents = [e for e in st.entities if e.entity_type == gemmi.EntityType.Polymer]
    for k, e in enumerate(ents):
        for s in e.subchains:
            sub_ent[s] = k
    base: dict[str, tuple[np.ndarray, int]] = {}
    for ch in model:
        for res in ch:
            a = res.find_atom("CA", "*")
            if a is None:
                continue
            key = res.subchain
            base.setdefault(key, ([], sub_ent.get(key, 0)))[0].append(a.pos.tolist())
    loc_of = {k: n for n, k in enumerate(base)}   # 不对称单位里第几条链（--by chain 上色用）
    xyz, ent, cid, loc = [], [], [], []
    asm = st.assemblies[0] if st.assemblies else None
    n = 0
    gens = asm.generators if asm else []
    if not gens:
        for key, (pts, e) in base.items():
            xyz.append(np.array(pts)); ent.append(np.full(len(pts), e)); cid.append(np.full(len(pts), n)); loc.append(np.full(len(pts), loc_of[key])); n += 1
    for g in gens:
        subs = list(g.subchains) or list(base)
        for op in g.operators:
            m = np.array(op.transform.mat.tolist()); v = np.array(op.transform.vec.tolist())
            for key in subs:
                if key not in base:
                    continue
                pts, e = base[key]
                p = np.array(pts) @ m.T + v
                xyz.append(p); ent.append(np.full(len(p), e)); cid.append(np.full(len(p), n)); loc.append(np.full(len(p), loc_of[key])); n += 1
    title = st.info["_struct.title"] if "_struct.title" in st.info else pid
    return np.concatenate(xyz), np.concatenate(ent), np.concatenate(cid), np.concatenate(loc), title


def rot(ax: float, ay: float, az: float) -> np.ndarray:
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return rz @ ry @ rx


def render(xyz, ent, cid, size: int, view, palette, bead_a: float = 4.2, fill: float = 0.86) -> Image.Image:
    xyz = xyz - xyz.mean(0)
    xyz = xyz @ rot(*view).T
    rmax = np.percentile(np.linalg.norm(xyz[:, :2], axis=1), 99.9)
    scale = size * fill / 2 / rmax                     # px per Å
    R = max(2.0, bead_a * scale)                        # bead radius px
    keep = xyz[:, 2] > -0.15 * rmax                    # 只画朝向观众的一半（背面看不见）
    xyz, ent, cid = xyz[keep], ent[keep], cid[keep]
    px = xyz[:, 0] * scale + size / 2
    py = -xyz[:, 1] * scale + size / 2
    pz = xyz[:, 2] * scale
    r = int(math.ceil(R))
    oy, ox = np.mgrid[-r:r + 1, -r:r + 1]
    inside = ox ** 2 + oy ** 2 <= R * R
    ox, oy = ox[inside], oy[inside]
    dz = np.sqrt(np.maximum(0, R * R - ox ** 2 - oy ** 2))
    zbuf = np.full(size * size, -1e9, dtype=np.float32)
    owner = np.full(size * size, -1, dtype=np.int64)
    order = np.argsort(pz)
    for s in range(0, len(order), 20000):
        b = order[s:s + 20000]
        X = (np.rint(px[b])[:, None] + ox[None]).astype(np.int64)
        Y = (np.rint(py[b])[:, None] + oy[None]).astype(np.int64)
        Z = (pz[b][:, None] + dz[None]).astype(np.float32)
        ok = (X >= 0) & (X < size) & (Y >= 0) & (Y < size)
        idx = (Y * size + X)[ok]
        zz = Z[ok]
        bid = np.broadcast_to(b[:, None], X.shape)[ok]
        np.maximum.at(zbuf, idx, zz)
        win = zz >= zbuf[idx] - 1e-3
        owner[idx[win]] = bid[win]
    hit = owner >= 0
    zimg = zbuf.reshape(size, size)
    own = owner.reshape(size, size)
    # 法线与光照
    yy, xx = np.mgrid[0:size, 0:size]
    o = np.where(hit.reshape(size, size), own, 0)
    nx = (xx - px[o]) / R
    ny = (yy - py[o]) / R
    nz = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    L = np.array([-0.45, -0.55, 0.70]); L /= np.linalg.norm(L)
    lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    spec = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1) ** 24
    # 屏幕空间环境光遮蔽：比周围平均深度低的地方变暗
    zf = np.where(hit.reshape(size, size), zimg, zimg[hit.reshape(size, size)].min())
    blur = ndimage.gaussian_filter(zf, sigma=R * 2.2)
    ao = np.clip(1 - (blur - zf) / (R * 2.5), 0.25, 1.0)
    # 轮廓：相邻像素属于不同链且深度跳变
    edge = (np.abs(ndimage.sobel(zf, 0)) + np.abs(ndimage.sobel(zf, 1))) > R * 1.6
    pal = np.stack([hexrgb(c) for c in palette])
    base = pal[ent[o] % len(pal)]
    jit = ((cid[o] * 2654435761) % 1000 / 1000.0 - 0.5)[..., None] * 0.10
    col = np.clip(base + jit, 0, 1)
    depth = np.clip((zf - zf.min()) / (zf.max() - zf.min() + 1e-6), 0, 1)[..., None]
    shade = (0.28 + 0.72 * lam)[..., None] * ao[..., None] * (0.70 + 0.30 * depth)
    rgb = col * shade + spec[..., None] * 0.25
    rgb[edge] *= 0.55
    # 背景：深色径向渐变 + 衣壳外一圈柔光
    rr = np.sqrt((xx - size / 2) ** 2 + (yy - size / 2) ** 2) / (size / 2)
    bg = (np.array([0.02, 0.035, 0.05]) + np.array([0.03, 0.07, 0.08]) * np.clip(1 - rr, 0, 1)[..., None]).astype(np.float32)
    mask = hit.reshape(size, size).astype(np.float32)
    glow = ndimage.gaussian_filter(mask, sigma=size * 0.02)[..., None] * (pal[0] * 0.35)
    out = np.where(mask[..., None] > 0, rgb, bg + glow)
    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
    return img.filter(ImageFilter.SMOOTH)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("pdb")
    ap.add_argument("--size", type=int, default=3000)
    ap.add_argument("--view", type=float, nargs=3, default=[0.35, 0.55, 0.1])
    ap.add_argument("--palette", default="warm")
    ap.add_argument("--bead", type=float, default=5.0)
    ap.add_argument("--fill", type=float, default=0.86)
    ap.add_argument("--by", choices=("entity", "chain"), default="entity")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    xyz, ent, cid, loc, title = beads(a.pdb)
    img = render(xyz, loc if a.by == "chain" else ent, cid, a.size, a.view, PALETTES[a.palette], a.bead, a.fill)
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    i, it = next((i, it) for i, it in enumerate(data["items"]) if it["key"] == a.key)
    d = BUILD / "reselect" / "cand" / f"{i:02d}_{Path(it['image']).stem}"
    d.mkdir(parents=True, exist_ok=True)
    cid_ = f"r{a.pdb.lower()}_{a.palette}{a.tag}"
    f = d / f"{cid_}.jpg"
    img.save(f, quality=93)
    mp = d / "meta.json"
    rows = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else []
    rows = [r for r in rows if r["id"] != cid_] + [{
        "id": cid_, "file": f.name, "w": img.size[0], "h": img.size[1], "found_by": "claude",
        "image_url": f"https://files.rcsb.org/download/{a.pdb.upper()}.cif.gz", "page_url": f"https://www.rcsb.org/structure/{a.pdb.upper()}",
        "source": "Claude render of RCSB PDB coordinates", "author": f"Rendered by the channel (Claude) from PDB {a.pdb.upper()}",
        "licence": "AI-generated (Claude-rendered from PDB coordinates; PDB data CC0)",
        "why": f"{title}; {len(xyz):,} Cα beads, assembly 1, view {a.view}, palette {a.palette}"}]
    mp.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f, img.size, title, len(xyz))


if __name__ == "__main__":
    main()
