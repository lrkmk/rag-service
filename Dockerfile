# Retrieval-only service: exposes the 4 search tools over MCP (streamable-http).
# Deliberately excludes crawl/chunk/ingest scripts and the raw 帮助中心/API文档
# source trees — those are build-time/offline tooling, not part of the runtime
# service. The vector data (chroma_db/) is NOT baked into this image; it's
# supplied at container-run time via a volume mount (see docker-compose.yml),
# so re-ingesting updated docs doesn't require rebuilding the image.

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

# Only the files mcp_server.py actually needs at runtime. Kept under
# ./scripts/ (not flattened into /app/) because rag_search.py derives
# DB_PATH and PARENTS_LOOKUP_PATH from its own file location assuming a
# <repo_root>/scripts/rag_search.py layout — flattening it would silently
# point DB_PATH at the filesystem root instead of /app/chroma_db.
COPY scripts/rag_search.py scripts/mcp_server.py scripts/parents_lookup.json ./scripts/

ENV MCP_TRANSPORT=streamable-http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=5000
EXPOSE 5000

CMD ["python", "scripts/mcp_server.py"]
