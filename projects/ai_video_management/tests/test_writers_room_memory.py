"""Independent story-memory invariants; no model or network calls."""
from __future__ import annotations

from copy import deepcopy
import json

import pytest

from libs.domain.entities.story_memory__entity import StoryMemoryEntity
from libs.domain.errors.writers_room__error import WritersRoomError
from libs.infrastructure.daos.writers_room__dao import SceneDraft


SECRET = "The captain is the masked murderer."
FALSE_BELIEF = "The captain was asleep during the murder."


def event(event_id="scene1_fact", kind="fact", **overrides):
    result = {
        "id": event_id, "kind": kind, "actor": "a", "target": "",
        "proposition_id": "identity", "value": SECRET,
        "epistemic_status": "known", "source_event_id": "",
        "evidence_quote": "He removes the mask.", "relationship_changes": {},
    }
    return {**result, **overrides}


def line(line_id="line1", speaker="a", uses=None):
    return {
        "id": line_id, "speaker": speaker, "text": "I know who he is.",
        "translation": "", "uses_knowledge": uses or [],
    }


def beat(beat_id="beat1", action="He removes the mask.", lines=None, events=None):
    return {
        "id": beat_id, "action": action, "lines": lines or [],
        "duration_s": 4, "events": events or [],
    }


def draft(*beats):
    result = {"title": "Masked captain", "beats": list(beats)}
    # Validate fixtures through the same external scene contract.
    SceneDraft.model_validate(result)
    return result


def dimensions(findings):
    return {finding["dimension"] for finding in findings}


def test_unknown_speaker_cannot_use_world_truth():
    memory = StoryMemoryEntity(facts={"identity": SECRET})
    projected, findings = memory.project(
        "scene1", draft(beat(lines=[line(uses=["identity"])])), ["a", "b"],
    )
    assert "knowledge_consistency" in dimensions(findings)
    assert not projected.accepted_scenes


def test_knowledge_is_usable_only_after_acquisition():
    memory = StoryMemoryEntity()
    projected, findings = memory.project("scene1", draft(
        beat(events=[event(), event("scene1_know", "knowledge", source_event_id="scene1_fact")]),
        beat("beat2", lines=[line(uses=["identity"])]),
    ), ["a", "b"])
    assert findings == []
    assert projected.character_view("a")["knowledge"]["identity"]["text"] == SECRET


def test_future_acquisition_cannot_authorize_previous_line():
    _, findings = StoryMemoryEntity().project("scene1", draft(
        beat(lines=[line(uses=["identity"])]),
        beat("beat2", events=[event(), event("scene1_know", "knowledge", source_event_id="scene1_fact")]),
    ), ["a", "b"])
    assert "knowledge_consistency" in dimensions(findings)


def test_future_source_event_is_rejected():
    projected, findings = StoryMemoryEntity().project("scene1", draft(beat(events=[
        event("scene1_know", "knowledge", source_event_id="scene1_fact"), event(),
    ])), ["a", "b"])
    assert "knowledge_consistency" in dimensions(findings)
    assert "identity" not in projected.knowledge.get("a", {})


def test_source_proposition_mismatch_is_rejected():
    projected, findings = StoryMemoryEntity().project("scene1", draft(beat(events=[
        event(), event("scene1_know", "knowledge", proposition_id="other", source_event_id="scene1_fact"),
    ])), ["a", "b"])
    assert "knowledge_consistency" in dimensions(findings)
    assert "other" not in projected.knowledge.get("a", {})


@pytest.mark.parametrize("status", ["believed", "suspected", "misbelieved", "unknown"])
def test_unconfirmed_knowledge_view_does_not_reveal_author_truth(status):
    memory = StoryMemoryEntity(
        facts={"identity": SECRET}, knowledge={"a": {"identity": {
            "status": status, "text": FALSE_BELIEF, "source_event_id": "prior_belief",
        }}},
        events=[event("prior_belief", "knowledge", value=FALSE_BELIEF,
                      epistemic_status=status, scene_id="prior", beat_id="prior_beat", order=0)],
    )
    view = memory.character_view("a")
    assert SECRET not in json.dumps(view), "Author truth leaked through a non-known proposition"
    if status != "unknown":
        assert FALSE_BELIEF in json.dumps(view), "Character must retain their own belief content"


def test_false_belief_event_cannot_promote_to_true_knowledge():
    memory = StoryMemoryEntity(
        facts={"identity": SECRET}, knowledge={"b": {"identity": {
            "status": "misbelieved", "text": FALSE_BELIEF, "source_event_id": "prior_claim",
        }}},
        events=[event("prior_claim", "knowledge", actor="b", value=FALSE_BELIEF,
                      epistemic_status="misbelieved", scene_id="prior", beat_id="prior_beat", order=0)],
    )
    _, findings = memory.project("scene1", draft(beat(events=[
        event("scene1_know", "knowledge", value=FALSE_BELIEF,
              source_event_id="prior_claim", epistemic_status="known"),
    ])), ["a", "b"])
    assert "knowledge_consistency" in dimensions(findings)


def test_claiming_true_value_cannot_launder_false_source_into_knowledge():
    memory = StoryMemoryEntity(
        facts={"identity": SECRET},
        events=[event("prior_claim", "knowledge", actor="b", value=FALSE_BELIEF,
                      epistemic_status="misbelieved", scene_id="prior", beat_id="prior_beat", order=0)],
    )
    _, findings = memory.project("scene1", draft(beat(events=[
        event("scene1_know", "knowledge", value=SECRET,
              source_event_id="prior_claim", epistemic_status="known"),
    ])), ["a", "b"])
    assert "knowledge_consistency" in dimensions(findings), "An accurate fact value alone is not a valid acquisition source"


def test_non_knowledge_state_event_cannot_authorize_secret_acquisition():
    memory = StoryMemoryEntity(facts={"identity": SECRET}, events=[
        event("prior_relation", "relationship", actor="b", target="a",
              value=SECRET, epistemic_status="known", relationship_changes={"trust": 1}),
    ])
    _, findings = memory.project("scene1", draft(beat(events=[
        event("scene1_know", "knowledge", source_event_id="prior_relation"),
    ])), ["a", "b"])
    assert "knowledge_consistency" in dimensions(findings), "A relationship event does not establish knowledge even if it has irrelevant fact-shaped fields"


def test_relationship_update_is_directional():
    memory = StoryMemoryEntity()
    projected, findings = memory.project("scene1", draft(beat(events=[
        event("scene1_relation", "relationship", target="b", relationship_changes={"trust": 1}),
    ])), ["a", "b"])
    assert findings == []
    assert projected.relationships["a->b"]["trust"] == 1
    assert "b->a" not in projected.relationships
    assert projected.character_view("b")["relationships"] == {}


@pytest.mark.parametrize("changes", [{"trust": 2}, {"invented_dimension": 1}])
def test_relationship_change_requires_valid_dimension_and_bounded_delta(changes):
    projected, findings = StoryMemoryEntity().project("scene1", draft(beat(events=[
        event("scene1_relation", "relationship", target="b", relationship_changes=changes),
    ])), ["a", "b"])
    assert "relationship_consistency" in dimensions(findings)
    assert projected.relationships == {}


def test_candidate_projection_does_not_mutate_accepted_memory():
    memory = StoryMemoryEntity()
    before = deepcopy(memory)
    projected, findings = memory.project("scene1", draft(beat(events=[event()])), ["a", "b"])
    assert findings == [] and projected.facts["identity"] == SECRET
    assert memory == before, "Generating a candidate must never advance accepted memory"


def test_event_requires_exact_current_beat_evidence():
    projected, findings = StoryMemoryEntity().project("scene1", draft(
        beat(action="He removes the mask."),
        beat("beat2", action="They leave.", events=[event()]),
    ), ["a", "b"])
    assert "grounding" in dimensions(findings)
    assert projected.facts == {}
    assert projected.events == []


def test_original_evidence_and_provenance_survive_projection():
    projected, findings = StoryMemoryEntity().project("scene1", draft(beat(events=[event()])), ["a", "b"])
    assert findings == []
    recorded = projected.events[0]
    assert recorded["evidence_quote"] == "He removes the mask."
    assert recorded["scene_id"] == "scene1"
    assert recorded["beat_id"] == "beat1"
    assert recorded["order"] == 0


def test_duplicate_event_cannot_apply_twice():
    projected, findings = StoryMemoryEntity().project("scene1", draft(beat(events=[
        event("scene1_relation", "relationship", target="b", relationship_changes={"trust": 1}),
        event("scene1_relation", "relationship", target="b", relationship_changes={"trust": 1}),
    ])), ["a", "b"])
    assert "timeline" in dimensions(findings)
    assert projected.relationships["a->b"]["trust"] == 1
    assert not projected.accepted_scenes


def test_duplicate_accepted_scene_is_rejected():
    memory = StoryMemoryEntity(accepted_scenes=["scene1"])
    with pytest.raises(WritersRoomError) as error:
        memory.project("scene1", draft(beat()), ["a", "b"])
    assert error.value.kind == "scene_already_accepted"


def test_duplicate_locators_are_blockers():
    _, findings = StoryMemoryEntity().project("scene1", draft(
        beat(lines=[line("same"), line("same")]),
    ), ["a", "b"])
    assert "identity" in dimensions(findings)


def test_existing_fact_cannot_be_rewritten_by_candidate():
    projected, findings = StoryMemoryEntity(facts={"identity": SECRET}).project("scene1", draft(beat(events=[
        event(value="The captain is innocent."),
    ])), ["a", "b"])
    assert "plot_logic" in dimensions(findings)
    assert projected.facts["identity"] == SECRET


@pytest.mark.parametrize("kind", ["knowledge", "physical", "relationship"])
def test_personal_state_event_requires_real_actor(kind):
    memory = StoryMemoryEntity(facts={"identity": SECRET}, events=[event("prior_fact")])
    projected, findings = memory.project("scene1", draft(beat(events=[
        event("scene1_personal", kind, actor="", target="b",
              source_event_id="prior_fact", relationship_changes={"trust": 1} if kind == "relationship" else {}),
    ])), ["a", "b"])
    assert findings, "Personal state cannot belong to an empty character ID"
    assert not projected.accepted_scenes
