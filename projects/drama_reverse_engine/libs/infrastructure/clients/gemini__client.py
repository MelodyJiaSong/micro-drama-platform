from __future__ import annotations

import httpx

_DEFAULT_BASE = "https://generativelanguage.googleapis.com"


class GeminiClient:
    def __init__(self, api_key: str, base_url: str = _DEFAULT_BASE, timeout_s: float = 30.0) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s

    @property
    def configured(self) -> bool:
        return bool(self._api_key)

    def ping(self) -> dict[str, str]:
        resp = httpx.get(
            f"{self._base_url}/v1beta/models",
            params={"pageSize": 1},
            headers={"x-goog-api-key": self._api_key},
            timeout=self._timeout_s,
        )
        return {"status_code": str(resp.status_code), "ok": str(resp.status_code == 200)}
