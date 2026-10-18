from __future__ import annotations

import json
import copy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.commands.episode_workflow__command import EpisodeWorkflowCommand
from libs.application.queries.episode_workflow__query import EpisodeWorkflowQuery
from libs.common.episode_workflow import COMPILER_VERSION, MODULES, WORKFLOW_ID, fingerprint
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.writers.episode_workflow__writer import EpisodeWorkflowWriter
from tests.conftest import make_app

EPISODE = "ai_videos/demo/episodes/ep01"
STORY = {"brief": "一个普通人的选择", "text": "他把最后一块面包分给陌生人。"}
FILMING = {"scenes": [{"id": "s1", "background": "bg1", "location": "门前", "time": "白天", "purpose": "分出面包", "shots": [{"id": "st1", "duration": 6, "action": "他掰开面包，递出一半。", "camera": "固定中景，双手在画面内。", "dialogue": "给你。", "cast": [], "blocking": "", "beats": "0–3秒 掰开面包；3–6秒 递出一半", "lighting": "门前白天的散射光"}]}]}


def prepare_overheads(root: Path, previz: bool = False) -> None:
    """Every shot needs an overhead before compiling (follow-up 227): the decision file and the image drawn for the model."""
    filming = json.loads((root / EPISODE / "filming.json").read_text(encoding="utf-8"))["content"]
    for scene in filming["scenes"]:
        for shot in scene["shots"]:
            folder = root / EPISODE / "scenes" / scene["id"] / "shots" / shot["id"]
            (folder / "planning").mkdir(parents=True, exist_ok=True)
            (folder / "planning" / "previz.json").write_text(json.dumps({"previz": previz, "why": "测试"}), encoding="utf-8")
            (folder / "planning" / f"{shot['id']}_overhead_ref.png").write_bytes(b"overhead")
            if previz:
                (folder / "previz").mkdir(exist_ok=True)
                (folder / "previz" / f"{shot['id']}_previz.mp4").write_bytes(b"previz")


def add_background(root: Path, bg: str = "bg1", name: str = "门前") -> Path:
    """A background asset: card with its prompt-ready 场景 section, and the image (follow-up 228)."""
    view = root / "ai_videos/demo/2_世界观人设/background/region" / f"{bg}_{name}"
    view.mkdir(parents=True, exist_ok=True)
    (view / f"{bg}_{name}.md").write_text(f"# {bg}\n\n## Shot prompt 场景\n\n```text\n石砌门廊，木门半开。\n```\n", encoding="utf-8")
    (view / f"{bg}_{name}.png").write_bytes(b"scene")
    return view


def add_character(root: Path) -> None:
    card = root / "ai_videos/demo/2_世界观人设/characters/c1_Hero"
    (card / "views").mkdir(parents=True)
    (card / "c1_Hero.md").write_text("# Hero · 阿明 · 主角\n\n## Shot prompt 外观\n\n```text\n瘦高青年，灰布衣。\n```\n\n## 其他\n", encoding="utf-8")
    (card / "views/c1_Hero_views.png").write_bytes(b"views")
    (card / "views/c1_Hero_audio.mp3").write_bytes(b"voice")
    (card / "c1-1_便服").mkdir()
    (card / "c1-1_便服/c1-1_views.png").write_bytes(b"stage views")


@pytest.fixture
def workflow(tmp_path: Path):
    (tmp_path / EPISODE).mkdir(parents=True)
    (tmp_path / "ai_videos/demo/workflow.json").write_text(json.dumps({"workflow": WORKFLOW_ID}), encoding="utf-8")
    add_background(tmp_path)
    reader = EpisodeWorkflowReader(tmp_path)
    return tmp_path, EpisodeWorkflowQuery(reader), EpisodeWorkflowCommand(reader, EpisodeWorkflowWriter(tmp_path))


def module(query: EpisodeWorkflowQuery, name: str):
    return next(item for item in query.read(EPISODE).modules if item["id"] == name)


def change(query, command, name, operation, content=None, scene=None):
    if operation == "compile" and not getattr(command, "keep_overheads", False):
        prepare_overheads(command.reader.root)
    snapshot = module(query, name)
    command.change(EPISODE, name, operation, snapshot["etag"], snapshot["input_revision"], content, scene)


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
    if dialogue:
        assert lines[lines.index("台词：") + 1] == f"  {dialogue}"
    else:
        assert "台词：无" in lines
    assert any(line.startswith("要求：连续镜头，不要切镜。不要字幕或水印。画面中每个人物只出现一次") for line in lines)


def test_old_sound_compiler_version_requires_recompile(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    change(query, command, "prompts", "compile")
    change(query, command, "prompts", "approve")
    path = root / EPISODE / "prompts.json"
    old = json.loads(path.read_text(encoding="utf-8"))
    old["content"]["compiler_version"] = 3
    path.write_text(json.dumps(old), encoding="utf-8")
    assert module(query, "prompts")["status"] == "stale"
    assert json.loads(path.read_text(encoding="utf-8")) == old
    change(query, command, "prompts", "compile")
    assert module(query, "prompts")["content"]["compiler_version"] == COMPILER_VERSION


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
    # validation/security.md SEC-ORIGIN-HOST-01/02: a write without Origin, or with a foreign one, is refused.
    assert client.post("/api/episode-workflow", json=body).status_code == 403
    assert client.post("/api/episode-workflow", json=body, headers={"Origin": "https://evil.example"}).status_code == 403
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
    root, query, command = workflow
    add_background(root, "bg2-2", "中庭")
    approved_filming(query, command)
    scene = {**FILMING["scenes"][0], "background": "bg2-2"}
    change(query, command, "filming", "save", {"scenes": [scene]})
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    shot = module(query, "prompts")["content"]["scenes"][0]["shots"][0]
    assert "参考：`ep1_s1_st1_overhead=>@`、`bg2-2_中庭=>@`" in shot["text"].splitlines()
    assert "场景：门前 · 白天（`bg2-2_中庭`）：石砌门廊，木门半开。" in shot["text"].splitlines()
    assert shot["refs"][1]["path"].endswith("bg2-2_中庭/bg2-2_中庭.png")


def test_every_shot_needs_a_background_and_its_scene_text(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    change(query, command, "filming", "save", {"scenes": [{**FILMING["scenes"][0], "background": ""}]})
    change(query, command, "filming", "approve")
    with pytest.raises(EpisodeWorkflowError, match="背景图"):
        change(query, command, "prompts", "compile")
    change(query, command, "filming", "save", FILMING)
    change(query, command, "filming", "approve")
    (root / "ai_videos/demo/2_世界观人设/background/region/bg1_门前/bg1_门前.md").write_text("# bg1\n", encoding="utf-8")
    with pytest.raises(EpisodeWorkflowError, match="Shot prompt 场景"):
        change(query, command, "prompts", "compile")


def test_prompt_lists_references_in_upload_order_with_their_use(workflow):
    root, query, command = workflow
    add_character(root)
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0].update(cast=["c1-1"], blocking="阿明站在门槛内，面朝门外。", dialogue="阿明：给你。")
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    shot = module(query, "prompts")["content"]["scenes"][0]["shots"][0]
    lines = shot["text"].splitlines()
    assert [(r["key"], r["kind"]) for r in shot["refs"]] == [("ep1_s1_st1_overhead", "image"), ("c1-1_便服", "image"),
                                                             ("bg1_门前", "image"), ("c1_Hero_audio", "audio")]
    assert shot["refs"][1]["path"].endswith("c1-1_便服/c1-1_views.png")
    assert "参考：`ep1_s1_st1_overhead=>@`、`c1-1_便服=>@`、`bg1_门前=>@`、`c1_Hero_audio=>@`" in lines
    usage = next(line for line in lines if line.startswith("参考用法："))
    assert "`ep1_s1_st1_overhead`是本镜的俯视站位示意图，不是画面" in usage and "同一个人的正面、侧面、背面" in usage
    assert "声音参考（`c1_Hero_audio`）只取该人物的音色" in usage
    assert "  阿明（三视图`c1-1_便服`；声音`c1_Hero_audio`；`ep1_s1_st1_overhead`里的蓝色圆点）：瘦高青年，灰布衣。" in lines
    assert "本场：分出面包" in lines and any(line.startswith("口型：") for line in lines)
    assert next(line for line in lines if line.startswith("负面词：")).startswith("负面词：分身，双胞胎")
    assert "走位：阿明站在门槛内，面朝门外。" in lines and "动作：0–3秒 掰开面包；3–6秒 递出一半" in lines
    assert "不要分身或双胞胎" in next(line for line in lines if line.startswith("要求："))


def add_animal(root: Path) -> None:
    card = root / "ai_videos/demo/2_世界观人设/characters/m2_Wolf"
    (card / "views").mkdir(parents=True)
    (card / "m2_Wolf.md").write_text("# Wolf · 野狼\n\n## Shot prompt 外观\n\n```text\n瘦削的成年灰狼。\n```\n", encoding="utf-8")
    (card / "views/m2_Wolf_views.png").write_bytes(b"views")
    (card / "views/m2_Wolf_audio.mp3").write_bytes(b"growl")


def test_animals_may_appear_several_times_people_only_once(workflow):
    """Three wolves share one card (follow-up 245): the twin rule binds people; animals appear as many times as written."""
    root, query, command = workflow
    add_character(root)
    add_animal(root)
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    pack = filming["scenes"][0]["shots"][0]
    pack.update(cast=["c1-1", "m2"], dialogue="", action="三只狼从坡上下来，阿明挡在门前。", blocking="阿明在门前，狼从画左来。")
    alone = copy.deepcopy(pack)
    alone.update(id="st2", cast=["c1-1"], action="阿明独自站在门前。")
    filming["scenes"][0]["shots"].append(alone)
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    wolves, person = (shot["text"].splitlines() for shot in module(query, "prompts")["content"]["scenes"][0]["shots"])
    for lines in (wolves, person):
        rule = next(line for line in lines if line.startswith("要求："))
        negatives = next(line for line in lines if line.startswith("负面词："))
        assert "画面中每个人物只出现一次，不要分身或双胞胎。" in rule and "同一人物出现两次" in negatives
        assert "角色只出现一次" not in rule and "同一角色出现两次" not in negatives
    assert "群演与动物（`m2_Wolf`）按「人物」「画面」写的数量出现，写了几个就画几个，一个都不能少；同一张三视图可以是几个同类，不算分身。" in next(
        line for line in wolves if line.startswith("要求："))
    assert "群演与动物" not in next(line for line in person if line.startswith("要求："))
    # follow-up 276: 「多出来的人」 fought the count and dropped the second guard; group shots leave it out
    assert "多出来的人" not in next(line for line in wolves if line.startswith("负面词："))
    assert "多出来的人" in next(line for line in person if line.startswith("负面词："))


def test_one_card_standing_for_several_people_says_how_many(workflow):
    """Two gate guards from one card (follow-up 274): the count comes from the overhead's actors and reaches the 人物 line."""
    root, query, command = workflow
    add_character(root)
    add_animal(root)
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0].update(cast=["c1-1", "m2"], dialogue="", action="两只狼守在门两侧，阿明走过。",
                                            blocking="狼一左一右，阿明从中间走过。")
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    prepare_overheads(root)
    plan = root / EPISODE / "scenes/s1/shots/st1/planning/overhead.toml"
    plan.write_text('[[actor]]\nkey = "c1_Hero"\n[[actor]]\nkey = "m2_Wolf"\nlabel = "左"\n[[actor]]\nkey = "m2_Wolf"\nlabel = "右"\n',
                    encoding="utf-8")
    command.keep_overheads = True
    change(query, command, "prompts", "compile")
    lines = module(query, "prompts")["content"]["scenes"][0]["shots"][0]["text"].splitlines()
    wolf = next(line for line in lines if line.startswith("  野狼"))
    assert wolf.startswith("  野狼 ×2（三视图`m2_Wolf`；同一张三视图画 2 个人，各在自己的位置")
    assert next(line for line in lines if line.startswith("  阿明")).startswith("  阿明（三视图")


def test_an_opening_still_goes_first_as_the_first_frame(workflow):
    """A shot with `planning/{stN}_first_frame.png` (follow-up 276) sends it first and says the video starts from it."""
    root, query, command = workflow
    add_character(root)
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0].update(cast=["c1"], blocking="阿明站在门槛内。", dialogue="")
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    prepare_overheads(root)
    still = root / EPISODE / "scenes/s1/shots/st1/planning/st1_first_frame.png"
    still.write_bytes(b"still")
    command.keep_overheads = True
    change(query, command, "prompts", "compile")
    shot = module(query, "prompts")["content"]["scenes"][0]["shots"][0]
    assert shot["refs"][0] == {"key": "ep1_s1_st1_first_frame", "kind": "image", "role": "首帧画面",
                               "path": f"{EPISODE}/scenes/s1/shots/st1/planning/st1_first_frame.png"}
    usage = next(line for line in shot["text"].splitlines() if line.startswith("参考用法："))
    assert usage.startswith("参考用法：`ep1_s1_st1_first_frame`是本镜的第一帧画面：视频就从这张图开始")
    still.unlink()
    change(query, command, "prompts", "compile")
    assert "首帧画面" not in [r["role"] for r in module(query, "prompts")["content"]["scenes"][0]["shots"][0]["refs"]]


def test_every_person_needs_a_three_view_sheet_a_voice_and_an_appearance(workflow):
    root, query, command = workflow
    add_character(root)
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0].update(cast=["c1"], blocking="阿明站在门槛内。", dialogue="")
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    shot = module(query, "prompts")["content"]["scenes"][0]["shots"][0]
    assert [r["role"] for r in shot["refs"]] == ["俯视站位图", "阿明三视图", "场景 门前", "阿明的声音"]   # 不说话也带声样
    card = root / "ai_videos/demo/2_世界观人设/characters/c1_Hero"
    (card / "views/c1_Hero_audio.mp3").unlink()
    with pytest.raises(EpisodeWorkflowError, match="声样"):
        change(query, command, "prompts", "compile")
    (card / "views/c1_Hero_audio.mp3").write_bytes(b"voice")
    (card / "views/c1_Hero_views.png").unlink()
    with pytest.raises(EpisodeWorkflowError, match="三视图"):
        change(query, command, "prompts", "compile")


def add_prop(root: Path, key: str = "p5", name: str = "葡萄手推车") -> Path:
    folder = root / "ai_videos/demo/2_世界观人设/props" / f"{key}_{name}"
    folder.mkdir(parents=True)
    (folder / f"{key}_{name}.md").write_text(f"# {name}\n\n## Shot prompt 外观\n\n```text\n敞开的单轴木手推车。\n```\n", encoding="utf-8")
    (folder / f"{key}_{name}.png").write_bytes(b"prop")
    return folder


def test_props_join_the_reference_line_with_their_description(workflow):
    root, query, command = workflow
    add_character(root)
    folder = add_prop(root)
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0].update(cast=["c1-1"], blocking="阿明站在车尾。", props=["p5"])
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    shot = module(query, "prompts")["content"]["scenes"][0]["shots"][0]
    lines = shot["text"].splitlines()
    assert [r["key"] for r in shot["refs"]] == ["ep1_s1_st1_overhead", "c1-1_便服", "p5_葡萄手推车", "bg1_门前", "c1_Hero_audio"]
    assert shot["refs"][2] == {"key": "p5_葡萄手推车", "kind": "image", "role": "道具 葡萄手推车",
                               "path": "ai_videos/demo/2_世界观人设/props/p5_葡萄手推车/p5_葡萄手推车.png"}
    assert "道具图（`p5_葡萄手推车`）是本镜出现的道具" in next(line for line in lines if line.startswith("参考用法："))
    assert lines[lines.index("道具：") + 1] == "  葡萄手推车（道具图`p5_葡萄手推车`）：敞开的单轴木手推车。"
    (folder / "p5_葡萄手推车.png").unlink()
    with pytest.raises(EpisodeWorkflowError, match="锚点图"):
        change(query, command, "prompts", "compile")


@pytest.mark.parametrize("value", [["p5", "p5"], ["c1"], "p5"])
def test_prop_keys_are_validated(workflow, value):
    _, query, command = workflow
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0]["props"] = value
    with pytest.raises(EpisodeWorkflowError, match="道具"):
        change(query, command, "filming", "save", filming)


def test_complex_shot_uses_the_previz_video_as_motion_reference(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    prepare_overheads(root, previz=True)
    command.keep_overheads = True
    change(query, command, "prompts", "compile")
    shot = module(query, "prompts")["content"]["scenes"][0]["shots"][0]
    assert shot["refs"][0] == {"key": "ep1_s1_st1_previz", "kind": "video", "role": "走位预演（绿幕小人偶）",
                               "path": f"{EPISODE}/scenes/s1/shots/st1/previz/st1_previz.mp4"}
    assert "绿幕前纯色小人偶的走位预演" in shot["text"]


def test_compile_refuses_shots_without_an_overhead(workflow):
    root, query, command = workflow
    approved_filming(query, command)
    command.keep_overheads = True
    with pytest.raises(EpisodeWorkflowError, match="还没有 overhead"):
        change(query, command, "prompts", "compile")
    prepare_overheads(root, previz=True)
    (root / EPISODE / "scenes/s1/shots/st1/previz/st1_previz.mp4").unlink()
    with pytest.raises(EpisodeWorkflowError, match="previz 视频"):
        change(query, command, "prompts", "compile")
    assert not (root / EPISODE / "prompts.json").exists()


@pytest.mark.parametrize("field,value", [("cast", ["c1", "c1"]), ("cast", ["主角"]), ("cast", "c1"), ("beats", " "),
                                         ("lighting", ""), ("blocking", "")])
def test_shot_reference_fields_are_validated(workflow, field, value):
    _, query, command = workflow
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0].update({"cast": ["c1"], "blocking": "站在门口。", field: value})
    with pytest.raises(EpisodeWorkflowError):
        change(query, command, "filming", "save", filming)


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
    from libs.domain.value_objects.shot_materials__valueobject import ShotMaterials
    with pytest.raises(EpisodeWorkflowError):
        entity.compile()
    entity.compile({"ep12_s1_st1": ShotMaterials("image", "x/st1_overhead_ref.png")})
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
    assert result.moved[0]["to"].endswith("episodes/ep01/scenes/s1/shots/st1/renders/generator_ep1_s1_st1/generator_ep1_s1_st1.mp4")
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

    assert find(tree, f"{EPISODE}/prompts.json/scenes/s1")["display_name"] == "s1 · 门前"
    shot = find(tree, f"{EPISODE}/prompts.json/scenes/s1/shots/st1")
    assert shot["display_name"] == "ep1_s1_st1"
    assert "scene=s1" in shot["navigation_href"] and "shot=ep1_s1_st1" in shot["navigation_href"]


def test_recompile_keeps_render_and_ordered_scene_media(workflow):
    from libs.common import drama_layout

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


def test_multi_line_dialogue_compiles_line_by_line(workflow):
    _, query, command = workflow
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0]["dialogue"] = "甲：给你。\n乙：谢谢。"
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    lines = module(query, "prompts")["content"]["scenes"][0]["shots"][0]["text"].splitlines()
    assert lines[lines.index("台词：") + 1:lines.index("台词：") + 3] == ["  甲：给你。", "  乙：谢谢。"]


def two_scenes(query, command, second_background="bg1"):
    """s1 and s2, both from FILMING's scene; s2 may point at a background that has no asset."""
    approved_filming(query, command)
    second = copy.deepcopy(FILMING["scenes"][0])
    second.update(id="s2", background=second_background, purpose="收下面包")
    change(query, command, "filming", "save", {"scenes": [FILMING["scenes"][0], second]})
    change(query, command, "filming", "approve")


def test_one_scene_compiles_alone_while_other_scenes_lack_references(workflow):
    root, query, command = workflow
    two_scenes(query, command, second_background="bg9")
    with pytest.raises(EpisodeWorkflowError, match="ep1_s2_st1"):
        change(query, command, "prompts", "compile")
    change(query, command, "prompts", "compile", scene="s1")
    scenes = module(query, "prompts")["content"]["scenes"]
    assert [s["id"] for s in scenes] == ["s1"]
    assert scenes[0]["shots"][0]["id"] == "ep1_s1_st1" and scenes[0]["source"]
    assert (root / EPISODE / "scenes/s1/shots/st1/prompt.txt").is_file()
    assert not (root / EPISODE / "scenes/s2/shots/st1/prompt.txt").exists()
    # the module as a whole is not up to date: s2 is not compiled
    assert module(query, "prompts")["status"] == "stale"


def test_scene_compile_replaces_only_that_scene(workflow):
    root, query, command = workflow
    two_scenes(query, command)
    change(query, command, "prompts", "compile")
    before = module(query, "prompts")["content"]["scenes"]
    filming = copy.deepcopy(module(query, "filming")["content"])
    filming["scenes"][1]["shots"][0]["action"] = "她接过面包，点头。"
    filming["scenes"][0]["shots"][0]["action"] = "他把面包揣回怀里。"
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile", scene="s2")
    after = module(query, "prompts")["content"]["scenes"]
    assert [s["id"] for s in after] == ["s1", "s2"]
    assert after[0] == before[0]
    assert "她接过面包" in after[1]["shots"][0]["text"] and after[1]["source"] != before[1]["source"]


def test_scene_compile_refuses_unknown_scene_old_compiler_and_unapproved_filming(workflow):
    root, query, command = workflow
    two_scenes(query, command)
    with pytest.raises(EpisodeWorkflowError, match="s7"):
        change(query, command, "prompts", "compile", scene="s7")
    change(query, command, "prompts", "compile")
    path = root / EPISODE / "prompts.json"
    old = json.loads(path.read_text(encoding="utf-8"))
    old["content"]["compiler_version"] = COMPILER_VERSION - 1
    path.write_text(json.dumps(old), encoding="utf-8")
    with pytest.raises(EpisodeWorkflowError, match="整集"):
        change(query, command, "prompts", "compile", scene="s1")
    filming = copy.deepcopy(module(query, "filming")["content"])
    filming["scenes"][0]["purpose"] = "改了没确定"
    change(query, command, "filming", "save", filming)
    with pytest.raises(EpisodeWorkflowError, match="上游版本尚未确定"):
        change(query, command, "prompts", "compile", scene="s1")


def test_a_shot_can_name_its_own_background_view(workflow):
    """follow-up 261: a scene has one background, but a shot that faces another way names its own view (`background`);
    its image and 场景 text replace the scene's for that shot only."""
    root, query, command = workflow
    add_background(root, "bg1-2", "门前南望")
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    second = copy.deepcopy(filming["scenes"][0]["shots"][0])
    second.update(id="st2", background="bg1-2")
    filming["scenes"][0]["shots"].append(second)
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    first, other = module(query, "prompts")["content"]["scenes"][0]["shots"]
    assert [r["key"] for r in first["refs"] if r["role"].startswith("场景")] == ["bg1_门前"]
    assert [r["key"] for r in other["refs"] if r["role"].startswith("场景")] == ["bg1-2_门前南望"]
    assert "（`bg1-2_门前南望`）" in next(line for line in other["text"].splitlines() if line.startswith("场景："))


@pytest.mark.parametrize("value", ["", "门前", ["bg1"], "bg0"])
def test_shot_background_is_a_bg_key(workflow, value):
    _, query, command = workflow
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0]["background"] = value
    with pytest.raises(EpisodeWorkflowError, match="环境引用"):
        change(query, command, "filming", "save", filming)


def test_missing_shot_background_blocks_compiling(workflow):
    _, query, command = workflow
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0]["background"] = "bg9"
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    with pytest.raises(EpisodeWorkflowError, match="bg9"):
        change(query, command, "prompts", "compile")


def test_a_shot_can_lift_named_drama_negatives(workflow):
    """follow-up 282: a spell shot lifts 夸张金光 from the drama negatives; other shots keep it, and a typo is refused."""
    root, query, command = workflow
    (root / "ai_videos/demo/workflow.json").write_text(json.dumps({"workflow": WORKFLOW_ID, "prompt": {"negatives": "人物自发光，夸张金光，卡通渲染"}}),
                                                       encoding="utf-8")
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    plain = copy.deepcopy(filming["scenes"][0]["shots"][0])
    glow = {**copy.deepcopy(plain), "id": "st2", "allow_negatives": ["夸张金光"]}
    filming["scenes"][0]["shots"] = [plain, glow]
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    change(query, command, "prompts", "compile")
    shots = module(query, "prompts")["content"]["scenes"][0]["shots"]
    negatives = [next(line for line in s["text"].splitlines() if line.startswith("负面词：")) for s in shots]
    assert negatives[0].endswith("人物自发光，夸张金光，卡通渲染")
    assert negatives[1].endswith("人物自发光，卡通渲染") and "夸张金光" not in negatives[1]
    filming["scenes"][0]["shots"][1]["allow_negatives"] = ["夸张光"]
    change(query, command, "filming", "save", filming)
    change(query, command, "filming", "approve")
    with pytest.raises(EpisodeWorkflowError, match="不在剧负面词里"):
        change(query, command, "prompts", "compile")


@pytest.mark.parametrize("value", [[], ["夸张金光", "夸张金光"], ["人物自发光，夸张金光"], "夸张金光"])
def test_lifted_negatives_are_validated(workflow, value):
    _, query, command = workflow
    approved_filming(query, command)
    filming = copy.deepcopy(FILMING)
    filming["scenes"][0]["shots"][0]["allow_negatives"] = value
    with pytest.raises(EpisodeWorkflowError, match="放开的负面词"):
        change(query, command, "filming", "save", filming)
