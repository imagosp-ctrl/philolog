#!/usr/bin/env python3
"""
Convert Psalm 69 from old tokens format to new words format with Strong's data.
"""

import json
import urllib.request
import unicodedata
from pathlib import Path

# Color mapping for parts of speech
POS_COLORS = {
    'noun': 'blue',
    'verb': 'gold',
    'adjective': 'lavender',
    'adverb': 'lavender',
    'preposition': 'green',
    'article': 'grey',
    'conjunction': 'grey',
    'pronoun': 'blue',
    'participle': 'gold',
    'particle': 'grey',
    'punct': 'black',
    'punctuation': 'black'
}

def load_strongs_cache():
    """Load cached Strong's data."""
    cache_file = Path('strongs_cache.json')
    if cache_file.exists():
        print("📚 Loading Strong's dictionary from cache...")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def normalize_greek(text):
    """Remove accents and diacritics from Greek text."""
    if not text:
        return text
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

def find_strongs_match(lemma, strongs_dict):
    """Find matching Strong's entry for a lemma. Returns (strongs_number, entry) tuple."""
    if not lemma:
        return None, None
    
    normalized_lemma = normalize_greek(lemma.lower().strip())
    
    for strongs_num, entry in strongs_dict.items():
        if 'lemma' in entry:
            entry_lemma = normalize_greek(entry['lemma'].lower().strip())
            if entry_lemma == normalized_lemma:
                return strongs_num, entry
    
    return None, None

def get_english_gloss(lemma, pos):
    """Provide English glosses for common liturgical words."""
    glosses = {
        ('ὁ', 'article'): 'the',
        ('θεός', 'noun'): 'God',
        ('εἰς', 'preposition'): 'to',
        ('βοήθεια', 'noun'): 'help',
        ('ἐγώ', 'pronoun'): 'my/me/I',
        ('προσέχω', 'verb'): 'attend',
        ('κύριος', 'noun'): 'Lord',
        ('βοηθέω', 'verb'): 'to help',
        ('σπεύδω', 'verb'): 'hasten',
        ('αἰσχύνω', 'verb'): 'be ashamed',
        ('καί', 'conjunction'): 'and',
        ('ἐντρέπω', 'verb'): 'be put to shame',
        ('ζητέω', 'participle'): 'seeking',
        ('ψυχή', 'noun'): 'soul',
        ('ἀποστρέφω', 'verb'): 'turn back',
        ('ὀπίσω', 'adverb'): 'backward',
        ('καταισχύνω', 'verb'): 'be dishonored',
        ('βούλομαι', 'participle'): 'wishing',
        ('κακός', 'adjective'): 'evil',
        ('παραυτίκα', 'adverb'): 'immediately',
        ('λέγω', 'participle'): 'saying',
        ('λέγω', 'verb'): 'let them say',
        ('εὖγε', 'particle'): 'well done',
        ('ἀγαλλιάω', 'verb'): 'rejoice',
        ('εὐφραίνω', 'verb'): 'be glad',
        ('ἐπί', 'preposition'): 'in/upon',
        ('σύ', 'pronoun'): 'you',
        ('πᾶς', 'adjective'): 'all',
        ('διαπαντός', 'adverb'): 'continually',
        ('μεγαλύνω', 'verb'): 'be magnified',
        ('ἀγαπάω', 'participle'): 'loving',
        ('σωτήριον', 'noun'): 'salvation',
        ('δέ', 'particle'): 'but',
        ('πτωχός', 'adjective'): 'poor',
        ('εἰμί', 'verb'): 'am/are',
        ('πένης', 'adjective'): 'needy',
        ('βοηθός', 'noun'): 'helper',
        ('ῥύστης', 'noun'): 'deliverer',
        ('μή', 'particle'): 'not',
        ('χρονίζω', 'verb'): 'delay'
    }
    
    key = (normalize_greek(lemma), pos)
    for (norm_lemma, norm_pos), gloss in glosses.items():
        if normalize_greek(norm_lemma) == key[0] and norm_pos == key[1]:
            return gloss
    
    return lemma  # Fallback

def convert_psalm_69():
    """Convert Psalm 69 from old format to new format."""
    
    # Load old psalms.json
    print("📖 Loading old psalms.json...")
    with open('texts/psalms.json', 'r', encoding='utf-8') as f:
        old_psalms = json.load(f)
    
    # Find Psalm 69
    psalm_69 = None
    for psalm in old_psalms:
        if psalm.get('number') == 69:
            psalm_69 = psalm
            break
    
    if not psalm_69:
        print("❌ Psalm 69 not found in psalms.json")
        return
    
    print(f"✅ Found Psalm 69 with {len(psalm_69['tokens'])} tokens")
    
    # Load Strong's dictionary
    strongs_dict = load_strongs_cache()
    print(f"📚 Loaded {len(strongs_dict)} Strong's entries")
    
    # Convert tokens to new format
    words = []
    matched_count = 0
    unmatched_words = []
    
    for token in psalm_69['tokens']:
        word_text = token.get('t', '')
        lemma = token.get('lemma', '')
        pos = token.get('pos', '')
        
        if pos == 'punct':
            # Skip punctuation - it's embedded in the word text
            continue
        
        # Find Strong's match
        strongs_num, strongs_entry = find_strongs_match(lemma, strongs_dict)
        
        # Create word object
        word_obj = {
            'word': word_text,
            'phonetic': '',  # We don't have phonetic in old format
            'lemma': lemma,
            'gloss': get_english_gloss(lemma, pos),
            'partOfSpeech': pos,
            'colorCode': POS_COLORS.get(pos, 'black')
        }
        
        # Add Strong's data if found
        if strongs_entry and strongs_num:
            word_obj['strongs'] = strongs_num
            word_obj['canonical_lemma'] = strongs_entry.get('lemma', lemma)
            word_obj['liturgical_gloss'] = word_obj['gloss']
            word_obj['definition'] = strongs_entry.get('strongs_def', strongs_entry.get('kjv_def', ''))
            word_obj['strongs_translit'] = strongs_entry.get('translit', '')
            word_obj['derivation'] = strongs_entry.get('derivation', '')
            matched_count += 1
        else:
            word_obj['liturgical_gloss'] = word_obj['gloss']
            unmatched_words.append(f"{word_text} ({lemma}, {pos})")
        
        words.append(word_obj)
    
    # Save to new file
    output_file = Path('texts/psalm_69.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Created {output_file} with {len(words)} words")
    print(f"✅ {matched_count} words matched to Strong's ({matched_count/len(words)*100:.1f}%)")
    
    if unmatched_words:
        print(f"⚠️  {len(unmatched_words)} words without Strong's match:")
        for word in unmatched_words[:10]:
            print(f"    - {word}")
        if len(unmatched_words) > 10:
            print(f"    ... and {len(unmatched_words) - 10} more")

if __name__ == '__main__':
    convert_psalm_69()
