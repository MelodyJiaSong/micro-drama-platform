"""The take review template carries an empty Vision item (follow-up 249: every take from 2026-10-12 answers it)."""
from __future__ import annotations

from tools import shot_take


def test_review_template_has_an_empty_vision_item_after_the_status() -> None:
    lines = shot_take.REVIEW_TEMPLATE.splitlines()
    assert "Vision：" in lines, "the reviewer fills the Vision item; left empty, audience_check --module render flags it"
    assert lines.index("Vision：") == lines.index("状态：待审核") + 2
