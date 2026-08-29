from __future__ import annotations

from libs.infrastructure.clients.claudecli__client import ClaudeCliClient


class ClaudeLlmComposer:
    """LlmComposer backend on the local Claude Code CLI (zero API key, follow-up 002).
    Prompts mirror the Doubao backend so either engine yields the same artifact shape."""

    def __init__(self, cli: ClaudeCliClient) -> None:
        self._cli = cli

    @property
    def available(self) -> bool:
        return self._cli.available

    def compose_novel(self, script_markdown: str, narrative: str) -> str:
        return self._cli.run_text(
            "你是短剧小说改编作者。基于剧本忠实改写为可发布的中文小说章节：情节与台词不改动，"
            "叙述文学化润色；大白话口语、不用书面腔。只输出小说 markdown 正文，不要输出任何解释。\n\n"
            f"叙事梗概：{narrative}\n\n剧本：\n{script_markdown}"
        )

    def author_descriptor(self, character_name: str, ref_notes: str) -> str:
        return self._cli.run_text(
            "为短剧角色写一条锁定中文外观描述符（一句话，含年龄段/脸型五官特征/发型/服装，"
            "不含情绪动作、不含角色名，60 字内），用于逐镜 byte-identical 复贴（prompt 会以「角色名，描述符」"
            "格式拼接）。只输出描述符本身，不要输出任何解释。\n\n"
            f"角色：{character_name}；参考信息：{ref_notes}"
        ).strip()
