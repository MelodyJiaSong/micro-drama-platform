import pytest

from libs.common.canonical_json import canonical_sha256, sha256_hex
from libs.common.enums import RefKind
from libs.domain.errors.precheck__error import InvalidRequestError
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from tests.libs.domain.builders import SHA_A, SHA_B, SHOT_SLOT, entity_create_request, entity_ref, image_ref, video_request

BASE = video_request(refs=(image_ref("bg11-1", SHA_A), entity_ref(), image_ref("p2-1", SHA_B, "随身装备锚点")))


def fp(**kwargs: object) -> str:
    return Fingerprint.of(video_request(**kwargs)).value  # type: ignore[arg-type]


def test_matches_fr24_formula() -> None:
    request = BASE
    expected = canonical_sha256(
        {
            "kind": "video",
            "prompt_sha256": sha256_hex(request.prompt),
            "negative_prompt_sha256": None,
            "references": [
                {"kind": "image", "name": "bg11-1", "sha256": SHA_A},
                {"kind": "entity", "name": "砌炉的老人", "entity": "hy3_主角"},
                {"kind": "image", "name": "p2-1", "sha256": SHA_B},
            ],
            "params": {"model": "seedance2.5", "ratio": "16:9", "resolution": "720p", "count": 1, "duration_s": 22, "reference_mode": None},
            "output_slot": SHOT_SLOT,
        }
    )
    assert Fingerprint.of(request).value == expected


def test_golden_value_is_pinned() -> None:
    assert Fingerprint.of(BASE).value == "b2b42ace25377b2a5f633b11c6a8130a85b47d3b4c052d76b72630dbd680e7dd"


@pytest.mark.parametrize("suffix", [" ", "，", "　", "\n"])
def test_prompt_is_byte_exact(suffix: str) -> None:
    assert fp(prompt="shot02" + suffix) != fp(prompt="shot02")


def test_reference_order_matters() -> None:
    a, b = image_ref("bg11-1", SHA_A), image_ref("p2-1", SHA_B)
    assert fp(refs=(a, b)) != fp(refs=(b, a))


def test_sha_and_entity_name_are_tagged() -> None:
    as_file = ReferenceItem(name="x", label="场景参考图", kind=RefKind.IMAGE, resolved_path="p", sha256="hy3_主角")
    as_entity = ReferenceItem(name="x", label="人物主体", kind=RefKind.ENTITY, entity_name="hy3_主角")
    assert fp(refs=(as_file,)) != fp(refs=(as_entity,))


def test_boundary_shift_differs() -> None:
    assert fp(prompt="a", refs=(image_ref("bc"),)) != fp(prompt="ab", refs=(image_ref("c"),))


def test_null_negative_differs_from_empty() -> None:
    assert fp(negative=None) != fp(negative="")
    assert fp(negative="水印") != fp(negative=None)


def test_same_content_different_path_equal() -> None:
    a = ReferenceItem(name="bg11-1", label="场景参考图", kind=RefKind.IMAGE, resolved_path="ai_videos/a.png", sha256=SHA_A)
    b = ReferenceItem(name="bg11-1", label="场景参考图", kind=RefKind.IMAGE, resolved_path="ai_videos/b.png", sha256=SHA_A)
    assert fp(refs=(a,)) == fp(refs=(b,))


def test_output_slot_and_params_and_entity_name_matter() -> None:
    assert fp(output_slot=SHOT_SLOT + "x") != fp()
    assert fp(duration=10) != fp()
    assert fp(refs=(entity_ref(entity="hy3_砌炉的老人"),)) != fp(refs=(entity_ref(),))
    assert Fingerprint.of(entity_create_request("hy3_獾")) != Fingerprint.of(entity_create_request("hy3_獾2"))


def test_source_path_not_part_of_fingerprint() -> None:
    from dataclasses import replace

    moved = replace(BASE, source=replace(BASE.source, path="elsewhere.md"))
    assert Fingerprint.of(moved) == Fingerprint.of(BASE)


def test_large_prompt_ok() -> None:
    assert len(fp(prompt="字" * 1_000_000)) == 64


def test_invalid_value_rejected() -> None:
    with pytest.raises(InvalidRequestError):
        Fingerprint("xyz")
