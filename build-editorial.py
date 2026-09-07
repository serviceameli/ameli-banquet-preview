from pathlib import Path
import re

root = Path(__file__).resolve().parent
source = (root / 'responsive-redesign.html').read_text()
html = re.sub(r'<style>.*?</style>', '', source, flags=re.S)
html = re.sub(r'  <link rel="stylesheet" href="(?:concept-one|spatial-redesign-responsive)\.css">\n', '', html)
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-modern.css">\n  <link rel="icon" href="premium-assets/ameli-rental-logo.png">\n</head>')
html = html.replace('<meta name="theme-color" content="#1a1a1a">', '<meta name="theme-color" content="#ffffff">')
html = html.replace('content="cover-photo.png"', 'content="https://serviceameli.github.io/ameli-banquet-preview/s2-banquet-hall.jpeg"')
html = html.replace('<strong>AMELI</strong><span>решения для площадок</span>', '<img src="premium-assets/ameli-rental-logo.png" alt="" width="44" height="44"><span class="brand-name"><strong>AMELI</strong><span>решения для площадок</span></span>')
html = html.replace('<a href="#order">Как мы работаем</a>', '<a href="#textile-payback">Окупаемость</a>\n        <a href="#order">Как мы работаем</a>')
html = html.replace('<p class="lead">Помогаем площадкам<br>выглядеть дороже, продавать<br>мероприятия выгоднее<br>и зарабатывать на оформлении.</p>', '<p class="lead">Помогаем площадкам выглядеть дороже, продавать мероприятия выгоднее и зарабатывать на оформлении.</p>')
# Preserve the source content and its calculators. Only replace presentation.
html = html.replace('example-gallery chair-gallery', 'example-gallery classic-gallery')
html = html.replace('<div class="example-gallery">', '<div class="example-gallery tables-gallery">', 1)
html = html.replace('<div class="example-gallery">', '<div class="example-gallery poufs-gallery">', 1)
for field, name in [('textileRoundQty', 'Количество круглых скатертей'), ('textileRectQty', 'Количество прямоугольных скатертей'), ('textileNapkinQty', 'Количество салфеток')]:
    html = html.replace(f'<input id="{field}"', f'<input aria-label="{name}" id="{field}"')
html = html.replace('<div class="combination-grid" id="combinationGrid"', '<div class="combination-grid" id="combinationGrid"')
html = html.replace('<p class="combination-gallery-note">', '<button class="combination-expand" type="button" aria-expanded="false" aria-controls="combinationGrid" hidden>Показать все сочетания</button>\n            <p class="combination-gallery-note">')
html = html.replace('<script>\n    (() => {\n      if (window.matchMedia', '<script>\n    (() => {\n      if (window.matchMedia')
html = html.replace('</body>', '  <script src="ameli-modern.js"></script>\n</body>')
# The menu remains usable without an icon font.
html = html.replace('<span class="material-symbols-outlined" aria-hidden="true">menu</span>', '<span class="menu-label">Меню</span><span class="menu-lines" aria-hidden="true"></span>')
html = html.replace('if (window.innerWidth > 900) close();', 'if (window.innerWidth > 1199) close();')
html = html.replace("nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', close));", """nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', close));
      document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && header.classList.contains('is-open')) { close(); toggle.focus(); }
      });
      document.addEventListener('click', event => { if (!header.contains(event.target)) close(); });
      header.addEventListener('focusout', event => { if (event.relatedTarget && !header.contains(event.relatedTarget)) close(); });""")
# Second pass: apply the approved UX audit while retaining the original text source.
html = html.replace('href="ameli-modern.css"', 'href="ameli-modern.css?v=20260907"')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-refinements.css?v=20260907">\n</head>')
html = html.replace('src="ameli-modern.js"', 'src="ameli-modern.js?v=20260907"')
html = html.replace('</body>', '  <script src="ameli-refinements.js?v=20260907"></script>\n</body>')
for filename, description in {
    'dishware-clear-glass.png': 'Прозрачные бокалы для классической сервировки',
    'dishware-clear-plate-black.png': 'Прозрачная тарелка с чёрным краем',
    'dishware-clear-plate-silver.png': 'Прозрачная тарелка с серебряным краем',
    'dishware-clear-plate-gold.png': 'Прозрачная тарелка с золотым краем',
    'dishware-rouming-glasses.png': 'Цветные бокалы «Роуминг»',
    'dishware-color-plates.png': 'Коллекция цветных тарелок',
}.items():
    html = re.sub(r'(<img src="premium-assets/' + re.escape(filename) + r'"[^>]*?)alt=""', r'\1alt="' + description + '"', html)
html = html.replace('class="dishware-duo" role="img"', 'class="dishware-duo" role="group"')
hero_start, hero_end = html.index('<section class="hero"'), html.index('<section class="section" id="problem">')
hero = html[hero_start:hero_end].replace('s2-banquet-hall.jpeg', 's4-hall-toile.jpg').replace('width="1280" height="854"', 'width="852" height="1280"')
html = html[:hero_start] + hero + html[hero_end:]
html = html.replace('<section class="section" id="problem">', '''<nav class="section-jump-nav" aria-label="Быстрый переход по разделам">
      <div class="shell jump-links">
        <a href="#furniture-options">Мебель</a><a href="#textile">Текстиль</a><a href="#tableware">Посуда</a><a href="#ceremony-zones">Фотозоны</a><a href="#before-after">До / после</a><a href="#textile-payback">Расчёт</a>
      </div>
    </nav>
    <section class="section" id="problem">''')
html = html.replace('Покажем один зал без оформления и несколько вариантов после обновления — с мебелью, текстилем и декором Ameli.', 'Один зал в одном ракурсе: без оформления и с мебелью, текстилем и декором Ameli.')
comparison_start = html.index('        <div class="before-after-grid">')
comparison_end = html.index('\n    <section class="section" id="reasons">', comparison_start)
html = html[:comparison_start] + '''        <div class="before-after-grid honest-comparison">
          <figure class="comparison-frame comparison-before">
            <img src="premium-assets/hall-without-decor-visualization.jpg" width="1535" height="1024" loading="lazy" alt="Визуализация того же зала без банкетной мебели и оформления">
            <figcaption><span>ДО · ВИЗУАЛИЗАЦИЯ</span><strong>Пространство без оформления</strong></figcaption>
          </figure>
          <figure class="comparison-frame comparison-after">
            <img src="s2-banquet-hall.jpeg" width="1280" height="854" loading="lazy" alt="Фотография того же банкетного зала с мебелью, текстилем и сервировкой">
            <figcaption><span>ПОСЛЕ · ФОТОГРАФИЯ</span><strong>Мебель и текстиль в единой палитре</strong></figcaption>
          </figure>
        </div>
        <p class="comparison-explanation">Слева — визуализация зала без оформления, созданная на основе фотографии справа. Справа — фотография готового оформления. Так можно сравнить одно пространство в одном ракурсе.</p>
      </div>
    </section>
''' + html[comparison_end:]
html = html.replace('<div class="textile-payback-layout">', '''<div class="calc-live-summary" aria-label="Текущий результат расчёта">
          <div><span>Инвестиция</span><output id="textileStickyInvestment">106 200 ₽</output></div>
          <div><span>Для 60 гостей</span><output id="textileStickyEvents">3 мероприятия</output></div>
          <a href="#textileResultPanel">К результату</a>
        </div>
        <div class="textile-payback-layout">''')
html = html.replace('<aside class="textile-payback-result"', '<aside id="textileResultPanel" class="textile-payback-result"')
html = html.replace('<p class="textile-result-status"', '<p class="textile-result-basis">По арендной выручке, без учёта расходов.</p>\n              <p class="textile-result-status"')
html = html.replace('<div class="textile-result-investment">', '''<div class="textile-result-actions"><a class="button" id="textileDiscussTelegram" href="https://t.me/amelirental" target="_blank" rel="noopener">Обсудить этот комплект</a><p>Откроется Telegram с черновиком вашего расчёта.</p></div>
              <div class="textile-result-investment">''')
html = html.replace('<footer><span>AMELI', '<div class="catalog-return"><a href="https://catalog.ameli-rental.ru/" target="_blank" rel="noopener">Перейти в каталог аренды Ameli<span class="material-symbols-outlined" aria-hidden="true">north_east</span></a></div>\n        <footer><span>AMELI')

# Validate before updating any figures: invalid values must never look like a quote.
html = html.replace('      function update() {\n        const roundQty', '''      function update() {
        let hasErrors = false;
        inputIds.forEach(id => {
          const input = inputs[id];
          const raw = input.value.trim();
          const value = Number(raw);
          const minimum = id === 'textileColors' ? 1 : 0;
          const invalid = raw === '' || !Number.isFinite(value) || !Number.isSafeInteger(value) || value < minimum || value > 1000000;
          const errorId = `${id}Error`;
          let error = get(errorId);
          if (!error) {
            error = document.createElement('p'); error.id = errorId; error.className = 'input-error';
            input.closest('.textile-input').append(error);
            input.setAttribute('aria-describedby', errorId);
          }
          input.setAttribute('aria-invalid', String(invalid));
          error.hidden = !invalid;
          error.textContent = invalid ? `Введите целое число от ${minimum} до 1 000 000.` : '';
          hasErrors ||= invalid;
        });
        root.dataset.valid = String(!hasErrors);
        if (hasErrors) {
          ['textileOneColorTotal','textileInvestmentTotal','textileResultInvestment','textileMainPayback'].forEach(id => { get(id).textContent = '—'; });
          get('textileMainStatus').textContent = 'Проверьте выделенные поля — расчёт обновится после исправления.';
          [40,60,80].forEach(n => { get(`textilePayback${n}`).textContent = '—'; get(`textileStatus${n}`).textContent = 'Проверьте значения в полях'; });
          root.dispatchEvent(new Event('calculationupdate'));
          return;
        }
        const roundQty''')
html = html.replace("      inputIds.forEach(id => inputs[id].addEventListener('input', update));", """      inputIds.forEach(id => {
        inputs[id].step = '1';
        inputs[id].addEventListener('input', update);
      });""")
html = html.replace("          get('textileMainStatus').textContent = 'Комплекта достаточно';\n        }\n      }", "          get('textileMainStatus').textContent = 'Комплекта достаточно';\n        }\n        root.dispatchEvent(new Event('calculationupdate'));\n      }")
(root / 'modern-redesign.html').write_text(html)
print('Created modern-redesign.html; source page unchanged.')
