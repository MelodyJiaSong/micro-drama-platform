from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class InitialFact(StrictModel):
    id: str
    text: str
    known_by: list[str]


class StoryBible(StrictModel):
    title: str
    genre: str
    language: str
    theme: str
    tone: str
    world_rules: list[str]
    hard_constraints: list[str]
    threads: list[str]
    initial_facts: list[InitialFact]


class BehavioralRule(StrictModel):
    trigger: str
    conditions: str
    appraisal: str
    preferred_action: str
    speech_strategy: str
    exceptions: str


class CharacterBible(StrictModel):
    id: str
    name: str
    core_identity: dict[str, str]
    psychology: dict[str, str]
    cognition: dict[str, str]
    speech: dict[str, str]
    forbidden_speech_patterns: list[str]
    behavioral_rules: list[BehavioralRule]
    goals: dict[str, str]
    relationships: dict[str, str]
    growth_range: str
    examples: list[str]
    counterexamples: list[str]
    unknowns: list[str]


class SceneSpec(StrictModel):
    id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    episode: str = Field(pattern=r"^ep[0-9]+$")
    brief: str
    participants: list[str]
    location: str
    story_time: str
    tags: list[str]
    target_seconds: int = Field(ge=15, le=1800)


class StorySeed(StrictModel):
    slug: str = Field(pattern=r"^[a-z0-9_]+$")
    premise: str = Field(min_length=10, max_length=20000)
    characters: list[dict[str, str]] = Field(min_length=1, max_length=20)
    scenes: list[SceneSpec] = Field(min_length=1, max_length=100)


class SceneBrief(StrictModel):
    objective: str
    conflict: str
    character_goals: dict[str, str]
    constraints: list[str]
    turn: str
    creative_intent: str


class Line(StrictModel):
    id: str
    speaker: str
    text: str
    translation: str
    uses_knowledge: list[str]


class MemoryEvent(StrictModel):
    id: str
    kind: Literal["fact", "knowledge", "relationship", "physical", "thread", "foreshadowing"]
    actor: str
    target: str
    proposition_id: str
    value: str
    epistemic_status: Literal["known", "believed", "suspected", "misbelieved", "unknown"]
    source_event_id: str
    evidence_quote: str
    relationship_changes: dict[str, int]


class Beat(StrictModel):
    id: str
    action: str
    lines: list[Line]
    duration_s: int = Field(ge=1, le=1800)
    events: list[MemoryEvent]


class SceneDraft(StrictModel):
    title: str
    beats: list[Beat] = Field(min_length=1, max_length=25)


class Finding(StrictModel):
    id: str
    severity: Literal["blocker", "high", "medium", "low"]
    dimension: str
    locator: str
    quote: str
    reason: str
    evidence_refs: list[str]
    repair_hint: str


class Review(StrictModel):
    findings: list[Finding]
    summary: str


class Opportunity(StrictModel):
    id: str
    locator: str
    suggestion: str
    intended_effect: str
    character_basis: str
    priority: int = Field(ge=1, le=10)
    risks: str


class EditorReview(StrictModel):
    opportunities: list[Opportunity] = Field(max_length=3)
    summary: str


class CreativeDecision(StrictModel):
    accepted: list[str]
    rejected: list[str]
    reasons: dict[str, str]


class RewritePlan(StrictModel):
    rewrite_required: bool
    instructions: list[str]
    adopted_opportunities: list[str]
    rejected_opportunities: list[str]
    reasons: dict[str, str]


class QualityReview(Review):
    grades: dict[str, int]
    confidence: Literal["high", "medium", "low"]


class Simulation(StrictModel):
    perceived_situation: str
    interpretation: str
    immediate_goal: str
    likely_action: str
    likely_speech: str
    alternative: str


class EpisodeReview(Review):
    audience_understanding: str
    relationship_progression: str
    ending_hook: str
