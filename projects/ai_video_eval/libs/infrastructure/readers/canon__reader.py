import os
import re

from libs.infrastructure.daos.canon__dao import CanonBundleDao, CharacterCardDao, SceneCardDao

_LOCKED_TAG_ROW = re.compile(r"^\|\s*\d+\w*\s*\|[^|]*角色识别标签[^|]*\|\s*(.+?)\s*\|", re.MULTILINE)
_VOICE_ID = re.compile(r"voice_id[:：]?\s*`?([A-Za-z0-9_\-]+)`?")


class CanonReader:
    def read(self, canon_dir: str | None) -> CanonBundleDao:
        if canon_dir is None or not os.path.isdir(canon_dir):
            return CanonBundleDao("", "", "", (), (), ())
        return CanonBundleDao(
            world_text=self._read_file(canon_dir, "world.md"),
            style_guide_text=self._read_file(canon_dir, "style_guide.md"),
            relationships_text=self._read_file(canon_dir, "relationships.md"),
            characters=self._read_characters(os.path.join(canon_dir, "characters")),
            scenes=self._read_cards(os.path.join(canon_dir, "scenes")),
            props=self._read_cards(os.path.join(canon_dir, "props")),
        )

    @staticmethod
    def _read_file(base: str, name: str) -> str:
        path = os.path.join(base, name)
        if not os.path.isfile(path):
            return ""
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()

    def _read_characters(self, chars_dir: str) -> tuple[CharacterCardDao, ...]:
        if not os.path.isdir(chars_dir):
            return ()
        cards = []
        for folder in sorted(os.listdir(chars_dir)):
            folder_path = os.path.join(chars_dir, folder)
            if not os.path.isdir(folder_path):
                continue
            main_md = os.path.join(folder_path, f"{folder}.md")
            if not os.path.isfile(main_md):
                continue
            with open(main_md, "r", encoding="utf-8") as fh:
                text = fh.read()
            name = folder.split("_", 1)[1] if "_" in folder else folder
            tag_match = _LOCKED_TAG_ROW.search(text)
            locked_tag = None
            if tag_match:
                locked_tag = re.sub(r"\*\*", "", tag_match.group(1)).strip()
            voice_match = _VOICE_ID.search(text)
            cards.append(
                CharacterCardDao(
                    name=name,
                    folder=folder,
                    text=text,
                    locked_tag=locked_tag,
                    voice_id=voice_match.group(1) if voice_match else None,
                )
            )
        return tuple(cards)

    @staticmethod
    def _read_cards(cards_dir: str) -> tuple[SceneCardDao, ...]:
        if not os.path.isdir(cards_dir):
            return ()
        cards = []
        for folder in sorted(os.listdir(cards_dir)):
            folder_path = os.path.join(cards_dir, folder)
            if os.path.isdir(folder_path):
                main_md = os.path.join(folder_path, f"{folder}.md")
                if not os.path.isfile(main_md):
                    continue
                with open(main_md, "r", encoding="utf-8") as fh:
                    text = fh.read()
                name = folder.split("_", 1)[1] if "_" in folder else folder
            elif folder.endswith(".md"):
                with open(folder_path, "r", encoding="utf-8") as fh:
                    text = fh.read()
                name = folder[:-3]
            else:
                continue
            cards.append(SceneCardDao(name=name, folder=folder, text=text))
        return tuple(cards)
