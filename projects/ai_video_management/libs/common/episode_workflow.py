from __future__ import annotations

import hashlib
import json
from typing import Any

WORKFLOW_ID = "three-module-v1"
WORKFLOW_MARKER = "workflow.json"
MODULES = ("story", "filming", "prompts")
MODULE_LABELS = {"story": "故事创作", "filming": "影视改编", "prompts": "Prompt 编译"}
MODULE_NAV_LABELS = {"story": "2_故事", "filming": "3_影视改编", "prompts": "4_prompt编译"}
WORLD_FACTS_FILE = "world_rules.md"
STATE_CHANGES_FILE = "state_changes.md"
COMPILER_VERSION = 3
VIDEO_SOUND_RULE = "声音：仅保留本镜指定对白、自然环境声和动作声；不要背景音乐或配乐。"
SILENT_SHOT_RULE = "本镜没有人说话。"


def fingerprint(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def empty_document(module: str) -> dict[str, Any]:
    content = {"brief": "", "text": ""} if module == "story" else {"scenes": []}
    return {"content": content, "source_revision": None, "approved_revision": None}
