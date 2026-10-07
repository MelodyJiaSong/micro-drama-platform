import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prompt_compact as pc


def test_fixed_short_phases_do_not_collapse_when_preserving_timing():
    full = "动作: 0–2.5s聚光；2.5–2.8s举手；2.8–3.05s光柱；3.05–4.2s收束\n台词: 0–2.5s Sammuel（正常台词·口型对Sammuel）：Pheta vi acahachi.\n时长: 14s"
    actual = pc.compact(full, [pc.Cast('c14', 'Sammuel', speaker='Sammuel')], 14, 'native', preserve_timing=True)
    assert '2.5–2.8秒举手' in actual
    assert '2.8–3.05秒光柱' in actual
    assert '3.05–4.2秒收束' in actual
    assert '0–2.5秒 Sammuel说：{Pheta vi acahachi.}' in actual
    assert '3–3秒' not in actual


def test_each_native_speaker_keeps_own_nonoverlapping_window():
    full = '台词: 0.4–1.8s Aaron（正常台词·口型对Aaron）：Here?；2.2–4.1s Duke（正常台词·口型对Duke）：Here.\n时长: 10s'
    actual = pc.compact(full, [pc.Cast('c1', 'Aaron', speaker='Aaron'), pc.Cast('c2', 'Duke', speaker='Duke')], 10, 'native', preserve_timing=True)
    assert '0.4–1.8秒 Aaron说：{Here?}' in actual
    assert '2.2–4.1秒 Duke说：{Here.}' in actual


def test_legacy_default_still_uses_existing_rounding_policy():
    assert pc.whole_seconds('2.5–2.8s举手') == '3–3秒举手'
    assert pc.exact_seconds('2.5–2.8s举手') == '2.5–2.8秒举手'
