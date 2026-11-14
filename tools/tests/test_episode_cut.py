from tools import episode_cut as ec


def _cut(**kw):
    cut = {"scenes": [{"scene": "s1"}, {"scene": "s2"}],
           "transitions": [{"from": "s1", "to": "s2", "type": "cut", "reason": "同一时刻"}]}
    cut.update(kw)
    return cut


def test_menu_covers_the_edit_side_of_the_transition_guide():
    # edit-transitions.md「剪辑可做」：切、淡入淡出、黑场、白场、叠化、叠印、硬切、J/L、光圈、划像
    for k in ("cut", "smash_cut", "dissolve", "superimpose", "dip_to_black", "dip_to_white", "iris_open", "wipe_left"):
        assert k in ec.MENU
    assert set(ec.EDGES) == {"cut", "fade_black", "fade_white"}
    assert all(xf is None for k, (_, xf, *_rest) in ec.MENU.items() if k in ("cut", "smash_cut"))


def test_valid_decision_passes():
    assert ec.check(_cut()) == []
    assert ec.check(_cut(transitions=[{"from": "s1", "to": "s2", "type": "cut", "audio": {"j": 0.75}, "reason": "x"}],
                         head={"type": "fade_black", "duration": 1.0})) == []


def test_every_transition_needs_a_menu_type_reason_and_duration():
    bad = ec.check(_cut(transitions=[{"from": "s1", "to": "s2", "type": "page_curl"}]))
    assert any("未知转场" in p for p in bad)
    bad = ec.check(_cut(transitions=[{"from": "s1", "to": "s2", "type": "dissolve", "reason": "x"}]))
    assert any("duration" in p for p in bad)
    bad = ec.check(_cut(transitions=[{"from": "s1", "to": "s2", "type": "cut"}]))
    assert any("理由" in p for p in bad)


def test_j_l_only_on_cuts_and_pairs_in_order():
    bad = ec.check(_cut(transitions=[{"from": "s1", "to": "s2", "type": "dissolve", "duration": 1, "audio": {"j": 1}, "reason": "x"}]))
    assert any("J / L" in p for p in bad)
    bad = ec.check(_cut(transitions=[{"from": "s2", "to": "s1", "type": "cut", "reason": "x"}]))
    assert any("相邻场" in p for p in bad)
    bad = ec.check(_cut(tail={"type": "fade_black"}))
    assert any("tail" in p for p in bad)


def test_assemble_mixes_cut_and_dissolve(tmp_path):
    """切（concat）之后接叠化（xfade）：两路时间基须一致，否则 ffmpeg 报 timebase do not match（chuanyue_yiri EP01）。"""
    import shutil
    import subprocess
    import pytest
    if not shutil.which("ffmpeg"):
        pytest.skip("没有 ffmpeg")
    clips = []
    for i, color in enumerate(("red", "green", "blue")):
        p = tmp_path / ("c%d.mp4" % i)
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=%s:s=160x90:r=24:d=2" % color,
                        "-f", "lavfi", "-i", "sine=f=440:d=2", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        str(p), "-y"], check=True)
        clips.append(p)
    segs = [{"video": p, "start": 0.0, "dur": 2.0} for p in clips]
    trans = [{"type": "cut"}, {"type": "dissolve", "duration": 0.5}]
    out = tmp_path / "out.mp4"
    total, cuts = ec.assemble(segs, trans, {"type": "cut"}, {"type": "fade_black", "duration": 0.5},
                              {"fps": 24, "audio_rate": 48000}, out)
    assert total == 5.5 and cuts == [2.0]
    assert out.is_file() and out.stat().st_size > 0
