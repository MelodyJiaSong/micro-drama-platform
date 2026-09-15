from __future__ import annotations

from tests.contract.ui_contract import FIXTURE_DIR, render


def test_ui_contract_fixtures_match_current_dtos() -> None:
    wanted = render()
    on_disk = {path.name: path.read_text(encoding="utf-8") for path in FIXTURE_DIR.glob("*.json")}
    stale = sorted(name for name in wanted if on_disk.get(name) != wanted[name])
    extra = sorted(set(on_disk) - set(wanted))
    assert not stale and not extra, f"UI contract fixtures out of date ({stale + extra}); run `make ui-contract`"
