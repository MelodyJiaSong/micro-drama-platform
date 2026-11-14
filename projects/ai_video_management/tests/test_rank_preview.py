"""排行榜预览（follow-up 320）：系列总览、单期审片数据、推荐审看版本与路径限制；列表期与公司卡字段（follow-up 321）。"""
from __future__ import annotations

import json
import struct
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.queries.rank_preview__query import RankPreviewQuery
from libs.common.origin import BoundOrigin
from libs.domain.errors.drama__error import DramaNotFoundError, InvalidDramaPathError
from libs.infrastructure.readers.rank_preview__reader import RankPreviewReader, mp4_duration, verdict_of

SERIES = "ai_videos/paihangbang"
EP = f"{SERIES}/episodes/ep02_peaks"


def mp4(seconds: int) -> bytes:
    """ftyp + moov/mvhd（v0，timescale 1000）+ mdat。"""
    mvhd_body = bytes(4) + bytes(8) + struct.pack(">II", 1000, seconds * 1000) + bytes(80)
    mvhd = struct.pack(">I4s", 8 + len(mvhd_body), b"mvhd") + mvhd_body
    moov = struct.pack(">I4s", 8 + len(mvhd), b"moov") + mvhd
    return struct.pack(">I4s", 16, b"ftyp") + b"isom" + bytes(4) + moov + struct.pack(">I4s", 12, b"mdat") + bytes(4)


def write(root: Path, rel: str, data: bytes | str = b"x") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)
    return path


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    data = {
        "episode": "ep02_peaks", "title": "Highest Peaks", "kicker": "TOP 3", "theme": "alpine", "period_label": "Nov 2026",
        "source_line": "Sources: Wikidata", "scope_note": "One per country.",
        "items": [
            {"rank": 3, "name": "K2", "country_iso2": "PK", "country_name": "Pakistan", "value_display": "8,611 m",
             "image": "assets/img/03.jpg", "image_risk": "licence unknown", "image_alt": "assets/img/03_alt.jpg"},
            {"rank": 1, "name": "Everest", "country_iso2": "CN", "value_display": "8,849 m", "badge": "SHARED",
             "image": "assets/img/01.jpg"},
            {"rank": 1, "name": "Everest", "country_iso2": "NP", "image": "../../../../etc/passwd"},
        ],
        "insights": [{"after_rank": 2, "text": "Next: Everest."}, {"text": ""}],
    }
    assets = [{"file": "assets/img/01.jpg", "licence": "Unsplash License", "author": "Ben", "source_page": "https://u/1"},
              {"file": "assets/img/03_alt.jpg", "licence": "AI-generated (Codex image_gen)", "author": "Codex"}]
    write(tmp_path, f"{EP}/data.json", json.dumps(data))
    write(tmp_path, f"{EP}/assets.json", json.dumps(assets))
    for rel in ("assets/img/01.jpg", "assets/img/03.jpg", "assets/img/03_alt.jpg", "render/thumbnail.png"):
        write(tmp_path, f"{EP}/{rel}")
    write(tmp_path, f"{SERIES}/_assets/flags/cn.png")
    write(tmp_path, f"{EP}/render/ep02_peaks_master.mp4", mp4(300))
    write(tmp_path, f"{EP}/render/ep02_peaks_master.manifest.json", json.dumps({"duration_s": 301.5, "inputs": {"music": [{"path": "a.mp3"}]}}))
    write(tmp_path, f"{EP}/render/ep02_peaks_master_with-risk-images.mp4", mp4(300))
    write(tmp_path, f"{EP}/render/ep02_peaks_master_with-risk-images.manifest.json", json.dumps({"duration_s": 301.5, "inputs": {}}))
    write(tmp_path, f"{EP}/render/ep02_peaks_bgm_v2.mp4", struct.pack(">I4s", 16, b"ftyp") + bytes(8) + struct.pack(">I4s", 0, b"mdat"))
    write(tmp_path, f"{EP}/qc.md", "# 审片\n\n## 结论：**修后可发布**\n\n旧\n\n## 第 2 轮\n\n**结论：可发布。**\n\n- 细节\n")
    write(tmp_path, f"{EP}/_build/handoff.md", "# 交接\n待用户决定：换图")
    write(tmp_path, f"{SERIES}/episodes/ep11_ships/data.json", "{broken")
    write(tmp_path, f"{SERIES}/episodes/ep11_ships/notes.txt")
    (tmp_path / SERIES / "episodes" / "_shared").mkdir()
    return tmp_path


def read(repo: Path, path: str):
    return RankPreviewQuery(RankPreviewReader(repo)).read(path)


def test_episode_reads_items_images_and_docs(repo: Path) -> None:
    ep = read(repo, EP).episode
    assert ep is not None
    assert (ep.card.title, ep.card.n, ep.card.champion, ep.kicker, ep.period_label, ep.scope_note) == (
        "Highest Peaks", 3, "Everest / Everest", "TOP 3", "Nov 2026", "One per country.")
    assert [i.rank for i in ep.items] == [1, 1, 3]
    everest, escaped, k2 = ep.items
    assert everest.flag == f"{SERIES}/_assets/flags/cn.png" and k2.flag == ""
    assert everest.image is not None and (everest.image.path, everest.image.licence, everest.image.author, everest.image.source) == (
        f"{EP}/assets/img/01.jpg", "Unsplash License", "Ben", "https://u/1")
    assert escaped.image is not None and escaped.image.path == ""          # 跑出期目录的路径不给
    assert k2.image_risk == "licence unknown" and k2.image_alt is not None and k2.image_alt.ai
    assert ep.card.stats.__dict__ == {"items": 3, "with_image": 2, "missing": 1, "risk": 1, "alt": 1, "ai": 1}
    assert [(i.after_rank, i.text) for i in ep.insights] == [(2, "Next: Everest.")]
    assert ep.card.verdict == "结论：可发布。" and ep.verdict_excerpt.startswith("## 第 2 轮")
    assert ep.publish.path == "" and ep.handoff.text.startswith("# 交接")
    assert ep.card.thumbnail == f"{EP}/render/thumbnail.png"


def test_videos_pick_the_recommended_cut(repo: Path) -> None:
    ep = read(repo, EP).episode
    assert ep is not None
    by_name = {v.name: v for v in ep.videos}
    assert [v.name for v in ep.videos][:2] == ["ep02_peaks_master.mp4", "ep02_peaks_master_with-risk-images.mp4"]
    master, risk, bgm = by_name["ep02_peaks_master.mp4"], by_name["ep02_peaks_master_with-risk-images.mp4"], by_name["ep02_peaks_bgm_v2.mp4"]
    assert (master.music, risk.music) == (True, False)
    assert master.recommended and not risk.recommended                   # 有配乐默认版 > 无配乐风险版
    assert not bgm.complete and not bgm.recommended and bgm.duration_s is None   # 还在渲染（没有 moov）
    assert master.duration_s == 301.5 and ep.card.duration_s == 301.5 and ep.card.music is True


def test_music_risk_cut_wins(repo: Path) -> None:
    write(repo, f"{EP}/render/ep02_peaks_master_with-risk-images.manifest.json", json.dumps({"inputs": {"music": [{"path": "b.mp3"}]}}))
    ep = read(repo, EP).episode
    assert ep is not None
    best = [v for v in ep.videos if v.recommended]
    assert [v.name for v in best] == ["ep02_peaks_master_with-risk-images.mp4"] and best[0].duration_s == 300.0


def test_series_lists_every_episode_by_number(repo: Path) -> None:
    series = read(repo, SERIES).series
    assert series is not None
    assert [c.key for c in series.episodes] == ["ep02_peaks", "ep11_ships"]
    ships = series.episodes[1]
    assert (ships.number, ships.n, ships.videos, ships.thumbnail, ships.verdict) == (11, 0, 0, "", "")
    assert ships.error.startswith("读不了 data.json") and 11 in series.focus


def test_mp4_duration_and_verdict_helpers(tmp_path: Path) -> None:
    assert mp4_duration(write(tmp_path, "a.mp4", mp4(12))) == 12.0
    assert mp4_duration(write(tmp_path, "b.mp4", b"junk")) is None
    assert verdict_of("# x\n\nno verdict here") == ("", "# x\n\nno verdict here")
    assert verdict_of("## Verdict: PASS\nok")[0] == "Verdict: PASS"


@pytest.mark.parametrize("path", ["", "ai_videos", f"{SERIES}/episodes", f"{EP}/render", f"{SERIES}/../dota",
                                  f"{SERIES}/episodes/../episodes/ep02_peaks", "ai_videos/other/episodes/ep02_peaks"])
def test_rejects_paths_outside_the_series(repo: Path, path: str) -> None:
    with pytest.raises(InvalidDramaPathError):
        read(repo, path)


def test_missing_episode_is_not_found(repo: Path) -> None:
    with pytest.raises(DramaNotFoundError):
        read(repo, f"{SERIES}/episodes/ep99_none")


LIST_EP = f"{SERIES}/episodes/ep03_ai"


@pytest.fixture
def list_repo(repo: Path) -> Path:
    """在 rank 期旁边造一个最小的列表期（契约 v1.3 mode=list + 公司卡字段）。"""
    data = {
        "episode": "ep03_ai", "mode": "list", "title": "AI Companies",
        "items": [
            {"rank": 1, "name": "DeepMind", "corner": "EST. 2010", "logo": "assets/logo/dm.png", "logo_bg": "#0d0b26",
             "person": {"name": "Demis Hassabis", "role": "Co-founder", "image": "assets/person/dm.jpg", "image_risk": "licence unknown"},
             "image": "assets/img/01.jpg", "image_risk": "news-agency photo (Getty/Reuters/AP): highest takedown risk",
             "image_alt": "assets/img/01_alt.jpg", "image_alt_credit": "AI-generated illustration",
             "secondary_display": "since 2014", "notes": "Subsidiary."},
            {"rank": 2, "name": "OpenAI", "corner": "est. 2015", "logo": "assets/logo/missing.png",
             "logo_bg": "red;background:url(x)", "person": {"name": "Sam Altman"}, "value_display": "$852B"},
        ],
    }
    write(repo, f"{LIST_EP}/data.json", json.dumps(data))
    write(repo, f"{LIST_EP}/assets.json", json.dumps([{"file": "assets/logo/dm.png", "kind": "logo", "licence": "Trademark"}]))
    for rel in ("assets/logo/dm.png", "assets/person/dm.jpg", "assets/img/01.jpg", "assets/img/01_alt.jpg"):
        write(repo, f"{LIST_EP}/{rel}")
    return repo


def test_list_episode_has_no_champion(list_repo: Path) -> None:
    ep = read(list_repo, LIST_EP).episode
    assert ep is not None
    c = ep.card
    assert (c.mode, c.champion, c.first, c.last, c.list_order) == ("list", "", "DeepMind", "OpenAI", "成立年份")
    dm, oa = ep.items
    assert (dm.corner, dm.logo_bg, dm.secondary_display, dm.notes, dm.image_alt_credit) == (
        "EST. 2010", "#0d0b26", "since 2014", "Subsidiary.", "AI-generated illustration")
    assert dm.logo is not None and dm.logo.path == f"{LIST_EP}/assets/logo/dm.png" and dm.logo.licence == "Trademark"
    assert dm.person is not None and (dm.person.name, dm.person.role, dm.person.image_risk) == ("Demis Hassabis", "Co-founder", "licence unknown")
    assert dm.person.image is not None and dm.person.image.path == f"{LIST_EP}/assets/person/dm.jpg"
    assert dm.image_risk.startswith("news-agency")
    assert oa.logo is not None and oa.logo.path == "" and oa.logo_bg == ""          # 文件不在；底色不是颜色值不收
    assert oa.person is not None and oa.person.image is None and oa.notes == ""


def test_list_order_unknown_without_founding_corners(list_repo: Path) -> None:
    raw = json.loads((list_repo / LIST_EP / "data.json").read_text(encoding="utf-8"))
    raw["items"][1]["corner"] = "NEW"
    write(list_repo, f"{LIST_EP}/data.json", json.dumps(raw))
    card = read(list_repo, LIST_EP).episode.card  # type: ignore[union-attr]
    assert (card.mode, card.list_order, card.champion) == ("list", "", "")


def test_rank_episode_keeps_champion_and_empty_company_fields(repo: Path) -> None:
    ep = read(repo, EP).episode
    assert ep is not None
    assert (ep.card.mode, ep.card.first, ep.card.last, ep.card.list_order) == ("rank", "", "", "")
    assert all(i.corner == "" and i.logo is None and i.person is None and i.notes == "" for i in ep.items)


def test_api_returns_series_and_episode(repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container

    container = Container()
    container.repo_root_path.override(repo)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    series = client.get("/api/rank-preview", params={"path": SERIES}).json()
    assert series["kind"] == "series" and series["episode"] is None
    assert [e["key"] for e in series["series"]["episodes"]] == ["ep02_peaks", "ep11_ships"]
    ep = client.get("/api/rank-preview", params={"path": f"{EP}/"}).json()
    assert ep["kind"] == "episode" and ep["episode"]["items"][0]["image"]["licence"] == "Unsplash License"
    bad = client.get("/api/rank-preview", params={"path": f"{SERIES}/../dota"})
    assert bad.status_code == 400 and bad.json()["detail"]["kind"] == "invalid_drama_path"
    assert client.get("/api/rank-preview", params={"path": f"{SERIES}/episodes/ep99"}).status_code == 404


def test_api_list_episode(list_repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container

    container = Container()
    container.repo_root_path.override(list_repo)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    ep = client.get("/api/rank-preview", params={"path": LIST_EP}).json()["episode"]
    assert ep["card"]["mode"] == "list" and ep["card"]["champion"] == ""
    assert ep["items"][0]["person"]["name"] == "Demis Hassabis" and ep["items"][0]["logo"]["declared"] == "assets/logo/dm.png"
    series = client.get("/api/rank-preview", params={"path": SERIES}).json()["series"]["episodes"]
    assert [(e["key"], e["mode"], e["champion"]) for e in series] == [
        ("ep02_peaks", "rank", "Everest / Everest"), ("ep03_ai", "list", ""), ("ep11_ships", "rank", "")]
