#!/usr/bin/env python3
"""
Script to add Latin transliteration searchKey fields to lexicon.json
This enables dual-language search in the lexicon (Greek and Latin notation)
"""

import json
import unicodedata

def greek_to_latin_transliteration(greek_text):
    """Convert Greek text to Latin transliteration"""
    # Greek to Latin character mapping
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

def main():
    # Load lexicon.json
    with open('texts/lexicon.json', 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
    
    count = 0
    # Add searchKey to each entry
    for entry in lexicon_data:
        if 'word' in entry:
            entry['searchKey'] = greek_to_latin_transliteration(entry['word'])
            count += 1
    
    # Save updated lexicon
    with open('texts/lexicon.json', 'w', encoding='utf-8') as f:
        json.dump(lexicon_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully added searchKey fields to {count} entries")
    print("Examples:")
    for i, entry in enumerate(lexicon_data[:5]):
        if 'word' in entry and 'searchKey' in entry:
            print(f"  {entry['word']} → {entry['searchKey']}")

if __name__ == "__main__":
    main()