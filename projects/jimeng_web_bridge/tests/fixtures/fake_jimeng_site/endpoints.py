"""Page-origin endpoints of the fake 即梦 site: HTML pages, static assets, `/mweb/v1/*` JSON with the real
`{ret, errmsg, systime, logid, data}` envelope, and the page-script action channel that feeds the ledger.

Response bodies follow a placeholder schema (`fake-pre-probe`) until the stage-6 probe captures real ones.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import quote, unquote

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles

from tests.fixtures.fake_jimeng_site.state import (
    PRICE_NOW_PER_S,
    SCHEMA_VERSION,
    WEB_VERSION,
    FakeRecord,
    FakeSiteState,
)

STATIC_DIR: Path = Path(__file__).resolve().parent / "static"
STATUS_CODES: dict[str, int] = {"queued": 10, "generating": 20, "failed": 30, "succeeded": 50}
LOGIN_RET, LOGIN_MSG = "1015", "login error"
PARALLEL_RET, PARALLEL_MSG = "1310", "并行任务已达上限，请稍后再试"
CREDIT_RET, CREDIT_MSG = "1006", "积分不足，请充值后再试"
UPLOAD_RET, UPLOAD_MSG = "4001", "上传失败：文件格式或大小不符合要求"
FACE_RET, FACE_MSG = "4002", "上传失败：暂不支持真人人脸，请更换素材"


def envelope(data: object, ret: str = "0", errmsg: str = "success") -> JSONResponse:
    return JSONResponse(
        {"ret": ret, "errmsg": errmsg, "systime": str(int(time.time())), "logid": f"fake{time.time_ns()}", "data": data}
    )


class FakePageEndpoints:
    def __init__(self, state: FakeSiteState) -> None:
        self._state = state
        self._template = (STATIC_DIR / "index.html").read_text(encoding="utf-8")

    def routes(self) -> list[BaseRoute]:
        return [
            Route("/ai-tool/generate", self.generate_page),
            Route("/ai-tool/elements", self.elements_page),
            Mount("/static", app=StaticFiles(directory=str(STATIC_DIR)), name="static"),
            Route("/__page__/act", self.act, methods=["POST"]),
            Route("/__page__/directives", self.directives),
            Route("/commerce/v1/benefits/user_credit", self.user_credit, methods=["POST"]),
            Route("/mweb/v1/dreamina_subject/get", self.subject_get, methods=["POST"]),
            Route("/mweb/v1/dreamina_subject/create", self.subject_create, methods=["POST"]),
            Route("/mweb/v1/get_history", self.history_list, methods=["POST"]),
            Route("/mweb/v1/get_history_by_ids", self.history_by_ids, methods=["POST"]),
            Route("/mweb/v1/get_history_queue_info", self.queue_info, methods=["POST"]),
            Route("/mweb/v1/aigc_draft/generate", self.generate, methods=["POST"]),
            Route("/mweb/v1/aigc_draft/generate_alt", self.generate, methods=["POST"]),
            Route("/mweb/v1/upload_material", self.upload, methods=["POST"]),
            Route("/download/{name}", self.download),
            Route("/favicon.ico", lambda request: Response(status_code=204)),
        ]

    async def generate_page(self, request: Request) -> HTMLResponse:
        return self._page("generate")

    async def elements_page(self, request: Request) -> HTMLResponse:
        return self._page("elements")

    def _page(self, page: str) -> HTMLResponse:
        state = self._state
        with state.lock:
            state.ledger.page_loads += 1
            config = {
                "page": page,
                "nonce": state.nonce,
                "web_version": WEB_VERSION,
                "poll_ms": state.config.poll_ms,
                "upload_delay_ms": state.config.upload_delay_ms,
                "last_creation_type": state.config.last_creation_type,
                "draft": state.config.draft,
                "negative_box": state.config.negative_box,
            }
        html = self._template.replace("__NONCE__", state.nonce).replace(
            "__FAKE_CONFIG__", json.dumps(config, ensure_ascii=False)
        )
        return HTMLResponse(html)

    async def act(self, request: Request) -> JSONResponse:
        payload = await request.json()
        kind = str(payload.get("kind", ""))
        detail = payload.get("detail") or {}
        state = self._state
        with state.lock:
            if kind == "login_input":
                state.ledger.login_inputs += 1
                return JSONResponse({})
            if kind == "editor_refill_swallow":
                return JSONResponse({"swallow": state.take_fault("editor_append_on_refill") is not None})
            if kind == "mention_select":
                return JSONResponse({"drop": state.take_fault("editor_drop_mention") is not None})
            if state.take_fault("captcha_popup") is not None:
                state.pending_captcha = True
            if state.pending_captcha:
                state.ledger.blocked_actions.append({"kind": kind, "t": time.monotonic()})
                return JSONResponse({"block": True, "captcha": True})
            if kind == "set_param":
                return JSONResponse(self._set_param(detail))
            if kind == "generate_click":
                return JSONResponse(self._generate_click(detail))
        return JSONResponse({})

    def _set_param(self, detail: dict[str, object]) -> dict[str, object]:
        state = self._state
        control, value = str(detail.get("control")), detail.get("value")
        display = value
        spec = state.fault("control_readback_mismatch")
        if spec is not None and spec.params.get("control") == control:
            state.take_fault("control_readback_mismatch")
            display = spec.params.get("display", value)
        state.ledger.param_sets.append({"control": control, "value": value, "display": display, "t": time.monotonic()})
        return {"display": display}

    def _generate_click(self, detail: dict[str, object]) -> dict[str, object]:
        state = self._state
        click = {
            "t": time.monotonic(),
            "via": detail.get("via"),
            "text": detail.get("text"),
            "mentions": detail.get("mentions"),
            "materials": detail.get("materials"),
            "params": detail.get("params"),
            "accepted": False,
            "task_id": None,
        }
        state.ledger.generate_clicks.append(click)
        click_id = len(state.ledger.generate_clicks) - 1
        if state.take_fault("risk_popup") is not None:
            return {"click_id": click_id, "route": "none", "risk": True}
        route = "alt" if state.take_fault("submit_response_hidden") is not None else "main"
        return {"click_id": click_id, "route": route}

    async def directives(self, request: Request) -> JSONResponse:
        state = self._state
        with state.lock:
            generating = any(not r.final and not r.external for r in state.records.values())
            reload = state.pending_reload and generating and state.take_fault("page_reload_mid_generation") is not None
            if reload:
                state.pending_reload = False
            hidden = state.fault("mention_candidate_missing")
            return JSONResponse(
                {
                    "logged_in": state.logged_in,
                    "credits": state.credits,
                    "captcha": state.pending_captcha,
                    "reload": reload,
                    "parallel_notice": state.fault("parallel_limit_notice") is not None
                    or state.running_count() >= state.config.running_limit,
                    "send_enabled": "send_enabled" not in state.held,
                    "hidden_candidates": [str(hidden.params.get("stem"))] if hidden is not None else [],
                    "layout_next": state.fault("layout_next") is not None,
                    "negative_box": state.config.negative_box,
                }
            )

    async def user_credit(self, request: Request) -> JSONResponse:
        with self._state.lock:
            if not self._state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            return envelope({"credit": {"total_credit": self._state.credits, "vip_level": "ultra"}})

    async def subject_get(self, request: Request) -> JSONResponse:
        with self._state.lock:
            if not self._state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            subjects = [dict(item) for item in self._state.entities]
        return envelope({"schema": SCHEMA_VERSION, "subject_list": subjects, "has_more": False, "total": len(subjects)})

    async def subject_create(self, request: Request) -> JSONResponse:
        payload = await request.json()
        state = self._state
        with state.lock:
            if not state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            name = str(payload.get("name", ""))
            state.ledger.entity_saves.append(
                {"name": name, "description": payload.get("description"), "materials": payload.get("material_ids")}
            )
            subject_id = f"subj_new_{len(state.ledger.entity_saves)}"
            if state.take_fault("entity_save_fail") is None:
                state.entities.append(
                    {"subject_id": subject_id, "name": name, "description": payload.get("description", ""),
                     "update_time": int(time.time())}
                )
        return envelope({"subject_id": subject_id})

    async def history_list(self, request: Request) -> Response:
        state = self._state
        with state.lock:
            state.ledger.status_requests += 1
            if not state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            records = sorted(state.records.values(), key=lambda record: record.created_time)
            items = [self._record_json(record) for record in records]
        return envelope({"schema": SCHEMA_VERSION, "records_list": items, "has_more": False})

    async def history_by_ids(self, request: Request) -> Response:
        payload = await request.json()
        blocked = await self._status_faults()
        if blocked is not None:
            return blocked
        state = self._state
        with state.lock:
            if not state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            data: dict[str, object] = {}
            for record_id in payload.get("history_ids") or []:
                record = state.records.get(str(record_id))
                if record is None:
                    continue
                state.advance(record)
                data[record.record_id] = self._record_json(record)
        return envelope(data)

    async def queue_info(self, request: Request) -> Response:
        payload = await request.json()
        blocked = await self._status_faults()
        if blocked is not None:
            return blocked
        state = self._state
        with state.lock:
            if not state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            infos = {
                record.record_id: {"status": STATUS_CODES[record.status], "progress": record.progress, "queue_idx": 0}
                for record in state.records.values()
                if record.record_id in {str(item) for item in payload.get("history_ids") or []}
            }
            data = {"running_count": state.running_count(), "running_limit": state.config.running_limit, "queue_infos": infos}
        return envelope(data)

    async def _status_faults(self) -> Response | None:
        state = self._state
        with state.lock:
            state.ledger.status_requests += 1
            delayed = state.fault("status_delayed")
            delay_s = float(delayed.params.get("delay_s", 2.0)) if delayed is not None else 0.0
            malformed = state.take_fault("status_malformed") is not None
        if delay_s:
            await asyncio.sleep(delay_s)
        if malformed:
            return Response("<html>502 bad gateway</html>", media_type="application/json")
        return None

    async def generate(self, request: Request) -> JSONResponse:
        payload = await request.json()
        state = self._state
        while state.is_held("submit_response"):
            await asyncio.sleep(0.05)
        with state.lock:
            clicks = state.ledger.generate_clicks
            click_id = payload.get("click_id")
            click = clicks[click_id] if isinstance(click_id, int) and 0 <= click_id < len(clicks) else {}
            params = payload.get("params") or {}
            cost = int(params.get("duration", 0)) * PRICE_NOW_PER_S.get(str(params.get("model")), 20) * int(params.get("count", 1))
            submit = {"path": request.url.path, "accepted": False, "task_id": None, "text": payload.get("text")}
            state.ledger.submits.append(submit)
            if not state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            if state.credits < cost:
                return envelope(None, CREDIT_RET, CREDIT_MSG)
            if state.take_fault("backpressure") is not None or state.running_count() >= state.config.running_limit:
                return envelope(None, PARALLEL_RET, PARALLEL_MSG)
            record = state.new_record(
                str(payload.get("text", "")), list(payload.get("mentions") or []), list(payload.get("materials") or []), params
            )
            record.credits = cost
            state.credits -= cost
            submit.update(accepted=True, task_id=record.record_id)
            click.update(accepted=True, task_id=record.record_id)
        return envelope({"aigc_data": {"history_record_id": record.record_id, "task": {"task_id": f"task_{record.record_id}"}}})

    async def upload(self, request: Request) -> JSONResponse:
        filename = unquote(request.headers.get("x-file-name", "unnamed"))
        body = await request.body()
        stem = filename.rsplit(".", 1)[0]
        state = self._state
        await asyncio.sleep(state.config.upload_delay_ms / 1000)
        while state.is_held("upload_done"):
            await asyncio.sleep(0.05)
        with state.lock:
            entry = {"filename": filename, "stem": stem, "sha256": hashlib.sha256(body).hexdigest(), "size": len(body), "accepted": False}
            state.ledger.uploads.append(entry)
            if not state.logged_in:
                return envelope(None, LOGIN_RET, LOGIN_MSG)
            if self._matches(state.fault("upload_reject"), stem):
                state.take_fault("upload_reject")
                return envelope(None, UPLOAD_RET, UPLOAD_MSG)
            face = state.fault("real_face_rejected")
            if self._matches(face, stem) and face is not None and face.params.get("stage", "upload") == "upload":
                state.take_fault("real_face_rejected")
                return envelope(None, FACE_RET, FACE_MSG)
            entry["accepted"] = True
        return envelope({"material_id": f"mat_{len(state.ledger.uploads)}", "name": stem})

    @staticmethod
    def _matches(spec: object, stem: str) -> bool:
        if spec is None:
            return False
        wanted = getattr(spec, "params", {}).get("stem")
        return wanted is None or wanted == stem

    async def download(self, request: Request) -> Response:
        record_id = request.path_params["name"].removesuffix(".mp4")
        state = self._state
        with state.lock:
            record = state.records.get(record_id)
            if record is None or record.status != "succeeded":
                return Response(status_code=404)
            state.ledger.downloads += 1
            data = state.video_bytes
            if state.take_fault("download_truncated") is not None:
                data = data[: len(data) // 3]
            prefix = record.prompt_text.replace("\n", " ")[:16]
        ascii_name = f"jimeng-2026-09-13-{int(record_id) % 10000:04d}.mp4"
        utf8_name = quote(f"jimeng-2026-09-13-{int(record_id) % 10000:04d}-{prefix}....mp4")
        return Response(
            data,
            media_type="video/mp4",
            headers={"Content-Disposition": f"attachment; filename=\"{ascii_name}\"; filename*=UTF-8''{utf8_name}"},
        )

    def _record_json(self, record: FakeRecord) -> dict[str, object]:
        params = record.params
        width, height = _dimensions(str(params.get("ratio", "16:9")), str(params.get("resolution", "720P")))
        items: list[dict[str, object]] = []
        if record.status == "succeeded":
            items.append(
                {
                    "video": {
                        "video_id": f"v_{record.record_id}",
                        "duration_ms": int(params.get("duration", 0)) * 1000,
                        "width": width,
                        "height": height,
                        "file_size": len(self._state.video_bytes),
                    }
                }
            )
        return {
            "history_record_id": record.record_id,
            "status": STATUS_CODES[record.status],
            "progress": record.progress,
            "fail_msg": record.fail_msg,
            "created_time": record.created_time,
            "prompt": record.prompt_text,
            "mention_list": record.mentions,
            "material_list": record.materials,
            "model_name": params.get("model"),
            "duration_s": params.get("duration"),
            "ratio": params.get("ratio"),
            "resolution": params.get("resolution"),
            "credits": record.credits if record.final else None,
            "item_list": items,
        }


def _dimensions(ratio: str, resolution: str) -> tuple[int, int]:
    short = 480 if resolution.upper().startswith("480") else 720
    try:
        w, h = (int(part) for part in ratio.split(":"))
    except ValueError:
        return 1280, 720
    if w >= h:
        return round(short * w / h), short
    return short, round(short * h / w)
