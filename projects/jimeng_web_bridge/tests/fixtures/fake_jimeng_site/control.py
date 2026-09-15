"""Control plane of the fake site, served on its own port so the page origin can never reach it."""
from __future__ import annotations

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute, Route

from tests.fixtures.fake_jimeng_site.state import FakeSiteState


class FakeControlEndpoints:
    def __init__(self, state: FakeSiteState) -> None:
        self._state = state

    def routes(self) -> list[BaseRoute]:
        return [
            Route("/__fake__/reset", self.reset, methods=["POST"]),
            Route("/__fake__/inject", self.inject, methods=["POST"]),
            Route("/__fake__/clear_fault", self.clear_fault, methods=["POST"]),
            Route("/__fake__/seed", self.seed, methods=["POST"]),
            Route("/__fake__/hold", self.hold, methods=["POST"]),
            Route("/__fake__/release", self.release, methods=["POST"]),
            Route("/__fake__/finish_external", self.finish_external, methods=["POST"]),
            Route("/__fake__/ledger", self.ledger),
            Route("/__fake__/records", self.records),
        ]

    async def reset(self, request: Request) -> JSONResponse:
        self._state.reset()
        return JSONResponse({"ok": True})

    async def inject(self, request: Request) -> JSONResponse:
        payload = await request.json()
        try:
            self._state.inject(str(payload["name"]), int(payload.get("times", 1)), **dict(payload.get("params") or {}))
        except (KeyError, ValueError) as error:
            return JSONResponse({"ok": False, "error": str(error)}, status_code=400)
        return JSONResponse({"ok": True})

    async def clear_fault(self, request: Request) -> JSONResponse:
        payload = await request.json()
        self._state.clear_fault(str(payload.get("name", "")))
        return JSONResponse({"ok": True})

    async def seed(self, request: Request) -> JSONResponse:
        payload = await request.json()
        self._state.seed(**payload)
        return JSONResponse({"ok": True})

    async def hold(self, request: Request) -> JSONResponse:
        payload = await request.json()
        self._state.hold(str(payload.get("gate", "")))
        return JSONResponse({"ok": True})

    async def release(self, request: Request) -> JSONResponse:
        payload = await request.json()
        self._state.release(str(payload.get("gate", "")))
        return JSONResponse({"ok": True})

    async def finish_external(self, request: Request) -> JSONResponse:
        payload = await request.json()
        self._state.finish_external(int(payload.get("count", 1)))
        return JSONResponse({"ok": True})

    async def ledger(self, request: Request) -> JSONResponse:
        state = self._state
        with state.lock:
            ledger = state.ledger
            return JSONResponse(
                {
                    "counts": ledger.counts(),
                    "param_sets": ledger.param_sets,
                    "uploads": ledger.uploads,
                    "generate_clicks": ledger.generate_clicks,
                    "submits": ledger.submits,
                    "entity_saves": ledger.entity_saves,
                }
            )

    async def records(self, request: Request) -> JSONResponse:
        with self._state.lock:
            return JSONResponse(
                [
                    {"record_id": r.record_id, "status": r.status, "progress": r.progress, "external": r.external}
                    for r in self._state.records.values()
                ]
            )
