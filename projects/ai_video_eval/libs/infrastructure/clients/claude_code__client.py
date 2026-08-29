import asyncio
import json
import os
import shutil
import tempfile

from libs.infrastructure.clients.anthropic__client import JudgeCallResult
from libs.infrastructure.daos.config__dao import EvalConfigDao, JudgeModelConfigDao
from libs.infrastructure.errors.judge__error import JudgeError

class ClaudeCodeClient:
    """Judge engine backed by headless `claude -p` subprocesses (subscription auth).

    Independence: each subprocess runs with cwd in the system temp dir (no repo
    CLAUDE.md / skills / .mcp.json can load) and --strict-mcp-config with no MCP
    config (zero MCP servers).
    """

    def __init__(self, config: EvalConfigDao) -> None:
        self._config = config
        self._exe = shutil.which("claude")
        self._workdir = os.path.join(tempfile.gettempdir(), "ai_video_eval_judge")

    async def judge(
        self,
        model_config: JudgeModelConfigDao,
        system: str,
        content_blocks: list[dict],
        output_schema: dict,
    ) -> JudgeCallResult:
        if self._exe is None:
            raise JudgeError("claude CLI not found on PATH (needed for engine=claude_code)")
        os.makedirs(self._workdir, exist_ok=True)
        prompt = self._build_prompt(system, content_blocks, output_schema)
        args = [
            self._exe,
            "-p",
            "--output-format", "json",
            "--model", model_config.model,
            "--strict-mcp-config",
            "--disallowedTools",
            "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Task,TodoWrite,NotebookEdit",
        ]
        process = await asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self._workdir,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(prompt.encode("utf-8")), timeout=self._config.timeout_s
            )
        except asyncio.TimeoutError as exc:
            process.kill()
            raise JudgeError(f"claude -p timed out after {self._config.timeout_s}s") from exc
        if process.returncode != 0:
            snippet = stderr.decode("utf-8", errors="replace")[-500:]
            raise JudgeError(f"claude -p exited {process.returncode}: {snippet}")
        try:
            wrapper = json.loads(stdout.decode("utf-8", errors="replace"))
        except json.JSONDecodeError as exc:
            raise JudgeError(f"claude -p emitted non-JSON wrapper: {exc}") from exc
        if wrapper.get("is_error") or wrapper.get("subtype") not in (None, "success"):
            raise JudgeError(f"claude -p error result: {str(wrapper.get('result'))[:300]}")
        text = str(wrapper.get("result", ""))
        usage = wrapper.get("usage") or {}
        return JudgeCallResult(
            text=text,
            model=model_config.model,
            input_tokens=int(usage.get("input_tokens", 0)),
            output_tokens=int(usage.get("output_tokens", 0)),
            cache_read_tokens=int(usage.get("cache_read_input_tokens", 0)),
            cache_write_tokens=int(usage.get("cache_creation_input_tokens", 0)),
        )

    @staticmethod
    def _build_prompt(system: str, content_blocks: list[dict], output_schema: dict) -> str:
        parts = [system]
        parts.extend(block["text"] for block in content_blocks)
        parts.append(
            "# 输出要求\n不要调用任何工具、不要读写任何文件——直接输出评审结果。"
            "只输出一个符合下述 JSON Schema 的 JSON 对象。"
            "不要用 markdown 代码块包裹、不要输出任何 JSON 之外的文字。\nSchema:\n"
            + json.dumps(output_schema, ensure_ascii=False)
        )
        return "\n\n".join(parts)
