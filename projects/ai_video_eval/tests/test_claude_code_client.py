import json

from libs.infrastructure.clients.claude_code__client import ClaudeCodeClient


def test_extract_json():
    from libs.application.mappers.judge__mapper import JudgeMapper

    fenced = "```json\n{\"a\": 1}\n```"
    assert JudgeMapper.extract_json(fenced) == '{"a": 1}'
    assert JudgeMapper.extract_json('  {"a": 1} ') == '{"a": 1}'
    assert JudgeMapper.extract_json("```\n{}\n```") == "{}"
    preamble = "抱歉，现在直接输出结果。\n\n```json\n{\"judgments\": []}\n```"
    assert JudgeMapper.extract_json(preamble) == '{"judgments": []}'
    bare = "前言文字 {\"a\": {\"b\": 2}} 尾注"
    assert JudgeMapper.extract_json(bare) == '{"a": {"b": 2}}'


def test_build_prompt_contains_schema_and_blocks():
    schema = {"type": "object", "properties": {"judgments": {}}}
    prompt = ClaudeCodeClient._build_prompt(
        "SYS", [{"type": "text", "text": "BLOCK1"}, {"type": "text", "text": "BLOCK2"}], schema
    )
    assert prompt.startswith("SYS")
    assert "BLOCK1" in prompt and "BLOCK2" in prompt
    assert json.dumps(schema, ensure_ascii=False) in prompt
    assert "只输出一个符合" in prompt
