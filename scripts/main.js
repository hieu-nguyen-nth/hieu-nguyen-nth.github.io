(() => {
  const human = document.querySelector('#human-view');
  const machine = document.querySelector('#machine-view');
  const humanButton = document.querySelector('#human-button');
  const machineButton = document.querySelector('#machine-button');
  const toggle = document.querySelector('.view-toggle');
  const openLinkedStory = () => {
    const target = document.getElementById(location.hash.slice(1));
    if (target && target.tagName === 'DETAILS') {
      target.open = true;
      let parent = target.parentElement;
      while (parent) {
        if (parent.tagName === 'DETAILS') parent.open = true;
        parent = parent.parentElement;
      }
      requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
    }
  };
  const applyView = () => {
    const isMachine = location.hash === '#machine';
    human.hidden = isMachine;
    machine.hidden = !isMachine;
    humanButton.setAttribute('aria-pressed', String(!isMachine));
    machineButton.setAttribute('aria-pressed', String(isMachine));
    if (isMachine) window.scrollTo(0, 0);
    else openLinkedStory();
  };
  toggle.hidden = false;
  humanButton.addEventListener('click', () => { if (location.hash === '#machine') location.hash = '#top'; });
  machineButton.addEventListener('click', () => { location.hash = '#machine'; });
  window.addEventListener('hashchange', applyView);
  applyView();
  document.querySelector('#copy-profile').addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    try {
      await navigator.clipboard.writeText(document.querySelector('#profile-text').textContent);
      status.textContent = 'Profile copied.';
    } catch {
      status.textContent = 'Select the profile text below to copy it, or download the Markdown file.';
      document.querySelector('#profile-text').focus();
    }
  });
})();
