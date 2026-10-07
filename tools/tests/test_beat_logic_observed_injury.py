import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import beat_logic


def check(action):
    actors = [{"key": "c1", "label": "Sammuel", "path": [[0, 0, 0], [10, 0, 0]]},
              {"key": "c2", "label": "Willem", "path": [[0, 1, 0], [10, 1, 0]]}]
    return beat_logic.check_shot("S01", action, action, {"actor": actors}, "", [], ["S01"])


def test_inspecting_other_person_is_not_a_new_injury_to_observer():
    assert not check("0–10s Sammuel察看Willem靴口的浅擦伤。")


def test_existing_and_healed_scrapes_are_not_new_injuries():
    assert not check("0–10s Willem右踝仍肿、浅擦伤清楚。")
    assert not check("0–10s Willem浅擦伤闭合。")


def test_new_scrape_still_requires_a_state_record():
    assert any("没在 states.toml" in x for x in check("0–10s Willem小腿擦过石头留下浅擦伤。"))


def test_bite_during_examination_still_requires_a_state_record():
    assert any("没在 states.toml" in x for x in check("0–10s Sammuel检查擦伤，狼咬住Sammuel手臂。"))
