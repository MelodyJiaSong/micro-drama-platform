"""场故事板（follow-up 336）：每镜从所属镜组板的第 i 格切出，按镜头顺序排时间；镜组板变了就重画。"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from tools import scene_board


def scene() -> dict:
    shot = lambda i, d: {"id": f"st{i}", "duration": d, "beats": f"第{i}镜", "action": "a", "dialogue": ""}
    return {"id": "s1", "location": "冰洞", "time": "白天", "shots": [shot(1, 8), shot(2, 6), shot(3, 5)],
            "groups": [{"id": "g1", "shots": ["st1", "st2"]}]}


def test_panels_follow_the_shots_and_redraw_when_a_board_changes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(scene_board, "REPO", tmp_path)
    ep = tmp_path / "ep01"
    board = ep / "scenes/s1/groups/g1/board.png"
    board.parent.mkdir(parents=True)
    im = Image.new("RGB", (200, 100), "white")
    im.paste((255, 0, 0), (0, 0, 100, 50))      # 第 1 格红
    im.paste((0, 0, 255), (100, 0, 200, 50))    # 第 2 格蓝
    im.save(board)
    items = scene_board.panels(scene(), ep)
    assert [(i["shot"], i["group"], i["start"], i["end"]) for i in items] == [("st1", "g1", 0, 8), ("st2", "g1", 8, 14), ("st3", None, 14, 19)]
    assert scene_board.cut(board, 0, 2).getpixel((10, 10)) == (255, 0, 0)
    assert scene_board.cut(board, 1, 2).getpixel((10, 10)) == (0, 0, 255)
    assert scene_board.build(ep, scene()) is True
    index = json.loads((ep / "scenes/s1/board/scene_board.json").read_text(encoding="utf-8"))
    assert index["total"] == 19 and [p["image"].rsplit("/", 1)[-1] for p in index["panels"]] == ["p01_st1.jpg", "p02_st2.jpg", "p03_st3.jpg"]
    assert (ep / "scenes/s1/board/scene_board.png").is_file()
    assert scene_board.build(ep, scene()) is False
    im.paste((0, 255, 0), (0, 0, 100, 50))
    im.save(board)
    assert scene_board.stale(ep, scene()) and scene_board.build(ep, scene()) is True


def test_single_shot_uses_its_first_frame(tmp_path: Path, monkeypatch) -> None:
    """没写镜组的单镜用它的首帧图当一格（chuanyue_yiri follow-up 020）。"""
    monkeypatch.setattr(scene_board, "REPO", tmp_path)
    ep = tmp_path / "ep01"
    frame = ep / "scenes/s1/shots/st3/planning/st3_first_frame.png"
    frame.parent.mkdir(parents=True)
    Image.new("RGB", (160, 90), (0, 200, 0)).save(frame)
    items = scene_board.panels(scene(), ep)
    assert items[2]["board"] == frame and items[2]["cells"] == 1
    assert scene_board.cut(frame, 0, 1).getpixel((10, 10)) == (0, 200, 0)
    assert scene_board.build(ep, scene()) is True
    Image.new("RGB", (160, 90), (0, 0, 0)).save(frame)
    assert scene_board.stale(ep, scene())
