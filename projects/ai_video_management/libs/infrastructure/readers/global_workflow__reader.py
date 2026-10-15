from __future__ import annotations

import hashlib
import json
import re
import tomllib
from dataclasses import asdict
from pathlib import Path
from typing import Any

from libs.common.config_redaction import redact_config, redact_text
from libs.common.global_workflow import CATALOG_PATH, GLOBAL_MAX_BYTES, source_identity
from libs.common.global_source_projection import project_defaults
from libs.common.global_source_references import source_references
from libs.infrastructure.daos.global_workflow__dao import GlobalSourceDao


class GlobalWorkflowReader:
    def __init__(self, repo_root: Path, user_root: Path | None = None) -> None:
        self.root = repo_root.resolve()
        self.user_root = (user_root or Path.home()).resolve()

    def _path(self, path: str, scope: str = "repo") -> Path:
        if not source_identity(path, scope):
            raise ValueError("invalid global source")
        base = self.user_root if scope == "user" else self.root
        candidate = base / path
        for parent in (candidate, *candidate.parents):
            if parent == base:
                break
            if parent.is_symlink() or getattr(parent, "is_junction", lambda: False)():
                raise ValueError("linked source refused")
        if candidate.resolve() != candidate or base not in candidate.resolve().parents:
            raise ValueError("source outside registered root")
        return candidate

    def _bytes(self, path: str, scope: str = "repo") -> bytes:
        candidate = self._path(path, scope)
        with candidate.open("rb") as stream:
            data = stream.read(GLOBAL_MAX_BYTES + 1)
        if len(data) > GLOBAL_MAX_BYTES:
            raise ValueError("source exceeds read limit")
        return data

    def catalog(self) -> tuple[list[dict[str, str]], list[GlobalSourceDao]]:
        data = json.loads(self._bytes(CATALOG_PATH).decode("utf-8-sig"))
        numbers = data.get("source_numbers", {})
        if not isinstance(numbers, dict) or any(not isinstance(number, str) or not re.fullmatch(r"[1-9]\d*\.(?:0|[1-9]\d*)(?:\.[1-9]\d*)+", number) for number in numbers.values()):
            raise ValueError("invalid global source numbers")
        if len(set(numbers.values())) != len(numbers):
            raise ValueError("duplicate global source numbers")
        records: dict[str, dict[str, str]] = {}
        for source in data["sources"]:
            records[f"{source.get('scope', 'repo')}:{source['path']}"] = source
        for discovery in data["discover"]:
            scope = discovery.get("scope", "repo")
            base = self.user_root if scope == "user" else self.root
            pattern = discovery["glob"]
            # Only canonical shared directories; never inspect private memory, auth or .env files.
            if ".." in pattern or pattern.startswith("/") or not source_identity(pattern, scope):
                raise ValueError("unsafe discovery")
            for path in sorted(base.glob(pattern)):
                relative = path.relative_to(base).as_posix()
                records.setdefault(f"{scope}:{relative}", {**discovery, "path": relative})
        entries = []
        for identity, source in records.items():
            path, scope = source["path"], source.get("scope", "repo")
            try:
                candidate = self._path(path, scope)
                status = "available" if candidate.is_file() else "missing"
            except (OSError, ValueError):
                status = "unavailable"
            title = source.get("title") or (path.split("/")[-2] if path.endswith("/SKILL.md") else path.split("/")[-1])
            historical = source.get("historical", False)
            formats = tuple(str(value) for value in source.get("formats", []))
            adapts = tuple({"source_id": f"{scope}:{entry['source']}", "section": str(entry.get("section", ""))} for entry in source.get("adapts", []))
            entries.append(GlobalSourceDao(identity, path, title, source["group"], scope, source.get("view", "document"), status, historical, numbers.get(identity, ""), f"{scope}:{source['parent']}" if source.get("parent") else "", formats, adapts))
        entries.sort(key=lambda entry: (not entry.number, tuple(int(part) for part in entry.number.split(".")) if entry.number else (), entry.path))
        return data["groups"], entries

    def categories(self) -> list[dict[str, str]]:
        return json.loads(self._bytes(CATALOG_PATH).decode("utf-8-sig")).get("categories", [])

    def formats(self) -> list[dict[str, str]]:
        return json.loads(self._bytes(CATALOG_PATH).decode("utf-8-sig")).get("formats", [])

    def source(self, identity: str) -> dict[str, Any]:
        _, entries = self.catalog()
        source = next((entry for entry in entries if entry.id == identity), None)
        if source is None:
            raise FileNotFoundError("unregistered global source")
        return self.read_source(source)

    def read_source(self, source: GlobalSourceDao) -> dict[str, Any]:
        if source.status != "available":
            return {**asdict(source), "content": "此配置未配置或不可读取。", "format": "text", "sha256": None}
        try:
            data = self._bytes(source.path, source.scope)
            text = data.decode("utf-8-sig")
            suffix = Path(source.path).suffix
            redacted = False
            if suffix in {".json", ".toml"}:
                value = json.loads(text) if suffix == ".json" else tomllib.loads(text)
                content = json.dumps(redact_config(value), ensure_ascii=False, indent=2)
                format_, redacted = "json", True
            elif source.view == "constants":
                content = json.dumps(project_defaults(text), ensure_ascii=False, indent=2, default=str)
                format_, redacted = "json", True
            else:
                content = redact_text(text)
                format_ = "markdown" if suffix == ".md" else "code"
                redacted = content != text
            return {**asdict(source), "status": "available", "content": content, "format": format_, "redacted": redacted,
                    "sha256": hashlib.sha256(data).hexdigest()}
        except (OSError, UnicodeError, ValueError, SyntaxError):
            return {**asdict(source), "status": "unavailable", "content": "无法安全解析此源文件，未展示原始配置。", "format": "text", "sha256": None}

    def inventory(self) -> dict[str, Any]:
        groups, entries = self.catalog()
        registered = {source.id for source in entries}
        issues = []
        references = []
        available = historical = 0
        for source in entries:
            detail = self.read_source(source)
            available += detail["status"] == "available"
            historical += bool(source.historical)
            if not source.number:
                issues.append({"source_id": source.id, "path": source.path, "kind": "unnumbered", "note": "待登记稳定编号"})
            if detail["status"] != "available":
                issues.append({"source_id": source.id, "path": source.path, "kind": detail["status"], "note": "未配置 / 不存在" if detail["status"] == "missing" else "无法安全解析"})
            if source.group not in {group["id"] for group in groups}:
                issues.append({"source_id": source.id, "path": source.path, "kind": "ungrouped", "note": "分类不存在，导航不可达"})
            if source.scope != "repo" or not source.path.endswith(".md") or detail["status"] != "available":
                continue
            for path in sorted(source_references(source.path, detail["content"])):
                if path.startswith("specs/") or (path.startswith("ai_videos/") and not path.startswith("ai_videos/_")):
                    continue  # Local facts and research evidence belong to drama/run navigation.
                identity = source_identity(path)
                if identity in registered:
                    continue
                try:
                    # Existing literal references only; placeholders and old deleted artifacts are not settings.
                    if not self._path(path).is_file():
                        continue
                except (OSError, ValueError):
                    continue
                references.append({"source_id": source.id, "path": path, "historical": source.historical})
        return {"total": len(entries), "available": available, "historical": historical,
                "numbered": sum(bool(source.number) for source in entries), "issues": issues, "references": references}
