"""follow-up 279：资料包检查要发现「overhead 改了、走位预演没重渲」。"""
import json
from pathlib import Path

from tools import overhead_previz, shot_pack
from tools.previz.planschema import PREVIZ_STAMP, render_inputs

OLD, NEW = "[g]\nlen = 6\n", "[g]\nlen = 8\n"


def _shot(tmp_path: Path, monkeypatch, config_now: str) -> Path:
    sd = tmp_path / "st1"
    (sd / "previz").mkdir(parents=True)
    monkeypatch.setattr(shot_pack, "REPO", tmp_path)
    monkeypatch.setattr(overhead_previz, "config", lambda _sd: config_now)
    return sd


def _render(sd: Path, text: str) -> None:
    cfg = sd / "previz" / "previz_config.toml"
    cfg.write_text(text, encoding="utf-8", newline="\n")
    (sd / "previz" / ("st1" + PREVIZ_STAMP)).write_text(json.dumps(render_inputs(cfg)), encoding="utf-8")


def test_fresh_previz_passes(tmp_path, monkeypatch):
    sd = _shot(tmp_path, monkeypatch, OLD)
    _render(sd, OLD)
    assert shot_pack.previz_problems(sd) == []


def test_overhead_changed_after_render_is_flagged(tmp_path, monkeypatch):
    sd = _shot(tmp_path, monkeypatch, NEW)     # overhead 现在生成的配置
    _render(sd, OLD)                           # 渲染时用的旧配置
    (problem,) = shot_pack.previz_problems(sd)
    assert "不是按当前 overhead 生成的" in problem and "--render" in problem


def test_config_rewritten_but_not_rerendered_is_flagged(tmp_path, monkeypatch):
    sd = _shot(tmp_path, monkeypatch, NEW)
    _render(sd, OLD)
    (sd / "previz" / "previz_config.toml").write_text(NEW, encoding="utf-8", newline="\n")
    (problem,) = shot_pack.previz_problems(sd)
    assert "不是按当前 previz 配置渲染的" in problem
