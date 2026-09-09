"""Approved launch copy and shared metadata for the preview and portable release."""
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parent


def apply_metadata(html, base_url=None):
    site = json.loads((ROOT / 'site-publication.json').read_text())
    # The repository page is a noindex preview. Only an explicit export URL
    # produces an indexable release; both point canonically to the chosen site.
    url = (base_url or site['url']).rstrip('/') + '/'
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or not parsed.netloc or parsed.query
            or parsed.fragment or parsed.username):
        raise ValueError('The public URL must be an HTTPS directory without query or fragment.')
    channels = json.loads((ROOT / 'contact-channels.json').read_text())
    hero = re.search(r'<figure class="hero-visual">.*?<img\s[^>]*src="([^"]+)"', html, re.S)
    if not hero:
        raise ValueError('Cannot find the current hero image for the share card.')
    image_url = urljoin(url, hero.group(1))
    graph = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Organization', '@id': url + '#organization',
                'name': site['name'], 'legalName': site['legalName'],
                'url': url, 'taxID': site['taxID'],
                'identifier': {'@type': 'PropertyValue', 'propertyID': 'ОГРНИП', 'value': site['ogrnip']},
                'logo': urljoin(url, 'premium-assets/ameli-rental-logo.png'),
                'email': channels['email'], 'telephone': channels['phone'],
                'areaServed': {'@type': 'Country', 'name': 'Россия'},
                'location': {
                    '@type': 'Place', 'name': 'Склад: просмотр изделий и самовывоз по согласованию',
                    'address': {'@type': 'PostalAddress', **site['warehouse']},
                },
                'sameAs': [channels['telegram'], channels['max']],
            },
            {
                '@type': 'WebSite', '@id': url + '#website', 'url': url,
                'name': site['name'], 'inLanguage': 'ru-RU',
                'publisher': {'@id': url + '#organization'},
            },
            {
                '@type': 'WebPage', '@id': url + '#webpage', 'url': url,
                'name': site['title'], 'description': site['description'],
                'inLanguage': 'ru-RU', 'isPartOf': {'@id': url + '#website'},
                'about': {'@id': url + '#organization'},
                'primaryImageOfPage': {'@type': 'ImageObject', 'url': image_url},
            },
        ],
    }
    html = re.sub(r'<title>.*?</title>', '<title>' + escape(site['title']) + '</title>', html, count=1)
    html = re.sub(r'\s*<meta\b(?=[^>]*(?:name="(?:description|robots|twitter:card)"|property="og:[^"]+"))[^>]*>', '', html)
    html = re.sub(r'\s*<link\b(?=[^>]*rel="canonical")[^>]*>', '', html)
    html = re.sub(r'\s*<script type="application/ld\+json" id="site-structured-data">.*?</script>', '', html, flags=re.S)
    metadata = {
        'description': site['description'],
        'robots': 'index, follow, max-image-preview:large' if base_url else 'noindex, follow',
        'twitter:card': 'summary_large_image',
    }
    additions = [f'  <meta name="{key}" content="{escape(value, quote=True)}">' for key, value in metadata.items()]
    og = {'type': 'website', 'locale': 'ru_RU', 'site_name': site['name'],
          'title': site['title'], 'description': site['description'],
          'url': url, 'image': image_url,
          'image:alt': 'Готовое оформление банкетного зала: мебель, текстиль и сервировка'}
    additions += [f'  <meta property="og:{key}" content="{escape(value, quote=True)}">' for key, value in og.items()]
    additions += [f'  <link rel="canonical" href="{escape(url, quote=True)}">',
                  '  <script type="application/ld+json" id="site-structured-data">'
                  + json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + '</script>']
    return html.replace('</head>', '\n'.join(additions) + '\n</head>', 1)


def apply_release_content(html):
    html = html.replace('<strong>AMELI</strong>', '<strong>Амели Декор ПРО</strong>')
    html = html.replace('AMELI · ДЛЯ ПЛОЩАДОК', 'Амели Декор ПРО')
    html = html.replace('Ameli в цифрах', 'Амели Декор ПРО в цифрах')
    html = html.replace('Перейти в каталог аренды Ameli', 'Перейти в каталог аренды Амели')
    html = html.replace('    <section class="final" id="contact">',
                        (ROOT / 'order-faq.html').read_text() + '\n    <section class="final" id="contact">', 1)
    checklist = '<div class="checklist"><span>мебель и текстиль</span><span>посуда и декор</span><span>визуализация зала</span><span>презентация для продаж</span></div>'
    assert html.count(checklist) == 1
    html = html.replace(checklist, '''<p class="minimum-order">Минимальной суммы заказа нет</p>
            <div class="warehouse-info">
              <h3>Посмотреть изделия и забрать заказ</h3>
              <address>Московская область, г. Дзержинский,<br>ул. Стройгородок, 5</address>
              <p>Посещение склада — по предварительному согласованию с менеджером.</p>
              <p>Самовывоз или доставка в любой регион России.</p>
            </div>''', 1)
    html, count = re.subn(r'        <footer>.*?</footer>', (ROOT / 'company-footer.html').read_text().rstrip(), html, count=1, flags=re.S)
    assert count == 1
    html = html.replace('</head>', '  <link rel="stylesheet" href="ameli-launch.css?v=20260909t">\n</head>', 1)
    return apply_metadata(html)
