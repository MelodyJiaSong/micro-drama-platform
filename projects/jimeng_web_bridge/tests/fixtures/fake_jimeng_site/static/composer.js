(function () {
  const FJ = window.FJ;
  const el = FJ.el;
  const C = (FJ.Composer = {});
  const TYPES = ['Agent 模式', '图片生成', '视频生成', '音乐生成', '音频生成', '数字人', '动作模仿'];
  const MODELS = [
    ['即梦 Seedance 2.5', '最强模型，支持 50 个参考，新增视频编辑、超长生成'],
    ['Seedance 2.0 mini', '极致性价比'],
    ['Seedance 2.0 Fast VIP', '会员专属通道；暂不支持真人人脸'],
    ['Seedance 2.0 VIP', '会员专属通道'],
    ['Seedance 2.0 Fast', '暂不支持真人人脸'],
    ['Seedance 2.0', '标准通道'],
  ];
  const MODES = ['全能参考', '首尾帧', '智能多帧', '智能编辑（Beta）', '超长视频（Beta）'];
  const RATIOS = ['21:9', '16:9', '4:3', '1:1', '3:4', '9:16'];
  const RESOLUTIONS = ['480P', '720P', '1080P'];
  const COUNTS = ['1', '2', '3', '4'];
  const PRICE = { '即梦 Seedance 2.5': 20, 'Seedance 2.0 VIP': 14, 'Seedance 2.0 Fast VIP': 10, 'Seedance 2.0': 8, 'Seedance 2.0 Fast': 6, 'Seedance 2.0 mini': 4 };

  C.params = { type: 'Agent 模式', model: '即梦 Seedance 2.5', mode: '全能参考', ratio: '9:16', resolution: '720P', count: '1', duration: '26' };

  C.mount = function (main) {
    const section = el('section', { class: 'composer', 'aria-label': '视频创作输入区' });
    C.uploadList = el('div', { role: 'list', 'aria-label': '参考素材', class: 'upload-list' });
    const uploadTile = el('div', { role: 'button', tabindex: '0', 'aria-label': '上传参考内容', title: '上传参考内容', class: 'upload-tile' }, ['+ 参考内容']);
    uploadTile.addEventListener('click', onUploadClick);
    section.append(C.uploadList, uploadTile);
    FJ.Editor.mount(section);
    C.negative = el('textarea', { 'aria-label': '负向提示词', placeholder: '不希望出现的内容' });
    C.negativeBox = el('div', { class: 'negative-box' }, [C.negative]);
    C.negativeBox.hidden = !FJ.cfg.negative_box;
    section.appendChild(C.negativeBox);

    const toolbar = el('div', { role: 'toolbar', 'aria-label': '创作工具栏', class: 'toolbar' });
    C.btnType = el('button', { 'aria-haspopup': 'listbox', 'aria-busy': 'true' });
    C.btnModel = el('button', { 'aria-haspopup': 'listbox' });
    C.btnMode = el('button', { 'aria-haspopup': 'listbox' });
    C.btnRrc = el('button', { 'aria-haspopup': 'dialog' });
    C.btnDuration = el('button', { 'aria-haspopup': 'dialog' });
    const btnAt = el('button', { 'aria-label': '@' }, ['@']);
    C.notice = el('div', { role: 'status', class: 'parallel-notice' }, ['并行任务已达上限，请稍后再试']);
    C.notice.hidden = true;
    C.credits = el('div', { class: 'credits', 'aria-label': '预计积分' }, [el('span', { class: 'now' }), el('s', { class: 'origin' })]);
    C.send = el('button', { 'aria-label': '发送', class: 'send' }, ['↑']);
    toolbar.append(C.btnType, C.btnModel, C.btnMode, C.btnRrc, C.btnDuration, btnAt, el('span', { class: 'spacer' }), C.notice, C.credits, C.send);
    section.appendChild(toolbar);
    main.appendChild(section);

    C.btnType.addEventListener('click', function () { openList('type', '创作类型', C.btnType, TYPES.map(function (t) { return [t, '']; })); });
    C.btnModel.addEventListener('click', function () { openList('model', '模型', C.btnModel, MODELS); });
    C.btnMode.addEventListener('click', function () { openList('mode', '参考模式', C.btnMode, MODES.map(function (m) { return [m, '']; })); });
    C.btnRrc.addEventListener('click', openRrc);
    C.btnDuration.addEventListener('click', openDuration);
    btnAt.addEventListener('click', function () { FJ.Editor.node.focus(); document.execCommand('insertText', false, '@'); });
    C.send.addEventListener('click', function () { C.generate('click'); });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape') closePopovers(); });
    document.addEventListener('mousedown', function (event) {
      if (C.popover && !C.popover.contains(event.target) && !event.target.closest('.toolbar')) closePopovers();
    });
    render();
    setTimeout(function () {
      C.params.type = FJ.cfg.last_creation_type;
      C.btnType.removeAttribute('aria-busy');
      render();
    }, 300);
  };

  function render() {
    const p = C.params;
    C.btnType.textContent = p.type;
    C.btnModel.textContent = p.model;
    C.btnMode.textContent = p.mode;
    C.btnRrc.textContent = p.ratio + ' · ' + p.resolution + ' · ' + p.count + '个';
    C.btnDuration.textContent = p.duration + 's';
    const seconds = parseInt(p.duration, 10) || 0;
    const count = parseInt(p.count, 10) || 1;
    C.credits.querySelector('.now').textContent = String(seconds * (PRICE[p.model] || 20) * count);
    C.credits.querySelector('.origin').textContent = String(seconds * 26 * count);
  }

  const KEYS = { type: 'type', model: 'model', mode: 'mode', ratio: 'ratio', resolution: 'resolution', count: 'count', duration: 'duration' };

  async function setParam(control, value) {
    const d = await FJ.act('set_param', { control: control, value: value });
    if (d.block) return;
    C.params[KEYS[control]] = String(d.display !== undefined && d.display !== null ? d.display : value);
    render();
  }

  function place(node, anchor) {
    const rect = anchor.getBoundingClientRect();
    node.style.left = Math.max(8, rect.left) + 'px';
    node.style.bottom = (window.innerHeight - rect.top + 6) + 'px';
    document.body.appendChild(node);
    C.popover = node;
  }

  function closePopovers() {
    if (C.popover) C.popover.remove();
    C.popover = null;
  }

  async function openList(control, label, anchor, options) {
    const d = await FJ.act('open_control', { control: control });
    if (d.block) return;
    closePopovers();
    const box = el('div', { role: 'listbox', 'aria-label': label, class: 'popover' });
    options.forEach(function (pair) {
      const option = el('div', { role: 'option', class: 'option', 'aria-selected': String(C.params[control] === pair[0]) }, [
        el('div', { class: 'opt-title' }, [pair[0]]),
        pair[1] ? el('div', { class: 'opt-desc' }, [pair[1]]) : null,
      ]);
      option.addEventListener('click', async function () {
        closePopovers();
        await setParam(control, pair[0]);
      });
      box.appendChild(option);
    });
    place(box, anchor);
  }

  function radioGroup(control, label, values) {
    const group = el('div', { role: 'radiogroup', 'aria-label': label, class: 'radiogroup' });
    values.forEach(function (value) {
      const radio = el('button', { role: 'radio', 'aria-checked': String(C.params[control] === value) }, [value]);
      radio.addEventListener('click', async function () {
        await setParam(control, value);
        group.querySelectorAll('[role=radio]').forEach(function (r) { r.setAttribute('aria-checked', String(r.textContent === C.params[control])); });
      });
      group.appendChild(radio);
    });
    return group;
  }

  async function openRrc() {
    const d = await FJ.act('open_control', { control: 'rrc' });
    if (d.block) return;
    closePopovers();
    const box = el('div', { role: 'dialog', 'aria-label': '比例与分辨率', class: 'popover' }, [
      el('div', {}, ['比例']), radioGroup('ratio', '比例', RATIOS),
      el('div', {}, ['分辨率']), radioGroup('resolution', '分辨率', RESOLUTIONS),
      el('div', {}, ['生成数量']), radioGroup('count', '生成数量', COUNTS),
    ]);
    place(box, C.btnRrc);
  }

  async function openDuration() {
    const d = await FJ.act('open_control', { control: 'duration' });
    if (d.block) return;
    closePopovers();
    const slider = el('input', { type: 'range', min: '0', max: '30', step: '1', value: C.params.duration, 'aria-label': '时长滑杆' });
    const number = el('input', { type: 'number', min: '4', max: '30', value: C.params.duration, 'aria-label': '时长' });
    let pending = null;
    const commit = function (raw) {
      const value = Math.max(4, Math.min(30, parseInt(raw, 10) || 4));
      clearTimeout(pending);
      pending = setTimeout(function () { setParam('duration', String(value)); }, 80);
    };
    slider.addEventListener('input', function () { number.value = slider.value; commit(slider.value); });
    number.addEventListener('input', function () { slider.value = number.value; commit(number.value); });
    const box = el('div', { role: 'dialog', 'aria-label': '时长设置', class: 'popover' }, [slider, number, el('span', {}, ['s'])]);
    place(box, C.btnDuration);
  }

  async function onUploadClick() {
    const d = await FJ.act('upload_click');
    if (d.block) return;
    FJ.pickFiles(false, function (files) { files.forEach(uploadOne); });
  }

  async function uploadOne(file) {
    const stem = file.name.replace(/\.[^.]+$/, '');
    const progress = el('div', { role: 'progressbar', 'aria-label': '上传进度', 'aria-valuenow': '30' });
    const remove = el('button', { class: 'remove', 'aria-label': '删除' }, ['×']);
    const tile = el('div', { role: 'listitem', 'aria-label': stem, class: 'ref-tile', 'data-state': 'uploading' }, [
      el('span', { class: 'thumb' }), el('span', { class: 'name' }, [stem]), progress, remove,
    ]);
    remove.addEventListener('click', function () {
      tile.remove();
      FJ.materials = FJ.materials.filter(function (m) { return m.tile !== tile; });
    });
    C.uploadList.appendChild(tile);
    const env = await FJ.uploadFile(file);
    if (env.ret !== '0') {
      tile.remove();
      FJ.toast(env.errmsg || '上传失败');
      if (env.ret === '1015') FJ.apply({ logged_in: false, credits: 0 });
      return;
    }
    progress.remove();
    tile.setAttribute('data-state', 'done');
    FJ.materials.push({ stem: stem, material_id: env.data.material_id, tile: tile });
  }

  C.onDirectives = function (d) {
    if (!C.send) return;
    if ('parallel_notice' in d) C.notice.hidden = !d.parallel_notice;
    if ('send_enabled' in d) C.send.disabled = !d.send_enabled;
    if ('negative_box' in d) C.negativeBox.hidden = !d.negative_box;
    if (d.layout_next) {
      FJ.Editor.node.removeAttribute('role');
      C.send.setAttribute('aria-label', '立即生成');
    }
  };

  C.generate = async function (via) {
    if (C.send.disabled) return;
    const snap = FJ.Editor.snapshot();
    const params = { model: C.params.model, ratio: C.params.ratio, resolution: C.params.resolution, count: parseInt(C.params.count, 10), duration: parseInt(C.params.duration, 10) };
    const payload = { via: via, text: snap.text, mentions: snap.mentions, materials: FJ.materials.map(function (m) { return m.stem; }), params: params, negative: C.negativeBox.hidden ? null : C.negative.value };
    const d = await FJ.act('generate_click', payload);
    if (d.block || d.route === 'none') return;
    payload.click_id = d.click_id;
    const path = d.route === 'alt' ? '/mweb/v1/aigc_draft/generate_alt' : '/mweb/v1/aigc_draft/generate';
    const env = await FJ.post(path, payload);
    if (env.ret !== '0') {
      FJ.toast(env.errmsg || '生成失败');
      if (env.ret === '1015') FJ.apply({ logged_in: false, credits: 0 });
      return;
    }
    FJ.History.track(env.data.aigc_data.history_record_id);
    FJ.History.refresh();
  };
})();
