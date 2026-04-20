#!/usr/bin/env python3
"""
Build comprehensive lexicon.json from all text files.
Extracts all unique lemmas with their data and merges with Strong's information.
"""

import json
from pathlib import Path
from collections import defaultdict

# Text files to process
TEXT_FILES = [
    "annunciation.json",
    "dormition.json", 
    "gladsome_light.json",
    "glory_to_the_father.json",
    "heavenly_king.json",
    "holy_cross.json",
    "it_is_truly_meet.json",
    "jesus_prayer.json",
    "kyrie_eleison.json",
    "lords_prayer.json",
    "nativity_of_christ.json",
    "presentation_christ.json",
    "psalm_50.json",
    "the_creed.json",
    "theotokos_nativity.json",
    "theotokos_presentation.json",
    "to_thee_the_champion_leader.json",
    "transfiguration.json",
    "trisagion.json",
    "troparion_nativity.json",
    "troparion_pascha.json",
    "troparion_theophany.json"
]

def build_comprehensive_lexicon():
    """Build lexicon from all text files."""
    texts_dir = Path("texts")
    
    # Dictionary to store unique lemmas
    lemma_dict = {}
    
    print("Building comprehensive lexicon from all text files...")
    print("="*60)
    
    total_words = 0
    
    for filename in TEXT_FILES:
        filepath = texts_dir / filename
        
        if not filepath.exists():
            print(f"⚠️  Skipping {filename} - not found")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            text_data = json.load(f)
        
        if not isinstance(text_data, list):
            print(f"⚠️  Skipping {filename} - not a word list")
            continue
        
        file_lemmas = 0
        for word_entry in text_data:
            lemma = word_entry.get('lemma')
            
            if not lemma or lemma.strip() == '':
                continue
            
            total_words += 1
            
            # If this lemma hasn't been seen before, add it
            if lemma not in lemma_dict:
                # Create lexicon entry with all available data
                lexicon_entry = {
                    'lemma': lemma,
                    'phonetic': word_entry.get('phonetic', ''),
                    'gloss': word_entry.get('gloss', word_entry.get('liturgical_gloss', '')),
                    'partOfSpeech': word_entry.get('partOfSpeech', ''),
                }
                
                # Add Strong's data if available
                if 'strongs' in word_entry:
                    lexicon_entry['strongs'] = word_entry['strongs']
                    lexicon_entry['canonical_lemma'] = word_entry.get('canonical_lemma', lemma)
                    lexicon_entry['definition'] = word_entry.get('definition', '')
                    lexicon_entry['strongs_translit'] = word_entry.get('strongs_translit', '')
                    lexicon_entry['derivation'] = word_entry.get('derivation', '')
                
                # Track frequency
                lexicon_entry['frequency'] = 1
                lexicon_entry['contexts'] = [filename.replace('.json', '')]
                
                lemma_dict[lemma] = lexicon_entry
                file_lemmas += 1
            else:
                # Update frequency and contexts
                lemma_dict[lemma]['frequency'] += 1
                context = filename.replace('.json', '')
                if context not in lemma_dict[lemma]['contexts']:
                    lemma_dict[lemma]['contexts'].append(context)
                
                # If this entry has Strong's data and the existing doesn't, add it
                if 'strongs' in word_entry and 'strongs' not in lemma_dict[lemma]:
                    lemma_dict[lemma]['strongs'] = word_entry['strongs']
                    lemma_dict[lemma]['canonical_lemma'] = word_entry.get('canonical_lemma', lemma)
                    lemma_dict[lemma]['definition'] = word_entry.get('definition', '')
                    lemma_dict[lemma]['strongs_translit'] = word_entry.get('strongs_translit', '')
                    lemma_dict[lemma]['derivation'] = word_entry.get('derivation', '')
        
        print(f"✓ {filename:40s} - {file_lemmas:3d} unique lemmas")
    
    # Convert to sorted list
    lexicon_list = sorted(lemma_dict.values(), key=lambda x: x.get('frequency', 0), reverse=True)
    
    print("\n" + "="*60)
    print(f"Total words processed: {total_words}")
    print(f"Unique lemmas: {len(lexicon_list)}")
    print(f"Lemmas with Strong's data: {sum(1 for entry in lexicon_list if 'strongs' in entry)}")
    print(f"Lemmas without Strong's: {sum(1 for entry in lexicon_list if 'strongs' not in entry)}")
    
    # Save to lexicon.json
    output_path = Path("texts/lexicon.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lexicon_list, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved comprehensive lexicon to {output_path}")
    
    # Show top 10 most frequent words
    print("\nTop 10 most frequent words:")
    for i, entry in enumerate(lexicon_list[:10], 1):
        strongs_info = f" ({entry.get('strongs', 'no Strong\'s')})" if 'strongs' in entry else ""
        print(f"  {i:2d}. {entry['lemma']:15s} - {entry['frequency']:3d}x {strongs_info}")
    
    return lexicon_list

if __name__ == "__main__":
    build_comprehensive_lexicon()
