"""多视角独立审稿（Claude / Codex 通用，dota_yingxiong follow-up 263 / 266）。"""
import json
from pathlib import Path

import pytest

from tools import qc_review

qc = qc_review.qc          # qc_review 以 `import qc` 引入；打桩必须打在它手里的那个模块对象上
qc_pre = qc_review.qc_pre
scale_table = qc_review.scale_table

DRAMA_REG = """
[[check]]
id = "video.agency"
stage = "video"
kind = "review"
perspective = "character"
gate = true

[[check]]
id = "video.timeline"
stage = "video"
kind = "review"
layer = "spec"
gate = true
how = "逐行判"

[[check]]
id = "video.readability"
stage = "video"
kind = "review"
perspective = "audience"
gate = true

[[check]]
id = "video.no_text"
stage = "video"
kind = "machine"
gate = true
auto = false

[[check]]
id = "video.slowmo"
stage = "video"
kind = "machine"
gate = true
auto = true

[[check]]
id = "spec.agency"
stage = "spec"
kind = "review"
perspective = "character"
gate = true

[[check]]
id = "spec.scale_table"
stage = "spec"
kind = "machine"
gate = true
auto = true
"""


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for mod in (qc, qc_review, scale_table):
        monkeypatch.setattr(mod, "REPO", tmp_path)
    (tmp_path / "repo_reg.toml").write_text("", encoding="utf-8")
    monkeypatch.setattr(qc, "REGISTRY", tmp_path / "repo_reg.toml")
    monkeypatch.setattr(qc, "SPECS", tmp_path / "specs")
    drama = tmp_path / "ai_videos" / "demo"
    drama.mkdir(parents=True)
    (drama / "qc_checks.toml").write_text(DRAMA_REG, encoding="utf-8")
    chars = drama / "2_世界观人设" / "characters"
    for key, row in (("c1_Hero", "人类男性，约 1.8 m"), ("m1_Treant", "古树，身高约 1.9 m")):
        (chars / key).mkdir(parents=True)
        (chars / key / f"{key}.md").write_text(f"# {key[3:]} · {key}\n\n| 1 | 体型 / 年龄 / 种族 | {row} |\n", encoding="utf-8")
    sd = chars / "c1_Hero" / "skills" / "k1_Bolt"
    (sd / "资料包").mkdir(parents=True)
    (sd / "planning").mkdir()
    (sd / "k1_Bolt.md").write_text("# 卡\n\n## 技能视频 prompt\n\n```text\n时长：14秒\n0–2秒 起势，不出特效\n负面词：血腥\n```\n", encoding="utf-8")
    for n in ("start", "peak"):
        (sd / "planning" / f"k1_{n}.png").write_bytes(n.encode())
    base = "ai_videos/demo/2_世界观人设/characters/c1_Hero/skills/k1_Bolt/planning"
    refs = [{"key": "k1_start", "src": f"{base}/k1_start.png", "sha256": "s1"},
            {"key": "k1_peak", "src": f"{base}/k1_peak.png", "sha256": "s2"},
            {"key": "c1_Hero", "sha256": "s3"}, {"key": "m1_Treant", "sha256": "s4"}, {"key": "m1_death_corpse", "sha256": "s5"}]
    (sd / "资料包" / "manifest.json").write_text(json.dumps({"prompt_sha256": "p1", "refs": refs}), encoding="utf-8")
    rd = sd / "renders" / "20261026-130000_ab"
    rd.mkdir(parents=True)
    (rd / "k1_Bolt_clip.mp4").write_bytes(b"v")
    (rd / "sheet_4fps.jpg").write_bytes(b"jpg")
    return tmp_path


def sd_of(env: Path) -> Path:
    return env / "ai_videos" / "demo" / "2_世界观人设" / "characters" / "c1_Hero" / "skills" / "k1_Bolt"


def verdicts(path: Path) -> dict[str, str]:
    return {k: v["verdict"] for k, v in json.loads(path.read_text(encoding="utf-8"))["checks"].items()}


def test_reviewer_is_the_other_model_by_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    assert qc_review.pick("auto") == ["codex", "claude"]
    monkeypatch.delenv("CLAUDECODE")
    assert qc_review.pick("auto") == ["claude", "codex"]


def test_parse_tolerates_prose_and_drops_unknown_or_bad_rows():
    raw = '好的：\n[{"id":"video.timeline","verdict":"FAIL","evidence":"0.5 秒"},{"id":"x","verdict":"pass"},{"id":"video.agency","verdict":"maybe"}]'
    assert qc_review.parse(raw, {"video.timeline", "video.agency"}) == {"video.timeline": ("fail", "0.5 秒", "")}


def test_cast_comes_from_cards_and_excludes_death_refs(env: Path):
    assert qc_pre.cast(sd_of(env)) == ["c1_Hero", "m1_Treant"]


def test_one_reviewer_per_character_and_any_fail_fails(env: Path, monkeypatch: pytest.MonkeyPatch):
    prompts: dict[str, str] = {}
    models: list[str] = []

    def fake(who, prompt, images, work, timeout):
        models.append(who)
        if "你就是「Treant」" in prompt:
            prompts["treant"] = prompt
            return '[{"id":"video.agency","verdict":"fail","evidence":"第 6 格挨打不动"}]'
        if "你就是「Hero」" in prompt:
            return '[{"id":"video.agency","verdict":"pass","evidence":"一直盯着树人"}]'
        if "普通观众" in prompt:
            prompts["audience"] = prompt
            return '[{"id":"video.readability","verdict":"pass","evidence":"看得懂"}]'
        prompts["director"] = prompt
        return '[{"id":"video.timeline","verdict":"pass","evidence":"第 3 格"},{"id":"video.no_text","verdict":"pass","evidence":"无字"}]'
    monkeypatch.setattr(qc_review, "run_reviewer", fake)
    rd = sd_of(env) / "renders" / "20261026-130000_ab"
    qc_review.main([str(rd), "--reviewer", "codex"])
    v = verdicts(rd / "qc.json")
    assert v == {"video.agency": "fail", "video.timeline": "pass", "video.readability": "pass", "video.no_text": "pass"}
    ev = json.loads((rd / "qc.json").read_text(encoding="utf-8"))["checks"]["video.agency"]["evidence"]
    assert "[Treant·" in ev and "[Hero·" in ev                                         # 证据写明是哪个角色说的
    assert "起势" not in prompts["audience"] and "身高" not in prompts["audience"]       # 观众不看规格
    assert "Hero 1.8 m" in prompts["treant"] and "起势" in prompts["treant"]             # 角色知道彼此身高与规格
    assert set(models) == {"codex", "claude"}                                           # 视角轮流分给两个模型
    assert "video.slowmo" not in prompts["director"]                                    # 有工具的机检项不交审稿


def test_all_reviewers_failing_records_unreviewed_never_pass(env: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(qc_review, "run_reviewer", lambda *a: "")
    rd = sd_of(env) / "renders" / "20261026-130000_ab"
    qc_review.main([str(rd)])
    assert set(verdicts(rd / "qc.json").values()) == {"未审"}


def test_pre_review_binds_to_spec_and_refs(env: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(qc_review, "run_reviewer",
                        lambda who, prompt, images, work, timeout: '[{"id":"spec.agency","verdict":"pass","evidence":"第 1 拍就戒备"}]')
    sd = sd_of(env)
    qc_pre.main(["machine", str(sd)])
    qc_review.main([str(sd), "--pre"])
    assert verdicts(sd / "qc_pre.json") == {"spec.scale_table": "pass", "spec.agency": "pass"}
    assert qc_pre.gate(sd) == ([], [])
    m = json.loads((sd / "资料包" / "manifest.json").read_text(encoding="utf-8"))
    m["prompt_sha256"] = "p2"                                                          # 规格改了
    (sd / "资料包" / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    assert any("作废" in b for b in qc_pre.gate(sd)[0])


def test_missing_height_blocks_before_render(env: Path):
    card = env / "ai_videos" / "demo" / "2_世界观人设" / "characters" / "m1_Treant" / "m1_Treant.md"
    card.write_text("# Treant · m1_Treant\n\n| 1 | 体型 / 年龄 / 种族 | 古树，很高 |\n", encoding="utf-8")
    items = {cid: (v, ev) for cid, v, _, ev in qc_pre.machine(sd_of(env))}
    assert items["spec.scale_table"][0] == "fail" and "m1_Treant" in items["spec.scale_table"][1]


def test_dry_run_writes_nothing(env: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(qc_review, "run_reviewer", lambda *a: pytest.fail("dry-run 不该调审稿人"))
    rd = sd_of(env) / "renders" / "20261026-130000_ab"
    (rd / "sheet_4fps.jpg").unlink()
    qc_review.main([str(rd), "--dry-run"])
    qc_review.main([str(sd_of(env)), "--pre", "--dry-run"])
    assert sorted(p.name for p in rd.iterdir()) == ["k1_Bolt_clip.mp4"] and not (sd_of(env) / "qc_pre.json").exists()


@pytest.mark.parametrize("raw,expect", [("约 1.9 m", 1.9), ("肩高约 1.45 m，体长约 2.7 m", 1.45), ("身高约两米四", 2.4),
                                         ("约 12 厘米高", 0.12), ("身高与常人相当", 1.8), ("很高", None)])
def test_height_parsing(raw: str, expect: float | None):
    assert scale_table.parse(raw)[0] == expect


def test_parse_ignores_trailing_text_after_array():
    raw = '前言\n[{"id":"a","verdict":"pass","evidence":"x"}]\n补充说明 [见上] {"k": 1}]'
    assert qc_review.parse(raw, {"a"}) == {"a": ("pass", "x", "")}


def test_parse_cannot_judge_keeps_reason():
    raw = ('[{"id":"a","verdict":"审不了","reason":"材料缺","evidence":"没有峰值图"},'
           '{"id":"b","verdict":"审不了","reason":"随便","evidence":"脸太小"}]')
    assert qc_review.parse(raw, {"a", "b"}) == {"a": ("审不了", "没有峰值图", "材料缺"), "b": ("审不了", "脸太小", "看不清")}


def test_prompt_has_three_verdicts_layers_and_no_fail_when_unsure(env: Path, monkeypatch: pytest.MonkeyPatch):
    seen: list[str] = []

    def fake(who, prompt, images, work, timeout):
        seen.append(prompt)
        if "你就是" in prompt:
            return '[{"id":"video.agency","verdict":"审不了","reason":"看不清","evidence":"脸只有几个像素"}]'
        if "普通观众" in prompt:
            return '[{"id":"video.readability","verdict":"pass","evidence":"看得懂"}]'
        return '[{"id":"video.timeline","verdict":"pass","evidence":"偏了 1 秒"},{"id":"video.no_text","verdict":"pass","evidence":"无字"}]'
    monkeypatch.setattr(qc_review, "run_reviewer", fake)
    rd = sd_of(env) / "renders" / "20261026-130000_ab"
    (rd / "prompt.txt").write_text("时长：14秒\n0–3秒 提交时的旧规格，蓄力\n", encoding="utf-8")
    qc_review.main([str(rd)])
    assert all("拿不准就判 fail" not in x and "审不了" in x for x in seen)
    director = next(x for x in seen if "导演" in x)
    assert "【对照规格】video.timeline" in director and "【通用】video.no_text" in director
    assert "提交时的旧规格" in director and "起势，不出特效" not in director          # 对照的是这一条提交时的 prompt，不是卡上现在的
    row = json.loads((rd / "qc.json").read_text(encoding="utf-8"))["checks"]["video.agency"]
    assert row["verdict"] == "审不了" and row["reason"] == "看不清" and row["rule"] == qc.REVIEW_RULE
