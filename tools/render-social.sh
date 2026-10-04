#!/bin/sh
# Renders the images shown when a page is shared, into og/<page>.jpg, and the
# home-screen icon, apple-touch-icon.png. Run it from the repository root
# while the local server is running (python3 -m http.server 5050), after
# adding a note or changing a note's title, description or first drawing.
set -e

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
BASE="${BASE:-http://localhost:5050}"
mkdir -p og

shot() { # name, url, width, height
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size="$3,$4" --virtual-time-budget=10000 --screenshot="$1" "$2" >/dev/null 2>&1
}

shot og/home.png "$BASE/tools/social-home.html" 1200 630
pages="notes about projects $(grep -o 'class="note-index-link[^"]*" href="/[^"/]*/' notes/index.html | sed 's|.*href="/||; s|/$||')"
for page in $pages; do
  shot "og/$page.png" "$BASE/tools/social-card.html?page=$page" 1200 630
done
shot apple-touch-icon.png "$BASE/tools/touch-icon.html" 180 180

# Shared images travel better as modest JPEGs.
python3 - <<'PY'
from pathlib import Path
from PIL import Image
for png in Path("og").glob("*.png"):
    Image.open(png).convert("RGB").save(png.with_suffix(".jpg"), quality=86, optimize=True, progressive=True)
    png.unlink()
PY
ls -l og apple-touch-icon.png
