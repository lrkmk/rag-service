"""
Ingest Atlas help-center RAG chunks (帮助中心/**/_rag-chunks/) into a local
Chroma vector store.

Design (see 帮助中心/_rag-chunks-index.md for the source schema):
  - Only *children* (rule-unit chunks) and *FAQ* QA pairs are embedded.
  - *Parents* are never embedded — they're written to a flat JSON lookup
    (parents_lookup.json) that the app reads by article_id at query time,
    after a child hit tells it which article to pull context from.
  - The 131-carrier refund time-limit table is NOT ingested here — it's a
    lookup table, not a semantic-search corpus. Query it directly from
    帮助中心/04-售后票务/退票/_rag-chunks/退票时限结构化表.json.
  - Rule chunks are enriched with level1_category/level2_category pulled
    from their parent record, so category filters work at query time
    without needing a join (Chroma metadata filters can't join collections).

Usage:
    pip install chromadb sentence-transformers
    python ingest_chroma.py

Re-running is safe: everything is upserted by chunk_id, so this is
idempotent — you can just re-run after re-generating the source jsonl files.
"""

import glob
import json
import os
import time

import chromadb
from chromadb.utils import embedding_functions

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HELP_CENTER = os.path.join(REPO_ROOT, "帮助中心")
DB_PATH = os.path.join(REPO_ROOT, "chroma_db")
PARENTS_LOOKUP_PATH = os.path.join(REPO_ROOT, "scripts", "parents_lookup.json")

MODEL_NAME = "BAAI/bge-large-zh-v1.5"


def _build_embedder():
    """Try HF_HUB_OFFLINE first if the model looks cached, to skip the
    network round-trip entirely — on a server with a slow/unstable path to
    huggingface.co, that round-trip (an etag/freshness check hit even when
    files are already cached) can hang for a long time after the weights
    finish downloading, which reads as "stuck" with no indication that it's
    actually a network wait rather than the CPU embedding step. Only used
    when a cache hit is likely; falls back to a normal (online) load
    otherwise so the very first run still downloads normally.
    """
    cache_hint = os.path.expanduser("~/.cache/huggingface/hub/models--BAAI--bge-large-zh-v1.5")
    if os.path.isdir(cache_hint) and "HF_HUB_OFFLINE" not in os.environ:
        os.environ["HF_HUB_OFFLINE"] = "1"
        try:
            return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
        except Exception:
            # Cache dir existed but wasn't actually complete/usable — fall
            # back to a normal online load rather than failing outright.
            del os.environ["HF_HUB_OFFLINE"]
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)


# Chroma's built-in default embedder (all-MiniLM-L6-v2) is English-tuned and
# performs poorly on Chinese text. This corpus is ~100% Chinese policy/FAQ
# text, so a Chinese-specific model (BGE) outperforms a general multilingual
# one. BGE's own docs recommend embedding *documents* (what we do here, at
# ingest time) with no special prefix — the asymmetric instruction prefix
# only applies to *queries*, handled separately in query_example.py.
# Swap for embedding_functions.OpenAIEmbeddingFunction(...) or another
# provider if you'd rather call a hosted API than run local inference.
EMBEDDER = _build_embedder()


def load_jsonl(path):
    with open(path, encoding="utf-8-sig") as f:
        return [json.loads(line) for line in f if line.strip()]


def clean_meta(d: dict) -> dict:
    """Chroma metadata values must be str/int/float/bool — no None, no nested objects."""
    out = {}
    for k, v in d.items():
        if v is None:
            out[k] = ""
        elif isinstance(v, (str, int, float, bool)):
            out[k] = v
        else:
            out[k] = json.dumps(v, ensure_ascii=False)
    return out


def build_parents_index():
    """article_id -> full parent record, plus a slim (level1, level2) map for enrichment."""
    paths = glob.glob(os.path.join(HELP_CENTER, "**", "_rag-chunks", "parents.jsonl"), recursive=True)
    full = {}
    slim = {}
    for p in paths:
        for rec in load_jsonl(p):
            aid = rec["article_id"]
            full[aid] = rec
            slim[aid] = {
                "level1_category": rec.get("level1_category", ""),
                "level2_category": rec.get("level2_category", ""),
            }
    return full, slim


def ingest_rule_chunks(client, parents_slim):
    paths = glob.glob(os.path.join(HELP_CENTER, "**", "_rag-chunks", "children.jsonl"), recursive=True)
    coll = client.get_or_create_collection(name="atlas_rule_chunks", embedding_function=EMBEDDER)

    ids, docs, metas = [], [], []
    skipped = 0
    for p in paths:
        rel_dir = os.path.relpath(os.path.dirname(p), HELP_CENTER)
        for rec in load_jsonl(p):
            parent_cat = parents_slim.get(rec.get("parent_id"), {})
            if not parent_cat:
                skipped += 1  # orphaned child, still ingest but flag it
            # Embed section header + rule text together — bare rule text is
            # often too terse on its own (e.g. "航班提前1小时及以上：可退").
            doc_text = f"{rec.get('section', '')}\n{rec['text']}"
            ids.append(rec["chunk_id"])
            docs.append(doc_text)
            metas.append(clean_meta({
                "parent_id": rec.get("parent_id"),
                "level1_category": parent_cat.get("level1_category", ""),
                "level2_category": parent_cat.get("level2_category", ""),
                "section": rec.get("section"),
                "rule_type": rec.get("rule_type"),
                "applicable_carrier": rec.get("applicable_carrier"),
                "updated_at": rec.get("updated_at"),
                "text": rec["text"],
                "source_dir": rel_dir,
            }))

    if ids:
        print(f"[atlas_rule_chunks] embedding {len(ids)} chunks (CPU inference on a "
              f"large Chinese model can take several minutes with no output in between "
              f"— this is expected, not a hang)...", flush=True)
        t0 = time.time()
        coll.upsert(ids=ids, documents=docs, metadatas=metas)
        print(f"[atlas_rule_chunks] embedding done in {time.time() - t0:.0f}s")
    print(f"[atlas_rule_chunks] ingested {len(ids)} chunks from {len(paths)} files"
          + (f" ({skipped} had no matching parent record)" if skipped else ""))
    return coll


def ingest_faq_chunks(client):
    paths = glob.glob(os.path.join(HELP_CENTER, "10-常见问题", "_rag-chunks", "*.jsonl"))
    coll = client.get_or_create_collection(name="atlas_faq_chunks", embedding_function=EMBEDDER)

    ids, docs, metas = [], [], []
    for p in paths:
        for rec in load_jsonl(p):
            ids.append(rec["chunk_id"])
            # Embed the question only — user queries look like questions,
            # not like answers; embedding the answer too adds noise.
            docs.append(rec["question"])
            metas.append(clean_meta({
                "parent_id": rec.get("parent_id"),
                "topic": rec.get("topic"),
                "level1_category": rec.get("level1_category"),
                "level2_category": rec.get("level2_category"),
                "question": rec["question"],
                "answer": rec["answer"],
                "source_path": rec.get("source_path"),
            }))

    if ids:
        print(f"[atlas_faq_chunks] embedding {len(ids)} QA pairs...", flush=True)
        t0 = time.time()
        coll.upsert(ids=ids, documents=docs, metadatas=metas)
        print(f"[atlas_faq_chunks] embedding done in {time.time() - t0:.0f}s")
    print(f"[atlas_faq_chunks] ingested {len(ids)} QA pairs from {len(paths)} files")
    return coll


def main():
    os.makedirs(os.path.dirname(PARENTS_LOOKUP_PATH), exist_ok=True)
    client = chromadb.PersistentClient(path=DB_PATH)

    parents_full, parents_slim = build_parents_index()
    with open(PARENTS_LOOKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(parents_full, f, ensure_ascii=False, indent=2)
    print(f"[parents_lookup] wrote {len(parents_full)} article summaries -> {PARENTS_LOOKUP_PATH}")

    ingest_rule_chunks(client, parents_slim)
    ingest_faq_chunks(client)

    print(f"\nDone. Chroma DB persisted at: {DB_PATH}")


if __name__ == "__main__":
    main()
