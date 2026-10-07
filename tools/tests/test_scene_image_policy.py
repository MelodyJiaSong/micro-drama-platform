from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import gen_bg_images as bg
from tools import image_engine as engines
from tools import service_request


@pytest.mark.parametrize('target,prompt', [
    ('ai_videos/new/2_assets/scenes/continent/bg2/foo.png', 'exterior'),
    ('ai_videos/new/2_assets/background/continent/bg2/foo.png', 'exterior'),
    ('ai_videos/old/_series/scenes/bg2-2/court.png', 'courtyard'),
    ('ai_videos/demo/episodes/ep01/shots/shot01/bg23-1_front.png', 'background'),
    ('ai_videos/demo/episodes/ep01/shots/shot01/reference.png', 'bg23-1_front\nbackground'),
])
def test_forbidden_cli_never_executes(tmp_path, monkeypatch, target, prompt):
    calls = []
    monkeypatch.setattr(service_request.subprocess, 'run', lambda *a, **k: calls.append(a))
    with pytest.raises(ValueError, match='禁止 Dreamina'):
        service_request.RequestLog(tmp_path / target).cli(['dreamina', 'text2image', '--prompt', prompt])
    assert not calls


@pytest.mark.parametrize('operation,target,prompt', [
    ('text2image', 'ai_videos/demo/characters/c1/a.png', 'portrait'),
    ('text2image', 'ai_videos/demo/episodes/ep01/scenes/s1/shots/st1/start.png', 'ep1_s1_st1\nportrait close-up'),
    ('image2image', 'ai_videos/demo/props/p1/a.png', 'wooden prop'),
    ('text2image', 'ai_videos/demo/music/bgm1.png', 'bgm music art'),
    ('video', 'ai_videos/demo/scenes/bg2/video.mp4', 'scene video'),
    ('query_result', 'ai_videos/demo/scenes/bg2/old.png', ''),
])
def test_allowed_assets_videos_and_old_job_queries_stay_audited(tmp_path, monkeypatch, operation, target, prompt):
    calls = []
    def run(*args, **kwargs):
        calls.append(args)
        return {'ok': True}
    monkeypatch.setattr(service_request.subprocess, 'run', run)
    log = service_request.RequestLog(tmp_path / target)
    log.cli(['dreamina', operation, '--prompt=' + prompt])
    assert len(calls) == 1
    assert '"event": "request"' in log.path.read_text(encoding='utf-8')
    assert '"event": "result"' in log.path.read_text(encoding='utf-8')


def test_scene_generation_failure_never_falls_back_or_resubmits(tmp_path, monkeypatch):
    job = SimpleNamespace(dir=tmp_path, plate=True)
    calls = []
    monkeypatch.setattr(bg, 'Job', lambda _: job)
    monkeypatch.setattr(bg, 'plan_for', lambda *args: (engines.ELEVENLABS, 'court', []))
    def fail(*args):
        calls.append('elevenlabs')
        raise TimeoutError('outcome unknown')
    monkeypatch.setattr(bg, '_elevenlabs', fail)
    monkeypatch.setattr(bg, '_dreamina', lambda *args: calls.append('dreamina'))
    with pytest.raises(TimeoutError):
        bg.generate(job, None, engines.AUTO)
    assert calls == ['elevenlabs']


def test_explicit_dreamina_rejected_before_scene_planning(tmp_path, monkeypatch):
    job = SimpleNamespace(dir=tmp_path, plate=False)
    monkeypatch.setattr(bg, 'Job', lambda _: job)
    monkeypatch.setattr(bg, 'plan_for', lambda *args: pytest.fail('should not plan a forbidden job'))
    with pytest.raises(ValueError, match='禁止 Dreamina'):
        bg.generate(job, None, engines.DREAMINA)


def test_scene_default_and_other_asset_defaults():
    assert engines.scene_choice() == engines.ELEVENLABS
    assert engines.first_choice(False) == engines.DREAMINA
    assert engines.first_choice(True) == engines.ELEVENLABS


def test_direct_logged_image_api_cannot_bypass_cli_guard(tmp_path):
    log = service_request.RequestLog(tmp_path / 'ai_videos/demo/scenes/bg2/a.png')
    with pytest.raises(ValueError, match='禁止 Dreamina'):
        log.invoke('dreamina', 'POST /image/generate', {'prompt': 'abbey'}, lambda: pytest.fail('forbidden API call'))
