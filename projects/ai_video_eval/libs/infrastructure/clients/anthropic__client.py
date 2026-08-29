import os
from dataclasses import dataclass

import anthropic

from libs.infrastructure.daos.config__dao import EvalConfigDao, JudgeModelConfigDao
from libs.infrastructure.errors.judge__error import ApiKeyMissingError, JudgeRefusedError


@dataclass(frozen=True)
class JudgeCallResult:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int


class AnthropicClient:
    def __init__(self, config: EvalConfigDao) -> None:
        self._config = config
        self._client: anthropic.AsyncAnthropic | None = None

    def _resolve_key(self) -> str:
        for env_name in self._config.api_key_envs:
            value = os.environ.get(env_name)
            if value:
                return value
        raise ApiKeyMissingError(
            f"no API key found; set one of: {', '.join(self._config.api_key_envs)}"
        )

    def _get_client(self) -> anthropic.AsyncAnthropic:
        if self._client is None:
            self._client = anthropic.AsyncAnthropic(
                api_key=self._resolve_key(),
                timeout=self._config.timeout_s,
                max_retries=3,
            )
        return self._client

    async def judge(
        self,
        model_config: JudgeModelConfigDao,
        system: str,
        content_blocks: list[dict],
        output_schema: dict,
    ) -> JudgeCallResult:
        client = self._get_client()
        response = await client.messages.create(
            model=model_config.model,
            max_tokens=model_config.max_tokens,
            system=system,
            messages=[{"role": "user", "content": content_blocks}],
            output_config={
                "format": {"type": "json_schema", "schema": output_schema},
                "effort": model_config.effort,
            },
        )
        if response.stop_reason == "refusal":
            raise JudgeRefusedError(f"judge request refused (model={model_config.model})")
        text = next((b.text for b in response.content if b.type == "text"), "")
        usage = response.usage
        return JudgeCallResult(
            text=text,
            model=response.model,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
            cache_write_tokens=getattr(usage, "cache_creation_input_tokens", 0) or 0,
        )
