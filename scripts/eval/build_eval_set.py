"""
Build golden query->expected_chunk_ids eval sets for Recall@k/MRR scoring,
one per corpus, without hand-labeling: every chunk already carries a natural-
language identifier (a FAQ's `question`, or a `title`/`section` pair), so
searching for that text and checking whether the chunk finds itself is a
free, always-fresh eval set that regenerates whenever the corpus changes.

Two query strategies:
  1. Chunk-level self-retrieval (all 3 corpora, every doc_type): query = the
     chunk's own question/section+title text, expected = [that chunk_id].
     Cheap, uniform, good for regression detection.
  2. Article-level, 帮助中心 only: for parent articles whose title is itself
     a real user question (source_path stem ends in "？"), query = the
     title, expected = ALL of that parent's child_chunk_ids (any one of them
     counts as a hit) — this is the more realistic test, matches the actual
     zytp-c01 incident this eval set was motivated by.

Atlas资讯 (产品介绍) needs special handling: search_product_news
deliberately suppresses superseded posts about the same entity (see
rag_search.search_product_news), so a chunk whose entity has since been
superseded should NOT expect to find itself — it should expect to find
whichever chunk is currently the most recent for that entity. Scoring self
instead of current would mark correct suppression as a failure.

Usage:
    python build_eval_set.py  # writes eval/*.jsonl
"""
import glob
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC_ROOT = os.path.join(REPO_ROOT, "doc")
EVAL_DIR = os.path.join(REPO_ROOT, "eval")


def load_jsonl(path):
    with open(path, encoding="utf-8-sig") as f:
        return [json.loads(l) for l in f if l.strip()]


def query_for(rec):
    """Most specific natural-language text available on a record.

    C-type (chunk_api_reference.py) and 对比消歧 (chunk_disambiguation.py)
    records carry no `title` field at all — falling back straight to
    `section` alone produces near-duplicate queries like "概述"/"常见问题"/
    "最佳实践" shared by dozens of unrelated articles (every guide has an
    "概述" section, every disambiguation doc has "常见问题"), which no
    retrieval system could disambiguate. Use whatever specific identifier
    IS present instead: compares (对比消歧's "A vs B"), endpoint (C-type's
    API path), or level2_category (usually the source article's own topic
    name) — in that order — before falling back to section alone."""
    if rec.get("question"):
        return rec["question"]
    title = (
        rec.get("title")
        or rec.get("parent_title")
        or (" vs ".join(rec["compares"]) if rec.get("compares") else "")
        or rec.get("endpoint")
        or rec.get("level2_category")
        or ""
    )
    section = rec.get("section") or ""
    if title and section and section not in title:
        return f"{title} {section}"
    return title or section


# ==================== 帮助中心 ====================

def build_bangzhu():
    rows = []
    # tier 1: chunk-level self-retrieval, rule chunks
    for fp in glob.glob(os.path.join(DOC_ROOT, "帮助中心", "**", "children.jsonl"), recursive=True):
        parent_fp = os.path.join(os.path.dirname(fp), "parents.jsonl")
        parents_by_id = {}
        if os.path.exists(parent_fp):
            parents_by_id = {p["article_id"]: p for p in load_jsonl(parent_fp)}
        for rec in load_jsonl(fp):
            parent = parents_by_id.get(rec.get("parent_id"), {})
            rec2 = dict(rec)
            rec2["title"] = parent.get("title")
            q = query_for(rec2)
            if not q:
                continue
            rows.append({"query": q, "tool": "search_rules", "expected_chunk_ids": [rec["chunk_id"]], "tier": "chunk",
                         "expected_source_path": parent.get("source_path")})

    # tier 1b: FAQ self-retrieval
    for fp in glob.glob(os.path.join(DOC_ROOT, "帮助中心", "10-常见问题", "_rag-chunks", "*.jsonl")):
        for rec in load_jsonl(fp):
            if not rec.get("question"):
                continue
            rows.append({"query": rec["question"], "tool": "search_faq", "expected_chunk_ids": [rec["chunk_id"]], "tier": "faq",
                         "expected_source_path": rec.get("source_path")})

    # tier 2: article-level, question-titled parents ("如何XX？")
    for fp in glob.glob(os.path.join(DOC_ROOT, "帮助中心", "**", "parents.jsonl"), recursive=True):
        for p in load_jsonl(fp):
            title = p.get("title", "")
            if not (title.endswith("？") or title.endswith("?")):
                continue
            if not p.get("child_chunk_ids"):
                continue
            rows.append({"query": title, "tool": "search_rules", "expected_chunk_ids": p["child_chunk_ids"], "tier": "article",
                         "expected_source_path": p.get("source_path")})

    return rows


# ==================== API文档 ====================

def build_apiwendang():
    rows = []
    # children.jsonl -> ingest_chunks() -> atlas_api_chunks, ALWAYS search_api_docs.
    # A minority of these records happen to carry doc_type=="FAQ" too (an
    # inline "常见问题" section within an otherwise-regular hand-chunked
    # article, e.g. sbxtest-c02) — that doc_type value describes the
    # SECTION's nature, not which collection it landed in. Routing on
    # doc_type alone sent these to search_api_faq, which queries a
    # different, separate collection they were never ingested into —
    # guaranteed misses that had nothing to do with retrieval quality.
    for fp in glob.glob(os.path.join(DOC_ROOT, "API文档", "**", "children.jsonl"), recursive=True):
        for rec in load_jsonl(fp):
            q = query_for(rec)
            if not q:
                continue
            rows.append({"query": q, "tool": "search_api_docs", "expected_chunk_ids": [rec["chunk_id"]], "tier": "chunk",
                         "doc_type": rec.get("doc_type"), "expected_source_path": rec.get("source_path")})

    # The REAL FAQ collection (atlas_api_faq_chunks) is populated only from
    # troubleshooting-faqs/_rag-chunks/faq-chunks.jsonl via ingest_faq() —
    # a different filename, not children.jsonl, so the loop above never
    # touches it.
    for fp in glob.glob(os.path.join(DOC_ROOT, "API文档", "**", "faq-chunks.jsonl"), recursive=True):
        for rec in load_jsonl(fp):
            if not rec.get("question"):
                continue
            rows.append({"query": rec["question"], "tool": "search_api_faq", "expected_chunk_ids": [rec["chunk_id"]], "tier": "faq",
                         "expected_source_path": rec.get("source_path")})
    return rows


# ==================== 产品介绍 ====================

def build_chanpin():
    rows = []
    intro_fp = os.path.join(DOC_ROOT, "产品介绍", "产品总览", "_rag-chunks", "children.jsonl")
    if os.path.exists(intro_fp):
        for rec in load_jsonl(intro_fp):
            q = query_for(rec)
            if q:
                rows.append({"query": q, "tool": "search_product_intro", "expected_chunk_ids": [rec["chunk_id"]], "tier": "chunk",
                             "expected_source_path": rec.get("source_path")})

    news_fp = os.path.join(DOC_ROOT, "产品介绍", "Atlas资讯", "_rag-chunks", "children.jsonl")
    if os.path.exists(news_fp):
        news = load_jsonl(news_fp)
        # entity -> chunk_id with the lowest (= most recent) recency_rank
        best_by_entity = {}
        for rec in news:
            for tag in rec.get("entity_tags", []):
                cur = best_by_entity.get(tag)
                if cur is None or rec["recency_rank"] < cur[1]:
                    best_by_entity[tag] = (rec["chunk_id"], rec["recency_rank"])
        for rec in news:
            q = query_for(rec)
            if not q:
                continue
            tags = rec.get("entity_tags", [])
            if tags:
                # expected = whichever chunk is currently "latest" for any of
                # this post's entities, NOT necessarily this post itself —
                # search_product_news is supposed to surface only the latest.
                expected = sorted({best_by_entity[t][0] for t in tags if t in best_by_entity})
            else:
                expected = [rec["chunk_id"]]
            rows.append({"query": q, "tool": "search_product_news", "expected_chunk_ids": expected, "tier": "chunk",
                         "expected_source_path": rec.get("source_path")})

    return rows


def main():
    os.makedirs(EVAL_DIR, exist_ok=True)
    builders = {
        "帮助中心": build_bangzhu,
        "API文档": build_apiwendang,
        "产品介绍": build_chanpin,
    }
    for name, fn in builders.items():
        rows = fn()
        out_path = os.path.join(EVAL_DIR, f"{name}_eval.jsonl")
        with open(out_path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{name}: {len(rows)} eval queries -> {out_path}")


if __name__ == "__main__":
    main()
