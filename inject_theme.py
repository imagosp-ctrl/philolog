"""
Injects dark-mode theme wiring into all Philolog HTML pages.
Run once, then delete this file.
"""
import os, re

BASE = '/Users/karispikkeland/Documents/philolog-github'

PAGES = [
    'prayers.html',
    'apolytikia.html',
    'memory.html',
    'lexicon.html',
    'index.html',
    'pronunciation-guide.html',
    'quick_guide.html',
    'resources.html',
    'about.html',
]

ANTI_FOUC = '  <script>(function(){var t=localStorage.getItem(\'philolog-theme\');if(t===\'dark\'||(t===null&&window.matchMedia(\'(prefers-color-scheme: dark)\').matches)){document.documentElement.classList.add(\'dark-theme\');}})()</script>\n  <link rel="stylesheet" href="theme.css">\n'

TOGGLE_BTN = '<button id="theme-toggle" aria-label="Toggle dark mode" style="width:36px;height:36px;border:none;border-radius:8px;background:transparent;font-size:1.2rem;cursor:pointer;display:flex;align-items:center;justify-content:center;">🌙</button>'

THEME_SCRIPT = '\n  <script src="theme.js"></script>\n'

for page in PAGES:
    path = os.path.join(BASE, page)
    if not os.path.exists(path):
        print(f'SKIP (not found): {page}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    changed = False

    # 1. Anti-FOUC + theme.css — inject after <meta name="viewport"...>
    if 'philolog-theme' not in html:
        html = re.sub(
            r'(<meta name="viewport"[^>]*>)',
            r'\1\n' + ANTI_FOUC,
            html,
            count=1
        )
        changed = True
    else:
        print(f'  already has anti-FOUC: {page}')

    # 2. Desktop toggle — inject inside the flex div that holds help-dropdown
    if 'theme-toggle' not in html:
        html = re.sub(
            r'(<div style="display:flex;align-items:center;gap:\.5rem">)',
            r'\1\n        ' + TOGGLE_BTN,
            html,
            count=1
        )
        changed = True
    else:
        print(f'  already has theme-toggle: {page}')

    # 3. theme.js before </body>
    if 'theme.js' not in html:
        html = html.replace('</body>', THEME_SCRIPT + '</body>', 1)
        changed = True
    else:
        print(f'  already has theme.js: {page}')

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'OK: {page}')
    else:
        print(f'NO CHANGES: {page}')

print('\nDone.')
