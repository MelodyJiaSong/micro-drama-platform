(function () {
  const FJ = window.FJ;
  const Editor = (FJ.Editor = {});
  const PLACEHOLDER = '上传最多50个参考素材、输入文字或 @ 参考内容，自由组合图、文、音、视频多元素……例如：@图片1 模仿 @视频1 的动作，音色参考 @音频1。';
  const TRIGGER = /@([^\s@`]*)$/;
  const BLOCKS = { P: 1, DIV: 1 };

  Editor.mount = function (container) {
    const wrap = FJ.el('div', { class: 'editor-wrap' });
    const node = FJ.el('div', {
      class: 'tiptap ProseMirror', contenteditable: 'true', role: 'textbox', 'aria-multiline': 'true',
      translate: 'no', tabindex: '0', 'data-placeholder': PLACEHOLDER,
    });
    const layoutCopy = FJ.el('div', { class: 'tiptap ProseMirror', contenteditable: 'true', role: 'textbox', 'aria-hidden': 'true' });
    layoutCopy.style.display = 'none';
    wrap.append(node, layoutCopy);
    container.appendChild(wrap);
    Editor.node = node;
    if (FJ.cfg.draft) node.textContent = FJ.cfg.draft;
    refreshEmpty();
    node.addEventListener('beforeinput', onBeforeInput);
    node.addEventListener('input', function () { refreshEmpty(); checkTrigger(); });
    node.addEventListener('keydown', onKeyDown);
    return node;
  };

  Editor.snapshot = function () {
    const out = [];
    const mentions = [];
    walk(Editor.node, out, mentions);
    return { text: out.join('').replace(/​/g, ''), mentions: mentions };
  };

  function walk(parent, out, mentions) {
    const children = parent.childNodes;
    for (let i = 0; i < children.length; i++) {
      const child = children[i];
      if (child.nodeType === 3) { out.push(child.data); continue; }
      if (child.nodeType !== 1) continue;
      if (child.getAttribute('data-type') === 'mention') {
        const name = child.getAttribute('data-id');
        out.push(name);
        mentions.push(name);
        continue;
      }
      if (child.tagName === 'BR') {
        if (child.nextSibling) out.push('\n');
        continue;
      }
      if (BLOCKS[child.tagName] && out.length && out[out.length - 1].slice(-1) !== '\n') out.push('\n');
      walk(child, out, mentions);
    }
  }

  function refreshEmpty() {
    const empty = Editor.node.textContent.replace(/​/g, '').length === 0 && !Editor.node.querySelector('[data-type=mention]');
    Editor.node.classList.toggle('is-empty', empty);
  }

  function selectsEverything() {
    const sel = window.getSelection();
    const node = Editor.node;
    if (!sel.rangeCount || sel.getRangeAt(0).collapsed || !node.firstChild) return false;
    return sel.containsNode(node.firstChild, true) && sel.containsNode(node.lastChild, true);
  }

  function collapseToEnd() {
    const range = document.createRange();
    range.selectNodeContents(Editor.node);
    range.collapse(false);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function onBeforeInput(event) {
    if (event.inputType.indexOf('delete') !== 0 || !selectsEverything()) return;
    if (Editor.node.textContent.replace(/​/g, '').length === 0) return;
    if (FJ.actSync('editor_refill_swallow').swallow) {
      event.preventDefault();
      collapseToEnd();
    }
  }

  function onKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      FJ.Composer.generate('enter');
      return;
    }
    if (event.key === 'Escape' && Popup.node) {
      event.preventDefault();
      event.stopPropagation();
      Popup.close();
    }
  }

  function currentTrigger() {
    const sel = window.getSelection();
    if (!sel.rangeCount) return null;
    const range = sel.getRangeAt(0);
    const node = range.startContainer;
    if (node.nodeType !== 3 || !Editor.node.contains(node)) return null;
    const before = node.data.slice(0, range.startOffset);
    const match = before.match(TRIGGER);
    if (!match) return null;
    return { node: node, start: range.startOffset - match[0].length, end: range.startOffset, query: match[1] };
  }

  function checkTrigger() {
    const trigger = currentTrigger();
    if (trigger) Popup.show(trigger.query); else Popup.close();
  }

  const Popup = (Editor.popup = { node: null, key: '' });

  Popup.candidates = function (query) {
    const hidden = FJ.directives.hidden_candidates || [];
    const names = FJ.materials.map(function (m) { return m.stem; }).filter(function (s) { return hidden.indexOf(s) < 0; })
      .concat(FJ.entities.map(function (e) { return e.name; }));
    const q = query.toLowerCase();
    return names.filter(function (name) { return name.toLowerCase().indexOf(q) >= 0; });
  };

  Popup.show = function (query) {
    const names = Popup.candidates(query);
    const key = names.join('');
    if (Popup.node && Popup.key === key) return;
    if (!Popup.node) {
      Popup.node = FJ.el('div', { class: 'mention-popup', role: 'listbox', 'aria-label': '可能@的内容' });
      document.body.appendChild(Popup.node);
    }
    Popup.key = key;
    Popup.node.textContent = '';
    Popup.node.append(
      FJ.el('div', { class: 'title' }, ['可能@的内容']),
      FJ.el('div', { class: 'create-entity', role: 'button' }, ['+ 创建主体'])
    );
    names.forEach(function (name) {
      const option = FJ.el('div', { role: 'option', class: 'mention-option' }, [
        FJ.el('span', { class: 'thumb' }),
        FJ.el('span', { class: 'name' }, [name]),
        FJ.el('span', { class: 'more', title: '更多' }, ['…']),
      ]);
      option.addEventListener('mousedown', function (event) { event.preventDefault(); });
      option.addEventListener('click', function () { Popup.select(name); });
      Popup.node.appendChild(option);
    });
  };

  Popup.close = function () {
    if (Popup.node) Popup.node.remove();
    Popup.node = null;
    Popup.key = '';
  };

  Popup.select = function (name) {
    const trigger = currentTrigger();
    Popup.close();
    if (!trigger) return;
    const drop = FJ.actSync('mention_select', { name: name }).drop;
    const range = document.createRange();
    range.setStart(trigger.node, trigger.start);
    range.setEnd(trigger.node, trigger.end);
    range.deleteContents();
    const sel = window.getSelection();
    if (drop) {
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
      return;
    }
    const chip = FJ.el('span', { class: 'mention-chip', 'data-type': 'mention', 'data-id': name, contenteditable: 'false' }, [
      FJ.el('span', { class: 'thumb' }), name,
    ]);
    range.insertNode(chip);
    const spacer = document.createTextNode('​');
    chip.after(spacer);
    const caret = document.createRange();
    caret.setStart(spacer, 1);
    caret.collapse(true);
    sel.removeAllRanges();
    sel.addRange(caret);
    refreshEmpty();
  };
})();
