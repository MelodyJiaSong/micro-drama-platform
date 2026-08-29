# Revised prompt — ai_video_eval

Task: `ai_video_eval` · task_type: `development` · Run: `ai_video_eval-20260728-194012` · Source: `raw_prompt.md` (2026-07-28)

## Goal

Build a comprehensive evaluation (eval) system that evaluates the episode and shot-prompt artifacts generated in the `ai_videos/` projects of this repo, and produces eval verdicts plus actionable insights that an AI-video generation agent can later consume to revise its artifacts.

## Context

- The artifacts under evaluation are the outputs of the existing AI 短剧 pipeline (episode scripts/dialogue, shot files with standardized 视频/台词配音 prompts, and related planning artifacts under `ai_videos/{name}/`).
- The system must be **100% independent**: it must not be affected by any existing Claude settings (skills, agent_refs, CLAUDE.md conventions, hooks) or any other existing configuration. *(Exact boundary of "independent" to be clarified in the interview.)*

## Known required stages (user-named examples; not exhaustive)

1. **Rubric definition** — a comprehensive, powerful, deterministic rubric:
   - Covers many dimensions (user examples: groundedness, consistency, faithfulness, etc.).
   - Each dimension has multiple layers of sub-categories and fields.
   - Each field should elicit a *graded/subjective* judgment (rich signal) rather than forcing the judging agent into a binary 0/1 decision.
2. **Result aggregation layer** — non-LLM-based, 100% deterministic aggregation of the per-field judgments into verdicts.

The user explicitly notes there are many other important stages beyond these two examples; the full stage list is to be established during interview/research.

## Desired outcome

- Eval verdicts + insights in a form consumable by the AI-video generation agent for artifact revision (feedback loop).
- First step requested by the user: a requirements-clarification interview from multiple angles, with **no fewer than 50 questions**.

## Explicit constraints

- 100% independence from existing Claude/harness settings.
- Deterministic rubric; deterministic (non-LLM) aggregation.
- Multi-dimensional, multi-layer rubric with graded (non-binary) field outputs.
