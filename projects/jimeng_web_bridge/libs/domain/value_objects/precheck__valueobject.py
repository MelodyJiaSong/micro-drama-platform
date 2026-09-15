from libs.common.enums import CheckSeverity, GenerationKind, PrecheckCheck
from libs.domain.value_objects.config_table__valueobject import key_path
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.precheck_capability__valueobject import check_capability
from libs.domain.value_objects.precheck_context__valueobject import PrecheckContext
from libs.domain.value_objects.precheck_result__valueobject import LEGACY_REFERENCE_SYNTAX, PrecheckItem, PrecheckResult
from libs.domain.value_objects.price_estimate__valueobject import PriceEstimate

C, SEV = PrecheckCheck, CheckSeverity
LEGACY_HINT = "v1 只支持现行写法，请把该镜 `参考:` 行改为 `{名}({类型})=>@`"


def _override_key(name: str) -> str:
    return key_path("references.overrides", name)


def run_precheck(request: GenerationRequest, ctx: PrecheckContext) -> PrecheckResult:
    items: list[PrecheckItem] = _references(request, ctx)
    if request.kind is GenerationKind.ENTITY:
        items.extend(_entity_create(request, ctx))
    else:
        items.extend(check_capability(request, ctx))
        items.append(_prompt_length(request, ctx))
        items.extend(_mentions(request, ctx))
        items.append(
            PrecheckItem(C.OUTPUT, SEV.ERROR, "output_not_writable", "输出目录不可写")
            if not ctx.output_dir_writable
            else PrecheckItem(C.OUTPUT, SEV.OK, "ok", "输出目录可写")
        )
    items.append(_fingerprint(ctx))
    estimate: PriceEstimate = ctx.price_table.estimate(request)
    items.append(
        PrecheckItem(C.PRICE, SEV.WARNING, "price_unavailable", estimate.warning or "无法估算", estimate.config_key)
        if not estimate.known
        else PrecheckItem(C.PRICE, SEV.OK, "ok", f"预计 {estimate.credits} 积分")
    )
    existing: str | None = None if ctx.reroll else ctx.fingerprint_hit_job_id
    return PrecheckResult(items=tuple(items), estimate=estimate, existing_job_id=existing)


def _references(request: GenerationRequest, ctx: PrecheckContext) -> list[PrecheckItem]:
    items: list[PrecheckItem] = []
    if ctx.legacy_reference_fragments:
        fragments: str = "、".join(ctx.legacy_reference_fragments)
        items.append(PrecheckItem(C.REFERENCES, SEV.ERROR, LEGACY_REFERENCE_SYNTAX, f"{LEGACY_HINT}（{fragments}）"))
    reported: set[str] = set()
    for issue in ctx.reference_issues:
        config_key: str | None = None if issue.error_code == LEGACY_REFERENCE_SYNTAX else issue.config_key
        items.append(PrecheckItem(C.REFERENCES, SEV.ERROR, issue.error_code, issue.message, config_key, issue.reference_name))
        if issue.reference_name is not None:
            reported.add(issue.reference_name)
    for ref in request.upload_references:
        if (ref.resolved_path is None or ref.sha256 is None) and ref.name not in reported:
            items.append(
                PrecheckItem(C.REFERENCES, SEV.ERROR, "reference_unreadable", f"参考项 {ref.name} 不存在或不可读", _override_key(ref.name), ref.name)
            )
    return items or [PrecheckItem(C.REFERENCES, SEV.OK, "ok", f"{len(request.references)} 个参考项均已解析")]


def _prompt_length(request: GenerationRequest, ctx: PrecheckContext) -> PrecheckItem:
    count: int = request.prompt_codepoints()
    if count > ctx.prompt_max_chars:
        return PrecheckItem(C.PROMPT_LENGTH, SEV.ERROR, "prompt_too_long", f"prompt {count} 码点，超过 {ctx.prompt_max_chars}", "precheck.prompt_max_chars")
    return PrecheckItem(C.PROMPT_LENGTH, SEV.OK, "ok", f"prompt {count} 码点")


def _snapshot_items(ctx: PrecheckContext) -> list[PrecheckItem]:
    if ctx.snapshot.never_synced:
        return [PrecheckItem(C.ENTITIES, SEV.ERROR, "entity_snapshot_missing", "从未同步过主体快照，请先在主体对账页同步")]
    if ctx.snapshot.is_stale(ctx.now, ctx.snapshot_stale_after):
        return [PrecheckItem(C.ENTITIES, SEV.WARNING, "entity_snapshot_stale", "主体快照已过期，建议重新同步", "entities.snapshot_stale_h")]
    return []


def _mentions(request: GenerationRequest, ctx: PrecheckContext) -> list[PrecheckItem]:
    refs = request.entity_references
    if not refs:
        return [PrecheckItem(C.ENTITIES, SEV.OK, "ok", "无主体引用")]
    items: list[PrecheckItem] = _snapshot_items(ctx)
    for ref in refs:
        name: str = ref.entity_name or ""
        card_dir: str | None = ctx.entity_card_dirs.get(name)
        key: str = key_path("entities.overrides", card_dir) if card_dir else _override_key(ref.name)
        if len(name) > ctx.entity_name_max_chars:
            items.append(PrecheckItem(C.ENTITIES, SEV.ERROR, "entity_name_too_long", f"主体名 {name} 超过 {ctx.entity_name_max_chars} 码点", key, ref.name))
        elif not ctx.snapshot.never_synced and name not in ctx.snapshot.names:
            items.append(PrecheckItem(C.ENTITIES, SEV.ERROR, "entity_not_on_platform", f"即梦上没有主体 {name}，请在主体对账页处理", key, ref.name))
    return items or [PrecheckItem(C.ENTITIES, SEV.OK, "ok", "主体均存在于快照")]


def _entity_create(request: GenerationRequest, ctx: PrecheckContext) -> list[PrecheckItem]:
    name: str = request.entity_name or ""
    card_dir_name: str = request.source.path.rstrip("/").split("/")[-1]
    items: list[PrecheckItem] = []
    if len(name) > ctx.entity_name_max_chars:
        items.append(PrecheckItem(C.ENTITY_CREATE, SEV.ERROR, "entity_name_too_long", f"主体名 {name} 超过 {ctx.entity_name_max_chars} 码点", key_path("entities.overrides", card_dir_name)))
    if not request.references:
        items.append(PrecheckItem(C.ENTITY_CREATE, SEV.ERROR, "entity_source_image_missing", "角色卡里找不到主体参考图", "entities.source_images"))
    items.extend(_snapshot_items(ctx))
    if any(item.severity is SEV.ERROR for item in items):
        return items
    if name in ctx.snapshot.names:
        return [*items, PrecheckItem(C.ENTITY_CREATE, SEV.OK, "entity_will_be_reused", f"即梦上已有同名主体 {name}，复用不创建")]
    return [*items, PrecheckItem(C.ENTITY_CREATE, SEV.OK, "ok", f"将新建主体 {name}")]


def _fingerprint(ctx: PrecheckContext) -> PrecheckItem:
    if ctx.fingerprint_hit_job_id is None:
        return PrecheckItem(C.FINGERPRINT, SEV.OK, "ok", "无重复作业")
    if ctx.reroll:
        return PrecheckItem(C.FINGERPRINT, SEV.OK, "reroll_new_attempt", f"reroll：与作业 {ctx.fingerprint_hit_job_id} 相同，将新建 attempt")
    return PrecheckItem(C.FINGERPRINT, SEV.WARNING, "duplicate_of_existing_job", f"与作业 {ctx.fingerprint_hit_job_id} 内容相同，确认后直接返回该作业")
