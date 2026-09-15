from __future__ import annotations

from collections.abc import Sequence

import pytest

batch_dto = pytest.importorskip(
    "libs.application.dtos.batch__dto", reason="impl-03 contract module libs/application/dtos/batch__dto.py not landed"
)

from libs.application.commands.entity__command import EntityCommand  # noqa: E402
from libs.application.dtos.entity__dto import EntitySnapshotEntryCdto  # noqa: E402
from libs.infrastructure.errors.config_io__error import DramaRootNotFoundError  # noqa: E402
from libs.infrastructure.errors.sandbox__error import SandboxError  # noqa: E402
from tests.libs.application.config_entities.support import HY3, T0, Harness  # noqa: E402

SENTINEL_RESULT: object = object()


class FakeBatches:
    def __init__(self) -> None:
        self.calls: list[tuple[list[object], str | None]] = []

    def precheck(self, items: Sequence[object], idempotency_key: str | None) -> object:
        self.calls.append((list(items), idempotency_key))
        return SENTINEL_RESULT


def _command(harness: Harness, batches: FakeBatches) -> EntityCommand:
    return EntityCommand(harness.configs, batches, harness.snapshot_writer, harness.clock, harness.entity_mapper)  # type: ignore[arg-type]


def test_request_create_delegates_one_entity_create_item_to_batch_precheck(ro_harness: Harness) -> None:
    batches = FakeBatches()
    result = _command(ro_harness, batches).request_create("huangye_shenghuo/hy3", "c2_獾", "成年欧洲獾")
    assert result is SENTINEL_RESULT
    assert len(batches.calls) == 1
    items, key = batches.calls[0]
    assert key is None and len(items) == 1
    item = items[0]
    assert isinstance(item, batch_dto.EntityCreateItemInput)
    assert (item.drama_rel, item.character_dir, item.description) == (HY3, "c2_獾", "成年欧洲獾")


def test_request_create_without_description_passes_none(ro_harness: Harness) -> None:
    batches = FakeBatches()
    _command(ro_harness, batches).request_create(HY3, "c1_砌炉的老人")
    assert batches.calls[0][0][0].description is None


@pytest.mark.parametrize(
    ("drama", "card", "error"),
    [
        ("huangye_shenghuo/../..", "c2_獾", SandboxError),
        ("huangye_shenghuo\\hy3", "c2_獾", SandboxError),
        (HY3, "../c2_獾", SandboxError),
        (HY3, "a\\b", SandboxError),
        (HY3, "..", SandboxError),
        (HY3, "c2_獾:stream", SandboxError),
        ("huangye_shenghuo", "c2_獾", DramaRootNotFoundError),
    ],
)
def test_request_create_rejects_unsafe_inputs_without_calling_precheck(
    ro_harness: Harness, drama: str, card: str, error: type[Exception]
) -> None:
    batches = FakeBatches()
    with pytest.raises(error):
        _command(ro_harness, batches).request_create(drama, card)
    assert batches.calls == []


def test_record_snapshot_replaces_the_snapshot_and_feeds_reconcile(ro_harness: Harness) -> None:
    command = _command(ro_harness, FakeBatches())
    ro_harness.sync("旧主体")
    command.record_snapshot(
        [EntitySnapshotEntryCdto("hy3_獾", "https://thumb/badger", "2026-09-10"), EntitySnapshotEntryCdto("hy3_獾")]
    )
    records = ro_harness.snapshot_reader.all()
    assert [(r.name, r.thumbnail_url, r.modified_at) for r in records] == [("hy3_獾", "https://thumb/badger", "2026-09-10")]
    assert ro_harness.snapshot_reader.last_synced_at() == "2026-09-13T10:00:00.000000Z" == records[0].synced_at
    assert T0.year == 2026
    row = next(row for row in ro_harness.entities.reconcile(HY3).rows if row.name == "hy3_獾")
    assert (row.state, row.thumbnail_url) == ("mapped", "https://thumb/badger")
