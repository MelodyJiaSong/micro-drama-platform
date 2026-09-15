from __future__ import annotations

import json
from dataclasses import asdict, fields, is_dataclass
from datetime import timedelta

import pytest

from libs.application.dtos.batch__dto import AssetItemInput, BatchParamsQdto, BatchQdto, ShotItemInput
from libs.application.errors.batch__error import BatchNotFoundError
from libs.common.clock import iso
from libs.common.enums import BatchState
from libs.domain.errors.batch__error import BatchExpiredError
from tests.libs.application.batch.support import BG11, C1_CARD, SHOT02, T0, BatchEnv


def _field_names(cls: type) -> set[str]:
    names: set[str] = set()
    for field in fields(cls):
        names.add(field.name)
    return names


def test_get_pages_items_with_resolved_references_and_no_token(env: BatchEnv) -> None:
    cdto = env.command.precheck([ShotItemInput(SHOT02), AssetItemInput(C1_CARD, "c1-1")], None)
    token = env.query.confirmation(cdto.batch_id).token

    second_page = env.query.get(cdto.batch_id, 2, 1)
    assert (second_page.total_items, second_page.page, second_page.page_size, len(second_page.items)) == (2, 2, 1, 1)
    assert second_page.items[0].index == 1 and second_page.items[0].source_type == "asset_image"

    first_page = env.query.get(cdto.batch_id, 1, 10_000)
    assert first_page.page_size == 200 and len(first_page.items) == 2
    shot = first_page.items[0]
    references = {(ref.name, ref.kind, ref.path, ref.entity) for ref in shot.references}
    assert ("砌炉的老人", "entity", None, "hy3_主角") in references and ("bg11-1", "image", BG11, None) in references
    assert shot.params == BatchParamsQdto("seedance2.5", "16:9", "720p", 1, 22, None)
    assert (shot.estimated_credits, shot.severity, shot.backend) == (440, "warning", "web")
    assert any(check.code == "negative_prompt_omitted" and check.config_key == "video.negative_prompt" for check in shot.checks)
    assert first_page.estimated_credits == 441 and first_page.expires_at == iso(T0 + timedelta(minutes=30))

    assert "token" not in _field_names(BatchQdto)
    for item in first_page.items:
        assert is_dataclass(item) and "token" not in _field_names(type(item))
    dumped = json.dumps(asdict(first_page), ensure_ascii=False)
    assert token not in dumped and token.rpartition(".")[2] not in dumped


def test_confirmation_expiry_is_fixed_at_first_issue(env: BatchEnv) -> None:
    batch_id = env.command.precheck([ShotItemInput(SHOT02)], None).batch_id

    first = env.query.confirmation(batch_id)
    env.clock.advance(timedelta(minutes=10))
    second = env.query.confirmation(batch_id)

    assert second.token == first.token
    assert first.expires_at == second.expires_at == iso(T0 + timedelta(minutes=30))
    assert (first.seconds_left, second.seconds_left, first.estimated_credits) == (1800, 1200, 440)
    assert first.token not in repr(first)

    env.clock.advance(timedelta(minutes=21))
    with pytest.raises(BatchExpiredError):
        env.query.confirmation(batch_id)
    batch = env.batches.get(batch_id)
    assert batch is not None and batch.state is BatchState.EXPIRED


def test_today_confirmed_credits_counts_confirmed_batches(env: BatchEnv) -> None:
    batch_id = env.command.precheck([ShotItemInput(SHOT02)], None).batch_id
    confirmation = env.query.confirmation(batch_id)
    assert confirmation.today_confirmed_credits == 0
    env.command.confirm(batch_id, confirmation.token, "ui_human")

    next_batch = env.command.precheck([ShotItemInput(SHOT02, reroll=True)], None).batch_id

    assert env.query.confirmation(next_batch).today_confirmed_credits == 440


def test_unknown_batch_is_a_typed_not_found(env: BatchEnv) -> None:
    with pytest.raises(BatchNotFoundError):
        env.query.get("batch_missing", 1, 50)
    with pytest.raises(BatchNotFoundError):
        env.query.confirmation("batch_missing")
