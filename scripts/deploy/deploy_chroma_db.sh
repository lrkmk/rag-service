#!/usr/bin/env bash
# Server-side counterpart to publish_chroma_db.sh: fetches the latest
# chroma_db snapshot from the rolling GitHub Release and swaps it in.
#
# Run this ON THE SERVER, from the repo root (where docker-compose.yml
# lives). Backs up the existing chroma_db before replacing it, and restarts
# the container so it picks up the new data (Chroma reads from disk, but
# rag_search.py's collection handles are cached in memory for the life of
# the process — see the atomic _lazy_init comment in rag_search.py — so a
# restart is the safe way to be sure new data is actually visible).
#
# Usage:
#   ./scripts/deploy/deploy_chroma_db.sh
#
# Requires: curl, docker compose, run from repo root.

set -euo pipefail

REPO_SLUG="lrkmk/rag-service"
TAG="chroma-db-latest"
ARCHIVE="chroma_db.tar.gz"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$REPO_ROOT"

if [ ! -f docker-compose.yml ]; then
    echo "ERROR: docker-compose.yml not found at $REPO_ROOT — run this from the repo root." >&2
    exit 1
fi

echo "Downloading latest chroma_db from GitHub Releases ..."
curl -fL -o "$ARCHIVE" "https://github.com/${REPO_SLUG}/releases/download/${TAG}/${ARCHIVE}"

if [ -d chroma_db ]; then
    echo "Backing up existing chroma_db -> chroma_db.bak (overwriting any previous backup) ..."
    rm -rf chroma_db.bak
    mv chroma_db chroma_db.bak
fi

echo "Extracting ..."
tar -xzf "$ARCHIVE"
rm -f "$ARCHIVE"

echo "Restarting container ..."
docker compose restart

echo ""
echo "Done. Verify before cleaning up the backup:"
echo "  docker compose logs --tail=20 atlas-docs-mcp   # confirm it's stably Up, no crash loop"
echo "  python scripts/test_mcp_remote.py               # or a manual query you know the answer to"
echo ""
echo "Once confirmed good:"
echo "  rm -rf chroma_db.bak"
echo ""
echo "If something's wrong, roll back with:"
echo "  rm -rf chroma_db && mv chroma_db.bak chroma_db && docker compose restart"
