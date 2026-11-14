"""商店货单（follow-up 316）：读剧的 `2_世界观人设/props/shop_items.json`。只读。

结构：`sellers[]`（`key,name_zh,name_en,kind,where,card,count,items[]`），物品 `prop_key,name_zh,name_en,
category,price,recipe,card,image`；`card` / `image` 相对 `2_世界观人设/`（旧剧平铺在剧根）。这里把路径换成
仓库相对路径，跑出剧目录、经过链接或文件不在的置空串，图片经 `/api/media` 显示。顶层 `items` 反查表不读：
「谁卖它」由 query 从各出售方的货单算，两边不会对不上。剧没有货单返回空 `source`，不报错。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.common import drama_layout, drama_ref
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.drama__error import DramaNotFoundError, InvalidDramaPathError
from libs.infrastructure.daos.shop_items__dao import ShopItemDao, ShopItemsDao, ShopSellerDao

SHOP_ITEMS_FILE = "shop_items.json"
SHOP_ITEMS_DOC = "shop_items.md"
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")
MAX_BYTES = 2_000_000


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return ""


class ShopItemsReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.resolver = SafeResolver(repo_root)

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def drama_dir(self, rel: str) -> tuple[Path, str]:
        """(剧目录, 规范化的仓库相对路径)；不是剧根抛 InvalidDramaPathError，不在盘上抛 DramaNotFoundError。"""
        norm = rel.strip().replace("\\", "/").strip("/")
        parts = norm.split("/")
        if not norm or drama_ref.drama_depth(self.root, parts) != len(parts):
            raise InvalidDramaPathError(f"不是剧目录：{rel}")
        resolved = self.resolver.resolve(norm)
        if resolved is None:
            raise InvalidDramaPathError(f"不是剧目录：{rel}")
        if not resolved.is_dir():
            raise DramaNotFoundError(f"剧目录不存在：{rel}")
        return resolved, norm

    def read(self, rel: str) -> tuple[str, ShopItemsDao]:
        """(剧路径, 货单)。"""
        drama, norm = self.drama_dir(rel)
        props = drama_layout.props_dir(drama)
        source = props / SHOP_ITEMS_FILE
        if not source.is_file() or source.is_symlink():
            return norm, ShopItemsDao("", "", "", "")
        doc = props / SHOP_ITEMS_DOC
        doc_rel = self._rel(doc) if doc.is_file() and not doc.is_symlink() else ""
        try:
            if source.stat().st_size > MAX_BYTES:
                raise ValueError("文件过大")
            data = json.loads(source.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("sellers"), list):
                raise ValueError("缺少 sellers 列表")
        except (OSError, ValueError) as exc:
            return norm, ShopItemsDao(self._rel(source), doc_rel, "", "", [], f"读不了 {SHOP_ITEMS_FILE}：{exc}")
        base = props.parent
        sellers = [self._seller(s, base, drama) for s in data["sellers"] if isinstance(s, dict) and _text(s.get("key"))]
        return norm, ShopItemsDao(self._rel(source), doc_rel, _text(data.get("version")), _text(data.get("note")), sellers)

    @staticmethod
    def _inside(base: Path, drama: Path, rel: Any) -> Path | None:
        """`2_世界观人设/` 下的相对路径 → 绝对路径；绝对路径、`..`、跑出剧目录、经过链接一律 None。"""
        text = _text(rel).replace("\\", "/")
        if not text or text.startswith("/") or ":" in text:
            return None
        parts = text.split("/")
        if any(p in {"", ".", ".."} for p in parts):
            return None
        path = base.joinpath(*parts)
        if drama not in path.parents:
            return None
        if any(p.is_symlink() for p in [path, *path.parents] if drama in p.parents):
            return None
        return path

    def _file(self, base: Path, drama: Path, rel: Any) -> str:
        path = self._inside(base, drama, rel)
        return self._rel(path) if path is not None and path.is_file() else ""

    def _seller(self, raw: dict[str, Any], base: Path, drama: Path) -> ShopSellerDao:
        folder = self._inside(base, drama, raw.get("card"))
        folder_rel = card = image = ""
        if folder is not None and folder.is_dir():
            folder_rel = self._rel(folder)
            md = folder / f"{folder.name}.md"
            card = self._rel(md) if md.is_file() else ""
            image = next((self._rel(folder / f"{folder.name}{ext}") for ext in IMAGE_EXTS
                          if (folder / f"{folder.name}{ext}").is_file()), "")
        elif folder is not None and folder.is_file():   # card 直接写成 .md 也认
            card = self._rel(folder)
        items = [ShopItemDao(_text(i.get("prop_key")), _text(i.get("name_zh")), _text(i.get("name_en")),
                             _text(i.get("category")), _text(i.get("price")), _text(i.get("recipe")),
                             self._file(base, drama, i.get("card")), self._file(base, drama, i.get("image")))
                 for i in raw.get("items") or [] if isinstance(i, dict) and _text(i.get("prop_key"))]
        count = raw.get("count")
        return ShopSellerDao(_text(raw.get("key")), _text(raw.get("name_zh")), _text(raw.get("name_en")),
                             _text(raw.get("kind")), _text(raw.get("where")), folder_rel, card, image,
                             count if isinstance(count, int) and not isinstance(count, bool) else len(items), items)
