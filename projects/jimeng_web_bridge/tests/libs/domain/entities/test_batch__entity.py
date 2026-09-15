from datetime import timedelta

import pytest

from libs.common.enums import BatchState, CheckSeverity, Confirmer
from libs.domain.entities.batch__entity import BatchEntity
from libs.domain.errors.batch__error import (
    BalanceAlreadyRecordedError, BatchAlreadyConfirmedError, BatchExpiredError, BatchHasErrorsError,
    BatchInvariantError, BatchNotAwaitingConfirmError, ConfirmationNotIssuedError, EmptyBatchError,
    InvalidConfirmerError, TokenBindingError, TokenDigestMismatchError, TokenExpiredError, TokenInvalidError,
)
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.confirmation_token__valueobject import ConfirmationToken
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.precheck__valueobject import run_precheck
from tests.libs.domain.builders import KEY, SHA_B, T0, context, image_ref, video_request

TTL = timedelta(minutes=30)


def item(index: int, request: GenerationRequest, **ctx: object) -> BatchItem:
    return BatchItem.of(index, request, run_precheck(request, context(**ctx)))


def batch(*requests: GenerationRequest) -> BatchEntity:
    reqs = requests or (video_request(),)
    return BatchEntity("batch-1", tuple(item(i, r) for i, r in enumerate(reqs)), T0)


def issue(b: BatchEntity, expires_in: timedelta = TTL) -> ConfirmationToken:
    token = ConfirmationToken.issue(b.batch_id, b.content_digest, b.estimated_credits, T0 + expires_in, KEY)
    b.issue_confirmation(token, T0)
    return token


def confirm_at(b: BatchEntity, token_text: str, minutes: float, key: bytes = KEY) -> BatchConfirmation:
    return b.confirm(token_text, key, Confirmer.UI_HUMAN, T0 + timedelta(minutes=minutes))


def test_new_batch_awaits_confirmation_with_totals() -> None:
    b = batch()
    assert b.state is BatchState.AWAITING_CONFIRM
    assert b.estimated_credits == 440
    assert b.severity_counts()[CheckSeverity.OK] == 1
    assert b.content_digest == batch().content_digest


@pytest.mark.parametrize(
    "variant",
    [
        video_request(prompt="shot02\n参考: `bg11-1(场景参考图)=>@` "),
        video_request(refs=(image_ref(sha=SHA_B),)),
        video_request(ratio="9:16"),
    ],
    ids=["prompt_byte", "reference_sha", "params_field"],
)
def test_digest_changes_with_any_content(variant: GenerationRequest) -> None:
    assert batch(variant).content_digest != batch(video_request()).content_digest


def test_digest_changes_with_item_order() -> None:
    a, c = video_request(), video_request(duration=10)
    assert batch(a, c).content_digest != batch(c, a).content_digest


def test_empty_batch_rejected() -> None:
    with pytest.raises(EmptyBatchError):
        BatchEntity("b", (), T0)


def test_confirm_happy_path_and_replay() -> None:
    b = batch()
    token = issue(b)
    proof = confirm_at(b, token.encode(), 29.99)
    assert b.state is BatchState.CONFIRMED and b.confirmer is Confirmer.UI_HUMAN
    assert b.consumed_token_signature == token.signature
    assert (proof.batch_id, proof.confirmer) == ("batch-1", Confirmer.UI_HUMAN)
    with pytest.raises(BatchAlreadyConfirmedError):
        confirm_at(b, token.encode(), 1)


@pytest.mark.parametrize("bogus", ["not-a-token", "", "abc.def", "OK"])
def test_entity_verifies_token_itself(bogus: str) -> None:
    b = batch()
    issue(b)
    with pytest.raises(TokenInvalidError):
        confirm_at(b, bogus, 1)
    assert b.state is BatchState.AWAITING_CONFIRM and b.consumed_token_signature is None


def test_token_signed_with_other_key_rejected() -> None:
    b = batch()
    issue(b)
    forged = ConfirmationToken.issue(b.batch_id, b.content_digest, b.estimated_credits, T0 + TTL, b"x" * 32)
    with pytest.raises(TokenInvalidError):
        confirm_at(b, forged.encode(), 1)


def test_valid_token_with_other_expiry_is_not_the_issued_one() -> None:
    b = batch()
    issue(b)
    longer = ConfirmationToken.issue(b.batch_id, b.content_digest, b.estimated_credits, T0 + 10 * TTL, KEY)
    with pytest.raises(TokenInvalidError):
        confirm_at(b, longer.encode(), 40)
    assert b.state is BatchState.AWAITING_CONFIRM


def test_expired_token_rejected_and_batch_expires() -> None:
    b = batch()
    token = issue(b)
    with pytest.raises(TokenExpiredError):
        confirm_at(b, token.encode(), 30.01)
    assert b.state is BatchState.EXPIRED
    with pytest.raises(BatchExpiredError):
        b.issue_confirmation(token, T0 + timedelta(minutes=31))


def test_tampered_token_rejected() -> None:
    b = batch()
    text = issue(b).encode()
    with pytest.raises(TokenInvalidError):
        confirm_at(b, text[:-1] + ("0" if text[-1] != "0" else "1"), 1)
    assert b.state is BatchState.AWAITING_CONFIRM


def test_token_of_other_batch_rejected() -> None:
    b = batch()
    issue(b)
    other = ConfirmationToken.issue("batch-2", b.content_digest, b.estimated_credits, T0 + TTL, KEY)
    with pytest.raises(TokenDigestMismatchError):
        confirm_at(b, other.encode(), 1)


def test_confirm_without_issued_token() -> None:
    b = batch()
    token = ConfirmationToken.issue(b.batch_id, b.content_digest, b.estimated_credits, T0 + TTL, KEY)
    with pytest.raises(ConfirmationNotIssuedError):
        confirm_at(b, token.encode(), 1)


@pytest.mark.parametrize("confirmer", ["mcp", "http_auto", "ui_human"])
def test_confirmer_must_be_ui_human_enum(confirmer: str) -> None:
    b = batch()
    token = issue(b)
    with pytest.raises(InvalidConfirmerError):
        b.confirm(token.encode(), KEY, confirmer, T0)  # type: ignore[arg-type]
    with pytest.raises(InvalidConfirmerError):
        BatchConfirmation(batch_id="batch-1", confirmed_at=T0, confirmer=confirmer)  # type: ignore[arg-type]


def test_batch_with_error_item_cannot_confirm() -> None:
    b = BatchEntity("batch-1", (item(0, video_request()), item(1, video_request(duration=31))), T0)
    token = issue(b)
    with pytest.raises(BatchHasErrorsError):
        confirm_at(b, token.encode(), 1)
    assert b.state is BatchState.AWAITING_CONFIRM


def test_issue_binding_checked() -> None:
    b = batch()
    with pytest.raises(TokenBindingError):
        b.issue_confirmation(ConfirmationToken.issue("batch-1", "x" * 64, b.estimated_credits, T0 + TTL, KEY), T0)
    with pytest.raises(TokenBindingError):
        b.issue_confirmation(ConfirmationToken.issue("batch-1", b.content_digest, b.estimated_credits + 1, T0 + TTL, KEY), T0)
    issue(b)
    with pytest.raises(TokenBindingError):
        issue(b, expires_in=2 * TTL)


def test_reissue_same_expiry_is_identical_token() -> None:
    b = batch()
    first = issue(b)
    assert issue(b) == first and b.token_signature == first.signature


def test_dedup_items_do_not_count_and_unknown_price_flagged() -> None:
    dup = item(0, video_request(), fingerprint_hit_job_id="job-0")
    unknown = item(1, video_request(model="seedance2.0fast", duration=10))
    b = BatchEntity("b", (dup, unknown), T0)
    assert b.estimated_credits == 0 and b.has_unestimated


def test_reject_and_balance() -> None:
    b = batch()
    b.record_balance_start(1000)
    with pytest.raises(BalanceAlreadyRecordedError):
        b.record_balance_start(900)
    b.record_balance_end(560)
    b.reject()
    assert b.state is BatchState.REJECTED
    with pytest.raises(BatchNotAwaitingConfirmError):
        b.reject()


def test_state_is_read_only() -> None:
    b = batch()
    with pytest.raises(AttributeError):
        b.state = BatchState.CONFIRMED  # type: ignore[misc]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"state": BatchState.CONFIRMED},
        {"state": BatchState.CONFIRMED, "confirmed_at": T0, "confirmer": Confirmer.UI_HUMAN, "consumed_token_signature": "s"},
        {"token_signature": "s"},
        {"confirmed_at": T0},
    ],
)
def test_rehydrate_invariants(kwargs: dict[str, object]) -> None:
    items = batch().items
    with pytest.raises(BatchInvariantError):
        BatchEntity("batch-1", items, T0, **kwargs)  # type: ignore[arg-type]


def test_rehydrate_confirmed_batch() -> None:
    b = batch()
    token = issue(b)
    confirm_at(b, token.encode(), 1)
    loaded = BatchEntity(
        b.batch_id, b.items, b.created_at, state=b.state, token_expires_at=b.token_expires_at,
        token_signature=b.token_signature, confirmed_at=b.confirmed_at, confirmer=b.confirmer,
        consumed_token_signature=b.consumed_token_signature,
    )
    assert loaded.state is BatchState.CONFIRMED
