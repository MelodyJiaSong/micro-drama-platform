(async function () {
  const FJ = window.FJ;
  const main = document.getElementById('main');
  await FJ.refreshDirectives();
  if (FJ.cfg.page === 'elements') {
    FJ.Entities.mount(main);
    FJ.Entities.load();
  } else {
    FJ.History.mount(main);
    FJ.Composer.mount(main);
    FJ.Composer.onDirectives(FJ.directives);
    FJ.loadEntities();
    FJ.History.refresh();
    FJ.History.startPolling();
  }
  FJ.post('/commerce/v1/benefits/user_credit', {});
  FJ.startDirectivePolling();
})();
