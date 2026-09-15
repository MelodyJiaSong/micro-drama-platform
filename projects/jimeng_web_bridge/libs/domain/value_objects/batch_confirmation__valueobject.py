from dataclasses import dataclass
from datetime import datetime

from libs.common.enums import Confirmer
from libs.domain.errors.batch__error import InvalidConfirmerError


@dataclass(frozen=True)
class BatchConfirmation:
    batch_id: str
    confirmed_at: datetime
    confirmer: Confirmer

    def __post_init__(self) -> None:
        if self.confirmer is not Confirmer.UI_HUMAN:
            raise InvalidConfirmerError("只有 UI 里的人可以确认批次")
