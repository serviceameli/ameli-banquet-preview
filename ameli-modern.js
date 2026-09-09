/* Presentation enhancements. Source calculator and combination logic stay intact. */
(() => {
  const grid = document.querySelector('#combinationGrid');
  const expand = document.querySelector('.combination-expand');
  const scrollHint = document.querySelector('.combination-scroll-hint');
  const desktopGallery = window.matchMedia('(min-width:901px)');
  const smallGallery = window.matchMedia('(max-width:600px)');
  const limit = () => smallGallery.matches ? 8 : 9;
  const reducedMotion = () => window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  const updateScrollHint = () => {
    const scrollable = desktopGallery.matches && grid.scrollHeight > grid.clientHeight + 1;
    if (scrollable) grid.setAttribute('tabindex', '0');
    else grid.removeAttribute('tabindex');
    if (!scrollHint) return;
    scrollHint.hidden = !scrollable;
    const atEnd = grid.scrollTop + grid.clientHeight >= grid.scrollHeight - 2;
    scrollHint.textContent = atEnd ? 'В начало ↑' : 'Листать сочетания ↓';
    scrollHint.setAttribute('aria-label', atEnd ? 'В начало сочетаний' : 'Листать сочетания вниз');
  };
  const updateGallery = () => {
    const total = grid.children.length;
    const expanded = expand.getAttribute('aria-expanded') === 'true';
    expand.hidden = desktopGallery.matches || total <= limit();
    grid.classList.toggle('is-collapsed', !desktopGallery.matches && !expanded && total > limit());
    expand.textContent = expanded ? 'Свернуть сочетания' : 'Показать все сочетания';
    updateScrollHint();
  };
  if (grid && expand) {
    expand.addEventListener('click', () => {
      const opening = expand.getAttribute('aria-expanded') !== 'true';
      expand.setAttribute('aria-expanded', String(opening));
      updateGallery();
      if (!opening) document.querySelector('.combination-gallery').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth',block:'start'});
    });
    new MutationObserver(() => {
      expand.setAttribute('aria-expanded','false');
      grid.scrollTop = 0;
      updateGallery();
    }).observe(grid,{childList:true});
    scrollHint?.addEventListener('click', () => {
      const atEnd = grid.scrollTop + grid.clientHeight >= grid.scrollHeight - 2;
      grid.scrollTo({top:atEnd ? 0 : grid.scrollTop + grid.clientHeight * .85,
        behavior:reducedMotion() ? 'instant' : 'smooth'});
    });
    grid.addEventListener('scroll', updateScrollHint, {passive:true});
    new ResizeObserver(updateScrollHint).observe(grid);
    smallGallery.addEventListener('change', updateGallery);
    desktopGallery.addEventListener('change', () => { grid.scrollTop = 0; updateGallery(); });
    updateGallery();
  }
  const topLink = document.createElement('a');
  topLink.className = 'back-top';
  topLink.href = '#hero';
  topLink.setAttribute('aria-label','Вернуться к началу страницы');
  topLink.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">arrow_upward</span>';
  topLink.hidden = true;
  document.body.append(topLink);
  const showTop = () => { topLink.hidden = window.scrollY < 1000; };
  window.addEventListener('scroll',showTop,{passive:true});
  showTop();
  const navLinks = [...document.querySelectorAll('.nav-links a:not(.button)')];
  const observer = new IntersectionObserver(entries => {
    for(const entry of entries) {
      if(!entry.isIntersecting) continue;
      navLinks.forEach(link => {
        if(link.hash === '#' + entry.target.id) link.setAttribute('aria-current','location');
        else link.removeAttribute('aria-current');
      });
    }
  }, {rootMargin:'-15% 0px -65% 0px'});
  document.querySelectorAll('main>section[id]').forEach(section=>observer.observe(section));
})();
