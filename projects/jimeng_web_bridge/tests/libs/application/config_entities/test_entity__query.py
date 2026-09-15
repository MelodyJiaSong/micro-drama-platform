from __future__ import annotations

from datetime import timedelta

from libs.application.dtos.entity__dto import EntitySnapshotEntryCdto, ReconcileQdto, ReconcileRowQdto
from tests.libs.application.config_entities.support import FLAT, HY1, HY2, HY3, T0, Harness, config_text


def _row(result: ReconcileQdto, name: str) -> ReconcileRowQdto:
    return next(row for row in result.rows if row.name == name)


def _states(result: ReconcileQdto) -> dict[str, str]:
    return {row.name: row.state for row in result.rows}


def _hy3_with_override(harness: Harness) -> None:
    harness.write_config(HY3, config_text(harness.mapper, "hy3", {"c1_砌炉的老人": "hy3_主角"}))


def test_reconcile_three_states_across_the_series(harness: Harness) -> None:
    _hy3_with_override(harness)
    harness.sync("hy3_主角", "hy1_造家的人", "旧主体X", at=T0 - timedelta(hours=1))
    result = harness.entities.reconcile()
    states = _states(result)
    assert states["hy3_主角"] == "mapped"
    assert states["hy1_造家的人"] == "mapped"
    assert states["hy3_獾"] == "missing_on_platform"
    assert states["hy2_香蕉蛞蝓"] == "missing_on_platform"
    assert states["旧主体X"] == "unmapped_on_platform"
    assert "hy2_造家的人" not in states and "hy3_砌炉的老人" not in states
    shared = _row(result, "hy1_造家的人")
    assert [(usage.drama_rel, usage.source_drama_rel, usage.via) for usage in shared.usages] == [
        (HY1, None, "card"),
        (HY2, HY1, "card"),
    ]
    assert [row.state for row in result.rows] == sorted(
        (row.state for row in result.rows), key=["mapped", "missing_on_platform", "unmapped_on_platform"].index
    )
    assert (result.mapped_count, result.unmapped_count) == (2, 1)
    assert result.missing_count == sum(1 for row in result.rows if row.state == "missing_on_platform")
    assert [(card.drama_rel, card.character_dir, card.error_code) for card in result.unnamed_cards] == [
        (FLAT, "c1_独行者", "drama_abbrev_missing"),
    ]
    assert (result.stale, result.never_synced, result.snapshot_age_h) == (False, False, 1.0)
    assert result.config_issues == ()


def test_reconcile_filter_narrows_expected_rows_but_keeps_unmapped_global(harness: Harness) -> None:
    _hy3_with_override(harness)
    harness.sync("hy3_主角", "hy1_造家的人", "旧主体X")
    result = harness.entities.reconcile("huangye_shenghuo/hy2")
    assert result.drama_rel == HY2
    assert _states(result) == {
        "hy1_造家的人": "mapped",
        "hy2_香蕉蛞蝓": "missing_on_platform",
        "旧主体X": "unmapped_on_platform",
    }
    assert [usage.drama_rel for usage in _row(result, "hy1_造家的人").usages] == [HY2]
    assert result.unnamed_cards == ()


def test_reconcile_marks_a_snapshot_older_than_the_threshold_stale(harness: Harness) -> None:
    harness.sync("hy3_獾", at=T0 - timedelta(hours=25))
    result = harness.entities.reconcile(HY3)
    assert (result.stale, result.snapshot_age_h) == (True, 25.0)
    assert result.snapshot_synced_at == "2026-09-12T09:00:00.000000Z"


def test_reconcile_without_any_sync_reports_never_synced(harness: Harness) -> None:
    result = harness.entities.reconcile()
    assert (result.never_synced, result.stale, result.snapshot_synced_at, result.snapshot_age_h) == (True, False, None, None)
    assert result.mapped_count == 0 and result.unmapped_count == 0 and result.missing_count > 0


def test_reconcile_counts_reference_entity_overrides_as_expected(harness: Harness) -> None:
    text = config_text(harness.mapper).replace("[references.overrides]\n", '[references.overrides]\n"砌炉的老人" = "entity:旧主体X"\n', 1)
    harness.write_config(HY3, text)
    harness.sync("旧主体X")
    row = _row(harness.entities.reconcile(), "旧主体X")
    assert row.state == "mapped"
    assert [(usage.drama_rel, usage.via) for usage in row.usages] == [(HY3, "reference_override")]


def test_reconcile_falls_back_to_defaults_for_an_invalid_config_and_reports_it(harness: Harness) -> None:
    harness.write_config(HY3, config_text(harness.mapper).replace("count = 1", "count = 9", 1))
    harness.sync("hy3_主角")
    result = harness.entities.reconcile()
    assert [(issue.drama_rel, issue.error.field_path) for issue in result.config_issues] == [(HY3, "video.count")]
    assert _states(result)["hy3_砌炉的老人"] == "missing_on_platform"


def test_snapshot_records_skip_empty_and_duplicate_names(harness: Harness) -> None:
    records = harness.entity_mapper.snapshot_records(
        [
            EntitySnapshotEntryCdto("hy3_主角", "https://thumb/1", "2026-09-01"),
            EntitySnapshotEntryCdto(""),
            EntitySnapshotEntryCdto("hy3_主角", "https://thumb/2"),
        ],
        "2026-09-13T10:00:00.000000Z",
    )
    assert [(record.name, record.thumbnail_url) for record in records] == [("hy3_主角", "https://thumb/1")]
