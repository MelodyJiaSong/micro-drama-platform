"""场剪辑用镜组的条（chuanyue_yiri follow-up 020）：事件写 group 时条在 groups/gN/ 下，shot 只标这一段画的是哪一镜。"""
from pathlib import Path

import pytest

from tools import scene_cut


def test_take_dir_resolves_group_takes(tmp_path: Path) -> None:
    scene = tmp_path / "s1"
    (scene / "groups/g1/renders/20261107-120000_abcd1234").mkdir(parents=True)
    (scene / "shots/st4/renders/20261107-120500_ef567890").mkdir(parents=True)
    g = scene_cut.take_dir(scene, {"shot": "st2", "group": "g1", "take": "20261107-120000_abcd1234"}, "final")
    assert g == scene / "groups/g1/renders/20261107-120000_abcd1234"
    s = scene_cut.take_dir(scene, {"shot": "st4", "take": "20261107-120500_ef567890"}, "final")
    assert s == scene / "shots/st4/renders/20261107-120500_ef567890"
    with pytest.raises(SystemExit):
        scene_cut.take_dir(scene, {"shot": "st2", "group": "g1", "take": "20261107-120000_abcd1234"}, "draft")
