import hashlib
import json
import os
import shutil
import time
from pathlib import Path

import pytest

from tools import review_run as rr


REAL_ROSTER = rr.ROSTER


@pytest.fixture(autouse=True)
def dual_roster(request, tmp_path_factory, monkeypatch):
    """双审机制（对比、裁决、Codex 代登记）仍保留在工具里：这些用例用一份「每类 Claude＋Codex 两位」的名册副本跑。
    正式名册 2026-11-14 起改为 Claude 单审（follow-up 065），单审用例标 @pytest.mark.single_review 用真名册。"""
    if request.node.get_closest_marker("single_review"):
        return
    r = json.loads(REAL_ROSTER.read_text(encoding="utf-8"))
    for law in r["laws"].values():
        law["reviewers"] = [{"slot": "a", "runner": "claude", "model": "claude-opus-5-5"}, {"slot": "b", "runner": "codex", "model": "gpt-6.1-sol"}]
    r["laws"]["native_ear"]["prefer_model"] = "codex"
    f = tmp_path_factory.mktemp("roster") / "review_roster.json"
    f.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(rr, "ROSTER", f)


def make_episode(tmp: Path) -> Path:
    drama = tmp / "demo"; ep = drama / "episodes" / "ep01"
    ep.mkdir(parents=True)
    (drama / "bible.md").write_text("# bible", encoding="utf-8")
    (drama / "README.md").write_text("# Demo Drama\n", encoding="utf-8")
    scenes = [{"id": f"s{i}", "location": "街", "time": "晨", "purpose": "p", "shots": [{"id": "st1", "duration": 8, "cast": ["c1"]}]}
              for i in range(1, 6)]
    (ep / "filming.json").write_text(json.dumps({"content": {"scenes": scenes}}), encoding="utf-8")
    (ep / "story.json").write_text("{}", encoding="utf-8")
    return ep


def runs(ep: Path) -> list[Path]:
    return sorted(p.parent for p in (ep.parent.parent / "reviews").glob("*/checklist.json"))


def load(run: Path) -> dict:
    return json.loads((run / "checklist.json").read_text(encoding="utf-8"))


HEAD = "| 镜头 | 原条秒数 | 法则·子类 | 严重度 | 本该哪关抓到 | 证据 | 建议改动 |\n|---|---|---|---|---|---|---|\n"
ROWS = HEAD + "| s1_st1 | 1 | 物理 | 重出 | ② | 第3格 | 改（便宜） |\n| s2_st1 | 2 | 物理 | 记录 | ④ | 第4格 | 改 |"


def report(item: dict, clean: bool = False, bad: str = "") -> str:
    """v2 报告：必查项 ✓/✗ ＋ 问题表。"""
    must = "\n".join(f"- {m['id']} {'✗ 有问题' if m['id'] == bad else '✓'}" for m in item["must"])
    body = "结论：无问题\n- 逐镜核过" if clean else ROWS
    return f"## 必查项\n{must}\n\n{body}\n"


def report5(item: dict, scores: dict | None = None, clean: bool = False, rows: str = "", r: bool = False) -> str:
    """v5 报告：评分表（默认每维 3 分＋证据）＋ 问题表 ＋ 整体观察。"""
    scores = scores or {}
    lines = []
    for d in item["rubric"]:
        s = scores.get(d["id"], 3)
        lines.append(f"- {d['id']} {s} " + ("原因：没有首帧可看" if s == 0 else f"证据：s1_st1 第3格逐格核过 {d['name']}"))
    if r:
        lines.append("- R 3 证据：上一轮问题逐条复核，都已改好")
    body = "结论：无问题" if clean else (rows or ROWS)
    return "## 评分表\n" + "\n".join(lines) + f"\n\n{body}\n\n## 整体观察\n- 还行\n"


def item_of(run: Path, iid: str) -> dict:
    return next(x for x in load(run)["items"] if x["id"] == iid)


def tick5(run: Path, tmp: Path, it: dict, slot: str, text: str) -> int:
    p = tmp / f"{run.name}_{it['id']}__{slot}.md"
    p.write_text(text, encoding="utf-8")
    return rr.main(["tick", str(run), it["id"], "--slot", slot, "--report", str(p), "--by", f"m{slot}/{it['id']}__{slot}"])


def judge(run: Path, tmp: Path, iid: str, rulings: dict | None = None, rows: str = "", drop: str = "", reason: str = "") -> int:
    it = item_of(run, iid)
    lines = [f"- {d} {(rulings or {}).get(d, 3)} 理由：{reason or '回到首帧第3格核过，证据成立'}" for d in it["judge"]["dims"] if d != drop]
    p = tmp / f"{run.name}_{iid}__judge.md"
    p.write_text("## 裁决\n" + "\n".join(lines) + "\n\n" + rows + "\n", encoding="utf-8")
    return rr.main(["adjudicate", str(run), iid, "--report", str(p), "--by", f"mj/{iid}__judge"])


def tick_all(run: Path, tmp: Path, clean: bool = False, skip: tuple = ()) -> None:
    loop = load(run)["loop"]
    for it in load(run)["items"]:
        if it["id"] in skip:
            continue
        for slot in ("a", "b"):
            assert tick5(run, tmp, it, slot, report5(it, clean=clean, r=loop > 1)) == 0
        if item_of(run, it["id"])["status"] == "adjudicating":
            assert judge(run, tmp, it["id"]) == 0
        assert item_of(run, it["id"])["status"] == "done"


def to_v2(run: Path) -> None:
    """把新开的审查单改写成 v2 格式（每项一位审稿人、没有 slots），模拟进行中的旧单。"""
    d = load(run); d["version"] = 2
    for k in ("scoring", "adjudicator"):
        d.pop(k, None)
    for it in d["items"]:
        for k in ("slots", "rubric", "method", "what", "problem", "model_why", "ticked_by", "ticked_by_list", "findings", "rows"):
            it.pop(k, None)
        it["report"] = f"reports/{it['id']}.md"
    (run / "checklist.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


def test_new_saves_under_the_drama_with_must_checks(tmp_path):
    ep = make_episode(tmp_path)
    assert rr.main(["new", str(ep), "--stage", "filming", "--known", "旧发色"]) == 0
    run, = runs(ep)
    assert run.parent == tmp_path / "demo" / "reviews" and run.name.startswith("ep01_") and run.name.endswith("_filming_r1")
    data = load(run)
    ids = [x["id"] for x in data["items"]]
    assert ids == ["physics_A", "physics_B", "physics_C", "character_A", "character_B", "continuity", "era", "prompt_text", "role_c1"]   # 角色立场：每个出场人物一位（follow-up 063）
    assert data["items"][0]["scope"] == ["s1", "s2"] and data["loop"] == 1 and data["state"] == "进行中"
    assert [m["id"] for m in data["items"][0]["must"]][:2] == ["P1", "P2"]
    task = (run / "items/physics_A.md").read_text(encoding="utf-8")
    assert "**P1**" in task and "tick" in task
    assert (run / "materials/shots/s1_st1/spec.md").is_file()
    assert data["version"] == 5 and data["adjudicator"]["model"] == "claude-opus-5-5"


def test_new_v5_gives_each_item_a_claude_and_a_codex_slot_with_their_own_task_file(tmp_path):
    """v5（用户 2026-11-08）：每项一位合适的 Claude 模型＋一位合适的 Codex 模型双审，各有任务书（是什么、rubric、评分规则、审法、范围、打勾命令）。"""
    ep = make_episode(tmp_path)
    assert rr.main(["new", str(ep), "--stage", "filming"]) == 0
    run, = runs(ep)
    it = item_of(run, "physics_A")
    a, b = it["slots"]["a"], it["slots"]["b"]
    assert (a["runner"], a["model"], b["runner"], b["model"]) == ("claude", "claude-opus-5-5", "codex", "gpt-6.1-sol")
    assert a["report"] == "reports/physics_A__a.md" and b["prompt"] == "items/physics_A__b.md" and it["report"] == "reconcile/physics_A.md"
    assert it["status"] == "pending" and it["findings"]["重出"] == 0 and [r["id"] for r in it["rubric"]][:2] == ["P1", "P2"]
    ta = (run / a["prompt"]).read_text(encoding="utf-8"); tb = (run / b["prompt"]).read_text(encoding="utf-8")
    for task in (ta, tb):
        assert "这一类是什么" in task and "生成模型最常犯" in task and "**P8** 首帧 = 第 0 秒" in task
        assert "0–3" in task and "证据规则" in task and "画一张「手与道具」表" in task and "s1、s2" in task and "materials/index.md" in task
    assert "--slot a" in ta and '--by "claude-opus-5-5/physics_A__a"' in ta and "REPORT WRITTEN" not in ta
    assert "--slot b" in tb and '--by "gpt-6.1-sol/physics_A__b"' in tb and rr.PY_FALLBACK in tb
    assert "REPORT WRITTEN:" in tb and "不要运行 tick" in tb
    brief = (run / "BRIEF.md").read_text(encoding="utf-8")
    assert "## 评分表" in brief and "--attest-log" in brief


def test_tick_requires_reviewer_table_and_every_must(tmp_path):
    """v5 下同样的规矩：报告要有、问题表要有、每维都要写、作者不能代勾；另外要用 --slot 指明哪一位。"""
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    it = item_of(run, "era")
    rep = tmp_path / "era.md"

    def t(by="m/era__a", slot="a"):
        return rr.main(["tick", str(run), "era", "--slot", slot, "--report", str(rep), "--by", by])
    with pytest.raises(SystemExit, match="报告不存在"):
        t()
    rep.write_text("看过了，挺好", encoding="utf-8")
    with pytest.raises(SystemExit, match="问题表"):
        t()
    rep.write_text("\n".join(ln for ln in report5(it).splitlines() if not ln.startswith("- E3 ")), encoding="utf-8")
    with pytest.raises(SystemExit, match="E3"):
        t()
    rep.write_text(report5(it, {"E2": 1}), encoding="utf-8")
    for who in ("Claude Code", "作者", "m/physics_A__a", "m/era", "m/era__b"):
        with pytest.raises(SystemExit, match="作者"):
            t(who)
    with pytest.raises(SystemExit, match="--slot"):
        rr.main(["tick", str(run), "era", "--report", str(rep), "--by", "m/era__a"])
    assert t() == 0
    got = item_of(run, "era")
    a = got["slots"]["a"]
    assert a["status"] == "done" and a["rows"] == 2 and a["scores"]["E2"]["score"] == 1 and a["scores"]["E1"]["score"] == 3
    assert got["status"] == "pending" and got["ticked_by"] == "m/era__a" and got["ticked_by_list"] == ["m/era__a"]


def test_gate_needs_every_box_and_failed_blocks(tmp_path):
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    assert rr.main(["gate", str(run)]) == 1
    with pytest.raises(SystemExit, match="--slot"):
        rr.main(["fail", str(run), "era", "--note", "网络 403"])
    rr.main(["fail", str(run), "era", "--slot", "b", "--note", "网络 403"])
    era = item_of(run, "era")
    assert era["status"] == "failed" and era["slots"]["b"]["status"] == "failed" and era["slots"]["a"]["status"] == "pending"
    assert rr.main(["gate", str(run)]) == 1
    tick_all(run, tmp_path)
    assert "note" not in item_of(run, "era")["slots"]["b"]
    assert rr.main(["gate", str(run)]) == 0


def test_loop_needs_changes_rechecks_previous_and_stops_at_three(tmp_path):
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "pregen"]); r1, = runs(ep)
    with pytest.raises(SystemExit, match="还没审完"):
        rr.main(["new", str(ep), "--after", str(r1), "--changes", "x"])
    tick_all(r1, tmp_path, clean=True)
    with pytest.raises(SystemExit, match="--changes"):
        rr.main(["new", str(ep), "--after", str(r1)])
    assert rr.main(["new", str(ep), "--after", str(r1), "--changes", "改了 s1_st1 的分镜"]) == 0
    r2 = runs(ep)[-1]; d2 = load(r2)
    assert d2["loop"] == 2 and d2["chain"] == load(r1)["id"] and d2["stage"] == "pregen"
    assert d2["items"][0]["must"][-1]["id"] == "R" and "改了 s1_st1 的分镜" in (r2 / "changes.md").read_text(encoding="utf-8")
    assert "**R**" in (r2 / "items/physics_A__a.md").read_text(encoding="utf-8")
    assert load(r1)["child"].endswith(r2.name)
    era = item_of(r2, "era")
    with pytest.raises(SystemExit, match="previous.md"):
        tick5(r2, tmp_path, era, "a", report5(era, clean=True))           # 第 2 轮缺 R 一行
    tick_all(r2, tmp_path, clean=True)
    assert item_of(r2, "era")["must_result"]["R"] == "✓"
    rr.main(["new", str(ep), "--after", str(r2), "--changes", "又改了"]); r3 = runs(ep)[-1]
    tick_all(r3, tmp_path, clean=True)
    with pytest.raises(SystemExit, match="3 轮"):
        rr.main(["new", str(ep), "--after", str(r3), "--changes", "再改"])


def test_conclude_confirm_and_submit_gate(tmp_path):
    ep = make_episode(tmp_path)
    ok, msg = rr.can_submit(ep, ["ep1_s1_st1"])
    assert not ok and "pregen" in msg
    rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1,s2"]); run, = runs(ep)
    with pytest.raises(SystemExit, match="收轮"):
        rr.main(["conclude", str(run)])
    tick_all(run, tmp_path)
    with pytest.raises(SystemExit, match="已收轮"):
        rr.main(["confirm", str(run), "--quote", "好的出吧"])
    assert rr.main(["conclude", str(run)]) == 0
    d = load(run)
    assert d["state"] == "已收轮" and (run / "结果.md").is_file()          # 每轮收轮不等用户 review（用户 2026-11-08）
    assert d["verdict"]["result"] == "不可出片" and d["verdict"]["reasons"]   # 默认 ROWS 有重出 → 严重问题未处理
    res = (run / "结果.md").read_text(encoding="utf-8")
    assert "各类评分" in res and "| P1 手数 | 3 | 3 | 3 |" in res and "claude-opus-5-5" in res and "gpt-6.1-sol" in res and "抽查" in res
    assert "问题清单" in res and (run / "issues.json").is_file()
    assert not rr.can_submit(ep, ["ep1_s1_st1"])[0]          # concluded but not yet confirmed by the user
    assert rr.main(["confirm", str(run), "--quote", "好的，出第一场"]) == 0
    assert rr.can_submit(ep, ["ep1_s1_st1", "ep1_s2_g1"])[0]
    assert not rr.can_submit(ep, ["ep1_s3_st1"])[0]          # s3 was not in this review
    (ep / "filming.json").write_text(json.dumps({"content": {"scenes": []}}), encoding="utf-8")
    assert not rr.can_submit(ep, ["ep1_s1_st1"])[0]          # materials changed after confirmation


def test_changed_materials_void_the_checklist(tmp_path):
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    it = load(run)["items"][-1]
    (ep / "filming.json").write_text(json.dumps({"content": {"scenes": []}}), encoding="utf-8")
    rep = tmp_path / "r.md"; rep.write_text(report5(it), encoding="utf-8")
    with pytest.raises(SystemExit, match="作废"):
        rr.main(["tick", str(run), it["id"], "--slot", "a", "--report", str(rep), "--by", f"m/{it['id']}__a"])
    assert rr.main(["gate", str(run)]) == 1
    assert load(run)["state"] == "已作废"


def test_dialogue_has_a_blind_native_ear_reviewer_on_another_model(tmp_path):
    """follow-up 036：每个大类至少一种审法；台词另有母语听感盲审，只读 lines.md，建议换模型（v5 下 b 位就是 codex）。"""
    ep = make_episode(tmp_path)
    shots = json.loads((ep / "filming.json").read_text(encoding="utf-8"))
    shots["content"]["scenes"][0]["shots"][0].update(action="她转身", dialogue="Riley：We'll still be reading it.")
    (ep / "filming.json").write_text(json.dumps(shots), encoding="utf-8")
    assert rr.main(["new", str(ep), "--stage", "pregen"]) == 0
    run, = runs(ep)
    items = {x["id"]: x for x in load(run)["items"]}
    ear = items["native_ear"]
    assert ear["blind"] and ear["prefer_model"] == "codex" and [m["id"] for m in ear["must"]][0] == "N1"
    assert ear["slots"]["b"]["runner"] == "codex" and ear["slots"]["a"]["runner"] == "claude"
    task = (run / "items/native_ear__b.md").read_text(encoding="utf-8")
    assert "lines.md" in task and "codex exec" in task and "英语母语观众，盲审" in task and "你就是这一位" in task
    assert "英语母语观众，盲审" in (run / "items/native_ear__a.md").read_text(encoding="utf-8")
    assert "We'll still be reading it." in (run / "materials/lines.md").read_text(encoding="utf-8")
    roster = json.loads(rr.ROSTER.read_text(encoding="utf-8"))
    assert all(law.get("mechanisms") for law in roster["laws"].values())


def test_run_for_one_scene_is_not_voided_by_edits_to_another_scene(tmp_path):
    """follow-up 036：一场一场走出片前循环；只改别的场不作废本单，改本场就作废。"""
    ep = make_episode(tmp_path)
    assert rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1"]) == 0
    run, = runs(ep)
    doc = json.loads((ep / "filming.json").read_text(encoding="utf-8"))
    doc["content"]["scenes"][1]["shots"][0]["action"] = "别的场改了"
    (ep / "filming.json").write_text(json.dumps(doc), encoding="utf-8")
    assert rr.stale_files(load(run)) == []
    doc["content"]["scenes"][0]["shots"][0]["action"] = "本场改了"
    (ep / "filming.json").write_text(json.dumps(doc), encoding="utf-8")
    assert any(k.endswith("filming.json#s1") for k in rr.stale_files(load(run)))


def test_must_id_r_is_not_matched_inside_riley():
    """follow-up 036：必查项 R 不能配到含「Riley」的 C1 行。"""
    text = "## 必查项\n- C1 ✗ Riley 的视线不对\n- R ✓ 上一轮都改好了\n\n| 镜头 | 严重度 |\n"
    got, missing = rr.parse_must(text, [{"id": "C1", "text": ""}, {"id": "R", "text": ""}])
    assert got == {"C1": "✗", "R": "✓"} and missing == []


def test_other_tables_in_a_report_are_not_counted_as_findings():
    """follow-up 036：报告里附的道具状态表不算问题行。"""
    text = ("| 镜头 | 严重度 |\n|---|---|\n| s1_st1 | 记录 |\n\n道具状态：\n\n| 镜头 | 进场 | 出场 |\n|---|---|---|\n"
            "| s1_st1 | 9 枚 | 9 枚 |\n| s1_st2 | 9 枚 | 9 枚 |\n")
    counts, rows, _ = rr.parse_report(text)
    assert rows == 1 and counts["记录"] == 1
    assert len(rr.parse_rows(text)) == 1


def test_dispatch_records_which_agent_reviewed_with_what_instructions(tmp_path):
    """follow-up 036：审查单记下每一步由哪个独立 agent 审、用的什么指令与依据，并能补登它的回复；v5 记到各自的审稿位。"""
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    prompt = tmp_path / "p.md"; prompt.write_text("Read the task file and do it.", encoding="utf-8")
    reply = tmp_path / "r.md"; reply.write_text("审完，已打勾。", encoding="utf-8")
    with pytest.raises(SystemExit, match="--slot"):
        rr.main(["dispatch", str(run), "era", "--runner", "x", "--model", "y", "--prompt-file", str(prompt)])
    with pytest.raises(SystemExit, match="裁决"):
        rr.main(["dispatch", str(run), "era", "--slot", "judge", "--runner", "x", "--model", "y", "--prompt-file", str(prompt)])
    assert rr.main(["dispatch", str(run), "era", "--slot", "a", "--runner", "Claude Code 子代理（general-purpose）", "--model", "claude-opus-5-5",
                    "--prompt-file", str(prompt)]) == 0
    assert rr.main(["dispatch", str(run), "era", "--slot", "a", "--reply-file", str(reply)]) == 0
    era = item_of(run, "era")
    rec, = era["slots"]["a"]["agents"]
    assert rec["model"] == "claude-opus-5-5" and rec["reply"] == "审完，已打勾。" and any("review_roster" in s for s in rec["skills"])
    assert any("items/era__a.md" in s for s in rec["skills"]) and rec["prompt"] == "agents/era__a_1.md"
    assert (run / rec["prompt"]).read_text(encoding="utf-8").startswith("Read the task file")
    mirror, = era["agents"]
    assert mirror["slot"] == "a" and mirror["reply"] == "审完，已打勾。" and era["slots"]["b"]["agents"] == []


# ---------------------------------------------------------------- v5：rubric、代登记、对比、裁决、问题清单、方案


def test_rubric_validation(tmp_path):
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    it = item_of(run, "era")
    rep = tmp_path / "era.md"

    def t(text):
        rep.write_text(text, encoding="utf-8")
        return rr.main(["tick", str(run), "era", "--slot", "a", "--report", str(rep), "--by", "m/era__a"])

    def swap(line_id, new):
        return "\n".join(new if ln.startswith(f"- {line_id} ") else ln for ln in report5(it).splitlines())
    with pytest.raises(SystemExit, match="缺这些维度：E7"):
        t("\n".join(ln for ln in report5(it).splitlines() if not ln.startswith("- E7 ")))
    with pytest.raises(SystemExit, match="E2 打了 3 分但没有证据"):
        t(swap("E2", "- E2 3"))
    with pytest.raises(SystemExit, match="E2 打了 2 分但没有证据"):
        t(swap("E2", "- E2 2 证据：好"))
    with pytest.raises(SystemExit, match="E4 打 1 分"):
        t(report5(it, {"E4": 1}, clean=True))
    with pytest.raises(SystemExit, match="E5 打 0 分"):
        t(swap("E5", "- E5 0"))
    with pytest.raises(SystemExit, match="不在 0–3"):
        t(swap("E6", "- E6 4 证据：s1_st1 第3格逐格核过"))
    assert t(swap("E1", "- **E1**：3分 证据: s1_st1 首帧放大核过器物")) == 0
    a = item_of(run, "era")["slots"]["a"]
    assert a["scores"]["E1"] == {"score": 3, "evidence": "s1_st1 首帧放大核过器物"}


def test_attested_tick_for_codex_slot(tmp_path):
    """Codex 沙箱跑不了 python：调用方凭 codex exec 日志代为登记；只限 Codex 位，日志要含报告路径且晚于派单。"""
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    it = item_of(run, "era")
    rep = tmp_path / "era_b.md"; rep.write_text(report5(it), encoding="utf-8")
    rep_a = tmp_path / "era_a.md"; rep_a.write_text(report5(it), encoding="utf-8")
    log = tmp_path / "codex.log"
    base = ["tick", str(run), "era", "--slot", "b", "--report", str(rep), "--by", "gpt-6-astra/era__b", "--attest-log", str(log)]
    with pytest.raises(SystemExit, match="只用于 Codex"):
        rr.main(["tick", str(run), "era", "--slot", "a", "--report", str(rep_a), "--by", "m/era__a", "--attest-log", str(log)])
    with pytest.raises(SystemExit, match="运行日志不存在"):
        rr.main(base)
    log.write_text("codex did some stuff\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="找不到报告"):
        rr.main(base)
    log.write_text(f"…\nREPORT WRITTEN: {rep}\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="派单"):
        rr.main(base)
    prompt = tmp_path / "p.md"; prompt.write_text("run the task", encoding="utf-8")
    rr.main(["dispatch", str(run), "era", "--slot", "b", "--runner", "codex exec", "--model", "gpt-6-astra", "--prompt-file", str(prompt),
             "--at", "2999-01-01T00:00:00"])
    with pytest.raises(SystemExit, match="早于派单"):
        rr.main(base)
    rr.main(["dispatch", str(run), "era", "--slot", "b", "--runner", "codex exec", "--model", "gpt-6-astra", "--prompt-file", str(prompt),
             "--at", "2020-01-01T00:00:00"])
    assert rr.main(base) == 0
    b = item_of(run, "era")["slots"]["b"]
    assert b["status"] == "done" and b["attested"]["log"].endswith("codex.log") and b["by"] == "gpt-6-astra/era__b"
    assert (run / b["attested"]["copy"].split(run.name + "/")[-1]).read_text(encoding="utf-8").startswith("…")
    assert any(e["event"].startswith("代为登记") and e.get("slot") == "b" for e in load(run)["log"])


def test_attested_tick_on_a_v2_item_needs_a_codex_dispatch(tmp_path):
    """v2 单（进行中的旧单）也可凭 Codex 日志代登记：最近一次派单的 runner 必须是 Codex。"""
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    to_v2(run)
    it = item_of(run, "era")
    rep = run / "reports" / "era.md"; rep.write_text(report(it), encoding="utf-8")
    log = tmp_path / "codex.log"; log.write_text(f"REPORT WRITTEN: {rep}\n", encoding="utf-8")
    prompt = tmp_path / "p.md"; prompt.write_text("run", encoding="utf-8")
    cmd = ["tick", str(run), "era", "--report", str(rep), "--by", "codex/era", "--attest-log", str(log)]
    rr.main(["dispatch", str(run), "era", "--runner", "Claude Code 子代理", "--model", "claude-opus-5-5", "--prompt-file", str(prompt),
             "--at", "2020-01-01T00:00:00"])
    with pytest.raises(SystemExit, match="Codex"):
        rr.main(cmd)
    rr.main(["dispatch", str(run), "era", "--runner", "Codex exec（workspace-write）", "--model", "gpt-6-astra", "--prompt-file", str(prompt),
             "--at", "2020-01-01T00:00:01"])
    assert rr.main(cmd) == 0
    got = item_of(run, "era")
    assert got["status"] == "done" and got["attested"]["log"].endswith("codex.log") and "slots" not in got
    assert load(run)["log"][-1]["event"].startswith("代为登记")


def test_v2_run_still_works(tmp_path):
    """进行中的 v2 单（没有 slots）：照旧 tick / gate / conclude / 开下一轮，不受 v5 影响。"""
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "pregen"]); r1, = runs(ep)
    to_v2(r1)
    for it in load(r1)["items"]:
        p = tmp_path / f"v2_{it['id']}.md"; p.write_text(report(it, bad="P2" if it["law"] == "physics" else ""), encoding="utf-8")
        if it["id"] == "era":
            with pytest.raises(SystemExit, match="v2"):
                rr.main(["tick", str(r1), "era", "--slot", "a", "--report", str(p), "--by", "m/era"])
        assert rr.main(["tick", str(r1), it["id"], "--report", str(p), "--by", f"m/{it['id']}"]) == 0
    phys = item_of(r1, "physics_A")
    assert phys["status"] == "done" and phys["must_result"]["P2"] == "✗" and phys["rows"] == 2 and isinstance(phys["ticked_by"], str)
    assert rr.main(["gate", str(r1)]) == 0 and rr.main(["status", str(r1)]) == 0
    with pytest.raises(SystemExit, match="--changes"):
        rr.main(["new", str(ep), "--after", str(r1)])
    assert rr.main(["new", str(ep), "--after", str(r1), "--changes", "改了 s1_st1"]) == 0
    r2 = runs(ep)[-1]
    assert load(r2)["version"] == 5 and "s1_st1" in (r2 / "previous.md").read_text(encoding="utf-8")
    assert rr.main(["conclude", str(r1)]) == 0 and "仍未解决" in (r1 / "结果.md").read_text(encoding="utf-8")


def test_reconcile_disagreement_goes_to_adjudication(tmp_path, capsys):
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    it = item_of(run, "era")
    assert tick5(run, tmp_path, it, "a", report5(it, {"E1": 1, "E2": 2})) == 0
    assert item_of(run, "era")["status"] == "pending"
    assert tick5(run, tmp_path, it, "b", report5(it, clean=True)) == 0
    x = item_of(run, "era")
    assert x["status"] == "adjudicating" and x["disputes"] == ["E1"] and x["scores"]["E1"]["verdict"] == "分歧"
    assert x["scores"]["E2"]["agreed"] == 2                     # 差 1 且都 ≥2：不算分歧，取低分
    assert len(x["audits"]) == 2 and set(x["audits"]) <= {"E2", "E3", "E4", "E5", "E6", "E7"}
    assert x["judge"]["model"] == "claude-opus-5-5" and x["judge"]["dims"] == ["E1", *x["audits"]]
    rec = (run / "reconcile/era.md").read_text(encoding="utf-8")
    assert "| E1 器物 | 1 |" in rec and "分歧" in rec and "抽查" in rec and "待裁决" in rec
    jt = (run / "items/era__judge.md").read_text(encoding="utf-8")
    assert "**E1**（分歧）" in jt and "adjudicate" in jt and "reports/era__a.md" in jt.replace("\\", "/") and "era__judge" in jt
    assert rr.main(["gate", str(run)]) == 1 and load(run)["state"] == "进行中"
    capsys.readouterr()
    rr.main(["status", str(run)])
    out = capsys.readouterr().out
    assert "E1 1/3→?（分歧）" in out and "a✓" in out and "b✓" in out


def test_agreement_is_still_audited_and_picks_are_deterministic(tmp_path):
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    it = item_of(run, "continuity")
    for slot in ("a", "b"):
        assert tick5(run, tmp_path, it, slot, report5(it, clean=True)) == 0
    x = item_of(run, "continuity")
    assert x["status"] == "adjudicating" and x["disputes"] == [] and len(x["audits"]) == 2
    assert x["audits"] == rr.audit_pick(load(run)["id"], "continuity", [r["id"] for r in x["rubric"]])
    assert rr.audit_pick("r", "i", list("ABCDEFG")) == rr.audit_pick("r", "i", list("ABCDEFG"))
    assert rr.audit_pick("r", "i", ["A"]) == ["A"]
    era = item_of(run, "era")                                  # 两人都打 1：没有分歧、没有可抽查维度 → 直接完成
    ones = {r["id"]: 1 for r in era["rubric"]}
    for slot in ("a", "b"):
        assert tick5(run, tmp_path, era, slot, report5(era, ones)) == 0
    e = item_of(run, "era")
    assert e["status"] == "done" and set(e["final_scores"].values()) == {1} and "judge" not in e


def test_adjudicate_validation_and_final_scores(tmp_path):
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    it = item_of(run, "era")
    tick5(run, tmp_path, it, "a", report5(it, {"E1": 1, "E2": 2}))
    tick5(run, tmp_path, it, "b", report5(it, {"E2": 3}))      # 同一张 ROWS：两份完全相同的行要去重
    with pytest.raises(SystemExit, match="E1"):
        judge(run, tmp_path, "era", drop="E1")
    with pytest.raises(SystemExit, match="理由太短"):
        judge(run, tmp_path, "era", reason="对")
    p = tmp_path / "j.md"; p.write_text("## 裁决\n- E1 1 理由：s1_st1 第3格确有问题", encoding="utf-8")
    with pytest.raises(SystemExit, match="作者"):
        rr.main(["adjudicate", str(run), "era", "--report", str(p), "--by", "mj/era__a"])
    extra = HEAD + "| s5_st1 | 5 | 时代·其他 | 存疑 | ③ | 第2格看不清 | 核实（便宜） |"
    assert judge(run, tmp_path, "era", {"E1": 1}, rows=extra) == 0
    x = item_of(run, "era")
    assert x["status"] == "done" and x["final_scores"]["E1"] == 1 and x["scores"]["E1"]["judge_reason"]
    assert x["final_scores"]["E2"] == (3 if "E2" in x["audits"] else 2)
    assert x["rows"] == 3 and x["findings"] == {"重出": 1, "可剪": 0, "记录": 1, "存疑": 1} and x["must_result"]["E1"] == "✗"
    assert "| 1 |" in (run / "reconcile/era.md").read_text(encoding="utf-8") and x["judge"]["by"] == "mj/era__judge"
    with pytest.raises(SystemExit, match="不需要裁决"):
        judge(run, tmp_path, "era")
    assert rr.main(["gate", str(run)]) == 1                     # 其他项还没审


ERA_A = HEAD + ("| s1_st1 | 1 | 时代·E2 | 可剪 | ② | 第3格 有百叶窗 | 改场景图（便宜） |\n"
                "| s3_st1 | 3 | 时代·招牌 | 重出 | ③ | 招牌上有字母 | 重出（要积分） |\n"
                "| s2_st1 | 2 | 时代·其他 | 存疑 | ④ | 第4格看不清 | 放大核实 |\n"
                "| s4_st1 | 4 | 时代·杂项 | 记录 | ④ | 小瑕疵 | 不改 |")
ERA_B = HEAD + ("| s1_st1 | 1 | 时代·E2 | 可剪 | ② | 第3格 百叶窗 | 改场景图（便宜） |\n"
                "| s3_st1 | 3 | 时代·招牌 | 重出 | ③ | 招牌有字 | 重出（要积分） |")


def era_issue_run(tmp_path: Path) -> tuple[Path, Path]:
    """其余各项干净；era：E1 0/1（0 分→严重）、E2 1/1（主要）、E3 1/3 分歧裁 1（名册标 critical→严重），外加重出 / 存疑 / 记录行。"""
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "filming"]); run, = runs(ep)
    d = load(run)
    era = next(x for x in d["items"] if x["id"] == "era")
    next(r for r in era["rubric"] if r["id"] == "E3")["critical"] = True
    (run / "checklist.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    tick_all(run, tmp_path, clean=True, skip=("era",))
    era = item_of(run, "era")
    assert tick5(run, tmp_path, era, "a", report5(era, {"E1": 0, "E2": 1, "E3": 1}, rows=ERA_A)) == 0
    assert tick5(run, tmp_path, era, "b", report5(era, {"E1": 1, "E2": 1}, rows=ERA_B)) == 0
    assert item_of(run, "era")["disputes"] == ["E3"]
    assert judge(run, tmp_path, "era", {"E3": 1}) == 0
    return ep, run


def test_issues_derivation_classification_and_dedupe(tmp_path):
    ep, run = era_issue_run(tmp_path)
    assert rr.main(["issues", str(run)]) == 0
    issues = json.loads((run / "issues.json").read_text(encoding="utf-8"))["issues"]
    by = {i["dimension"].split()[0] if i["key"].startswith("dim:") else i["shots"][0]: i for i in issues}
    assert sorted(by) == ["E1", "E2", "E3", "s2_st1", "s3_st1", "s4_st1"]
    assert [i["id"] for i in issues] == ["I1", "I2", "I3", "I4", "I5", "I6"] and issues[0]["level"] == "critical"
    assert by["E1"]["level"] == "critical" and by["E1"]["scores"] == {"a": 0, "b": 1, "final": 0}
    assert by["E2"]["level"] == "major" and by["E2"]["shots"] == ["s1_st1"] and by["E2"]["cost"] == "便宜"
    assert any("有百叶窗" in e for e in by["E2"]["evidence"]) and any(e.startswith("b（1 分）") for e in by["E2"]["evidence"])
    assert by["E3"]["level"] == "critical" and any(e.startswith("裁决（1 分）") for e in by["E3"]["evidence"])
    s3 = by["s3_st1"]                                          # a、b 两行证据不同，但同镜头＋同子类：去重成一条
    assert s3["level"] == "critical" and s3["cost"] == "要积分" and len(s3["rows"]) == 2
    assert {"ma/era__a", "mb/era__b"} <= set(s3["sources"]) and s3["fix"] == "重出（要积分）" and s3["status"] == "open"
    assert by["s2_st1"]["level"] == "verify" and by["s4_st1"]["level"] == "minor"
    md = (run / "issues.md").read_text(encoding="utf-8")
    assert "| I1 | 严重 |" in md and "要积分" in md
    assert rr.main(["fix", str(run), "I1", "--solution", "重画首帧", "--status", "planned"]) == 0
    assert rr.main(["issues", str(run)]) == 0                  # 重推不丢方案与编号
    again = json.loads((run / "issues.json").read_text(encoding="utf-8"))["issues"]
    assert [i["id"] for i in again] == [i["id"] for i in issues] and again[0]["status"] == "planned" and again[0]["solution"] == "重画首帧"


def test_next_round_refused_while_critical_open_and_changes_built_from_solutions(tmp_path):
    ep, run = era_issue_run(tmp_path)
    rr.main(["issues", str(run)])
    with pytest.raises(SystemExit, match="严重 / 主要"):
        rr.main(["new", str(ep), "--after", str(run), "--changes", "改了"])
    with pytest.raises(SystemExit, match="--reason"):
        rr.main(["fix", str(run), "I1", "--solution", "不改", "--status", "wontfix"])
    issues = json.loads((run / "issues.json").read_text(encoding="utf-8"))["issues"]
    must = [i for i in issues if i["level"] in ("critical", "major")]
    for i in must[:-1]:
        rr.main(["fix", str(run), i["id"], "--solution", f"已改 {i['dimension']}", "--status", "implemented"])
    with pytest.raises(SystemExit, match="1 个"):
        rr.main(["new", str(ep), "--after", str(run)])
    rr.main(["fix", str(run), must[-1]["id"], "--solution", "保留现状", "--status", "wontfix", "--reason", "要积分，交用户决定"])
    assert rr.main(["new", str(ep), "--after", str(run), "--changes", "另外改了工具"]) == 0
    r2 = runs(ep)[-1]
    assert r2.name.endswith("_r2")
    ch = (r2 / "changes.md").read_text(encoding="utf-8")
    assert all(f"已改 {i['dimension']}" in ch for i in must[:-1]) and "要积分，交用户决定" in ch and "另外改了工具" in ch
    prev = (r2 / "previous.md").read_text(encoding="utf-8")
    assert "I1" in prev and "s3_st1" in prev and "## 时代与世界观" in prev
    assert load(r2)["changes"] == ch.split("\n\n", 1)[1].strip()


def test_gate_reports_open_critical_issues_after_conclude(tmp_path, capsys):
    ep, run = era_issue_run(tmp_path)
    assert rr.main(["gate", str(run)]) == 0                    # 审完未收轮：闸门只看是否审完
    assert rr.main(["conclude", str(run)]) == 0
    res = (run / "结果.md").read_text(encoding="utf-8")
    assert "### 时代与世界观" in res and "| E1 器物 | 0 | 1 | 0 |" in res and "E3 服饰与发型（分歧）：a 1 / b 3 → 1" in res
    capsys.readouterr()
    assert rr.main(["gate", str(run)]) == 1
    assert "未处理的严重（critical）问题 3 个" in capsys.readouterr().out
    for i in json.loads((run / "issues.json").read_text(encoding="utf-8"))["issues"]:
        if i["level"] == "critical":
            rr.main(["fix", str(run), i["id"], "--solution", "改好了", "--status", "implemented"])
    assert rr.main(["gate", str(run)]) == 0


# ---------------------------------------------------------------- 收轮不等用户、迁移、修复页（用户 2026-11-08）
def put_frame(ep: Path, sid: str, st: str, data: bytes, archive: str = "", mtime: float | None = None) -> Path:
    """写一张首帧（或归档到 planning/<archive>/）；mtime 给了就改修改时间。"""
    pl = ep / f"scenes/{sid}/shots/{st}/planning"
    f = (pl / archive if archive else pl) / f"{st}_first_frame.png"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(data)
    if mtime is not None:
        os.utime(f, (mtime, mtime))
    return f


def put_prompt(ep: Path, sid: str, st: str, text: str) -> None:
    p = ep / f"scenes/{sid}/shots/{st}/资料包/prompt.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def set_action(ep: Path, sid: str, text: str) -> None:
    doc = json.loads((ep / "filming.json").read_text(encoding="utf-8"))
    sc = next(x for x in doc["content"]["scenes"] if x["id"] == sid)
    sc["shots"][0]["action"] = text
    (ep / "filming.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")


def test_new_snapshots_reviewed_materials(tmp_path):
    """修复页的「修复前」：new 把每场分镜、每镜 prompt、首帧路径与 sha 存进 materials/snapshot/。"""
    ep = make_episode(tmp_path)
    set_action(ep, "s1", "她转身。看城门。")
    put_frame(ep, "s1", "st1", b"OLD-FRAME")
    put_prompt(ep, "s1", "st1", "ep1_s1_st1\n画面：她转身")
    assert rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1,s2"]) == 0
    run, = runs(ep)
    snap = run / "materials/snapshot"
    assert json.loads((snap / "filming_s1.json").read_text(encoding="utf-8"))["shots"][0]["action"] == "她转身。看城门。"
    assert (snap / "filming_s2.json").is_file() and not (snap / "filming_s3.json").exists()
    assert (snap / "prompts/s1_st1.txt").read_text(encoding="utf-8").startswith("ep1_s1_st1")
    ff = json.loads((snap / "first_frames.json").read_text(encoding="utf-8"))
    assert ff["s1_st1"]["sha256"] == hashlib.sha256(b"OLD-FRAME").hexdigest() and ff["s1_st1"]["path"].endswith("planning/st1_first_frame.png")
    assert "s2_st1" not in ff                                 # s2 还没有首帧


def test_fix_records_files_and_before_after_pairs(tmp_path):
    ep, run = era_issue_run(tmp_path)
    rr.main(["issues", str(run)])
    old = put_frame(ep, "s1", "st1", b"A", archive="_r1"); new = put_frame(ep, "s1", "st1", b"B")
    with pytest.raises(SystemExit, match="成对"):
        rr.main(["fix", str(run), "I1", "--solution", "x", "--before", str(old)])
    with pytest.raises(SystemExit, match="图不存在"):
        rr.main(["fix", str(run), "I1", "--solution", "x", "--before", str(old), "--after", str(tmp_path / "nope.png")])
    assert rr.main(["fix", str(run), "I1", "--solution", "重画首帧", "--status", "implemented", "--by", "Claude Code",
                    "--file", str(ep / "filming.json"), "--file", str(new), "--before", str(old), "--after", str(new)]) == 0
    i = json.loads((run / "issues.json").read_text(encoding="utf-8"))["issues"][0]
    assert [Path(f).name for f in i["files"]] == ["filming.json", "st1_first_frame.png"]
    assert i["frames"] == [{"before": rr.rel(old), "after": rr.rel(new)}]
    h = i["history"][-1]
    assert h["by"] == "Claude Code" and len(h["files"]) == 2 and h["frames"] == i["frames"]
    rr.main(["fix", str(run), "I1", "--solution", "重画首帧（再改）", "--status", "implemented", "--file", str(ep / "filming.json")])
    assert len(json.loads((run / "issues.json").read_text(encoding="utf-8"))["issues"][0]["files"]) == 2    # 去重


def corrections_chain(tmp_path: Path) -> tuple[Path, Path]:
    """第 1 轮：每类都报 s1_st1 物理重出 → fix 全部严重 / 主要 → 改分镜、重画首帧（旧图归档 _r1）。"""
    ep = make_episode(tmp_path)
    set_action(ep, "s1", "她站着。看城门。")
    put_frame(ep, "s1", "st1", b"FRAME-R1")
    put_frame(ep, "s2", "st1", b"S2-SAME")
    rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1,s2"]); r1, = runs(ep)
    tick_all(r1, tmp_path)
    rr.main(["issues", str(r1)])
    for i in json.loads((r1 / "issues.json").read_text(encoding="utf-8"))["issues"]:
        if i["level"] in ("critical", "major"):
            rr.main(["fix", str(r1), i["id"], "--solution", "改分镜、重画首帧", "--status", "implemented", "--file", str(ep / "filming.json")])
    pl = ep / "scenes/s1/shots/st1/planning"
    (pl / "_r1").mkdir()
    os.replace(pl / "st1_first_frame.png", pl / "_r1/st1_first_frame.png")
    put_frame(ep, "s1", "st1", b"FRAME-R2")
    set_action(ep, "s1", "她转身。看城门。")
    return ep, r1


def tick_r2(r2: Path, tmp: Path) -> None:
    """第 2 轮：物理仍报 s1_st1 物理可剪，其余各类干净。"""
    for it in load(r2)["items"]:
        rows = HEAD + "| s1_st1 | 1 | 物理 | 可剪 | ② | 还是没改好 | 改 |" if it["law"] == "physics" else ""
        for slot in ("a", "b"):
            assert tick5(r2, tmp, it, slot, report5(it, clean=not rows, rows=rows, r=True)) == 0
        if item_of(r2, it["id"])["status"] == "adjudicating":
            assert judge(r2, tmp, it["id"]) == 0


def test_corrections_before_after_diff_and_next_round_verification(tmp_path, capsys):
    ep, r1 = corrections_chain(tmp_path)
    assert rr.main(["corrections", str(r1)]) == 0             # 还没开下一轮：修复后＝现行，全部待复核
    doc = json.loads((r1 / "corrections.json").read_text(encoding="utf-8"))
    s1 = next(x for x in doc["shots"] if x["key"] == "s1_st1")
    assert s1["frame"]["changed"] and s1["frame"]["before"]["label"] == "_r1" and s1["frame"]["after"]["label"] == "现行"
    assert s1["frame"]["before"]["sha256"] == hashlib.sha256(b"FRAME-R1").hexdigest()
    act = next(f for f in s1["spec"]["fields"] if f["field"] == "action")
    assert act["before"] == "她站着。看城门。" and "-她站着。" in act["diff"] and "+她转身。" in act["diff"] and " 看城门。" in act["diff"]
    s2 = next(x for x in doc["shots"] if x["key"] == "s2_st1")
    assert not s2["frame"]["changed"] and not s2["spec"]["changed"]
    assert doc["corrections"] and all(c["verification"]["status"] == "待复核" for c in doc["corrections"])
    crit = [c for c in doc["corrections"] if c["level"] == "critical"]
    assert crit and all(c["keys"] == ["s1_st1"] and c["files"][0].endswith("filming.json") for c in crit)
    assert doc["summary"]["frames_changed"] == 1 and doc["summary"]["by_verification"]["待复核"] == len(doc["corrections"])
    md = (r1 / "corrections.md").read_text(encoding="utf-8")
    assert "### s1_st1" in md and "```diff" in md and "_r1" in md
    assert load(r1)["corrections"] == "corrections.json" and load(r1)["log"][-1]["event"] == "corrections"
    first = (r1 / "corrections.json").read_text(encoding="utf-8"); n_log = len(load(r1)["log"])
    time.sleep(1.1)
    capsys.readouterr()
    assert rr.main(["corrections", str(r1)]) == 0              # 重跑幂等：内容不变就不改时间、不加 log
    assert (r1 / "corrections.json").read_text(encoding="utf-8") == first and len(load(r1)["log"]) == n_log
    assert "内容没变" in capsys.readouterr().out
    assert rr.main(["new", str(ep), "--after", str(r1)]) == 0
    r2 = runs(ep)[-1]
    tick_r2(r2, tmp_path)
    assert rr.main(["corrections", str(r1)]) == 0
    doc = json.loads((r1 / "corrections.json").read_text(encoding="utf-8"))
    assert doc["child"] == rr.rel(r2) and doc["child_state"] == "已完成"
    s1 = next(x for x in doc["shots"] if x["key"] == "s1_st1")
    assert s1["frame"]["after"]["sha256"] == hashlib.sha256(b"FRAME-R2").hexdigest() and "下一轮" in s1["frame"]["after"]["how"]
    assert all(c["files"] for c in doc["corrections"] if c["level"] == "critical")        # 开下一轮重推问题清单不丢 --file
    v = {c["law"]: c["verification"] for c in doc["corrections"] if c["level"] == "critical"}
    assert v["physics"]["status"] == "复核仍有问题" and any("可剪" in h for h in v["physics"]["how"]) and v["physics"]["rows"]
    assert v["era"]["status"] == "已复核通过" and any("R ✓" in h for h in v["era"]["how"])
    assert doc["summary"]["by_verification"]["复核仍有问题"] >= 1 and doc["summary"]["by_verification"]["待复核"] == 0


def test_corrections_for_old_runs_use_archives_by_time_and_spec_md(tmp_path):
    """旧单没有快照：修复前取审查开始时已在的那版首帧（按修改时间，含 _r1 等归档）和 materials/shots 的 spec.md；
    修复后取下一轮开始时的那版和下一轮的 spec.md。没有 issues.json 的旧单从问题表现推，方案配下一轮 changes.md。"""
    ep, r1 = corrections_chain(tmp_path)
    rr.main(["new", str(ep), "--after", str(r1)]); r2 = runs(ep)[-1]
    for r in (r1, r2):
        shutil.rmtree(r / "materials/snapshot")
    t0 = rr.dt.datetime.fromisoformat(load(r1)["created_at"]).timestamp()
    os.utime(ep / "scenes/s1/shots/st1/planning/_r1/st1_first_frame.png", (t0 - 60, t0 - 60))
    os.utime(ep / "scenes/s1/shots/st1/planning/st1_first_frame.png", (t0 + 60, t0 + 60))
    put_frame(ep, "s1", "st1", b"FRAME-R2", archive="_r2", mtime=t0 + 60)
    put_frame(ep, "s1", "st1", b"FRAME-R3", mtime=t0 + 600)           # 第 2 轮之后又重画：不算第 1 轮的修复
    d2 = load(r2); d2["created_at"] = rr.dt.datetime.fromtimestamp(t0 + 120).isoformat(timespec="seconds")
    (r2 / "checklist.json").write_text(json.dumps(d2, ensure_ascii=False), encoding="utf-8")
    (r2 / "changes.md").write_text("# 改了什么\n\n### physics\n- physics · s1_st1 · 物理 → 第 1 轮之后已改成转身\n", encoding="utf-8")
    (r1 / "issues.json").unlink()
    doc = rr.build_corrections(r1, load(r1))
    s1 = next(x for x in doc["shots"] if x["key"] == "s1_st1")
    assert s1["frame"]["before"]["label"] == "_r1" and s1["frame"]["after"]["label"] == "_r2"
    assert s1["frame"]["after"]["sha256"] == hashlib.sha256(b"FRAME-R2").hexdigest()
    assert s1["spec"]["before_source"].endswith("materials/shots/s1_st1/spec.md") and s1["spec"]["after_source"].endswith("s1_st1/spec.md")
    assert [f["field"] for f in s1["spec"]["fields"]] == ["action"]
    assert doc["issues_source"].startswith("推导") and doc["changes_md"].endswith("changes.md")
    assert doc["corrections"] and all(c["law"] == "physics" for c in doc["corrections"])      # changes.md 只写了物理的方案
    assert doc["corrections"][0]["solution"] == "第 1 轮之后已改成转身" and doc["corrections"][0]["solution_source"] == "changes.md"


def test_shot_keys_and_spec_md_parsing():
    assert rr.shot_keys("s3_st3", []) == ["s3_st3"]
    assert rr.shot_keys("s1_st3→s1_st5", []) == ["s1_st3", "s1_st5"]
    assert rr.shot_keys("s1 全场（st3、st4、st5）", []) == ["s1_st3", "s1_st4", "s1_st5"]
    assert rr.shot_keys("st4", ["s1"]) == ["s1_st4"] and rr.shot_keys("st4", ["s1", "s2"]) == []
    assert rr.parse_spec_md("- 设计时长：7 秒；出场：c1, c2；单拍\n\n## 分镜规格\n**动作**：走。\n停。\n**台词**：（无）\n") == \
        {"duration": "7", "cast": "c1, c2", "action": "走。\n停。", "dialogue": ""}


def test_conclude_closes_without_waiting_for_user_and_records_verdict(tmp_path):
    """用户 2026-11-08：每一次审查结果不需要 human gate——conclude 直接「已收轮」并记结论；用户只在出片时确认。"""
    ep = make_episode(tmp_path)
    rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1"]); run, = runs(ep)
    tick_all(run, tmp_path, clean=True)
    assert rr.main(["conclude", str(run)]) == 0
    d = load(run)
    assert d["state"] == "已收轮" and d["verdict"] == {"result": "可出片", "text": "没有未处理的严重问题", "reasons": []}
    assert "- 结论：可出片" in (run / "结果.md").read_text(encoding="utf-8")
    assert rr.main(["gate", str(run)]) == 0
    assert "已收轮" in rr.STATES and "待用户确认" not in rr.STATES
    with pytest.raises(SystemExit, match="已收轮"):
        tick5(run, tmp_path, item_of(run, "era"), "a", report5(item_of(run, "era"), clean=True))
    time.sleep(1.1)
    rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s2"]); r2 = runs(ep)[-1]
    tick_all(r2, tmp_path, clean=True)
    rr.main(["conclude", str(r2), "--verdict", "暂不建议出片：先修 st5"])     # 自己写的结论：结果按文字判
    assert load(r2)["verdict"]["result"] == "不可出片" and load(r2)["verdict"]["text"].startswith("暂不建议")


def test_migrate_old_waiting_state(tmp_path, capsys):
    ep = make_episode(tmp_path)
    rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1"]); run, = runs(ep)
    tick_all(run, tmp_path, clean=True)
    rr.main(["conclude", str(run)])
    d = load(run); d["state"] = "待用户确认"; d.pop("verdict")
    (run / "checklist.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    (run / "结果.md").write_text("# 审查结果\n\n- 结论：暂不建议直接出片：先修 st5 首帧\n", encoding="utf-8")
    assert rr.main(["migrate", str(tmp_path / "demo")]) == 0
    d = load(run)
    assert d["state"] == "已收轮" and d["log"][-1]["event"] == "migrate" and "已收轮" in d["log"][-1]["note"]
    assert d["verdict"]["result"] == "不可出片" and d["verdict"]["text"].startswith("暂不建议")
    capsys.readouterr()
    assert rr.main(["migrate", str(run)]) == 0 and "共迁移 0 张" in capsys.readouterr().out      # 再跑不重复
    d["state"] = "待用户确认"; (run / "checklist.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    assert rr.main(["status", str(run)]) == 0 and load(run)["state"] == "已收轮"               # status 也顺手迁移


def test_can_submit_needs_user_confirmation_on_the_latest_concluded_run(tmp_path):
    """出片时才要用户确认：覆盖该场的最新一张已收轮出片前审查单要 confirm 过、材料未变。"""
    ep = make_episode(tmp_path)
    rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1"]); r1, = runs(ep)
    tick_all(r1, tmp_path, clean=True); rr.main(["conclude", str(r1)])
    ok, msg = rr.can_submit(ep, ["ep1_s1_st1"])
    assert not ok and "已收轮" in msg and "confirm" in msg
    rr.main(["confirm", str(r1), "--quote", "出吧"])
    assert rr.can_submit(ep, ["ep1_s1_st1"])[0]
    time.sleep(1.1)
    rr.main(["new", str(ep), "--stage", "pregen", "--scenes", "s1"]); r2 = runs(ep)[-1]
    assert rr.can_submit(ep, ["ep1_s1_st1"])[0]                # 新单还没收轮：仍以已确认的那张为准
    tick_all(r2, tmp_path, clean=True); rr.main(["conclude", str(r2)])
    ok, msg = rr.can_submit(ep, ["ep1_s1_st1"])
    assert not ok and r2.name in msg                            # 最新收轮的那张还没确认
    rr.main(["confirm", str(r2), "--quote", "再出"])
    assert rr.can_submit(ep, ["ep1_s1_st1"])[0]


@pytest.mark.single_review
def test_single_claude_review_finishes_without_reconcile_or_judge(tmp_path):
    """正式名册：每项只有 Claude 一位（follow-up 065）；打勾不写 --slot 也行，勾完直接完成、没有裁决。"""
    ep = make_episode(tmp_path)
    assert rr.main(["new", str(ep), "--stage", "filming"]) == 0
    run = runs(ep)[-1]
    it = load(run)["items"][0]
    assert list(it["slots"]) == ["a"] and it["slots"]["a"]["runner"] == "claude"
    rep = run / it["slots"]["a"]["report"]; rep.parent.mkdir(exist_ok=True)
    rep.write_text(report5(it, scores={it["rubric"][0]["id"]: 1}), encoding="utf-8")
    assert rr.main(["tick", str(run), it["id"], "--report", str(rep), "--by", f"claude-opus-5-5/{it['id']}__a"]) == 0
    got = item_of(run, it["id"])
    assert got["status"] == "done" and "judge" not in got and got["final_scores"][it["rubric"][0]["id"]] == 1
    assert (run / got["report"]).read_text(encoding="utf-8").startswith(f"# {it['id']}") and "单审" in (run / got["report"]).read_text(encoding="utf-8")


@pytest.mark.single_review
def test_drop_slot_turns_a_running_dual_review_into_single(tmp_path, monkeypatch):
    r = json.loads(REAL_ROSTER.read_text(encoding="utf-8"))
    for law in r["laws"].values():
        law["reviewers"] = [{"slot": "a", "runner": "claude", "model": "claude-opus-5-5"}, {"slot": "b", "runner": "codex", "model": "gpt-6.1-sol"}]
    f = tmp_path / "roster.json"; f.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(rr, "ROSTER", f)
    ep = make_episode(tmp_path)
    assert rr.main(["new", str(ep), "--stage", "filming"]) == 0
    run = runs(ep)[-1]
    it = load(run)["items"][0]
    rep = run / it["slots"]["a"]["report"]; rep.parent.mkdir(exist_ok=True)
    rep.write_text(report5(it), encoding="utf-8")
    assert rr.main(["tick", str(run), it["id"], "--slot", "a", "--report", str(rep), "--by", f"claude-opus-5-5/{it['id']}__a"]) == 0
    assert item_of(run, it["id"])["status"] == "pending"
    assert rr.main(["drop-slot", str(run), "--note", "用户：改成 Claude 单审"]) == 0
    got = item_of(run, it["id"])
    assert got["status"] == "done" and list(got["slots"]) == ["a"] and got["dropped_slots"][0]["slot"] == "b"


def test_final_round_concludes_on_fixed_materials_with_accept_fixes(tmp_path):
    """follow-up 069：最后一轮修复后材料必然变；--accept-fixes 只在最后一轮、问题都登记后按修复后材料收轮，之后再变照样拦。"""
    ep = make_episode(tmp_path); rr.main(["new", str(ep), "--stage", "pregen"]); r1, = runs(ep)
    tick_all(r1, tmp_path)
    with pytest.raises(SystemExit, match="最后一轮"):
        accept = lambda r: rr.main(["conclude", str(r), "--accept-fixes"])
        (ep.parent.parent / "bible.md").write_text("# bible v1", encoding="utf-8")
        accept(r1)
    rr.main(["issues", str(r1)])
    for i in json.loads((r1 / "issues.json").read_text(encoding="utf-8"))["issues"]:
        rr.main(["fix", str(r1), i["id"], "--solution", "改好了", "--status", "implemented"])
    rr.main(["new", str(ep), "--after", str(r1), "--changes", "x"]); r2 = runs(ep)[-1]; tick_all(r2, tmp_path, clean=True)
    rr.main(["new", str(ep), "--after", str(r2), "--changes", "y"]); r3 = runs(ep)[-1]; tick_all(r3, tmp_path)
    (ep.parent.parent / "bible.md").write_text("# bible v3", encoding="utf-8")
    with pytest.raises(SystemExit, match="收轮"):
        rr.main(["conclude", str(r3)])                                    # 不加开关：材料变了照旧拦
    with pytest.raises(SystemExit, match="没登记"):
        rr.main(["conclude", str(r3), "--accept-fixes"])
    for i in json.loads((r3 / "issues.json").read_text(encoding="utf-8"))["issues"]:
        if i["level"] in ("critical", "major"):
            rr.main(["fix", str(r3), i["id"], "--solution", "改好了", "--status", "implemented"])
    assert rr.main(["conclude", str(r3), "--accept-fixes"]) == 0
    d = load(r3)
    assert d["state"] == "已收轮" and d["accepted_fixes"]["changed"] and d["reviewed_materials"] != d["materials"]
    assert "未经独立复审" in (r3 / "结果.md").read_text(encoding="utf-8")
    first = d["reviewed_materials"]
    (ep.parent.parent / "bible.md").write_text("# bible v3b", encoding="utf-8")       # 收轮后、确认前又补一处修复
    assert rr.main(["conclude", str(r3), "--accept-fixes"]) == 0
    d = load(r3)
    assert d["state"] == "已收轮" and d["reviewed_materials"] == first and rr.stale_files(d) == []
    assert rr.main(["confirm", str(r3), "--quote", "出"]) == 0
    (ep.parent.parent / "bible.md").write_text("# bible v3c", encoding="utf-8")
    with pytest.raises(SystemExit, match="确认"):
        rr.main(["conclude", str(r3), "--accept-fixes"])
    (ep.parent.parent / "bible.md").write_text("# bible v4", encoding="utf-8")
    assert not rr.can_submit(ep, ["ep1_s1_st1"])[0]
