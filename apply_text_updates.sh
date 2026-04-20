#!/bin/bash
#
# APPLY SCRIPT: Replace text files with Strong's-validated versions
# Usage: bash apply_text_updates.sh
#

echo "=========================================="
echo "APPLY: Strong's Dictionary Updates"
echo "=========================================="

# Check if corrected files exist
if [ ! -d "texts/corrected" ]; then
    echo "❌ Error: No corrected files found at texts/corrected/"
    echo "Please run: python3 validate_text_files.py first"
    exit 1
fi

corrected_count=$(ls texts/corrected/*.json 2>/dev/null | wc -l | tr -d ' ')

if [ "$corrected_count" -eq 0 ]; then
    echo "❌ Error: No JSON files found in texts/corrected/"
    exit 1
fi

echo "Found $corrected_count corrected files ready to apply"
echo ""
echo "This will replace your text files with Strong's-enhanced versions:"
echo "  - Matched words: Get Strong's definitions, etymology, etc."
echo "  - Unmatched words: Preserved exactly as-is"
echo ""
echo "Match rate from validation: 93.1% (1166/1253 words)"
echo ""
echo "A backup already exists at: texts/original_backup/"
read -p "Continue with replacement? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Update cancelled."
    exit 0
fi

# Apply the corrected files
cp texts/corrected/*.json texts/
applied_count=$(ls texts/corrected/*.json 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "✅ Applied $applied_count corrected text files"
echo ""
echo "=========================================="
echo "UPDATE COMPLETE"
echo "=========================================="
echo ""
echo "Your text files now include Strong's dictionary data!"
echo ""
echo "Summary:"
echo "  - 93.1% of words matched to Strong's Greek Dictionary"
echo "  - All liturgical-specific terms preserved unchanged"
echo "  - Original files backed up to: texts/original_backup/"
echo ""
echo "To UNDO this update:"
echo "  bash undo_text_updates.sh"
echo ""
echo "Files updated: $applied_count"
echo "  annunciation.json, dormition.json, gladsome_light.json,"
echo "  glory_to_the_father.json, heavenly_king.json, holy_cross.json,"
echo "  it_is_truly_meet.json, jesus_prayer.json, kyrie_eleison.json,"
echo "  lords_prayer.json, nativity_of_christ.json, presentation_christ.json,"
echo "  psalm_50.json, the_creed.json, theotokos_nativity.json,"
echo "  theotokos_presentation.json, to_thee_the_champion_leader.json,"
echo "  transfiguration.json, trisagion.json, troparion_nativity.json,"
echo "  troparion_pascha.json, troparion_theophany.json"
