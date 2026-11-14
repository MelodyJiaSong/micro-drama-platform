from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode


class SharedLibraryTreeReader:
    def read(self, library: Path, rel: str) -> list[dict[str, Any]]:
        data = json.loads((library / "library.json").read_text(encoding="utf-8"))
        assets = {asset["id"]: asset for asset in data.get("assets", [])}
        children: list[dict[str, Any]] = []
        for group in data.get("navigation", []):
            group_node = self._folder(rel, group["id"], group["name"], {"group": group["id"]})
            for subgroup in group["children"]:
                params = {"group": group["id"], "sub": subgroup["id"]}
                sub_node = self._folder(rel, f"{group['id']}/{subgroup['id']}", subgroup["name"], params)
                for asset_id in subgroup["asset_ids"]:
                    asset = assets[asset_id]
                    sub_node["children"].append({
                        "type": "directory", "name": asset_id, "display_name": asset["name"],
                        "path": f"{rel}/_catalog/{group['id']}/{subgroup['id']}/{asset_id}",
                        "navigation_href": self._href(rel, {**params, "open": asset_id}), "children": [],
                    })
                group_node["children"].append(sub_node)
            children.append(group_node)
        documents = self._folder(rel, "documents", "设定与研究资料", {})
        documents.pop("navigation_href")
        for path, label in [
            ("systems.md", "升级与品阶"), ("appendix.md", "术语与采用手册"),
            ("research/report.md", "深度研究"), ("visual_guide.md", "视觉规范"),
            ("STATUS.md", "图片完成与验收状态"), ("README.md", "资产库说明"),
        ]:
            if (library / path).is_file():
                documents["children"].append({"type": "file", "name": path, "display_name": label, "path": f"{rel}/{path}"})
        if documents["children"]:
            children.append(documents)
        return children

    @staticmethod
    def _href(rel: str, params: dict[str, str]) -> str:
        return "/assets?" + urlencode({"library": rel, **params})

    def _folder(self, rel: str, key: str, label: str, params: dict[str, str]) -> dict[str, Any]:
        return {"type": "directory", "name": key, "display_name": label, "path": f"{rel}/_catalog/{key}",
                "navigation_href": self._href(rel, params), "children": []}
