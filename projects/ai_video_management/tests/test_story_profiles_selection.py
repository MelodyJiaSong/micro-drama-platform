from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.commands.story_run__command import StoryRunCommand
from libs.application.queries.story_input__query import StoryInputQuery
from libs.application.queries.story_runs__query import StoryRunsQuery
from libs.common.episode_workflow import WORKFLOW_ID, fingerprint
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.common.story_runs import STORY_INPUT_FILE, STORY_SELECTION_FILE, StoryRunsError
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.readers.story_input__reader import StoryInputReader
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader
from libs.infrastructure.readers.story_selection__reader import StorySelectionReader
from libs.infrastructure.writers.story_runs__writer import StoryRunsWriter
from libs.infrastructure.readers.tree__reader import TreeReader
from tests.conftest import make_app
from tests.test_story_runs import EPISODE, INPUT


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


@pytest.fixture
def system(tmp_path: Path):
    (tmp_path / EPISODE).mkdir(parents=True)
    (tmp_path / "ai_videos/demo/episodes/ep02").mkdir()
    write_json(tmp_path / "ai_videos/demo/workflow.json", {"workflow": WORKFLOW_ID})
    profiles = []
    for key, rules in (("baseline-v1", []), ("workflow-v2", [{"path": "explicit.md", "sha256": "abc", "content": "更明确的规则", "selection": "explicit"}])):
        folder = f"shared/profiles/{key}"
        source = {**copy.deepcopy(INPUT), "rules_path": "rules.json"}
        source.pop("rules")
        write_json(tmp_path / EPISODE / folder / "input.json", source)
        write_json(tmp_path / EPISODE / folder / "rules.json", {"schema_version": 1, "rules": rules})
        profiles.append({"id": key, "label": key, "input_path": f"{folder}/input.json", "rules_path": f"{folder}/rules.json"})
    write_json(tmp_path / EPISODE / STORY_INPUT_FILE, {"schema_version": 1, "selected_profile": "baseline-v1", "profiles": profiles})
    reader, selections, workflows, inputs = StoryRunsReader(tmp_path), StorySelectionReader(tmp_path), EpisodeWorkflowReader(tmp_path), StoryInputReader(tmp_path)
    command = StoryRunCommand(reader, StoryRunsWriter(tmp_path), inputs, selections, workflows)
    return tmp_path, command, StoryRunsQuery(reader, selections, workflows), StoryInputQuery(inputs)


def finish(root: Path, run: dict, text: str, title: str) -> dict:
    path = root / run["audit_path"]
    document = json.loads(path.read_text(encoding="utf-8"))
    document["status"] = "ready_for_review"
    document["candidate"].update(text=text, title=title)
    write_json(path, document)
    return document


def test_current_episode_link_tracks_promotion_without_duplicating_documents(system):
    root, command, _, _ = system

    class Exposed:
        def __init__(self, folder: Path):
            self.root = folder

        def excluded_dirs(self):
            return set()

    def current():
        tree = TreeReader(Exposed(root))._walk_project(root / "ai_videos/demo")
        story = next(stage for stage in tree["children"] if stage["name"] == "story")
        episode = story["children"][0]
        return next(node for node in episode["children"] if node["name"] == "current")

    assert current()["children"] == []
    first, second = command.begin(EPISODE, INPUT), command.begin(EPISODE, INPUT)
    finish(root, first, "第一稿", "Run1")
    finish(root, second, "第二稿", "Run2")
    before = [(root / item["audit_path"]).read_bytes() for item in (first, second)]
    for run, label in ((first, "run1"), (second, "run2"), (first, "run1")):
        command.promote(EPISODE, run["run_id"])
        link = current()
        assert link["type"] == "story_runs" and link["is_link"] is True
        assert link["display_name"] == f"当前 EP1 → {label}"
        assert link["story_run_id"] == run["run_id"]
        assert link["story_run_source"] == run["audit_path"].rsplit("/", 1)[0] + "/story.md"
        assert "children" not in link
    assert [(root / item["audit_path"]).read_bytes() for item in (first, second)] == before


def test_profiles_compose_without_metadata_and_baseline_hash_matches_frozen_run(system):
    root, command, _, inputs = system
    original = command.begin(EPISODE, INPUT)
    view = inputs.read(EPISODE)
    assert view.profile_id == view.selected_profile == "baseline-v1"
    assert view.input == original["input"]
    assert view.input["input_hash"] == original["input"]["input_hash"]
    assert "rules_path" not in view.input
    assert "profile_id" not in view.input
    second = command.begin_from_file(EPISODE, str(root / EPISODE / "shared/profiles/baseline-v1/input.json"))
    assert second["input"] == original["input"]
    updated = inputs.read(EPISODE, "workflow-v2")
    assert updated.input["input_hash"] != original["input"]["input_hash"]
    assert updated.profiles[0]["rules_hash"] == fingerprint([])
    assert updated.profiles[1]["rules_hash"] == fingerprint(updated.input["rules"])
    old_bytes = (root / original["audit_path"]).read_bytes()
    write_json(root / EPISODE / "shared/profiles/baseline-v1/rules.json", {"schema_version": 1, "rules": ["modified shared rule"]})
    assert inputs.read(EPISODE).input["input_hash"] != original["input"]["input_hash"]
    assert (root / original["audit_path"]).read_bytes() == old_bytes


@pytest.mark.parametrize("bad", ["../ep02/input.json", "shared/../../ep02/input.json", "shared/./profiles/baseline-v1/input.json", "C:/outside/input.json", "shared/profiles/baseline-v1/../../../ep02/input.json"])
def test_profile_paths_cannot_escape_episode_shared(system, bad):
    root, _, _, inputs = system
    index_path = root / EPISODE / STORY_INPUT_FILE
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["profiles"][0]["input_path"] = bad
    write_json(index_path, index)
    with pytest.raises(StoryRunsError) as error:
        inputs.read(EPISODE)
    assert error.value.status_code == 400


@pytest.mark.parametrize("rules_path", ["../rules.json", "../../ep02/rules.json", "/rules.json", "folder/rules.json", "C:rules.json", "rules\\rules.json"])
def test_relative_rule_path_must_remain_same_folder(system, rules_path):
    root, command, _, inputs = system
    path = root / EPISODE / "shared/profiles/baseline-v1/input.json"
    source = json.loads(path.read_text(encoding="utf-8"))
    source["rules_path"] = rules_path
    write_json(path, source)
    for action in (lambda: inputs.read(EPISODE), lambda: command.begin_from_file(EPISODE, str(path))):
        with pytest.raises(StoryRunsError) as error:
            action()
        assert error.value.status_code == 400


def test_shared_input_api_and_missing_profile(system):
    root, _, _, inputs = system
    client = TestClient(make_app(RepoRoot(path=root), BoundOrigin(host="127.0.0.1", port=8766)), base_url="http://127.0.0.1:8766")
    response = client.get("/api/story-input", params={"episode_path": EPISODE})
    assert response.status_code == 200
    assert response.json()["input"] == inputs.read(EPISODE).input
    assert client.get("/api/story-input", params={"episode_path": EPISODE, "profile_id": "workflow-v2"}).json()["profile_id"] == "workflow-v2"
    assert client.get("/api/story-input", params={"episode_path": EPISODE, "profile_id": "missing"}).status_code == 404
    assert client.get("/api/story-input", params={"episode_path": "ai_videos/demo/episodes/ep02"}).status_code in {400, 404}
    assert client.post("/api/story-input", json={}).status_code == 405


def test_two_promotions_and_switch_back_preserve_runs_states_and_downstream(system):
    root, command, runs, _ = system
    first, second = command.begin(EPISODE, INPUT), command.begin(EPISODE, INPUT)
    finish(root, first, "第一个候选正文", "第一版")
    finish(root, second, "第二个候选正文", "第二版")
    state = root / EPISODE / "state_changes.md"
    state.write_text("未确定状态保持原样", encoding="utf-8")
    run_bytes = {run["run_id"]: (root / run["audit_path"]).read_bytes() for run in (first, second)}
    command.promote(EPISODE, first["run_id"])
    story_path = root / EPISODE / "story.json"
    story = json.loads(story_path.read_text(encoding="utf-8"))
    assert story["content"]["text"] == "第一个候选正文"
    assert story["approved_revision"] is None
    revision = runs.read(EPISODE).selection["story_revision"]
    story["approved_revision"] = revision
    write_json(story_path, story)
    filming = {"content": {"scenes": [{"id": "s1", "background": "", "location": "树林", "time": "白天", "purpose": "出发", "shots": [{"id": "st1", "duration": 5, "action": "走路", "camera": "固定", "dialogue": ""}]}]},
               "source_revision": revision, "approved_revision": None}
    write_json(root / EPISODE / "filming.json", filming)
    before_filming = (root / EPISODE / "filming.json").read_bytes()
    selected = command.promote(EPISODE, second["run_id"])
    assert selected["status"] == "selected" and selected["story_status"] == "draft"
    assert len(selected["history"]) == 2
    assert runs.read(EPISODE).selection["run_id"] == second["run_id"]
    from libs.domain.entities.episode_workflow__entity import EpisodeWorkflowEntity
    entity = EpisodeWorkflowEntity(EpisodeWorkflowReader(root).read(EPISODE).documents)
    assert entity.status("story") == "draft"
    assert entity.status("filming") == "stale"
    assert (root / EPISODE / "filming.json").read_bytes() == before_filming
    command.promote(EPISODE, first["run_id"])
    view = runs.read(EPISODE)
    assert [event["run_id"] for event in view.selection["history"]] == [first["run_id"], second["run_id"], first["run_id"]]
    assert view.selection["status"] == "selected"
    assert [run["selected"] for run in view.runs] == [True, False]
    assert view.runs[0]["title"] == "第一版"
    for run in (first, second):
        assert (root / run["audit_path"]).read_bytes() == run_bytes[run["run_id"]]
    assert state.read_text(encoding="utf-8") == "未确定状态保持原样"


@pytest.mark.parametrize("target", ["story", "candidate"])
def test_selection_stales_when_binding_changes(system, target):
    root, command, runs, _ = system
    first = command.begin(EPISODE, INPUT)
    finish(root, first, "完整候选", "第一版")
    command.promote(EPISODE, first["run_id"])
    if target == "story":
        path = root / EPISODE / "story.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc["content"]["text"] = "工作区已经另改"
    else:
        path = root / first["audit_path"]
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc["candidate"]["text"] = "候选已经另改"
    write_json(path, doc)
    view = runs.read(EPISODE)
    assert view.selection["status"] == "stale"
    assert all(not run["selected"] for run in view.runs)


def test_incomplete_and_other_episode_runs_cannot_be_promoted(system):
    root, command, _, _ = system
    incomplete = command.begin(EPISODE, INPUT)
    with pytest.raises(StoryRunsError):
        command.promote(EPISODE, incomplete["run_id"])
    future = command.begin("ai_videos/demo/episodes/ep02", INPUT)
    finish(root, future, "未来集的候选", "不能混入EP1")
    with pytest.raises(StoryRunsError) as error:
        command.promote(EPISODE, future["run_id"])
    assert error.value.status_code == 404
    assert not (root / EPISODE / "story.json").exists()
    assert not (root / EPISODE / STORY_SELECTION_FILE).exists()


def test_explicit_shared_input_from_other_episode_is_refused(system):
    root, command, _, _ = system
    future = root / "ai_videos/demo/episodes/ep02/shared/input.json"
    write_json(future, INPUT)
    with pytest.raises(StoryRunsError) as error:
        command.begin_from_file(EPISODE, str(future))
    assert error.value.status_code == 400


def test_cli_begin_composes_rules_and_promote_loads_draft(system):
    root, _, runs, inputs = system
    entry = Path(__file__).resolve().parents[3] / "tools/story_run.py"
    args = [sys.executable, str(entry)]
    result = subprocess.run([*args, "begin", "--episode-path", EPISODE, "--input", str(root / EPISODE / "shared/profiles/baseline-v1/input.json")],
                            cwd=root, text=True, capture_output=True, check=True)
    run = json.loads(result.stdout)
    assert runs.detail(EPISODE, run["run_id"])["input"] == inputs.read(EPISODE).input
    finish(root, run, "CLI候选正文", "CLI第一版")
    result = subprocess.run([*args, "promote", "--episode-path", EPISODE, "--run-id", run["run_id"]],
                            cwd=root, text=True, capture_output=True, check=True)
    assert json.loads(result.stdout)["story_status"] == "draft"
    assert runs.read(EPISODE).selection["run_id"] == run["run_id"]
