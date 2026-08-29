from __future__ import annotations

from libs.infrastructure.clients.ark__client import ArkClient

_MODEL = "doubao-seed-1-6-251015"


class DoubaoLlmComposer:
    """LlmComposer backend on 火山方舟 chat completions (same vendor as Seedance)."""

    def __init__(self, ark: ArkClient, model: str = _MODEL) -> None:
        self._ark = ark
        self._model = model

    @property
    def available(self) -> bool:
        return self._ark.configured

    def compose_novel(self, script_markdown: str, narrative: str) -> str:
        return self._ark.chat(self._model, [
            {"role": "system", "content": (
                "你是短剧小说改编作者。基于剧本忠实改写为可发布的中文小说章节：情节与台词不改动，"
                "叙述文学化润色；大白话口语、不用书面腔。输出 markdown。")},
            {"role": "user", "content": f"叙事梗概：{narrative}\n\n剧本：\n{script_markdown}"},
        ])

    def author_descriptor(self, character_name: str, ref_notes: str) -> str:
        return self._ark.chat(self._model, [
            {"role": "system", "content": (
                "为短剧角色写一条锁定中文外观描述符（一句话，含年龄段/脸型五官特征/发型/服装，"
                "不含情绪动作，60 字内），用于逐镜 byte-identical 复贴。只输出描述符本身。")},
            {"role": "user", "content": f"角色：{character_name}；参考信息：{ref_notes}"},
        ]).strip()
