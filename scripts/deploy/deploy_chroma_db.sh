#!/usr/bin/env bash
# Server-side counterpart to publish_chroma_db.sh: fetches the latest
# chroma_db snapshot from the rolling GitHub Release and swaps it in.
#
# Run `git pull` FIRST, then this script. scripts/ingest/parents_lookup.json
# (帮助中心 parent-article summaries, keyed by article_id) is git-tracked and
# volume-mounted (see docker-compose.yml) rather than baked into the image,
# so `git pull` is what actually updates it — this script only handles
# chroma_db (gitignored, shipped via GitHub Release instead, since it's a
# large binary artifact). Skipping the git pull leaves parents_lookup.json
# stale even after this script runs: confirmed for real in production, a
# child pointing at a newly-added parent_id resolved to null
# parent_title/parent_summary/source_path because the running container's
# parents_lookup.json predated that parent record.
#
# Run this ON THE SERVER, from the repo root (where docker-compose.yml
# lives). Backs up the existing chroma_db before replacing it, and restarts
# the container so it picks up both the new chroma_db and the git-pulled
# parents_lookup.json (Chroma reads from disk, but rag_search.py's
# collection handles are cached in memory for the life of the process — see
# the atomic _lazy_init comment in rag_search.py — so a restart is the safe
# way to be sure new data is actually visible). A plain restart is enough
# for both files now; a full image rebuild is no longer required.
#
# Usage:
#   git pull
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
echo "  a manual MCP query you know the answer to (e.g. via mcporter) -- check parent_title/source_path aren't null"
echo ""
echo "Once confirmed good:"
echo "  rm -rf chroma_db.bak"
echo ""
echo "If something's wrong, roll back with:"
echo "  rm -rf chroma_db && mv chroma_db.bak chroma_db && docker compose restart"
