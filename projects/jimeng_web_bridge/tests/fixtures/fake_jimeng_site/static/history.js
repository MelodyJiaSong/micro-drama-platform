(function () {
  const FJ = window.FJ;
  const el = FJ.el;
  const H = (FJ.History = { tracked: {}, nodes: {} });
  const STATUS = { 10: 'queued', 20: 'generating', 30: 'failed', 50: 'succeeded' };

  H.mount = function (main) {
    H.list = el('div', { role: 'list', 'aria-label': '生成记录', class: 'history' });
    H.badge = el('div', { class: 'float-badge' });
    H.badge.hidden = true;
    main.append(H.list, H.badge);
  };

  H.track = function (id) { H.tracked[id] = true; };

  H.refresh = async function () {
    const env = await FJ.post('/mweb/v1/get_history', { count: 20 });
    if (env.ret !== '0' || !env.data) return;
    env.data.records_list.forEach(upsert);
  };

  H.startPolling = function () {
    const loop = async function () {
      try {
        const ids = Object.keys(H.tracked);
        const queue = await FJ.post('/mweb/v1/get_history_queue_info', { history_ids: ids });
        const byIds = await FJ.post('/mweb/v1/get_history_by_ids', { history_ids: ids });
        if (queue.ret === '0' && queue.data) {
          const running = queue.data.running_count;
          H.badge.hidden = running === 0;
          H.badge.textContent = running + '/' + queue.data.running_limit + ' 生成中… 回到底部';
        }
        if (byIds.ret === '0' && byIds.data) Object.keys(byIds.data).forEach(function (id) { upsert(byIds.data[id]); });
      } catch (e) { /* teardown */ }
      setTimeout(loop, FJ.cfg.poll_ms);
    };
    setTimeout(loop, FJ.cfg.poll_ms);
  };

  function upsert(rec) {
    const status = STATUS[rec.status] || 'queued';
    if (status === 'succeeded' || status === 'failed') delete H.tracked[rec.history_record_id];
    else H.tracked[rec.history_record_id] = true;
    let entry = H.nodes[rec.history_record_id];
    if (!entry) {
      entry = { key: '', node: build(rec) };
      H.nodes[rec.history_record_id] = entry;
      H.list.appendChild(entry.node);
    }
    const key = status + ':' + rec.progress;
    if (entry.key === key) return;
    const statusChanged = entry.key.split(':')[0] !== status;
    entry.key = key;
    if (statusChanged) renderMedia(entry.node, rec, status);
    const overlay = entry.node.querySelector('.progress-overlay');
    if (overlay) overlay.textContent = rec.progress + '%造梦中';
    entry.node.dataset.credits = rec.credits === null || rec.credits === undefined ? '' : String(rec.credits);
    H.list.scrollTop = H.list.scrollHeight;
  }

  function build(rec) {
    const details = el('span', { class: 'details', tabindex: '0' }, ['详细信息ⓘ']);
    const node = el('div', { role: 'listitem', class: 'record', 'data-history-id': rec.history_record_id }, [
      el('div', { class: 'ref-strip' }, (rec.material_list || []).map(function () { return el('span', { class: 'thumb' }); })),
      el('div', { class: 'prompt' }, [rec.prompt || '']),
      el('div', { class: 'meta' }, [
        [rec.model_name || '', (rec.duration_s || 0) + 's', rec.ratio || '', rec.resolution || ''].join(' | ') + ' | ',
        details,
      ]),
      el('div', { class: 'media' }),
      el('div', { class: 'record-actions' }),
    ]);
    details.addEventListener('mouseenter', function () {
      const credits = node.dataset.credits;
      const tip = el('div', { role: 'tooltip', class: 'tooltip' }, [
        '生成时间 2026-09-13 · 消耗积分数 ' + (credits ? credits : '计算中'),
      ]);
      node.appendChild(tip);
    });
    details.addEventListener('mouseleave', function () {
      const tip = node.querySelector('[role=tooltip]');
      if (tip) tip.remove();
    });
    return node;
  }

  function renderMedia(node, rec, status) {
    const media = node.querySelector('.media');
    const actions = node.querySelector('.record-actions');
    media.textContent = '';
    actions.textContent = '';
    if (status === 'queued' || status === 'generating') {
      media.append(el('div', { class: 'progress-overlay' }, [rec.progress + '%造梦中']));
      actions.append(el('div', { class: 'vip-tip' }, ['超级会员 成功进入生成阶段，为您节省约 1 小时排队时间']));
      return;
    }
    if (status === 'failed') {
      media.append(el('div', { class: 'fail' }, ['生成失败：' + (rec.fail_msg || '未知原因')]));
      return;
    }
    const download = el('span', { class: 'action-button action-button-download', role: 'button', title: '下载' });
    const more = el('span', { class: 'action-button action-button-more', role: 'button', title: '更多' });
    const fav = el('span', { class: 'action-button action-button-fav', role: 'button', title: '收藏' });
    download.addEventListener('click', async function () {
      const d = await FJ.act('download_click', { id: rec.history_record_id });
      if (d.block) return;
      const link = el('a', { href: '/download/' + rec.history_record_id + '.mp4', download: '' });
      document.body.appendChild(link);
      link.click();
      link.remove();
    });
    media.append(el('video', { preload: 'none', muted: true }), el('div', { class: 'card-actions' }, [download, more, fav]));
    const regenerate = el('button', {}, ['再次生成']);
    regenerate.addEventListener('click', function () { FJ.Composer.generate('regenerate'); });
    actions.append(el('button', {}, ['重新编辑']), regenerate, el('button', { 'aria-label': '更多操作' }, ['⋯']));
  }
})();
