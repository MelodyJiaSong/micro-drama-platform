from dataclasses import replace

import pytest

from libs.common.enums import BackendKind, GenerationKind, RefKind, SourceType
from libs.domain.errors.precheck__error import FrozenRequestIncompleteError, InvalidRequestError
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from tests.libs.domain.builders import SHA_A, SHA_B, confirmed_item, entity_create_request, entity_ref, image_ref, video_request


def test_request_helpers() -> None:
    req = video_request(prompt="字🙂\n", refs=(image_ref(), entity_ref()), negative="水印")
    assert req.prompt_codepoints() == 3
    assert req.mentioned_entity_names == ("hy3_主角",)
    assert [r.name for r in req.upload_references] == ["bg11-1"]
    assert req.negative_prompt_sha256() is not None and video_request().negative_prompt_sha256() is None


@pytest.mark.parametrize(
    "kwargs",
    [{"model": ""}, {"ratio": ""}, {"resolution": ""}, {"count": 0}, {"count": True}, {"duration_s": -1}],
)
def test_params_invariants(kwargs: dict[str, object]) -> None:
    base: dict[str, object] = {"model": "m", "ratio": "16:9", "resolution": "720p", "count": 1, "duration_s": 4}
    base.update(kwargs)
    with pytest.raises(InvalidRequestError):
        GenerationParams(**base)  # type: ignore[arg-type]


def test_reference_item_invariants() -> None:
    with pytest.raises(InvalidRequestError):
        ReferenceItem(name="x", label="人物主体", kind=RefKind.ENTITY)
    with pytest.raises(InvalidRequestError):
        ReferenceItem(name="x", label="人物主体", kind=RefKind.ENTITY, entity_name="e", resolved_path="p")
    with pytest.raises(InvalidRequestError):
        ReferenceItem(name="x", label="场景参考图", kind=RefKind.IMAGE, entity_name="e")
    with pytest.raises(InvalidRequestError):
        ReferenceItem(name="", label="场景参考图", kind=RefKind.IMAGE)


def test_request_invariants() -> None:
    base = video_request()
    with pytest.raises(InvalidRequestError):
        replace(base, references=[image_ref()])  # type: ignore[arg-type]
    with pytest.raises(InvalidRequestError):
        replace(base, output_slot="")
    with pytest.raises(InvalidRequestError):
        replace(base, params=None)
    with pytest.raises(InvalidRequestError):
        replace(base, kind=GenerationKind.IMAGE)
    with pytest.raises(InvalidRequestError):
        replace(base, entity_name="hy3_x")


def test_entity_create_invariants() -> None:
    req = entity_create_request()
    assert req.params is None and req.entity_name == "hy3_獾"
    with pytest.raises(InvalidRequestError):
        replace(req, entity_name=None)
    with pytest.raises(InvalidRequestError):
        replace(req, references=(entity_ref(),))
    with pytest.raises(InvalidRequestError):
        replace(req, source=replace(req.source, type=SourceType.SHOT))


def test_freeze_requires_resolved_references() -> None:
    with pytest.raises(FrozenRequestIncompleteError):
        FrozenRequest.freeze(video_request(refs=(image_ref(sha=None),)), BackendKind.WEB, "digest", 440, 20)
    with pytest.raises(FrozenRequestIncompleteError):
        FrozenRequest.freeze(video_request(), BackendKind.WEB, "", 440, 20)


@pytest.mark.parametrize(("credits", "tolerance"), [(-1, 20), (True, 20), (440, -1), (440, 101), (440, True)])
def test_frozen_estimate_and_tolerance_bounds(credits: int, tolerance: int) -> None:
    with pytest.raises(FrozenRequestIncompleteError):
        FrozenRequest.freeze(video_request(), BackendKind.WEB, "digest", credits, tolerance)


def test_from_item_copies_confirmed_estimate() -> None:
    item = confirmed_item(video_request(), 440)
    frozen = FrozenRequest.from_item(item, BackendKind.CLI, "digest", 15)
    assert (frozen.request, frozen.backend, frozen.credits_estimated, frozen.estimate_tolerance_pct) == (item.request, BackendKind.CLI, 440, 15)
    assert FrozenRequest.from_item(confirmed_item(video_request(), None), BackendKind.WEB, "d", 0).credits_estimated is None


def test_frozen_fingerprint_must_match_content() -> None:
    other = Fingerprint.of(video_request(duration=10))
    with pytest.raises(FrozenRequestIncompleteError):
        FrozenRequest(video_request(), BackendKind.WEB, "digest", 440, 20, other)


def test_changed_references_detects_inputs_changed() -> None:
    a, b = image_ref("bg11-1", SHA_A), image_ref("p2-1", SHA_B)
    frozen = FrozenRequest.freeze(video_request(refs=(a, b, entity_ref())), BackendKind.WEB, "digest", 440, 20)
    assert frozen.entity_names == ("hy3_主角",)
    assert frozen.changed_references({a.resolved_path or "": SHA_A, b.resolved_path or "": SHA_B}) == ()
    assert frozen.changed_references({a.resolved_path or "": SHA_A, b.resolved_path or "": "c" * 64}) == (b,)
    assert frozen.changed_references({a.resolved_path or "": SHA_A}) == (b,)
