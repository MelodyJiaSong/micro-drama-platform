from __future__ import annotations

import json
import copy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.commands.episode_workflow__command import EpisodeWorkflowCommand
from libs.application.queries.episode_workflow__query import EpisodeWorkflowQuery
from libs.common.episode_workflow import MODULES, WORKFLOW_ID, fingerprint
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.writers.episode_workflow__writer import EpisodeWorkflowWriter
from tests.conftest import make_app

EPISODE = "ai_videos/demo/episodes/ep01"
STORY = {"brief": "一个普通人的选择", "text": "他把最后一块面包分给陌生人。"}
FILMING = {"scenes": [{"id": "s1", "background": "", "location": "门前", "time": "白天", "purpose": "分出面包", "shots": [{"id": "st1", "duration": 6, "action": "他掰开面包，递出一半。", "camera": "固定中景，双手在画面内。", "dialogue": "给你。"}]}]}


@pytest.fixture
def workflow(tmp_path: Path):
    (tmp_path / EPISODE).mkdir(parents=True)
    (tmp_path / "ai_videos/demo/workflow.json").write_text(json.dumps({"workflow": WORKFLOW_ID}), encoding="utf-8")
    reader = EpisodeWorkflowReader(tmp_path)
    return tmp_path, EpisodeWorkflowQuery(reader), EpisodeWorkflowCommand(reader, EpisodeWorkflowWriter(tmp_path))


def module(query: EpisodeWorkflowQuery, name: str):
    return next(item for item in query.read(EPISODE).modules if item["id"] == name)


def change(query, command, name, operation, content=None):
    snapshot = module(query, name)
    command.change(EPISODE, name, operation, snapshot["etag"], snapshot["input_revision"], content)


def approved_filming(query, command):
    change(query, command, "story", "save", STORY)
    change(query, command, "story", "approve")
    change(query, command, "filming", "save", FILMING)
    change(query, command, "filming", "approve")


def test_compilation_is_deterministic_and_writes_only_its_own_module(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    originals = {name: (root / EPISODE / f"{name}.json").read_bytes() for name in ("story", "filming")}
    change(query, command, "prompts", "compile")
    first = (root / EPISODE / "prompts.json").read_bytes()
    change(query, command, "prompts", "compile")
    assert first == (root / EPISODE / "prompts.json").read_bytes()
    assert "他掰开面包" in module(query, "prompts")["content"]["scenes"][0]["shots"][0]["text"]
    prompt = root / EPISODE / "scenes/s1/shots/st1/prompt.txt"
    assert prompt.read_text(encoding="utf-8").splitlines()[0] == "ep1_s1_st1"
    for name, content in originals.items():
        assert (root / EPISODE / f"{name}.json").read_bytes() == content
    change(query, command, "prompts", "approve")
    change(query, command, "prompts", "compile")
    assert module(query, "prompts")["status"] == "approved"


@pytest.mark.parametrize("dialogue", ["给你。", ""])
def test_compiled_sound_rules_keep_dialogue_and_effects_without_music(workflow, dialogue):
    _, query, command = workflow
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0]["dialogue"] = dialogue
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    lines = module(query, "prompts")["content"]["scenes"][0]["shots"][0]["text"].splitlines()
    assert lines[0] == "ep1_s1_st1"
    for sound in (lines[1], lines[-1]):
        assert "本镜指定对白、自然环境声和动作声" in sound
        assert "不要背景音乐或配乐" in sound
        assert ("本镜没有人说话" in sound) == (not dialogue)
    assert f"对白：{dialogue or '无'}" in lines


def test_old_sound_compiler_version_requires_recompile(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    change(query, command, "prompts", "compile")
    change(query, command, "prompts", "approve")
    path = root / EPISODE / "prompts.json"
    old = json.loads(path.read_text(encoding="utf-8"))
    old["content"]["compiler_version"] = 2
    path.write_text(json.dumps(old), encoding="utf-8")
    assert module(query, "prompts")["status"] == "stale"
    assert json.loads(path.read_text(encoding="utf-8")) == old
    change(query, command, "prompts", "compile")
    assert module(query, "prompts")["content"]["compiler_version"] == 3


def test_upstream_changes_preserve_downstream_bytes_but_invalidate_status(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    change(query, command, "prompts", "compile")
    change(query, command, "prompts", "approve")
    preserved = {name: (root / EPISODE / f"{name}.json").read_bytes() for name in ("filming", "prompts")}
    change(query, command, "story", "save", {**STORY, "text": "他留下整块面包，自己转身离开。"})
    assert module(query, "filming")["status"] == "stale"
    assert module(query, "prompts")["status"] == "blocked"
    with pytest.raises(EpisodeWorkflowError):
        change(query, command, "prompts", "compile")
    for name, content in preserved.items():
        assert (root / EPISODE / f"{name}.json").read_bytes() == content


def test_conflicting_edits_and_changed_upstream_are_rejected(workflow):
    _, query, command = workflow
    stale_story = module(query, "story")
    change(query, command, "story", "save", STORY)
    with pytest.raises(EpisodeWorkflowError, match="其他会话"):
        command.change(EPISODE, "story", "save", stale_story["etag"], None, STORY)
    change(query, command, "story", "approve")
    stale_filming = module(query, "filming")
    change(query, command, "story", "save", {**STORY, "text": "另一个选择"})
    change(query, command, "story", "approve")
    with pytest.raises(EpisodeWorkflowError, match="上游版本"):
        command.change(EPISODE, "filming", "save", stale_filming["etag"], stale_filming["input_revision"], FILMING)


def test_no_empty_approval_no_prompt_invention_and_no_extra_fields(workflow):
    _, query, command = workflow
    with pytest.raises(EpisodeWorkflowError):
        change(query, command, "story", "approve")
    with pytest.raises(EpisodeWorkflowError):
        change(query, command, "story", "save", {**STORY, "camera": "偷加摄影"})
    approved_filming(query, command)
    with pytest.raises(EpisodeWorkflowError):
        change(query, command, "prompts", "save", {"scenes": []})
    with pytest.raises(EpisodeWorkflowError):
        change(query, command, "filming", "save", {"scenes": [{**FILMING["scenes"][0], "shots": [{**FILMING["scenes"][0]["shots"][0], "duration": True}]}]})


def test_api_wiring_origin_and_scope(workflow):
    root, _, _ = workflow
    client = TestClient(make_app(RepoRoot(path=root), BoundOrigin(host="127.0.0.1", port=8766)), base_url="http://127.0.0.1:8766")
    response = client.get("/api/episode-workflow", params={"episode_path": EPISODE})
    assert response.status_code == 200
    assert [item["id"] for item in response.json()["modules"]] == list(MODULES)
    story = response.json()["modules"][0]
    body = {"episode_path": EPISODE, "module": "story", "operation": "save", "expected": story["etag"], "content": STORY}
    assert client.post("/api/episode-workflow", json=body).status_code == 403
    assert client.post("/api/episode-workflow", json=body, headers={"Origin": "http://127.0.0.1:8766"}).status_code == 200
    assert client.post("/api/episode-workflow", json=body, headers={"Origin": "http://127.0.0.1:8766"}).status_code == 409
    assert client.get("/api/episode-workflow", params={"episode_path": "ai_videos/demo/episodes/../../outside"}).status_code == 404
    with pytest.raises(FileNotFoundError):
        EpisodeWorkflowReader(root).read("ai_videos/demo/episodes/../../outside")
    assert fingerprint(STORY) == fingerprint(dict(reversed(list(STORY.items()))))


def test_invalid_module_file_is_reported_without_overwriting(workflow):
    root, query, command = workflow
    path = root / EPISODE / "story.json"
    path.write_text('{"content": "invalid"}', encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(EpisodeWorkflowError, match="格式无效"):
        query.read(EPISODE)
    with pytest.raises(EpisodeWorkflowError, match="格式无效"):
        command.change(EPISODE, "story", "save", "any", None, STORY)
    assert path.read_bytes() == before


def test_scene_and_shot_ids_stay_stable_across_reordering(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    scene = copy.deepcopy(FILMING["scenes"][0])
    scene["id"] = "s10"
    scene["shots"].insert(0, {**scene["shots"][0], "id": "st10"})
    change(query, command, "filming", "save", {"scenes": [scene, FILMING["scenes"][0]]})
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    content = module(query, "prompts")["content"]
    assert [s["id"] for s in content["scenes"]] == ["s10", "s1"]
    assert [s["id"] for s in content["scenes"][0]["shots"]] == ["ep1_s10_st10", "ep1_s10_st1"]
    assert query.read(EPISODE).shot_keys["s10"]["st1"] == "ep1_s10_st1"
    assert (root / EPISODE / "scenes/s10/shots/st10/prompt.txt").is_file()


@pytest.mark.parametrize("field,value", [("id", "s01"), ("id", "../s1"), ("background", "bg2/path"), ("shots", [])])
def test_invalid_scene_boundaries_are_rejected(workflow, field, value):
    _, query, command = workflow
    approved_filming(query, command)
    scene = {**FILMING["scenes"][0], field: value}
    with pytest.raises(EpisodeWorkflowError):
        change(query, command, "filming", "save", {"scenes": [scene]})


def test_duplicate_scene_or_shot_ids_cannot_compile(workflow):
    _, query, command = workflow
    approved_filming(query, command)
    scene = FILMING["scenes"][0]
    for content in ({"scenes": [scene, scene]}, {"scenes": [{**scene, "shots": scene["shots"] * 2}]}):
        with pytest.raises(EpisodeWorkflowError):
            change(query, command, "filming", "save", content)


def test_scene_can_bind_a_specific_background_view(workflow):
    _, query, command = workflow
    approved_filming(query, command)
    scene = {**FILMING["scenes"][0], "background": "bg2-2"}
    change(query, command, "filming", "save", {"scenes": [scene]})
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    assert "环境资产：bg2-2。" in module(query, "prompts")["content"]["scenes"][0]["shots"][0]["text"]


def test_other_episode_key_is_derived_from_its_own_path(workflow):
    root, _, _ = workflow
    directory = root / "ai_videos/demo/episodes/ep12"
    directory.mkdir()
    reader = EpisodeWorkflowReader(root)
    from libs.domain.entities.episode_workflow__entity import EpisodeWorkflowEntity
    entity = EpisodeWorkflowEntity(reader.read("ai_videos/demo/episodes/ep12").documents, "ep12")
    entity.save("story", STORY)
    entity.approve("story")
    entity.save("filming", FILMING)
    entity.approve("filming")
    entity.compile()
    assert entity.documents["prompts"]["content"]["scenes"][0]["shots"][0]["id"] == "ep12_s1_st1"


def test_compile_import_and_navigation_share_the_same_key(workflow):
    from libs.common.exposed_tree import ExposedTree
    from libs.common.safe_resolve import SafeResolver
    from libs.infrastructure.readers.tree__reader import TreeReader
    from libs.infrastructure.writers.downloads__writer import DownloadsImporter
    from libs.infrastructure.writers.media__writer import MediaRenamer
    from libs.common import drama_layout

    root, query, command = workflow
    approved_filming(query, command)
    change(query, command, "prompts", "compile")
    downloads = root / "Downloads"
    downloads.mkdir()
    (downloads / "generator_ep1_s1_st1.mp4").write_bytes(b"a take")
    exposed, resolver = ExposedTree(root), SafeResolver(root)
    importer = DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)
    result = importer.import_drama("ai_videos/demo")
    assert result.moved[0]["to"].endswith("episodes/ep01/scenes/s1/shots/st1/renders/generator_ep1_s1_st1.mp4")
    assert [p.name for p in drama_layout.episode_shot_dirs(root / EPISODE)] == ["st1"]
    tree = TreeReader(exposed).build()

    def find(node, path):
        if node.get("path") == path:
            return node
        for child in node.get("children", []):
            result = find(child, path)
            if result:
                return result
        return None

    shot = find(tree, f"{EPISODE}/prompts.json/scenes/s1/shots/st1")
    assert shot["display_name"] == "ep1_s1_st1"
    assert "scene=s1" in shot["navigation_href"] and "shot=ep1_s1_st1" in shot["navigation_href"]


def test_recompile_keeps_render_and_ordered_scene_media(workflow):
    from libs.common import drama_layout
    from libs.common.exposed_tree import ExposedTree
    from libs.common.safe_resolve import SafeResolver
    from libs.infrastructure.writers.episode_takes__writer import EpisodeTakesSelector
    from libs.infrastructure.readers.drama_episodes__reader import DramaEpisodesReader
    from libs.infrastructure.writers.frame__writer import FrameExtractor

    root, query, command = workflow
    approved_filming(query, command)
    scene = copy.deepcopy(FILMING["scenes"][0])
    scene["id"] = "s10"
    scene["shots"].insert(0, {**scene["shots"][0], "id": "st10"})
    change(query, command, "filming", "save", {"scenes": [scene, FILMING["scenes"][0]]})
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    folders = drama_layout.episode_shot_dirs(root / EPISODE)
    assert [(p.parents[1].name, p.name) for p in folders] == [("s10", "st10"), ("s10", "st1"), ("s1", "st1")]
    for folder in folders:
        renders = folder / "renders"
        renders.mkdir()
        (renders / "take.mp4").write_bytes(b"preserved take")
    change(query, command, "prompts", "compile")
    assert all((p / "renders/take.mp4").read_bytes() == b"preserved take" for p in folders)
    exposed, resolver = ExposedTree(root), SafeResolver(root)
    selected = EpisodeTakesSelector(exposed, resolver).select(EPISODE)
    assert [item.shot for item in selected.selected] == ["ep1_s10_st10", "ep1_s10_st1", "ep1_s1_st1"]
    counts = DramaEpisodesReader(exposed, resolver).list("ai_videos/demo")
    assert counts.episodes[0].shots == 3 and counts.episodes[0].locked == 3
    frames = FrameExtractor(exposed, resolver)
    assert frames._next_shot_folder(folders[0]) == folders[1]
    assert frames._next_shot_folder(folders[1]) is None
    from libs.infrastructure.writers.subtitle__writer import SubtitleBurner
    from libs.infrastructure.writers.subtitle_batch__writer import SubtitleBatchBurner
    burner = SubtitleBurner(exposed, resolver)
    subtitles = SubtitleBatchBurner(exposed, resolver, burner).scaffold_episode(EPISODE)
    assert [item.shot for item in subtitles.outcomes] == ["ep1_s10_st10", "ep1_s10_st1", "ep1_s1_st1"]
    assert all(item.ok for item in subtitles.outcomes)
    assert burner.spoken_lines(folders[0]) == [FILMING["scenes"][0]["shots"][0]["dialogue"]]
