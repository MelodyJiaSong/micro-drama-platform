import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import shot_overhead


def test_low_wall_center_gate_allows_passage_but_solid_sides_still_block():
    wall = {"id": "b13", "name": "院北墙", "kind": "low_wall", "xy": [45, 13],
            "size": [42, .7], "h_m": 1.3, "gate_w": 3}
    cfg = {"meta": {}, "actor": [{"key": "c1", "label": "甲",
                                   "path": [[9, 44.6, 13], [10, 45.4, 13]]}]}
    assert shot_overhead.low_block_errors(cfg, {"block": [wall]}) == []
    cfg["actor"][0]["path"] = [[9, 47, 13]]
    assert len(shot_overhead.low_block_errors(cfg, {"block": [wall]})) == 1
    solid = {k: v for k, v in wall.items() if k != "gate_w"}
    cfg["actor"][0]["path"] = [[9, 45, 13]]
    assert len(shot_overhead.low_block_errors(cfg, {"block": [solid]})) == 1


def test_low_wall_opening_tracks_north_south_and_explicit_rotation():
    wall = {"kind": "low_wall", "xy": [0, 0], "size": [.7, 42], "gate_w": 3}
    assert shot_overhead._in_opening(wall, 0, 1)
    assert not shot_overhead._in_opening(wall, 0, 2)
    rotated = {**wall, "size": [42, .7], "rot": 45}
    assert shot_overhead._in_opening(rotated, .7, .7)
    assert not shot_overhead._in_opening(rotated, 1.5, 1.5)


def test_unrelated_block_gate_attribute_does_not_create_fake_opening():
    block = {"kind": "hall", "xy": [0, 0], "size": [10, 10], "gate_w": 3}
    assert not shot_overhead._in_opening(block, 0, 0)
