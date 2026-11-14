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


@pytest.mark.parametrize('target,prompt', [
    ('ai_videos/demo/characters/c1/a.png', 'portrait'),
    ('ai_videos/demo/episodes/ep01/scenes/s1/shots/st1/start.png', 'ep1_s1_st1 portrait close-up'),
    ('ai_videos/demo/props/p1/a.png', 'wooden prop'),
    ('ai_videos/demo/music/bgm1.png', 'bgm music art'),
])
@pytest.mark.parametrize('operation', ['text2image', 'image2image'])
def test_dreamina_never_makes_any_image(tmp_path, monkeypatch, operation, target, prompt):
    # follow-up 270：即梦只用于视频；人物、道具、镜头图、bgm 封面也一律拒绝，且不落请求日志、不执行
    calls = []
    monkeypatch.setattr(service_request.subprocess, 'run', lambda *a, **k: calls.append(a))
    log = service_request.RequestLog(tmp_path / target)
    with pytest.raises(ValueError, match='禁止 Dreamina'):
        log.cli(['dreamina', operation, '--prompt=' + prompt])
    assert not calls
    assert not log.path.exists()


@pytest.mark.parametrize('operation,target', [
    ('multimodal2video', 'ai_videos/demo/episodes/ep01/scenes/s1/shots/st1/take.mp4'),
    ('query_result', 'ai_videos/demo/scenes/bg2/old.png'),
    ('user_credit', 'ai_videos/demo/episodes/ep01/x'),
])
def test_dreamina_video_and_old_job_queries_stay_audited(tmp_path, monkeypatch, operation, target):
    calls = []
    def run(*args, **kwargs):
        calls.append(args)
        return {'ok': True}
    monkeypatch.setattr(service_request.subprocess, 'run', run)
    log = service_request.RequestLog(tmp_path / target)
    log.cli(['dreamina', operation, '--prompt=x'])
    assert len(calls) == 1
    assert '"event": "request"' in log.path.read_text(encoding='utf-8')
    assert '"event": "result"' in log.path.read_text(encoding='utf-8')


def _failing(calls, name, err):
    def run(*args):
        calls.append(name)
        raise err
    return run


def test_auto_never_calls_elevenlabs_and_fails_without_fallback(tmp_path, monkeypatch):
    """2026-11-08 用户：出图一律 Codex，没有用户允许不用 ElevenLabs（chuanyue_yiri follow-up 036）。"""
    job = SimpleNamespace(dir=tmp_path, plate=True, name='bg2')
    calls = []
    monkeypatch.setattr(bg, 'Job', lambda _: job)
    monkeypatch.setattr(bg, 'plan_for', lambda *args: (engines.CODEX, 'court', []))
    monkeypatch.setattr(bg, '_elevenlabs', _failing(calls, 'elevenlabs', TimeoutError('should not be called')))
    monkeypatch.setattr(bg, '_codex', _failing(calls, 'codex', TimeoutError('outcome unknown')))
    monkeypatch.setattr(bg, '_dreamina', lambda *args: calls.append('dreamina'))
    with pytest.raises(TimeoutError):
        bg.generate(job, None, engines.AUTO)
    assert calls == ['codex']   # 只用 Codex；失败就报出，不换 ElevenLabs、不退即梦


def test_scene_generation_stops_at_first_success(tmp_path, monkeypatch):
    job = SimpleNamespace(dir=tmp_path, plate=True, name='bg2')
    calls = []
    monkeypatch.setattr(bg, 'Job', lambda _: job)
    monkeypatch.setattr(bg, 'plan_for', lambda *args: (engines.CODEX, 'court', []))
    monkeypatch.setattr(bg, '_codex', lambda *args: calls.append('codex'))
    monkeypatch.setattr(bg, '_elevenlabs', lambda *args: calls.append('elevenlabs'))
    bg.generate(job, None, engines.AUTO)
    assert calls == ['codex']


def test_explicit_dreamina_rejected_before_scene_planning(tmp_path, monkeypatch):
    job = SimpleNamespace(dir=tmp_path, plate=False)
    monkeypatch.setattr(bg, 'Job', lambda _: job)
    monkeypatch.setattr(bg, 'plan_for', lambda *args: pytest.fail('should not plan a forbidden job'))
    with pytest.raises(ValueError, match='禁止 Dreamina'):
        bg.generate(job, None, engines.DREAMINA)


def test_engine_order_codex_only_never_dreamina():
    # 2026-11-08 用户：auto ＝ 只用 Codex；ElevenLabs 只在用户允许、显式点名时用（此前 follow-up 275 是 ElevenLabs → Codex）
    assert engines.CHOICES == (engines.AUTO, engines.CODEX, engines.ELEVENLABS)
    assert engines.scene_choice() == [engines.CODEX]
    for target in ('ai_videos/demo/2_世界观人设/characters/c1/c1.png', 'ai_videos/demo/background/bg2/bg2.png',
                   'ai_videos/demo/props/p1/p1-1_正面.png', None):
        assert engines.order(target=target) == [engines.CODEX]
        assert engines.order(target=target, dreamina_ok=False) == [engines.CODEX]
    # 显式 `--engine X` ＝ 只用 X；点名即梦一律报错
    for e in (engines.CODEX, engines.ELEVENLABS):
        assert engines.order(e, target='ai_videos/demo/props/p1/p1-1_正面.png') == [e]
    for target in ('ai_videos/demo/background/bg2/bg2.png', 'ai_videos/demo/props/p1/p1-1_正面.png'):
        with pytest.raises(ValueError, match='禁止 Dreamina'):
            engines.order(engines.DREAMINA, target=target)
    with pytest.raises(ValueError):
        engines.order('kling')


@pytest.mark.parametrize('target', ['ai_videos/demo/scenes/bg2/a.png', 'ai_videos/demo/props/p1/a.png'])
def test_direct_logged_image_api_cannot_bypass_cli_guard(tmp_path, target):
    log = service_request.RequestLog(tmp_path / target)
    with pytest.raises(ValueError, match='禁止 Dreamina'):
        log.invoke('dreamina', 'POST /image/generate', {'prompt': 'abbey'}, lambda: pytest.fail('forbidden API call'))


def test_elevenlabs_any_failure_falls_back_to_codex():
    # dota_yingxiong follow-up 066：ElevenLabs 有任何 blocker 都直接换 Codex，不问用户（取代 275 的只看额度）
    for err in ('ElevenLabs POST /flows/image HTTP 401：{"detail":{"status":"quota_exceeded"}}',
                '402 套餐不够（/flows/image 需要 Pro 及以上）', 'insufficient credits',
                'ElevenLabs POST /flows/image HTTP 422：invalid aspect_ratio', 'moderated', 'curl: (56)', 'timed out'):
        assert engines.fallback_ok(engines.ELEVENLABS, RuntimeError(err))
    assert engines.fallback_ok(engines.CODEX, RuntimeError('anything'))


def test_routing_key_line_not_sent(tmp_path):
    # dota_yingxiong follow-up 053：首行目录名常带原名（如「bg33_恶魔遗物」），只给人看，不发给模型
    d = tmp_path / 'background' / 'zone' / 'bg33_恶魔遗物'
    d.mkdir(parents=True)
    (d / 'bg33_恶魔遗物.md').write_text(
        '# 卡\n\n```text\nbg33_恶魔遗物\n参考: `bg1_x/bg1_x.png(世界基调)=>@`\n[主体]\n灰白退台石塔\n比例: 16:9\n```\n',
        encoding='utf-8')
    sent = bg.Job(d).send(with_neg=False)
    assert '恶魔遗物' not in sent and '参考:' not in sent
    assert sent.startswith('[主体]')
