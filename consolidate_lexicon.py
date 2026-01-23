#!/usr/bin/env python3
"""
Script to consolidate all vocabulary from text files into lexicon.json
Ensures all words from liturgical texts are included in the main lexicon
"""

import json
import os
import unicodedata

def greek_to_latin_transliteration(greek_text):
    """Convert Greek text to Latin transliteration"""
    char_map = {
        'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'e', 'θ': 'th',
        'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p',
        'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'u', 'φ': 'ph', 'χ': 'ch', 'ψ': 'ps', 'ω': 'o',
        'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'E', 'Θ': 'Th',
        'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X', 'Ο': 'O', 'Π': 'P',
        'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'U', 'Φ': 'Ph', 'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'O'
    }
    
    # Normalize Unicode (remove accents)
    normalized = unicodedata.normalize('NFD', greek_text)
    no_accents = ''.join(c for c in normalized if not unicodedata.combining(c))
    
    # Apply character mapping
    result = ""
    for char in no_accents:
        result += char_map.get(char, char)
    
    return result.lower()

def load_json_file(filepath):
    """Load a JSON file and return its contents"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found, skipping...")
        return []
    except json.JSONDecodeError:
        print(f"Warning: {filepath} has invalid JSON format, skipping...")
        return []

def main():
    # Text files to check
    text_files = [
        'annunciation.json',
        'dormition.json',
        'gladsome_light.json',
        'glory_to_the_father.json', 
        'heavenly_king.json',
        'holy_cross.json',
        'it_is_truly_meet.json',
        'jesus_prayer.json',
        'kyrie_eleison.json',
        'lords_prayer.json',
        'nativity_of_christ.json',
        'presentation_christ.json',
        'psalm_50.json',
        'the_creed.json',
        'theotokos_nativity.json',
        'theotokos_presentation.json',
        'to_thee_the_champion_leader.json',
        'transfiguration.json',
        'trisagion.json',
        'troparion_nativity.json',
        'troparion_pascha.json',
        'troparion_theophany.json'
    ]
    
    # Load existing lexicon
    print("Loading existing lexicon...")
    lexicon_data = load_json_file('texts/lexicon.json')
    existing_lemmas = {entry.get('lemma', entry.get('word', '')).lower() for entry in lexicon_data}
    print(f"Existing lexicon has {len(lexicon_data)} entries")
    
    # Collect all vocabulary from text files
    print("\nScanning text files for vocabulary...")
    all_vocabulary = {}
    
    for filename in text_files:
        filepath = f'texts/{filename}'
        print(f"Processing {filename}...")
        
        data = load_json_file(filepath)
        if not data:
            continue
            
        # Handle different file structures
        if isinstance(data, dict) and 'words' in data:
            # File has structure like {"words": [...]}
            words = data['words']
        elif isinstance(data, list):
            # File is directly a list of words
            words = data
        else:
            print(f"Warning: Unexpected structure in {filename}")
            continue
            
        file_count = 0
        for entry in words:
            if not isinstance(entry, dict) or 'word' not in entry:
                continue
                
            lemma = entry.get('lemma', entry['word']).lower()
            
            # Only add if not already in existing lexicon
            if lemma not in existing_lemmas and lemma not in all_vocabulary:
                # Add searchKey if missing
                if 'searchKey' not in entry:
                    entry['searchKey'] = greek_to_latin_transliteration(entry['word'])
                
                all_vocabulary[lemma] = entry
                file_count += 1
        
        print(f"  Found {file_count} new entries in {filename}")
    
    # Add new entries to lexicon
    new_entries = list(all_vocabulary.values())
    if new_entries:
        print(f"\nAdding {len(new_entries)} new entries to lexicon...")
        lexicon_data.extend(new_entries)
        
        # Sort by lemma
        lexicon_data.sort(key=lambda x: x.get('lemma', x.get('word', '')).lower())
        
        # Save updated lexicon
        with open('texts/lexicon.json', 'w', encoding='utf-8') as f:
            json.dump(lexicon_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Successfully updated lexicon.json with {len(new_entries)} new entries")
        print(f"Total entries in lexicon: {len(lexicon_data)}")
        
        # Show sample of new entries
        print("\nSample of new entries added:")
        for entry in new_entries[:5]:
            word = entry.get('word', '')
            gloss = entry.get('gloss', '')
            pos = entry.get('partOfSpeech', '')
            print(f"  {word} → {gloss} ({pos})")
            
    else:
        print("✅ All vocabulary from text files is already in lexicon.json")
        print("No updates needed!")

if __name__ == "__main__":
    main()