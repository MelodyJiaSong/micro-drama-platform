import pytest

from libs.domain.errors.config__error import ConfigError, MissingAbbrevError
from libs.domain.value_objects.entity_naming__valueobject import DEFAULT_NAME_TEMPLATE, EntityNaming

HY3 = EntityNaming(abbrev="hy3", name_template=DEFAULT_NAME_TEMPLATE, overrides={})


@pytest.mark.parametrize(
    ("card_dir", "expected"),
    [("c1_砌炉的老人", "hy3_砌炉的老人"), ("c12_围观武者乙", "hy3_围观武者乙"), ("driver", "hy3_driver"), ("裴知秋", "hy3_裴知秋"), ("c1_", "hy3_c1_")],
)
def test_template_strips_card_prefix(card_dir: str, expected: str) -> None:
    assert HY3.entity_name(card_dir) == expected


def test_override_wins() -> None:
    naming = EntityNaming("hy3", DEFAULT_NAME_TEMPLATE, {"c1_砌炉的老人": "hy3_主角"})
    assert naming.entity_name("c1_砌炉的老人") == "hy3_主角" and naming.entity_name("c2_獾") == "hy3_獾"


def test_standalone_without_abbrev() -> None:
    naming = EntityNaming("", DEFAULT_NAME_TEMPLATE, {"c4_裴昭": "wj_裴昭"})
    assert naming.entity_name("c4_裴昭") == "wj_裴昭"
    with pytest.raises(MissingAbbrevError) as err:
        naming.entity_name("c5_裴知秋")
    assert err.value.field_path == "drama.abbrev"
    assert EntityNaming("", "{character_name}", {}).entity_name("c5_裴知秋") == "裴知秋"


def test_linked_card_follows_source_config() -> None:
    hy1 = EntityNaming("hy1", DEFAULT_NAME_TEMPLATE, {"c1_造家的人": "hy1_主角"})
    assert EntityNaming.for_linked_card(hy1, "hy1", DEFAULT_NAME_TEMPLATE).entity_name("c1_造家的人") == "hy1_主角"


def test_linked_card_without_source_config_uses_source_dir_as_abbrev() -> None:
    naming = EntityNaming.for_linked_card(None, "hy1", DEFAULT_NAME_TEMPLATE)
    assert naming.entity_name("c1_造家的人") == "hy1_造家的人"


@pytest.mark.parametrize("template", ["", "{abbrev}_{unknown}", "{abbrev}", "{abbrev}_{character_name!r}", "{abbrev}_{character_name:>5}", "{abbrev_{character_name}"])
def test_invalid_templates(template: str) -> None:
    with pytest.raises(ConfigError) as err:
        EntityNaming("hy3", template, {})
    assert err.value.field_path == "entities.name_template"
