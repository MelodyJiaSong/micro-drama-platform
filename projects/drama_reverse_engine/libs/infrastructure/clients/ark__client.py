from __future__ import annotations

from typing import Any

import httpx

from libs.infrastructure.errors.ark__error import ArkApiError

_DEFAULT_BASE = "https://ark.cn-beijing.volces.com"


class ArkClient:
    """火山方舟 (Volcengine Ark) chat completions — powers the LLM composer (novel +
    descriptor authoring). Video/image generation endpoints were removed with the
    Seedance regeneration side (follow-up 001)."""

    def __init__(self, api_key: str, base_url: str = _DEFAULT_BASE, timeout_s: float = 60.0) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s

    @property
    def configured(self) -> bool:
        return bool(self._api_key)

    def chat(self, model: str, messages: list[dict[str, Any]], temperature: float = 0.7) -> str:
        data = self._post("/api/v3/chat/completions",
                          {"model": model, "messages": messages, "temperature": temperature})
        return str(data["choices"][0]["message"]["content"])

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        resp = httpx.post(self._base_url + path, json=body, headers=self._headers(), timeout=self._timeout_s)
        return self._unwrap(resp)

    @staticmethod
    def _unwrap(resp: httpx.Response) -> dict[str, Any]:
        if resp.status_code >= 400:
            try:
                err = resp.json().get("error", {})
            except ValueError:
                err = {}
            raise ArkApiError(code=str(err.get("code", resp.status_code)), message=str(err.get("message", resp.text[:300])))
        return resp.json()
