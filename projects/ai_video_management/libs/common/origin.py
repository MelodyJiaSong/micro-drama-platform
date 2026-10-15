"""Pure value object for the backend's bound origin (host + port) and the
static security rules (which requests the Origin/Host gate checks, CSP_HEADER).
Used by both the middleware adapter in libs/infrastructure/ and the
container/app_factory wiring in apps/api/.

These are pure data — no framework, no I/O — so they live in libs/common/
where domain, infrastructure, and apps can all import them without
violating the dependency arrows in development.md §1.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BoundOrigin:
    host: str
    port: int

    def origin_allow_list(self) -> frozenset[str]:
        if self.host in {"127.0.0.1", "localhost"}:
            return frozenset(
                {
                    f"http://127.0.0.1:{self.port}",
                    f"http://localhost:{self.port}",
                }
            )
        return frozenset({f"http://{self.host}:{self.port}"})

    def host_allow_list(self) -> frozenset[str]:
        if self.host in {"127.0.0.1", "localhost"}:
            return frozenset(
                {
                    f"127.0.0.1:{self.port}",
                    f"localhost:{self.port}",
                }
            )
        return frozenset({f"{self.host}:{self.port}"})


# Methods that never change state here; the Origin/Host gate lets them through.
SAFE_METHODS: frozenset[str] = frozenset({"GET", "HEAD", "OPTIONS"})


def is_guarded(method: str) -> bool:
    """True for every request the Origin/Host gate must check (follow-up 239).

    Any page open in the browser can send a no-preflight POST to 127.0.0.1 — a
    plain form post or `fetch(..., {mode: "no-cors"})`. The gate used to check
    only `PUT /api/file` and `POST /api/episode-workflow`, so a foreign page
    could archive, delete, hard-delete, empty the recycle bin, import Downloads
    or overwrite research marks.

    The rule is by method, not by a route list: a new write endpoint is covered
    without anyone remembering to register it, and nothing depends on how a
    request path is spelled or normalized. Every write endpoint lives under
    `/api/`; the static bundle only answers GET/HEAD, so checking other methods
    elsewhere changes nothing but the status a foreign page sees (403, not 405).
    """
    return method.upper() not in SAFE_METHODS


CSP_HEADER: str = (
    "default-src 'self'; "
    "img-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "script-src 'self' 'wasm-unsafe-eval'; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'"
)
