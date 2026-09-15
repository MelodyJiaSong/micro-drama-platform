(function () {
  const FJ = window.FJ;
  const el = FJ.el;
  const E = (FJ.Entities = {});

  E.mount = function (main) {
    const filters = el('div', { class: 'toolbar' }, [el('button', {}, ['筛选']), el('button', {}, ['时间']), el('button', {}, ['排序'])]);
    E.grid = el('div', { role: 'list', 'aria-label': '主体列表', class: 'entity-grid' });
    main.append(filters, E.grid);
  };

  E.load = async function () {
    const subjects = await FJ.loadEntities();
    E.grid.textContent = '';
    const create = el('button', { class: 'new-entity' }, ['新建主体']);
    create.addEventListener('click', openForm);
    E.grid.appendChild(el('div', { role: 'listitem', class: 'entity-card' }, [create]));
    subjects.forEach(function (subject) {
      E.grid.appendChild(el('div', { role: 'listitem', class: 'entity-card' }, [
        el('span', { class: 'thumb' }),
        el('div', { class: 'name' }, [subject.name]),
        el('div', { class: 'time' }, ['1小时前修改']),
      ]));
    });
  };

  function openForm() {
    const images = el('div', { class: 'imgs' });
    const materialIds = [];
    const addImage = el('button', { 'aria-label': '添加参考主体图片' }, ['+ 添加']);
    addImage.addEventListener('click', function () {
      FJ.pickFiles(true, function (files) {
        files.forEach(async function (file) {
          const thumb = el('span', { class: 'thumb', 'data-state': 'uploading', 'aria-label': file.name });
          images.appendChild(thumb);
          const env = await FJ.uploadFile(file);
          if (env.ret !== '0') { thumb.remove(); FJ.toast(env.errmsg || '上传失败'); return; }
          thumb.setAttribute('data-state', 'done');
          materialIds.push(env.data.material_id);
        });
      });
    });
    const name = el('input', { 'aria-label': '名称', maxlength: '20' });
    const counter = el('span', { class: 'counter' }, ['0/20']);
    name.addEventListener('input', function () { counter.textContent = Array.from(name.value).length + '/20'; });
    const description = el('textarea', { 'aria-label': '描述' });
    const cancel = el('button', {}, ['取消']);
    const save = el('button', { class: 'primary' }, ['保存']);
    const dialog = el('div', { class: 'dialog', role: 'dialog', 'aria-label': '设置主体' }, [
      el('div', { class: 'field' }, [el('div', {}, ['参考主体*']), images, addImage]),
      el('button', { class: 'add-role' }, ['添加角色']),
      el('label', { class: 'field' }, ['名称*', name]), counter,
      el('label', { class: 'field' }, ['描述', description]),
      el('div', { class: 'actions' }, [cancel, save]),
    ]);
    const backdrop = el('div', { class: 'dialog-backdrop' }, [dialog]);
    cancel.addEventListener('click', function () { backdrop.remove(); });
    save.addEventListener('click', async function () {
      if (!name.value || materialIds.length === 0 || images.querySelector('[data-state=uploading]')) {
        FJ.toast('请填写名称并上传参考主体');
        return;
      }
      const env = await FJ.post('/mweb/v1/dreamina_subject/create', { name: name.value, description: description.value, material_ids: materialIds });
      if (env.ret !== '0') { FJ.toast(env.errmsg || '保存失败'); return; }
      backdrop.remove();
      E.load();
    });
    document.getElementById('overlays').appendChild(backdrop);
  }
})();
