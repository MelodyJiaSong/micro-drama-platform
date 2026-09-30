# -*- coding: utf-8 -*-
"""AIGC 隐式标识：进片 take 的 `AIGC` / `UserComment` 元数据 → 写回成片 → 回读。

即梦出片的 format tags 带 `AIGC`（JSON：Label / ContentProducer / ProduceID / ContentPropagator / PropagateID）与
`UserComment`（aigc_label_type）；平台条款禁止去掉 AI 标识，而 mp4 muxer 默认只写标准键，ffmpeg 一重编码就丢。
写回用 `-movflags +use_metadata_tags`：键写进 moov/udta/meta（mdta 的 keys + ilst，与即梦源片同一布局），ffprobe 读得回。
flag 必须带「+」：ffmpeg 对带 +/- 的 flags 选项是追加，不带是覆盖——不带「+」会把 pc.DELIVER 的 `+faststart` 冲掉（实测）。
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import post_common as pc

KEY = "AIGC"
COMMENT = "UserComment"
FIELDS = ("Label", "ContentProducer", "ProduceID", "ContentPropagator", "PropagateID")
ID_SEP = ","


def format_tags(p: Path) -> dict[str, str]:
    r = subprocess.run([pc.FFPROBE, "-v", "error", "-show_entries", "format_tags", "-of", "json", str(p)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"ffprobe 读不了 {p}：{r.stderr.decode('utf-8', 'replace')[-300:]}")
    return json.loads(r.stdout).get("format", {}).get("tags", {})


def _label(raw: str, p: Path) -> dict[str, str]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit(f"{p.name} 的 {KEY} 标签不是 JSON：{raw[:120]}")


def _ids(label: dict[str, str]) -> list[str]:
    return [i for i in label.get("ProduceID", "").split(ID_SEP) if i]


def collect(takes: list[Path]) -> dict[str, str]:
    """→ 写回用的标签：`AIGC` 取第一个带标签的 take，ProduceID 换成全部 take 的（按进片顺序去重、逗号连接）；
    `UserComment` 取同一个 take 的原样。没带标签的 take 警告后跳过；全都没有就返回空（成片将不带标识，回读会报）。"""
    base: tuple[dict[str, str], dict[str, str]] | None = None
    ids: list[str] = []
    for p in dict.fromkeys(takes):
        t = format_tags(p)
        if KEY not in t:
            pc.warn(f"{p.name} 没有 {KEY} 标签，成片的 ProduceID 里不会有它")
            continue
        label = _label(t[KEY], p)
        ids += _ids(label)
        base = base or (label, t)
    if base is None:
        pc.warn(f"进片的 {len(takes)} 条 take 都没有 {KEY} 标签——成片带不上 AI 隐式标识")
        return {}
    label, t = base
    out = {KEY: json.dumps({**label, "ProduceID": ID_SEP.join(dict.fromkeys(ids))}, ensure_ascii=False)}
    if COMMENT in t:
        out[COMMENT] = t[COMMENT]
    return out


def ffmpeg_args(tags: dict[str, str]) -> list[str]:
    return ["-movflags", "+use_metadata_tags"] + [x for k, v in tags.items() for x in ("-metadata", f"{k}={v}")]


def readback(p: Path, expect: dict[str, str] | None = None) -> list[str]:
    """成片回读 → 缺失项（空列表＝通过）。只给路径：`AIGC` 在、是 JSON、五个字段都非空。
    给了 expect（collect 的结果）再逐项核对：ProduceID 一个不少、其余字段与 expect 相同、`UserComment` 原样在。"""
    got = format_tags(p)
    miss: list[str] = []
    if KEY not in got:
        miss.append(KEY)
    else:
        try:
            label = json.loads(got[KEY])
        except json.JSONDecodeError:
            label = None
        if not isinstance(label, dict):
            miss.append(f"{KEY}（不是 JSON 对象）")
        else:
            miss += [f"{KEY}.{k}" for k in FIELDS if not label.get(k)]
            if expect and KEY in expect:
                want = json.loads(expect[KEY])
                have = set(_ids(label))
                miss += [f"{KEY}.ProduceID:{i}" for i in _ids(want) if i not in have]
                miss += [f"{KEY}.{k}（{label.get(k)!r} ≠ 源 {want[k]!r}）" for k in FIELDS
                         if k != "ProduceID" and k in want and label.get(k) and label.get(k) != want[k]]
    if expect:
        miss += [k for k in expect if k != KEY and got.get(k) != expect[k]]
    return miss
