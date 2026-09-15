import pytest

from libs.common.enums import ReferenceResolver, RefKind
from libs.domain.errors.config__error import ConfigError
from libs.domain.value_objects.config_table__valueobject import ConfigTable
from libs.domain.value_objects.reference_routing__valueobject import ReferenceOverride, ReferenceRouting
from libs.domain.value_objects.reference_rule__valueobject import DEFAULT_REFERENCE_RULES, ReferenceRule

DEFAULT = ReferenceRouting(rules=DEFAULT_REFERENCE_RULES, overrides={})

LABELS: list[tuple[str, RefKind | None, ReferenceResolver | None]] = [
    ("场景参考图", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("场景参考图·第四段：坑口全景（根盘背面冒烟）", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("随身装备锚点", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("犀鸟锚点", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("角色参考图", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("单位参考图", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("道具参考图", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("场景主体", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("物件主体", RefKind.IMAGE, ReferenceResolver.ASSET_FILE),
    ("Seedance 人物 entity", RefKind.ENTITY, ReferenceResolver.ENTITY),
    ("人物主体", RefKind.ENTITY, ReferenceResolver.ENTITY),
    ("previz灰模视频", RefKind.VIDEO, ReferenceResolver.SHOT_VIDEO),
    ("3D预演视频", RefKind.VIDEO, ReferenceResolver.SHOT_VIDEO),
    ("上一镜末帧", RefKind.FIRST_FRAME, ReferenceResolver.PREV_SHOT_LASTFRAME),
    ("大地裂痕参考图", None, None),
    ("道家手印参考图", None, None),
    ("砌炉的老人声音", None, None),
    ("seedance 人物 entity", None, None),
    ("角色参考图2", None, None),
]


@pytest.mark.parametrize(("label", "kind", "resolver"), LABELS)
def test_default_rules_fr8_table(label: str, kind: RefKind | None, resolver: ReferenceResolver | None) -> None:
    route = DEFAULT.route("x", label)
    if kind is None:
        assert route is None
    else:
        assert route is not None and route.kind is kind and route.resolver is resolver and route.override is None


def test_first_matching_rule_wins() -> None:
    first = ReferenceRule("场景*", RefKind.IMAGE, ReferenceResolver.ASSET_FILE)
    second = ReferenceRule("场景参考图", RefKind.FIRST_FRAME, ReferenceResolver.PREV_SHOT_LASTFRAME)
    assert ReferenceRouting((first, second), {}).first_rule("场景参考图") is first


def test_override_beats_rules() -> None:
    routing = ReferenceRouting(
        DEFAULT_REFERENCE_RULES,
        {
            "砌炉的老人": ReferenceOverride.parse("砌炉的老人", "entity:hy3_主角"),
            "bg3-1": ReferenceOverride.parse("bg3-1", "ai_videos/x/bg3-1_远景.png"),
            "本镜首帧": ReferenceOverride.parse("本镜首帧", "ai_videos/x/shot01_lastframe.png"),
            "dilie": ReferenceOverride.parse("dilie", "ai_videos/x/dilie.mp4"),
        },
    )
    entity = routing.route("砌炉的老人", "Seedance 人物 entity")
    assert entity is not None and entity.kind is RefKind.ENTITY and entity.override and entity.override.entity_name == "hy3_主角"
    image = routing.route("bg3-1", "场景参考图")
    assert image is not None and image.kind is RefKind.IMAGE and image.resolver is None
    first_frame = routing.route("本镜首帧", "上一镜末帧")
    assert first_frame is not None and first_frame.kind is RefKind.FIRST_FRAME
    unmatched_label = routing.route("dilie", "大地裂痕参考图")
    assert unmatched_label is not None and unmatched_label.kind is RefKind.VIDEO


@pytest.mark.parametrize("value", ["entity:", "ai_videos/../projects/x.png", "C:/Windows/x.png", "ai_videos\\x.png", "x.png", "ai_videos//x.png", "ai_videos/a:b.png"])
def test_invalid_override_values(value: str) -> None:
    with pytest.raises(ConfigError) as err:
        ReferenceOverride.parse("砌炉的老人", value)
    assert err.value.field_path == 'references.overrides."砌炉的老人"'


@pytest.mark.parametrize(
    ("row", "field_path"),
    [
        ({"label_glob": "", "kind": "image", "resolver": "asset_file"}, "references.rules[0].label_glob"),
        ({"label_glob": "x", "kind": "gif", "resolver": "asset_file"}, "references.rules[0].kind"),
        ({"label_glob": "x", "kind": "image", "resolver": "unknown"}, "references.rules[0].resolver"),
        ({"label_glob": "x", "kind": "entity", "resolver": "shot_video"}, "references.rules[0].kind"),
        ({"label_glob": "x", "kind": "image", "resolver": "asset_file", "extra": 1}, "references.rules[0].extra"),
    ],
)
def test_invalid_rule_rows(row: dict[str, object], field_path: str) -> None:
    with pytest.raises(ConfigError) as err:
        ReferenceRule.from_table(ConfigTable.of(row, "references.rules[0]"))
    assert err.value.field_path == field_path


def test_rule_as_dict_roundtrip() -> None:
    for rule in DEFAULT_REFERENCE_RULES:
        assert ReferenceRule.from_table(ConfigTable.of(rule.as_dict(), "r")) == rule
