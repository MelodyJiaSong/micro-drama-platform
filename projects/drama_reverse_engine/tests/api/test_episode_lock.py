from __future__ import annotations


def _create(client):
    return client.post("/api/dramas", json={
        "drama_id": "d1", "title": "锁测试", "declaration_accepted": True, "declared_by": "op",
    })


def test_api_step_contends_for_worker_lock(app_ctx) -> None:
    """UI「自动跑完」racing a worker double-executed stages (2026-07-18 real run:
    compose read understanding.json mid-write) — API runs must claim the same lock."""
    client, container, root = app_ctx
    _create(client)
    states = container.state_writer()
    (root / "d1/ep01").mkdir(parents=True, exist_ok=True)
    states.init_state("d1/ep01")

    assert states.try_claim("d1/ep01", "worker-elsewhere")
    resp = client.post("/api/episodes/step", json={"drama_id": "d1", "episode_rel_dir": "d1/ep01"})
    assert resp.status_code == 409 and "busy" in resp.json()["detail"]

    states.release("d1/ep01")
    resp = client.post("/api/episodes/step", json={"drama_id": "d1", "episode_rel_dir": "d1/ep01"})
    assert resp.status_code == 200
    assert not (root / "d1/ep01/.worker_lock").exists()  # api released its claim
