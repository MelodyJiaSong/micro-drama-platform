import re

import yaml

from libs.infrastructure.daos.shot__dao import ShotDao, VoiceBlockDao

_CONTEXT_BULLET = re.compile(r"^-\s+\*\*(.+?)\*\*\s*[:：]\s*(.*)$")
_PROMPT_FIELD = re.compile(
    r"^(参考|角色识别[^:：]*|角色|情节|场景|镜头|走位|动作|台词|光线[^:：]*|节奏|渲染样式|负面词|比例|时长)\s*[:：]\s?(.*)$"
)
_VOICE_FIELD = re.compile(r"^(角色|音色|情绪|语速|类型|台词|时长目标)\s*[:：]\s?(.*)$")


class ShotReader:
    def read(self, path: str) -> ShotDao:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
        envelope, body = self._split_envelope(raw)
        sections = self._split_sections(body)

        novel = sections.get("小说原文", "") or sections.get("原作与结构依据", "")
        title = ""
        for line in body.splitlines():
            if line.startswith("# ") and not line.startswith("## "):
                title = line[2:].strip()
                break

        context = self._parse_context(sections.get("Shot context", ""))
        prompt_title, prompt_fields, prompt_body = self._parse_prompt(sections.get("视频 prompt", ""))
        voice_blocks = tuple(
            self._parse_voice(block)
            for name, text in sections.items()
            if "台词配音" in name
            for block in self._fenced_blocks(text)
        )
        return ShotDao(
            path=path,
            raw_text=raw,
            envelope=envelope,
            title=title,
            novel_excerpt=novel.strip(),
            context_bullets=context,
            prompt_title=prompt_title,
            prompt_fields=prompt_fields,
            prompt_body=prompt_body,
            voice_blocks=voice_blocks,
        )

    @staticmethod
    def _split_envelope(raw: str) -> tuple[dict[str, str], str]:
        stripped = raw.lstrip()
        if not stripped.startswith("---"):
            return {}, raw
        parts = stripped.split("---", 2)
        if len(parts) < 3:
            return {}, raw
        try:
            loaded = yaml.safe_load(parts[1]) or {}
            envelope = {str(k): str(v) for k, v in loaded.items()} if isinstance(loaded, dict) else {}
        except yaml.YAMLError:
            envelope = {}
        return envelope, parts[2]

    @staticmethod
    def _split_sections(body: str) -> dict[str, str]:
        sections: dict[str, str] = {}
        current: str | None = None
        buffer: list[str] = []
        for line in body.splitlines():
            if line.startswith("## "):
                if current is not None:
                    sections[current] = "\n".join(buffer)
                current = line[3:].strip()
                buffer = []
            elif current is not None:
                buffer.append(line)
        if current is not None:
            sections[current] = "\n".join(buffer)
        normalized: dict[str, str] = {}
        for name, text in sections.items():
            if "台词配音" in name and "台词配音" not in normalized:
                normalized[name] = text
            normalized[name] = text
        return normalized

    @staticmethod
    def _parse_context(text: str) -> dict[str, str]:
        bullets: dict[str, str] = {}
        current_key: str | None = None
        for line in text.splitlines():
            match = _CONTEXT_BULLET.match(line.strip())
            if match:
                current_key = match.group(1).strip()
                bullets[current_key] = match.group(2).strip()
            elif current_key and line.strip():
                bullets[current_key] += "\n" + line.strip()
        return bullets

    def _parse_prompt(self, text: str) -> tuple[str, dict[str, str], str]:
        blocks = self._fenced_blocks(text)
        if not blocks:
            return "", {}, ""
        body = blocks[0]
        fields: dict[str, str] = {}
        prompt_title = ""
        current: str | None = None
        from libs.common.constants import PROMPT_FIELD_ALIASES

        for idx, line in enumerate(body.splitlines()):
            match = _PROMPT_FIELD.match(line)
            if match:
                raw_key = match.group(1).strip()
                key = PROMPT_FIELD_ALIASES.get(raw_key)
                if key is None:
                    key = "角色识别" if raw_key.startswith("角色识别") else ("光线" if raw_key.startswith("光线") else raw_key)
                fields[key] = match.group(2).strip()
                current = key
            elif current is not None:
                fields[current] += "\n" + line
            elif idx == 0 and line.strip():
                prompt_title = line.strip()
        fields = {k: v.strip().strip("`").strip() for k, v in fields.items()}
        return prompt_title, fields, body

    @staticmethod
    def _fenced_blocks(text: str) -> list[str]:
        return [m.group(1).strip() for m in re.finditer(r"```text\n(.*?)```", text, re.DOTALL)]

    @staticmethod
    def _parse_voice(block: str) -> VoiceBlockDao:
        fields: dict[str, str] = {}
        for line in block.splitlines():
            match = _VOICE_FIELD.match(line.strip())
            if match:
                fields[match.group(1)] = match.group(2).strip()
        return VoiceBlockDao(raw=block, fields=fields)
