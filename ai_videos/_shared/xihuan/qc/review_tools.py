"""审图辅助：生成独立审图批次清单，合并审图结论到 qc/reviews.json（绑定 SHA256）。

    python ai_videos/_shared/xihuan/qc/review_tools.py manifest OUT_DIR --batches 4   # 只含有图且未验收的条目
    python ai_videos/_shared/xihuan/qc/review_tools.py merge VERDICT.json [VERDICT.json ...]

审图结论 JSON：[{"id": "PS01", "sha256": "...", "verdict": "pass|pass_with_notes|revise", "notes": ["..."]}]
SHA 与当前图片不一致的结论不收（图被换过）。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "qc" / "reviews.json"
STATUS = {"pass": "reviewed", "pass_with_notes": "reviewed_with_notes", "revise": "revision_required"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(out_dir: Path, batches: int) -> None:
    lib = json.loads((ROOT / "library.json").read_text(encoding="utf-8"))
    data = {e["id"]: e for f in sorted((ROOT / "data").glob("*.json")) for s in json.loads(f.read_text(encoding="utf-8"))["subgroups"] for e in s["entries"]}
    todo = [a for a in lib["assets"] if a["image"]["sha256"] and a["image"]["status"] == "generated_unreviewed"]
    items = [{"id": a["id"], "name": f"{a['name']} / {a['name_en']}", "purpose": a["image"]["purpose"],
              "image": str((ROOT / a["image"]["anchor"]).resolve()), "sha256": a["image"]["sha256"],
              "brief": data[a["id"]]["image"]["brief"], "visual": a["visual_signature"]} for a in todo]
    out_dir.mkdir(parents=True, exist_ok=True)
    size = -(-len(items) // max(1, batches))
    for i in range(0, len(items), size):
        (out_dir / f"batch_{i // size + 1:02d}.json").write_text(json.dumps(items[i:i + size], ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)} 张，{-(-len(items) // size) if items else 0} 批 → {out_dir}")


def merge(files: list[Path]) -> None:
    reviews = json.loads(REVIEWS.read_text(encoding="utf-8")) if REVIEWS.is_file() else {}
    lib = {a["id"]: a for a in json.loads((ROOT / "library.json").read_text(encoding="utf-8"))["assets"]}
    taken = skipped = 0
    for f in files:
        for v in json.loads(f.read_text(encoding="utf-8")):
            a = lib.get(v["id"])
            current = a and (ROOT / a["image"]["anchor"]).is_file() and sha(ROOT / a["image"]["anchor"])
            if not current or current != v["sha256"] or v["verdict"] not in STATUS:
                skipped += 1
                continue
            reviews[v["id"]] = {"sha256": v["sha256"], "status": STATUS[v["verdict"]], "notes": v.get("notes", []), "evidence": f.as_posix()}
            taken += 1
    REVIEWS.write_text(json.dumps(reviews, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"收 {taken}，弃 {skipped}（SHA 不符或结论无效）")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    if cmd == "manifest":
        manifest(Path(rest[0]), int(rest[2]) if len(rest) > 2 and rest[1] == "--batches" else 4)
    elif cmd == "merge":
        merge([Path(p) for p in rest])
    else:
        raise SystemExit(__doc__)
