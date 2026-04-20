#!/usr/bin/env python3
"""
Lexicon Validation and Correction Script
Compares Philolog lexicon against Strong's Greek Dictionary
and corrects any inaccuracies while preserving custom data.

Usage: python3 validate_and_correct_lexicon.py
"""

import json
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple

# Paths
LEXICON_PATH = Path("texts/lexicon.json")
ENHANCED_LEXICON_PATH = Path("texts/enhanced_lexicon.json")
STRONGS_URL = "https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-greek-dictionary.js"
OUTPUT_PATH = Path("texts/lexicon_corrected.json")
REPORT_PATH = Path("lexicon_correction_report.txt")

def fetch_strongs_data() -> Dict:
    """Download and parse Strong's Greek Dictionary from GitHub."""
    print("Fetching Strong's Greek Dictionary from GitHub...")
    try:
        with urllib.request.urlopen(STRONGS_URL, timeout=30) as response:
            js_content = response.read().decode('utf-8')
        
        # Extract JSON from JavaScript variable declaration
        # Remove the variable declaration and module.exports
        json_start = js_content.find('{')
        json_end = js_content.rfind('}') + 1
        json_str = js_content[json_start:json_end]
        
        strongs_dict = json.loads(json_str)
        print(f"✓ Successfully loaded {len(strongs_dict)} Strong's entries")
        return strongs_dict
    except Exception as e:
        print(f"✗ Error fetching Strong's data: {e}")
        sys.exit(1)

def load_lexicon(path: Path) -> List:
    """Load existing Philolog lexicon."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded {len(data)} entries from {path.name}")
        return data
    except FileNotFoundError:
        print(f"✗ Lexicon file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in {path}: {e}")
        sys.exit(1)

def normalize_greek(text: str) -> str:
    """Normalize Greek text for comparison (remove accents/breathing marks)."""
    # This is a simple normalization - you may need more sophisticated handling
    import unicodedata
    # Decompose to separate base characters from diacritics
    decomposed = unicodedata.normalize('NFD', text)
    # Filter out combining characters (accents, breathing marks)
    base = ''.join(c for c in decomposed if not unicodedata.combining(c))
    return base.lower().strip()

def find_strongs_match(greek_word: str, strongs_dict: Dict) -> Tuple[str, Dict]:
    """
    Find the matching Strong's entry for a Greek word.
    Returns (strongs_number, entry_data) or (None, None) if not found.
    """
    normalized_word = normalize_greek(greek_word)
    
    for strongs_num, entry in strongs_dict.items():
        if 'lemma' in entry:
            if normalize_greek(entry['lemma']) == normalized_word:
                return strongs_num, entry
    
    return None, None

def validate_and_correct_entry(
    word: str,
    philolog_entry: Dict,
    strongs_dict: Dict
) -> Tuple[Dict, List[str]]:
    """
    Validate a Philolog lexicon entry against Strong's and correct if needed.
    Returns (corrected_entry, list_of_changes)
    """
    changes = []
    corrected = philolog_entry.copy()
    
    # Find matching Strong's entry
    strongs_num, strongs_entry = find_strongs_match(word, strongs_dict)
    
    if strongs_num is None:
        changes.append(f"⚠️  No Strong's match found for '{word}'")
        return corrected, changes
    
    # Store Strong's number for reference
    corrected['strongs'] = strongs_num
    changes.append(f"✓ Matched to Strong's {strongs_num}")
    
    # Validate and correct lemma
    if 'lemma' in strongs_entry:
        strongs_lemma = strongs_entry['lemma']
        if word != strongs_lemma and normalize_greek(word) == normalize_greek(strongs_lemma):
            changes.append(f"  Lemma: '{word}' → '{strongs_lemma}' (corrected spelling/accents)")
            # Note: We keep the original word as the key, but record the canonical form
            corrected['canonical_lemma'] = strongs_lemma
    
    # Validate and correct transliteration
    if 'translit' in strongs_entry:
        strongs_translit = strongs_entry['translit']
        philolog_translit = philolog_entry.get('pronunciation', philolog_entry.get('transliteration', ''))
        
        if philolog_translit and philolog_translit != strongs_translit:
            # Keep liturgical pronunciation, but add Strong's transliteration for reference
            corrected['strongs_translit'] = strongs_translit
            changes.append(f"  Note: Pronunciation differs - Kept: '{philolog_translit}', Strong's: '{strongs_translit}'")
    
    # Validate and correct definition
    if 'strongs_def' in strongs_entry or 'kjv_def' in strongs_entry:
        strongs_def = strongs_entry.get('strongs_def', strongs_entry.get('kjv_def', ''))
        philolog_def = philolog_entry.get('gloss', philolog_entry.get('definition', ''))
        
        if strongs_def and strongs_def != philolog_def:
            # Update definition but preserve original as 'liturgical_gloss' if different
            if philolog_def:
                corrected['liturgical_gloss'] = philolog_def
            corrected['definition'] = strongs_def
            changes.append(f"  Definition updated: '{philolog_def[:50]}...' → '{strongs_def[:50]}...'")
    
    # Add derivation if available
    if 'derivation' in strongs_entry:
        corrected['derivation'] = strongs_entry['derivation']
        changes.append(f"  Added derivation info")
    
    return corrected, changes

def validate_lexicon(philolog_lex: List, strongs_dict: Dict) -> Tuple[List, Dict]:
    """
    Validate entire lexicon and generate correction report.
    Returns (corrected_lexicon, report_data)
    """
    corrected_lexicon = []
    report_data = {
        'total_entries': len(philolog_lex),
        'matched': 0,
        'unmatched': 0,
        'corrected': 0,
        'unchanged': 0,
        'details': []
    }
    
    print("\nValidating and correcting lexicon entries...")
    print("=" * 70)
    
    for entry in philolog_lex:
        word = entry.get('lemma', '')
        if not word:
            continue
            
        corrected_entry, changes = validate_and_correct_entry(word, entry, strongs_dict)
        corrected_lexicon.append(corrected_entry)
        
        if changes:
            report_entry = {
                'word': word,
                'changes': changes
            }
            report_data['details'].append(report_entry)
            
            # Print progress
            print(f"\n{word}:")
            for change in changes:
                print(f"  {change}")
            
            if any('No Strong\'s match' in c for c in changes):
                report_data['unmatched'] += 1
            elif any('corrected' in c or 'updated' in c or 'Added' in c for c in changes):
                report_data['corrected'] += 1
                report_data['matched'] += 1
            else:
                report_data['matched'] += 1
                report_data['unchanged'] += 1
    
    return corrected_lexicon, report_data

def generate_report(report_data: Dict, output_path: Path):
    """Generate a human-readable correction report."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("PHILOLOG LEXICON VALIDATION AND CORRECTION REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total entries processed: {report_data['total_entries']}\n")
        f.write(f"Matched to Strong's: {report_data['matched']}\n")
        f.write(f"Not found in Strong's: {report_data['unmatched']}\n")
        f.write(f"Corrected: {report_data['corrected']}\n")
        f.write(f"Unchanged (already correct): {report_data['unchanged']}\n")
        f.write("\n" + "=" * 70 + "\n\n")
        
        f.write("DETAILED CHANGES:\n\n")
        for detail in report_data['details']:
            f.write(f"{detail['word']}:\n")
            for change in detail['changes']:
                f.write(f"  {change}\n")
            f.write("\n")
    
    print(f"\n✓ Detailed report saved to: {output_path}")

def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("PHILOLOG LEXICON VALIDATION & CORRECTION")
    print("=" * 70 + "\n")
    
    # Step 1: Fetch Strong's data
    strongs_dict = fetch_strongs_data()
    
    # Step 2: Load Philolog lexicon (try both possible files)
    if ENHANCED_LEXICON_PATH.exists():
        philolog_lex = load_lexicon(ENHANCED_LEXICON_PATH)
    elif LEXICON_PATH.exists():
        philolog_lex = load_lexicon(LEXICON_PATH)
    else:
        print(f"✗ No lexicon file found")
        sys.exit(1)
    
    # Step 3: Validate and correct
    corrected_lexicon, report_data = validate_lexicon(philolog_lex, strongs_dict)
    
    # Step 4: Save corrected lexicon
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(corrected_lexicon, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Corrected lexicon saved to: {OUTPUT_PATH}")
    
    # Step 5: Generate report
    generate_report(report_data, REPORT_PATH)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total entries: {report_data['total_entries']}")
    print(f"✓ Matched: {report_data['matched']}")
    print(f"⚠️  Unmatched: {report_data['unmatched']}")
    print(f"📝 Corrected: {report_data['corrected']}")
    print(f"✅ Already correct: {report_data['unchanged']}")
    print("\nNext steps:")
    print(f"1. Review the report: {REPORT_PATH}")
    print(f"2. Verify corrections: {OUTPUT_PATH}")
    print(f"3. If satisfied, replace your lexicon with the corrected version")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
