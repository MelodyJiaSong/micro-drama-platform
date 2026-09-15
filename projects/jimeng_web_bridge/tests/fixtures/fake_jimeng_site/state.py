"""In-memory state of the offline fake 即梦 site: account, records, faults, gates and the ledger.

Nothing here talks to the network. The page server and the control server both mutate one
`FakeSiteState` under its lock, so tests can drive it in-process or over the control port.
"""
from __future__ import annotations

import secrets
import threading
import time
from dataclasses import dataclass, field

WEB_VERSION: str = "7.5.0-fake"
SCHEMA_VERSION: str = "fake-pre-probe"
PRICE_NOW_PER_S: dict[str, int] = {
    "即梦 Seedance 2.5": 20,
    "Seedance 2.0 VIP": 14,
    "Seedance 2.0 Fast VIP": 10,
    "Seedance 2.0": 8,
    "Seedance 2.0 Fast": 6,
    "Seedance 2.0 mini": 4,
}
PRICE_ORIGIN_PER_S: int = 26
DEFAULT_ENTITIES: tuple[str, ...] = ("hy3_主角", "hy1_主角", "f80_f80", "xj_酒剑仙", "xj_阿奴")

FAULTS: frozenset[str] = frozenset(
    {
        "captcha_popup",
        "risk_popup",
        "login_expired",
        "insufficient_credit",
        "parallel_limit_notice",
        "backpressure",
        "moderation_reject",
        "real_face_rejected",
        "upload_reject",
        "editor_append_on_refill",
        "editor_drop_mention",
        "mention_candidate_missing",
        "control_readback_mismatch",
        "layout_next",
        "status_malformed",
        "status_delayed",
        "submit_response_hidden",
        "page_reload_mid_generation",
        "download_truncated",
        "entity_save_fail",
    }
)
GATES: frozenset[str] = frozenset({"completion", "submit_response", "upload_done", "send_enabled"})


@dataclass
class FaultSpec:
    name: str
    remaining: int
    params: dict[str, object]


@dataclass
class FakeRecord:
    record_id: str
    prompt_text: str
    mentions: list[str]
    materials: list[str]
    params: dict[str, object]
    created_time: float
    status: str = "queued"
    progress: int = 0
    fail_msg: str = ""
    credits: int = 0
    external: bool = False

    @property
    def final(self) -> bool:
        return self.status in ("succeeded", "failed")


@dataclass
class Ledger:
    param_sets: list[dict[str, object]] = field(default_factory=list)
    uploads: list[dict[str, object]] = field(default_factory=list)
    generate_clicks: list[dict[str, object]] = field(default_factory=list)
    submits: list[dict[str, object]] = field(default_factory=list)
    entity_saves: list[dict[str, object]] = field(default_factory=list)
    blocked_actions: list[dict[str, object]] = field(default_factory=list)
    login_inputs: int = 0
    page_loads: int = 0
    downloads: int = 0
    status_requests: int = 0

    def counts(self) -> dict[str, int]:
        return {
            "generate_clicks": len(self.generate_clicks),
            "uploads": len(self.uploads),
            "submits": len(self.submits),
            "accepted_submits": sum(1 for item in self.submits if item.get("accepted")),
            "param_sets": len(self.param_sets),
            "entity_saves": len(self.entity_saves),
            "blocked_actions": len(self.blocked_actions),
            "login_inputs": self.login_inputs,
            "page_loads": self.page_loads,
            "downloads": self.downloads,
            "status_requests": self.status_requests,
        }


@dataclass
class PageConfig:
    poll_ms: int = 300
    progress_step: int = 50
    upload_delay_ms: int = 120
    last_creation_type: str = "视频生成"
    draft: str = ""
    negative_box: bool = False
    running_limit: int = 3


class FakeSiteState:
    def __init__(self, video_bytes: bytes) -> None:
        self.lock = threading.RLock()
        self.nonce: str = secrets.token_hex(8)
        self.video_bytes = video_bytes
        self._counter: int = 0
        self.reset()

    def reset(self) -> None:
        with self.lock:
            self.logged_in: bool = True
            self.credits: int = 11000
            self.entities: list[dict[str, object]] = [
                {"subject_id": f"subj_{index}", "name": name, "description": "", "update_time": 1789290000 + index}
                for index, name in enumerate(DEFAULT_ENTITIES)
            ]
            self.records: dict[str, FakeRecord] = {}
            self.faults: dict[str, FaultSpec] = {}
            self.held: set[str] = set()
            self.ledger = Ledger()
            self.config = PageConfig()
            self.pending_reload: bool = False
            self.pending_captcha: bool = False

    def inject(self, name: str, times: int = 1, **params: object) -> None:
        if name not in FAULTS:
            raise ValueError(f"unknown fault: {name}")
        with self.lock:
            self.faults[name] = FaultSpec(name, times, dict(params))
            if name == "login_expired":
                self.logged_in = False
            if name == "insufficient_credit":
                self.credits = 0
            if name == "captcha_popup" and params.get("now"):
                self.pending_captcha = True
            if name == "page_reload_mid_generation":
                self.pending_reload = True

    def clear_fault(self, name: str) -> None:
        with self.lock:
            self.faults.pop(name, None)
            if name == "login_expired":
                self.logged_in = True
            if name == "captcha_popup":
                self.pending_captcha = False
            if name == "insufficient_credit":
                self.credits = 11000

    def fault(self, name: str) -> FaultSpec | None:
        with self.lock:
            spec = self.faults.get(name)
            return spec if spec is not None and spec.remaining > 0 else None

    def take_fault(self, name: str) -> FaultSpec | None:
        with self.lock:
            spec = self.fault(name)
            if spec is None:
                return None
            spec.remaining -= 1
            return spec

    def hold(self, gate: str) -> None:
        if gate not in GATES:
            raise ValueError(f"unknown gate: {gate}")
        with self.lock:
            self.held.add(gate)

    def release(self, gate: str) -> None:
        with self.lock:
            self.held.discard(gate)

    def is_held(self, gate: str) -> bool:
        with self.lock:
            return gate in self.held

    def seed(
        self,
        logged_in: bool | None = None,
        credits: int | None = None,
        entities: list[str] | None = None,
        external_running: int | None = None,
        draft: str | None = None,
        last_creation_type: str | None = None,
        running_limit: int | None = None,
        poll_ms: int | None = None,
        progress_step: int | None = None,
        negative_box: bool | None = None,
    ) -> None:
        with self.lock:
            if logged_in is not None:
                self.logged_in = logged_in
            if credits is not None:
                self.credits = credits
            if entities is not None:
                self.entities = [
                    {"subject_id": f"subj_seed_{index}", "name": name, "description": "", "update_time": 1789290000}
                    for index, name in enumerate(entities)
                ]
            if external_running is not None:
                for index in range(external_running):
                    record = self.new_record(f"用户手工任务 {index + 1}", [], [], {}, external=True)
                    record.status = "generating"
                    record.progress = 10
            if draft is not None:
                self.config.draft = draft
            if last_creation_type is not None:
                self.config.last_creation_type = last_creation_type
            if running_limit is not None:
                self.config.running_limit = running_limit
            if poll_ms is not None:
                self.config.poll_ms = poll_ms
            if progress_step is not None:
                self.config.progress_step = progress_step
            if negative_box is not None:
                self.config.negative_box = negative_box

    def new_record(
        self,
        prompt_text: str,
        mentions: list[str],
        materials: list[str],
        params: dict[str, object],
        external: bool = False,
    ) -> FakeRecord:
        with self.lock:
            self._counter += 1
            record_id = f"{7000000000000000 + self._counter}"
            record = FakeRecord(
                record_id=record_id,
                prompt_text=prompt_text,
                mentions=list(mentions),
                materials=list(materials),
                params=dict(params),
                created_time=time.time(),
                external=external,
            )
            self.records[record_id] = record
            return record

    def running_count(self) -> int:
        with self.lock:
            return sum(1 for record in self.records.values() if not record.final)

    def finish_external(self, count: int = 1) -> None:
        with self.lock:
            for record in [r for r in self.records.values() if r.external and not r.final][:count]:
                record.status = "succeeded"
                record.progress = 100

    def advance(self, record: FakeRecord) -> None:
        with self.lock:
            if record.final or record.external:
                return
            record.status = "generating"
            if "completion" in self.held:
                record.progress = min(90, record.progress + self.config.progress_step)
                return
            record.progress = min(100, record.progress + self.config.progress_step)
            if record.progress < 100:
                return
            moderation = self.faults.get("moderation_reject")
            real_face = self.faults.get("real_face_rejected")
            if moderation is not None and moderation.remaining > 0:
                moderation.remaining -= 1
                record.status, record.fail_msg = "failed", "内容审核未通过，请修改后重试"
            elif real_face is not None and real_face.remaining > 0 and real_face.params.get("stage") == "generate":
                real_face.remaining -= 1
                record.status, record.fail_msg = "failed", "暂不支持真人人脸"
            else:
                record.status = "succeeded"
