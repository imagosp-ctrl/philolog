#!/usr/bin/env python3
"""
Create Psalm 103 (LXX) - "Bless the Lord, O my soul"
Used at Vespers
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
    'particle': 'grey',
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

def create_word_entry(word, lemma, gloss, pos, phonetic, strongs_dict):
    """Create a word entry with Strong's data if available."""
    strongs_num, strongs_entry = find_strongs_match(lemma, strongs_dict)
    
    word_obj = {
        'word': word,
        'phonetic': phonetic,
        'lemma': lemma,
        'gloss': gloss,
        'partOfSpeech': pos,
        'colorCode': POS_COLORS.get(pos, 'black')
    }
    
    if strongs_entry and strongs_num:
        word_obj['strongs'] = strongs_num
        word_obj['canonical_lemma'] = strongs_entry.get('lemma', lemma)
        word_obj['liturgical_gloss'] = gloss
        word_obj['definition'] = strongs_entry.get('strongs_def', strongs_entry.get('kjv_def', ''))
        word_obj['strongs_translit'] = strongs_entry.get('translit', '')
        word_obj['derivation'] = strongs_entry.get('derivation', '')
    else:
        word_obj['liturgical_gloss'] = gloss
    
    return word_obj

def create_psalm_103():
    """Create Psalm 103 JSON file."""
    print("Creating Psalm 103 (LXX 103 / Masoretic 104)...")
    print("'Bless the Lord, O my soul' - Used at Vespers")
    
    # Load Strong's dictionary
    strongs_dict = load_strongs_cache()
    
    # Psalm 103 text with parsing
    # Format: (word, lemma, gloss, pos, phonetic)
    psalm_words = [
        ('Εὐλόγει,', 'εὐλογέω', 'Bless', 'verb', 'ev-LOH-yee'),
        ('ἡ', 'ὁ', 'O', 'article', 'ee'),
        ('ψυχή', 'ψυχή', 'soul', 'noun', 'psee-KHEE'),
        ('μου,', 'ἐγώ', 'my', 'pronoun', 'moo'),
        ('τὸν', 'ὁ', 'the', 'article', 'ton'),
        ('Κύριον.', 'κύριος', 'Lord.', 'noun', 'KEE-ree-on'),
        
        ('Κύριε', 'κύριος', 'O Lord', 'noun', 'KEE-ree-eh'),
        ('ὁ', 'ὁ', 'the', 'article', 'ho'),
        ('Θεός', 'θεός', 'God', 'noun', 'theh-OS'),
        ('μου', 'ἐγώ', 'my', 'pronoun', 'moo'),
        ('ἐμεγαλύνθης', 'μεγαλύνω', 'You are magnified', 'verb', 'eh-meh-gah-LEEN-thees'),
        ('σφόδρα.', 'σφόδρα', 'exceedingly.', 'adverb', 'SFOH-drah'),
        
        ('Ἐξομολόγησιν', 'ἐξομολόγησις', 'Confession', 'noun', 'ex-o-mo-LOH-yee-sin'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('μεγαλοπρέπειαν', 'μεγαλοπρέπεια', 'majesty', 'noun', 'meh-gah-lo-PREH-pee-an'),
        ('ἐνεδύσω,', 'ἐνδύω', 'You have clothed Yourself,', 'verb', 'eh-neh-DEE-so'),
        
        ('ἀναβαλλόμενος', 'ἀναβάλλω', 'wrapping Yourself', 'verb', 'ah-nah-bah-LOH-meh-nos'),
        ('φῶς', 'φῶς', 'light', 'noun', 'fohs'),
        ('ὡς', 'ὡς', 'as', 'conjunction', 'ohs'),
        ('ἱμάτιον.', 'ἱμάτιον', 'a garment.', 'noun', 'hee-MAH-tee-on'),
        
        ('Ἐκτείνων', 'ἐκτείνω', 'Stretching out', 'verb', 'ek-TEE-nohn'),
        ('τὸν', 'ὁ', 'the', 'article', 'ton'),
        ('οὐρανὸν', 'οὐρανός', 'heaven', 'noun', 'oo-rah-NON'),
        ('ὡσεὶ', 'ὡσεί', 'like', 'particle', 'ho-SEE'),
        ('δέῤῥιν,', 'δέῤῥις', 'a hide,', 'noun', 'DEHR-reen'),
        
        ('ὁ', 'ὁ', 'the One', 'article', 'ho'),
        ('στεγάζων', 'στεγάζω', 'covering', 'verb', 'steh-GAH-zohn'),
        ('ἐν', 'ἐν', 'with', 'preposition', 'en'),
        ('ὕδασι', 'ὕδωρ', 'waters', 'noun', 'EE-dah-see'),
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('ὑπερῷα', 'ὑπερῷον', 'upper chambers', 'noun', 'ee-peh-ROH-ah'),
        ('αὐτοῦ.', 'αὐτός', 'His.', 'pronoun', 'af-TOO'),
        
        ('Ὁ', 'ὁ', 'The One', 'article', 'ho'),
        ('τιθεὶς', 'τίθημι', 'making', 'verb', 'tee-THEES'),
        ('νέφη', 'νέφος', 'clouds', 'noun', 'NEH-fee'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('ἐπίβασιν', 'ἐπίβασις', 'ascent', 'noun', 'eh-PEE-bah-sin'),
        ('αὐτοῦ,', 'αὐτός', 'His,', 'pronoun', 'af-TOO'),
        
        ('ὁ', 'ὁ', 'the One', 'article', 'ho'),
        ('περιπατῶν', 'περιπατέω', 'walking', 'verb', 'peh-ree-pah-TOHN'),
        ('ἐπὶ', 'ἐπί', 'upon', 'preposition', 'eh-PEE'),
        ('πτερύγων', 'πτέρυξ', 'wings', 'noun', 'pteh-REE-gohn'),
        ('ἀνέμων.', 'ἄνεμος', 'of winds.', 'noun', 'ah-NEH-mohn'),
        
        ('Ὁ', 'ὁ', 'The One', 'article', 'ho'),
        ('ποιῶν', 'ποιέω', 'making', 'verb', 'pee-OHN'),
        ('τοὺς', 'ὁ', 'the', 'article', 'toos'),
        ('Ἀγγέλους', 'ἄγγελος', 'Angels', 'noun', 'AHN-geh-loos'),
        ('αὐτοῦ', 'αὐτός', 'His', 'pronoun', 'af-TOO'),
        ('πνεύματα,', 'πνεῦμα', 'spirits,', 'noun', 'PNEV-mah-tah'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('τοὺς', 'ὁ', 'the', 'article', 'toos'),
        ('λειτουργοὺς', 'λειτουργός', 'ministers', 'noun', 'lee-toor-GOOS'),
        ('αὐτοῦ', 'αὐτός', 'His', 'pronoun', 'af-TOO'),
        ('πυρὸς', 'πῦρ', 'of fire', 'noun', 'pee-ROS'),
        ('φλόγα.', 'φλόξ', 'a flame.', 'noun', 'FLOH-gah'),
        
        ('Ὁ', 'ὁ', 'The One', 'article', 'ho'),
        ('θεμελιῶν', 'θεμελιόω', 'founding', 'verb', 'theh-meh-lee-OHN'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('γῆν', 'γῆ', 'earth', 'noun', 'geen'),
        ('ἐπὶ', 'ἐπί', 'upon', 'preposition', 'eh-PEE'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('ἀσφάλειαν', 'ἀσφάλεια', 'stability', 'noun', 'as-FAH-lee-an'),
        ('αὐτῆς,', 'αὐτός', 'its,', 'pronoun', 'af-TEES'),
        
        ('οὐ', 'οὐ', 'not', 'particle', 'oo'),
        ('κλιθήσεται', 'κλίνω', 'it shall be moved', 'verb', 'klee-THEE-seh-teh'),
        ('εἰς', 'εἰς', 'unto', 'preposition', 'ees'),
        ('τὸν', 'ὁ', 'the', 'article', 'ton'),
        ('αἰῶνα', 'αἰών', 'age', 'noun', 'eh-OH-nah'),
        ('τοῦ', 'ὁ', 'of the', 'article', 'too'),
        ('αἰῶνος.', 'αἰών', 'age.', 'noun', 'eh-OH-nos'),
        
        ('Ἄβυσσος', 'ἄβυσσος', 'The deep', 'noun', 'AH-bees-sos'),
        ('ὡς', 'ὡς', 'as', 'conjunction', 'ohs'),
        ('ἱμάτιον', 'ἱμάτιον', 'a garment', 'noun', 'hee-MAH-tee-on'),
        ('τὸ', 'ὁ', 'the', 'article', 'to'),
        ('περιβόλαιον', 'περιβόλαιον', 'covering', 'noun', 'peh-ree-BOH-leh-on'),
        ('αὐτοῦ,', 'αὐτός', 'of it,', 'pronoun', 'af-TOO'),
        
        ('ἐπὶ', 'ἐπί', 'upon', 'preposition', 'eh-PEE'),
        ('τῶν', 'ὁ', 'the', 'article', 'tohn'),
        ('ὀρέων', 'ὄρος', 'mountains', 'noun', 'oh-REH-ohn'),
        ('στήσονται', 'ἵστημι', 'shall stand', 'verb', 'STEE-son-teh'),
        ('ὕδατα.', 'ὕδωρ', 'waters.', 'noun', 'EE-dah-tah'),
        
        ('Ἀπὸ', 'ἀπό', 'At', 'preposition', 'ah-POH'),
        ('ἐπιτιμήσεώς', 'ἐπιτίμησις', 'rebuke', 'noun', 'eh-pee-tee-MEE-seh-os'),
        ('σου', 'σύ', 'Your', 'pronoun', 'soo'),
        ('φεύξονται,', 'φεύγω', 'they shall flee,', 'verb', 'FEFK-son-teh'),
        
        ('ἀπὸ', 'ἀπό', 'at', 'preposition', 'ah-POH'),
        ('φωνῆς', 'φωνή', 'voice', 'noun', 'foh-NEES'),
        ('βροντῆς', 'βροντή', 'of thunder', 'noun', 'bron-TEES'),
        ('σου', 'σύ', 'Your', 'pronoun', 'soo'),
        ('δειλιάσουσιν.', 'δειλιάω', 'they shall be afraid.', 'verb', 'dee-lee-AH-soo-sin'),
        
        ('Ἀναβαίνουσιν', 'ἀναβαίνω', 'They go up', 'verb', 'ah-nah-BEH-noo-sin'),
        ('ὄρη,', 'ὄρος', 'mountains,', 'noun', 'OH-ree'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('καταβαίνουσι', 'καταβαίνω', 'go down', 'verb', 'kah-tah-BEH-noo-see'),
        ('πεδία', 'πεδίον', 'plains', 'noun', 'peh-DEE-ah'),
        
        ('εἰς', 'εἰς', 'to', 'preposition', 'ees'),
        ('τὸν', 'ὁ', 'the', 'article', 'ton'),
        ('τόπον,', 'τόπος', 'place,', 'noun', 'TOH-pon'),
        ('ὃν', 'ὅς', 'which', 'pronoun', 'hon'),
        ('ἐθεμελίωσας', 'θεμελιόω', 'You founded', 'verb', 'eh-theh-meh-LEE-oh-sahs'),
        ('αὐτά.', 'αὐτός', 'them.', 'pronoun', 'af-TAH'),
        
        ('Ὅριον', 'ὅριον', 'A boundary', 'noun', 'HOH-ree-on'),
        ('ἔθου,', 'τίθημι', 'You set,', 'verb', 'EH-thoo'),
        ('ὃ', 'ὅς', 'which', 'pronoun', 'ho'),
        ('οὐ', 'οὐ', 'not', 'particle', 'oo'),
        ('παρελεύσονται,', 'παρέρχομαι', 'they shall pass,', 'verb', 'pah-reh-LEF-son-teh'),
        
        ('οὐδὲ', 'οὐδέ', 'nor', 'conjunction', 'oo-DEH'),
        ('ἐπιστρέψουσι', 'ἐπιστρέφω', 'shall they return', 'verb', 'eh-pee-STREH-psoo-see'),
        ('καλύψαι', 'καλύπτω', 'to cover', 'verb', 'kah-LEEP-seh'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('γῆν.', 'γῆ', 'earth.', 'noun', 'geen'),
        
        ('Ὁ', 'ὁ', 'The One', 'article', 'ho'),
        ('ἐξαποστέλλων', 'ἐξαποστέλλω', 'sending forth', 'verb', 'ex-ah-pos-TEHL-lohn'),
        ('πηγὰς', 'πηγή', 'springs', 'noun', 'pee-GAHS'),
        ('ἐν', 'ἐν', 'in', 'preposition', 'en'),
        ('φάραγξιν,', 'φάραγξ', 'valleys,', 'noun', 'FAH-rahnks-in'),
        
        ('ἀναμέσον', 'ἀναμέσον', 'in the midst', 'preposition', 'ah-nah-MEH-son'),
        ('τῶν', 'ὁ', 'of the', 'article', 'tohn'),
        ('ὀρέων', 'ὄρος', 'mountains', 'noun', 'oh-REH-ohn'),
        ('διελεύσονται', 'διέρχομαι', 'shall pass', 'verb', 'dee-eh-LEF-son-teh'),
        ('ὕδατα·', 'ὕδωρ', 'waters;', 'noun', 'EE-dah-tah'),
        
        ('ποτιοῦσι', 'ποτίζω', 'they water', 'verb', 'poh-tee-OO-see'),
        ('πάντα', 'πᾶς', 'all', 'adjective', 'PAHN-tah'),
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('θηρία', 'θηρίον', 'beasts', 'noun', 'thee-REE-ah'),
        ('τοῦ', 'ὁ', 'of the', 'article', 'too'),
        ('ἀγροῦ,', 'ἀγρός', 'field,', 'noun', 'ah-GROO'),
        
        ('προσδέξονται', 'προσδέχομαι', 'shall receive', 'verb', 'pros-DEHK-son-teh'),
        ('ὄναγροι', 'ὄναγρος', 'wild donkeys', 'noun', 'OH-nah-gree'),
        ('εἰς', 'εἰς', 'for', 'preposition', 'ees'),
        ('δίψαν', 'δίψα', 'thirst', 'noun', 'DEEP-sahn'),
        ('αὐτῶν.', 'αὐτός', 'their.', 'pronoun', 'af-TOHN'),
        
        ('Ἐπʼ', 'ἐπί', 'By', 'preposition', 'ep'),
        ('αὐτὰ', 'αὐτός', 'them', 'pronoun', 'af-TAH'),
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('πετεινὰ', 'πετεινόν', 'birds', 'noun', 'peh-tee-NAH'),
        ('τοῦ', 'ὁ', 'of the', 'article', 'too'),
        ('οὐρανοῦ', 'οὐρανός', 'heaven', 'noun', 'oo-rah-NOO'),
        ('κατασκηνώσει,', 'κατασκηνόω', 'shall dwell,', 'verb', 'kah-tah-skee-NOH-see'),
        
        ('ἐκ', 'ἐκ', 'from', 'preposition', 'ek'),
        ('μέσου', 'μέσος', 'midst', 'adjective', 'MEH-soo'),
        ('τῶν', 'ὁ', 'of the', 'article', 'tohn'),
        ('πετρῶν', 'πέτρα', 'rocks', 'noun', 'peh-TROHN'),
        ('δώσουσι', 'δίδωμι', 'they shall give', 'verb', 'DOH-soo-see'),
        ('φωνήν.', 'φωνή', 'voice.', 'noun', 'foh-NEEN'),
        
        ('Ποτίζων', 'ποτίζω', 'He waters', 'verb', 'poh-TEE-zohn'),
        ('ὄρη', 'ὄρος', 'mountains', 'noun', 'OH-ree'),
        ('ἐκ', 'ἐκ', 'from', 'preposition', 'ek'),
        ('τῶν', 'ὁ', 'the', 'article', 'tohn'),
        ('ὑπερῴων', 'ὑπερῷον', 'upper chambers', 'noun', 'ee-peh-ROH-ohn'),
        ('αὐτοῦ,', 'αὐτός', 'His,', 'pronoun', 'af-TOO'),
        
        ('ἀπὸ', 'ἀπό', 'from', 'preposition', 'ah-POH'),
        ('καρποῦ', 'καρπός', 'fruit', 'noun', 'kahr-POO'),
        ('τῶν', 'ὁ', 'of the', 'article', 'tohn'),
        ('ἔργων', 'ἔργον', 'works', 'noun', 'EHR-gohn'),
        ('σου', 'σύ', 'Your', 'pronoun', 'soo'),
        ('χορτασθήσεται', 'χορτάζω', 'shall be satisfied', 'verb', 'khor-tas-THEE-seh-teh'),
        ('ἡ', 'ὁ', 'the', 'article', 'ee'),
        ('γῆ.', 'γῆ', 'earth.', 'noun', 'ghee'),
        
        ('Ὁ', 'ὁ', 'The One', 'article', 'ho'),
        ('ἐξανατέλλων', 'ἐξανατέλλω', 'causing to spring up', 'verb', 'ex-ah-nah-TEHL-lohn'),
        ('χόρτον', 'χόρτος', 'grass', 'noun', 'KHOR-ton'),
        ('τοῖς', 'ὁ', 'for the', 'article', 'tees'),
        ('κτήνεσι,', 'κτῆνος', 'cattle,', 'noun', 'KTEE-neh-see'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('χλόην', 'χλόη', 'green herb', 'noun', 'KLOH-een'),
        ('τῇ', 'ὁ', 'for the', 'article', 'tee'),
        ('δουλείᾳ', 'δουλεία', 'service', 'noun', 'doo-LEE-ah'),
        ('τῶν', 'ὁ', 'of', 'article', 'tohn'),
        ('ἀνθρώπων.', 'ἄνθρωπος', 'men.', 'noun', 'ahn-THROH-pohn'),
        
        ('Τοῦ', 'ὁ', 'To', 'article', 'too'),
        ('ἐξαγαγεῖν', 'ἐξάγω', 'bring forth', 'verb', 'ex-ah-gah-GEEN'),
        ('ἄρτον', 'ἄρτος', 'bread', 'noun', 'AHR-ton'),
        ('ἐκ', 'ἐκ', 'from', 'preposition', 'ek'),
        ('τῆς', 'ὁ', 'the', 'article', 'tees'),
        ('γῆς,', 'γῆ', 'earth,', 'noun', 'ghees'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('οἶνος', 'οἶνος', 'wine', 'noun', 'EE-nos'),
        ('εὐφραίνει', 'εὐφραίνω', 'gladdens', 'verb', 'ef-FREH-nee'),
        ('καρδίαν', 'καρδία', 'heart', 'noun', 'kahr-DEE-an'),
        ('ἀνθρώπου.', 'ἄνθρωπος', 'of man.', 'noun', 'ahn-THROH-poo'),
        
        ('Τοῦ', 'ὁ', 'To', 'article', 'too'),
        ('ἱλαρῦναι', 'ἱλαρύνω', 'make cheerful', 'verb', 'hee-lah-REE-neh'),
        ('πρόσωπον', 'πρόσωπον', 'face', 'noun', 'PROH-soh-pon'),
        ('ἐν', 'ἐν', 'with', 'preposition', 'en'),
        ('ἐλαίῳ,', 'ἔλαιον', 'oil,', 'noun', 'eh-LEH-oh'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ἄρτος', 'ἄρτος', 'bread', 'noun', 'AHR-tos'),
        ('καρδίαν', 'καρδία', 'heart', 'noun', 'kahr-DEE-an'),
        ('ἀνθρώπου', 'ἄνθρωπος', 'of man', 'noun', 'ahn-THROH-poo'),
        ('στηρίζει.', 'στηρίζω', 'strengthens.', 'verb', 'stee-REE-zee'),
        
        ('Χορτασθήσονται', 'χορτάζω', 'Shall be satisfied', 'verb', 'khor-tas-THEE-son-teh'),
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('ξύλα', 'ξύλον', 'trees', 'noun', 'KSEE-lah'),
        ('τοῦ', 'ὁ', 'of the', 'article', 'too'),
        ('πεδίου,', 'πεδίον', 'plain,', 'noun', 'peh-DEE-oo'),
        
        ('αἱ', 'ὁ', 'the', 'article', 'heh'),
        ('κέδροι', 'κέδρος', 'cedars', 'noun', 'KEH-dree'),
        ('τοῦ', 'ὁ', 'of', 'article', 'too'),
        ('Λιβάνου,', 'Λίβανος', 'Lebanon,', 'noun', 'lee-BAH-noo'),
        ('ἃς', 'ὅς', 'which', 'pronoun', 'has'),
        ('ἐφύτευσας.', 'φυτεύω', 'You planted.', 'verb', 'eh-FEE-tef-sahs'),
        
        ('Ἐκεῖ', 'ἐκεῖ', 'There', 'adverb', 'eh-KEE'),
        ('στρουθία', 'στρουθίον', 'sparrows', 'noun', 'stroo-THEE-ah'),
        ('ἐννοσσεύσουσι,', 'ἐννοσσεύω', 'shall nest,', 'verb', 'en-nos-SEF-soo-see'),
        
        ('τοῦ', 'ὁ', 'of the', 'article', 'too'),
        ('ἐρωδιοῦ', 'ἐρωδιός', 'heron', 'noun', 'eh-roh-dee-OO'),
        ('ἡ', 'ὁ', 'the', 'article', 'ee'),
        ('κατοικία', 'κατοικία', 'dwelling', 'noun', 'kah-tee-KEE-ah'),
        ('ἡγεῖται', 'ἡγέομαι', 'leads', 'verb', 'ee-GEE-teh'),
        ('αὐτῶν.', 'αὐτός', 'them.', 'pronoun', 'af-TOHN'),
        
        ('Ὄρη', 'ὄρος', 'Mountains', 'noun', 'OH-ree'),
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('ὑψηλὰ', 'ὑψηλός', 'high', 'adjective', 'eep-see-LAH'),
        ('ταῖς', 'ὁ', 'for the', 'article', 'tees'),
        ('ἐλάφοις,', 'ἔλαφος', 'deer,', 'noun', 'EH-lah-fees'),
        
        ('πέτρα', 'πέτρα', 'rock', 'noun', 'PEH-trah'),
        ('καταφυγὴ', 'καταφυγή', 'refuge', 'noun', 'kah-tah-fee-GEE'),
        ('τοῖς', 'ὁ', 'for the', 'article', 'tees'),
        ('λαγωοῖς.', 'λαγωός', 'hares.', 'noun', 'lah-goh-EES'),
        
        ('Ἐποίησε', 'ποιέω', 'He made', 'verb', 'eh-PEE-ee-seh'),
        ('σελήνην', 'σελήνη', 'moon', 'noun', 'seh-LEE-neen'),
        ('εἰς', 'εἰς', 'for', 'preposition', 'ees'),
        ('καιρούς,', 'καιρός', 'seasons,', 'noun', 'keh-ROOS'),
        
        ('ὁ', 'ὁ', 'the', 'article', 'ho'),
        ('ἥλιος', 'ἥλιος', 'sun', 'noun', 'HEE-lee-os'),
        ('ἔγνω', 'γινώσκω', 'knows', 'verb', 'EHG-noh'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('δύσιν', 'δύσις', 'setting', 'noun', 'DEE-sin'),
        ('αὐτοῦ.', 'αὐτός', 'its.', 'pronoun', 'af-TOO'),
        
        ('Ἔθου', 'τίθημι', 'You appointed', 'verb', 'EH-thoo'),
        ('σκότος,', 'σκότος', 'darkness,', 'noun', 'SKOH-tos'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ἐγένετο', 'γίνομαι', 'it became', 'verb', 'eh-GEH-neh-to'),
        ('νύξ,', 'νύξ', 'night,', 'noun', 'neeks'),
        
        ('ἐν', 'ἐν', 'in', 'preposition', 'en'),
        ('αὐτῇ', 'αὐτός', 'it', 'pronoun', 'af-TEE'),
        ('διελεύσονται', 'διέρχομαι', 'shall pass', 'verb', 'dee-eh-LEF-son-teh'),
        ('πάντα', 'πᾶς', 'all', 'adjective', 'PAHN-tah'),
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('θηρία', 'θηρίον', 'beasts', 'noun', 'thee-REE-ah'),
        ('τοῦ', 'ὁ', 'of the', 'article', 'too'),
        ('δρυμοῦ.', 'δρυμός', 'forest.', 'noun', 'dree-MOO'),
        
        ('Σκύμνοι', 'σκύμνος', 'Young lions', 'noun', 'SKEEM-nee'),
        ('ὠρυόμενοι', 'ὠρύομαι', 'roaring', 'verb', 'oh-ree-OH-meh-nee'),
        ('τοῦ', 'ὁ', 'to', 'article', 'too'),
        ('ἁρπάσαι,', 'ἁρπάζω', 'seize,', 'verb', 'ahr-PAH-seh'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ζητῆσαι', 'ζητέω', 'to seek', 'verb', 'zee-TEE-seh'),
        ('παρὰ', 'παρά', 'from', 'preposition', 'pah-RAH'),
        ('τῷ', 'ὁ', 'the', 'article', 'toh'),
        ('Θεῷ', 'θεός', 'God', 'noun', 'theh-OH'),
        ('βρῶσιν', 'βρῶσις', 'food', 'noun', 'BROH-sin'),
        ('αὐτοῖς.', 'αὐτός', 'for themselves.', 'pronoun', 'af-TEES'),
        
        ('Ἀνέτειλεν', 'ἀνατέλλω', 'Rose', 'verb', 'ah-NEH-tee-len'),
        ('ὁ', 'ὁ', 'the', 'article', 'ho'),
        ('ἥλιος,', 'ἥλιος', 'sun,', 'noun', 'HEE-lee-os'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('συνήχθησαν,', 'συνάγω', 'they gathered together,', 'verb', 'seen-EEK-thee-sahn'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('εἰς', 'εἰς', 'into', 'preposition', 'ees'),
        ('τὰς', 'ὁ', 'the', 'article', 'tas'),
        ('μάνδρας', 'μάνδρα', 'dens', 'noun', 'MAHN-dras'),
        ('αὐτῶν', 'αὐτός', 'their', 'pronoun', 'af-TOHN'),
        ('κοιτασθήσονται.', 'κοιτάζω', 'they shall lie down.', 'verb', 'kee-tas-THEE-son-teh'),
        
        ('Ἐξελεύσεται', 'ἐξέρχομαι', 'Shall go forth', 'verb', 'ex-eh-LEF-seh-teh'),
        ('ἄνθρωπος', 'ἄνθρωπος', 'man', 'noun', 'AHN-throh-pos'),
        ('ἐπὶ', 'ἐπί', 'to', 'preposition', 'eh-PEE'),
        ('τὸ', 'ὁ', 'the', 'article', 'to'),
        ('ἔργον', 'ἔργον', 'work', 'noun', 'EHR-gon'),
        ('αὐτοῦ,', 'αὐτός', 'his,', 'pronoun', 'af-TOO'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ἐπὶ', 'ἐπί', 'to', 'preposition', 'eh-PEE'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('ἐργασίαν', 'ἐργασία', 'labor', 'noun', 'ehr-gah-SEE-an'),
        ('αὐτοῦ', 'αὐτός', 'his', 'pronoun', 'af-TOO'),
        ('ἕως', 'ἕως', 'until', 'preposition', 'EH-ohs'),
        ('ἑσπέρας.', 'ἑσπέρα', 'evening.', 'noun', 'eh-SPEH-ras'),
        
        ('Ὡς', 'ὡς', 'How', 'conjunction', 'ohs'),
        ('ἐμεγαλύνθη', 'μεγαλύνω', 'magnified are', 'verb', 'eh-meh-gah-LEEN-thee'),
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('ἔργα', 'ἔργον', 'works', 'noun', 'EHR-gah'),
        ('σου,', 'σύ', 'Your,', 'pronoun', 'soo'),
        ('Κύριε,', 'κύριος', 'O Lord,', 'noun', 'KEE-ree-eh'),
        
        ('πάντα', 'πᾶς', 'all things', 'adjective', 'PAHN-tah'),
        ('ἐν', 'ἐν', 'in', 'preposition', 'en'),
        ('σοφίᾳ', 'σοφία', 'wisdom', 'noun', 'so-FEE-ah'),
        ('ἐποίησας,', 'ποιέω', 'You made,', 'verb', 'eh-PEE-ee-sahs'),
        
        ('ἐπληρώθη', 'πληρόω', 'is filled', 'verb', 'eh-plee-ROH-thee'),
        ('ἡ', 'ὁ', 'the', 'article', 'ee'),
        ('γῆ', 'γῆ', 'earth', 'noun', 'ghee'),
        ('τῆς', 'ὁ', 'with the', 'article', 'tees'),
        ('κτίσεώς', 'κτίσις', 'creation', 'noun', 'KTEE-seh-os'),
        ('σου.', 'σύ', 'Your.', 'pronoun', 'soo'),
        
        ('Αὕτη', 'οὗτος', 'This', 'pronoun', 'AHF-tee'),
        ('ἡ', 'ὁ', 'the', 'article', 'ee'),
        ('θάλασσα', 'θάλασσα', 'sea', 'noun', 'THAH-las-sah'),
        ('ἡ', 'ὁ', 'the', 'article', 'ee'),
        ('μεγάλη', 'μέγας', 'great', 'adjective', 'meh-GAH-lee'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('εὐρύχωρος,', 'εὐρύχωρος', 'spacious,', 'adjective', 'ev-REE-kho-ros'),
        
        ('ἐκεῖ', 'ἐκεῖ', 'there', 'adverb', 'eh-KEE'),
        ('ἑρπετὰ', 'ἑρπετόν', 'creeping things', 'noun', 'ehr-peh-TAH'),
        ('ὧν', 'ὅς', 'of which', 'pronoun', 'hohn'),
        ('οὐκ', 'οὐ', 'not', 'particle', 'ook'),
        ('ἔστιν', 'εἰμί', 'there is', 'verb', 'EH-stin'),
        ('ἀριθμός,', 'ἀριθμός', 'number,', 'noun', 'ah-rith-MOS'),
        
        ('ζῷα', 'ζῷον', 'creatures', 'noun', 'ZOH-ah'),
        ('μικρὰ', 'μικρός', 'small', 'adjective', 'mee-KRAH'),
        ('μετὰ', 'μετά', 'with', 'preposition', 'meh-TAH'),
        ('μεγάλων.', 'μέγας', 'great.', 'adjective', 'meh-GAH-lohn'),
        
        ('Ἐκεῖ', 'ἐκεῖ', 'There', 'adverb', 'eh-KEE'),
        ('πλοῖα', 'πλοῖον', 'ships', 'noun', 'PLEE-ah'),
        ('διαπορεύονται,', 'διαπορεύομαι', 'pass through,', 'verb', 'dee-ah-po-REF-on-teh'),
        
        ('δράκων', 'δράκων', 'dragon', 'noun', 'DRAH-kohn'),
        ('οὗτος,', 'οὗτος', 'this,', 'pronoun', 'HOO-tos'),
        ('ὃν', 'ὅς', 'which', 'pronoun', 'hon'),
        ('ἔπλασας', 'πλάσσω', 'You formed', 'verb', 'EH-plah-sahs'),
        ('ἐμπαίζειν', 'ἐμπαίζω', 'to play', 'verb', 'em-PEH-zeen'),
        ('αὐτῇ.', 'αὐτός', 'in it.', 'pronoun', 'af-TEE'),
        
        ('Πάντα', 'πᾶς', 'All', 'adjective', 'PAHN-tah'),
        ('πρὸς', 'πρός', 'to', 'preposition', 'pros'),
        ('σὲ', 'σύ', 'You', 'pronoun', 'seh'),
        ('προσδοκῶσι,', 'προσδοκάω', 'look,', 'verb', 'pros-doh-KOH-see'),
        
        ('δοῦναι', 'δίδωμι', 'to give', 'verb', 'DOO-neh'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('τροφὴν', 'τροφή', 'food', 'noun', 'troh-FEEN'),
        ('αὐτῶν', 'αὐτός', 'their', 'pronoun', 'af-TOHN'),
        ('εἰς', 'εἰς', 'in', 'preposition', 'ees'),
        ('εὔκαιρον,', 'εὔκαιρος', 'due season,', 'adjective', 'EF-keh-ron'),
        
        ('δόντος', 'δίδωμι', 'giving', 'verb', 'DON-tos'),
        ('σου', 'σύ', 'You', 'pronoun', 'soo'),
        ('αὐτοῖς', 'αὐτός', 'to them', 'pronoun', 'af-TEES'),
        ('συλλέξουσιν.', 'συλλέγω', 'they shall gather.', 'verb', 'seel-LEH-ksoo-sin'),
        
        ('Ἀνοίξαντός', 'ἀνοίγω', 'Opening', 'verb', 'ah-NEE-ksan-tos'),
        ('σου', 'σύ', 'You', 'pronoun', 'soo'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('χεῖρα,', 'χείρ', 'hand,', 'noun', 'KHEE-rah'),
        
        ('τὰ', 'ὁ', 'the', 'article', 'tah'),
        ('σύμπαντα', 'σύμπας', 'all things', 'adjective', 'SEEM-pahn-tah'),
        ('πλησθήσονται', 'πίμπλημι', 'shall be filled', 'verb', 'plees-THEE-son-teh'),
        ('χρηστότητος,', 'χρηστότης', 'with goodness,', 'noun', 'khrees-TOH-tee-tos'),
        
        ('ἀποστρέψαντος', 'ἀποστρέφω', 'turning away', 'verb', 'ah-po-STREH-psan-tos'),
        ('δέ', 'δέ', 'but', 'particle', 'deh'),
        ('σου', 'σύ', 'You', 'pronoun', 'soo'),
        ('τὸ', 'ὁ', 'the', 'article', 'to'),
        ('πρόσωπον,', 'πρόσωπον', 'face,', 'noun', 'PROH-soh-pon'),
        ('ταραχθήσονται.', 'ταράσσω', 'they shall be troubled.', 'verb', 'tah-rahkh-THEE-son-teh'),
        
        ('Ἀντανελεῖς', 'ἀνταναιρέω', 'You take away', 'verb', 'ahn-tah-neh-LEES'),
        ('τὸ', 'ὁ', 'the', 'article', 'to'),
        ('πνεῦμα', 'πνεῦμα', 'spirit', 'noun', 'PNEV-mah'),
        ('αὐτῶν,', 'αὐτός', 'their,', 'pronoun', 'af-TOHN'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ἐκλείψουσι,', 'ἐκλείπω', 'they shall fail,', 'verb', 'ek-LEEP-soo-see'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('εἰς', 'εἰς', 'unto', 'preposition', 'ees'),
        ('τὸν', 'ὁ', 'the', 'article', 'ton'),
        ('χοῦν', 'χοῦς', 'dust', 'noun', 'khoon'),
        ('αὐτῶν', 'αὐτός', 'their', 'pronoun', 'af-TOHN'),
        ('ἐπιστρέψουσιν.', 'ἐπιστρέφω', 'they shall return.', 'verb', 'eh-pee-STREH-psoo-sin'),
        
        ('Ἐξαποστελεῖς', 'ἐξαποστέλλω', 'You shall send forth', 'verb', 'ex-ah-pos-teh-LEES'),
        ('τὸ', 'ὁ', 'the', 'article', 'to'),
        ('πνεῦμα', 'πνεῦμα', 'Spirit', 'noun', 'PNEV-mah'),
        ('σου,', 'σύ', 'Your,', 'pronoun', 'soo'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('κτισθήσονται,', 'κτίζω', 'they shall be created,', 'verb', 'ktees-THEE-son-teh'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ἀνακαινιεῖς', 'ἀνακαινίζω', 'You shall renew', 'verb', 'ah-nah-keh-nee-EES'),
        ('τὸ', 'ὁ', 'the', 'article', 'to'),
        ('πρόσωπον', 'πρόσωπον', 'face', 'noun', 'PROH-soh-pon'),
        ('τῆς', 'ὁ', 'of the', 'article', 'tees'),
        ('γῆς.', 'γῆ', 'earth.', 'noun', 'ghees'),
        
        ('Ἤτω', 'εἰμί', 'May be', 'verb', 'EE-toh'),
        ('ἡ', 'ὁ', 'the', 'article', 'ee'),
        ('δόξα', 'δόξα', 'glory', 'noun', 'DOHK-sah'),
        ('Κυρίου', 'κύριος', 'of the Lord', 'noun', 'kee-REE-oo'),
        ('εἰς', 'εἰς', 'unto', 'preposition', 'ees'),
        ('τοὺς', 'ὁ', 'the', 'article', 'toos'),
        ('αἰῶνας,', 'αἰών', 'ages,', 'noun', 'eh-OH-nas'),
        
        ('εὐφρανθήσεται', 'εὐφραίνω', 'shall be glad', 'verb', 'ef-frahn-THEE-seh-teh'),
        ('Κύριος', 'κύριος', 'the Lord', 'noun', 'KEE-ree-os'),
        ('ἐπὶ', 'ἐπί', 'in', 'preposition', 'eh-PEE'),
        ('τοῖς', 'ὁ', 'the', 'article', 'tees'),
        ('ἔργοις', 'ἔργον', 'works', 'noun', 'EHR-gees'),
        ('αὐτοῦ.', 'αὐτός', 'His.', 'pronoun', 'af-TOO'),
        
        ('Ὁ', 'ὁ', 'The One', 'article', 'ho'),
        ('ἐπιβλέπων', 'ἐπιβλέπω', 'looking upon', 'verb', 'eh-pee-BLEH-pohn'),
        ('ἐπὶ', 'ἐπί', 'upon', 'preposition', 'eh-PEE'),
        ('τὴν', 'ὁ', 'the', 'article', 'teen'),
        ('γῆν,', 'γῆ', 'earth,', 'noun', 'gheen'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ποιῶν', 'ποιέω', 'making', 'verb', 'pee-OHN'),
        ('αὐτὴν', 'αὐτός', 'it', 'pronoun', 'af-TEEN'),
        ('τρέμειν,', 'τρέμω', 'to tremble,', 'verb', 'TREH-meen'),
        
        ('ὁ', 'ὁ', 'the One', 'article', 'ho'),
        ('ἁπτόμενος', 'ἅπτω', 'touching', 'verb', 'ahp-TOH-meh-nos'),
        ('τῶν', 'ὁ', 'the', 'article', 'tohn'),
        ('ὀρέων,', 'ὄρος', 'mountains,', 'noun', 'oh-REH-ohn'),
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('καπνίζονται.', 'καπνίζω', 'they smoke.', 'verb', 'kahp-NEE-zon-teh'),
        
        ('ᾌσω', 'ᾄδω', 'I will sing', 'verb', 'AH-soh'),
        ('τῷ', 'ὁ', 'to the', 'article', 'toh'),
        ('Κυρίῳ', 'κύριος', 'Lord', 'noun', 'kee-REE-oh'),
        ('ἐν', 'ἐν', 'in', 'preposition', 'en'),
        ('τῇ', 'ὁ', 'the', 'article', 'tee'),
        ('ζωῇ', 'ζωή', 'life', 'noun', 'zo-EE'),
        ('μου,', 'ἐγώ', 'my,', 'pronoun', 'moo'),
        
        ('ψαλῶ', 'ψάλλω', 'I will sing praise', 'verb', 'psah-LOH'),
        ('τῷ', 'ὁ', 'to the', 'article', 'toh'),
        ('Θεῷ', 'θεός', 'God', 'noun', 'theh-OH'),
        ('μου', 'ἐγώ', 'my', 'pronoun', 'moo'),
        ('ἕως', 'ἕως', 'as long as', 'preposition', 'EH-ohs'),
        ('ὑπάρχω.', 'ὑπάρχω', 'I exist.', 'verb', 'ee-PAHR-kho'),
        
        ('Ἡδυνθείη', 'ἡδύνω', 'May be sweet', 'verb', 'ee-deen-THEE-ee'),
        ('αὐτῷ', 'αὐτός', 'to Him', 'pronoun', 'af-TOH'),
        ('ἡ', 'ὁ', 'the', 'article', 'ee'),
        ('διαλογή', 'διαλογή', 'meditation', 'noun', 'dee-ah-lo-GEE'),
        ('μου,', 'ἐγώ', 'my,', 'pronoun', 'moo'),
        
        ('ἐγὼ', 'ἐγώ', 'I', 'pronoun', 'eh-GOH'),
        ('δὲ', 'δέ', 'but', 'particle', 'deh'),
        ('εὐφρανθήσομαι', 'εὐφραίνω', 'shall be glad', 'verb', 'ef-frahn-THEE-so-meh'),
        ('ἐπὶ', 'ἐπί', 'in', 'preposition', 'eh-PEE'),
        ('τῷ', 'ὁ', 'the', 'article', 'toh'),
        ('Κυρίῳ.', 'κύριος', 'Lord.', 'noun', 'kee-REE-oh'),
        
        ('Ἐκλείποιεν', 'ἐκλείπω', 'May fail', 'verb', 'ek-LEEP-ee-en'),
        ('ἁμαρτωλοὶ', 'ἁμαρτωλός', 'sinners', 'adjective', 'ah-mahr-toh-LEE'),
        ('ἀπὸ', 'ἀπό', 'from', 'preposition', 'ah-POH'),
        ('τῆς', 'ὁ', 'the', 'article', 'tees'),
        ('γῆς,', 'γῆ', 'earth,', 'noun', 'ghees'),
        
        ('καὶ', 'καί', 'and', 'conjunction', 'keh'),
        ('ἄνομοι,', 'ἄνομος', 'lawless,', 'adjective', 'AH-no-mee'),
        ('ὥστε', 'ὥστε', 'so as', 'conjunction', 'HOH-steh'),
        ('μὴ', 'μή', 'not', 'particle', 'mee'),
        ('ὑπάρχειν', 'ὑπάρχω', 'to exist', 'verb', 'ee-PAHR-kheen'),
        ('αὐτούς.', 'αὐτός', 'them.', 'pronoun', 'af-TOOS'),
        
        ('Εὐλόγει,', 'εὐλογέω', 'Bless,', 'verb', 'ev-LOH-yee'),
        ('ἡ', 'ὁ', 'O', 'article', 'ee'),
        ('ψυχή', 'ψυχή', 'soul', 'noun', 'psee-KHEE'),
        ('μου,', 'ἐγώ', 'my,', 'pronoun', 'moo'),
        ('τὸν', 'ὁ', 'the', 'article', 'ton'),
        ('Κύριον.', 'κύριος', 'Lord.', 'noun', 'KEE-ree-on')
    ]
    
    # Create word entries with Strong's lookups
    words = []
    matched = 0
    unmatched = []
    
    for word, lemma, gloss, pos, phonetic in psalm_words:
        word_entry = create_word_entry(word, lemma, gloss, pos, phonetic, strongs_dict)
        words.append(word_entry)
        
        if 'strongs' in word_entry and word_entry['strongs']:
            matched += 1
        else:
            unmatched.append(f"{word} ({lemma})")
    
    # Save to file
    output_file = Path('texts/psalm_103.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Created {output_file} with {len(words)} words")
    print(f"✅ {matched} words matched to Strong's ({matched/len(words)*100:.1f}%)")
    
    if unmatched:
        print(f"⚠️  {len(unmatched)} words without Strong's match:")
        for word in unmatched[:15]:
            print(f"    - {word}")
        if len(unmatched) > 15:
            print(f"    ... and {len(unmatched) - 15} more")

if __name__ == '__main__':
    create_psalm_103()
