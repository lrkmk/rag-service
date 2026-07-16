"""
Shared search helpers against the Chroma store built by ingest_help_center.py.
Imported by both query_example.py (fixed demo queries) and ask.py (CLI tool
for ad hoc natural-language questions).

BGE asymmetric embedding note:
  BAAI/bge-large-zh-v1.5 (used in ingest_help_center.py) recommends prefixing
  *queries* with an instruction string, but leaving *documents* unprefixed.
  Chroma's `query_texts=` would embed the query with the exact same
  (unprefixed) code path used for documents, silently losing that signal.
  So here we load the model directly, encode the query with the prefix
  ourselves, and pass `query_embeddings=` instead of `query_texts=`.
"""

import json
import os
import re
import sys

import chromadb
from sentence_transformers import SentenceTransformer

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# chunk_diff.py lives in the sibling chunking/ directory, not here -- it's a
# chunking-QA tool by primary purpose, but get_full_article() below also
# needs its strip_boilerplate() at runtime. Add it to sys.path explicitly
# rather than relying on same-directory import discovery.
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "chunking"))
import chunk_diff  # noqa: E402

DB_PATH = os.path.join(REPO_ROOT, "chroma_db")
PARENTS_LOOKUP_PATH = os.path.join(REPO_ROOT, "scripts", "ingest", "parents_lookup.json")
HELP_CENTER_ROOT = os.path.join(REPO_ROOT, "doc", "帮助中心")
API_DOCS_ROOT = os.path.join(REPO_ROOT, "doc", "API文档")
PRODUCT_INTRO_ROOT = os.path.join(REPO_ROOT, "doc", "产品介绍")

# Must match the model used in ingest_help_center.py's EMBEDDER — the two sides
# have to produce vectors in the same space.
MODEL_NAME = "BAAI/bge-large-zh-v1.5"
QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："

_model = None
_client = None
_rule_coll = None
_faq_coll = None
_api_coll = None
_api_faq_coll = None
_intro_coll = None
_news_coll = None
_parents = None


def _lazy_init():
    global _model, _client, _rule_coll, _faq_coll, _api_coll, _api_faq_coll, _intro_coll, _news_coll, _parents
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
    intro_coll = client.get_collection(name="atlas_intro_chunks")
    news_coll = client.get_collection(name="atlas_news_chunks")
    with open(PARENTS_LOOKUP_PATH, encoding="utf-8") as f:
        parents = json.load(f)

    _model, _client = model, client
    _rule_coll, _faq_coll, _api_coll, _api_faq_coll = rule_coll, faq_coll, api_coll, api_faq_coll
    _intro_coll, _news_coll = intro_coll, news_coll
    _parents = parents


def embed_query(text: str) -> list[float]:
    _lazy_init()
    return _model.encode(QUERY_INSTRUCTION + text, normalize_embeddings=True).tolist()


def search_rules(
    query: str,
    n_results: int = 3,
    where: dict | None = None,
    query_embedding: list[float] | None = None,
):
    _lazy_init()
    embedding = query_embedding if query_embedding is not None else embed_query(query)
    res = _rule_coll.query(query_embeddings=[embedding], n_results=n_results, where=where)
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


def search_faq(query: str, n_results: int = 3, query_embedding: list[float] | None = None):
    _lazy_init()
    embedding = query_embedding if query_embedding is not None else embed_query(query)
    res = _faq_coll.query(query_embeddings=[embedding], n_results=n_results)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "topic": meta.get("topic"),
            "level1_category": meta.get("level1_category"),
            "level2_category": meta.get("level2_category"),
            "question": meta.get("question"),
            "answer": meta.get("answer"),
            "source_path": meta.get("source_path"),
        })
    return hits


def search_api_docs(
    query: str,
    n_results: int = 3,
    where: dict | None = None,
    query_embedding: list[float] | None = None,
):
    """Search API文档 (developer/API reference corpus) — separate collection
    from 帮助中心 on purpose, see RAG-切片设计总览.md. No parent-summary
    bolt-on here: API文档 chunks have no parent tier (the C-type "端点概览"
    chunk_type serves that role for OpenAPI endpoints, A/B-type chunks stand
    alone)."""
    _lazy_init()
    embedding = query_embedding if query_embedding is not None else embed_query(query)
    res = _api_coll.query(query_embeddings=[embedding], n_results=n_results, where=where)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        # `fields` is only present on C-type request/response/component chunks,
        # stored as a JSON string (Chroma metadata can't hold nested objects
        # directly — see clean_meta() in ingest_api_docs.py). It's the full,
        # uncollapsed field list that `text` intentionally trims for deeply
        # nested fields (chunk_api_reference.py's format_fields_for_text) —
        # read this when `text` says "还有 N 个嵌套子字段...见 fields" instead
        # of re-fetching or guessing at the missing sub-fields.
        fields_raw = meta.get("fields")
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
            "fields": json.loads(fields_raw) if fields_raw else None,
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

    Tries all corpus roots since source_path alone doesn't say which one
    it came from (the roots use the same relative-path convention)."""
    for root in (HELP_CENTER_ROOT, API_DOCS_ROOT, PRODUCT_INTRO_ROOT):
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


def search_product_intro(query: str, n_results: int = 3, query_embedding: list[float] | None = None):
    """Search 产品总览 (Atlas product overview + 10 role-based guide pages)
    — evergreen concept prose, no recency handling needed (contrast with
    search_product_news below)."""
    _lazy_init()
    embedding = query_embedding if query_embedding is not None else embed_query(query)
    res = _intro_coll.query(query_embeddings=[embedding], n_results=n_results)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "title": meta.get("title"),
            "section": meta.get("section"),
            "text": meta.get("text"),
            "source_path": meta.get("source_path"),
        })
    return hits


def search_product_news(query: str, n_results: int = 3, query_embedding: list[float] | None = None):
    """Search Atlas资讯 (product news/announcements) — unlike every other
    search_* here, this corpus can have MULTIPLE posts about the same
    subject where a later one supersedes an earlier one's conclusion (e.g.
    "精神航空停运" followed later by "精神航空已恢复运营"). Returning both
    un-ranked would let a stale announcement outrank the current status.

    Fix: over-fetch candidates, then collapse by entity_tags — when two
    candidates share an entity (an airline/product code extracted from the
    title, e.g. "NK"), keep only the one with the lower recency_rank (site's
    own listing order; 1 = newest — see chunk_product_news.py for why an
    ordinal rank is used instead of a real timestamp). Candidates with no
    entity_tags (one-off posts, not part of a recurring status thread) are
    never collapsed against each other.
    """
    _lazy_init()
    embedding = query_embedding if query_embedding is not None else embed_query(query)
    fetch_n = max(n_results * 4, 12)
    res = _news_coll.query(query_embeddings=[embedding], n_results=fetch_n)
    candidates = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        entity_tags_raw = meta.get("entity_tags", "")
        try:
            entity_tags = json.loads(entity_tags_raw) if entity_tags_raw else []
        except (json.JSONDecodeError, TypeError):
            entity_tags = []
        candidates.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "title": meta.get("title"),
            "entity_tags": entity_tags,
            "recency_rank": meta.get("recency_rank"),
            "text": meta.get("text"),
            "source_path": meta.get("source_path"),
        })

    kept: list[dict] = []
    best_rank_by_entity: dict[str, int] = {}
    for c in candidates:
        tags = c["entity_tags"]
        if not tags:
            kept.append(c)
            continue
        # Has this entity already been kept by a MORE recent post? Skip.
        superseded = any(tag in best_rank_by_entity and best_rank_by_entity[tag] < c["recency_rank"] for tag in tags)
        if superseded:
            continue
        # This is the most recent post seen so far for all its entities —
        # drop any already-kept OLDER posts about the same entity, then keep this one.
        kept = [k for k in kept if not (set(k.get("entity_tags", [])) & set(tags))]
        for tag in tags:
            best_rank_by_entity[tag] = c["recency_rank"]
        kept.append(c)

    kept.sort(key=lambda c: c["distance"])
    return kept[:n_results]


def search_api_faq(query: str, n_results: int = 3, query_embedding: list[float] | None = None):
    _lazy_init()
    embedding = query_embedding if query_embedding is not None else embed_query(query)
    res = _api_faq_coll.query(query_embeddings=[embedding], n_results=n_results)
    hits = []
    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]
        hits.append({
            "chunk_id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "topic": meta.get("topic"),
            "doc_type": meta.get("doc_type"),
            "level1_category": meta.get("level1_category"),
            "level2_category": meta.get("level2_category"),
            "question": meta.get("question"),
            "answer": meta.get("answer"),
            "source_path": meta.get("source_path"),
        })
    return hits


def search_help_center_context(
    query: str,
    n_results: int = 3,
    faq_n_results: int = 2,
    where: dict | None = None,
) -> dict:
    """Return Help Center rules and related FAQ in separately labelled lists.

    The two result types are not mixed into one rank: rule chunks embed a
    section plus its content, whereas FAQ chunks embed only the question, so
    their distance values are not calibrated against each other.
    """
    embedding = embed_query(query)
    standard_results = search_rules(
        query, n_results=n_results, where=where, query_embedding=embedding
    )
    faq_results = search_faq(query, n_results=faq_n_results, query_embedding=embedding)
    return {
        "query": query,
        "standard_results": standard_results,
        "faq_results": faq_results,
        "retrieval_summary": {
            "standard_count": len(standard_results),
            "faq_count": len(faq_results),
            "faq_note": "FAQ is supplementary evidence; use the standard policy/rule result as authoritative context when both apply.",
        },
    }


def search_all(query: str, n_results: int = 2, faq_n_results: int = 1) -> dict:
    """Fan a single query out across all three corpora (帮助中心/API文档/
    产品介绍) in one embedding pass, returning a small top-k from each
    labeled separately -- for when it isn't clear up front which corpus
    actually has the answer.

    This exists because corpus routing was being done by guessing: an
    agent would judge a question as "policy" vs "technical" vs "product"
    and search only that one corpus, and sometimes guess wrong when a
    question's real answer lived in a different corpus than the one that
    looked most likely on its face. Re-embedding the query per corpus would
    make a fan-out expensive, so this computes the embedding once and reuses
    it across all 6 underlying collection queries -- the added cost over a
    single-corpus search is a handful of cheap local vector lookups, not
    another model inference pass.

    Deliberately keeps n_results small per corpus (default 2 standard + 1
    FAQ each) since the point is breadth across corpora, not depth within
    one -- call the corpus-specific search_*_context tool with a higher
    top_k once you know which corpus actually has the answer.
    """
    _lazy_init()
    embedding = embed_query(query)
    return {
        "query": query,
        "帮助中心": {
            "standard_results": search_rules(query, n_results=n_results, query_embedding=embedding),
            "faq_results": search_faq(query, n_results=faq_n_results, query_embedding=embedding),
        },
        "API文档": {
            "standard_results": search_api_docs(query, n_results=n_results, query_embedding=embedding),
            "faq_results": search_api_faq(query, n_results=faq_n_results, query_embedding=embedding),
        },
        "产品介绍": {
            "product_intro_results": search_product_intro(query, n_results=n_results, query_embedding=embedding),
            "product_news_results": search_product_news(query, n_results=n_results, query_embedding=embedding),
        },
    }


def search_api_docs_context(
    query: str,
    n_results: int = 3,
    faq_n_results: int = 2,
    where: dict | None = None,
) -> dict:
    """Return API documentation and troubleshooting FAQ as labelled evidence."""
    embedding = embed_query(query)
    standard_results = search_api_docs(
        query, n_results=n_results, where=where, query_embedding=embedding
    )
    faq_results = search_api_faq(query, n_results=faq_n_results, query_embedding=embedding)
    return {
        "query": query,
        "standard_results": standard_results,
        "faq_results": faq_results,
        "retrieval_summary": {
            "standard_count": len(standard_results),
            "faq_count": len(faq_results),
            "faq_note": "FAQ is supplementary troubleshooting guidance; use API documentation for endpoint and field definitions.",
        },
    }
