/* Approved usability refinements: gallery disclosure, image viewer and live quote. */
(() => {
  'use strict';
  const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gallerySelectors = '.example-gallery, .textile-grid, .tableware-showcase, .ceremony-grid, .visual-sales-grid';
  const mobileGallery = matchMedia('(max-width:600px)');
  const tabletGallery = matchMedia('(max-width:900px)');

  document.querySelectorAll(gallerySelectors).forEach((gallery, index) => {
    const cards = [...gallery.children];
    if (cards.length < 3) return;
    gallery.id ||= `productGallery${index}`;
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'gallery-more';
    button.setAttribute('aria-controls', gallery.id);
    button.setAttribute('aria-expanded', 'false');
    gallery.after(button);
    let expanded = false;
    const render = () => {
      const limit = mobileGallery.matches ? 2 : tabletGallery.matches ? 4 : cards.length;
      cards.forEach((card, i) => { card.hidden = !expanded && i >= limit; });
      button.hidden = cards.length <= limit;
      button.setAttribute('aria-expanded', String(expanded));
      button.textContent = expanded ? 'Свернуть подборку' : `Показать ещё ${cards.length - limit}`;
    };
    button.addEventListener('click', () => {
      expanded = !expanded; render();
      if (!expanded) gallery.scrollIntoView({behavior:reducedMotion()?'instant':'smooth',block:'start'});
    });
    mobileGallery.addEventListener('change', render);
    tabletGallery.addEventListener('change', render);
    render();
  });

  const photoSelector = '.example-media img, .offer-gallery img, .visual-sales-item img, .chair-change-media img, .model-image img, .ceremony-example > img, .comparison-frame > img, .tableware-example.setting > img, .dishware-duo img';
  const photos = [...document.querySelectorAll(photoSelector)];
  const dialog = document.createElement('dialog');
  dialog.className = 'photo-dialog';
  dialog.setAttribute('aria-labelledby', 'photoViewerCaption');
  dialog.innerHTML = `<div class="photo-dialog-panel">
    <div class="photo-dialog-toolbar"><span id="photoViewerCount"></span><button type="button" class="photo-close" aria-label="Закрыть фотографию"><span class="material-symbols-outlined" aria-hidden="true">close</span></button></div>
    <div class="photo-dialog-stage"><button class="photo-prev" type="button" aria-label="Предыдущая фотография"><span class="material-symbols-outlined" aria-hidden="true">chevron_left</span></button><img class="photo-full" alt=""><button class="photo-next" type="button" aria-label="Следующая фотография"><span class="material-symbols-outlined" aria-hidden="true">chevron_right</span></button></div>
    <p id="photoViewerCaption" aria-live="polite"></p></div>`;
  document.body.append(dialog);
  let group = [], current = 0, opener;
  const fullImage = dialog.querySelector('.photo-full');
  const renderPhoto = () => {
    const image = group[current];
    fullImage.src = image.currentSrc || image.src;
    fullImage.alt = image.alt;
    dialog.querySelector('#photoViewerCaption').textContent = image.alt;
    dialog.querySelector('#photoViewerCount').textContent = `${current + 1} / ${group.length}`;
    dialog.querySelector('.photo-prev').hidden = group.length < 2;
    dialog.querySelector('.photo-next').hidden = group.length < 2;
  };
  const move = direction => { current = (current + direction + group.length) % group.length; renderPhoto(); };
  photos.forEach(image => {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'image-zoom';
    button.setAttribute('aria-label', `Увеличить: ${image.alt}`);
    image.before(button); button.append(image);
    const hint = document.createElement('span');
    hint.className = 'zoom-hint material-symbols-outlined'; hint.setAttribute('aria-hidden','true'); hint.textContent = 'zoom_in';
    button.append(hint);
    button.addEventListener('click', () => {
      const gallery = image.closest(`${gallerySelectors}, .offer-gallery, .honest-comparison`);
      group = gallery ? photos.filter(photo => gallery.contains(photo)) : [image];
      current = group.indexOf(image); opener = button; renderPhoto();
      dialog.showModal(); document.body.classList.add('photo-viewer-open');
      dialog.querySelector('.photo-close').focus();
    });
  });
  dialog.querySelector('.photo-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.photo-prev').addEventListener('click', () => move(-1));
  dialog.querySelector('.photo-next').addEventListener('click', () => move(1));
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('keydown', event => {
    if(event.key === 'ArrowLeft') { event.preventDefault(); move(-1); }
    if(event.key === 'ArrowRight') { event.preventDefault(); move(1); }
  });
  dialog.addEventListener('close', () => { document.body.classList.remove('photo-viewer-open'); opener?.focus({preventScroll:true}); });

  const calculator = document.getElementById('textile-payback');
  const get = id => document.getElementById(id);
  const discuss = get('textileDiscussTelegram');
  const syncQuote = () => {
    const valid = calculator.dataset.valid !== 'false';
    get('textileStickyInvestment').textContent = get('textileInvestmentTotal').textContent;
    get('textileStickyEvents').textContent = valid ? get('textilePayback60').textContent : 'Проверьте поля';
    discuss.setAttribute('aria-disabled', String(!valid));
    if(!valid) { discuss.removeAttribute('href'); return; }
    const lines = [
      'Здравствуйте! Хочу обсудить комплект текстиля для площадки.',
      `В одном цвете: круглые скатерти — ${get('textileRoundQty').value} шт., прямоугольные — ${get('textileRectQty').value} шт., салфетки — ${get('textileNapkinQty').value} шт.`,
      `Количество цветов: ${get('textileColors').value}.`,
      `Инвестиция по калькулятору: ${get('textileInvestmentTotal').textContent}.`,
      `Ставки аренды: круглая скатерть — ${get('textileRentRound').value} ₽, прямоугольная — ${get('textileRentRect').value} ₽, салфетка — ${get('textileRentNapkin').value} ₽.`,
      `Окупаемость для 60 гостей по арендной выручке, без учёта расходов: ${get('textilePayback60').textContent}.`,
      get('textileMainStatus').textContent,
      'Хочу уточнить комплектацию и стоимость для моего зала.'
    ];
    discuss.href = `https://t.me/amelirental?text=${encodeURIComponent(lines.join('\n'))}`;
  };
  calculator.addEventListener('calculationupdate', syncQuote);
  discuss.addEventListener('click', event => { if (discuss.getAttribute('aria-disabled') === 'true') event.preventDefault(); });
  syncQuote();

  const jumpLinks = [...document.querySelectorAll('.jump-links a')];
  const sectionObserver = new IntersectionObserver(entries => {
    entries.filter(entry => entry.isIntersecting).forEach(entry => {
      jumpLinks.forEach(link => {
        const active = link.hash === `#${entry.target.id}`;
        if(active) link.setAttribute('aria-current','location'); else link.removeAttribute('aria-current');
      });
    });
  }, {rootMargin:'-25% 0px -60% 0px'});
  document.querySelectorAll('main > section[id]').forEach(section => sectionObserver.observe(section));
})();
