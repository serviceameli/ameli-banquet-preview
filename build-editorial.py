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
# Fit the complete source photo to the same presentation frame as neighbouring chairs.
# The SVG only positions the original bitmap; the furniture pixels are unchanged.
html = re.sub(r'<img src="premium-assets/marseille-blue-silver\.webp"[^>]*>',
              '<svg class="marseille-source-photo" viewBox="0 0 840 1240" width="840" height="1240" role="img" aria-label="Стул Марсель с голубой обивкой и серебряным каркасом">'
              '<image href="premium-assets/marseille-blue-silver-full.webp" x="-30" y="88" width="1024" height="1024"/></svg>', html)
html = html.replace('src="premium-assets/visualization-crossback-table.png"', 'src="premium-assets/visualization-crossback-table.webp"')
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
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-refinements.css?v=20260908n">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-calculator.css?v=20260908b">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-order.css?v=20260908c">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-benefits.css?v=20260908d">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-showcase.css?v=20260908e">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-furniture.css?v=20260908k">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-categories.css?v=20260908l">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-spacing.css?v=20260908o">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-opening.css?v=20260909d">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-contact.css?v=20260909b">\n</head>')
html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-headings.css?v=20260909a">\n</head>')
html = html.replace('src="ameli-modern.js"', 'src="ameli-modern.js?v=20260908b"')
html = html.replace('</body>', '  <script src="ameli-refinements.js?v=20260908q"></script>\n</body>')
html = html.replace('</body>', '  <script src="ameli-showcase.js?v=20260908e"></script>\n</body>')
html = html.replace('</body>', '  <script src="ameli-contact.js?v=20260908q"></script>\n</body>')
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
# Retain all four furniture explanations while making each benefit visually distinct.
furniture_start = html.index('    <section class="section soft furniture-section" id="furniture">')
furniture_end = html.index('    <section class="section furniture-examples-section"', furniture_start)
furniture = html[furniture_start:furniture_end]
furniture = furniture.replace('<div class="furniture-story-copy">', '<div class="furniture-story-copy"><div class="furniture-intro">', 1)
furniture = furniture.replace('<ol class="furniture-benefits">', '</div><ol class="furniture-benefits">', 1)
furniture_icons = re.findall(r'<svg\b.*?</svg>', (root / 'furniture-icons.html').read_text(), flags=re.S)
assert len(furniture_icons) == 4
for number, icon in enumerate(furniture_icons, start=1):
    furniture = furniture.replace(f'<b>{number:02}</b>', icon, 1)
# Real photograph IMG_0169.jpg from the owner's shared shoot, compressed without retouching.
furniture = re.sub(r'<img src="premium-assets/textile-chair-covers\.png"[^>]*>',
                  '<img src="premium-assets/furniture-marseille-set-1000.webp" srcset="premium-assets/furniture-marseille-set-480.webp 480w, premium-assets/furniture-marseille-set-1000.webp 1000w" '
                  'sizes="(max-width:600px) 96px, (max-width:900px) 160px, (max-width:1406px) calc((91vw - 28px) * .301), 377px" '
                  'width="1000" height="1500" loading="lazy" decoding="async" alt="Зелёные стулья «Марсель» с золотистым каркасом у столов со светлыми скатертями">', furniture)
html = html[:furniture_start] + furniture + html[furniture_end:]
# Keep every original category explanation; use four cards beside a photograph
# and a fifth card below it, so the extra point does not add a full desktop row.
category_icons = {re.search(r'data-key="([^"]+)"', svg).group(1): svg
                  for svg in re.findall(r'<svg\b.*?</svg>', (root / 'category-icons.html').read_text(), flags=re.S)}
category_icons['palette'] = furniture_icons[1].replace('furniture-icon', 'category-icon')
category_icons['covers'] = furniture_icons[2].replace('furniture-icon', 'category-icon')
category_specs = [
    ('textile', ['tablecloth', 'drapery', 'cushion', 'covers', 'sewing'],
     'premium-assets/textile-banquet-set-1200.webp', 'premium-assets/textile-banquet-set-480.webp', 1200, 800,
     'Бархатные скатерти и салфетки в согласованной зелёной палитре в оформлении зала'),
    ('tableware', ['dishware', 'setting', 'palette', 'care', 'calculate'],
     'premium-assets/space-showcase/light-detail-1600.webp', 'premium-assets/space-showcase/light-detail-800.webp', 1600, 1067,
     'Фигурные белые тарелки, прозрачные бокалы и золотистые приборы в готовой сервировке'),
    ('ceremony', ['modular', 'instructions', 'quick', 'storage', 'palette'],
     'premium-assets/ceremony-terrace-960.webp', 'premium-assets/ceremony-terrace-480.webp', 960, 1280,
     'Зона церемонии на террасе с волнообразным текстильным фоном и кремовыми пуфами'),
]
for category, icon_keys, large, small, width, height, alt in category_specs:
    pattern = (rf'<div class="furniture-top {category}-top">\s*<div>(.*?)</div>\s*'
               rf'<div class="furniture-points {category}-points">(.*?)</div>\s*</div>')
    match = re.search(pattern, html, flags=re.S)
    assert match, f'Missing {category} introduction'
    intro, points = match.groups()
    lead_start = intro.index('<p class="lead">')
    intro = '<div class="category-heading">' + intro[:lead_start] + '</div>' + intro[lead_start:]
    points = re.findall(r'<article class="furniture-point"><b>\d+</b><div><strong>(.*?)</strong><p>(.*?)</p></div></article>', points, flags=re.S)
    assert len(points) == len(icon_keys) == 5, f'Expected all five {category} points'
    cards = [f'<article class="category-card{ " category-final" if i == 4 else ""}">{category_icons[key]}<h3>{title}</h3><p>{body}</p></article>'
             for i, ((title, body), key) in enumerate(zip(points, icon_keys))]
    small_width = 800 if category == 'tableware' else 480
    photo = (f'<figure class="category-photo"><img src="{large}" srcset="{small} {small_width}w, {large} {width}w" '
             'sizes="(max-width:600px) 96px, (max-width:900px) 160px, (max-width:1406px) calc((91vw - 28px) * .301), 377px" '
             f'width="{width}" height="{height}" loading="lazy" decoding="async" alt="{escape(alt)}"></figure>')
    story = ('<div class="category-story"><div class="category-story-copy"><div class="category-intro">' + intro + '</div>'
             '<div class="category-benefits">' + ''.join(cards[:4]) + '</div></div>'
             '<div class="category-visual-column">' + photo + cards[4] + '</div></div>')
    html = html[:match.start()] + story + html[match.end():]
# Recompose the existing catalogue fragments in HTML without altering product pixels.
def textile_fragment(class_name, box, label):
    x, y, width, height = box
    style = f'aspect-ratio:{width}/{height};--fragment-width:{1190 / width * 100:.6f}%;--fragment-left:{-x / width * 100:.6f}%;--fragment-top:{-y / height * 100:.6f}%'
    return (f'<span class="textile-fragment {class_name}" style="{style}" role="img" aria-label="{escape(label)}">'
            '<img src="premium-assets/textile-velvet-catalog.png" width="1190" height="649" loading="lazy" decoding="async" alt=""></span>')

textile_products = ''.join(textile_fragment(name, box, label) for name, box, label in [
    ('textile-fragment-rect', (96, 110, 336, 155), 'Прямоугольная скатерть из зелёного бархата'),
    ('textile-fragment-round', (39, 296, 254, 171), 'Круглая скатерть из зелёного бархата'),
    ('textile-fragment-napkin', (312, 270, 151, 213), 'Салфетка из зелёного бархата'),
])
swatch_columns = [508, 593, 678, 762, 847, 932, 1016]
swatch_rows = [
    (110, ['Чёрный', 'Тёмная ночь', 'Синий Ван Гога', 'Тихий океан', 'Голубой сапфир', 'Белый ландыш', 'Жемчужный']),
    (214, ['Серо-серебряный', 'Пепельно-серый', 'Серый', 'Фиалковая', 'Сиреневая дымка', 'Пастельно-сиреневый', 'Бледно-розовый']),
    (317, ['Малиновый', 'Розовая сакура', 'Фруктовый зефир', 'Кокосовый раф', 'Капучино', 'Латте', 'Миндальный латте']),
    (419, ['Зелёный малахит', 'Зелёный чай', 'Шалфей', 'Светло-зелёный', 'Золотая горчица', 'Спелая дыня', 'Рыжая лиса']),
    (522, ['Гранатовая', 'Красный дракон', 'Янтарная']),
]
textile_swatches = ''
for row_index, (y, names) in enumerate(swatch_rows):
    columns = swatch_columns[2:5] if row_index == 4 else swatch_columns
    for x, name in zip(columns, names):
        textile_swatches += textile_fragment('textile-swatch', (x, y, 53, 30), name)
textile_composition = ('<div class="model-image textile-image textile-composition" role="group" aria-label="Скатерти, салфетка и палитра бархата">'
                       + textile_products + '<div class="textile-swatch-grid" role="group" aria-label="31 оттенок бархата">'
                       + textile_swatches + '</div></div>')
html, textile_replacements = re.subn(r'<div class="model-image textile-image catalog"><img src="premium-assets/textile-velvet-catalog\.png"[^>]*></div>', textile_composition, html)
assert textile_replacements == 1, 'Expected one textile catalogue card.'
# Use compressed originals supplied by the owner; retain complete compositions.
ceremony_images = json.loads((root / 'ceremony-images.json').read_text())
ceremony_figures = []
for item in ceremony_images:
    small, large = item['variants']
    ceremony_figures.append(
        f'          <figure class="ceremony-example"><img src="{large["path"]}" '
        f'srcset="{small["path"]} {small["width"]}w, {large["path"]} {large["width"]}w" '
        'sizes="(max-width:600px) calc((100vw - 54px) / 2), (max-width:1000px) calc((91vw - 24px) / 2), (max-width:1406px) calc((91vw - 48px) / 3), 411px" '
        f'width="{large["width"]}" height="{large["height"]}" loading="lazy" decoding="async" alt="{escape(item["alt"])}">'
        '</figure>'
    )
ceremony_start = html.index('        <div class="ceremony-grid"')
ceremony_end = html.index('\n        </div>', ceremony_start)
html = html[:ceremony_start] + '        <div class="ceremony-grid" aria-label="Примеры фотозон и зон церемонии">\n' + '\n'.join(ceremony_figures) + html[ceremony_end:]
hero_start, hero_end = html.index('<section class="hero"'), html.index('<section class="section" id="problem">')
opening_images = json.loads((root / 'opening-images.json').read_text())

def opening_image(slug, alt, sizes, eager=False):
    variants = opening_images[slug]
    large = variants[-1]
    srcset = ', '.join(f'{item["path"]} {item["width"]}w' for item in variants)
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{large["path"]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{large["width"]}" height="{large["height"]}" {loading} decoding="async" alt="{escape(alt)}">')

hero = html[hero_start:hero_end]
hero = re.sub(r'<picture>.*?</picture>', '<picture>' + opening_image(
    'banquet-hall', 'Светлый банкетный зал с круглыми столами, светлыми скатертями и стульями с серебристым каркасом',
    '(max-width:600px) calc(100vw - 40px), (max-width:900px) 91vw, (max-width:1406px) 50vw, 690px', eager=True) + '</picture>', hero, flags=re.S)
# Put the trust facts next to the introduction, before the primary actions.
hero_facts = re.search(r'\n        <div class="hero-facts".*?\n        </div>', hero, flags=re.S)
assert hero_facts, 'Expected the hero trust facts'
hero = hero[:hero_facts.start()] + hero[hero_facts.end():]
hero = hero.replace('          <div class="hero-actions">',
                    '\n'.join('  ' + line for line in hero_facts.group().strip('\n').splitlines()) + '\n          <div class="hero-actions">', 1)
html = html[:hero_start] + hero + html[hero_end:]
html = html.replace('https://serviceameli.github.io/ameli-banquet-preview/s2-banquet-hall.jpeg',
                    'https://serviceameli.github.io/ameli-banquet-preview/premium-assets/opening/banquet-hall-1280.webp')
# Use the four original explanations as a typographic row, without a new icon system.
problem_start = html.index('    <section class="section" id="problem">')
problem_end = html.index('    <section class="section offer-section" id="business">', problem_start)
problem = html[problem_start:problem_end].replace('class="section"', 'class="section soft"', 1)
problem = re.sub(r'\n        <figure class="problem-photo">.*?</figure>', '', problem, flags=re.S)
html = html[:problem_start] + problem + html[problem_end:]
# Give each of the five original services its own supplied image.
offer_start = html.index('    <section class="section offer-section" id="business">')
offer_end = html.index('    <section class="section soft about-section"', offer_start)
offer_source = html[offer_start:offer_end]
offer_points = re.findall(r'<article class="offer-item"><b>\d+</b><div><strong>(.*?)</strong><p>(.*?)</p></div></article>', offer_source, flags=re.S)
assert len(offer_points) == 5, 'Preserve all five original offer explanations'
service_photos = [
    ('visualization-layout', 'Визуализация светлого зала с двумя группами фигурных столов и голубыми стульями'),
    ('banquet-chairs', 'Банкетная мебель со светлой обивкой в готовом оформлении зала'),
    ('velvet-napkin', 'Терракотовая бархатная салфетка с золотистой кисточкой на тёмной тарелке'),
    ('pink-glass', 'Розовые бокалы и стаканы со светлой сервировкой стола'),
    ('forest-ceremony', 'Фотозона в лесу со светлым текстильным фоном, белыми цветами, пуфами и зеркальной дорожкой'),
]
service_cards = []
for number, ((title, copy), (slug, alt)) in enumerate(zip(offer_points, service_photos), start=1):
    sizes = '(max-width:400px) 36vw, (max-width:600px) 144px, (max-width:1100px) calc((91vw - 24px) / 2), (max-width:1406px) calc((91vw - 72px) / 5), 242px'
    if number == 1:
        sizes = '(max-width:400px) 36vw, (max-width:600px) 144px, (max-width:1100px) 260px, (max-width:1406px) calc((91vw - 72px) / 5), 242px'
    photograph = opening_image(slug, alt, sizes)
    photo_class = 'offer-service-photo' + (' offer-service-photo-full' if slug in ('visualization-layout', 'velvet-napkin', 'forest-ceremony') else '')
    service_cards.append(f'          <article class="offer-service"><figure class="{photo_class}">{photograph}</figure>'
                         f'<div class="offer-service-heading"><span class="offer-index" aria-hidden="true">{number:02}</span><h3>{title}</h3></div><p>{copy}</p></article>')
offer = (root / 'opening-offer.html').read_text()
offer_values = {
    'LABEL': re.search(r'<p class="label">.*?</p>', offer_source).group(),
    'HEADING': re.search(r'<h2>.*?</h2>', offer_source).group(),
    'INTRO': re.search(r'<p class="offer-intro">.*?</p>', offer_source).group(),
    'SERVICES': '\n'.join(service_cards),
}
for key, value in offer_values.items():
    offer = offer.replace('{{' + key + '}}', value)
assert '{{' not in offer
html = html[:offer_start] + offer.rstrip() + '\n\n' + html[offer_end:]
# A real-photo showcase with explicitly labelled empty-room visualizations.
comparison_start = html.index('    <section class="section dark before-after-section"')
comparison_end = html.index('    <section class="section" id="reasons">', comparison_start)
showcase_assets = json.loads((root / 'showcase-images.json').read_text())

def showcase_image(slug, sizes, decorative=False):
    item = showcase_assets[slug]
    variants = item['variants']
    large = variants[-1]
    srcset = ', '.join(f'{variant["path"]} {variant["width"]}w' for variant in variants)
    alt = '' if decorative else escape(item['alt'])
    return f'<img src="{large["path"]}" srcset="{srcset}" sizes="{sizes}" width="{large["width"]}" height="{large["height"]}" loading="lazy" decoding="async" alt="{alt}">'

showcase = (root / 'space-showcase.html').read_text()
for slug in showcase_assets:
    showcase = showcase.replace('{{IMAGE:' + slug + '}}', showcase_image(slug, '(max-width:900px) calc(100vw - 40px), (max-width:1406px) calc((91vw - 24px) * .678), 852px'))
    showcase = showcase.replace('{{DETAIL:' + slug + '}}', showcase_image(slug, '(max-width:600px) calc((100vw - 52px) / 2), (max-width:900px) calc((100vw - 64px) / 2), (max-width:1406px) calc((91vw - 24px) * .322), 404px'))
    showcase = showcase.replace('{{THUMB:' + slug + '}}', showcase_image(slug, '(max-width:600px) 86px, 112px', decorative=True))
assert not re.search(r'\{\{(?:IMAGE|DETAIL|THUMB):', showcase), 'A showcase image has not been prepared.'
html = html[:comparison_start] + showcase + html[comparison_end:]
# Make the business mechanism explicit while keeping all six original explanations.
benefits_start = html.index('    <section class="section" id="reasons">')
benefits_end = html.index('    <section class="section dark color-combinations-section" id="color-combinations">', benefits_start)
benefit_factors = re.search(r'<ul class="payback-factors".*?</ul>', html[benefits_start:benefits_end], flags=re.S).group()
for old_icon, icon_id in zip(re.findall(r'<span class="payback-icon".*?</span>', benefit_factors), ['income', 'conversion', 'check', 'content', 'referral', 'refresh']):
    benefit_factors = benefit_factors.replace(old_icon, f'<svg class="benefit-icon" width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><use href="#benefit-{icon_id}"/></svg>', 1)
benefits = (root / 'business-benefits.html').read_text().replace('{{FACTORS}}', benefit_factors)
html = html[:benefits_start] + benefits.rstrip() + '\n\n' + html[benefits_end:]
# The colour controls and examples already explain the combinations; remove the redundant introduction.
combinations_start = html.index('    <section class="section dark color-combinations-section" id="color-combinations">')
combinations_end = html.index('</section>', combinations_start)
combinations, removed = re.subn(r'\s*<p class="lead">.*?</p>', '', html[combinations_start:combinations_end], count=1, flags=re.S)
assert removed == 1
html = html[:combinations_start] + combinations + html[combinations_end:]
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
# Render the same verified contact channels in the footer and in one native dialog.
channels = json.loads((root / 'contact-channels.json').read_text())
options = (root / 'contact-options.html').read_text()
max_channel = ('<div class="contact-channel contact-channel-pending" data-contact-pending="max" role="group" aria-disabled="true">'
               '<span class="contact-channel-icon contact-channel-icon-max" aria-hidden="true">MAX</span>'
               '<span class="contact-channel-text"><strong>MAX</strong><span>Скоро подключим</span></span></div>')
if channels['max']:
    assert channels['max'].startswith(('https://max.ru/', 'https://max.me/'))
    max_channel = ('<a class="contact-channel" data-contact-channel="max" href="' + escape(channels['max'], quote=True) + '" target="_blank" rel="noopener">'
                   '<span class="contact-channel-icon contact-channel-icon-max" aria-hidden="true">MAX</span>'
                   '<span class="contact-channel-text"><strong>MAX</strong><span>Ameli Rental</span></span>'
                   '<span class="contact-channel-arrow" aria-hidden="true">↗</span></a>')
options = options.replace('{{max_channel}}', max_channel)
for key, value in channels.items():
    if value:
        options = options.replace('{{' + key + '}}', escape(value, quote=True))
assert '{{' not in options
contact_box = ('<aside class="contact-box"><strong>Связаться с менеджером</strong>'
               '<p>Для первого разговора достаточно фотографий зала и краткого описания задачи. Выберите удобный способ связи.</p>'
               + options + '</aside>')
html, contact_count = re.subn(r'<aside class="contact-box">.*?</aside>', lambda _: contact_box, html, flags=re.S)
assert contact_count == 1
# Keep navigation and interactive controls intact; only sales CTAs open the chooser.
def contact_trigger(match):
    tag = match.group()
    classes = re.search(r'class="([^"]+)"', tag)
    if not classes or 'button' not in classes.group(1).split():
        return tag
    tag = re.sub(r'href="[^"]+"', 'href="#contact"', tag)
    tag = re.sub(r' (?:target|rel)="[^"]*"', '', tag)
    return tag[:-1] + ' data-contact-open>'
html, _ = re.subn(r'<a\b[^>]*href="(?:#contact|https://t\.me/amelirental|https://wa\.me/79850843855)"[^>]*>', contact_trigger, html)
assert html.count(' data-contact-open') == 7
dialog = (root / 'contact-dialog.html').read_text().replace('{{contact_options}}', options)
html = html.replace('  <div class="mobile-cta">', dialog + '\n\n  <div class="mobile-cta">', 1)
(root / 'modern-redesign.html').write_text(html)
print('Created modern-redesign.html; source page unchanged.')
