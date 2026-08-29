from __future__ import annotations

from libs.infrastructure.clients.claude_composer__client import ClaudeLlmComposer


class _FakeCli:
    available = True

    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.prompts: list[str] = []

    def run_text(self, prompt: str, read_dirs: tuple[str, ...] = (), max_turns: int = 8) -> str:
        self.prompts.append(prompt)
        return self.reply


def test_compose_novel_passes_script_and_narrative() -> None:
    cli = _FakeCli("# 第一章\n\n他回来了。")
    out = ClaudeLlmComposer(cli).compose_novel("# 剧本\n> 裴远：「你还敢回来？」", "废婿归来")  # type: ignore[arg-type]
    assert out.startswith("# 第一章")
    assert "废婿归来" in cli.prompts[0] and "你还敢回来？" in cli.prompts[0]


def test_author_descriptor_strips_whitespace() -> None:
    cli = _FakeCli("  裴远：三十岁上下，剑眉星目，玄色劲装。\n")
    out = ClaudeLlmComposer(cli).author_descriptor("裴远", "参考帧×3")  # type: ignore[arg-type]
    assert out == "裴远：三十岁上下，剑眉星目，玄色劲装。"
    assert "裴远" in cli.prompts[0] and "参考帧×3" in cli.prompts[0]


def test_availability_mirrors_cli() -> None:
    cli = _FakeCli("x")
    cli.available = False
    assert ClaudeLlmComposer(cli).available is False  # type: ignore[arg-type]
