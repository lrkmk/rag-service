#!/usr/bin/env bash
# Package the current chroma_db/ and publish it as a GitHub Release asset,
# so the server can fetch the latest vector data with a stable URL instead
# of scp/rsync — chroma_db is a binary SQLite+index artifact, deliberately
# NOT tracked in git (see .gitignore) since committing it directly would
# bloat the repo's history on every re-ingest (see commit 77ceed3's message
# for the reasoning).
#
# Uses a single rolling tag (chroma-db-latest) and overwrites its asset each
# run (--clobber), so the download URL never changes between publishes —
# the server always fetches the same URL to get whatever was last published.
#
# Usage:
#   ./scripts/deploy/publish_chroma_db.sh
#
# Requires: gh CLI, authenticated (gh auth login), run from repo root.

set -euo pipefail

GH="${GH_BIN:-gh}"
TAG="chroma-db-latest"
ARCHIVE="chroma_db.tar.gz"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$REPO_ROOT"

if [ ! -d chroma_db ]; then
    echo "ERROR: chroma_db/ not found at $REPO_ROOT/chroma_db — run the ingest_*.py scripts first." >&2
    exit 1
fi

echo "Packaging chroma_db/ -> $ARCHIVE ..."
tar -czf "$ARCHIVE" chroma_db/
SIZE=$(du -h "$ARCHIVE" | cut -f1)
echo "Done, $SIZE."

if "$GH" release view "$TAG" >/dev/null 2>&1; then
    echo "Release $TAG exists, replacing asset ..."
    "$GH" release upload "$TAG" "$ARCHIVE" --clobber
else
    echo "Creating release $TAG ..."
    "$GH" release create "$TAG" "$ARCHIVE" \
        --title "Chroma DB (latest)" \
        --notes "Rolling snapshot of chroma_db/, published by scripts/deploy/publish_chroma_db.sh. Published: $(date -u '+%Y-%m-%d %H:%M UTC')."
fi

rm -f "$ARCHIVE"

REPO_SLUG=$("$GH" repo view --json nameWithOwner -q .nameWithOwner)
echo ""
echo "Published. Server-side fetch command (stable URL, doesn't change between publishes):"
echo ""
echo "  curl -L -o chroma_db.tar.gz https://github.com/${REPO_SLUG}/releases/download/${TAG}/${ARCHIVE}"
echo ""
