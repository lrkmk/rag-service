"""
Ingest doc/产品介绍 RAG chunks into two SEPARATE collections from both
帮助中心 and API文档 — per RAG-切片设计总览.md's rationale (mixing dilutes
retrieval), extended here: 产品介绍 also mixes two internally-different
content types (see chunk_product_intro.py / chunk_product_news.py), so they
get their own collections too rather than sharing one:

  - atlas_intro_chunks — 产品总览 (11 pages, evergreen concept prose, no
    recency handling needed).
  - atlas_news_chunks  — Atlas资讯 (32 announcements). Time-stamped, and the
    same subject can recur across multiple posts where a later one
    supersedes an earlier one's conclusion (e.g. "精神航空停运" then later
    "精神航空已恢复运营") — search_product_news() in rag_search.py handles
    this at query time via entity_tags + recency_rank, not here at ingest
    time; this script just stores what chunk_product_news.py produced.

Usage:
    python ingest_product_intro.py
"""
import glob
import json
import os
import time

import chromadb
from chromadb.utils import embedding_functions

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_INTRO_ROOT = os.path.join(REPO_ROOT, "doc", "产品介绍")
DB_PATH = os.path.join(REPO_ROOT, "chroma_db")

# BAAI/bge-m3 as of 2026-07-22 -- see rag_search.py's MODEL_NAME comment
# for the full switch rationale (mixed Chinese/English content matching).
MODEL_NAME = "BAAI/bge-m3"


def _build_embedder():
    """Same rationale as ingest_help_center.py's _build_embedder."""
    cache_hint = os.path.expanduser("~/.cache/huggingface/hub/models--BAAI--bge-m3")
    if os.path.isdir(cache_hint) and "HF_HUB_OFFLINE" not in os.environ:
        os.environ["HF_HUB_OFFLINE"] = "1"
        try:
            return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
        except Exception:
            del os.environ["HF_HUB_OFFLINE"]
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)


EMBEDDER = _build_embedder()


def load_jsonl(path):
    with open(path, encoding="utf-8-sig") as f:
        return [json.loads(l) for l in f if l.strip()]


def clean_meta(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if v is None:
            out[k] = ""
        elif isinstance(v, (str, int, float, bool)):
            out[k] = v
        else:
            out[k] = json.dumps(v, ensure_ascii=False)
    return out


def reconcile(coll, current_ids: list[str]):
    """Delete any id left in the collection that this run's source files
    didn't produce (doc deleted, or re-chunked with new chunk_ids) — see
    ingest_help_center.py's reconcile() for the full rationale. Skipped when
    current_ids is empty to avoid wiping the collection on a path/glob error.
    """
    if not current_ids:
        return
    existing_ids = set(coll.get(include=[])["ids"])
    stale_ids = existing_ids - set(current_ids)
    if stale_ids:
        coll.delete(ids=list(stale_ids))
        print(f"[{coll.name}] deleted {len(stale_ids)} stale ids no longer produced by source files")


def incremental_upsert(coll, ids: list[str], docs: list[str], metas: list[dict]):
    """Only (re-)embed ids whose document text actually changed since the
    last ingest — see ingest_help_center.py's incremental_upsert() for the
    full rationale. coll.upsert() re-embeds everything it's given regardless
    of whether the text changed, which used to force re-embedding the whole
    corpus for a one-line edit to a single source file.
    """
    if not ids:
        return
    existing = coll.get(ids=ids, include=["documents", "metadatas"])
    existing_docs = dict(zip(existing["ids"], existing["documents"]))
    existing_metas = dict(zip(existing["ids"], existing["metadatas"]))

    embed_ids, embed_docs, embed_metas = [], [], []
    meta_only_ids, meta_only_metas = [], []
    unchanged = 0
    for cid, doc, meta in zip(ids, docs, metas):
        if cid not in existing_docs or existing_docs[cid] != doc:
            embed_ids.append(cid)
            embed_docs.append(doc)
            embed_metas.append(meta)
        elif existing_metas.get(cid) != meta:
            meta_only_ids.append(cid)
            meta_only_metas.append(meta)
        else:
            unchanged += 1

    if embed_ids:
        print(f"[{coll.name}] embedding {len(embed_ids)} new/changed chunks "
              f"({unchanged} unchanged skipped, {len(meta_only_ids)} metadata-only)...", flush=True)
        t0 = time.time()
        coll.upsert(ids=embed_ids, documents=embed_docs, metadatas=embed_metas)
        print(f"[{coll.name}] embedding done in {time.time() - t0:.0f}s")
    if meta_only_ids:
        coll.update(ids=meta_only_ids, metadatas=meta_only_metas)
        print(f"[{coll.name}] updated metadata only for {len(meta_only_ids)} chunks (no re-embed)")
    if not embed_ids and not meta_only_ids:
        print(f"[{coll.name}] nothing changed, all {unchanged} chunks already up to date")


def ingest_intro(client):
    path = os.path.join(PRODUCT_INTRO_ROOT, "产品总览", "_rag-chunks", "children.jsonl")
    coll = client.get_or_create_collection(name="atlas_intro_chunks", embedding_function=EMBEDDER)
    if not os.path.exists(path):
        print("[atlas_intro_chunks] no children.jsonl found, skipping")
        return coll

    ids, docs, metas = [], [], []
    for rec in load_jsonl(path):
        doc_text = f"{rec.get('title', '')} {rec.get('section', '')}\n{rec['text']}"
        ids.append(rec["chunk_id"])
        docs.append(doc_text)
        metas.append(clean_meta({
            "doc_type": rec.get("doc_type"),
            "level1_category": rec.get("level1_category"),
            "level2_category": rec.get("level2_category"),
            "title": rec.get("title"),
            "section": rec.get("section"),
            "text": rec["text"],
            "source_path": rec.get("source_path"),
        }))

    incremental_upsert(coll, ids, docs, metas)
    reconcile(coll, ids)
    print(f"[atlas_intro_chunks] ingested {len(ids)} chunks")
    return coll


def ingest_news(client):
    path = os.path.join(PRODUCT_INTRO_ROOT, "Atlas资讯", "_rag-chunks", "children.jsonl")
    coll = client.get_or_create_collection(name="atlas_news_chunks", embedding_function=EMBEDDER)
    if not os.path.exists(path):
        print("[atlas_news_chunks] no children.jsonl found, skipping")
        return coll

    ids, docs, metas = [], [], []
    for rec in load_jsonl(path):
        doc_text = f"{rec.get('title', '')}\n{rec['text']}"
        ids.append(rec["chunk_id"])
        docs.append(doc_text)
        metas.append(clean_meta({
            "doc_type": rec.get("doc_type"),
            "level1_category": rec.get("level1_category"),
            "level2_category": rec.get("level2_category"),
            "title": rec.get("title"),
            "entity_tags": rec.get("entity_tags"),
            "recency_rank": rec.get("recency_rank"),
            "text": rec["text"],
            "source_path": rec.get("source_path"),
        }))

    incremental_upsert(coll, ids, docs, metas)
    reconcile(coll, ids)
    print(f"[atlas_news_chunks] ingested {len(ids)} chunks")
    return coll


def main():
    client = chromadb.PersistentClient(path=DB_PATH)
    ingest_intro(client)
    ingest_news(client)


if __name__ == "__main__":
    main()
