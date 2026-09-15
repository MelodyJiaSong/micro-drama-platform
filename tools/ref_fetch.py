"""Historical reference-image fetcher for `ai_videos/` assets (proposal G §7, follow-up 004).

Every scene / prop / costume / food asset gets a `ref/` folder of historical reference images
plus a tracked `refs.md` index (URL, collection, accession, date, license, what it evidences).
Images themselves are media and stay out of git (R2 via assets_sync); only `refs.md` is tracked.

    search <query>... [--source met,commons] [--limit N]      candidates as JSON Lines on stdout
    pull   <asset_dir> <source:id>...                          download into <asset_dir>/ref/ + append refs.md
    register <asset_dir> <file> --source-url U --collection C  index a manually downloaded file

Only key-less open APIs are wired (Met Collection API, Wikimedia Commons). Collections without
an API (故宫名画记, 台北故宫 Open Data, 考古报告图版) are downloaded by hand and `register`ed.
The license is recorded on every entry: anything that is not CC0 / CC-BY is marked
「只进 prompt 不入画」 so the format contract can check it (ai_video.md rule 15 / R15).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator

from ref_aspect import fit

UA = "spec_coding-ref-fetch/0.1 (https://github.com/; contact: repo owner)"
MET = "https://collectionapi.metmuseum.org/public/collection/v1"
COMMONS = "https://commons.wikimedia.org/w/api.php"
OPEN_LICENSES = ("CC0", "Public domain", "CC BY ", "CC-BY-", "CC BY-SA", "CC-BY-SA")


@dataclass(frozen=True)
class Candidate:
    source: str
    id: str
    title: str
    date: str
    license: str
    image_url: str
    page_url: str
    collection: str
    accession: str

    @property
    def key(self) -> str:
        return f"{self.source}:{self.id}"

    @property
    def usable_in_frame(self) -> bool:
        return any(self.license.startswith(p) or p in self.license for p in OPEN_LICENSES)


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def _download(url: str, dest: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp, dest.open("wb") as fh:
        data = resp.read()
        fh.write(data)
        return len(data)


# ---------------------------------------------------------------- Met
def met_object(object_id: str) -> Candidate | None:
    o = _get_json(f"{MET}/objects/{object_id}")
    image = o.get("primaryImage") or ""
    if not image:
        return None
    return Candidate(
        source="met", id=str(o["objectID"]), title=o.get("title") or "", date=o.get("objectDate") or "",
        license="CC0" if o.get("isPublicDomain") else "版权保留", image_url=image,
        page_url=o.get("objectURL") or "", collection="The Metropolitan Museum of Art",
        accession=o.get("accessionNumber") or "",
    )


def met_search(query: str, limit: int) -> Iterator[Candidate]:
    q = urllib.parse.quote(query)
    ids = _get_json(f"{MET}/search?q={q}&hasImages=true").get("objectIDs") or []
    for object_id in ids[:limit]:
        try:
            c = met_object(str(object_id))
        except urllib.error.HTTPError as e:
            if e.code == 404:  # search index lists objects whose record has since been withdrawn
                continue
            raise
        if c is not None:
            yield c


# ---------------------------------------------------------------- Wikimedia Commons
def _commons_pages(params: dict[str, str]) -> list[dict]:
    base = {"action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url|extmetadata|size|mime", "iiurlwidth": "2000"}
    data = _get_json(COMMONS + "?" + urllib.parse.urlencode({**base, **params}))
    return list((data.get("query") or {}).get("pages", {}).values())


def _commons_candidate(page: dict) -> Candidate | None:
    infos = page.get("imageinfo") or []
    if not infos:
        return None
    info = infos[0]
    meta = info.get("extmetadata") or {}
    def m(k: str) -> str:
        return re.sub(r"<[^>]+>", "", str((meta.get(k) or {}).get("value", ""))).strip()
    return Candidate(
        source="commons", id=str(page["pageid"]), title=page.get("title", "").removeprefix("File:"),
        date=m("DateTimeOriginal"), license=m("LicenseShortName") or "unknown",
        image_url=info.get("thumburl") or info.get("url") or "", page_url=info.get("descriptionurl") or "",
        collection="Wikimedia Commons · " + (m("Credit") or m("Artist"))[:80], accession="",
    )


def commons_search(query: str, limit: int) -> Iterator[Candidate]:
    for page in _commons_pages({"generator": "search", "gsrsearch": query, "gsrnamespace": "6", "gsrlimit": str(limit)}):
        c = _commons_candidate(page)
        if c is not None and c.image_url:
            yield c


def commons_page(page_id: str) -> Candidate | None:
    pages = _commons_pages({"pageids": page_id})
    return _commons_candidate(pages[0]) if pages else None


SEARCHERS = {"met": met_search, "commons": commons_search}
FETCHERS = {"met": met_object, "commons": commons_page}


# ---------------------------------------------------------------- refs.md
def _slug(text: str, n: int = 24) -> str:
    return re.sub(r"[^\w一-鿿]+", "_", text).strip("_")[:n] or "ref"


def _next_index(ref_dir: Path) -> int:
    nums = [int(m.group(1)) for p in ref_dir.iterdir() if (m := re.match(r"ref(\d+)_", p.name))]
    return max(nums, default=0) + 1


def append_ref(asset_dir: Path, file: Path, c: Candidate, evidences: list[str], use: str) -> str:
    ref_id = f"{asset_dir.name}.{file.stem.split('_')[0]}"
    entry = (
        f"- ref_id: {ref_id}\n  file: ref/{file.name}\n  source_url: {c.page_url or c.image_url}\n"
        f"  collection: {c.collection}\n  accession: {c.accession}\n  date: {c.date}\n  title: {c.title}\n"
        f"  license: {c.license}{'' if c.usable_in_frame else '（只进 prompt 不入画）'}\n"
        f"  evidences: [{', '.join(evidences)}]\n  use: {use}\n"
    )
    refs = asset_dir / "refs.md"
    if not refs.exists():
        refs.write_text(f"# {asset_dir.name} · 历史参考图索引\n\n> 图片在 `ref/`（媒体走 R2，不进 git）；本索引进 git。每张图写清它证明哪个 `fact_id`、许可能否入画。\n\n```yaml\n```\n", encoding="utf-8")
    text = refs.read_text(encoding="utf-8")
    text = text[: text.rindex("```")] + entry + "```\n"
    refs.write_text(text, encoding="utf-8")
    return ref_id


def pull(asset_dir: Path, keys: list[str], evidences: list[str], use: str) -> None:
    ref_dir = asset_dir / "ref"
    ref_dir.mkdir(parents=True, exist_ok=True)
    for key in keys:
        source, _, ident = key.partition(":")
        c = FETCHERS[source](ident)
        if c is None:
            print(f"-- {key}: no image", file=sys.stderr)
            continue
        ext = Path(urllib.parse.urlparse(c.image_url).path).suffix.lower() or ".jpg"
        file = ref_dir / f"ref{_next_index(ref_dir):02d}_{_slug(c.title)}_{source}{ext}"
        size = _download(c.image_url, file)
        fit(file)  # Seedance only accepts uploads between 1:3 and 3:1
        ref_id = append_ref(asset_dir, file, c, evidences, use)
        print(json.dumps({"ref_id": ref_id, "file": str(file), "bytes": size, "license": c.license}, ensure_ascii=False))


def register(asset_dir: Path, file: Path, c: Candidate, evidences: list[str], use: str) -> None:
    ref_dir = asset_dir / "ref"
    ref_dir.mkdir(parents=True, exist_ok=True)
    dest = file if file.parent == ref_dir else ref_dir / f"ref{_next_index(ref_dir):02d}_{_slug(file.stem)}_manual{file.suffix.lower()}"
    if dest != file:
        file.replace(dest)
    fit(dest)
    print(json.dumps({"ref_id": append_ref(asset_dir, dest, c, evidences, use), "file": str(dest)}, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and choke on Chinese titles
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query", nargs="+"); s.add_argument("--source", default="met,commons"); s.add_argument("--limit", type=int, default=15)
    p = sub.add_parser("pull"); p.add_argument("asset_dir"); p.add_argument("keys", nargs="+"); p.add_argument("--evidence", default=""); p.add_argument("--use", default="锚点 prompt 形制依据")
    r = sub.add_parser("register"); r.add_argument("asset_dir"); r.add_argument("file")
    for name in ("source-url", "collection", "accession", "date", "title", "license"):
        r.add_argument("--" + name, default="")
    r.add_argument("--evidence", default=""); r.add_argument("--use", default="锚点 prompt 形制依据")
    a = ap.parse_args(argv)
    if a.cmd == "search":
        seen: set[str] = set()
        for src in a.source.split(","):
            for q in a.query:
                for c in SEARCHERS[src](q, a.limit):
                    if c.key not in seen:
                        seen.add(c.key)
                        print(json.dumps({**asdict(c), "query": q, "usable_in_frame": c.usable_in_frame}, ensure_ascii=False))
        print(f"-- emitted {len(seen)} unique", file=sys.stderr)
    elif a.cmd == "pull":
        pull(Path(a.asset_dir), a.keys, [e for e in a.evidence.split(",") if e], a.use)
    else:
        c = Candidate("manual", "", a.title or Path(a.file).stem, a.date, a.license or "unknown", "", a.source_url, a.collection, a.accession)
        register(Path(a.asset_dir), Path(a.file), c, [e for e in a.evidence.split(",") if e], a.use)
    return 0


if __name__ == "__main__":
    sys.exit(main())
