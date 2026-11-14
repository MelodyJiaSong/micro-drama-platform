# -*- coding: utf-8 -*-
"""follow-up 016 补搜：复用 _tools/image_reselect.py 的 Codex 搜索（同一 RequestLog 先记日志），
只对指定项（或全部）再搜一轮，要求至少 N 张、排除已找到的链接。输出 _build/reselect/codex_b2_<tag>.json，
image_reselect.py download 会一并读入（glob codex_b*.json）。

    python image_search2.py [--only idx idx ...] [--n 6] [--batch 5] [--workers 2] [--tag r2] [--extra "..."]
"""
import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools"))
import image_reselect as R  # noqa: E402

EXTRA = """
IMPORTANT: return AT LEAST {n} candidates per subject (more is fine), all real photographs of exactly the named place in the named country.
Do NOT repeat any of these already-found image URLs: {seen}
Search widely: Pexels, Unsplash, Pixabay, Flickr (CC-licensed: CC BY / CC BY-SA / CC0 / PDM), national park or tourism-board press pages, NASA / USGS (public domain) where relevant.
{extra}"""


def seen_urls(key: str) -> list[str]:
    out = []
    for f in sorted((EP / "_build" / "reselect").glob("codex_b*.json")):
        for row in json.loads(f.read_text(encoding="utf-8")).get("items", []):
            if row["key"] == key:
                out += [c["image_url"] for c in row["images"]]
    return out


def run(batch, tag, shape, prefer, n, extra):
    p = R.ep_paths(EP)
    out = p["build"] / f"codex_b2_{tag}.json"
    if out.exists():
        return f"{tag} 已有，跳过"
    seen = sum((seen_urls(R.item_key(i, it)) for i, it in batch), [])
    prompt = R.PROMPT.format(shape=shape, n=n + 2, prefer=prefer, subjects="\n".join(R.subject_line(i, it) for i, it in batch))
    prompt += EXTRA.format(n=n, seen=", ".join(seen) or "none", extra=extra)
    schema = p["build"] / "codex_schema.json"
    argv = [shutil.which("codex") or "codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
            "--output-schema", str(schema), "-o", str(out), "-"]
    req = {"argv": argv, "prompt": prompt, "purpose": "排行榜主图候选链接补搜（follow-up 016，只找链接，不生成图）", "output": str(out), "cost": "ChatGPT 订阅额度，未知"}
    r = R.RequestLog(EP).invoke("codex_cli", "web_search", req, lambda: subprocess.run(
        argv, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1500))
    return f"{tag} rc={r.returncode} {'ok' if out.exists() else 'NO OUTPUT ' + r.stderr[-200:]}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", type=int, default=None)
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--batch", type=int, default=5)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--tag", default="r2")
    ap.add_argument("--extra", default="")
    a = ap.parse_args()
    data, _ = R.load(EP)
    lay = data.get("layout") or {}
    shape = "portrait (3:4)" if lay.get("card_w", 600) / R.CARD_H < 0.8 else "near-square (9:10)"
    prefer = lay.get("image_prefer") or "the classic recognisable view"
    items = [(i, it) for i, it in enumerate(data["items"]) if a.only is None or i in a.only]
    batches = [items[k:k + a.batch] for k in range(0, len(items), a.batch)]
    with ThreadPoolExecutor(a.workers) as ex:
        for msg in ex.map(lambda kb: run(kb[1], f"{a.tag}_{kb[0]:02d}", shape, prefer, a.n, a.extra), enumerate(batches)):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
