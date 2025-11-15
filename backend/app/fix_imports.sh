#!/bin/bash

BACKEND_DIR="backend/app"

echo "🔍 Starting automatic import cleanup in $BACKEND_DIR"

# 1 — Create a backup folder
BACKUP_DIR="backup_import_fix_$(date +%Y%m%d_%H%M%S)"
echo "📦 Creating backup folder: $BACKUP_DIR"
mkdir $BACKUP_DIR
cp -r $BACKEND_DIR $BACKUP_DIR/

# 2 — Find all Python files
FILES=$(find $BACKEND_DIR -name "*.py")

echo "📝 Processing Python files..."

for file in $FILES; do
    echo "  → Fixing imports in: $file"

    # FIX 1: replace "from app." → "from "
    sed -i 's/from app\./from /g' "$file"

    # FIX 2: replace "import app." → "import "
    sed -i 's/import app\./import /g' "$file"
done

echo "✅ Import cleanup complete!"
echo "📁 Backup of original files saved in: $BACKUP_DIR"
