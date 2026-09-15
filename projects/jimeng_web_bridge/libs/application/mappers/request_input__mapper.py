from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from libs.application.dtos.batch__dto import (
    AssetItemInput,
    BatchItemInput,
    EntityCreateItemInput,
    RawItemInput,
    ShotItemInput,
)


class RequestInputMapper:
    """Batch item inputs ↔ canonical dicts: the idempotency body, and what `reprecheck` replays."""

    def to_dict(self, item: BatchItemInput) -> dict[str, object]:
        if isinstance(item, ShotItemInput):
            return {"type": "shot", "shot_path": item.shot_path, "reroll": item.reroll}
        if isinstance(item, AssetItemInput):
            return {"type": "asset", "card_path": item.card_path, "key": item.key, "reroll": item.reroll}
        if isinstance(item, RawItemInput):
            return {
                "type": "raw",
                "kind": item.kind,
                "prompt": item.prompt,
                "reference_paths": list(item.reference_paths),
                "entity_names": list(item.entity_names),
                "params": dict(item.params),
                "output_dir": item.output_dir,
                "negative_prompt": item.negative_prompt,
                "reroll": item.reroll,
            }
        return {
            "type": "entity_create",
            "drama_rel": item.drama_rel,
            "character_dir": item.character_dir,
            "description": item.description,
        }

    def from_dict(self, data: Mapping[str, Any]) -> BatchItemInput:
        kind: str = data["type"]
        if kind == "shot":
            return ShotItemInput(shot_path=data["shot_path"], reroll=data["reroll"])
        if kind == "asset":
            return AssetItemInput(card_path=data["card_path"], key=data["key"], reroll=data["reroll"])
        if kind == "raw":
            return RawItemInput(
                kind=data["kind"],
                prompt=data["prompt"],
                reference_paths=tuple(data["reference_paths"]),
                entity_names=tuple(data["entity_names"]),
                params=dict(data["params"]),
                output_dir=data["output_dir"],
                negative_prompt=data["negative_prompt"],
                reroll=data["reroll"],
            )
        return EntityCreateItemInput(
            drama_rel=data["drama_rel"], character_dir=data["character_dir"], description=data["description"]
        )
