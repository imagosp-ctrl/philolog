#!/usr/bin/env python3
"""
Generate Modern/Liturgical Greek phonetics for all JSON text files.

Rules:
  - Surface form: use `word` field in text files, `lemma` in lexicon.json
  - Modern/Liturgical pronunciation (β=v, η=ee, υ=ee, γ=gh/y, δ=dh, θ=th, χ=kh, φ=f)
  - Syllables separated by hyphens; stressed syllable in UPPERCASE
  - No use of strongs_translit
"""

import json, unicodedata, re, glob, os, sys

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _nfd(c):
    return unicodedata.normalize('NFD', c)

def has_stress(c):
    """True if character carries an acute, grave, or perispomeni accent."""
    return any(x in ('\u0301', '\u0300', '\u0342') for x in _nfd(c))

def has_diaeresis(c):
    """True if character has a diaeresis (marks split diphthong)."""
    return '\u0308' in _nfd(c)

def base(c):
    """Lowercase base letter, all diacritics stripped."""
    return ''.join(x for x in _nfd(c) if unicodedata.category(x) != 'Mn').lower()

def is_greek(c):
    cp = ord(c)
    return (0x0370 <= cp <= 0x03FF) or (0x1F00 <= cp <= 0x1FFF)

# ---------------------------------------------------------------------------
# Phoneme tables
# ---------------------------------------------------------------------------

VOWEL_MAP = {
    'α': 'ah', 'ε': 'eh', 'η': 'ee', 'ι': 'ee',
    'ο': 'o',  'υ': 'ee', 'ω': 'oh',
}

CONS_MAP = {
    'β': 'v',  'δ': 'dh', 'ζ': 'z',  'θ': 'th',
    'κ': 'k',  'λ': 'l',  'μ': 'm',  'ν': 'n',
    'ξ': 'ks', 'π': 'p',  'ρ': 'r',  'σ': 's',
    'ς': 's',  'τ': 't',  'φ': 'f',  'χ': 'kh',
    'ψ': 'ps',
}

# γ palatalises before these
FRONT = {'ε', 'η', 'ι', 'υ'}

# αυ/ευ → af/ef before these (unvoiced or word boundary)
UNVOICED = {'κ', 'π', 'τ', 'θ', 'φ', 'χ', 'σ', 'ς', 'ξ', 'ψ'}

# ---------------------------------------------------------------------------
# Core conversion
# ---------------------------------------------------------------------------

def greek_to_phonetic(word: str) -> str:
    """
    Convert a Greek word to hyphenated phonetic notation.
    Stressed syllable is UPPERCASED.
    """
    if not word:
        return ''

    word = unicodedata.normalize('NFC', word.strip())

    # Collect Greek letters: (original_char, base_letter, stressed)
    chars = []
    for c in word:
        if is_greek(c) and unicodedata.category(c).startswith('L'):
            chars.append((c, base(c), has_stress(c)))

    if not chars:
        return ''

    # Build phoneme list: (phoneme_str, is_vowel, is_stressed)
    phonemes = []
    i = 0
    n = len(chars)

    while i < n:
        c0, b0, s0 = chars[i]
        c1, b1, s1 = chars[i+1] if i+1 < n else ('', '', False)
        c2, b2, s2 = chars[i+2] if i+2 < n else ('', '', False)

        # Diphthong helper: next char must NOT carry diaeresis (which splits it)
        def no_diaer_next():
            return c1 and not has_diaeresis(c1)

        # ─── Two-char digraphs / diphthongs ─────────────────────────────────

        # αυ / ευ  →  av/af  ev/ef
        if b0 in ('α', 'ε') and b1 == 'υ' and no_diaer_next():
            root = 'a' if b0 == 'α' else 'e'
            suffix = 'f' if (not b2 or b2 in UNVOICED) else 'v'
            phonemes.append((root + suffix, True, s0 or s1))
            i += 2; continue

        # αι → eh
        if b0 == 'α' and b1 == 'ι' and no_diaer_next():
            phonemes.append(('eh', True, s0 or s1))
            i += 2; continue

        # ει → ee
        if b0 == 'ε' and b1 == 'ι' and no_diaer_next():
            phonemes.append(('ee', True, s0 or s1))
            i += 2; continue

        # οι → ee
        if b0 == 'ο' and b1 == 'ι' and no_diaer_next():
            phonemes.append(('ee', True, s0 or s1))
            i += 2; continue

        # υι → ee
        if b0 == 'υ' and b1 == 'ι' and no_diaer_next():
            phonemes.append(('ee', True, s0 or s1))
            i += 2; continue

        # ου → oo
        if b0 == 'ο' and b1 == 'υ' and no_diaer_next():
            phonemes.append(('oo', True, s0 or s1))
            i += 2; continue

        # ηυ → ee (rare, treat as simple η)
        if b0 == 'η' and b1 == 'υ' and no_diaer_next():
            phonemes.append(('ee', True, s0 or s1))
            i += 2; continue

        # γγ → ng
        if b0 == 'γ' and b1 == 'γ':
            phonemes.append(('ng', False, False))
            i += 2; continue

        # γκ → g (word-initial) or ng (medial)
        if b0 == 'γ' and b1 == 'κ':
            phonemes.append(('g' if i == 0 else 'ng', False, False))
            i += 2; continue

        # μπ → b (initial) or mb (medial)
        if b0 == 'μ' and b1 == 'π':
            phonemes.append(('b' if i == 0 else 'mb', False, False))
            i += 2; continue

        # ντ → d (initial) or nd (medial)
        if b0 == 'ν' and b1 == 'τ':
            phonemes.append(('d' if i == 0 else 'nd', False, False))
            i += 2; continue

        # τζ → dz
        if b0 == 'τ' and b1 == 'ζ':
            phonemes.append(('dz', False, False))
            i += 2; continue

        # τσ → ts
        if b0 == 'τ' and b1 == 'σ':
            phonemes.append(('ts', False, False))
            i += 2; continue

        # ─── Single characters ───────────────────────────────────────────────

        if b0 in VOWEL_MAP:
            phonemes.append((VOWEL_MAP[b0], True, s0))
        elif b0 == 'γ':
            # Palatal (y) before front vowels, else velar (gh)
            phonemes.append(('y' if b1 in FRONT else 'gh', False, False))
        elif b0 in CONS_MAP:
            phonemes.append((CONS_MAP[b0], False, False))
        # else: skip unknown

        i += 1

    if not phonemes:
        return ''

    # ─── Syllabification ─────────────────────────────────────────────────────
    # Onset consonants accumulate; when a vowel is hit, flush onset+vowel as syllable.
    syllables = []   # [[str, stressed_bool], ...]
    onset = []

    for ph, is_v, stressed in phonemes:
        if is_v:
            syl = ''.join(onset) + ph
            syllables.append([syl, stressed])
            onset = []
        else:
            onset.append(ph)

    # Trailing consonants (coda) attach to last syllable
    if onset:
        coda = ''.join(onset)
        if syllables:
            syllables[-1][0] += coda
        else:
            syllables.append([coda, False])

    # Fallback stress (no accent found in word — e.g., enclitics)
    if not any(s for _, s in syllables):
        if len(syllables) == 1:
            syllables[0][1] = True
        elif len(syllables) >= 2:
            syllables[-2][1] = True

    return '-'.join(syl.upper() if stressed else syl for syl, stressed in syllables)


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(path: str, dry_run: bool = False):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        return 0  # skip non-list JSON

    # Determine which field holds the surface word
    is_lexicon = os.path.basename(path) == 'lexicon.json'
    surface_field = 'lemma' if is_lexicon else 'word'

    changed = 0
    for entry in data:
        if not isinstance(entry, dict):
            continue
        surface = entry.get(surface_field, '')
        if not surface:
            continue
        new_ph = greek_to_phonetic(surface)
        if new_ph and entry.get('phonetic') != new_ph:
            entry['phonetic'] = new_ph
            changed += 1

    if changed and not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return changed


# ---------------------------------------------------------------------------
# Spot-check: print some examples before committing
# ---------------------------------------------------------------------------

SPOT_CHECK = [
    'θεοῦ', 'ἡμῶν', 'τοῖς', 'Πάτερ', 'εὐλογητός',
    'ἅγιος', 'κύριος', 'πνεύματος', 'ἁγίου', 'εἰρήνην',
    'ἐκκλησίᾳ', 'αὐτοῦ', 'σωτηρίας', 'δόξα',
]

def run_spot_check():
    print("=== Spot-check phonetic output ===")
    for w in SPOT_CHECK:
        print(f"  {w:20s} → {greek_to_phonetic(w)}")
    print()

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    dry = '--dry-run' in sys.argv

    run_spot_check()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    texts_dir = os.path.join(base_dir, 'texts')

    # Skip backup/old files
    skip_patterns = {'_old', '_backup', 'enhanced_lexicon_backup'}

    total_changed = 0
    for path in sorted(glob.glob(os.path.join(texts_dir, '*.json'))):
        fname = os.path.basename(path)
        if any(p in fname for p in skip_patterns):
            print(f"  SKIP  {fname}")
            continue
        try:
            n = process_file(path, dry_run=dry)
            if n:
                print(f"  {'DRY ' if dry else ''}UPDATED {fname}: {n} entries")
        except Exception as e:
            print(f"  ERROR {fname}: {e}")

    print(f"\nDone. {'(dry run — no files written)' if dry else 'Files updated.'}")
