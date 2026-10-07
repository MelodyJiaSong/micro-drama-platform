from __future__ import annotations

import re

STORY_RUNS_FILE = "story_runs.json"
STORY_RUN_INPUT_FILE = "input.json"
STORY_INPUT_FILE = "shared/index.json"
STORY_INPUT_NODE_TYPE = "story_input"
STORY_INPUT_LABEL = "共享创作输入"
STORY_SELECTION_FILE = "story_selection.json"
STORY_PROFILE_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
STORY_PROMOTABLE_STATUSES = frozenset({"ready_for_review", "completed", "reviewed", "candidate_acceptable", "approved"})
STORY_RUNS_NODE_TYPE = "story_runs"
STORY_RUNS_LABEL = "创作记录"
STORY_RUN_VIEWS = {"output": "候选故事", "state": "候选状态变化", "input": "输入快照", "process": "创作过程"}
STORY_RUN_DOCUMENT_FILES = {"output": "story.md", "state": "state_changes.json", "input": STORY_RUN_INPUT_FILE, "process": "run.json"}
STORY_RUN_SCHEMA_VERSION = 1
STORY_FRAME_FIELDS = ("who", "what", "why", "when", "where", "how")
STORY_RUN_ID_RE = re.compile(r"story-run-[A-Za-z0-9][A-Za-z0-9_-]*")
STORY_RUN_PATH_RE = re.compile(r"\.audit/adhoc_agents/(\d{4}-\d{2}-\d{2})/(story-run-[A-Za-z0-9][A-Za-z0-9_-]*)/run\.json")
STORY_PROPOSAL_DECISIONS = frozenset({"accepted", "rejected", "partial", "deferred"})


class StoryRunsError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.status_code = status_code
