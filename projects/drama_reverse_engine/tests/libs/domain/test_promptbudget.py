from __future__ import annotations

from libs.domain.value_objects.promptbudget__valueobject import check_prompt_budget, visible_char_count


def test_chinese_ascii_punctuation_each_count_one() -> None:
    assert visible_char_count("中文abc,。@x") == 9


def test_internal_and_edge_whitespace_excluded() -> None:
    assert visible_char_count("  中 文\na\tb  ") == 4


def test_astral_plane_counts_two_utf16_units() -> None:
    assert visible_char_count("😀") == 2
    assert visible_char_count("a😀b") == 4


def test_budget_boundary_exact_limit_ok() -> None:
    assert check_prompt_budget("中" * 2000).ok


def test_budget_over_limit_fails() -> None:
    assert not check_prompt_budget("中" * 2001).ok


def test_empty_and_whitespace_only_count_zero() -> None:
    assert visible_char_count("") == 0
    assert visible_char_count(" \n\t") == 0


def test_fullwidth_space_u3000_excluded() -> None:
    assert visible_char_count("中　文") == 2


def test_whitespace_does_not_count_toward_limit() -> None:
    assert check_prompt_budget(("中" * 100 + "\n") * 20).count == 2000
