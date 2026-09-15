from collections.abc import Mapping
from types import MappingProxyType

from libs.common.enums import CheckSeverity, GenerationKind, NegativePromptStrategy, PrecheckCheck, RefKind, SourceType
from libs.domain.value_objects.config_table__valueobject import key_path
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.model_limits__valueobject import ModelCapability
from libs.domain.value_objects.precheck_context__valueobject import PrecheckContext
from libs.domain.value_objects.precheck_result__valueobject import PrecheckItem

_KEYS: Mapping[SourceType, Mapping[str, str]] = MappingProxyType({
    SourceType.SHOT: MappingProxyType({"model": "video.model", "resolution": "video.resolution", "ratio": "video.model", "duration": "video.model"}),
    SourceType.ASSET_VIDEO: MappingProxyType({
        "model": "assets.video_default.model",
        "resolution": "assets.video_default.resolution",
        "ratio": "assets.video_default.ratio",
        "duration": "assets.video_default.duration_s",
    }),
    SourceType.ASSET_IMAGE: MappingProxyType({"model": "image.model", "resolution": "image.resolution", "ratio": "image.ratio_by_subject", "duration": "image.model"}),
})

C, SEV = PrecheckCheck, CheckSeverity


def _key(request: GenerationRequest, leaf: str) -> str | None:
    return _KEYS.get(request.source.type, {}).get(leaf)


def _ok(check: PrecheckCheck, message: str, code: str = "ok") -> PrecheckItem:
    return PrecheckItem(check, SEV.OK, code, message)


def check_capability(request: GenerationRequest, ctx: PrecheckContext) -> list[PrecheckItem]:
    params = request.params
    assert params is not None
    capability: ModelCapability | None = ctx.limits.find(params.model)
    if capability is None:
        return [PrecheckItem(C.PARAMS, SEV.ERROR, "unknown_model", f"model_limits 里没有模型 {params.model}", _key(request, "model"))]
    if capability.kind is not request.kind:
        return [PrecheckItem(C.PARAMS, SEV.ERROR, "model_kind_mismatch", f"{params.model} 不能用于 {request.kind} 请求", _key(request, "model"))]
    return [
        *_params(request, capability),
        *_counts(request, capability),
        *_backend(request, capability, ctx),
        *_negative(request, capability, ctx),
    ]


def _params(request: GenerationRequest, cap: ModelCapability) -> list[PrecheckItem]:
    params = request.params
    assert params is not None
    items: list[PrecheckItem] = []
    if request.kind is GenerationKind.VIDEO:
        if params.duration_s is None:
            items.append(PrecheckItem(C.PARAMS, SEV.ERROR, "duration_missing", "缺少时长", _key(request, "duration")))
        elif not cap.supports_duration(params.duration_s):
            low, high = cap.duration_range or (0, 0)
            items.append(PrecheckItem(C.PARAMS, SEV.ERROR, "duration_out_of_range", f"{cap.key} 时长范围 {low}–{high}s，实际 {params.duration_s}s", _key(request, "duration")))
    if not cap.supports_resolution(params.resolution):
        items.append(PrecheckItem(C.PARAMS, SEV.ERROR, "resolution_unsupported", f"{cap.key} 不支持分辨率 {params.resolution}", _key(request, "resolution")))
    if not cap.supports_ratio(params.ratio):
        items.append(PrecheckItem(C.PARAMS, SEV.ERROR, "ratio_unsupported", f"{cap.key} 不支持比例 {params.ratio}", _key(request, "ratio")))
    return items or [_ok(C.PARAMS, "时长、分辨率、比例在模型范围内")]


def _counts(request: GenerationRequest, cap: ModelCapability) -> list[PrecheckItem]:
    refs = request.references
    limit_key: str = key_path(key_path("model_limits.models", cap.key), "max_images")
    checks: tuple[tuple[str, int, int], ...] = (
        ("图片", cap.image_count(refs), cap.max_images),
        ("视频", ModelCapability.count_of(refs, RefKind.VIDEO), cap.max_videos),
        ("音频", ModelCapability.count_of(refs, RefKind.AUDIO), cap.max_audios),
    )
    items: list[PrecheckItem] = [
        PrecheckItem(C.REFERENCE_COUNTS, SEV.ERROR, "reference_limit_exceeded", f"{label}参考 {count} 个，超过 {cap.key} 上限 {limit}", limit_key.replace("max_images", field))
        for (label, count, limit), field in zip(checks, ("max_images", "max_videos", "max_audios"))
        if count > limit
    ]
    return items or [_ok(C.REFERENCE_COUNTS, "参考种类与数量在上限内")]


def _backend(request: GenerationRequest, cap: ModelCapability, ctx: PrecheckContext) -> list[PrecheckItem]:
    routing_key: str | None = "routing.video" if request.kind is GenerationKind.VIDEO else None
    items: list[PrecheckItem] = []
    if not cap.supports_backend(ctx.backend):
        items.append(PrecheckItem(C.BACKEND, SEV.ERROR, "backend_unsupported", f"{ctx.backend} 通道不支持 {cap.key}（不降级）", routing_key))
    if request.entity_references:
        if cap.entities and not cap.supports_entities_on(ctx.backend):
            items.append(PrecheckItem(C.BACKEND, SEV.ERROR, "entities_unsupported_on_backend", f"{ctx.backend} 通道不支持主体", routing_key))
        elif not cap.entities:
            items.append(PrecheckItem(C.BACKEND, SEV.ERROR, "entities_unsupported", f"{cap.key} 不支持主体", _key(request, "model")))
    return items or [_ok(C.BACKEND, f"{ctx.backend} 通道具备所需能力")]


def _negative(request: GenerationRequest, cap: ModelCapability, ctx: PrecheckContext) -> list[PrecheckItem]:
    if request.kind is not GenerationKind.VIDEO or request.negative_prompt is None or cap.negative_prompt_field:
        return [_ok(C.NEGATIVE_PROMPT, "负向提示词无需处理或平台有负向输入框")]
    strategy: NegativePromptStrategy = ctx.negative_prompt_strategy
    if strategy is NegativePromptStrategy.FAIL:
        return [PrecheckItem(C.NEGATIVE_PROMPT, SEV.ERROR, "negative_prompt_unsupported", f"{cap.key} 没有负向输入框，策略为 fail", "video.negative_prompt")]
    if strategy is NegativePromptStrategy.PLATFORM_FIELD_OR_OMIT:
        return [PrecheckItem(C.NEGATIVE_PROMPT, SEV.WARNING, "negative_prompt_omitted", "平台无负向框，已省略负向提示词", "video.negative_prompt")]
    return [_ok(C.NEGATIVE_PROMPT, "按 config 策略省略负向提示词", "negative_prompt_omitted_by_config")]
