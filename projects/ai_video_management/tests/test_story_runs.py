from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.commands.story_run__command import StoryRunCommand
from libs.application.queries.story_runs__query import StoryRunsQuery
from libs.common.episode_workflow import WORKFLOW_ID
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.common.story_runs import STORY_FRAME_FIELDS, STORY_INPUT_FILE, STORY_RUNS_FILE, STORY_RUN_INPUT_FILE, StoryRunsError
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader
from libs.infrastructure.readers.story_input__reader import StoryInputReader
from libs.infrastructure.readers.story_selection__reader import StorySelectionReader
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.readers.tree__reader import TreeReader
from libs.infrastructure.writers.story_runs__writer import StoryRunsWriter
from tests.conftest import make_app

EPISODE = "ai_videos/demo/episodes/ep01"
FRAME = dict(zip(STORY_FRAME_FIELDS, ("主角", "送信", "救人", "清晨", "北郡", "穿越树林")))
INPUT = {"frame": FRAME, "brief": "一次有代价的选择", "assumptions": [], "sources": [], "rules": [],
         "independence": {"previous_candidates": "excluded", "future_episodes": "excluded"}}


@pytest.fixture
def runs(tmp_path: Path):
    (tmp_path / EPISODE).mkdir(parents=True)
    (tmp_path / "ai_videos/demo/episodes/ep02").mkdir()
    (tmp_path / "ai_videos/demo/workflow.json").write_text(json.dumps({"workflow": WORKFLOW_ID}), encoding="utf-8")
    reader = StoryRunsReader(tmp_path)
    selections = StorySelectionReader(tmp_path)
    workflows = EpisodeWorkflowReader(tmp_path)
    return tmp_path, StoryRunsQuery(reader, selections, workflows), StoryRunCommand(
        reader, StoryRunsWriter(tmp_path), StoryInputReader(tmp_path), selections, workflows)


def test_independent_runs_freeze_inputs_and_preserve_previous_logs(runs):
    root, query, command = runs
    source = copy.deepcopy(INPUT)
    (root / EPISODE / "story.json").write_text("old discarded candidate", encoding="utf-8")
    (root / EPISODE / "state_changes.md").write_text("old unapproved state", encoding="utf-8")
    first = command.begin(EPISODE, source)
    original = (root / first["audit_path"]).read_bytes()
    frozen = (root / first["audit_path"]).parent / STORY_RUN_INPUT_FILE
    assert json.loads(frozen.read_text(encoding="utf-8")) == first["input"]
    source["frame"]["who"] = "changed outside"
    second = command.begin(EPISODE, INPUT)
    assert first["run_id"] != second["run_id"]
    assert first["input"]["input_hash"] == second["input"]["input_hash"]
    assert (root / first["audit_path"]).read_bytes() == original
    assert first["candidate"]["text"] == second["candidate"]["text"] == ""
    assert first["candidate"]["state_changes"] == []
    assert query.detail(EPISODE, first["run_id"])["input"]["frame"] == FRAME
    assert [run["run_id"] for run in query.read(EPISODE).runs] == [first["run_id"], second["run_id"]]
    assert not (root / EPISODE / ".story_runs.lock").exists()


@pytest.mark.parametrize("alter", [
    lambda value: value["frame"].pop("why"),
    lambda value: value["frame"].update(what=""),
    lambda value: value.update(sources="wrong"),
    lambda value: value.update(independence=[]),
    lambda value: value.update(not_json=object()),
    lambda value: value.update(nonfinite=float("nan")),
])
def test_bad_inputs_create_no_run_or_index(runs, alter):
    root, _, command = runs
    source = copy.deepcopy(INPUT)
    alter(source)
    with pytest.raises(StoryRunsError):
        command.begin(EPISODE, source)
    assert not (root / EPISODE / STORY_RUNS_FILE).exists()
    assert not (root / ".audit").exists()


def test_api_is_episode_scoped_and_never_exposes_unindexed_audit(runs):
    root, _, command = runs
    first = command.begin(EPISODE, INPUT)
    future_episode = "ai_videos/demo/episodes/ep02"
    future = command.begin(future_episode, INPUT)
    client = TestClient(make_app(RepoRoot(path=root), BoundOrigin(host="127.0.0.1", port=8766)), base_url="http://127.0.0.1:8766")
    response = client.get("/api/story-runs", params={"episode_path": EPISODE})
    assert response.status_code == 200
    summary = response.json()["runs"][0]
    assert summary["run_id"] == first["run_id"]
    assert summary["input_hash"] == first["input"]["input_hash"]
    assert summary["audit_path"] == first["audit_path"]
    assert summary["audit_folder"] == first["audit_path"].rsplit("/", 1)[0]
    assert response.json()["selection"] is None
    assert client.get("/api/story-runs/detail", params={"episode_path": EPISODE, "run_id": first["run_id"]}).status_code == 200
    for missing in (future["run_id"], "../../outside", "story-run-unindexed"):
        assert client.get("/api/story-runs/detail", params={"episode_path": EPISODE, "run_id": missing}).status_code == 404
    assert client.get("/api/story-runs", params={"episode_path": EPISODE + "/../../outside"}).status_code == 404
    assert client.get("/api/file", params={"path": first["audit_path"]}).status_code == 404
    assert client.post("/api/story-runs", json={}).status_code == 405


def test_missing_index_is_empty_and_bad_logs_have_safe_errors(runs):
    root, query, command = runs
    assert query.read(EPISODE).runs == []
    first = command.begin(EPISODE, INPUT)
    path = root / first["audit_path"]
    path.write_text("{bad json", encoding="utf-8")
    with pytest.raises(StoryRunsError) as error:
        query.read(EPISODE)
    assert error.value.status_code == 400
    assert ".audit" not in str(error.value)


def test_complete_observed_log_and_forward_fields_survive_unchanged(runs):
    root, query, command = runs
    first = command.begin(EPISODE, INPUT)
    path = root / first["audit_path"]
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["participants"] = [{"id": "editor", "name": "主编", "role": "editor", "scope": "story",
                            "runtime_id": None, "model": "unknown", "status": "complete", "started_at": None,
                            "finished_at": None, "prompt": "完整实际任务", "output": "完整实际回复"}]
    doc["proposals"] = [{"id": "p1", "agent_id": "editor", "title": "明确代价", "detail": "送信会失去奖励",
                         "reason": "选择需要有代价", "location": "结尾", "decision": "accepted", "decision_reason": "让结果承接选择",
                         "decided_by": "editor", "criteria": ["因果"], "evidence": ["正文结尾"], "applied_in": ["candidate.text"]}]
    doc["events"] = [{"id": "e1", "at": "2026-10-03T13:00:00+00:00", "actor": "editor", "type": "decision",
                      "title": "采纳代价", "body": "依据因果标准采纳", "proposal_ids": ["p1"], "artifact_refs": []}]
    doc["future_extension"] = {"value": "preserved"}
    path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    before = path.read_bytes()
    detail = query.detail(EPISODE, first["run_id"])
    assert detail.pop("io")["items"]
    assert detail == doc
    assert query.read(EPISODE).runs[0]["proposal_count"] == 1
    assert path.read_bytes() == before


def test_cli_creates_run_in_selected_workspace(runs):
    root, query, _ = runs
    input_path = root / "input.json"
    input_path.write_text(json.dumps(INPUT, ensure_ascii=False), encoding="utf-8")
    entry = Path(__file__).resolve().parents[3] / "tools/story_run.py"
    result = subprocess.run([sys.executable, str(entry), "begin", "--episode-path", EPISODE, "--input", str(input_path)],
                            cwd=root, text=True, capture_output=True, check=True)
    created = json.loads(result.stdout)
    assert created["audit_path"].endswith(f"{created['run_id']}/run.json")
    assert query.detail(EPISODE, created["run_id"])["input"]["frame"] == FRAME


def test_missing_log_and_duplicate_index_are_not_silently_ignored(runs):
    root, query, command = runs
    first = command.begin(EPISODE, INPUT)
    (root / first["audit_path"]).unlink()
    with pytest.raises(StoryRunsError) as error:
        query.detail(EPISODE, first["run_id"])
    assert error.value.status_code == 404
    index_path = root / EPISODE / STORY_RUNS_FILE
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["runs"].append(index["runs"][0])
    index_path.write_text(json.dumps(index), encoding="utf-8")
    with pytest.raises(StoryRunsError) as error:
        query.read(EPISODE)
    assert error.value.status_code == 400


def test_busy_index_does_not_overwrite_existing_runs(runs):
    root, _, command = runs
    first = command.begin(EPISODE, INPUT)
    index = root / EPISODE / STORY_RUNS_FILE
    before = index.read_bytes()
    lock_path = root / EPISODE / ".story_runs.lock"
    lock_path.touch()
    with pytest.raises(StoryRunsError):
        command.begin(EPISODE, INPUT)
    assert index.read_bytes() == before
    assert lock_path.exists()
    assert (root / first["audit_path"]).is_file()


@pytest.mark.parametrize("target", ["run", "snapshot"])
def test_tampered_frozen_input_is_refused(runs, target):
    root, query, command = runs
    first = command.begin(EPISODE, INPUT)
    path = root / first["audit_path"]
    if target == "snapshot":
        path = path.parent / STORY_RUN_INPUT_FILE
    doc = json.loads(path.read_text(encoding="utf-8"))
    source = doc["input"] if target == "run" else doc
    source["frame"]["what"] = "悄悄改变创作方向"
    path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(StoryRunsError) as error:
        query.detail(EPISODE, first["run_id"])
    assert error.value.status_code == 400


@pytest.mark.parametrize("path", [
    "../private/run.json", ".audit/adhoc_agents/2026-10-03/other-run/run.json",
    ".audit/adhoc_agents/2026-10-03/story-run-other/../../secret.json",
    "C:/outside/run.json", ".audit/adhoc_agents/2026-99-99/story-run-other/run.json",
])
def test_bad_audit_paths_are_refused(runs, path):
    root, query, command = runs
    command.begin(EPISODE, INPUT)
    index_path = root / EPISODE / STORY_RUNS_FILE
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["runs"][0]["audit_path"] = path
    index_path.write_text(json.dumps(index), encoding="utf-8")
    with pytest.raises(StoryRunsError) as error:
        query.read(EPISODE)
    assert error.value.status_code == 400


@pytest.mark.parametrize("field,new_value", [("episode_path", "ai_videos/demo/episodes/ep02"), ("run_id", "story-run-forged"),
                                             ("created_at", "other time"), ("participants", {}), ("schema_version", True)])
def test_cross_episode_and_corrupt_run_contract_are_refused(runs, field, new_value):
    root, query, command = runs
    first = command.begin(EPISODE, INPUT)
    path = root / first["audit_path"]
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc[field] = new_value
    path.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(StoryRunsError) as error:
        query.detail(EPISODE, first["run_id"])
    assert error.value.status_code == 400


def test_audit_file_external_symlink_is_refused(runs, tmp_path):
    root, query, command = runs
    first = command.begin(EPISODE, INPUT)
    path = root / first["audit_path"]
    external = tmp_path.parent / f"outside-{tmp_path.name}.json"
    external.write_bytes(path.read_bytes())
    path.unlink()
    try:
        path.symlink_to(external)
    except OSError:
        external.unlink()
        pytest.skip("当前Windows权限不允许创建符号链接")
    try:
        with pytest.raises(StoryRunsError) as error:
            query.detail(EPISODE, first["run_id"])
        assert error.value.status_code == 400
    finally:
        external.unlink()


def test_tree_runs_and_documents_keep_index_order_and_episode_scope(runs):
    root, _, command = runs
    run1 = command.begin(EPISODE, INPUT)
    run2 = command.begin(EPISODE, INPUT)
    (root / EPISODE / "shared").mkdir()
    (root / EPISODE / STORY_INPUT_FILE).write_text(json.dumps(INPUT), encoding="utf-8")

    class Exposed:
        def __init__(self, path):
            self.root = path

        def excluded_dirs(self):
            return set()

    node = TreeReader(Exposed(root))._walk_project(root / "ai_videos/demo")
    stage = next(child for child in node["children"] if child["name"] == "story")
    first, second = stage["children"]
    shared = first["children"][0]
    assert shared["type"] == "directory" and shared["display_name"] == "共享配置 · Persistent"
    assert shared["path"] == f"{EPISODE}/shared"
    assert shared["lifetime"] == "persistent"
    assert [child["story_input_view"] for child in shared["children"]] == ["input", "rules"]
    assert [child["display_name"] for child in shared["children"]] == ["创作输入", "创作规则"]
    assert shared["children"][0]["path"] == f"{EPISODE}/{STORY_INPUT_FILE}"
    assert shared["children"][1]["path"] == f"{EPISODE}/shared/rules-view.json"
    assert not shared["children"][0].get("whole_file_editable", False)
    record = first["children"][-1]
    assert record["type"] == "directory" and record["name"] == "runs"
    assert [child["display_name"] for child in record["children"]] == ["run1", "run2"]
    assert [child["story_run_id"] for child in record["children"]] == [run1["run_id"], run2["run_id"]]
    for run_node, run in zip(record["children"], (run1, run2)):
        assert run_node["path"] == f"{EPISODE}/runs/{run['run_id']}"
        assert run_node["audit_folder"] == run["audit_path"].rsplit("/", 1)[0]
        assert [child["display_name"] for child in run_node["children"]] == ["输入与规则", "产出", "过程"]
        assert all(child["type"] == "directory" for child in run_node["children"])
        def leaves(node):
            if "children" in node:
                return [leaf for child in node["children"] for leaf in leaves(child)]
            return [node]
        documents = leaves(run_node)
        assert [child["story_run_view"] for child in documents if child["story_run_view"] != "item"] == ["input", "output", "state", "process"]
        assert len({child["path"] for child in documents}) == len(documents)
        links = [child for child in documents if child["story_run_view"] == "item"]
        assert links and all(child["is_link"] and "#" in child["story_run_source"] for child in links)
        assert all(child["episode_path"] == EPISODE and child["story_run_id"] == run["run_id"]
                   for child in documents)
    assert all(child.get("name") != "runs" for child in second["children"])


def test_run_io_keeps_frozen_sources_tasks_and_missing_settings_explicit(runs):
    import hashlib
    root, query, command = runs
    source = root / "ai_videos/demo/background.md"
    source.write_text("full background with unused content", encoding="utf-8")
    old_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    incoming = copy.deepcopy(INPUT)
    incoming["sources"] = [{"path": "ai_videos/demo/background.md", "content": "selected excerpt",
                            "sha256": old_hash, "selection": "explicit_excerpt"}]
    incoming["extra_setting"] = "additional explicit condition"
    incoming["display/style~mix"] = "setting with a JSON pointer escape"
    guideline = root / ".agents/references/project/story_guidelines.md"
    guideline.parent.mkdir(parents=True)
    guideline.write_text("shared guideline current version", encoding="utf-8")
    incoming["rules"] = [{"path": guideline.relative_to(root).as_posix(), "content": "shared guideline snapshot",
                          "sha256": hashlib.sha256(guideline.read_bytes()).hexdigest()}]
    first = command.begin(EPISODE, incoming)
    path = root / first["audit_path"]
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["participants"] = [{"id": "author", "name": "作者", "role": "writer", "scope": "story", "runtime_id": "worker1",
                            "model": None, "status": "complete", "started_at": None, "finished_at": None,
                            "prompt": "actual instruction with extra constraints", "output": "complete raw reply"}]
    doc["artifacts"] = [{"kind": "input", "name": "unused profile", "path": f"{EPISODE}/shared/profiles/workflow-v2/input.json"}]
    doc["candidate"]["fictional_facts"] = [{"fact": "candidate only"}]
    path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    original = path.read_bytes()
    items = {item["id"]: item for item in query.detail(EPISODE, first["run_id"])["io"]["items"]}
    assert items["sources-0"]["value"] == "selected excerpt"
    assert items["sources-0"]["source_status"]["status"] == "same"
    assert items["setting-extra_setting"]["value"] == "additional explicit condition"
    assert items["setting-display/style~mix"]["target"].endswith("#/input/display~1style~0mix")
    assert items["rules-0"]["source_status"]["status"] == "same"
    assert items["rules-0"]["value"] == "shared guideline snapshot"
    assert items["task-0"]["value"] == doc["participants"][0]["prompt"]
    assert items["runtime"]["value"]["sampling_parameters"] == "未记录"
    assert items["runtime"]["value"]["participants"][0]["model"] is None
    assert items["candidate-fictional_facts"]["kind"] == "output"
    assert not any("workflow-v2" in item.get("source_path", "") for item in items.values())
    source.write_text("new source content", encoding="utf-8")
    changed = next(item for item in query.detail(EPISODE, first["run_id"])["io"]["items"] if item["id"] == "sources-0")
    assert changed["value"] == "selected excerpt" and changed["source_status"]["status"] == "changed"
    source.unlink()
    missing = next(item for item in query.detail(EPISODE, first["run_id"])["io"]["items"] if item["id"] == "sources-0")
    assert missing["source_status"]["status"] == "missing" and missing["value"] == "selected excerpt"
    assert path.read_bytes() == original


@pytest.mark.parametrize("bad_path", ["../secret.txt", "C:/private.txt", "ai_videos/demo/../private.txt", ".audit/other-run/secret.txt"])
def test_run_io_never_reads_unrelated_or_traversal_sources(runs, bad_path):
    _, query, command = runs
    source = copy.deepcopy(INPUT)
    source["rules"] = [{"path": bad_path, "content": "recorded historical rule"}]
    run = command.begin(EPISODE, source)
    item = next(item for item in query.detail(EPISODE, run["run_id"])["io"]["items"] if item["id"] == "rules-0")
    assert item["value"] == "recorded historical rule"
    assert item["source_status"] == {"status": "unavailable"}


def test_run_io_links_exact_audited_review_packet_and_never_substitutes_changed_file(runs):
    import hashlib
    root, query, command = runs
    incoming = copy.deepcopy(INPUT)
    incoming["user_requests"] = ["input-level condition distinct from run metadata"]
    first = command.begin(EPISODE, incoming)
    path = root / first["audit_path"]
    packet = path.parent / "review_packet.json"
    packet.write_text(json.dumps({"candidate": "author draft actually reviewed"}), encoding="utf-8")
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["artifacts"] = [{"kind": "input", "scope": "run", "path": packet.relative_to(root).as_posix(),
                         "sha256": hashlib.sha256(packet.read_bytes()).hexdigest()}]
    doc["user_requests"] = ["actual user direction"]
    doc["comparison_plan"] = {"purpose": "same frozen conditions"}
    path.write_text(json.dumps(doc), encoding="utf-8")
    original = path.read_bytes()
    items = {item["id"]: item for item in query.detail(EPISODE, first["run_id"])["io"]["items"]}
    assert items["setting-user_requests"]["value"] == incoming["user_requests"]
    assert items["run-user_requests"]["value"] == doc["user_requests"]
    assert items["run-comparison_plan"]["value"] == doc["comparison_plan"]
    item = items["file-review_packet-json"]
    assert item["value"] == {"candidate": "author draft actually reviewed"}
    assert item["target"] == packet.relative_to(root).as_posix() and item["kind"] == "input"
    packet.write_text('{"candidate": "changed draft, not actual historical input"}', encoding="utf-8")
    changed = next(item for item in query.detail(EPISODE, first["run_id"])["io"]["items"] if item["id"] == "file-review_packet-json")
    assert changed["source_status"]["status"] == "changed"
    assert "changed draft" not in json.dumps(changed["value"])
    packet.unlink()
    missing = next(item for item in query.detail(EPISODE, first["run_id"])["io"]["items"] if item["id"] == "file-review_packet-json")
    assert missing["source_status"]["status"] == "missing"
    assert path.read_bytes() == original
