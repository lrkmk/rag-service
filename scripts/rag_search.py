"""
Shared search helpers against the Chroma store built by ingest_chroma.py.
Imported by both query_example.py (fixed demo queries) and ask.py (CLI tool
for ad hoc natural-language questions).

BGE asymmetric embedding note:
  BAAI/bge-large-zh-v1.5 (used in ingest_chroma.py) recommends prefixing
  *queries* with an instruction string, but leaving *documents* unprefixed.
  Chroma's `query_texts=` would embed the query with the exact same
  (unprefixed) code path used for documents, silently losing that signal.
  So here we load the model directly, encode the query with the prefix
  ourselves, and pass `query_embeddings=` instead of `query_texts=`.
"""

import json
import os
import re

import chromadb
from sentence_transformers import SentenceTransformer

import chunk_diff

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(REPO_ROOT, "chroma_db")
PARENTS_LOOKUP_PATH = os.path.join(REPO_ROOT, "scripts", "parents_lookup.json")
HELP_CENTER_ROOT = os.path.join(REPO_ROOT, "帮助中心")
API_DOCS_ROOT = os.path.join(REPO_ROOT, "API文档")

# Must match the model used in ingest_chroma.py's EMBEDDER — the two sides
# have to produce vectors in the same space.
MODEL_NAME = "BAAI/bge-large-zh-v1.5"
QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："

_model = None
_client = None
_rule_coll = None
_faq_coll = None
_api_coll = None
_api_faq_coll = None
_parents = None


def _lazy_init():
    global _model, _client, _rule_coll, _faq_coll, _api_coll, _api_faq_coll, _parents
    # Guard on the LAST value set, not the first: if init fails partway
    # (e.g. get_collection raises after _model/_client are already
    # assigned), a "if _model is not None: return" guard would treat
    # future calls as already-initialized and skip retrying forever —
    # this actually happened against the deployed service (a bad read-only
    # volume mount made get_collection fail, and every call after the
    # first returned "'NoneType' object has no attribute 'query'" instead
    # of retrying). Build everything into locals first and only publish to
    # the module globals once every step has succeeded, so a failed
    # attempt leaves nothing half-set and the next call retries cleanly.
    if _parents is not None:
        return
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=DB_PATH)
    # No embedding_function passed to get_collection on purpose: we only ever
    # call these with query_embeddings=/pre-embedded documents, so Chroma
    # never needs to invoke an embedder itself on this side.
    rule_coll = client.get_collection(name="atlas_rule_chunks")
    faq_coll = client.get_collection(name="atlas_faq_chunks")
    api_coll = client.get_collection(name="atlas_api_chunks")
    api_faq_coll = client.get_collection(name="atlas_api_faq_chunks")
    with open(PARENTS_LOOKUP_PATH, encoding="utf-8") as f:
        parents = json.load(f)

    _model, _client = model, client
    _rule_coll, _faq_coll, _api_coll, _api_faq_coll = rule_coll, faq_coll, api_coll, api_faq_coll
    _parents = parents


def embed_query(text: str) -> list[float]:
    _lazy_init()
    return _model.encode(QUERY_INSTRUCTION + text, normalize_embeddings=True).tolist()


def search_rules(query: str, n_results: int = 3, where: dict | None = None):
    _lazy_init()
    res = _rule_coll.query(query_embeddings=[embed_query(query)], n_results=n_results, where=where)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        parent = _parents.get(meta.get("parent_id"), {})
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "level1_category": meta.get("level1_category"),
            "level2_category": meta.get("level2_category"),
            "section": meta.get("section"),
            "text": meta.get("text"),
            "applicable_carrier": meta.get("applicable_carrier"),
            "parent_title": parent.get("title"),
            "parent_summary": parent.get("summary"),
            "source_path": parent.get("source_path"),
        })
    return hits


def search_faq(query: str, n_results: int = 3):
    _lazy_init()
    res = _faq_coll.query(query_embeddings=[embed_query(query)], n_results=n_results)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "topic": meta.get("topic"),
            "question": meta.get("question"),
            "answer": meta.get("answer"),
        })
    return hits


def search_api_docs(query: str, n_results: int = 3, where: dict | None = None):
    """Search API文档 (developer/API reference corpus) — separate collection
    from 帮助中心 on purpose, see RAG-切片设计总览.md. No parent-summary
    bolt-on here: API文档 chunks have no parent tier (the C-type "端点概览"
    chunk_type serves that role for OpenAPI endpoints, A/B-type chunks stand
    alone)."""
    _lazy_init()
    res = _api_coll.query(query_embeddings=[embed_query(query)], n_results=n_results, where=where)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "doc_type": meta.get("doc_type"),
            "level1_category": meta.get("level1_category"),
            "level2_category": meta.get("level2_category"),
            "section": meta.get("section"),
            "text": meta.get("text"),
            "applicable_carrier": meta.get("applicable_carrier"),
            "compares": meta.get("compares"),
            "endpoint": meta.get("endpoint"),
            "source_path": meta.get("source_path"),
        })
    return hits


def get_full_article(source_path: str) -> dict:
    """Reads the full source article for a source_path as returned by
    search_rules/search_api_docs (帮助中心 chunks get it via parent lookup,
    API文档 chunks carry it directly). This is the get_full_article
    equivalent of the old GitBook MCP's getPage(url) tool — for when a
    chunk's snippet doesn't have enough context and the whole article is
    needed (a chunk is one rule/concept; an article can cover several).

    Tries both corpus roots since source_path alone doesn't say which one
    it came from (the two roots use the same relative-path convention)."""
    for root in (HELP_CENTER_ROOT, API_DOCS_ROOT):
        candidate = os.path.normpath(os.path.join(root, source_path))
        if not candidate.startswith(os.path.normpath(root)):
            continue  # reject path traversal, same guard as webapp.py's _resolve_doc
        if os.path.isfile(candidate):
            raw = open(candidate, encoding="utf-8").read()
            cleaned = chunk_diff.strip_boilerplate(raw)
            title_m = re.search(r"^#\s+(.+)$", cleaned, re.MULTILINE)
            return {
                "source_path": source_path,
                "title": title_m.group(1).strip() if title_m else None,
                "text": cleaned.strip(),
            }
    return {"error": f"no source file found for source_path='{source_path}'"}


def search_api_faq(query: str, n_results: int = 3):
    _lazy_init()
    res = _api_faq_coll.query(query_embeddings=[embed_query(query)], n_results=n_results)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "topic": meta.get("topic"),
            "question": meta.get("question"),
            "answer": meta.get("answer"),
        })
    return hits
