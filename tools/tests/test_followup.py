"""follow-up 唯一写入口（2026-10-26 dota_yingxiong 日志复盘：漏记 25 条、撞号 7 个、条目串写）；
2026-10-27 follow-up 280：各会话先各自记（_inbox）、周期性汇聚，只拦本会话自己，没有单点拦截。"""
import datetime as dt
import io
import json
from pathlib import Path

import pytest

from tools import followup

ME, OTHER = "session-me", "session-other"


def test_codex_session_owns_followup_without_kimi_environment(spec: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("FOLLOWUP_OWNER", raising=False)
    monkeypatch.delenv("KIMI_CODE_SESSION_ID", raising=False)
    monkeypatch.setenv("CODEX_THREAD_ID", "codex-thread")
    new("codex-work")
    assert followup.inbox_entries(spec)[0][0].owner == "codex-thread"


@pytest.fixture
def spec(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(followup, "REPO", tmp_path)
    monkeypatch.setattr(followup, "SPECS", tmp_path / "specs")
    monkeypatch.setattr(followup, "ENFORCE_FROM", "2000-01-01")
    monkeypatch.setenv("FOLLOWUP_OWNER", ME)
    sp = tmp_path / "specs" / "ai_video" / "demo"
    (sp / "user_input" / "follow_ups").mkdir(parents=True)
    (sp / "user_input" / "raw_prompt.md").write_text("原始需求", encoding="utf-8")
    (sp / "changelog.md").write_text("# changelog\n", encoding="utf-8")
    return sp


def new(slug: str, owner: str | None = None) -> None:
    args = ["new", "demo", "--slug", slug, "--instruction", "做一件事", "--summary", f"{slug} 摘要"]
    assert followup.main(args + (["--owner", owner] if owner else [])) == 0


def done(n: str, *extra: str) -> int:
    return followup.main(["done", "demo", n, "--updated", f"{n}.png — 重出", "--verified", "自检通过", *extra])


def problems(spec: Path, me: str = ME) -> list[followup.Problem]:
    return followup.check_one(spec, me)


def central(spec: Path) -> tuple[str, str]:
    month = "".join(f.read_text(encoding="utf-8") for f in followup.fu_files(spec))
    return month, (spec / "changelog.md").read_text(encoding="utf-8")


def later(monkeypatch: pytest.MonkeyPatch) -> None:
    t = dt.datetime.now() + dt.timedelta(hours=followup.STALE_HOURS + 1)
    monkeypatch.setattr(followup, "now", lambda: t.replace(microsecond=0))


def test_new_records_in_own_inbox_not_shared_logs(spec: Path):
    new("first")
    new("second", owner=OTHER)
    assert [n for n, *_ in followup.headings(spec)] == [1, 2]          # 编号连续、不撞（_inbox 也算）
    assert all(followup.FU_CANON.match(h) for *_, h, _ in followup.headings(spec))
    month, cl = central(spec)
    assert month == "" and "Follow-up" not in cl                       # 不碰共用的月度文件与 changelog
    entries, bad = followup.inbox_entries(spec)
    assert [(e.n, e.owner) for e in entries] == [(1, ME), (2, OTHER)] and not bad
    assert "second 摘要" in (spec / "user_input" / "revised_prompt.md").read_text(encoding="utf-8")
    assert [(p.kind, p.blocking) for p in problems(spec)] == [("未收尾", False), ("未收尾", False)]


def test_done_finishes_own_entry_and_merges_it(spec: Path):
    new("first")
    new("second")
    assert done("001", "--cost", "任务 abc · 120 积分") == 0
    month, cl = central(spec)
    assert "## 001 —" in month and "## 002 —" not in month             # 只汇聚收尾的那条
    assert "001.png — 重出" in cl and "费用: 任务 abc · 120 积分" in cl and followup.PENDING not in cl
    assert [e.n for e in followup.inbox_entries(spec)[0]] == [2]
    assert followup.CL_CANON.findall(cl) and [p.kind for p in problems(spec)] == ["未收尾"]
    assert "002" not in "".join(p.detail for p in problems(spec) if p.kind == "漏记")


def test_done_requires_an_update_line(spec: Path):
    new("first")
    with pytest.raises(SystemExit):
        followup.main(["done", "demo", "001", "--verified", "x"])


def test_merge_keeps_number_order_and_leaves_pending(spec: Path):
    for s in ("a", "b", "c"):
        new(s)
    for n in ("003", "001"):
        e = next(e for e in followup.inbox_entries(spec)[0] if e.n == int(n))
        e.cl = e.cl.replace(followup.PENDING_MARK, "（")             # 模拟已收尾但还没汇聚
        e.save()
    assert followup.main(["merge", "demo"]) == 0
    month, cl = central(spec)
    assert month.index("## 001 —") < month.index("## 003 —") and "## 002 —" not in month
    assert [e.n for e in followup.inbox_entries(spec)[0]] == [2]


def test_only_own_stale_entry_blocks(spec: Path, monkeypatch: pytest.MonkeyPatch):
    new("mine")
    new("theirs", owner=OTHER)
    assert not any(p.blocking for p in problems(spec))                 # 新的都不拦
    later(monkeypatch)
    assert [p.detail[:15] for p in problems(spec) if p.blocking] == ["Follow-up 001 还"]
    assert not any(p.blocking for p in problems(spec, OTHER) if "001" in p.detail)
    assert not any(p.blocking for p in problems(spec, ""))             # 认不出会话：谁也不拦


def test_legacy_central_pending_only_warns_and_done_edits_in_place(spec: Path, monkeypatch: pytest.MonkeyPatch):
    month = spec / "user_input" / "follow_ups" / "202610.md"
    month.write_text("\n---\n\n## 001 — 2026-10-26 08:00:00 — old\n\n### 指令\n\nx\n", encoding="utf-8")
    (spec / "changelog.md").write_text(
        "# changelog\n\n## Follow-up 001 — 2026-10-26 08:00:00\nSource: s\nSummary: old\n\nAuto-updated:\n"
        f"- （{followup.PENDING}：x）\n\n验证: （{followup.PENDING}）\n\nNo conflicts found in: （{followup.PENDING}）\n",
        encoding="utf-8")
    later(monkeypatch)
    assert [(p.kind, p.blocking) for p in problems(spec)] == [("未收尾", False)]   # 别人丢下的旧条目不挡人
    assert done("001") == 0
    assert followup.PENDING_MARK not in central(spec)[1] and problems(spec) == []


def test_hand_written_central_dup_warns_but_own_collision_blocks(spec: Path):
    new("first")
    done("001")
    month = next(iter(followup.fu_files(spec)))
    with month.open("a", encoding="utf-8") as fh:            # 绕过工具手写：同号 + 不规范标题 + 无 changelog
        fh.write("\n---\n\n## 001 — 2026-10-26T08:00:00+08:00 — hand\n\n正文\n")
        fh.write("\n---\n\n## 002 — 2026-10-26 08:00:00 — hand2\n\n正文\n")
    kinds = sorted(p.kind for p in problems(spec))
    assert kinds == ["撞号", "撞号", "格式", "漏记"] and not any(p.blocking for p in problems(spec))
    new("third")                                             # 工具照样分配下一个号，不撞
    assert max(e.n for e in followup.inbox_entries(spec)[0]) == 3


def test_history_before_cutoff_is_ignored(spec: Path, monkeypatch: pytest.MonkeyPatch):
    month = spec / "user_input" / "follow_ups" / "202610.md"
    month.write_text("## 045 — 2026-10-21 — a\n\nx\n\n## 045 — 2026-10-21 — b\n\ny\n", encoding="utf-8")
    monkeypatch.setattr(followup, "ENFORCE_FROM", "2026-10-26")
    assert problems(spec) == []                                # 旧剧旧条目不回溯


def test_pending_word_in_prose_is_not_a_placeholder(spec: Path):
    new("first")
    followup.main(["done", "demo", "001", "--updated", "k1.png — 出成；其余三张待补", "--verified", "自检通过"])
    assert problems(spec) == []                                # 「待补」出现在正文里不是未收尾


def test_hook_merges_and_checks_as_the_stdin_session(spec: Path, monkeypatch: pytest.MonkeyPatch):
    new("mine")
    new("theirs", owner=OTHER)
    e = next(e for e in followup.inbox_entries(spec)[0] if e.n == 2)
    e.cl = e.cl.replace(followup.PENDING_MARK, "（")
    e.save()
    later(monkeypatch)
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"session_id": OTHER})))
    assert followup.main(["check", "--all", "--hook"]) == 0      # 我的 001 超时，但钩子是 OTHER 会话的：不拦它
    assert "## 002 —" in central(spec)[0]                        # 顺手汇聚了已收尾的 002
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"session_id": ME})))
    assert followup.main(["check", "--all", "--hook"]) == 2      # 轮到我自己收尾才拦我
