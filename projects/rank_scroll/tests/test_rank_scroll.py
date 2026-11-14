import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

from rank_scroll.contract import ContractError, load_episode
from rank_scroll.render import RenderOptions, Renderer, render_video
from rank_scroll.timeline import FPS, SPEED, W, build

from fixture import make_episode


@pytest.fixture(scope="module")
def ep_dir(tmp_path_factory):
    return make_episode(tmp_path_factory.mktemp("ep") / "fx")


@pytest.fixture(scope="module")
def ep(ep_dir):
    e, _ = load_episode(ep_dir)
    return e


def test_validate_ok(ep):
    assert len(ep.items) == 14 and len(ep.insights) == 2


@pytest.mark.parametrize("mutate,needle", [
    (lambda d: d["items"][0]["tags"].append({"icon": "rocket", "text": "x"}), "unknown icon"),
    (lambda d: d["items"][1].update(badge="X" * 30), "badge longer"),
    (lambda d: d["insights"].append({"after_rank": 99, "text": "x"}), "after_rank 99"),
    (lambda d: d["items"].reverse(), "out of order"),
    (lambda d: d["items"][2].update(country_iso2="QQ"), "flag not found"),
    (lambda d: d["items"][3].update(image="assets/img/not_in_ledger.jpg"), "image missing"),
])
def test_validate_errors(ep_dir, tmp_path, mutate, needle):
    bad = tmp_path / "bad"
    shutil.copytree(ep_dir, bad)
    d = json.loads((bad / "data.json").read_text(encoding="utf-8"))
    mutate(d)
    (bad / "data.json").write_text(json.dumps(d), encoding="utf-8")
    try:
        _, warnings = load_episode(bad, strict_images=True)
    except ContractError as e:
        assert any(needle in err for err in e.errors), e.errors
    else:
        pytest.fail(f"expected ContractError containing {needle!r}; warnings={warnings}")


def test_rejects_nc_licence(ep_dir, tmp_path):
    bad = tmp_path / "nc"
    shutil.copytree(ep_dir, bad)
    led = json.loads((bad / "assets.json").read_text(encoding="utf-8"))
    led[0]["licence"] = "CC BY-NC 4.0"
    (bad / "assets.json").write_text(json.dumps(led), encoding="utf-8")
    with pytest.raises(ContractError) as ei:
        load_episode(bad)
    assert any("licence not accepted" in e for e in ei.value.errors)


@pytest.mark.parametrize("lic", ["Pexels License", "Unsplash License", "Pixabay Content License"])
def test_accepts_free_stock_licences(ep_dir, tmp_path, lic):
    ok = tmp_path / "stock"
    shutil.copytree(ep_dir, ok)
    led = json.loads((ok / "assets.json").read_text(encoding="utf-8"))
    led[0]["licence"] = lic
    (ok / "assets.json").write_text(json.dumps(led), encoding="utf-8")
    load_episode(ok)


def test_unknown_licence_only_with_risk_signoff(ep_dir, tmp_path):
    d = tmp_path / "risk"
    shutil.copytree(ep_dir, d)
    led = json.loads((d / "assets.json").read_text(encoding="utf-8"))
    led[0]["licence"] = "unknown"
    (d / "assets.json").write_text(json.dumps(led), encoding="utf-8")
    data = json.loads((d / "data.json").read_text(encoding="utf-8"))
    item = next(it for it in data["items"] if it.get("image", "").replace("\\", "/") == led[0]["file"])
    with pytest.raises(ContractError):
        load_episode(d)                                   # 未标风险：许可未知直接拒
    item["image_risk"] = "licence unknown"
    (d / "data.json").write_text(json.dumps(data), encoding="utf-8")
    ep, _ = load_episode(d)                               # 标了风险、默认：扣下不用
    assert all(i.image is None for i in ep.items if i.name == item["name"])
    ep, _ = load_episode(d, allow_risk_images=True)       # 签字放行：用图
    assert any(i.image is not None for i in ep.items if i.name == item["name"])


@pytest.mark.parametrize("iso", ["TW", "HK", "MO"])
def test_zh_rejects_region_as_country(ep_dir, tmp_path, iso):
    d = tmp_path / "zh"
    shutil.copytree(ep_dir, d)
    data = json.loads((d / "data.json").read_text(encoding="utf-8"))
    data["items"][0]["country_iso2"] = iso
    (d / "data.zh.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ContractError) as ei:
        load_episode(d, lang="zh")
    assert any("中文版不得使用" in e for e in ei.value.errors)


def test_zh_reads_zh_file_and_tally_labels(ep_dir, tmp_path):
    d = tmp_path / "zh2"
    shutil.copytree(ep_dir, d)
    data = json.loads((d / "data.json").read_text(encoding="utf-8"))
    data["title"] = "中文标题"
    data.setdefault("tally", {"by": "country", "title": "计分"})["labels"] = {"CN": "中国"}
    (d / "data.zh.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    ep, _ = load_episode(d, lang="zh")
    assert ep.lang == "zh" and ep.title == "中文标题" and ep.tally_labels == {"CN": "中国"}
    en, _ = load_episode(d)
    assert en.lang == "en" and en.title != "中文标题"


def test_timeline_order_and_champion(ep):
    tl = build(ep)
    cards = [e for e in tl.elements if e.kind == "card"]
    assert [ep.items[e.index].rank for e in cards] == sorted((it.rank for it in ep.items), reverse=True)
    assert tl.elements[-1].kind == "card" and ep.items[tl.elements[-1].index].rank == 1
    # insight after rank 11 sits right after the rank-11 card
    k = next(i for i, e in enumerate(tl.elements) if e.kind == "card" and e.rank == 11)
    assert tl.elements[k + 1].kind == "insight"
    end_scroll = tl.segments[1][2]
    assert tl.camera(end_scroll) == tl.cam_end
    assert tl.camera(end_scroll + 100) == tl.cam_end


def test_constant_segment_is_integer_pixels(ep):
    tl = build(ep)
    xs = [tl.camera(f) for f in range(tl.f_intro, tl.f_intro + tl.f_const + 1)]
    steps = {round(b - a, 6) for a, b in zip(xs, xs[1:])}
    assert steps == {float(SPEED)}
    assert all(float(x).is_integer() for x in xs)


def test_first_card_left_third_at_scroll_start(ep):
    tl = build(ep)
    first = tl.elements[0]
    screen_x = W / 2 + first.center - tl.camera(tl.f_intro)
    left_edge = screen_x - ep.card_w * first.scale / 2
    assert 38 <= left_edge <= 42 and float(screen_x).is_integer()


def test_frames_deterministic(ep):
    r1, r2 = Renderer(ep, RenderOptions(out_scale=0.5)), Renderer(ep, RenderOptions(out_scale=0.5))
    for f in (30, 600, 3000):
        assert np.array_equal(r1.frame(f).copy(), r2.frame(f).copy())


def test_short_render_ffprobe(ep, tmp_path):
    out = tmp_path / "clip.mp4"
    m = render_video(ep, out, RenderOptions(out_scale=0.5, step=2, draft=False), None, 8.0, 10.0, log=lambda *_: None)
    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(out)],
        capture_output=True, text=True, check=True).stdout)
    v = next(s for s in probe["streams"] if s["codec_type"] == "video")
    a = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    assert (v["width"], v["height"], v["codec_name"], v["pix_fmt"]) == (960, 540, "h264", "yuv420p")
    assert v["r_frame_rate"] == "30/1" and a["codec_name"] == "aac"
    assert abs(float(probe["format"]["duration"]) - 2.0) < 0.1
    assert Path(str(out.with_suffix(".manifest.json"))).is_file() and m["inputs"]["data.json"]


def test_image_risk_withheld_by_default(ep_dir, tmp_path):
    d2 = tmp_path / "risk"
    shutil.copytree(ep_dir, d2)
    d = json.loads((d2 / "data.json").read_text(encoding="utf-8"))
    d["items"][0]["image_risk"] = "no commercial FoP"
    d["scope_note"] = "What counts: test."
    (d2 / "data.json").write_text(json.dumps(d), encoding="utf-8")
    safe, warns = load_episode(d2)
    assert safe.items[0].image is None and safe.items[0].image_withheld and "withheld" in safe.items[0].image_note.lower()
    assert any("withheld" in w for w in warns) and safe.scope_note == "What counts: test."
    full, _ = load_episode(d2, allow_risk_images=True)
    assert full.items[0].image is not None
    from rank_scroll.publish import draft
    text = draft(safe)
    assert "What counts: test." in text and "#1 Test Tower Number 1:" not in text.split("## Comment")[0]


def test_image_alt_replaces_withheld_risk_photo(ep_dir, tmp_path):
    """contract v1.4 (paihangbang follow-up 020): image_alt fills the tile in the default master."""
    d2 = tmp_path / "alt"
    shutil.copytree(ep_dir, d2)
    d = json.loads((d2 / "data.json").read_text(encoding="utf-8"))
    led = json.loads((d2 / "assets.json").read_text(encoding="utf-8"))
    alt = dict(next(e for e in led if e["file"] == d["items"][1]["image"].replace("\\", "/")))
    alt.update(file="assets/img/alt_gen.png", licence="AI-generated (Codex image_gen)", author="AI-generated")
    shutil.copy(d2 / d["items"][1]["image"], d2 / alt["file"])
    led.append(alt)
    d["items"][0].update(image_risk="no commercial FoP", image_alt=alt["file"], image_alt_credit="AI-generated")
    (d2 / "data.json").write_text(json.dumps(d), encoding="utf-8")
    (d2 / "assets.json").write_text(json.dumps(led), encoding="utf-8")
    safe, _ = load_episode(d2, strict_images=True)
    assert safe.items[0].image.name == "alt_gen.png" and not safe.items[0].image_withheld
    assert safe.items[0].image_credit == "AI-generated"
    full, _ = load_episode(d2, allow_risk_images=True)
    assert full.items[0].image.name != "alt_gen.png"
    from rank_scroll.publish import draft
    assert "AI-generated (Codex image_gen)" in draft(safe)
    assert safe.items[0].image_ai and not full.items[0].image_ai   # AI IMAGE chip only on the generated photo
    from rank_scroll.cards import card_image
    from rank_scroll.theme import get_theme
    assert card_image(safe, safe.items[0], get_theme(safe.theme)[0], 1.0) is not None


# ---------- list mode + company card (contract v1.3, follow-up 004) ----------
def _make_list_episode(src: Path, dst: Path, person_risk: bool = False) -> Path:
    shutil.copytree(src, dst)
    d = json.loads((dst / "data.json").read_text(encoding="utf-8"))
    ledger = json.loads((dst / "assets.json").read_text(encoding="utf-8"))
    d["mode"] = "list"
    d["kicker"] = "14 COMPANIES"
    d["layout"] = {"card_w": 720, "focus": [0.5, 0.4]}
    for i, it in enumerate(d["items"]):
        it["corner"] = f"EST. {2010 + i}"
        it["logo"] = "assets/img/01_item.jpg"
        it["person"] = {"name": f"Founder Person {i}", "role": "Co-founder & CEO", "image": "assets/img/02_item.jpg",
                        "credit": "Synthetic / CC0", **({"image_risk": "licence unknown"} if person_risk and i == 0 else {})}
    # 01_item.jpg becomes a logo-only ledger entry (trademark: no free licence needed, identification only)
    ledger = [e for e in ledger if e["file"] != "assets/img/01_item.jpg"]
    ledger.append({"file": "assets/img/01_item.jpg", "kind": "logo", "licence": "Trademark (identification only)"})
    d["items"][0]["image"] = "assets/img/03_item.jpg"       # so item 1 needs another main photo
    d["insights"] = [{"after_rank": 5, "text": "Insight after the fifth item."}]
    (dst / "data.json").write_text(json.dumps(d), encoding="utf-8")
    (dst / "assets.json").write_text(json.dumps(ledger), encoding="utf-8")
    return dst


@pytest.fixture(scope="module")
def list_dir(ep_dir, tmp_path_factory):
    return _make_list_episode(ep_dir, tmp_path_factory.mktemp("ls") / "list", person_risk=True)


def test_list_mode_order_and_no_champion(list_dir):
    ep, warns = load_episode(list_dir)
    assert ep.is_list and all(it.company_card for it in ep.items)
    assert ep.items[0].person_image is None and any("person photo withheld" in w for w in warns)
    assert ep.items[1].person_image is not None and ep.items[0].logo is not None
    tl = build(ep)
    cards = [e for e in tl.elements if e.kind == "card"]
    assert [e.rank for e in cards] == list(range(1, 15))        # file order, first item enters first
    assert all(e.scale == 1.0 for e in cards)                    # no enlarged top 10
    assert tl.elements[-1].index == 13 and tl.camera(tl.segments[1][2]) == tl.elements[-1].center
    assert (tl.segments[2][2] - tl.segments[2][1]) / FPS == 4.0
    k = next(i for i, e in enumerate(tl.elements) if e.kind == "card" and e.rank == 5)
    assert tl.elements[k + 1].kind == "insight"
    r = Renderer(ep, RenderOptions(out_scale=0.5))
    for f in (400, tl.segments[2][1] + 30):
        assert r.frame(f).any()


@pytest.mark.parametrize("mutate,needle", [
    (lambda d: d["items"][0].update(rank=2), "must equal its position"),
    (lambda d: d["items"][0].update(corner="X" * 20), "corner longer"),
    (lambda d: d["items"][1].update(logo="assets/img/04_item.jpg"), "kind='logo'"),
    (lambda d: d["insights"].append({"after_rank": 14, "text": "x"}), "after the last item"),
    (lambda d: d.update(mode="carousel"), "mode must be"),
])
def test_list_mode_errors(list_dir, tmp_path, mutate, needle):
    bad = tmp_path / "bad"
    shutil.copytree(list_dir, bad)
    d = json.loads((bad / "data.json").read_text(encoding="utf-8"))
    mutate(d)
    (bad / "data.json").write_text(json.dumps(d), encoding="utf-8")
    with pytest.raises(ContractError) as ei:
        load_episode(bad)
    assert any(needle in e for e in ei.value.errors), ei.value.errors


# ── music bed (follow-up: audio QC — junction energy hole, cut-off ending, loudnorm gain drift) ──
def test_parse_track_in_out(tmp_path):
    from rank_scroll.render import parse_track
    assert parse_track("C:/m/a.mp3") == (Path("C:/m/a.mp3"), None, None)
    assert parse_track("C:/m/a.mp3@:188") == (Path("C:/m/a.mp3"), None, 188.0)
    assert parse_track("a.mp3@12.5:190") == (Path("a.mp3"), 12.5, 190.0)
    assert parse_track("a.mp3@7") == (Path("a.mp3"), 7.0, None)


def test_music_bed_fit_end_and_linear_loudnorm(tmp_path):
    import shutil as _sh
    import subprocess as _sp
    import pytest
    if not _sh.which("ffmpeg"):
        pytest.skip("ffmpeg missing")
    from rank_scroll.render import build_music_bed
    a, b = tmp_path / "a.wav", tmp_path / "b.wav"
    for f, hz, d in ((a, 220, 30), (b, 330, 40)):
        _sp.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"sine=frequency={hz}:duration={d}",
                 "-ac", "2", str(f)], check=True)
    out = tmp_path / "bed.wav"
    info = build_music_bed([f"{a}@:25", str(b)], 50.0, 0.0, 50.0, "end", out, log=lambda *_: None)
    # chain = 25 + 40 - 4 = 61 s for a 50 s video → the last track skips its first 11 s and ends with the video
    assert info["tracks"][0]["out_s"] == 25.0
    assert abs(info["tracks"][1]["in_s"] - 11.0) < 0.01
    dur = float(_sp.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                        capture_output=True, text=True).stdout)
    assert abs(dur - 50.0) < 0.1
    assert "input_i" in info["loudnorm_pass1"]


def test_flagless_mode_skips_flags(ep_dir, tmp_path):
    """layout.flags=false (follow-up 007): blank country_iso2 is fine, no flag is drawn or scheduled to wave."""
    d = tmp_path / "noflags"
    shutil.copytree(ep_dir, d)
    data = json.loads((d / "data.json").read_text(encoding="utf-8"))
    data.setdefault("layout", {})["flags"] = False
    data["theme"] = "virus"
    for it in data["items"]:
        it["country_iso2"] = ""
    (d / "data.json").write_text(json.dumps(data), encoding="utf-8")
    ep, _ = load_episode(d)
    assert not ep.show_flags
    r = Renderer(ep, RenderOptions(out_scale=0.5, step=2, draft=True))
    r.frame(int(build(ep).segments[1][1]) + 60)
    assert all(not v for v in r._elem_flags.values())
    bad = json.loads(json.dumps(data))
    bad["layout"]["flags"] = "no"
    (d / "data.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ContractError, match="layout.flags"):
        load_episode(d)


def test_licence_ai_generated_accepted():
    from rank_scroll.contract import _licence_ok
    assert _licence_ok("AI-generated")
    assert not _licence_ok("CC BY-NC 2.0")


def test_intro_hold_keeps_band_still_then_scrolls(ep):
    """layout.intro_hold (follow-up 008): the first card stays readable before the scroll starts."""
    import dataclasses
    base = build(ep)
    held = build(dataclasses.replace(ep, intro_hold=2.5))
    hold = int(2.5 * FPS)
    assert held.f_hold == hold and base.f_hold == 0
    assert held.segments[1][2] - held.segments[1][1] == base.segments[1][2] - base.segments[1][1] + hold
    assert {held.camera(f) for f in range(held.f_intro, held.f_intro + hold + 1)} == {float(held.cam_start)}
    assert held.camera(held.f_intro + hold + 1) == held.cam_start + SPEED
    assert held.camera(held.segments[1][2]) == held.cam_end


def test_tally_icons_and_synthetic_disclosure(ep_dir, tmp_path):
    """tally.icons maps groups to icons; AI-generated ledger entries switch the upload checklist to Yes (follow-up 009)."""
    d = tmp_path / "icons"
    shutil.copytree(ep_dir, d)
    data = json.loads((d / "data.json").read_text(encoding="utf-8"))
    data["tally"] = {"by": "continent", "title": "Groups", "icons": {"Asia": "paw"}}
    (d / "data.json").write_text(json.dumps(data), encoding="utf-8")
    ledger = json.loads((d / "assets.json").read_text(encoding="utf-8"))
    ledger[0]["licence"] = "AI-generated (test)"
    (d / "assets.json").write_text(json.dumps(ledger), encoding="utf-8")
    ep, _ = load_episode(d)
    assert ep.tally_icons == {"Asia": "paw"}
    from rank_scroll.publish import draft
    assert "选 Yes" in draft(ep)
    data["tally"]["icons"] = {"Asia": "not-an-icon"}
    (d / "data.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ContractError, match="tally.icons"):
        load_episode(d)
