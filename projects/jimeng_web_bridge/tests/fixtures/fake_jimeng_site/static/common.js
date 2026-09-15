(function () {
  const cfg = window.__FAKE__;
  const FJ = (window.FJ = { cfg: cfg, materials: [], entities: [], directives: {} });

  FJ.q = function (path) {
    const sep = path.indexOf('?') >= 0 ? '&' : '?';
    return path + sep + 'aid=513695&web_version=' + encodeURIComponent(cfg.web_version) + '&da_version=3.3.27-fake';
  };

  FJ.post = async function (path, body) {
    const res = await fetch(FJ.q(path), {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body || {}),
    });
    const text = await res.text();
    try { return JSON.parse(text); } catch (e) { return { ret: 'malformed', errmsg: 'malformed', data: null }; }
  };

  FJ.act = async function (kind, detail) {
    const res = await fetch('/__page__/act', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ kind: kind, detail: detail || {} }),
    });
    const d = await res.json();
    FJ.apply(d);
    return d;
  };

  FJ.actSync = function (kind, detail) {
    const x = new XMLHttpRequest();
    x.open('POST', '/__page__/act', false);
    x.setRequestHeader('content-type', 'application/json');
    x.send(JSON.stringify({ kind: kind, detail: detail || {} }));
    return JSON.parse(x.responseText);
  };

  FJ.el = function (tag, attrs, children) {
    const node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) {
      const value = attrs[key];
      if (value === null || value === undefined || value === false) return;
      if (key === 'class') node.className = value;
      else if (key === 'text') node.textContent = value;
      else node.setAttribute(key, value === true ? '' : String(value));
    });
    (children || []).forEach(function (child) {
      if (child === null || child === undefined) return;
      node.appendChild(typeof child === 'string' ? document.createTextNode(child) : child);
    });
    return node;
  };

  FJ.toast = function (text, ms) {
    const node = FJ.el('div', { role: 'alert', class: 'toast' }, [text]);
    document.getElementById('toasts').appendChild(node);
    setTimeout(function () { node.remove(); }, ms || 6000);
  };

  FJ.formatCredits = function (n) {
    return n >= 10000 ? (Math.round(n / 1000) / 10) + '万' : String(n);
  };

  let headerKey = '';
  FJ.renderHeader = function (loggedIn, credits) {
    const key = loggedIn + ':' + credits;
    if (key === headerKey) return;
    headerKey = key;
    const header = document.getElementById('header');
    header.textContent = '';
    if (loggedIn) {
      header.append(
        FJ.el('span', { class: 'vip' }, ['超级会员']),
        FJ.el('span', { class: 'credits-total' }, [FJ.formatCredits(credits)]),
        FJ.el('img', { role: 'img', alt: '用户头像', class: 'avatar', src: 'data:image/gif;base64,R0lGODlhAQABAAAAACw=' })
      );
      const dialog = document.getElementById('login-dialog');
      if (dialog) dialog.remove();
    } else {
      header.append(FJ.el('button', { class: 'login-btn' }, ['登录']));
      FJ.showLogin();
    }
  };

  FJ.showLogin = function () {
    if (document.getElementById('login-dialog')) return;
    const inputs = ['手机号', '密码', '验证码'].map(function (label) {
      const input = FJ.el('input', { 'aria-label': label });
      input.addEventListener('input', function () { FJ.act('login_input'); });
      return input;
    });
    const panel = FJ.el('div', { class: 'dialog', role: 'dialog', 'aria-label': '登录' }, [
      FJ.el('div', {}, ['扫码登录']),
      FJ.el('div', { class: 'qr' }, ['[二维码]']),
    ].concat(inputs));
    document.getElementById('overlays').appendChild(FJ.el('div', { id: 'login-dialog', class: 'dialog-backdrop' }, [panel]));
  };

  FJ.showCaptcha = function () {
    if (document.getElementById('captcha')) return;
    const panel = FJ.el('div', { class: 'panel', role: 'dialog', 'aria-modal': 'true', 'aria-label': '安全验证' }, [
      FJ.el('div', {}, ['安全验证']),
      FJ.el('div', {}, ['请拖动滑块完成拼图']),
      FJ.el('div', { class: 'slider', role: 'slider', 'aria-label': '滑块', 'aria-valuenow': '0' }),
    ]);
    document.getElementById('overlays').appendChild(FJ.el('div', { id: 'captcha', class: 'blocker' }, [panel]));
  };

  FJ.showRisk = function () {
    if (document.getElementById('risk')) return;
    const panel = FJ.el('div', { class: 'panel', role: 'dialog', 'aria-modal': 'true', 'aria-label': '风险提示' }, [
      FJ.el('div', {}, ['检测到异常行为，请稍后再试']),
    ]);
    document.getElementById('overlays').appendChild(FJ.el('div', { id: 'risk', class: 'blocker' }, [panel]));
  };

  FJ.apply = function (d) {
    if (!d) return;
    Object.keys(d).forEach(function (key) { FJ.directives[key] = d[key]; });
    if (d.captcha) FJ.showCaptcha();
    if (d.captcha === false) {
      const node = document.getElementById('captcha');
      if (node) node.remove();
    }
    if (d.risk) FJ.showRisk();
    if (d.toast) FJ.toast(d.toast);
    if ('logged_in' in d) FJ.renderHeader(d.logged_in, d.credits || 0);
    if (d.reload) { location.reload(); return; }
    if (FJ.Composer && FJ.Composer.onDirectives) FJ.Composer.onDirectives(d);
  };

  FJ.refreshDirectives = async function () {
    try {
      const res = await fetch('/__page__/directives');
      FJ.apply(await res.json());
    } catch (e) { /* server gone during teardown */ }
  };

  FJ.startDirectivePolling = function () {
    const loop = async function () {
      await FJ.refreshDirectives();
      setTimeout(loop, cfg.poll_ms);
    };
    setTimeout(loop, cfg.poll_ms);
  };

  FJ.loadEntities = async function () {
    const env = await FJ.post('/mweb/v1/dreamina_subject/get', { page: 1 });
    if (env.ret === '1015') { FJ.apply({ logged_in: false, credits: 0 }); return []; }
    FJ.entities = env.ret === '0' && env.data ? env.data.subject_list : [];
    return FJ.entities;
  };

  FJ.pickFiles = function (multiple, onFiles) {
    const input = FJ.el('input', { type: 'file', accept: 'image/*,video/*,audio/*', multiple: multiple });
    input.style.display = 'none';
    document.body.appendChild(input);
    input.addEventListener('change', function () {
      const files = Array.prototype.slice.call(input.files);
      input.remove();
      onFiles(files);
    });
    input.click();
  };

  FJ.uploadFile = async function (file) {
    const res = await fetch(FJ.q('/mweb/v1/upload_material'), {
      method: 'POST',
      headers: { 'x-file-name': encodeURIComponent(file.name), 'content-type': 'application/octet-stream' },
      body: await file.arrayBuffer(),
    });
    try { return await res.json(); } catch (e) { return { ret: 'malformed', errmsg: '上传失败' }; }
  };
})();
