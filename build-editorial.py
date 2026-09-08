from pathlib import Path
from html import escape
import json
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
html = html.replace('href="ameli-modern.css"', 'href="ameli-modern.css?v=20260908b"')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-refinements.css?v=20260908b">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-calculator.css?v=20260908b">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-order.css?v=20260908c">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-benefits.css?v=20260908d">\n</head>')
html = html.replace('src="ameli-modern.js"', 'src="ameli-modern.js?v=20260908b"')
html = html.replace('</body>', '  <script src="ameli-refinements.js?v=20260908b"></script>\n</body>')
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
# Use compressed originals supplied by the owner; retain complete compositions.
ceremony_images = json.loads((root / 'ceremony-images.json').read_text())
ceremony_figures = []
for number, item in enumerate(ceremony_images, start=1):
    small, large = item['variants']
    ceremony_figures.append(
        f'          <figure class="ceremony-example"><img src="{large["path"]}" '
        f'srcset="{small["path"]} {small["width"]}w, {large["path"]} {large["width"]}w" '
        'sizes="(max-width:600px) calc((100vw - 54px) / 2), (max-width:1000px) calc((91vw - 24px) / 2), (max-width:1406px) calc((91vw - 48px) / 3), 411px" '
        f'width="{large["width"]}" height="{large["height"]}" loading="lazy" decoding="async" alt="{escape(item["alt"])}">'
        f'<figcaption><span>{number:02}</span><strong>{escape(item["title"])}</strong></figcaption></figure>'
    )
ceremony_start = html.index('        <div class="ceremony-grid"')
ceremony_end = html.index('\n        </div>', ceremony_start)
html = html[:ceremony_start] + '        <div class="ceremony-grid" aria-label="Примеры фотозон и зон церемонии">\n' + '\n'.join(ceremony_figures) + html[ceremony_end:]
hero_start, hero_end = html.index('<section class="hero"'), html.index('<section class="section" id="problem">')
hero = html[hero_start:hero_end].replace('s2-banquet-hall.jpeg', 's4-hall-toile.jpg').replace('width="1280" height="854"', 'width="852" height="1280"')
html = html[:hero_start] + hero + html[hero_end:]
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
# Make the business mechanism explicit while keeping all six original explanations.
benefits_start = html.index('    <section class="section" id="reasons">')
benefits_end = html.index('    <section class="section dark color-combinations-section" id="color-combinations">', benefits_start)
benefit_factors = re.search(r'<ul class="payback-factors".*?</ul>', html[benefits_start:benefits_end], flags=re.S).group()
for old_icon, icon_id in zip(re.findall(r'<span class="payback-icon".*?</span>', benefit_factors), ['income', 'conversion', 'check', 'content', 'referral', 'refresh']):
    benefit_factors = benefit_factors.replace(old_icon, f'<svg class="benefit-icon" width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><use href="#benefit-{icon_id}"/></svg>', 1)
benefits = (root / 'business-benefits.html').read_text().replace('{{FACTORS}}', benefit_factors)
html = html[:benefits_start] + benefits.rstrip() + '\n\n' + html[benefits_end:]
# The compact calculator reuses the original field IDs and calculation logic.
calculator_start = html.index('    <section class="section soft textile-payback-section"')
calculator_end = html.index('    <section class="section order-section"', calculator_start)
html = html[:calculator_start] + (root / 'textile-calculator.html').read_text().rstrip() + '\n\n' + html[calculator_end:]
# Keep the six original steps and perks, replacing hidden photos with light SVG illustrations.
order_start = html.index('    <section class="section order-section"')
order_end = html.index('    <section class="final"', order_start)
order = html[order_start:order_end]
order_icons = re.findall(r'<svg\b.*?</svg>', (root / 'order-icons.html').read_text(), flags=re.S)
order_steps = re.findall(r'<article class="order-step">.*?</article>', order, flags=re.S)
assert len(order_icons) == len(order_steps) == 6
for number, (step, icon) in enumerate(zip(order_steps, order_icons), start=1):
    heading = re.search(r'<h3>.*?</h3>', step, flags=re.S).group()
    description = re.search(r'<div class="order-step-copy"><h3>.*?</h3>(<p>.*?</p>)</div>', step, flags=re.S).group(1)
    perk = re.search(r'<p class="order-perk">.*?</p>', step, flags=re.S)
    replacement = (
        '<article class="order-step">\n'
        f'            <span class="order-step-number" aria-hidden="true">{number:02}</span>\n'
        f'            <div class="order-step-heading">{icon}{heading}</div>\n'
        f'            {description}\n'
        + (f'            {perk.group()}\n' if perk else '')
        + '          </article>'
    )
    order = order.replace(step, replacement, 1)
html = html[:order_start] + order + html[order_end:]
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
