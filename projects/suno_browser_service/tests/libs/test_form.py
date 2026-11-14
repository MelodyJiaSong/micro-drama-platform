import io
from pathlib import Path

import pytest

from projects.suno_browser_service.tests.libs.test_browser import ui, browser_context, fixture_site, V6_FORM
from projects.suno_browser_service.tests.api.test_options import audio
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.generation import GenerationRequest
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.asset__client import AssetClient
from projects.suno_browser_service.libs.infrastructure.clients.form__client import FormClient

FORM = """<button role="tab" aria-selected="true">Songs</button><button role="tab" aria-selected="false" onclick="this.setAttribute('aria-selected','true')">Sounds</button>
<button role="tab" aria-selected="true">Advanced</button><button role="tab" aria-selected="false" onclick="this.setAttribute('aria-selected','true')">Simple</button>
<label>Style of Music<textarea id="styles"></textarea></label><label>Song Title<input></label>
<label>Lyrics<textarea></textarea></label><label>Instrumental<input type="checkbox"></label>
<label>Song description<textarea></textarea></label><label>Describe the sound you want<textarea></textarea></label>
<label>Model<select><option>v6</option><option>v6-wild</option><option>v6-mini</option></select></label>
<label>Add Voice<select><option>None</option><option>My Voice</option></select></label>
<label>Inspo<select><option>None</option><option>My Playlist</option></select></label>
<label>Exclude styles<input></label>
<label>Weirdness<input type="range" min="0" max="100" value="50"></label>
<label>Style Influence<input type="range" min="0" max="100" value="50"></label>
<label>Audio Influence<input type="range" min="0" max="100" value="50"></label>
<label>Variety<input type="range" min="0" max="100" value="50"></label>
<label>Max Mode<input type="checkbox"></label><label>My Taste<input type="checkbox"></label>
<div><span>Duration</span><button>Custom</button><input type="number" aria-label="Duration seconds" min="1" max="480"></div>
<div><span>Vocal Gender</span><button aria-pressed="false" onclick="this.setAttribute('aria-pressed','true')">Male</button><button aria-pressed="false" onclick="this.setAttribute('aria-pressed','true')">Female</button></div>
<button aria-pressed="false" onclick="this.setAttribute('aria-pressed','true')">One Shot</button><button aria-pressed="false" onclick="this.setAttribute('aria-pressed','true')">Loop</button><label>BPM<input type="number"></label>
<input type="file" onchange="const s=document.createElement('span');s.textContent=this.files[0].name;document.body.append(s)">
<button aria-label="Create song" onclick="window.createClicks++">Create</button><script>window.createClicks=0</script>"""


def test_all_advanced_options_read_back_and_rechecked_before_submit(ui, tmp_path):
    ui.page.set_content(FORM)
    assets = AssetClient(Settings(tmp_path))
    ref = assets.put("reference.wav", io.BytesIO(audio()), True)
    request = GenerationRequest(prompt="warm strings", instrumental=False, lyrics="A new day", references=[{"asset_id": ref["id"]}],
                                options={"model": "v6-wild", "exclude_styles": "drums", "vocal_gender": "female", "weirdness": 12,
                                         "style_influence": 88, "audio_influence": 35, "variety": 0, "duration_seconds": 90,
                                         "max_mode": False, "my_taste": True, "voice_name": "My Voice", "inspiration_name": "My Playlist"})
    form = FormClient(ui)
    form.prepare(request, "job-full-options", assets)
    assert ui.page.locator("#styles").input_value() == "warm strings"
    assert ui.page.get_by_label("Exclude styles").input_value() == "drums"
    assert ui.page.locator('input[type="file"]').evaluate("e=>e.files[0].type") == "audio/wav"
    assert set(request.options.model_dump(exclude_none=True)) <= set(form.applied)
    ui.submit("job-full-options")
    assert ui.page.evaluate("window.createClicks") == 1
    ui.page.get_by_label("Weirdness").press("ArrowRight")
    with pytest.raises(ServiceError, match="读回"):
        ui.submit("job-full-options")
    assert ui.page.evaluate("window.createClicks") == 1
    assert "upload_reference" in ui.audit.log.path.read_text(encoding="utf-8")


@pytest.mark.parametrize("mode,options", [("simple", {}), ("sounds", {"sound_type": "loop", "bpm": 90})])
def test_alternative_modes_fill_prompt_and_title(ui, tmp_path, mode, options):
    ui.page.set_content(FORM)
    form = FormClient(ui)
    form.prepare(GenerationRequest(prompt="Forest breeze", mode=mode, options=options), "job-mode", AssetClient(Settings(tmp_path)))
    ui.submit("job-mode")
    assert ui.page.evaluate("window.createClicks") == 1
    label = "Song description" if mode == "simple" else "Describe the sound you want"
    assert ui.page.get_by_label(label).input_value() == "Forest breeze"


# Live v6 Sounds panel (2026-10-24): no title field, One-Shot/Loop report data-selected, panel renders after the tab click.
V6_SOUNDS = """<button role="tab" aria-selected="true">Songs</button>
<button role="tab" aria-selected="false" onclick="this.setAttribute('aria-selected','true');setTimeout(()=>document.getElementById('panel').hidden=false,600)">Sounds</button>
<div id="panel" hidden><textarea placeholder="Describe the sound you want" maxlength="500"></textarea>
<button type="button" data-selected="true" onclick="this.dataset.selected='true';this.nextElementSibling.dataset.selected='false'">One-Shot</button><button type="button" data-selected="false" onclick="this.dataset.selected='true';this.previousElementSibling.dataset.selected='false'">Loop</button>
<input type="number" placeholder="Auto" min="1" max="300"></div>
<button aria-label="Create song" onclick="window.createClicks++">Create</button><script>window.createClicks=0</script>"""


@pytest.mark.parametrize("sound_type", ["one_shot", "loop"])
def test_v6_sounds_without_title_waits_for_panel_and_reads_back_type(ui, tmp_path, sound_type):
    ui.page.set_content(V6_SOUNDS)
    form = FormClient(ui)
    form.prepare(GenerationRequest(prompt="Holy bell impact", mode="sounds", options={"sound_type": sound_type}), "job-sounds", AssetClient(Settings(tmp_path)))
    assert ui.title_field is False
    label = "One-Shot" if sound_type == "one_shot" else "Loop"
    assert ui.page.get_by_role("button", name=label, exact=True).get_attribute("data-selected") == "true"
    ui.submit("job-sounds")
    assert ui.page.evaluate("window.createClicks") == 1
    assert ui.page.get_by_placeholder("Describe the sound you want").input_value() == "Holy bell impact"


def test_v6_sounds_prompt_over_page_limit_never_submits(ui, tmp_path):
    ui.page.set_content(V6_SOUNDS)
    with pytest.raises(ValueError):
        GenerationRequest(prompt="x" * 501, mode="sounds")
    # The page's maxlength still guards requests that bypass validation.
    request = GenerationRequest.model_construct(prompt="x" * 501, mode="sounds", instrumental=True, references=[], options=GenerationRequest.model_fields["options"].default_factory())
    with pytest.raises(ServiceError) as error:
        FormClient(ui).prepare(request, "job-long", AssetClient(Settings(tmp_path)))
    assert error.value.code == "prompt_too_long"
    assert ui.page.evaluate("window.createClicks") == 0


def test_missing_requested_option_never_submits(ui, tmp_path):
    ui.page.set_content(FORM)
    ui.page.get_by_label("Weirdness").evaluate("e=>e.remove()")
    with pytest.raises(ServiceError):
        FormClient(ui).prepare(GenerationRequest(prompt="Piano", options={"weirdness": 20}), "job-missing", AssetClient(Settings(tmp_path)))
    assert ui.page.evaluate("window.createClicks") == 0


def test_v6_style_does_not_match_exclude_styles_placeholder(ui):
    ui.page.set_content(V6_FORM + '<input placeholder="Exclude styles">')
    ui.prepare("Soft cello", "job-style", True, None)
    assert ui.page.locator('textarea:not([aria-label])').input_value() == "Soft cello"
    assert ui.page.get_by_placeholder("Exclude styles", exact=True).input_value() == ""


def test_missing_unique_title_cannot_generate_in_simple(ui, tmp_path):
    ui.page.set_content(FORM)
    ui.page.get_by_label("Song Title").evaluate("e=>e.remove()")
    ui.overrides["title"] = "#nonexistent"
    with pytest.raises(ServiceError):
        FormClient(ui).prepare(GenerationRequest(prompt="Piano", mode="simple"), "task", AssetClient(Settings(tmp_path)))
    assert ui.page.evaluate("window.createClicks") == 0


def test_upload_audit_failure_prevents_file_input(ui, tmp_path, monkeypatch):
    ui.page.set_content(FORM)
    assets = AssetClient(Settings(tmp_path))
    ref = assets.put("ref.wav", io.BytesIO(audio()), True)
    original = ui.audit.call
    def audited(operation, request, action):
        if operation == "upload_reference":
            raise OSError("audit unavailable")
        return original(operation, request, action)
    monkeypatch.setattr(ui.audit, "call", audited)
    with pytest.raises(OSError, match="audit unavailable"):
        FormClient(ui).prepare(GenerationRequest(prompt="Piano", references=[{"asset_id": ref["id"]}]), "task", assets)
    assert ui.page.locator('input[type="file"]').evaluate("e=>e.files.length") == 0
    assert ui.page.evaluate("window.createClicks") == 0


def test_rights_checkbox_is_never_implicitly_accepted(ui, tmp_path):
    ui.page.set_content(FORM + '<label>I own the rights<input type="checkbox"></label><button>Upload</button>')
    assets = AssetClient(Settings(tmp_path))
    ref = assets.put("ref.wav", io.BytesIO(audio()), False)
    with pytest.raises(ServiceError) as error:
        FormClient(ui).prepare(GenerationRequest(prompt="Piano", references=[{"asset_id": ref["id"]}]), "task", assets)
    assert error.value.code == "reference_rights_required"
    assert not ui.page.get_by_label("I own the rights").is_checked()
    assert ui.page.evaluate("window.createClicks") == 0


def test_sounds_clips_are_claimed_by_prompt_not_by_other_sessions(ui, tmp_path):
    rows = """<div><div><a href="/song/00000000-0000-4000-8000-0000000000a1">Divine Shield Cast...</a><p>SOUND</p><p>Divine shield cast, a crisp burst, No speech</p><button aria-label="More options">o</button></div></div>
<div><div><a href="/song/00000000-0000-4000-8000-0000000000b2">Freezing Field...</a><p>SOUND</p><p>Freezing field ice storm</p><button aria-label="More options">o</button></div></div>
<div><div><a href="/song/00000000-0000-4000-8000-0000000000a3">Divine Shield Cast...</a><p>SOUND</p><p>Divine shield cast, a crisp burst, No speech</p><button aria-label="More options">o</button></div></div>"""
    ui.page.set_content(V6_SOUNDS)
    FormClient(ui).prepare(GenerationRequest(prompt="Divine shield cast. A crisp burst. No speech.", mode="sounds"), "job-claim", AssetClient(Settings(tmp_path)))
    ui.page.evaluate("html => document.body.insertAdjacentHTML('beforeend', html)", rows)
    assert ui.collect("job-claim", []) == ["https://suno.com/song/00000000-0000-4000-8000-0000000000a1", "https://suno.com/song/00000000-0000-4000-8000-0000000000a3"]
