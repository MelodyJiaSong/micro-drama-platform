"""流程与自检的共用常量与纯逻辑。

登记表与缺陷记录的**写入与闸门**只在仓库工具 `tools/qc.py`；本站只读、不执行仓库工具源码。
逃逸原因的四分法与 `tools/qc.py escape_reason` 同义——改一处必须同步另一处。
"""
from __future__ import annotations

from collections.abc import Mapping

from libs.infrastructure.daos.process_qc__dao import QcCheckDao, QcDefectDao

REPO_REGISTRY: str = ".agents/references/project/qc_checks.toml"
DRAMA_REGISTRY_NAME: str = "qc_checks.toml"
SPEC_ROOT: str = "specs/ai_video"
STAGE_ORDER: tuple[str, ...] = ("ref_image", "ref_audio", "spec", "prompt", "keyframe", "video", "audio", "cut")
MAX_BYTES: int = 8 * 1024 * 1024


def escape(defect: QcDefectDao, checks: Mapping[str, QcCheckDao], verdict: str | None) -> tuple[str, str]:
    """用户抓到的缺陷 → (为什么检查没抓到, 该做的进化动作)。`verdict` 是该产物在这条检查上的记录结论。"""
    cat = defect.category
    check = checks.get(cat)
    if cat.startswith("new:") or check is None:
        return "没有这条检查", f"在剧级登记表新增 {cat.removeprefix('new:')}，带上来源"
    if verdict is None:
        if not check.gate:
            return "有检查但不是闸门", f"把 {cat} 改成闸门"
        if not defect.artifact:
            return "闸门建立前交付", "只计入基线" + ("；还缺机检工具" if not check.auto else "")
        return "这件产物没走闸门", "查交付路径为什么没调 qc.py gate"
    if verdict == "pass":
        return "检查放过了", f"用这个例子收紧 {cat}，存进回归样本"
    if not check.auto:
        return "只靠审稿、还没自动化", f"给 {cat} 做机检工具"
    return "检查报了但仍交付", "查闸门为什么没挡住"


DEFECT_SOURCES: tuple[str, ...] = ("user", "machine", "review")   # override＝用户放行闸门结论（误报），不算缺陷


def real_defects(defects: list[QcDefectDao]) -> list[QcDefectDao]:
    return [d for d in defects if d.caught_by in DEFECT_SOURCES]


def escape_rate(defects: list[QcDefectDao]) -> float | None:
    rows = real_defects(defects)
    return sum(d.caught_by == "user" for d in rows) / len(rows) if rows else None
