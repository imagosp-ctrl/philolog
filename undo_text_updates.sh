#!/bin/bash
#
# UNDO SCRIPT: Restore original text files from backup
# Usage: bash undo_text_updates.sh
#

echo "=========================================="
echo "UNDO: Restoring Original Text Files"
echo "=========================================="

# Check if backup exists
if [ ! -d "texts/original_backup" ]; then
    echo "❌ Error: No backup found at texts/original_backup/"
    echo "Cannot undo - backup directory does not exist."
    exit 1
fi

# Count files in backup
backup_count=$(ls texts/original_backup/*.json 2>/dev/null | wc -l | tr -d ' ')

if [ "$backup_count" -eq 0 ]; then
    echo "❌ Error: No JSON files found in backup directory"
    exit 1
fi

echo "Found $backup_count files in backup"
echo ""
echo "This will restore ALL text files to their original state"
echo "and remove Strong's dictionary enhancements."
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Undo cancelled."
    exit 0
fi

# Create a backup of the corrected versions (just in case)
mkdir -p texts/corrected_backup
cp texts/corrected/*.json texts/corrected_backup/ 2>/dev/null
echo "✅ Saved corrected versions to texts/corrected_backup/ (just in case)"

# Restore original files
cp texts/original_backup/*.json texts/
restored_count=$(ls texts/original_backup/*.json 2>/dev/null | wc -l | tr -d ' ')

echo "✅ Restored $restored_count original text files"
echo ""
echo "=========================================="
echo "UNDO COMPLETE"
echo "=========================================="
echo ""
echo "Your text files have been restored to their original state."
echo ""
echo "If you want to re-apply the Strong's updates:"
echo "  bash apply_text_updates.sh"
echo ""
echo "Backups preserved:"
echo "  - Original files: texts/original_backup/"
echo "  - Corrected files: texts/corrected/ and texts/corrected_backup/"
