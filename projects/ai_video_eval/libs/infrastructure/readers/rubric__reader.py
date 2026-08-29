import hashlib
import os

import yaml

from libs.domain.errors.eval__error import RubricError


class RubricReader:
    def __init__(self, rubric_dir: str) -> None:
        self._rubric_dir = rubric_dir

    def read(self) -> tuple[dict, list[dict], str]:
        top_path = os.path.join(self._rubric_dir, "rubric.yaml")
        if not os.path.isfile(top_path):
            raise RubricError(f"rubric.yaml not found at {top_path}")
        hasher = hashlib.sha256()
        with open(top_path, "rb") as fh:
            top_bytes = fh.read()
        hasher.update(top_bytes)
        top = yaml.safe_load(top_bytes)

        dims: list[dict] = []
        dim_dir = os.path.join(self._rubric_dir, "dimensions")
        for dim_id in top.get("dimensions", []):
            path = os.path.join(dim_dir, f"{dim_id}.yaml")
            if not os.path.isfile(path):
                raise RubricError(f"dimension file missing: {path}")
            with open(path, "rb") as fh:
                raw = fh.read()
            hasher.update(raw)
            dims.append(yaml.safe_load(raw))
        return top, dims, hasher.hexdigest()
