import ast
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest

from libs.common.enums import BackendKind, CheckSeverity, NegativePromptStrategy, RefKind, SourceType
from libs.domain.value_objects.model_limits__valueobject import ModelLimits
from libs.domain.value_objects.precheck__valueobject import run_precheck
from libs.domain.value_objects.precheck_context__valueobject import EntitySnapshotFacts, ReferenceIssue
from libs.domain.value_objects.precheck_result__valueobject import PrecheckResult
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from tests.libs.domain.builders import (
    T0, context, entity_create_request, entity_ref, global_data, image_ref, image_request, video_request,
)


def refs(images: int = 0, videos: int = 0, audios: int = 0, entities: int = 0, first_frames: int = 0) -> tuple[ReferenceItem, ...]:
    items: list[ReferenceItem] = []
    items += [image_ref(f"i{n}") for n in range(images)]
    items += [image_ref(f"v{n}", kind=RefKind.VIDEO) for n in range(videos)]
    items += [image_ref(f"a{n}", kind=RefKind.AUDIO) for n in range(audios)]
    items += [image_ref(f"f{n}", label="上一镜末帧", kind=RefKind.FIRST_FRAME) for n in range(first_frames)]
    items += [entity_ref(f"e{n}") for n in range(entities)]
    return tuple(items)


def codes(result: PrecheckResult) -> dict[str, str | None]:
    return {item.error_code: item.config_key for item in result.errors}


CAPABILITY: list[tuple[str, dict[str, object], BackendKind, dict[str, str | None]]] = [
    ("C01", {"duration": 30, "refs": refs(3, entities=1), "prompt": "字" * 1200}, BackendKind.WEB, {}),
    ("C02", {"duration": 31, "refs": refs(3, entities=1)}, BackendKind.WEB, {"duration_out_of_range": "video.model"}),
    ("C03", {"duration": 3, "refs": refs(1)}, BackendKind.WEB, {"duration_out_of_range": "video.model"}),
    ("C04", {"duration": 4, "resolution": "480p", "refs": refs(1)}, BackendKind.WEB, {}),
    ("C05", {"resolution": "1080p", "refs": refs(3, entities=1)}, BackendKind.WEB, {"resolution_unsupported": "video.resolution"}),
    ("C06", {"model": "seedance2.0_vip", "duration": 15, "resolution": "1080p", "refs": refs(9, 3, 3, 1)}, BackendKind.WEB, {}),
    ("C07", {"model": "seedance2.0_vip", "duration": 16, "refs": refs(1)}, BackendKind.WEB, {"duration_out_of_range": "video.model"}),
    ("C08", {"model": "seedance2.0", "duration": 10, "resolution": "1080p", "refs": refs(1)}, BackendKind.WEB, {"resolution_unsupported": "video.resolution"}),
    ("C09", {"model": "seedance2.0fast", "duration": 10, "refs": refs(1)}, BackendKind.WEB, {}),
    ("C10", {"refs": refs(30, 10, 10, 1)}, BackendKind.WEB, {}),
    ("C11", {"refs": refs(31)}, BackendKind.WEB, {"reference_limit_exceeded": 'model_limits.models."seedance2.5".max_images'}),
    ("C12", {"refs": refs(videos=11)}, BackendKind.WEB, {"reference_limit_exceeded": 'model_limits.models."seedance2.5".max_videos'}),
    ("C13", {"model": "seedance2.0_vip", "duration": 10, "refs": refs(10)}, BackendKind.WEB, {"reference_limit_exceeded": 'model_limits.models."seedance2.0_vip".max_images'}),
    ("C14", {"refs": refs(30, first_frames=1)}, BackendKind.WEB, {"reference_limit_exceeded": 'model_limits.models."seedance2.5".max_images'}),
    ("C15", {"refs": refs(3)}, BackendKind.CLI, {"backend_unsupported": "routing.video"}),
    ("C16", {"model": "seedance2.0_vip", "duration": 15, "refs": refs(9, 3, 3)}, BackendKind.CLI, {}),
    ("C17", {"model": "seedance2.0_vip", "duration": 12, "refs": refs(2, entities=1)}, BackendKind.CLI, {"entities_unsupported_on_backend": "routing.video"}),
    ("C25", {"refs": refs(1), "prompt": "字" * 5000}, BackendKind.WEB, {}),
    ("C26", {"refs": refs(1), "prompt": "字" * 5001}, BackendKind.WEB, {"prompt_too_long": "precheck.prompt_max_chars"}),
    ("C28", {"model": "seedance3.0", "refs": refs(1)}, BackendKind.WEB, {"unknown_model": "video.model"}),
    ("kind", {"model": "seedream5.0", "refs": refs(1)}, BackendKind.WEB, {"model_kind_mismatch": "video.model"}),
]


@pytest.mark.parametrize(("case", "kwargs", "backend", "expected"), CAPABILITY, ids=[c[0] for c in CAPABILITY])
def test_video_capability(case: str, kwargs: dict[str, object], backend: BackendKind, expected: dict[str, str | None]) -> None:
    request = video_request(**kwargs)  # type: ignore[arg-type]
    result = run_precheck(request, context(backend=backend))
    assert codes(result) == expected
    assert request.params == video_request(**kwargs).params  # type: ignore[arg-type]


IMAGE_CASES: list[tuple[str, dict[str, object], BackendKind, dict[str, str | None]]] = [
    ("C18", {}, BackendKind.CLI, {}),
    ("C19", {"resolution": "4k", "refs": refs(10)}, BackendKind.CLI, {}),
    ("C20", {"refs": refs(11)}, BackendKind.CLI, {"reference_limit_exceeded": 'model_limits.models."seedream5.0".max_images'}),
    ("C21", {"resolution": "1k"}, BackendKind.CLI, {"resolution_unsupported": "image.resolution"}),
    ("C22", {"model": "seedream3.0", "resolution": "4k", "ratio": "1:1"}, BackendKind.CLI, {"resolution_unsupported": "image.resolution"}),
    ("C23", {"refs": refs(1, entities=1)}, BackendKind.CLI, {"entities_unsupported": "image.model"}),
    ("C24", {}, BackendKind.WEB, {"backend_unsupported": None}),
    ("ratio", {"ratio": "5:4"}, BackendKind.CLI, {"ratio_unsupported": "image.ratio_by_subject"}),
]


@pytest.mark.parametrize(("case", "kwargs", "backend", "expected"), IMAGE_CASES, ids=[c[0] for c in IMAGE_CASES])
def test_image_capability(case: str, kwargs: dict[str, object], backend: BackendKind, expected: dict[str, str | None]) -> None:
    assert codes(run_precheck(image_request(**kwargs), context(backend=backend))) == expected  # type: ignore[arg-type]


def test_asset_video_and_raw_config_keys() -> None:
    asset = video_request(duration=31, source_type=SourceType.ASSET_VIDEO)
    assert codes(run_precheck(asset, context())) == {"duration_out_of_range": "assets.video_default.duration_s"}
    raw = video_request(duration=31, source_type=SourceType.RAW)
    assert codes(run_precheck(raw, context())) == {"duration_out_of_range": None}


def test_missing_duration() -> None:
    assert "duration_missing" in codes(run_precheck(video_request(duration=None), context()))


def test_reference_issues_relayed_and_legacy_not_waivable() -> None:
    ctx = context(
        legacy_reference_fragments=("学校泳池_bg2_水面_俯拍=>@1", "裴昭=>"),
        reference_issues=(
            ReferenceIssue("ambiguous_reference", "多重匹配", "bg3-1", 'references.overrides."bg3-1"'),
            ReferenceIssue("legacy_reference_syntax", "旧写法", "x", "references.overrides.x"),
        ),
    )
    result = run_precheck(video_request(refs=(image_ref("bg3-1", sha=None),)), ctx)
    legacy = [i for i in result.errors if i.error_code == "legacy_reference_syntax"]
    assert len(legacy) == 2 and all(i.config_key is None and not i.waivable for i in legacy)
    assert "`{名}({类型})=>@`" in legacy[0].message
    ambiguous = next(i for i in result.errors if i.error_code == "ambiguous_reference")
    assert ambiguous.config_key == 'references.overrides."bg3-1"' and ambiguous.waivable
    assert not any(i.error_code == "reference_unreadable" for i in result.errors)


def test_unresolved_reference_without_issue_is_error() -> None:
    result = run_precheck(video_request(refs=(image_ref("砍刀", sha=None),)), context())
    assert codes(result) == {"reference_unreadable": 'references.overrides."砍刀"'}


def test_entity_checks() -> None:
    assert codes(run_precheck(video_request(refs=(entity_ref(entity="hy3_砌炉的老人"),)), context())) == {
        "entity_not_on_platform": 'references.overrides."砌炉的老人"'
    }
    long_name = "hy3_" + "长" * 17
    assert "entity_name_too_long" in codes(run_precheck(video_request(refs=(entity_ref(entity=long_name),)), context()))
    never = context(snapshot=EntitySnapshotFacts(frozenset(), None))
    assert codes(run_precheck(video_request(refs=(entity_ref(),)), never)) == {"entity_snapshot_missing": None}


def test_entity_hint_uses_card_dir_when_known() -> None:
    long_name = "hy3_" + "长" * 17
    request = video_request(refs=(entity_ref(name="老人", entity=long_name),))
    card = "c3_在草崖下砌了一辈子炉子的沉默的老人"
    known = run_precheck(request, context(entity_card_dirs={long_name: card}))
    assert codes(known) == {"entity_name_too_long": f'entities.overrides."{card}"'}
    assert codes(run_precheck(request, context())) == {"entity_name_too_long": 'references.overrides."老人"'}
    missing = video_request(refs=(entity_ref(entity="hy3_砌炉的老人"),))
    hinted = run_precheck(missing, context(entity_card_dirs={"hy3_砌炉的老人": "c1_砌炉的老人"}))
    assert codes(hinted) == {"entity_not_on_platform": 'entities.overrides."c1_砌炉的老人"'}


def test_seedream3_is_text2image_only() -> None:
    result = run_precheck(image_request(model="seedream3.0", refs=(image_ref(),)), context(backend=BackendKind.CLI))
    assert codes(result) == {"reference_limit_exceeded": 'model_limits.models."seedream3.0".max_images'}


@pytest.mark.parametrize(("age", "severity"), [(timedelta(hours=23, minutes=59), CheckSeverity.OK), (timedelta(hours=24, minutes=1), CheckSeverity.WARNING)])
def test_snapshot_staleness(age: timedelta, severity: CheckSeverity) -> None:
    ctx = context(snapshot=EntitySnapshotFacts(frozenset({"hy3_主角"}), T0 - age))
    assert run_precheck(video_request(refs=(entity_ref(),)), ctx).severity is severity


def test_output_and_fingerprint() -> None:
    assert codes(run_precheck(video_request(), context(output_dir_writable=False))) == {"output_not_writable": None}
    hit = run_precheck(video_request(), context(fingerprint_hit_job_id="job-0"))
    assert hit.existing_job_id == "job-0" and hit.severity is CheckSeverity.WARNING
    reroll = run_precheck(video_request(), context(fingerprint_hit_job_id="job-0", reroll=True))
    assert reroll.existing_job_id is None and reroll.severity is CheckSeverity.OK


def _limits_with_negative_field() -> ModelLimits:
    data = global_data()
    data["model_limits"]["models"]["seedance2.5"]["negative_prompt_field"] = True  # type: ignore[index]
    return ModelLimits.from_dict(data["model_limits"])  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("strategy", "negative", "has_field", "severity"),
    [
        (NegativePromptStrategy.FAIL, "水印", False, CheckSeverity.ERROR),
        (NegativePromptStrategy.FAIL, "水印", True, CheckSeverity.OK),
        (NegativePromptStrategy.FAIL, None, False, CheckSeverity.OK),
        (NegativePromptStrategy.PLATFORM_FIELD_OR_OMIT, "水印", False, CheckSeverity.WARNING),
        (NegativePromptStrategy.PLATFORM_FIELD_OR_OMIT, "水印", True, CheckSeverity.OK),
        (NegativePromptStrategy.OMIT, "水印", False, CheckSeverity.OK),
    ],
)
def test_negative_prompt_strategy(strategy: NegativePromptStrategy, negative: str | None, has_field: bool, severity: CheckSeverity) -> None:
    overrides: dict[str, object] = {"negative_prompt_strategy": strategy}
    if has_field:
        overrides["limits"] = _limits_with_negative_field()
    result = run_precheck(video_request(negative=negative), context(**overrides))
    assert result.severity is severity
    if severity is CheckSeverity.ERROR:
        assert codes(result) == {"negative_prompt_unsupported": "video.negative_prompt"}


def test_entity_create() -> None:
    assert run_precheck(entity_create_request(), context()).severity is CheckSeverity.OK
    reuse = run_precheck(entity_create_request("hy3_主角"), context())
    assert any(i.error_code == "entity_will_be_reused" for i in reuse.items) and reuse.estimate.credits == 0
    assert codes(run_precheck(entity_create_request("hy3_" + "长" * 17), context())) == {"entity_name_too_long": 'entities.overrides."c2_獾"'}
    assert codes(run_precheck(entity_create_request(refs=()), context())) == {"entity_source_image_missing": "entities.source_images"}
    never = context(snapshot=EntitySnapshotFacts(frozenset(), None))
    assert codes(run_precheck(entity_create_request(), never)) == {"entity_snapshot_missing": None}


def test_price_estimates() -> None:
    assert run_precheck(video_request(count=2), context()).estimate.credits == 880
    unknown = run_precheck(video_request(resolution="480p"), context())
    assert unknown.estimate.credits is None and unknown.severity is CheckSeverity.WARNING
    assert next(i for i in unknown.warnings if i.error_code == "price_unavailable").config_key == "price_table.video"


def test_aggregation_and_purity() -> None:
    request, ctx = video_request(), context()
    first, second = run_precheck(request, ctx), run_precheck(request, ctx)
    assert first == second and first.severity is CheckSeverity.OK and not first.has_errors
    bad = run_precheck(replace(request, prompt="字" * 5001), ctx)
    assert bad.has_errors and bad.severity is CheckSeverity.ERROR


def test_precheck_modules_do_no_io() -> None:
    root = Path(__file__).resolve().parents[4] / "libs" / "domain" / "value_objects"
    for name in ("precheck__valueobject.py", "precheck_capability__valueobject.py", "precheck_context__valueobject.py"):
        tree = ast.parse((root / name).read_text(encoding="utf-8"))
        imported = {alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        imported |= {(node.module or "").split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        assert not imported & {"os", "pathlib", "sqlite3", "subprocess", "io"}
