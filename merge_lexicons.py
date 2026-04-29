import json

def merge_lexicons(original_path, corrected_path, output_path):
    with open(original_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    with open(corrected_path, 'r', encoding='utf-8') as f:
        corrected_data = json.load(f)

    merged_dict = {}

    for entry in original_data:
        lemma = entry.get('lemma')
        if lemma:
            merged_dict[lemma] = entry

    for entry in corrected_data:
        lemma = entry.get('lemma')
        if lemma:
            if lemma in merged_dict:
                merged_dict[lemma].update(entry)
            else:
                merged_dict[lemma] = entry

    merged_list = list(merged_dict.values())
    merged_list.sort(key=lambda x: x.get('lemma', ''))

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=2)

    print(f"Successfully merged {len(merged_list)} entries into {output_path}")

merge_lexicons(
    'texts/lexicon.json',
    'texts/lexicon_corrected.json',
    'texts/lexicon.json'   # write back to lexicon.json in-place
)
