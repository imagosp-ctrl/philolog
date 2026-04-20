#!/usr/bin/env python3
"""
Validate and correct all liturgical text files against Strong's Greek Dictionary.
Updates lemmas, adds definitions, and ensures consistency across all text files.
"""

import json
import unicodedata
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.request import urlopen

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

STRONGS_URL = "https://raw.githubusercontent.com/openscriptures/strongs/master/greek/strongs-dictionary.json"
CACHE_FILE = Path(__file__).parent / "strongs_cache.json"

def fetch_strongs_data() -> Dict[str, Any]:
    """Fetch Strong's Greek Dictionary from GitHub or use cache."""
    # Try to use cached data first
    if CACHE_FILE.exists():
        print("📥 Loading Strong's Dictionary from cache...")
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} Strong's entries from cache")
        return data
    
    # Fetch from GitHub
    print("📥 Fetching Strong's Greek Dictionary from GitHub...")
    try:
        with urlopen(STRONGS_URL) as response:
            data = json.loads(response.read().decode('utf-8'))
        print(f"✅ Loaded {len(data)} Strong's entries")
        
        # Cache for future use
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Cached data to {CACHE_FILE}")
        
        return data
    except Exception as e:
        print(f"❌ Error fetching from GitHub: {e}")
        raise

def normalize_greek(text: str) -> str:
    """Remove accents and diacritics from Greek text for matching."""
    # Normalize to NFD (decomposed form) then filter out combining characters
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

def find_strongs_match(lemma: str, strongs_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find matching Strong's entry for a given lemma."""
    if not lemma:
        return None
    
    normalized_lemma = normalize_greek(lemma.lower())
    
    # Try exact match first
    for strongs_num, entry in strongs_data.items():
        if 'lemma' in entry:
            strongs_lemma = entry['lemma']
            if normalize_greek(strongs_lemma.lower()) == normalized_lemma:
                return {**entry, 'strongs': strongs_num}
    
    return None

def validate_and_correct_word(word_entry: Dict[str, Any], strongs_data: Dict[str, Any], 
                               report: List[str]) -> Dict[str, Any]:
    """Validate and correct a single word entry against Strong's."""
    lemma = word_entry.get('lemma', '')
    word = word_entry.get('word', '')
    
    if not lemma:
        report.append(f"  ⚠️  Word '{word}': No lemma found")
        return word_entry
    
    # Find Strong's match
    strongs_match = find_strongs_match(lemma, strongs_data)
    
    if strongs_match:
        # Create corrected entry preserving original structure
        corrected = word_entry.copy()
        
        # Add Strong's data
        corrected['strongs'] = strongs_match['strongs']
        corrected['canonical_lemma'] = strongs_match['lemma']
        
        # Preserve original gloss as liturgical_gloss
        if 'gloss' in corrected:
            corrected['liturgical_gloss'] = corrected['gloss']
        
        # Add Strong's definition
        if 'strongs_def' in strongs_match:
            corrected['definition'] = strongs_match['strongs_def']
        elif 'kjv_def' in strongs_match:
            corrected['definition'] = strongs_match['kjv_def']
        
        # Add transliteration
        if 'translit' in strongs_match:
            corrected['strongs_translit'] = strongs_match['translit']
        
        # Add derivation
        if 'derivation' in strongs_match:
            corrected['derivation'] = strongs_match['derivation']
        
        # Check if lemma needs correction
        if lemma != strongs_match['lemma']:
            report.append(f"  ✓ '{word}' (lemma: {lemma} → {strongs_match['lemma']}) - {strongs_match['strongs']}")
        else:
            report.append(f"  ✓ '{word}' (lemma: {lemma}) - {strongs_match['strongs']}")
        
        return corrected
    else:
        report.append(f"  ⚠️  '{word}' (lemma: {lemma}): No Strong's match found")
        return word_entry

def process_text_file(filepath: Path, strongs_data: Dict[str, Any]) -> tuple[List[Dict[str, Any]], List[str]]:
    """Process a single text file and return corrected data and report."""
    print(f"\n📖 Processing {filepath.name}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text_data = json.load(f)
    
    report = [f"\n{'='*70}", f"FILE: {filepath.name}", f"{'='*70}"]
    
    if not isinstance(text_data, list):
        report.append("⚠️  ERROR: File is not a list of word entries")
        return text_data, report
    
    corrected_words = []
    matched_count = 0
    unmatched_count = 0
    
    for word_entry in text_data:
        corrected = validate_and_correct_word(word_entry, strongs_data, report)
        corrected_words.append(corrected)
        
        if 'strongs' in corrected:
            matched_count += 1
        else:
            unmatched_count += 1
    
    report.append(f"\n📊 Summary: {len(text_data)} words | ✅ {matched_count} matched | ⚠️  {unmatched_count} unmatched")
    
    return corrected_words, report

def main():
    """Main execution function."""
    print("="*70)
    print("PHILOLOG TEXT FILES VALIDATION AND CORRECTION")
    print("="*70)
    
    # Setup paths
    texts_dir = Path(__file__).parent / "texts"
    output_dir = texts_dir / "corrected"
    output_dir.mkdir(exist_ok=True)
    
    # Fetch Strong's data once
    strongs_data = fetch_strongs_data()
    
    # Process all text files
    all_reports = []
    summary_stats = {
        'total_files': 0,
        'total_words': 0,
        'total_matched': 0,
        'total_unmatched': 0
    }
    
    for filename in TEXT_FILES:
        filepath = texts_dir / filename
        
        if not filepath.exists():
            print(f"⚠️  Skipping {filename} - file not found")
            continue
        
        try:
            corrected_data, report = process_text_file(filepath, strongs_data)
            
            # Save corrected file
            output_filepath = output_dir / filename
            with open(output_filepath, 'w', encoding='utf-8') as f:
                json.dump(corrected_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Saved corrected version to {output_filepath}")
            
            # Update statistics
            summary_stats['total_files'] += 1
            summary_stats['total_words'] += len(corrected_data)
            summary_stats['total_matched'] += sum(1 for w in corrected_data if 'strongs' in w)
            summary_stats['total_unmatched'] += sum(1 for w in corrected_data if 'strongs' not in w)
            
            all_reports.extend(report)
            
        except Exception as e:
            error_msg = f"❌ ERROR processing {filename}: {str(e)}"
            print(error_msg)
            all_reports.append(error_msg)
    
    # Generate comprehensive report
    report_path = Path(__file__).parent / "text_files_validation_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("PHILOLOG TEXT FILES VALIDATION REPORT\n")
        f.write("="*70 + "\n\n")
        f.write(f"Files Processed: {summary_stats['total_files']}\n")
        f.write(f"Total Words: {summary_stats['total_words']}\n")
        f.write(f"Matched to Strong's: {summary_stats['total_matched']}\n")
        f.write(f"Unmatched: {summary_stats['total_unmatched']}\n")
        f.write(f"Match Rate: {summary_stats['total_matched']/summary_stats['total_words']*100:.1f}%\n")
        f.write("\n" + "="*70 + "\n")
        f.write("\nDETAILED FILE REPORTS:\n")
        f.write("\n".join(all_reports))
    
    print("\n" + "="*70)
    print("📊 FINAL SUMMARY")
    print("="*70)
    print(f"Files Processed: {summary_stats['total_files']}")
    print(f"Total Words: {summary_stats['total_words']}")
    print(f"✅ Matched to Strong's: {summary_stats['total_matched']}")
    print(f"⚠️  Unmatched: {summary_stats['total_unmatched']}")
    print(f"Match Rate: {summary_stats['total_matched']/summary_stats['total_words']*100:.1f}%")
    print(f"\n📄 Detailed report saved to: {report_path}")
    print(f"📁 Corrected files saved to: {output_dir}/")
    print("\n✅ Validation complete!")

if __name__ == "__main__":
    main()
