"""AI 短剧 previz 的用户侧配置层（rule 12.16 §8，follow-up 051）。

**动机**：用户要在不读建场脚本的前提下直接调 previz——每个动作段的起止时间、机位远近角度、
动作细节（转几圈、绕多大、插多散）。所以每个 previz `.blend` 旁边配一个 `previz_config.toml`，
按「动作 1..N × 段内主体」组织；改完重跑建场脚本即生效。

**契约**
- TOML（Blender 自带 Python 3.11 的 `tomllib` 能读，支持注释；JSON 不能带注释，YAML 无内置解析器）。
- 表结构是**自由的组织层**：`[[动作]]`、`[动作.主体.XXX]` 只为了人读；加载器只认**叶子键名**，
  把叶子键平展后按规则写回建场脚本的模块常量。因此同一个键放在哪个表里都行，但**键名全局唯一**。
- 键名 = 建场脚本常量名的小写（`a_orbit0` → `A_ORBIT0`）。四类语义：
    * `a_*`    —— 第一幕绝对秒；
    * `t_*`    —— 第二幕相对秒（加载后自动加 `act2_t0`）；时长类键（在 `DURATION_KEYS` 里）不加偏移；
    * `pose_*` / `hand_*` —— **整表姿态**：表本身是值（关节名 → [X,Y,Z] 角度 / 指名 → 各节角度），整个赋给同名常量；
    * 其余     —— 普通参数（圈数/半径/比例/角度…），原样写回。
- 数组 → tuple；缺的键用脚本默认值；多出的未知键**报错**（拼错键名静默忽略是最恶劣的失败模式）。
"""
from __future__ import annotations

import tomllib
from pathlib import Path

# 时长/跨度类 t_* 键：是"多少秒"而不是"第几秒"，不加 act2_t0 偏移
DURATION_KEYS = {"t_drop_span", "t_drop_dur"}
# 组织层保留键：不是参数
META_KEYS = {"名称", "说明", "起", "止", "name", "note", "start", "end", "id"}


POSE_TABLE_PREFIXES = ("pose_", "hand_")


def _tupleize(v):
    if isinstance(v, list):
        return tuple(_tupleize(x) for x in v)
    if isinstance(v, dict):
        return {k: _tupleize(x) for k, x in v.items()}
    return v


def _walk(node, out: dict, path: str) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, dict) and k.startswith(POSE_TABLE_PREFIXES):
                if k in out:
                    raise ValueError(f"previz_config: 姿态 {k!r} 出现了两次")
                out[k] = (_tupleize(v), f"{path}.{k}" if path else k)
                continue
            _walk(v, out, f"{path}.{k}" if path else k)
    elif isinstance(node, list) and node and isinstance(node[0], dict):
        for i, v in enumerate(node):
            _walk(v, out, f"{path}[{i}]")
    else:
        leaf = path.rsplit(".", 1)[-1]
        if leaf in META_KEYS:
            return
        if leaf in out:
            raise ValueError(f"previz_config: 键 {leaf!r} 出现了两次（{out[leaf][1]} 与 {path}）——键名必须全局唯一")
        out[leaf] = (node, path)


def apply_config(
    script_globals: dict,
    config_path: str | Path,
    *,
    act2_offset_key: str = "act2_t0",
    include_prefixes: tuple[str, ...] | None = None,
    exclude_prefixes: tuple[str, ...] = (),
) -> list[str]:
    """读 TOML 并把叶子键写回建场脚本的模块常量。返回被覆盖的常量名列表。

    用法（建场脚本里，所有默认常量定义完之后、任何派生量计算之前）：
        applied = apply_config(globals(), Path(__file__).with_name("previz_config.toml"))
    """
    config_path = Path(config_path)
    if not config_path.is_file():
        return []
    with open(config_path, "rb") as fh:
        cfg = tomllib.load(fh)
    leaves: dict = {}
    _walk(cfg, leaves, "")

    act2_t0 = leaves.pop(act2_offset_key, (script_globals.get("ACT2_T0", 0.0), ""))[0]
    applied: list[str] = []
    unknown: list[str] = []
    for key, (value, where) in leaves.items():
        if include_prefixes is not None and not key.startswith(include_prefixes):
            continue
        if key.startswith(exclude_prefixes) and exclude_prefixes:
            continue
        gname = key.upper()
        if gname not in script_globals:
            unknown.append(f"{key}（在 {where}）")
            continue
        if isinstance(value, (list, dict)):
            value = _tupleize(value)
        if key.startswith("t_") and key not in DURATION_KEYS:
            value = (
                tuple(act2_t0 + v for v in value) if isinstance(value, tuple) else act2_t0 + value
            )
        script_globals[gname] = value
        applied.append(gname)
    script_globals["ACT2_T0"] = act2_t0
    if unknown:
        raise ValueError("previz_config: 未知键（拼写检查）: " + "; ".join(unknown))
    return applied
