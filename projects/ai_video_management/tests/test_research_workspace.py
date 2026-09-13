"""Research workspace: the user's decisions, kept separate from the dataset."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.infrastructure.errors.research__error import ResearchError
from libs.infrastructure.readers.research__reader import ResearchReader
from libs.infrastructure.writers.research__writer import ResearchWriter

DATASET = {
    "schema_version": 1,
    "title": "t",
    "series": [
        {
            "rank": 1,
            "slug": "alpha",
            "name_zh": "甲",
            "videos": [{"video_id": "vid00000001"}, {"video_id": "vid00000002"}],
        },
        {"rank": 2, "slug": "beta", "name_zh": "乙", "videos": [{"video_id": "vid00000003"}]},
    ],
}


@pytest.fixture()
def writer(tmp_path: Path) -> ResearchWriter:
    research = tmp_path / "ai_videos" / "_research"
    research.mkdir(parents=True)
    (research / "ds.json").write_text(json.dumps(DATASET, ensure_ascii=False), encoding="utf-8")
    return ResearchWriter(tmp_path, ResearchReader(tmp_path))


def test_workspace_defaults_to_empty(writer: ResearchWriter) -> None:
    assert writer.workspace("ds") == {"dataset": "ds", "series": {}, "videos": {}}


def test_mark_series_persists_and_merges(writer: ResearchWriter) -> None:
    writer.mark_series("ds", "alpha", "shortlist", None, None)
    writer.mark_series("ds", "alpha", None, 4, None)
    writer.mark_series("ds", "alpha", None, None, "先做这个")
    assert writer.workspace("ds")["series"]["alpha"] == {
        "status": "shortlist",
        "rating": 4,
        "note": "先做这个",
    }


def test_marking_back_to_empty_drops_the_entry(writer: ResearchWriter) -> None:
    writer.mark_series("ds", "alpha", "shortlist", None, None)
    writer.mark_series("ds", "alpha", "none", 0, "")
    assert writer.workspace("ds")["series"] == {}


def test_mark_video_bookmark_and_note(writer: ResearchWriter) -> None:
    writer.mark_video("ds", "vid00000002", True, "封面参考")
    assert writer.workspace("ds")["videos"]["vid00000002"] == {
        "bookmarked": True,
        "note": "封面参考",
    }
    writer.mark_video("ds", "vid00000002", False, "")
    assert writer.workspace("ds")["videos"] == {}


def test_unknown_series_rejected(writer: ResearchWriter) -> None:
    with pytest.raises(ResearchError) as exc:
        writer.mark_series("ds", "ghost", "shortlist", None, None)
    assert exc.value.kind == "not_found"


def test_unknown_video_rejected(writer: ResearchWriter) -> None:
    with pytest.raises(ResearchError) as exc:
        writer.mark_video("ds", "notinset01", True, None)
    assert exc.value.kind == "not_found"


@pytest.mark.parametrize("status", ["maybe", "SHORTLIST", "done"])
def test_bad_status_rejected(writer: ResearchWriter, status: str) -> None:
    with pytest.raises(ResearchError) as exc:
        writer.mark_series("ds", "alpha", status, None, None)
    assert exc.value.kind == "bad_status"


@pytest.mark.parametrize("rating", [-1, 6, 99])
def test_rating_out_of_range_rejected(writer: ResearchWriter, rating: int) -> None:
    with pytest.raises(ResearchError) as exc:
        writer.mark_series("ds", "alpha", None, rating, None)
    assert exc.value.kind == "bad_rating"


def test_oversized_note_rejected(writer: ResearchWriter) -> None:
    with pytest.raises(ResearchError) as exc:
        writer.mark_series("ds", "alpha", None, None, "x" * 4001)
    assert exc.value.kind == "note_too_long"


def test_workspace_file_sits_beside_the_dataset_not_inside_it(
    writer: ResearchWriter, tmp_path: Path
) -> None:
    writer.mark_series("ds", "alpha", "doing", None, None)
    research = tmp_path / "ai_videos" / "_research"
    assert (research / "ds.workspace.json").is_file()
    # the dataset itself is untouched — a re-run of the research must not clobber decisions
    assert json.loads((research / "ds.json").read_text(encoding="utf-8")) == DATASET


def test_decisions_survive_a_dataset_regeneration(writer: ResearchWriter, tmp_path: Path) -> None:
    writer.mark_series("ds", "beta", "shortlist", 5, "保留")
    regenerated = json.loads(json.dumps(DATASET))
    regenerated["series"][1]["rank"] = 9
    regenerated["series"][1]["name_zh"] = "乙（改名）"
    (tmp_path / "ai_videos" / "_research" / "ds.json").write_text(
        json.dumps(regenerated, ensure_ascii=False), encoding="utf-8"
    )
    assert writer.workspace("ds")["series"]["beta"] == {
        "status": "shortlist",
        "rating": 5,
        "note": "保留",
    }
