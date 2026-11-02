(() => {
  const layout = document.querySelector('.resume-layout');
  const reader = document.querySelector('#reader-content');
  const close = document.querySelector('#close-story');
  const status = document.querySelector('.reader-status');
  const entries = [...document.querySelectorAll('.resume-story')];
  const desktop = matchMedia('(min-width: 1000px)');
  const initial = reader.innerHTML;
  let selected = null;
  layout.classList.add('enhanced');
  function select(entry, updateURL = true) {
    entries.forEach(item => {
      item.open = item === entry;
      item.classList.toggle('selected', item === entry);
    });
    selected = entry;
    reader.replaceChildren(entry.querySelector('.resume-inline').cloneNode(true));
    close.hidden = false;
    document.querySelector('.story-reader').scrollTop = 0;
    status.textContent = 'Story selected: ' + entry.querySelector('summary > span').textContent;
    if (updateURL) history.replaceState(null, '', '#' + entry.id);
  }
  entries.forEach(entry => {
    entry.querySelector('summary').addEventListener('click', event => {
      if (desktop.matches) {
        event.preventDefault();
        select(entry);
      }
    });
  });
  reader.addEventListener('click', event => {
    const button = event.target.closest('[data-story]');
    if (!button) return;
    const entry = document.getElementById(button.dataset.story);
    if (entry) select(entry);
  });
  close.addEventListener('click', () => {
    const previous = selected;
    entries.forEach(entry => { entry.open = false; entry.classList.remove('selected'); });
    selected = null;
    reader.innerHTML = initial;
    close.hidden = true;
    history.replaceState(null, '', location.pathname);
    status.textContent = 'Story closed.';
    previous?.querySelector('summary').focus({preventScroll:true});
  });
  function openHash() {
    const entry = entries.find(item => item.id === location.hash.slice(1));
    if (entry) {
      select(entry, false);
      if (!desktop.matches) entry.scrollIntoView({block:'start'});
    }
  }
  window.addEventListener('hashchange', openHash);
  openHash();
})();
