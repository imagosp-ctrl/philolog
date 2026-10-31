#!/usr/bin/env python3
"""
Build texts/smallparaklisis.json from tools/smallparaklisis_source.txt.

Each word reuses an existing glossed entry from the other texts/*.json files
when the same form is already on the site; otherwise it comes from
tools/smallparaklisis_glossary.json (lemma, gloss, part of speech, definition),
with phonetics, colour and Strong's data filled in here.

Usage: python3 tools/build_smallparaklisis.py
"""

import glob, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from generate_phonetics import greek_to_phonetic

SOURCE   = os.path.join(ROOT, 'tools', 'smallparaklisis_source.txt')
GLOSSARY = os.path.join(ROOT, 'tools', 'smallparaklisis_glossary.json')
OUTPUT   = os.path.join(ROOT, 'texts', 'smallparaklisis.json')
STRONGS  = os.path.join(ROOT, 'strongs_cache.json')

PUNCT = re.compile(r'[,.·;:!]+$')
# Greek punctuation → the English mark used at the end of a gloss
GLOSS_PUNCT = {',': ',', '.': '.', '·': ';', ';': '?', ':': ':', '!': '!'}

# Site-wide colour per part of speech
COLOURS = {
    'noun': 'blue', 'pronoun': 'blue', 'article': 'grey', 'verb': 'gold',
    'verb (participle)': 'gold', 'verb (infinitive)': 'gold', 'adjective': 'lavender',
    'preposition': 'vibrant green', 'conjunction': 'grey', 'adverb': 'grey',
    'particle': 'grey', 'interjection': 'purple',
}

# Texts that aren't word lists, or are older copies
SKIP = re.compile(r'lexicon|cache|chunks|cloze|matching|root_fam|vocab|hero_quotes|psalms\.json|_old|backup|smallparaklisis')


def nfc(s):
    return unicodedata.normalize('NFC', s)

def key(word):
    """Match key: no trailing punctuation, grave → acute, lowercase."""
    d = unicodedata.normalize('NFD', PUNCT.sub('', word)).replace('̀', '́')
    return unicodedata.normalize('NFC', d).lower()

def bare(s):
    """Lowercase with all diacritics removed (for Strong's lookups)."""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()


def load_existing():
    entries = {}
    # Earlier smallparaklisis entries first, so its hymns keep their curated glosses
    paths = [OUTPUT] + [p for p in sorted(glob.glob(os.path.join(ROOT, 'texts', '*.json'))) if not SKIP.search(p)]
    for path in paths:
        try:
            data = json.load(open(path, encoding='utf-8'))
        except (ValueError, OSError):
            continue
        for w in data if isinstance(data, list) else []:
            if w.get('type') or w.get('partOfSpeech') in ('rubric', 'punctuation') or not w.get('gloss'):
                continue
            entries.setdefault(key(w['word']), w)
    return entries


def load_strongs():
    by_lemma = {}
    for num, s in json.load(open(STRONGS, encoding='utf-8')).items():
        if s.get('lemma'):
            by_lemma.setdefault(nfc(s['lemma']), (num, s))
            by_lemma.setdefault(bare(s['lemma']), (num, s))
    return by_lemma


def new_entry(g, strongs):
    pos = g['partOfSpeech']
    hit = strongs.get(nfc(g['lemma'])) or strongs.get(bare(g['lemma']))
    num, s = hit if hit else ('', {})
    return {
        'word': g['word'], 'phonetic': '', 'lemma': g['lemma'], 'gloss': g['gloss'],
        'partOfSpeech': pos, 'colorCode': COLOURS.get(pos, 'grey'), 'strongs': num,
        'canonical_lemma': g['lemma'], 'liturgical_gloss': g['gloss'],
        'definition': g.get('definition', ''), 'strongs_translit': s.get('translit', ''),
        'derivation': (s.get('derivation') or '').strip(),
    }


def token_entry(token, existing, glossary, strongs):
    k = key(token)
    base = existing.get(k)
    entry = dict(base) if base else new_entry(glossary[k], strongs)
    mark = PUNCT.search(token)
    gloss = re.sub(r'[,.;:?!]+$', '', entry.get('gloss', ''))
    if mark:
        gloss += GLOSS_PUNCT.get(mark.group(0)[-1], '')
    entry['word'] = token
    entry['gloss'] = gloss
    entry['liturgical_gloss'] = gloss
    if not base or not entry.get('phonetic'):
        entry['phonetic'] = greek_to_phonetic(PUNCT.sub('', token))
    return entry


def main():
    existing = load_existing()
    glossary = {}
    if os.path.exists(GLOSSARY):
        for g in json.load(open(GLOSSARY, encoding='utf-8')):
            glossary.setdefault(key(g['word']), g)
    strongs = load_strongs()

    lines = []
    for raw in open(SOURCE, encoding='utf-8'):
        line = nfc(raw.strip())
        if not line or (line.startswith('#') and not line.startswith('##')):
            continue
        lines.append(line)

    out, missing = [], []
    for i, line in enumerate(lines):
        if line.startswith('@@'):
            out.append({'word': line[2:].strip(), 'type': 'section'})
            continue
        if line.startswith('##'):
            out.append({'word': line[2:].strip(), 'partOfSpeech': 'rubric'})
            continue
        for token in line.split():
            if key(token) not in existing and key(token) not in glossary:
                missing.append(token)
                continue
            out.append(token_entry(token, existing, glossary, strongs))
        # Break between consecutive text lines; a rubric or section already starts its own row
        if i + 1 < len(lines) and not lines[i + 1].startswith(('##', '@@')):
            out.append({'word': '\n', 'type': 'lineBreak'})

    if missing:
        print(f'{len(missing)} words have no entry yet, e.g. {missing[:10]}')
        sys.exit(1)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    words = sum(1 for e in out if 'type' not in e and e.get('partOfSpeech') != 'rubric')
    print(f'Wrote {OUTPUT}: {words} words, {sum(1 for e in out if e.get("partOfSpeech") == "rubric")} labels')


if __name__ == '__main__':
    main()
