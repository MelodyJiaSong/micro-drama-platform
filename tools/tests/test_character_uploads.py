from pathlib import Path
import hashlib
import json
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from character_references import CharacterReferences, REFERENCE_MODE, audio_sample
import seedance_kit
from character_sheet import compose
from PIL import Image


def test_triptych_upload_and_stale_source_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = assets(tmp_path, 'c1_Person', named=True)
    for role, color in zip(('front', 'side', 'back'), ('red', 'green', 'blue')):
        Image.new('RGB', (9, 16), color).save(source.views / f'c1_Person_{role}.png')
    compose(source.views, source.card)
    refs = source.files(True, combined=True)
    assert len(refs) == 2 and refs[0][0] == 'c1_Person三视图'
    (tmp_path/'seedance.toml').write_text('character_reference_mode="uploads"\ncharacter_reference_layout="triptych"\naudio_mode="native"\n',encoding='utf-8')
    md = tmp_path/'shot01.md'
    uploads = '\n'.join(f'- {label} → [`{label}`]({path.relative_to(tmp_path).as_posix()})' for label,path,_ in refs)
    reference = '、'.join(f'`{label}({kind})=>@`' for label,_,kind in refs)
    md.write_text(f'---\nduration_s: 10\n---\n{uploads}\n## Seedance prompt\n```text\n参考: {reference}\n参考用法: {source.usage({source.card: "Person"}, combined=True)}\n角色: c1_Person＝Person\n```\n## 台词配音 prompt\n```text\n类型: 正常台词\n音色: zh-m-test-person-01\n角色: Person\n```\n',encoding='utf-8')
    monkeypatch.setattr(seedance_kit,'REPO',tmp_path)
    parsed,prompt,_ = seedance_kit.parse(md,seedance_kit.config(tmp_path))
    assert [ref.kind for ref in parsed] == ['图片','音频']
    assert '@图片1' in seedance_kit.kit_prompt(prompt,parsed)
    seedance_kit.build(md)
    assert seedance_kit.stale(md) == []
    Image.new('RGB',(9,16),'yellow').save(source.views/'c1_Person_side.png')
    with pytest.raises(SystemExit, match='合图与源图不一致'):
        seedance_kit.parse(md,seedance_kit.config(tmp_path))
    compose(source.views, source.card)
    assert any('哈希已变' in reason for reason in seedance_kit.stale(md))


def test_triptych_preserves_pixels_and_direction_with_mixed_sizes(tmp_path: Path) -> None:
    original = []
    for role,size,color in zip(('front','side','back'),((5,9),(7,4),(3,6)),('red','green','blue')):
        im = Image.new('RGB',size,color)
        im.save(tmp_path/f'c1_Test_{role}.png')
        original.append(im)
    row = compose(tmp_path,'c1_Test')
    with Image.open(row['path']) as image:
        assert image.size == (21,9)
        for i,im in enumerate(original):
            x,y = i*7+(7-im.width)//2,(9-im.height)//2
            assert image.crop((x,y,x+im.width,y+im.height)).tobytes() == im.tobytes()
    assert compose(tmp_path,'c1_Test')['status'] == 'current'


def assets(drama: Path, card: str, named: bool = False, voice: bool = True) -> CharacterReferences:
    root = drama / "2_world" / "characters" / card
    views = root / "views"
    views.mkdir(parents=True)
    (root / f"{card}.md").write_text("voice_id: zh-m-test-person-01" if voice else "Silent character", encoding="utf-8")
    names = [f"{card}_{side}.png" for side in ("front", "side", "back")] if named else [f"views{i}.png" for i in (1, 2, 3)]
    for name in names:
        (views / name).write_bytes(b"image")
    (views / (f"{card}_audio.mp3" if named else "views.mp3")).write_bytes(b"voice")
    return CharacterReferences(drama, card)


def shot(drama: Path, source: CharacterReferences, voiced: bool = True) -> Path:
    (drama / "seedance.toml").write_text('character_reference_mode = "uploads"\naudio_mode = "native"\n[dreamina_cli]\nmax_images = 9\nmax_audios = 3\nmax_seconds = 15\n', encoding="utf-8")
    refs = source.files(voiced)
    md = drama / "shot01.md"
    uploads = "\n".join(f"- {name} → [`{name}`]({path.relative_to(drama).as_posix()})" for name, path, _kind in refs)
    reference = "、".join(f"`{name}({kind})=>@`" for name, _path, kind in refs)
    dub = "\n## 台词配音 prompt\n```text\n类型: 正常台词\n音色: zh-m-test-person-01\n角色: Person\n```\n" if voiced else ""
    usage = CharacterReferences.usage({source.card: "Person"} if voiced else {})
    md.write_text(f"---\nduration_s: 10\n---\n{uploads}\n## Seedance prompt\n```text\n参考: {reference}\n参考用法: {usage}\n角色: {source.card}＝Person\n```\n{dub}", encoding="utf-8")
    return md


@pytest.mark.parametrize("declaration", ["voice_id: male-cold-01", "| **voice_id** | `male-cold-01` |", "**voice_id（全剧复用）**: male-cold-01"])
def test_explicit_voice_id_accepts_shared_templates(tmp_path: Path, declaration: str) -> None:
    source = assets(tmp_path, "c1_Person")
    (source.root / "c1_Person.md").write_text(declaration, encoding="utf-8")
    assert source.voice_id() == "male-cold-01"


def test_selected_outfit_stays_inside_character(tmp_path: Path) -> None:
    source = assets(tmp_path, "c1_Person")
    outfit = source.root / "c1-1_便服"
    outfit.mkdir()
    for i, side in enumerate(("正面", "侧面", "背面"), 1):
        (outfit / f"c1-1-{i}_{side}.png").write_bytes(b"outfit")
    selected = CharacterReferences(tmp_path, "c1_Person", outfit)
    md = shot(tmp_path, selected)
    refs, _, _ = seedance_kit.parse(md, seedance_kit.config(tmp_path))
    assert all(ref.src.parent == outfit for ref in refs[:3])
    assert refs[-1].src.parent == source.root / "views"
    with pytest.raises(ValueError, match="不属于"):
        CharacterReferences(tmp_path, "c1_Person", tmp_path / "other")


def test_canonical_outfit_roles_and_shared_audio(tmp_path: Path) -> None:
    source = assets(tmp_path, "c1_Person", named=True)
    outfit = source.root / "c1-2_造型"
    outfit.mkdir()
    for role in ("front", "side", "back"):
        (outfit / f"c1-2_{role}.png").write_bytes(role.encode())
    refs = CharacterReferences(tmp_path, "c1_Person", outfit).files(True)
    assert [path.read_bytes() for _, path, _ in refs[:3]] == [b"front", b"side", b"back"]
    assert refs[-1][1] == audio_sample(source.root)
    assert refs[-1][1].name == "c1_Person_audio.mp3"
    (source.root / 'views/views.mp3').write_bytes(b'other voice')
    with pytest.raises(ValueError, match='不唯一'):
        audio_sample(source.root)


@pytest.mark.parametrize("error", ["wrong_voice", "duplicate_reference", "duplicate_upload"])
def test_upload_contract_rejects_ambiguous_bindings(tmp_path: Path, error: str) -> None:
    md = shot(tmp_path, assets(tmp_path, "c1_Person"))
    original = md.read_text(encoding="utf-8")
    if error == "wrong_voice":
        broken = original.replace("c1_Person声音＝Person", "c1_Person声音＝SomeoneElse")
    elif error == "duplicate_reference":
        broken = original.replace("参考: ", "参考: `c1_Person视图1(人物三面视图)=>@`、")
    else:
        broken = original.replace("## Seedance prompt", "- c1_Person视图1 → [`views1.png`](2_world/characters/c1_Person/views/views1.png)\n## Seedance prompt")
    md.write_text(broken, encoding="utf-8")
    with pytest.raises(SystemExit):
        seedance_kit.parse(md, seedance_kit.config(tmp_path))


@pytest.mark.parametrize('combined', [False, True])
def test_compaction_keeps_character_voice_binding(combined: bool) -> None:
    import prompt_compact
    full = "参考: `c1_Person视图1(人物三面视图)=>@`、`c1_Person声音(声音音频)=>@`\n参考用法: " + CharacterReferences.usage({"c1_Person": "Person"}) + "\n角色: c1_Person＝Person\n镜头: 静止\n动作: 0–4s 点头\n台词: 1–3s Person（正常台词·对口型）：Hello.\n"
    if combined:
        full = full.replace('视图1(人物三面视图)', '三视图(人物三视图合图)')
    result = prompt_compact.compact(full, [prompt_compact.Cast("c1_Person", "Person")], 4, "native")
    assert "c1_Person声音＝Person" in result
    if combined:
        assert 'front/side/back' in result and '(角色合图)=>@' in result
    else:
        assert "三张视图" in result and "(角色视图)=>@" in result
@pytest.mark.parametrize("named", [False, True])
def test_existing_asset_naming_and_foreign_language_voice(tmp_path: Path, named: bool) -> None:
    source = assets(tmp_path, "c1_Person", named)
    files = source.files(True)
    assert len(files) == 4 and files[-1][1].suffix == ".mp3"
    assert source.voice_id() == "zh-m-test-person-01"
    source.files()[1][1].unlink()
    with pytest.raises(ValueError, match="三张视图"):
        source.files()


def test_kit_uploads_and_manifest_are_bound_without_entities(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(seedance_kit, "REPO", tmp_path)
    source = assets(tmp_path, "c1_Person")
    md = shot(tmp_path, source)
    cfg = seedance_kit.config(tmp_path)
    refs, prompt, _ = seedance_kit.parse(md, cfg)
    filled = seedance_kit.kit_prompt(prompt, refs)
    assert all(f"@图片{i}" in filled for i in (1, 2, 3)) and "@音频1" in filled
    assert all(ref.src is not None for ref in refs)
    kit = seedance_kit.build(md)
    manifest = json.loads((kit / "kit.json").read_text(encoding="utf-8"))
    assert manifest["entities"] == [] and manifest[REFERENCE_MODE] == "uploads"
    for file in manifest["files"]:
        assert file["sha256"] == hashlib.sha256((tmp_path / file["src"]).read_bytes()).hexdigest()
    assert seedance_kit.stale(md) == []
    # 硬链接仍指同一文件时，也要识别内容改变，重新记录请求所用SHA。
    source.files(True)[-1][1].write_bytes(b"updated voice")
    assert any("哈希已变" in reason for reason in seedance_kit.stale(md))
    seedance_kit.build(md)
    assert seedance_kit.stale(md) == []


@pytest.mark.parametrize("card", ["c1_Person", "m1_Creature"])
def test_native_speaker_cannot_omit_audio(tmp_path: Path, card: str) -> None:
    source = assets(tmp_path, card)
    md = shot(tmp_path, source)
    md.write_text(md.read_text(encoding="utf-8").replace(f"、`{card}声音(声音音频)=>@`", ""), encoding="utf-8")
    with pytest.raises(SystemExit, match="声音缺失"):
        seedance_kit.parse(md, seedance_kit.config(tmp_path))


def test_silent_character_needs_no_voice_id(tmp_path: Path) -> None:
    md = shot(tmp_path, assets(tmp_path, "c1_Person", voice=False), voiced=False)
    refs, _, _ = seedance_kit.parse(md, seedance_kit.config(tmp_path))
    assert len(refs) == 3 and all(ref.kind == "图片" for ref in refs)


def test_unmatched_native_voice_is_not_treated_as_silent(tmp_path: Path) -> None:
    md = shot(tmp_path, assets(tmp_path, "c1_Person"), voiced=False)
    text = md.read_text(encoding="utf-8")
    md.write_text(text + "\n## 台词配音 prompt\n```text\n类型: 正常台词\n音色: male-wrong-person-01\n角色: Person\n```\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="voice_id未对应"):
        seedance_kit.parse(md, seedance_kit.config(tmp_path))


def test_upload_mode_rejects_entity_and_wrong_person_file(tmp_path: Path) -> None:
    source = assets(tmp_path, "c1_Person")
    md = shot(tmp_path, source)
    original = md.read_text(encoding="utf-8")
    md.write_text(original.replace("(2_world/characters/c1_Person/views/views1.png)", "(2_world/characters/c1_Person/views/views2.png)"), encoding="utf-8")
    with pytest.raises(SystemExit, match="绑定了其他角色文件"):
        seedance_kit.parse(md, seedance_kit.config(tmp_path))
    md.write_text(original.replace("- c1_Person视图1 → [`c1_Person视图1`](2_world/characters/c1_Person/views/views1.png)", "- c1_Person视图1 → 在 Seedance 里 @wow_c1_Person"), encoding="utf-8")
    with pytest.raises(SystemExit, match="禁止预建entity"):
        seedance_kit.parse(md, seedance_kit.config(tmp_path))


def test_cli_limit_failure_preserves_full_reference_set() -> None:
    refs = [seedance_kit.Ref(f"image{i}", Path(f"{i}.png"), "图片", i) for i in range(1, 16)]
    result = seedance_kit.cli_compatibility(refs, {"duration_s": "18"}, {"dreamina_cli": {"max_images": 9, "max_seconds": 15}})
    assert not result["ready"] and len(result["blockers"]) == 2
    assert len(refs) == 15


@pytest.mark.parametrize("model,ready", [("seedance2.5", True), ("seedance2.0", False), ("seedance2.0fast_vip", False)])
def test_cli_limits_follow_selected_model(model: str, ready: bool) -> None:
    refs = [seedance_kit.Ref(f"image{i}", Path(f"{i}.png"), "图片", i) for i in range(1, 15)]
    refs.extend(seedance_kit.Ref(f"audio{i}", Path(f"{i}.mp3"), "音频", i) for i in (1, 2))
    result = seedance_kit.cli_compatibility(refs, {"duration_s": 30}, {"dreamina_cli": {"model_version": model}})
    assert result["ready"] is ready
    assert result["model_version"] == model
    assert len(refs) == 16


@pytest.mark.parametrize("kind,key,suffix", [("图片", "max_images", "png"), ("视频", "max_videos", "mp4"), ("音频", "max_audios", "mp3")])
def test_seedance25_boundary_rejects_one_more_reference(kind: str, key: str, suffix: str) -> None:
    limit = seedance_kit.MODEL_LIMITS["seedance2.5"][key]
    refs = [seedance_kit.Ref(str(i), Path(f"{i}.{suffix}"), kind, i) for i in range(1, limit + 1)]
    cfg = {"dreamina_cli": {"model_version": "seedance2.5"}}
    assert seedance_kit.cli_compatibility(refs, {"duration_s": 30}, cfg)["ready"]
    refs.append(seedance_kit.Ref("extra", Path(f"extra.{suffix}"), kind, limit + 1))
    result = seedance_kit.cli_compatibility(refs, {"duration_s": 30}, cfg)
    assert not result["ready"] and len(result["blockers"]) == 1


def test_unknown_model_does_not_inherit_seedance25_limits() -> None:
    result = seedance_kit.cli_compatibility([], {"duration_s": 10}, {"dreamina_cli": {"model_version": "unverified", "max_images": 30}})
    assert not result["ready"]
    assert "未登记目标CLI模型" in result["blockers"][0]


def test_seedance25_rejects_31_seconds_and_respects_endpoint_override() -> None:
    cfg = {"dreamina_cli": {"model_version": "seedance2.5"}}
    result = seedance_kit.cli_compatibility([], {"duration_s": 31}, cfg)
    assert not result["ready"] and "镜长31s" in result["blockers"][0]
    refs = [seedance_kit.Ref(str(i), Path(f"{i}.png"), "图片", i) for i in range(1, 15)]
    cfg["dreamina_cli"]["max_images"] = 9
    result = seedance_kit.cli_compatibility(refs, {"duration_s": 10}, cfg)
    assert not result["ready"] and result["limits"]["max_images"] == 9


def test_cli_config_change_marks_kit_stale(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(seedance_kit, "REPO", tmp_path)
    md = shot(tmp_path, assets(tmp_path, "c1_Person"))
    seedance_kit.build(md)
    assert not seedance_kit.stale(md)
    (tmp_path / "seedance.toml").write_text('character_reference_mode = "uploads"\naudio_mode = "native"\n[dreamina_cli]\nmodel_version = "seedance2.5"\n', encoding="utf-8")
    assert "目标CLI模型或能力限制已变" in seedance_kit.stale(md)
