from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import beat_logic


def breathing_errors(action: str) -> list[str]:
    return [e for e in beat_logic.check_shot("S01", action, action, None, "", [], ["S01"]) if "喘" in e]


def test_slow_shoulder_carry_explains_breathing_in_next_beat():
    assert not breathing_errors("0–8s Aaron肩扶伤者沿墙慢行。/ 8–10s Aaron停下喘气。")


def test_explicit_carry_walk_explains_breathing_without_running():
    assert not breathing_errors("0–6s 负重走过院子后，Aaron停下喘气。")
    assert not breathing_errors("0–6s 沿墙扶行一路的两个新人停下喘气。")


def test_breathing_without_exertion_still_requires_cause():
    assert breathing_errors("0–6s Aaron站在院子里，停下喘气。")
