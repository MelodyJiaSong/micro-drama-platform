from libs.common.constants import SEAM_HARD_CUT


def test_envelope_and_sections(shot01):
    assert shot01.title.startswith("ep01 / shot01")
    assert "山门" in shot01.novel_excerpt
    assert shot01.shot_context["Summary"].startswith("林小雨")
    assert shot01.seam_mode == SEAM_HARD_CUT


def test_prompt_fields(shot01):
    assert shot01.prompt_fields["角色"].startswith("林小雨 — 青衫束发")
    assert shot01.prompt_fields["场景"].startswith("bg1_山门")
    assert "光线" in shot01.prompt_fields
    assert shot01.duration_s == 8.0
    assert shot01.aspect_ratio == "9:16"
    assert shot01.prompt_char_count > 100


def test_dialogue_and_voice(shot01):
    assert shot01.has_dialogue
    assert shot01.dialogue_types == frozenset({"内心独白"})
    assert len(shot01.voice_blocks) == 1
    block = shot01.voice_blocks[0]
    assert block.speaker == "林小雨"
    assert block.timbre.startswith("清亮")
    assert block.duration_target_s == 3.0


def test_applicability_vars(shot01, shot02):
    vars01 = shot01.applicability_vars()
    assert vars01["is_first_shot"] is True
    assert vars01["has_next_shot"] is True
    assert vars01["sub_type"] == "novel"
    vars02 = shot02.applicability_vars()
    assert vars02["is_last_shot"] is True
    assert "对白" in vars02["dialogue_types"]


def test_shot02_missing_timbre(shot02):
    assert shot02.voice_blocks[0].timbre == ""
