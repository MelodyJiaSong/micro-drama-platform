from __future__ import annotations

import httpx

_DEFAULT_BASE = "https://dashscope.aliyuncs.com"


class QwenClient:
    def __init__(self, api_key: str, base_url: str = _DEFAULT_BASE, timeout_s: float = 30.0) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s

    @property
    def configured(self) -> bool:
        return bool(self._api_key)

    def ping(self) -> dict[str, str]:
        resp = httpx.post(
            f"{self._base_url}/compatible-mode/v1/chat/completions",
            json={"model": "qwen3-vl-plus", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1},
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=self._timeout_s,
        )
        return {"status_code": str(resp.status_code), "ok": str(resp.status_code == 200)}
