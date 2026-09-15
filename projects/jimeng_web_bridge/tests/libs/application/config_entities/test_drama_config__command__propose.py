from __future__ import annotations

import tomlkit

from libs.application.dtos.drama_config__dto import NeedsConfirmationQdto, ProposeCdto
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from tests.libs.application.config_entities.support import FLAT, HY1, HY2, HY3, Harness, config_text, sha256_of


def _confirmation(result: ProposeCdto, key: str) -> NeedsConfirmationQdto:
    matches = [item for item in result.needs_confirmation if item.key == key]
    assert len(matches) == 1, [item.key for item in result.needs_confirmation]
    return matches[0]


def _codes(result: ProposeCdto) -> list[str]:
    return [item.code for item in result.needs_confirmation]


def test_propose_hy3_flags_a_possible_existing_entity_and_writes_nothing(harness: Harness) -> None:
    harness.sync("hy3_主角", "hy1_造家的人")
    result = harness.config_command.propose("huangye_shenghuo/hy3")
    assert (result.exists, result.diff, result.current_sha256) == (False, (), None)
    assert result.proposed_data["drama"] == {"abbrev": "hy3"}
    assert {entity.character_dir: entity.entity_name for entity in result.entities} == {
        "c1_砌炉的老人": "hy3_砌炉的老人",
        "c2_獾": "hy3_獾",
    }
    item = _confirmation(result, 'entities.overrides."c1_砌炉的老人"')
    assert item.code == "entity_name_conflict"
    assert item.config_key == 'entities.overrides."c1_砌炉的老人"'
    assert "可能已有同一角色的主体，名称不同，例如 hy3_主角" in item.reason
    assert '"hy3_主角"' in (item.suggestion or "")
    assert "drama_abbrev_missing" not in _codes(result) and "entities_never_synced" not in _codes(result)
    assert not harness.config_path(HY3).exists()


def test_proposed_toml_round_trips_to_the_proposed_data(harness: Harness) -> None:
    result = harness.config_command.propose(HY3)
    parsed = tomlkit.parse(result.proposed_toml).unwrap()
    assert parsed == result.proposed_data
    DramaConfig.from_dict(parsed, harness.configs.model_limits())


def test_propose_without_any_sync_asks_to_sync_first(harness: Harness) -> None:
    result = harness.config_command.propose(HY3)
    item = _confirmation(result, "entities.sync")
    assert (item.code, item.config_key) == ("entities_never_synced", None)
    assert "entity_name_conflict" not in _codes(result)
    assert all(entity.in_snapshot is None for entity in result.entities)


def test_propose_flat_drama_without_abbrev_needs_confirmation(harness: Harness) -> None:
    harness.sync("hy3_主角")
    result = harness.config_command.propose("solo_drama")
    assert result.proposed_data["drama"] == {"abbrev": ""}
    assert result.needs_confirmation[0].key == "drama.abbrev"
    assert result.needs_confirmation[0].code == "drama_abbrev_missing"
    card = result.entities[0]
    assert (card.character_dir, card.entity_name, card.error_code, card.config_key) == (
        "c1_独行者", None, "drama_abbrev_missing", "drama.abbrev",
    )
    assert not harness.config_path(FLAT).exists()


def test_propose_flat_drama_reference_failures_suggest_override_keys(harness: Harness) -> None:
    harness.sync("x")
    result = harness.config_command.propose(FLAT)
    by_key = {item.key: item for item in result.needs_confirmation}
    assert by_key['references.overrides."缺失图"'].code == "reference_not_found"
    assert by_key['references.overrides."双胞胎"'].code == "ambiguous_reference"
    assert f"{FLAT}/props/p1_甲/双胞胎.png" in (by_key['references.overrides."双胞胎"'].suggestion or "")
    assert by_key['references.overrides."某物"'].code == "reference_label_unmatched"
    assert by_key['references.overrides."缺失图"'].shots == ("shot01",)
    assert all(item.code != "legacy_reference_syntax" for item in result.needs_confirmation)


def test_propose_hy2_linked_card_follows_the_source_episode(harness: Harness) -> None:
    harness.sync("hy1_主角")
    result = harness.config_command.propose(HY2)
    card = next(entity for entity in result.entities if entity.character_dir == "c1_造家的人")
    assert (card.entity_name, card.source_drama_rel, card.naming_abbrev) == ("hy1_造家的人", HY1, "hy1")
    item = _confirmation(result, 'entities.overrides."c1_造家的人"')
    assert item.code == "entity_name_conflict" and "hy1_主角" in item.reason
    assert "hy2_造家的人" not in {entity.entity_name for entity in result.entities}


def test_propose_linked_card_uses_the_source_config_overrides(harness: Harness) -> None:
    harness.write_config(HY1, config_text(harness.mapper, "hy1", {"c1_造家的人": "hy1_主角"}))
    harness.sync("hy1_主角")
    result = harness.config_command.propose(HY2)
    card = next(entity for entity in result.entities if entity.character_dir == "c1_造家的人")
    assert (card.entity_name, card.in_snapshot) == ("hy1_主角", True)
    assert 'entities.overrides."c1_造家的人"' not in {item.key for item in result.needs_confirmation}


def test_propose_existing_config_returns_diff_and_leaves_the_file_untouched(harness: Harness) -> None:
    text = config_text(harness.mapper, overrides={"c1_砌炉的老人": "hy3_主角"}).replace(
        'search_exclude = ["_deleted", "_candidates", "renders", "frames", "_blender"]', 'search_exclude = ["_deleted"]'
    )
    path = harness.write_config(HY3, text)
    before, mtime = path.read_bytes(), path.stat().st_mtime_ns
    harness.sync("hy3_主角")
    result = harness.config_command.propose(HY3)
    assert result.exists and result.current_sha256 == sha256_of(path)
    assert [(item.key, item.change, item.current) for item in result.diff] == [
        ("references.search_exclude", "changed", ["_deleted"]),
    ]
    assert result.proposed_data["entities"]["overrides"] == {"c1_砌炉的老人": "hy3_主角"}
    assert path.read_bytes() == before and path.stat().st_mtime_ns == mtime


def test_proposal_can_be_saved_as_is(harness: Harness) -> None:
    result = harness.config_command.propose(HY3)
    saved = harness.config_command.save(HY3, None, result.proposed_toml, None)
    path = harness.config_path(HY3)
    assert path.read_text(encoding="utf-8") == result.proposed_toml
    assert saved.sha256 == sha256_of(path) and saved.location == f"{HY3}/jimeng_config.toml"
    assert harness.configs.get(HY3).validation_error is None
