from collections.abc import Sequence
from datetime import datetime

from libs.common.canonical_json import canonical_sha256
from libs.common.enums import BatchState, CheckSeverity, Confirmer, TokenVerdict
from libs.domain.errors.batch__error import (
    BalanceAlreadyRecordedError, BatchAlreadyConfirmedError, BatchExpiredError, BatchHasErrorsError,
    BatchInvariantError, BatchNotAwaitingConfirmError, ConfirmationNotIssuedError, EmptyBatchError,
    InvalidConfirmerError, TokenBindingError, TokenDigestMismatchError, TokenExpiredError, TokenInvalidError,
)
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.confirmation_token__valueobject import ConfirmationToken


class BatchEntity:
    def __init__(
        self,
        batch_id: str,
        items: Sequence[BatchItem],
        created_at: datetime,
        *,
        state: BatchState = BatchState.AWAITING_CONFIRM,
        token_expires_at: datetime | None = None,
        token_signature: str | None = None,
        confirmed_at: datetime | None = None,
        confirmer: Confirmer | None = None,
        consumed_token_signature: str | None = None,
        balance_start: int | None = None,
        balance_end: int | None = None,
    ) -> None:
        self._batch_id: str = batch_id
        self._items: tuple[BatchItem, ...] = tuple(items)
        self._created_at: datetime = created_at
        self._state: BatchState = state
        self._token_expires_at: datetime | None = token_expires_at
        self._token_signature: str | None = token_signature
        self._confirmed_at: datetime | None = confirmed_at
        self._confirmer: Confirmer | None = confirmer
        self._consumed_token_signature: str | None = consumed_token_signature
        self._balance_start: int | None = balance_start
        self._balance_end: int | None = balance_end
        if not self._items:
            raise EmptyBatchError("批次至少要有一条")
        if [item.index for item in self._items] != list(range(len(self._items))):
            raise EmptyBatchError("批次条目序号必须从 0 连续递增")
        if confirmer is not None and confirmer is not Confirmer.UI_HUMAN:
            raise InvalidConfirmerError("只有 UI 里的人可以确认批次")
        if (token_expires_at is None) != (token_signature is None):
            raise BatchInvariantError("token 过期时间与签名必须同时存在")
        confirmed: bool = state is BatchState.CONFIRMED
        confirmation_fields: tuple[object | None, ...] = (confirmed_at, confirmer, consumed_token_signature)
        if confirmed and any(value is None for value in confirmation_fields):
            raise BatchInvariantError("confirmed 批次必须带确认时间、确认人与已消费的 token")
        if not confirmed and any(value is not None for value in confirmation_fields):
            raise BatchInvariantError("未确认的批次不能带确认时间、确认人或已消费的 token")
        if confirmed and consumed_token_signature != token_signature:
            raise BatchInvariantError("已消费的 token 不是本批次签发的")

    @property
    def batch_id(self) -> str:
        return self._batch_id

    @property
    def items(self) -> tuple[BatchItem, ...]:
        return self._items

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def state(self) -> BatchState:
        return self._state

    @property
    def token_expires_at(self) -> datetime | None:
        return self._token_expires_at

    @property
    def token_signature(self) -> str | None:
        return self._token_signature

    @property
    def confirmed_at(self) -> datetime | None:
        return self._confirmed_at

    @property
    def confirmer(self) -> Confirmer | None:
        return self._confirmer

    @property
    def consumed_token_signature(self) -> str | None:
        return self._consumed_token_signature

    @property
    def balance_start(self) -> int | None:
        return self._balance_start

    @property
    def balance_end(self) -> int | None:
        return self._balance_end

    @property
    def content_digest(self) -> str:
        return canonical_sha256([item.canonical() for item in self._items])

    @property
    def estimated_credits(self) -> int:
        return sum(item.precheck.estimate.credits or 0 for item in self._items if item.spends_credits)

    @property
    def has_unestimated(self) -> bool:
        return any(not item.precheck.estimate.known for item in self._items if item.spends_credits)

    @property
    def has_errors(self) -> bool:
        return any(item.precheck.has_errors for item in self._items)

    def severity_counts(self) -> dict[CheckSeverity, int]:
        counts: dict[CheckSeverity, int] = {severity: 0 for severity in CheckSeverity}
        for item in self._items:
            counts[item.precheck.severity] += 1
        return counts

    def expire(self, at: datetime) -> bool:
        if (
            self._state is BatchState.AWAITING_CONFIRM
            and self._token_expires_at is not None
            and at >= self._token_expires_at
        ):
            self._state = BatchState.EXPIRED
            return True
        return False

    def issue_confirmation(self, token: ConfirmationToken, at: datetime) -> None:
        self.expire(at)
        self._require_awaiting()
        if (token.batch_id, token.content_digest, token.estimated_credits) != (
            self._batch_id,
            self.content_digest,
            self.estimated_credits,
        ):
            raise TokenBindingError("token 与批次 id / 内容摘要 / 合计积分不一致")
        if self._token_signature is not None and token.signature != self._token_signature:
            raise TokenBindingError("本批次已签发 token，过期时间与内容不能改变")
        self._token_expires_at = token.expires_at
        self._token_signature = token.signature

    def confirm(self, token_text: str, key: bytes, confirmer: Confirmer, at: datetime) -> BatchConfirmation:
        if self._state is BatchState.CONFIRMED:
            raise BatchAlreadyConfirmedError("该批次已确认，token 只能使用一次")
        if confirmer is not Confirmer.UI_HUMAN:
            raise InvalidConfirmerError("只有 UI 里的人可以确认批次")
        if self._token_signature is None:
            raise ConfirmationNotIssuedError("该批次还没有签发确认 token")
        verdict: TokenVerdict = ConfirmationToken.verify(
            token_text, self._batch_id, self.content_digest, self.estimated_credits, at, key
        )
        if verdict is TokenVerdict.BAD_SIGNATURE:
            raise TokenInvalidError("token 签名无效")
        if verdict is TokenVerdict.DIGEST_MISMATCH:
            raise TokenDigestMismatchError("token 与批次内容不一致")
        signature: str = token_text.rsplit(".", 1)[-1]
        if signature != self._token_signature:
            raise TokenInvalidError("token 不是本批次签发的那一枚")
        if self.expire(at) or verdict is TokenVerdict.EXPIRED or self._state is BatchState.EXPIRED:
            raise TokenExpiredError("确认 token 已过期，请重新预检")
        self._require_awaiting()
        if self.has_errors:
            raise BatchHasErrorsError("批次含 error 条目，剔除后重新预检才能确认")
        proof = BatchConfirmation(batch_id=self._batch_id, confirmed_at=at, confirmer=confirmer)
        self._state = BatchState.CONFIRMED
        self._confirmed_at = at
        self._confirmer = confirmer
        self._consumed_token_signature = signature
        return proof

    def reject(self) -> None:
        self._require_awaiting()
        self._state = BatchState.REJECTED

    def record_balance_start(self, balance: int) -> None:
        if self._balance_start is not None:
            raise BalanceAlreadyRecordedError("批次开始余额已记录")
        self._balance_start = balance

    def record_balance_end(self, balance: int) -> None:
        if self._balance_end is not None:
            raise BalanceAlreadyRecordedError("批次结束余额已记录")
        self._balance_end = balance

    def _require_awaiting(self) -> None:
        if self._state is BatchState.EXPIRED:
            raise BatchExpiredError("批次确认已过期，请重新预检")
        if self._state is not BatchState.AWAITING_CONFIRM:
            raise BatchNotAwaitingConfirmError(f"批次处于 {self._state}，不能确认")
