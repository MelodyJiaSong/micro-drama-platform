"""Research module: reader over a fake ai_videos/_research tree."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.infrastructure.errors.research__error import ResearchError
from libs.infrastructure.readers.research__reader import ResearchReader

DATASET = {
    "schema_version": 1,
    "title": "近半年 YouTube AIGC 系列排行",
    "generated_at": "2026-09-06",
    "window": {"from": "20260306", "to": "20260906"},
    "method": "yt-dlp 实测",
    "criteria": ["点赞率 + 播放量", "单人可翻拍"],
    "series": [
        {
            "rank": 1,
            "slug": "demo-series",
            "name_zh": "演示系列",
            "name_en": "Demo Series",
            "videos": [{"video_id": "abc123", "view_count": 10, "like_count": 1}],
        }
    ],
}


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    research = tmp_path / "ai_videos" / "_research"
    research.mkdir(parents=True)
    (research / "youtube_series.json").write_text(
        json.dumps(DATASET, ensure_ascii=False), encoding="utf-8"
    )
    return tmp_path


def test_datasets_lists_summary(repo_root: Path) -> None:
    rows = ResearchReader(repo_root).datasets()
    assert [r["dataset"] for r in rows] == ["youtube_series"]
    assert rows[0]["series_count"] == 1
    assert rows[0]["generated_at"] == "2026-09-06"


def test_datasets_empty_when_surface_absent(tmp_path: Path) -> None:
    assert ResearchReader(tmp_path).datasets() == []


def test_dataset_returns_full_payload(repo_root: Path) -> None:
    data = ResearchReader(repo_root).dataset("youtube_series")
    assert data["window"] == {"from": "20260306", "to": "20260906"}
    assert data["series"][0]["name_zh"] == "演示系列"


def test_series_lookup_by_slug(repo_root: Path) -> None:
    series = ResearchReader(repo_root).series("youtube_series", "demo-series")
    assert series["rank"] == 1


def test_unknown_series_is_not_found(repo_root: Path) -> None:
    with pytest.raises(ResearchError) as exc:
        ResearchReader(repo_root).series("youtube_series", "nope")
    assert exc.value.kind == "not_found"


def test_missing_dataset_is_not_found(repo_root: Path) -> None:
    with pytest.raises(ResearchError) as exc:
        ResearchReader(repo_root).dataset("absent")
    assert exc.value.kind == "not_found"


@pytest.mark.parametrize("name", ["../secrets", "youtube series", "Upper", "a/b"])
def test_traversal_and_odd_names_rejected(repo_root: Path, name: str) -> None:
    with pytest.raises(ResearchError) as exc:
        ResearchReader(repo_root).dataset(name)
    assert exc.value.kind == "bad_name"


def test_malformed_json_reported_not_crashed(repo_root: Path) -> None:
    (repo_root / "ai_videos" / "_research" / "broken.json").write_text("{nope", encoding="utf-8")
    with pytest.raises(ResearchError) as exc:
        ResearchReader(repo_root).dataset("broken")
    assert exc.value.kind == "bad_json"
    # a broken file must not take the whole listing down with it
    assert [r["dataset"] for r in ResearchReader(repo_root).datasets()] == ["youtube_series"]


def test_dataset_without_series_array_rejected(repo_root: Path) -> None:
    (repo_root / "ai_videos" / "_research" / "shapeless.json").write_text(
        json.dumps({"title": "x"}), encoding="utf-8"
    )
    with pytest.raises(ResearchError) as exc:
        ResearchReader(repo_root).dataset("shapeless")
    assert exc.value.kind == "bad_shape"
