"""The fake site's control plane and envelopes, over HTTP (no browser)."""
from __future__ import annotations

import json
import urllib.request

from tests.fixtures.fake_jimeng_site.server import LOCAL_OPENER, FakeJimengSite


def post(url: str, payload: dict[str, object]) -> dict[str, object]:
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST", headers={"content-type": "application/json"})
    with LOCAL_OPENER.open(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def test_control_plane_injects_and_reports_ledger(fake_jimeng_site: FakeJimengSite) -> None:
    site = fake_jimeng_site
    site.control("reset", {})
    assert site.control("inject", {"name": "login_expired", "times": 1})["ok"] is True
    body = post(f"{site.origin}/mweb/v1/get_history_by_ids?aid=513695", {"history_ids": []})
    assert (body["ret"], body["errmsg"], body["data"]) == ("1015", "login error", None)
    assert set(body) == {"ret", "errmsg", "systime", "logid", "data"}
    ledger = site.control("ledger")
    assert ledger["counts"]["generate_clicks"] == 0 and ledger["counts"]["status_requests"] == 1
    site.control("reset", {})
    assert post(f"{site.origin}/mweb/v1/get_history_queue_info?aid=1", {"history_ids": []})["ret"] == "0"


def test_control_plane_is_not_on_the_page_origin(fake_jimeng_site: FakeJimengSite) -> None:
    assert fake_jimeng_site.control_url.split("/__fake__")[0] != fake_jimeng_site.origin
