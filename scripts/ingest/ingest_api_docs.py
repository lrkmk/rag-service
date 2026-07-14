"""
Ingest API文档 RAG chunks (API文档/**/_rag-chunks/) into the same local Chroma
store used by ingest_help_center.py, but into SEPARATE collections from the
帮助中心 ones — this corpus is developer/API reference content, not
customer-service policy content, and mixing them dilutes retrieval.

Two collections:
  - atlas_api_chunks     — all A/B/C-type children.jsonl records (719 records:
                            概念说明/操作步骤/对比消歧/端点概览/请求参数/
                            响应字段/响应组件/etc.)
  - atlas_api_faq_chunks — troubleshooting-faqs QA pairs (104 records)

Structured lookup tables (17 JSON files: error-code enums, locale/test-card/
test-route reference data, the payment-card requirement matrix) are NOT
ingested here — same rationale as 帮助中心's 退票时限结构化表.json: these are
exact-lookup data, not semantic-search content. They stay as plain JSON files
under their respective _rag-chunks/ folders for the app layer to query
directly (see RAG-切片设计总览.md).

Usage:
    python ingest_api_docs.py
"""

import glob
import json
import os
import time

import chromadb
from chromadb.utils import embedding_functions

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
API_DOCS_ROOT = os.path.join(REPO_ROOT, "doc", "API文档")
DB_PATH = os.path.join(REPO_ROOT, "chroma_db")

MODEL_NAME = "BAAI/bge-large-zh-v1.5"


def _build_embedder():
    """Same rationale as ingest_help_center.py's _build_embedder: prefer
    HF_HUB_OFFLINE when the model is already cached, so a slow/unstable
    path to huggingface.co can't hang on a post-download freshness check
    that looks identical to "still embedding" from the terminal."""
    cache_hint = os.path.expanduser("~/.cache/huggingface/hub/models--BAAI--bge-large-zh-v1.5")
    if os.path.isdir(cache_hint) and "HF_HUB_OFFLINE" not in os.environ:
        os.environ["HF_HUB_OFFLINE"] = "1"
        try:
            return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
        except Exception:
            del os.environ["HF_HUB_OFFLINE"]
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)


# Must match ingest_help_center.py's model choice so both corpora live in a
# consistent embedding space (not strictly required since they're separate
# collections, but keeps the whole pipeline using one model).
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


def ingest_chunks(client):
    paths = glob.glob(os.path.join(API_DOCS_ROOT, "**", "_rag-chunks", "children.jsonl"), recursive=True)
    coll = client.get_or_create_collection(name="atlas_api_chunks", embedding_function=EMBEDDER)

    ids, docs, metas = [], [], []
    for p in paths:
        rel_dir = os.path.relpath(os.path.dirname(p), API_DOCS_ROOT)
        for rec in load_jsonl(p):
            doc_text = f"{rec.get('section', '')}\n{rec['text']}"
            ids.append(rec["chunk_id"])
            docs.append(doc_text)
            metas.append(clean_meta({
                "doc_type": rec.get("doc_type"),
                "level1_category": rec.get("level1_category"),
                "level2_category": rec.get("level2_category"),
                "applicable_carrier": rec.get("applicable_carrier"),
                "compares": rec.get("compares"),  # only present on 对比消歧 chunks
                "endpoint": rec.get("endpoint"),   # only present on C-type chunks
                "section": rec.get("section"),
                "text": rec["text"],
                # Full recursively-flattened field list (chunk_api_reference.py's
                # flatten_fields) -- only present on C-type request/response/component
                # chunks. NOT part of `text`/`doc_text` above, so it never
                # participates in the embedding and can't be truncated out of the
                # match computation by BGE's max_seq_length=512 -- it just rides
                # along as metadata on every hit for whatever reads the result
                # afterward (see rag_search.py's search_api_docs), same pattern as
                # the 帮助中心 parent/child lookup for `text` that's too long to embed.
                "fields": rec.get("fields"),
                "source_path": rec.get("source_path"),
                "source_dir": rel_dir,
            }))

    if ids:
        print(f"[atlas_api_chunks] embedding {len(ids)} chunks (CPU inference on a large "
              f"Chinese model can take several minutes with no output in between — this "
              f"is expected, not a hang)...", flush=True)
        t0 = time.time()
        coll.upsert(ids=ids, documents=docs, metadatas=metas)
        print(f"[atlas_api_chunks] embedding done in {time.time() - t0:.0f}s")
    reconcile(coll, ids)
    print(f"[atlas_api_chunks] ingested {len(ids)} chunks from {len(paths)} files")
    return coll


def ingest_faq(client):
    path = os.path.join(API_DOCS_ROOT, "05-支持与参考", "troubleshooting-faqs", "_rag-chunks", "faq-chunks.jsonl")
    coll = client.get_or_create_collection(name="atlas_api_faq_chunks", embedding_function=EMBEDDER)

    if not os.path.exists(path):
        print("[atlas_api_faq_chunks] no faq-chunks.jsonl found, skipping")
        return coll

    ids, docs, metas = [], [], []
    for rec in load_jsonl(path):
        ids.append(rec["chunk_id"])
        docs.append(rec["question"])
        metas.append(clean_meta({
            "doc_type": rec.get("doc_type", "FAQ"),
            "level1_category": rec.get("level1_category"),
            "level2_category": rec.get("level2_category"),
            "topic": rec.get("topic"),
            "question": rec["question"],
            "answer": rec["answer"],
            "source_path": rec.get("source_path"),
        }))

    if ids:
        print(f"[atlas_api_faq_chunks] embedding {len(ids)} QA pairs...", flush=True)
        t0 = time.time()
        coll.upsert(ids=ids, documents=docs, metadatas=metas)
        print(f"[atlas_api_faq_chunks] embedding done in {time.time() - t0:.0f}s")
    reconcile(coll, ids)
    print(f"[atlas_api_faq_chunks] ingested {len(ids)} QA pairs")
    return coll


def main():
    client = chromadb.PersistentClient(path=DB_PATH)
    ingest_chunks(client)
    ingest_faq(client)
    print(f"\nDone. Structured lookup tables (17 files) were NOT ingested — "
          f"query them directly as JSON, see RAG-切片设计总览.md.")


if __name__ == "__main__":
    main()
