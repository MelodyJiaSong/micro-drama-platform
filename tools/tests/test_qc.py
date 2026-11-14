"""自检与自我进化（dota_yingxiong follow-up 257）。"""
from pathlib import Path

import pytest

from tools import qc

REG = """
[[check]]
id = "video.slowmo"
stage = "video"
kind = "machine"
gate = true
auto = true

[[check]]
id = "video.timeline"
stage = "video"
kind = "review"
gate = true
auto = false

[[check]]
id = "video.onetake_cuts"
stage = "video"
kind = "machine"
gate = true
auto = true
when = "一镜到底"

[[check]]
id = "video.fidelity"
stage = "video"
kind = "review"
layer = "spec"
gate = true
when = "峰值"
"""


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    reg = tmp_path / "qc_checks.toml"
    reg.write_text(REG, encoding="utf-8")
    monkeypatch.setattr(qc, "REGISTRY", reg)
    monkeypatch.setattr(qc, "REPO", tmp_path)
    monkeypatch.setattr(qc, "SPECS", tmp_path / "specs")
    (tmp_path / "specs" / "ai_video" / "demo").mkdir(parents=True)
    return tmp_path


def render(env: Path, name: str = "20261026-120000_abcd1234") -> Path:
    rd = env / "ai_videos" / "demo" / "k1" / "renders" / name
    rd.mkdir(parents=True)
    (rd / "clip.mp4").write_bytes(b"video-bytes")
    return rd


def rec(rd: Path, *checks: str, by: str = "machine", ev: str = "ok") -> int:
    args = ["record", str(rd), "--by", by, "--evidence", ev]
    for c in checks:
        args += ["--check", c]
    return qc.main(args)


def test_gate_requires_qc_and_all_gate_checks(env: Path):
    rd = render(env)
    assert qc.gate_problems(rd, "video", set())[0] == ["没有 qc.json（先跑检查再 `qc.py record`）"]
    rec(rd, "video.slowmo=pass")
    block, _ = qc.gate_problems(rd, "video", set())
    assert any("video.timeline 没查" in b for b in block)           # 审稿项没做 → 挡
    rec(rd, "video.timeline=pass", by="review")
    assert qc.gate_problems(rd, "video", set()) == ([], [])


def test_author_cannot_pass_a_review_check(env: Path):
    rd = render(env)
    with pytest.raises(SystemExit):
        rec(rd, "video.timeline=pass", by="author")


def test_machine_verdict_on_review_check_is_blocked(env: Path):
    rd = render(env)
    rec(rd, "video.slowmo=pass", "video.timeline=pass")             # 机检冒充审稿
    assert any("要独立审稿" in b for b in qc.gate_problems(rd, "video", set())[0])


def test_unreviewed_passes_but_is_counted(env: Path):
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    with pytest.raises(SystemExit):
        rec(rd, "video.timeline=未审", by="review", ev="")             # 未审必须写原因
    rec(rd, "video.timeline=未审", by="review", ev="Codex 无独立上下文")
    block, soft = qc.gate_problems(rd, "video", set())
    assert block == [] and soft == ["video.timeline 未审：Codex 无独立上下文"]


def test_changed_artifact_voids_the_verdict(env: Path):
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=pass", by="review")
    (rd / "clip.mp4").write_bytes(b"re-rendered")
    assert any("sha" in b for b in qc.gate_problems(rd, "video", set())[0])


def test_conditional_check_only_when_spec_asks(env: Path):
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=pass", by="review")
    assert qc.gate_problems(rd, "video", set()) == ([], [])
    assert any("onetake" in b for b in qc.gate_problems(rd, "video", {"一镜到底"})[0])


def test_old_renders_are_not_exempt(env: Path):
    """通用质量不按出片日期豁免（follow-up 354）。"""
    rd = render(env, "20261020-100000_old00000")
    assert qc.gate_problems(rd, "video", set())[0] == ["没有 qc.json（先跑检查再 `qc.py record`）"]


def test_escape_reasons_map_to_evolution_actions(env: Path):
    reg = qc.registry()
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    art = str((rd / "clip.mp4").relative_to(env))
    assert qc.escape_reason({"category": "new:wing_shape", "artifact": art}, reg)[0] == "没有这条检查"
    assert qc.escape_reason({"category": "video.slowmo", "artifact": art}, reg)[0] == "检查放过了"
    assert qc.escape_reason({"category": "video.onetake_cuts", "artifact": art}, reg)[0] == "这件产物没走闸门"
    assert qc.escape_reason({"category": "video.onetake_cuts", "artifact": ""}, reg)[0] == "闸门建立前交付"
    rec(rd, "video.timeline=fail", by="review")
    assert qc.escape_reason({"category": "video.timeline", "artifact": art}, reg)[0] == "只靠审稿、还没自动化"


def test_defect_log_and_escape_rate(env: Path, capsys: pytest.CaptureFixture[str]):
    qc.main(["defect", "demo", "--category", "video.slowmo", "--caught-by", "user", "--followup", "245"])
    qc.main(["defect", "demo", "--category", "video.slowmo", "--caught-by", "machine"])
    with pytest.raises(SystemExit):
        qc.main(["defect", "demo", "--category", "video.made_up", "--caught-by", "user"])
    qc.main(["stats", "demo"])
    assert "逃逸率 50%" in capsys.readouterr().out


def test_drama_registry_merges_and_is_labelled(env: Path):
    (env / "ai_videos" / "demo").mkdir(parents=True, exist_ok=True)
    (env / "ai_videos" / "demo" / "qc_checks.toml").write_text(
        '[[check]]\nid = "video.scale"\nstage = "video"\nkind = "review"\ngate = true\nauto = false\n', encoding="utf-8")
    rd = render(env)
    reg = qc.registry(qc.drama_dir_of(rd))
    assert reg["video.scale"].level == "剧级" and reg["video.slowmo"].level == "仓库级"
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=pass", by="review")
    assert any("video.scale 没查" in b for b in qc.gate_problems(rd, "video", set())[0])   # 剧级闸门也生效
    other = env / "ai_videos" / "other" / "renders" / "20261026-130000_x"
    other.mkdir(parents=True)
    assert "video.scale" not in qc.registry(qc.drama_dir_of(other))                      # 不串到别的剧


def test_same_id_in_both_levels_is_rejected(env: Path):
    (env / "ai_videos" / "demo").mkdir(parents=True, exist_ok=True)
    (env / "ai_videos" / "demo" / "qc_checks.toml").write_text(
        '[[check]]\nid = "video.slowmo"\nstage = "video"\nkind = "machine"\ngate = false\n', encoding="utf-8")
    with pytest.raises(SystemExit):
        qc.registry(env / "ai_videos" / "demo")


def test_override_turns_block_into_counted_false_positive(env: Path, capsys: pytest.CaptureFixture[str]):
    (env / "ai_videos" / "demo").mkdir(parents=True, exist_ok=True)
    (env / "ai_videos" / "demo" / "workflow.json").write_text("{}", encoding="utf-8")
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=fail", by="review", ev="1.75 秒提前出弹道")
    assert any("video.timeline 不通过" in b for b in qc.gate_problems(rd, "video", set())[0])
    with pytest.raises(SystemExit):
        qc.main(["override", str(rd), "--check", "video.slowmo", "--kind", "false_positive", "--note", "x"])  # 只有 fail 才能放行
    qc.main(["override", str(rd), "--check", "video.timeline", "--kind", "false_positive", "--note", "用户：提前一点没关系"])
    block, soft = qc.gate_problems(rd, "video", set())
    assert block == [] and any("用户放行" in s for s in soft)
    qc.main(["stats", "demo"])
    out = capsys.readouterr().out
    assert "误报" in out and "缺陷 0 条" in out                                                # 误报不算缺陷


def demo_drama(env: Path) -> None:
    (env / "ai_videos" / "demo").mkdir(parents=True, exist_ok=True)
    (env / "ai_videos" / "demo" / "workflow.json").write_text("{}", encoding="utf-8")


def test_cannot_judge_needs_reason_and_splits_by_layer(env: Path):
    """审不了（follow-up 354）：通用项缺材料挡住；看不清放行并标待人看；对照规格项缺材料只记录。"""
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    with pytest.raises(SystemExit):
        rec(rd, "video.timeline=审不了", by="review", ev="脸太小")                       # 必须写原因
    qc.main(["record", str(rd), "--by", "review", "--check", "video.timeline=审不了", "--reason", "看不清", "--evidence", "脸太小"])
    block, soft = qc.gate_problems(rd, "video", set())
    assert block == [] and any("待人看" in x for x in soft)
    qc.main(["record", str(rd), "--by", "review", "--check", "video.timeline=审不了", "--reason", "材料缺", "--evidence", "没有拼图"])
    assert any("材料缺" in b for b in qc.gate_problems(rd, "video", set())[0])          # 通用项缺材料 → 挡
    rec(rd, "video.timeline=pass", by="review")
    qc.main(["record", str(rd), "--by", "review", "--check", "video.fidelity=审不了", "--reason", "材料缺", "--evidence", "旧条没有峰值图"])
    block, soft = qc.gate_problems(rd, "video", {"峰值"})
    assert block == [] and any("对照规格" in x and "只记录" in x for x in soft)          # 对照规格项缺材料 → 只记录


def test_fail_from_old_review_rule_must_be_rereviewed(env: Path):
    import json
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=fail", by="review", ev="拿不准")
    qcj = rd / "qc.json"
    data = json.loads(qcj.read_text(encoding="utf-8"))
    del data["checks"]["video.timeline"]["rule"]                                          # 模拟旧规则下的审稿结论
    qcj.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    assert any("旧审稿规则" in b for b in qc.gate_problems(rd, "video", set())[0])


def test_accept_is_not_a_false_positive(env: Path, capsys: pytest.CaptureFixture[str]):
    demo_drama(env)
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=fail", by="review", ev="第 3 拍晚了 4 秒")
    qc.main(["override", str(rd), "--check", "video.timeline", "--kind", "accept", "--note", "这条先这样用"])
    block, soft = qc.gate_problems(rd, "video", set())
    assert block == [] and any("接受这次的瑕疵" in x for x in soft)
    qc.main(["stats", "demo"])
    out = capsys.readouterr().out
    assert "接受瑕疵" in out and "误报（" not in out                                      # 接受瑕疵不提示放松检查


def test_override_voided_when_check_definition_changes(env: Path):
    demo_drama(env)
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=fail", by="review", ev="x")
    qc.main(["override", str(rd), "--check", "video.timeline", "--kind", "accept", "--note", "先这样"])
    assert qc.gate_problems(rd, "video", set())[0] == []
    reg = env / "qc_checks.toml"
    reg.write_text(reg.read_text(encoding="utf-8").replace('id = "video.timeline"', 'id = "video.timeline"\ndesc = "收紧了"'),
                   encoding="utf-8")
    assert any("放行已作废" in b for b in qc.gate_problems(rd, "video", set())[0])


def test_one_quote_covers_one_check_category(env: Path):
    demo_drama(env)
    reg = env / "qc_checks.toml"
    reg.write_text(reg.read_text(encoding="utf-8") + '\n[[check]]\nid = "video.gaze"\nstage = "video"\nkind = "review"\ngate = true\n',
                   encoding="utf-8")
    rd = render(env)
    rec(rd, "video.slowmo=pass")
    rec(rd, "video.timeline=fail", "video.gaze=fail", by="review", ev="x")
    quote = "ok，不用确认，你自己按 best effort 重出视频就行"
    qc.main(["override", str(rd), "--check", "video.timeline", "--kind", "accept", "--note", quote])
    with pytest.raises(SystemExit):                                                       # 同一句泛化授权不能再放行另一类
        qc.main(["override", str(rd), "--check", "video.gaze", "--kind", "accept", "--note", quote])
    with pytest.raises(SystemExit):                                                       # --mention 必须是原话的一部分
        qc.main(["override", str(rd), "--check", "video.gaze", "--kind", "accept", "--note", quote, "--mention", "视线"])
    quote2 = "时间轴和视线这两类都放行"
    qc.main(["override", str(rd), "--check", "video.timeline", "--kind", "accept", "--note", quote2])
    qc.main(["override", str(rd), "--check", "video.gaze", "--kind", "accept", "--note", quote2, "--mention", "视线"])
    assert qc.gate_problems(rd, "video", set())[0] == []
