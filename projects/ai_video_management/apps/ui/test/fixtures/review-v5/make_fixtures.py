"""用 tools/review_run.py 自己在临时目录跑出真实的 v5 审查单，导出成 UI 测试 fixture（test/review-v5.test.tsx）。

重生成（仓库根目录）：
    python projects/ai_video_management/apps/ui/test/fixtures/review-v5/make_fixtures.py <临时目录> projects/ai_video_management/apps/ui/test/fixtures/review-v5
注意：会清空输出目录后重写；审查单 id 带生成时间，重生成后测试按 checklist.json 里的 id 取路径，不用改测试。
"""
import json, re, shutil, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(REPO))
from tools import review_run as rr
from tools.tests import test_review_run as t

tmp = Path(sys.argv[1]); out = Path(sys.argv[2])
shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
for old in out.glob("*_checklist.json"):
    old.unlink()
out.mkdir(parents=True, exist_ok=True)
ep, run = t.era_issue_run(tmp)                      # 完成的单：era 有分歧裁决、0 分、1 分
rr.main(["issues", str(run)])
issues = json.loads((run / "issues.json").read_text(encoding="utf-8"))["issues"]
rr.main(["fix", str(run), issues[0]["id"], "--solution", "重画首帧，器物换成陶碗", "--status", "planned"])
rr.main(["fix", str(run), issues[0]["id"], "--solution", "重画首帧，器物换成陶碗（已出图）", "--status", "implemented"])
rr.main(["fix", str(run), issues[1]["id"], "--solution", "保留现状", "--status", "wontfix", "--reason", "要积分，交用户决定"])
rr.main(["fix", str(run), issues[2]["id"], "--solution", "改场景图去掉百叶窗", "--status", "planned"])
for name in ("checklist.json", "issues.json"):
    shutil.copyfile(run / name, out / f"done_{name}")
shutil.copyfile(run / "reconcile/era.md", out / "done_reconcile_era.md")
# 进行中的单：era 双勾待裁决（分歧）；physics_A a 勾、b 凭 Codex 日志代登记 → 待裁决（抽查）；physics_B 只勾 a；continuity b 失败
tmp2 = tmp / "live"; tmp2.mkdir()
ep2 = t.make_episode(tmp2); rr.main(["new", str(ep2), "--stage", "filming"]); run2, = t.runs(ep2)
era = t.item_of(run2, "era")
t.tick5(run2, tmp2, era, "a", t.report5(era, {"E1": 1, "E2": 2}))
t.tick5(run2, tmp2, era, "b", t.report5(era, clean=True))
ph = t.item_of(run2, "physics_A")
t.tick5(run2, tmp2, ph, "a", t.report5(ph))
pf = tmp2 / "p.md"; pf.write_text("run the task", encoding="utf-8")
rr.main(["dispatch", str(run2), "physics_A", "--slot", "b", "--runner", "codex exec", "--model", "gpt-6-astra", "--prompt-file", str(pf),
         "--at", "2020-01-01T00:00:00"])
rep = tmp2 / "pa_b.md"; rep.write_text(t.report5(ph), encoding="utf-8")
log = tmp2 / "codex.log"; log.write_text("REPORT WRITTEN: " + str(rep) + "\n", encoding="utf-8")
assert rr.main(["tick", str(run2), "physics_A", "--slot", "b", "--report", str(rep), "--by", "gpt-6-astra/physics_A__b", "--attest-log", str(log)]) == 0
pb = t.item_of(run2, "physics_B"); t.tick5(run2, tmp2, pb, "a", t.report5(pb))
rr.main(["fail", str(run2), "continuity", "--slot", "b", "--note", "Codex 网络 403"])
shutil.copyfile(run2 / "checklist.json", out / "live_checklist.json")

# 归一化：临时路径 → ai_videos/demo；测试署名 ma/mb/mj → 真实模型名；去掉体积大的材料指纹
roots = [p.resolve() for p in (tmp / "live", tmp)]
for f in [out / n for n in ("done_checklist.json", "done_issues.json", "done_reconcile_era.md", "live_checklist.json")]:
    s = f.read_text(encoding="utf-8")
    for root in roots:
        for form in (root.as_posix(), str(root).replace("\\", "\\\\"), str(root)):
            s = s.replace(form, "ai_videos")
    s = s.replace("ai_videos/demo", "ai_videos/demo").replace("ai_videos\\demo", "ai_videos/demo")
    s = re.sub(r"\bm([abj])/", lambda m: {"a": "claude-opus-5-5/", "b": "gpt-6-astra/", "j": "claude-opus-5-5/"}[m.group(1)], s)
    if f.suffix == ".json":
        d = json.loads(s)
        if "materials" in d:
            d["materials"] = {}
        s = json.dumps(d, ensure_ascii=False, indent=1)
    f.write_text(s, encoding="utf-8")
print("ok")
