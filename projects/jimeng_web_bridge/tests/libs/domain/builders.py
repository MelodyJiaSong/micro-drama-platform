import copy
import tomllib
from datetime import datetime, timedelta, timezone
from pathlib import Path

from libs.common.enums import (
    BackendKind, Confirmer, GenerationKind, JobState, NegativePromptStrategy, PauseReason, RefKind, SourceType,
)
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.precheck_result__valueobject import PrecheckResult
from libs.domain.value_objects.price_estimate__valueobject import PriceEstimate
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.domain.value_objects.pause_reason__valueobject import PauseReasonPolicy
from libs.domain.value_objects.precheck_context__valueobject import EntitySnapshotFacts, PrecheckContext
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem

T0 = datetime(2026, 9, 13, 10, 0, 0, tzinfo=timezone.utc)
KEY = b"0123456789abcdef0123456789abcdef"
SHA_A = "a" * 64
SHA_B = "b" * 64
SHOT_SLOT = "ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02"
STATIC_CREDITS = 440
PAGE_OVER_ESTIMATE = 600
TOLERANCE_PCT = 20
GLOBAL_TOML: Path = Path(__file__).resolve().parents[3] / "config" / "global.toml"
GLOBAL_DATA: dict[str, object] = tomllib.loads(GLOBAL_TOML.read_text(encoding="utf-8"))


def global_data() -> dict[str, object]:
    return copy.deepcopy(GLOBAL_DATA)


def global_config() -> GlobalConfig:
    return GlobalConfig.from_dict(global_data())


def image_ref(name: str = "bg11-1", sha: str | None = SHA_A, label: str = "场景参考图", kind: RefKind = RefKind.IMAGE) -> ReferenceItem:
    path: str | None = None if sha is None else f"ai_videos/x/{name}.png"
    return ReferenceItem(name=name, label=label, kind=kind, resolved_path=path, sha256=sha)


def entity_ref(name: str = "砌炉的老人", entity: str = "hy3_主角") -> ReferenceItem:
    return ReferenceItem(name=name, label="Seedance 人物 entity", kind=RefKind.ENTITY, entity_name=entity)


def video_request(
    prompt: str = "shot02\n参考: `bg11-1(场景参考图)=>@`",
    refs: tuple[ReferenceItem, ...] = (image_ref(),),
    model: str = "seedance2.5",
    ratio: str = "16:9",
    duration: int | None = 22,
    resolution: str = "720p",
    count: int = 1,
    negative: str | None = None,
    source_type: SourceType = SourceType.SHOT,
    output_slot: str = SHOT_SLOT,
) -> GenerationRequest:
    return GenerationRequest(
        kind=GenerationKind.VIDEO,
        prompt=prompt,
        negative_prompt=negative,
        references=refs,
        params=GenerationParams(model=model, ratio=ratio, resolution=resolution, count=count, duration_s=duration),
        output_slot=output_slot,
        source=RequestSource(type=source_type, path=f"{output_slot}/shot02.md"),
    )


def image_request(refs: tuple[ReferenceItem, ...] = (), model: str = "seedream5.0", resolution: str = "2k", count: int = 1, ratio: str = "3:4") -> GenerationRequest:
    card = "ai_videos/huangye_shenghuo/hy3/2_世界观人设/characters/c1_砌炉的老人"
    return GenerationRequest(
        kind=GenerationKind.IMAGE,
        prompt="c1-1_砌炉的老人立绘",
        negative_prompt=None,
        references=refs,
        params=GenerationParams(model=model, ratio=ratio, resolution=resolution, count=count),
        output_slot=f"{card}#c1-1",
        source=RequestSource(type=SourceType.ASSET_IMAGE, path=f"{card}/c1_砌炉的老人.md", block_key="c1-1"),
    )


def entity_create_request(name: str = "hy3_獾", refs: tuple[ReferenceItem, ...] = (image_ref("c2-1"),), prompt: str = "锁定描述符") -> GenerationRequest:
    card = "ai_videos/huangye_shenghuo/hy3/2_世界观人设/characters/c2_獾"
    return GenerationRequest(
        kind=GenerationKind.ENTITY,
        prompt=prompt,
        negative_prompt=None,
        references=refs,
        params=None,
        output_slot=card,
        source=RequestSource(type=SourceType.ENTITY_CREATE, path=card),
        entity_name=name,
    )


def context(**overrides: object) -> PrecheckContext:
    cfg = global_config()
    values: dict[str, object] = {
        "backend": BackendKind.WEB,
        "limits": cfg.model_limits,
        "price_table": cfg.price_table,
        "prompt_max_chars": 5000,
        "entity_name_max_chars": 20,
        "negative_prompt_strategy": NegativePromptStrategy.PLATFORM_FIELD_OR_OMIT,
        "snapshot": EntitySnapshotFacts(names=frozenset({"hy3_主角", "hy1_造家的人"}), synced_at=T0 - timedelta(hours=1)),
        "snapshot_stale_after": timedelta(hours=24),
        "now": T0,
        "output_dir_writable": True,
    }
    values.update(overrides)
    return PrecheckContext(**values)  # type: ignore[arg-type]


def proof(batch_id: str = "batch-1") -> BatchConfirmation:
    return BatchConfirmation(batch_id=batch_id, confirmed_at=T0, confirmer=Confirmer.UI_HUMAN)


def confirmed_item(request: GenerationRequest, credits: int | None = STATIC_CREDITS, index: int = 0) -> BatchItem:
    return BatchItem.of(index, request, PrecheckResult(items=(), estimate=PriceEstimate(credits=credits)))


def new_job(
    request: GenerationRequest | None = None,
    confirmed: bool = True,
    backend: BackendKind = BackendKind.WEB,
    credits: int | None = STATIC_CREDITS,
) -> GenerationJobEntity:
    req: GenerationRequest = request or video_request()
    job = GenerationJobEntity("job-1", "batch-1", backend, req, Fingerprint.of(req))
    if confirmed:
        item = confirmed_item(req, credits)
        job.confirm(proof(), FrozenRequest.from_item(item, backend, "cfg-digest", TOLERANCE_PCT), item)
    return job


def prepared_to_last_step(job: GenerationJobEntity, page_credits: int | None = STATIC_CREDITS) -> GenerationJobEntity:
    job.start_preparing(T0)
    for step in job.preparing_steps[1:]:
        job.advance_step(step)
    if job.backend is BackendKind.WEB and job.request.kind is not GenerationKind.ENTITY and page_credits is not None:
        job.record_page_estimate(page_credits, False, T0)
    return job


_ORDER: list[JobState] = [JobState.PREPARING, JobState.SUBMITTING, JobState.GENERATING, JobState.DOWNLOADING]


def job_in(
    state: JobState,
    reason: PauseReason | None = None,
    origin: JobState | None = None,
    backend: BackendKind = BackendKind.WEB,
) -> GenerationJobEntity:
    job = new_job(backend=backend)
    if state is JobState.QUEUED:
        return job
    if state is JobState.CANCELLED:
        job.cancel(T0)
        return job
    if state is JobState.PAUSED_NEEDS_HUMAN:
        pause_reason: PauseReason = reason or PauseReason.FILL_MISMATCH
        source: JobState = origin or sorted(PauseReasonPolicy.rule(pause_reason).from_states, key=_ORDER.index)[0]
        job = job_in(source, backend=backend)
        if pause_reason is PauseReason.ESTIMATE_EXCEEDS_CONFIRMED:
            job.record_page_estimate(PAGE_OVER_ESTIMATE, False, T0)
        else:
            job.pause(pause_reason, T0)
        return job
    if state is JobState.FAILED:
        job = job_in(JobState.GENERATING, backend=backend)
        job.fail(PauseReason.MODERATION_REJECT, T0)
        return job
    if state is JobState.PREPARING:
        job.start_preparing(T0)
        return job
    prepared_to_last_step(job).mark_submitting(T0)
    if state is JobState.SUBMITTING:
        return job
    job.mark_generating("task-1", T0)
    if state is JobState.GENERATING:
        return job
    job.mark_downloading(T0)
    if state is JobState.DOWNLOADING:
        return job
    job.mark_done(T0)
    return job


def rehydrate(job: GenerationJobEntity) -> GenerationJobEntity:
    return GenerationJobEntity(
        job.job_id, job.batch_id, job.backend, job.request, job.fingerprint,
        attempt=job.attempt, state=job.state, blocked_on=job.blocked_on, current_step=job.current_step,
        pause_reason=job.pause_reason, paused_from=job.paused_from, failure_reason=job.failure_reason,
        confirmation=job.confirmation, frozen_request=job.frozen_request, platform_task_id=job.platform_task_id,
        cancel_requested=job.cancel_requested, credits_spent=job.credits_spent,
        page_estimated_credits=job.page_estimated_credits, approved_credits=job.approved_credits,
        transitions=job.transitions,
    )
