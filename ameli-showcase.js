/* Two real sets, with a separate labelled visualization for each matching camera view. */
(() => {
  'use strict';
  const root = document.getElementById('before-after');
  if (!root) return;
  const tablist = root.querySelector('.showcase-tabs');
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));

  const activate = (index, moveFocus = false, loadNow = true) => {
    tabs.forEach((tab, i) => {
      const active = i === index;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      panels[i].hidden = !active;
      if (active && loadNow) panels[i].querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
    });
    if (moveFocus) tabs[index].focus();
  };
  tabs.forEach((tab, index) => {
    panels[index].setAttribute('role', 'tabpanel');
    panels[index].setAttribute('aria-labelledby', tab.id);
    tab.addEventListener('click', () => activate(index));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      activate(next, true);
    });
  });

  panels.forEach(panel => {
    const comparison = panel.querySelector('.showcase-comparison');
    const range = panel.querySelector('.showcase-range');
    const controls = [...panel.querySelectorAll('[data-reveal]')];
    const update = value => {
      const reveal = Math.max(0, Math.min(100, Number(value)));
      range.value = String(reveal);
      range.setAttribute('aria-valuetext', `${reveal}% изображения «До», ${100 - reveal}% изображения «После»`);
      comparison.style.setProperty('--reveal', `${reveal}%`);
      comparison.dataset.edge = String(reveal === 0 || reveal === 100);
      controls.forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.reveal) === reveal)));
    };
    range.addEventListener('input', () => update(range.value));
    controls.forEach(button => button.addEventListener('click', () => update(button.dataset.reveal)));
    update(range.value);
    range.hidden = false;
    panel.querySelector('.showcase-compare-footer').hidden = false;
  });

  activate(0, false, false);
  root.classList.add('showcase-ready');
  tablist.hidden = false;
})();
