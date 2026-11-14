"""用 tools/review_run.py 在临时目录真跑一条两轮的链，导出修复页 fixture（test/review-corrections.test.tsx）。

第 1 轮各类都报 s1_st1 物理重出 → fix 全部严重 / 主要（带 --file）→ 改分镜、重画首帧（旧图归档 _r1）→ 第 2 轮：物理仍报 s1_st1，
其余各类干净 → 对第 1 轮跑 corrections。重生成（仓库根目录）：
    python projects/ai_video_management/apps/ui/test/fixtures/review-corrections/make_fixture.py <临时目录> projects/ai_video_management/apps/ui/test/fixtures/review-corrections
"""
import json, re, shutil, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(REPO))
from tools import review_run as rr
from tools.tests import test_review_run as t

tmp = Path(sys.argv[1]); out = Path(sys.argv[2])
shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
out.mkdir(parents=True, exist_ok=True)
ep, r1 = t.corrections_chain(tmp)
rr.main(["new", str(ep), "--after", str(r1)])
r2 = t.runs(ep)[-1]
t.tick_r2(r2, tmp)
rr.main(["corrections", str(r1)])
pairs = [(r1 / "corrections.json", "r1_corrections.json"), (r1 / "checklist.json", "r1_checklist.json"), (r2 / "checklist.json", "r2_checklist.json")]
root = tmp.resolve()
for src, name in pairs:
    s = src.read_text(encoding="utf-8")
    for form in (root.as_posix(), str(root).replace("\\", "\\\\"), str(root)):
        s = s.replace(form, "ai_videos")
    s = re.sub(r"\bm([abj])/", lambda m: {"a": "claude-opus-5-5/", "b": "gpt-6-astra/", "j": "claude-opus-5-5/"}[m.group(1)], s)
    d = json.loads(s)
    if "materials" in d and isinstance(d["materials"], dict):
        d["materials"] = {}
    (out / name).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok")
