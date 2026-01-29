#!/bin/bash
echo "Testing page layouts..."
echo ""
for page in index.html ebooks.html audiobooks.html music.html apps.html games.html store.html; do
  if [ -f "$page" ]; then
    # Check for the corrupt text
    if grep -q "claude/evaluate-website" "$page"; then
      echo "❌ $page - Still has corrupt text"
    else
      echo "✅ $page - Clean"
    fi
  fi
done
