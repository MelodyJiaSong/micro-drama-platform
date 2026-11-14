"""查询 8 条草稿并下载到各变体目录（每次查询经 service_call 记日志）。完成的不再查。"""
import json, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parents[3]
TARGET = HERE.relative_to(REPO).as_posix()


def query(sid: str, dl: Path) -> dict:
    cmd = [sys.executable, "tools/service_call.py", "--target", TARGET, "--", "dreamina", "query_result",
           f"--submit_id={sid}", f"--download_dir={dl}"]
    out = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    m = re.search(r"\{.*\}", out, re.S)
    try:
        return json.loads(m.group(0)) if m else {"raw": out}
    except Exception:
        return {"raw": out}


def main(rounds: int, wait: int):
    for r in range(rounds):
        pending = 0
        for sub in sorted(HERE.glob("*/submit_t[12].json")):
            take = sub.stem.split("_")[-1]
            dl = sub.parent / take
            if any(dl.glob("*.mp4")):
                continue
            sid = json.loads(sub.read_text(encoding="utf-8"))["submit_id"]
            dl.mkdir(exist_ok=True)
            res = query(sid, dl)
            st = res.get("gen_status", "?")
            (dl / "query_result.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
            got = list(dl.glob("*.mp4"))
            print(f"{sub.parent.name}/{take} {sid[:8]} {st} {'下载 ' + got[0].name if got else ''} {res.get('fail_reason', '')}", flush=True)
            if st not in ("success", "fail") or (st == "success" and not got):
                pending += 1
        if not pending:
            print("全部结束")
            return
        time.sleep(wait)


main(int(sys.argv[1]) if len(sys.argv) > 1 else 1, int(sys.argv[2]) if len(sys.argv) > 2 else 60)
