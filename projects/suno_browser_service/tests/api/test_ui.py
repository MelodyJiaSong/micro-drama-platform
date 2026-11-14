import json
import re
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from projects.suno_browser_service.libs.common.settings import AUTOMATION_PAUSE_FILENAME
from projects.suno_browser_service.tests.api.test_pipeline import live_pipeline, pipeline_site, TOKEN
from projects.suno_browser_service.tests.api.test_jobs import api


def test_openapi_describes_requests_operations_and_static_routes(api):
    client, _, _ = api
    spec = client.get('/openapi.json').json()
    assert spec['info']['description']
    for name in ['GenerationRequest', 'GenerationOptions', 'ReferenceInput', 'ResumeBody']:
        assert all(field.get('description') for field in spec['components']['schemas'][name]['properties'].values()), name
    for path, operations in spec['paths'].items():
        for operation in operations.values():
            assert operation['summary'] and operation['description'], path
    assert client.get('/ui/').status_code == 200, 'Build UI before testing: npm run build in apps/ui'
    assert "frame-ancestors 'none'" in client.get('/ui/').headers['content-security-policy']
    assert client.get('/v1/jobs').status_code == 401
    assert client.get('/v1/nonexistent').status_code == 404
    assert client.post('/ui/').status_code == 405
    assert client.get('/ui/../service-token.txt').status_code == 404


def test_ui_reference_modes_generate_preview_download_and_pause(live_pipeline, tmp_path):
    client, settings, site = live_pipeline
    media = tmp_path / 'reference.wav'
    media.write_bytes(site.audio)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 1100})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(str(client.base_url) + '/ui/')
        page.get_by_label('服务访问令牌', exact=True).fill(TOKEN)
        page.get_by_role('button', name='进入工作台').click()
        expect(page.get_by_role('heading', name='创作声音')).to_be_visible()
        page.get_by_role('button', name='音效 · Sounds', exact=True).click()
        page.locator('summary').filter(has_text='更多选项').click()
        page.get_by_label('声音类型', exact=False).select_option('loop')
        page.get_by_label('速度 · BPM', exact=False).fill('80')
        page.get_by_label('声音描述', exact=True).fill('Forest wind')
        page.get_by_role('button', name='预检 · 不收费', exact=True).click()
        expect(page.get_by_text('预检通过', exact=True)).to_be_visible()
        assert site.submissions == []
        page.get_by_role('button', name='自定义 · Advanced', exact=True).click()
        page.get_by_label('我有权使用接下来上传的素材').check()
        page.get_by_label('参考文件', exact=True).set_input_files(media)
        expect(page.get_by_text('reference.wav', exact=True)).to_be_visible()
        page.get_by_label('音乐风格', exact=True).fill('A quiet piano')
        page.get_by_role('button', name='预检 · 不收费', exact=True).click()
        expect(page.get_by_text('预检通过', exact=True)).to_be_visible()
        assert site.submissions == []
        page.get_by_role('button', name='移除参考 1', exact=True).click()
        page.get_by_label('下载格式', exact=True).select_option('wav')
        page.get_by_role('button', name='生成音乐', exact=False).click()
        expect(page.get_by_role('button', name='加载试听 / 下载').first).to_be_visible(timeout=35000)
        page.get_by_role('button', name='加载试听 / 下载').first.click()
        expect(page.get_by_text('SHA256 已核对', exact=True)).to_be_visible()
        expect(page.locator('audio')).to_have_count(1)
        with page.expect_download() as downloading:
            page.get_by_role('link', name='下载音频').click()
        saved = tmp_path / 'delivered.wav'
        downloading.value.save_as(saved)
        assert saved.read_bytes() == site.audio
        assert len(site.submissions) == 1
        (settings.data_dir / AUTOMATION_PAUSE_FILENAME).write_text('{}', encoding='utf-8')
        page.get_by_role('button', name='刷新任务', exact=True).click()
        expect(page.get_by_text('Suno 自动化已暂停', exact=True)).to_be_visible()
        expect(page.get_by_role('button', name='生成音乐', exact=False)).to_be_disabled()
        assert page.evaluate('sessionStorage.getItem("suno-pending-request-v1")') is None
        assert TOKEN not in page.content()
        for size in [{'width': 1440, 'height': 1100}, {'width': 390, 'height': 844}]:
            page.set_viewport_size(size)
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        assert not errors
        browser.close()


def test_ui_lost_submit_response_reuses_key_after_reload(live_pipeline):
    client, _, site = live_pipeline
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page()
        page.goto(str(client.base_url) + '/ui/')
        def login():
            page.get_by_label('服务访问令牌', exact=True).fill(TOKEN)
            page.get_by_role('button', name='进入工作台').click()
            expect(page.get_by_role('heading', name='创作声音')).to_be_visible()
        login()
        keys = []
        def lose_once(route):
            if route.request.method != 'POST':
                route.continue_(); return
            keys.append(route.request.headers['idempotency-key'])
            response = route.fetch()
            if len(keys) == 1: route.abort('failed')
            else: route.fulfill(response=response)
        page.route('**/v1/jobs', lose_once)
        page.get_by_label('音乐风格', exact=True).fill('A quiet piano')
        page.get_by_label('下载格式', exact=True).select_option('wav')
        page.get_by_role('button', name='生成音乐', exact=False).click()
        expect(page.get_by_role('button', name='重试同一请求')).to_be_enabled()
        pending = page.evaluate('sessionStorage.getItem("suno-pending-request-v1")')
        assert json.loads(pending)['key'] == keys[0] and TOKEN not in pending
        page.reload(); login()
        expect(page.get_by_label('音乐风格', exact=True)).to_be_disabled()
        page.get_by_role('button', name='重试同一请求').click()
        expect(page.get_by_role('button', name='加载试听 / 下载').first).to_be_visible(timeout=35000)
        assert len(keys) == 2 and len(set(keys)) == 1
        assert len(client.get('/v1/jobs').json()) == len(site.submissions) == 1
        browser.close()
