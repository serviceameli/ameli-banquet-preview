/* Every sales CTA shares this dialog. Opening a channel only creates a draft. */
(() => {
  'use strict';
  const dialog = document.getElementById('contactDialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;

  const title = document.getElementById('contactDialogTitle');
  const quote = document.getElementById('contactQuote');
  const status = quote.querySelector('.contact-copy-status');
  const fallback = quote.querySelector('textarea');
  const links = [...dialog.querySelectorAll('[data-contact-channel]')];
  const baseLinks = new Map(links.map(link => [link, link.getAttribute('href')]));
  let opener = null;
  let message = '';
  let scrollPosition = 0;
  let previousBodyStyle = null;
  let pointerStartedOutside = false;

  const lockPage = () => {
    scrollPosition = window.scrollY;
    previousBodyStyle = document.body.getAttribute('style');
    const scrollbar = window.innerWidth - document.documentElement.clientWidth;
    const padding = parseFloat(getComputedStyle(document.body).paddingRight) || 0;
    Object.assign(document.body.style, {
      position: 'fixed', top: `-${scrollPosition}px`, left: '0', right: '0',
      paddingRight: `${padding + scrollbar}px`
    });
  };
  const unlockPage = () => {
    if (previousBodyStyle === null) document.body.removeAttribute('style');
    else document.body.setAttribute('style', previousBodyStyle);
    window.scrollTo({top: scrollPosition, behavior: 'instant'});
  };

  document.querySelectorAll('[data-contact-open]').forEach(trigger => {
    trigger.setAttribute('aria-haspopup', 'dialog');
    trigger.setAttribute('aria-controls', dialog.id);
    trigger.addEventListener('click', event => {
      if (trigger.getAttribute('aria-disabled') === 'true') { event.preventDefault(); return; }
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      if (dialog.open) return;
      opener = trigger;
      message = trigger.dataset.contactMessage || '';
      quote.hidden = !message;
      status.textContent = '';
      fallback.hidden = true;
      fallback.value = '';
      links.forEach(link => {
        const base = baseLinks.get(link);
        const channel = link.dataset.contactChannel;
        if (message && (channel === 'telegram' || channel === 'whatsapp')) {
          const url = new URL(base);
          url.searchParams.set('text', message);
          link.href = url.href;
        } else if (message && channel === 'email') {
          link.href = `${base}?subject=${encodeURIComponent('Расчёт комплекта текстиля для площадки')}&body=${encodeURIComponent(message)}`;
        } else link.href = base;
      });
      lockPage();
      dialog.showModal();
      dialog.scrollTop = 0;
      title.focus({preventScroll:true});
    });
  });

  dialog.querySelector('.contact-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const focusable = [...dialog.querySelectorAll('a[href], button:not(:disabled), textarea')]
      .filter(element => element.getClientRects().length > 0);
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && (document.activeElement === first || document.activeElement === title)) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  });
  const outside = event => {
    const rect = dialog.getBoundingClientRect();
    return event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom);
  };
  dialog.addEventListener('pointerdown', event => { pointerStartedOutside = outside(event); });
  dialog.addEventListener('click', event => {
    if (pointerStartedOutside && outside(event)) dialog.close();
    pointerStartedOutside = false;
  });
  dialog.addEventListener('close', () => {
    unlockPage();
    const target = opener?.getClientRects().length ? opener : document.querySelector('.menu-toggle');
    target?.focus({preventScroll:true});
    message = '';
  });

  quote.querySelector('.contact-copy').addEventListener('click', async () => {
    if (!message) return;
    const text = message;
    try {
      await navigator.clipboard.writeText(text);
      if (dialog.open && message === text) status.textContent = 'Расчёт скопирован. Его можно вставить в сообщение.';
    } catch {
      if (!dialog.open || message !== text) return;
      fallback.value = text;
      fallback.hidden = false;
      fallback.focus();
      fallback.select();
      status.textContent = 'Выделили текст — скопируйте его и вставьте в сообщение.';
    }
  });
})();
