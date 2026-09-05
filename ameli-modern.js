/* Presentation enhancements. Source calculator and combination logic stay intact. */
(() => {
  const grid = document.querySelector('#combinationGrid');
  const expand = document.querySelector('.combination-expand');
  const limit = () => window.matchMedia('(max-width:600px)').matches ? 8 : 9;
  const updateGallery = () => {
    const total = grid.children.length;
    const expanded = expand.getAttribute('aria-expanded') === 'true';
    expand.hidden = total <= limit();
    grid.classList.toggle('is-collapsed', !expanded && total > limit());
    expand.textContent = expanded ? 'Свернуть сочетания' : `Показать все ${total} сочетаний`;
  };
  if (grid && expand) {
    expand.addEventListener('click', () => {
      const opening = expand.getAttribute('aria-expanded') !== 'true';
      expand.setAttribute('aria-expanded', String(opening));
      updateGallery();
      if (!opening) document.querySelector('.combination-gallery').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth',block:'start'});
    });
    new MutationObserver(() => { expand.setAttribute('aria-expanded','false'); updateGallery(); }).observe(grid,{childList:true});
    window.matchMedia('(max-width:600px)').addEventListener('change', updateGallery);
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
