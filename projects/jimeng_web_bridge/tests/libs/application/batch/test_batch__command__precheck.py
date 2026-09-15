from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, fields
from datetime import timedelta

import pytest

from libs.application.dtos.batch__dto import (
    AssetItemInput,
    BatchPrecheckCdto,
    EntityCreateItemInput,
    RawItemInput,
    ShotItemInput,
)
from libs.application.errors.batch__error import BatchItemRejectedError, BatchTooLargeError, IdempotencyKeyReusedError
from libs.common.enums import BackendKind, CheckSeverity, GenerationKind, PrecheckCheck, RefKind, SourceType
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.precheck_result__valueobject import PrecheckItem
from tests.libs.application.batch.support import (
    BG11,
    C1_1,
    C1_CARD,
    C1_DIR,
    C1_DIR_NAME,
    DUIKANG_SHOT01,
    HY3,
    P2,
    P3,
    REXUE,
    REXUE_SHOT01,
    REXUE_SHOT21,
    SHOT02,
    SHOT02_DIR,
    BatchEnv,
    hy3_config,
)
from tests.libs.infrastructure.support import write_file


def _items(env: BatchEnv, batch_id: str) -> tuple[BatchItem, ...]:
    stored = env.batches.get_stored(batch_id)
    assert stored is not None
    return stored.entity.items


def _only(env: BatchEnv, batch_id: str) -> BatchItem:
    items = _items(env, batch_id)
    assert len(items) == 1
    return items[0]


def _errors(item: BatchItem, code: str) -> list[PrecheckItem]:
    return [check for check in item.precheck.errors if check.error_code == code]


def test_hy3_shot02_is_three_hy3_uploads_plus_one_entity_mention(env: BatchEnv) -> None:
    cdto = env.command.precheck([ShotItemInput(SHOT02)], None)

    assert (cdto.error_count, cdto.warning_count, cdto.estimated_credits, cdto.state) == (0, 1, 440, "awaiting_confirm")
    item = _only(env, cdto.batch_id)
    request = item.request
    assert request.kind is GenerationKind.VIDEO and request.output_slot == SHOT02_DIR
    assert request.source.type is SourceType.SHOT and request.source.path == SHOT02
    assert request.params is not None
    assert (request.params.model, request.params.ratio, request.params.duration_s, request.params.resolution) == (
        "seedance2.5", "16:9", 22, "720p",
    )
    assert [ref.name for ref in request.references] == ["bg11-1", "砌炉的老人", "p2-1", "p3-1"]
    uploads = {ref.name: ref for ref in request.upload_references}
    assert {name: ref.resolved_path for name, ref in uploads.items()} == {"bg11-1": BG11, "p2-1": P2, "p3-1": P3}
    for ref in uploads.values():
        assert ref.kind is RefKind.IMAGE
        assert ref.sha256 == hashlib.sha256((env.repo / str(ref.resolved_path)).read_bytes()).hexdigest()
    assert request.mentioned_entity_names == ("hy3_主角",)
    assert request.negative_prompt is not None
    assert [check.error_code for check in item.precheck.warnings] == ["negative_prompt_omitted"]
    assert item.precheck.estimate.credits == 440
    stored = env.batches.get_stored(cdto.batch_id)
    assert stored is not None and stored.metas[0].backend is BackendKind.WEB and stored.metas[0].drama_rel == HY3


def test_precheck_result_never_carries_a_token(env: BatchEnv) -> None:
    cdto = env.command.precheck([ShotItemInput(SHOT02)], None)

    assert "token" not in {field.name for field in fields(BatchPrecheckCdto)}
    assert cdto.confirm_path == f"/batches/{cdto.batch_id}"
    token = env.query.confirmation(cdto.batch_id).token
    signature = token.rpartition(".")[2]
    assert signature not in json.dumps(asdict(cdto), ensure_ascii=False)
    assert signature not in json.dumps(asdict(env.query.get(cdto.batch_id, 1, 50)), ensure_ascii=False)


def test_legacy_reference_syntax_is_an_error_no_config_can_waive(env: BatchEnv) -> None:
    env.write_drama_config(REXUE, lambda data: data["references"]["overrides"].update({"学校泳池_bg2_水面_俯拍": f"{REXUE}/x.png"}))

    cdto = env.command.precheck([ShotItemInput(REXUE_SHOT01)], None)

    legacy = _errors(_only(env, cdto.batch_id), "legacy_reference_syntax")
    assert len(legacy) == 1
    assert legacy[0].config_key is None and not legacy[0].waivable
    assert "学校泳池_bg2_水面_俯拍=>@1" in legacy[0].message
    assert cdto.error_count == 1


def test_explicit_none_reference_line_is_legal_zero_references(env: BatchEnv) -> None:
    item = _only(env, env.command.precheck([ShotItemInput(REXUE_SHOT21)], None).batch_id)

    assert item.request.references == ()
    reference_checks = [check for check in item.precheck.items if check.check is PrecheckCheck.REFERENCES]
    assert [(check.severity, check.error_code) for check in reference_checks] == [(CheckSeverity.OK, "ok")]


@pytest.mark.parametrize(
    ("reference_line", "code"),
    [
        ("参考: 随手写的说明文字", "reference_line_unrecognized"),
        ("参考: 无\n备注: 还是要用 `bg11-1(场景参考图)=>@`", "reference_marker_mismatch"),
    ],
)
def test_unparsable_or_miscounted_reference_line_is_never_silently_zero(env: BatchEnv, reference_line: str, code: str) -> None:
    text = (env.repo / SHOT02).read_text(encoding="utf-8")
    original = next(line for line in text.split("\n") if line.startswith("参考:"))
    write_file(env.repo, f"{HY3}/5_6_分镜与prompt/shots/shot90/shot90.md", text.replace(original, reference_line))

    item = _only(env, env.command.precheck([ShotItemInput(f"{HY3}/5_6_分镜与prompt/shots/shot90/shot90.md")], None).batch_id)

    assert item.request.references == ()
    assert _errors(item, code)


def test_unsupported_ratio_keeps_the_raw_value_in_the_message(env: BatchEnv) -> None:
    item = _only(env, env.command.precheck([ShotItemInput(DUIKANG_SHOT01)], None).batch_id)

    assert item.request.params is not None and item.request.params.ratio == "2.35:1"
    ratio = _errors(item, "ratio_unsupported")
    assert len(ratio) == 1 and "2.35:1" in ratio[0].message


def test_ambiguous_reference_names_the_override_key_and_the_override_resolves_it(env: BatchEnv) -> None:
    write_file(env.repo, BG11.replace(".png", ".jpg"), b"a second bg11-1 in hy3")

    ambiguous = _errors(_only(env, env.command.precheck([ShotItemInput(SHOT02)], None).batch_id), "ambiguous_reference")

    assert len(ambiguous) == 1
    assert ambiguous[0].reference_name == "bg11-1"
    assert ambiguous[0].config_key == "references.overrides.bg11-1" and ambiguous[0].waivable

    env.write_drama_config(HY3, hy3_config(**{"bg11-1": BG11}))
    item = _only(env, env.command.precheck([ShotItemInput(SHOT02)], None).batch_id)
    assert not item.precheck.has_errors
    assert next(ref for ref in item.request.references if ref.name == "bg11-1").resolved_path == BG11


def test_missing_reference_names_the_override_key(env: BatchEnv) -> None:
    (env.repo / P3).unlink()

    missing = _errors(_only(env, env.command.precheck([ShotItemInput(SHOT02)], None).batch_id), "reference_not_found")

    assert [(check.reference_name, check.config_key) for check in missing] == [("p3-1", "references.overrides.p3-1")]


def test_missing_drama_config_uses_defaults_and_points_to_propose(env: BatchEnv) -> None:
    (env.repo / HY3 / "jimeng_config.toml").unlink()

    item = _only(env, env.command.precheck([ShotItemInput(SHOT02)], None).batch_id)

    assert "drama_config_missing" in [check.error_code for check in item.precheck.warnings]
    assert item.request.mentioned_entity_names == ("hy3_砌炉的老人",)
    not_on_platform = _errors(item, "entity_not_on_platform")
    assert [check.config_key for check in not_on_platform] == [f'entities.overrides."{C1_DIR_NAME}"']


def test_invalid_drama_config_is_an_error_item_with_its_field_path(env: BatchEnv) -> None:
    env.write_drama_config(HY3, lambda data: data["video"].update({"model": "seedream5.0"}))

    invalid = _errors(_only(env, env.command.precheck([ShotItemInput(SHOT02)], None).batch_id), "drama_config_invalid")

    assert [check.config_key for check in invalid] == ["video.model"]


def test_idempotency_same_body_replays_and_other_body_conflicts_until_retention_ends(env: BatchEnv) -> None:
    first = env.command.precheck([ShotItemInput(SHOT02)], "k-hy3-ep-01")
    env.clock.advance(timedelta(hours=1))

    assert env.command.precheck([ShotItemInput(SHOT02)], "k-hy3-ep-01") == first
    assert env.batch_count() == 1
    with pytest.raises(IdempotencyKeyReusedError):
        env.command.precheck([ShotItemInput(SHOT02, reroll=True)], "k-hy3-ep-01")
    assert env.batch_count() == 1

    env.clock.advance(timedelta(hours=24))
    later = env.command.precheck([ShotItemInput(SHOT02, reroll=True)], "k-hy3-ep-01")
    assert later.batch_id != first.batch_id


def test_item_limit_comes_from_global_config(env: BatchEnv) -> None:
    env.set_global("api", "max_batch_items", 1)

    with pytest.raises(BatchTooLargeError) as caught:
        env.command.precheck([ShotItemInput(SHOT02), ShotItemInput(SHOT02)], None)

    assert caught.value.config_key == "api.max_batch_items"
    assert env.batch_count() == 0


def test_hy3_c1_card_yields_cli_image_block_and_web_turntable_block(env: BatchEnv) -> None:
    cdto = env.command.precheck([AssetItemInput(C1_CARD, "c1-1"), AssetItemInput(C1_CARD, "c1-2")], None)

    stored = env.batches.get_stored(cdto.batch_id)
    assert stored is not None and cdto.error_count == 0
    (image, video), (image_meta, video_meta) = stored.entity.items, stored.metas
    assert image.request.kind is GenerationKind.IMAGE and image_meta.backend is BackendKind.CLI
    assert image.request.params is not None
    assert (image.request.params.model, image.request.params.ratio, image.request.params.resolution) == ("seedream5.0", "3:4", "2k")
    assert image.request.references == () and image.request.output_slot == f"{C1_DIR}#c1-1"
    assert (image.request.source.type, image.request.source.block_key) == (SourceType.ASSET_IMAGE, "c1-1")
    assert image.precheck.estimate.credits == 1

    assert video.request.kind is GenerationKind.VIDEO and video_meta.backend is BackendKind.WEB
    assert video.request.params is not None
    assert (video.request.params.model, video.request.params.ratio, video.request.params.duration_s) == ("seedance2.5", "9:16", 4)
    assert [(ref.name, ref.kind, ref.resolved_path) for ref in video.request.references] == [("c1-1", RefKind.IMAGE, C1_1)]
    assert video.request.output_slot == f"{C1_DIR}#c1-2" and video.request.source.type is SourceType.ASSET_VIDEO
    assert video.precheck.estimate.credits == 80


def test_entity_create_item_estimates_zero_and_reuses_an_existing_entity(env: BatchEnv) -> None:
    cdto = env.command.precheck([EntityCreateItemInput(HY3, C1_DIR_NAME)], None)

    item = _only(env, cdto.batch_id)
    assert item.request.kind is GenerationKind.ENTITY and item.request.entity_name == "hy3_主角"
    assert [(ref.name, ref.resolved_path) for ref in item.request.references] == [("c1-1", C1_1)]
    assert item.request.prompt == "旧靛蓝粗布对襟上衣深棕灯芯绒长裤褐色毡帽，腰后别一把木柄旧抹泥板，六十余岁精瘦"
    assert item.precheck.estimate.credits == 0 and cdto.estimated_credits == 0
    assert "entity_will_be_reused" in [check.error_code for check in item.precheck.items]

    env.write_drama_config(HY3)
    fresh = _only(env, env.command.precheck([EntityCreateItemInput(HY3, C1_DIR_NAME, "改过的描述")], None).batch_id)
    assert fresh.request.entity_name == "hy3_砌炉的老人" and fresh.request.prompt == "改过的描述"
    assert fresh.precheck.severity is CheckSeverity.OK


@pytest.mark.parametrize(
    "item",
    [
        ShotItemInput(SHOT02.replace("/", "\\")),
        ShotItemInput("ai_videos/../CLAUDE.md"),
        AssetItemInput(C1_CARD.replace("/", "\\", 1), "c1-1"),
        EntityCreateItemInput(HY3.replace("/", "\\"), C1_DIR_NAME),
        EntityCreateItemInput(HY3, "..\\c1"),
        RawItemInput("image", "x", (BG11.replace("/", "\\"),), (), {"ratio": "1:1"}, SHOT02_DIR),
        RawItemInput("image", "x", (BG11,), (), {"ratio": "1:1"}, "projects/jimeng_web_bridge"),
        RawItemInput("image", "x", ("//server/share/x.png",), (), {"ratio": "1:1"}, SHOT02_DIR),
    ],
)
def test_client_paths_must_be_canonical_and_sandboxed(env: BatchEnv, item: object) -> None:
    with pytest.raises(BatchItemRejectedError) as caught:
        env.command.precheck([item], None)  # type: ignore[list-item]

    assert caught.value.reason == "path_rejected" and caught.value.index == 0
    assert env.batch_count() == 0


def test_raw_video_item_orders_files_then_entities(env: BatchEnv) -> None:
    raw = RawItemInput("video", "镜头 `bg11-1(场景参考图)=>@` 他 `主角(人物主体)=>@`", (BG11,), ("hy3_主角",), {"ratio": "16:9", "duration_s": 5}, SHOT02_DIR)

    item = _only(env, env.command.precheck([raw], None).batch_id)

    assert [(ref.name, ref.kind) for ref in item.request.references] == [("bg11-1", RefKind.IMAGE), ("hy3_主角", RefKind.ENTITY)]
    assert item.request.source.type is SourceType.RAW and item.precheck.estimate.credits == 100
    assert not item.precheck.has_errors
