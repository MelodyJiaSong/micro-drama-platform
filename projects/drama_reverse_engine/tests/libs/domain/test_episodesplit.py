from __future__ import annotations

import pytest

from libs.domain.value_objects.episodesplit__valueobject import fuse_episode_boundaries


def test_short_file_is_single_episode() -> None:
    spans = fuse_episode_boundaries(120.0, [])
    assert len(spans) == 1
    assert spans[0].confidence == "high"


def test_blackdetect_only_cuts_are_medium_confidence() -> None:
    spans = fuse_episode_boundaries(360.0, [(118.0, 119.0), (239.5, 240.5)])
    assert [s.start_s for s in spans] == [0.0, 118.5, 240.0]
    assert all(s.confidence == "medium" for s in spans)


def test_fingerprint_corroborated_cuts_upgrade_to_high() -> None:
    spans = fuse_episode_boundaries(
        360.0, [(118.0, 119.0), (239.5, 240.5)], fingerprint_cuts=[118.0, 240.3]
    )
    assert [s.confidence for s in spans[:2]] == ["high", "high"]


def test_black_gap_too_early_is_skipped() -> None:
    spans = fuse_episode_boundaries(240.0, [(10.0, 10.5), (119.0, 120.0)])
    assert len(spans) == 2
    assert round(spans[0].end_s) == 120


def test_no_usable_cuts_falls_back_to_low_confidence_even_split() -> None:
    spans = fuse_episode_boundaries(600.0, [])
    assert len(spans) >= 2
    assert all(s.confidence == "low" for s in spans)
    assert spans[-1].end_s == pytest.approx(600.0)


def test_degenerate_tail_merged_into_previous_span() -> None:
    spans = fuse_episode_boundaries(240.6, [(119.9, 120.1), (240.4, 240.6)])
    assert spans[-1].end_s == pytest.approx(240.6)
    assert all(s.end_s - s.start_s >= 1.0 for s in spans)


def test_spans_are_contiguous_and_cover_total() -> None:
    spans = fuse_episode_boundaries(500.0, [(99.0, 100.0), (249.0, 250.0), (399.0, 400.0)])
    for a, b in zip(spans, spans[1:]):
        assert a.end_s == pytest.approx(b.start_s)
    assert spans[0].start_s == 0.0
    assert spans[-1].end_s == pytest.approx(500.0)
