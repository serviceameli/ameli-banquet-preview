/* Approved usability refinements: gallery disclosure and live quote. */
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
      const ceremony = gallery.classList.contains('ceremony-grid');
      const visualization = gallery.classList.contains('visual-sales-grid');
      const limit = visualization ? cards.length : ceremony ? (mobileGallery.matches ? 4 : cards.length) : (mobileGallery.matches ? 2 : tabletGallery.matches ? 4 : cards.length);
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

  const calculator = document.getElementById('textile-payback');
  const get = id => document.getElementById(id);
  const discuss = get('textileDiscussTelegram');
  const syncQuote = () => {
    const valid = calculator.dataset.valid !== 'false';
    get('textileStickyInvestment').textContent = get('textileInvestmentTotal').textContent;
    get('textileStickyEvents').textContent = valid ? get('textilePayback60').textContent : 'Проверьте поля';
    discuss.setAttribute('aria-disabled', String(!valid));
    if(!valid) { discuss.removeAttribute('href'); delete discuss.dataset.contactMessage; return; }
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
    discuss.href = '#contact';
    discuss.dataset.contactMessage = lines.join('\n');
  };
  calculator.addEventListener('calculationupdate', syncQuote);
  discuss.addEventListener('click', event => { if (discuss.getAttribute('aria-disabled') === 'true') event.preventDefault(); });
  syncQuote();

})();
