# Retrieval-only service: exposes the search/lookup tools over MCP
# (streamable-http). Deliberately excludes crawl/chunk/ingest scripts —
# those are build-time/offline tooling, not part of the runtime service. The
# vector data (chroma_db/) is NOT baked into this image; it's supplied at
# container-run time via a volume mount (see docker-compose.yml), so
# re-ingesting updated docs doesn't require rebuilding the image.
#
# doc/ (the raw source .md trees) IS baked in, despite being crawl/offline
# output: get_full_article() reads directly from doc/帮助中心, doc/API文档,
# doc/产品介绍 on disk (source_path -> file), not from Chroma — without it
# every get_full_article call 404s. Text only, small.

FROM python:3.11-slim

WORKDIR /app

# Only the retrieval-side dependencies — no requests/bs4/curl-equivalents for
# crawling, no ingest-time-only tooling.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download and cache the embedding model at build time, not first request:
# avoids a slow/network-dependent cold start and keeps the container usable
# with no outbound internet access at runtime.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-large-zh-v1.5')"

# Only the files mcp_server.py actually needs at runtime. Copied preserving
# their scripts/<category>/ subdirectory structure (not flattened into
# ./scripts/) because rag_search.py derives DB_PATH and PARENTS_LOOKUP_PATH
# from its own file location assuming a <repo_root>/scripts/search/rag_search.py
# layout — flattening it would silently point DB_PATH at the wrong directory.
#
# lookup_tables.py (scripts/search/) and chunk_diff.py (scripts/chunking/)
# are runtime imports (mcp_server imports lookup_tables directly; rag_search
# imports chunk_diff for strip_boilerplate in get_full_article) even though
# chunk_diff.py also gets swept up in the broader "chunking scripts are
# offline tooling" .dockerignore rule — without an explicit COPY here the
# container crash-loops on startup with ModuleNotFoundError.
COPY scripts/search/rag_search.py scripts/search/mcp_server.py scripts/search/lookup_tables.py ./scripts/search/
COPY scripts/ingest/parents_lookup.json ./scripts/ingest/
COPY scripts/chunking/chunk_diff.py ./scripts/chunking/
COPY doc/ ./doc/

ENV MCP_TRANSPORT=streamable-http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=5000
EXPOSE 5000

CMD ["python", "scripts/search/mcp_server.py"]
