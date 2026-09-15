"""Entity (主体) access through the 即梦 entity page (FR-47, FR-49, FR-50).

`sync_snapshot` opens the page and reads the page's own subject response passively. `create` reuses an existing
subject with the same name and otherwise fills the 新建主体 form once, then re-syncs to verify. Nothing here
renames, deletes or edits an existing subject.
"""
from __future__ import annotations

import time
from collections.abc import Sequence
from pathlib import Path

from libs.application.backends.web_ui__backend import STEP_REASONS
from libs.common.enums import PauseReason
from libs.infrastructure.clients.jimeng_browser__client import JimengBrowserClient
from libs.infrastructure.clients.jimeng_page_entity__steps import open_entity_page, submit_entity_form
from libs.infrastructure.daos.jimeng_history__dao import ParseOutcome, SubjectListParseDao
from libs.infrastructure.errors.jimeng_browser__error import (
    BrowserCommandTimeoutError,
    BrowserLostError,
    BrowserNotStartedError,
    PageStepError,
    WebBackendError,
)
from libs.infrastructure.readers.jimeng_history__reader import SUBJECT_GET, JimengHistoryReader


class WebEntityGateway:
    def __init__(
        self,
        client: JimengBrowserClient,
        reader: JimengHistoryReader | None = None,
        name_max_chars: int = 20,
        sync_timeout_s: float = 15.0,
    ) -> None:
        self._client = client
        self._reader = reader or JimengHistoryReader()
        self._name_max_chars = name_max_chars
        self._sync_timeout_s = sync_timeout_s

    def sync_snapshot(self) -> list[dict[str, object]]:
        with self._client.exclusive():
            after = self._client.latest_seq()
            self._run_page(open_entity_page)
            parsed = self._await_subjects(after)
        return [
            {"subject_id": subject.subject_id, "name": subject.name, "description": subject.description,
             "updated_at": subject.updated_at}
            for subject in parsed.subjects
        ]

    def create(self, name: str, description: str, image_paths: Sequence[Path]) -> dict[str, object]:
        if not name or len(name) > self._name_max_chars:
            raise WebBackendError(PauseReason.STEP_FAILED, False, f"主体名须为 1–{self._name_max_chars} 个字符：{name!r}")
        missing = [str(path) for path in image_paths if not Path(path).is_file()]
        if not image_paths or missing:
            raise WebBackendError(PauseReason.STEP_FAILED, False, f"参考主体图片缺失：{missing or '未提供'}")
        with self._client.exclusive():
            existing = _find(self.sync_snapshot(), name)
            if existing is not None:
                return {"name": name, "subject_id": existing["subject_id"], "created": False, "reused": True, "verified": True}
            self._run_page(lambda session: submit_entity_form(session, name, description, tuple(image_paths)))
            created = _find(self.sync_snapshot(), name)
        return {
            "name": name,
            "subject_id": None if created is None else created["subject_id"],
            "created": True,
            "reused": False,
            "verified": created is not None,
        }

    def _run_page(self, command: object) -> None:
        try:
            self._client.run(command)  # type: ignore[arg-type]
        except PageStepError as error:
            raise WebBackendError(STEP_REASONS[error.kind], False, str(error)) from error
        except (BrowserLostError, BrowserNotStartedError) as error:
            raise WebBackendError(PauseReason.BROWSER_LOST, False, str(error)) from error
        except BrowserCommandTimeoutError as error:
            raise WebBackendError(PauseReason.PAGE_CONTRACT_BROKEN, True, str(error)) from error

    def _await_subjects(self, after: int) -> SubjectListParseDao:
        deadline = time.monotonic() + self._sync_timeout_s
        while time.monotonic() < deadline:
            observed = self._client.observations(SUBJECT_GET, after)
            if observed:
                parsed = self._reader.subjects_body(observed[-1].body)
                if parsed.outcome is ParseOutcome.OK:
                    return parsed
                if parsed.outcome is ParseOutcome.LOGIN_ERROR:
                    raise WebBackendError(PauseReason.LOGIN_EXPIRED, False, "主体接口返回未登录")
                raise WebBackendError(PauseReason.PAGE_CONTRACT_BROKEN, False, f"主体响应无法解析（{parsed.outcome.value}）")
            time.sleep(0.1)
        raise WebBackendError(PauseReason.PAGE_CONTRACT_BROKEN, True, "打开主体页后没有观察到主体列表响应")


def _find(snapshot: list[dict[str, object]], name: str) -> dict[str, object] | None:
    return next((item for item in snapshot if item["name"] == name), None)
