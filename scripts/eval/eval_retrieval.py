"""
Run the eval/*.jsonl golden query sets (see build_eval_set.py) against
rag_search's search_* functions and report Recall@k / MRR per corpus.

Usage:
    python eval_retrieval.py                    # all 3 corpora, k=3 and k=5
    python eval_retrieval.py --corpus 帮助中心   # just one
    python eval_retrieval.py --sample 50         # subsample for a fast run
"""
import argparse
import glob
import json
import os
import random
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVAL_DIR = os.path.join(REPO_ROOT, "eval")

# rag_search.py lives in the sibling search/ directory, not here -- add it to
# sys.path explicitly rather than relying on same-directory import discovery.
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "search"))
import rag_search  # noqa: E402

TOOL_FNS = {
    "search_rules": rag_search.search_rules,
    "search_faq": rag_search.search_faq,
    "search_api_docs": rag_search.search_api_docs,
    "search_api_faq": rag_search.search_api_faq,
    "search_product_intro": rag_search.search_product_intro,
    "search_product_news": rag_search.search_product_news,
}

K_VALUES = (3, 5)


def load_jsonl(path):
    with open(path, encoding="utf-8-sig") as f:
        return [json.loads(l) for l in f if l.strip()]


def eval_corpus(name, rows, max_k):
    hits_at_k = {k: 0 for k in K_VALUES}
    reciprocal_ranks = []
    misses = []
    by_tier = {}
    article_hits, article_n = 0, 0

    for row in rows:
        fn = TOOL_FNS[row["tool"]]
        results = fn(row["query"], n_results=max_k)
        result_ids = [r["chunk_id"] for r in results]
        expected = set(row["expected_chunk_ids"])

        rank = next((i + 1 for i, rid in enumerate(result_ids) if rid in expected), None)
        reciprocal_ranks.append(1.0 / rank if rank else 0.0)
        for k in K_VALUES:
            if rank and rank <= k:
                hits_at_k[k] += 1

        tier = row.get("tier", "chunk")
        by_tier.setdefault(tier, {"n": 0, "hit5": 0})
        by_tier[tier]["n"] += 1
        if rank and rank <= 5:
            by_tier[tier]["hit5"] += 1

        # Looser article-level check: did we get ANY chunk from the same
        # source article in top-5, even if not the exact expected chunk_id?
        # A user is usually well served by a sibling section of the right
        # article, not just the one literal chunk this query was derived
        # from — strict chunk-id matching alone understates real usefulness,
        # especially for generic-sounding sections like "概述"/"常见问题".
        exp_src = row.get("expected_source_path")
        if exp_src:
            article_n += 1
            if any(r.get("source_path") == exp_src for r in results[:5]):
                article_hits += 1

        if not rank:
            misses.append(row)

    n = len(rows)
    print(f"\n=== {name} (n={n}) ===")
    for k in K_VALUES:
        print(f"  Recall@{k}: {hits_at_k[k]}/{n} = {hits_at_k[k]/n:.1%}")
    print(f"  MRR: {sum(reciprocal_ranks)/n:.3f}")
    for tier, s in by_tier.items():
        print(f"  [{tier}] Recall@5: {s['hit5']}/{s['n']} = {s['hit5']/s['n']:.1%}")
    if article_n:
        print(f"  Article-level Recall@5 (same source article, any chunk): {article_hits}/{article_n} = {article_hits/article_n:.1%}")

    summary = {
        "name": name,
        "n": n,
        "recall_at_k": {k: hits_at_k[k] / n for k in K_VALUES},
        "mrr": sum(reciprocal_ranks) / n,
        "article_recall5": (article_hits / article_n) if article_n else None,
    }
    return misses, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", choices=["帮助中心", "API文档", "产品介绍"], default=None)
    parser.add_argument("--sample", type=int, default=None, help="Random-subsample each corpus to N queries (fast run)")
    parser.add_argument("--show-misses", type=int, default=10, help="Print up to N missed queries per corpus")
    args = parser.parse_args()

    corpora = [args.corpus] if args.corpus else ["帮助中心", "API文档", "产品介绍"]
    all_misses = {}
    summaries = []

    t0 = time.time()
    for name in corpora:
        path = os.path.join(EVAL_DIR, f"{name}_eval.jsonl")
        if not os.path.exists(path):
            print(f"{name}: no eval set found at {path}, run build_eval_set.py first")
            continue
        rows = load_jsonl(path)
        if args.sample and len(rows) > args.sample:
            rows = random.sample(rows, args.sample)
        misses, summary = eval_corpus(name, rows, max_k=max(K_VALUES))
        all_misses[name] = misses
        summaries.append(summary)

    print(f"\n(total eval time: {time.time()-t0:.0f}s)")

    if summaries:
        print("\n| 语料库 | Recall@3 | Recall@5 | MRR | 文章级Recall@5 |")
        print("|---|---|---|---|---|")
        for s in summaries:
            article = f"{s['article_recall5']:.1%}" if s["article_recall5"] is not None else "—"
            print(f"| {s['name']} (n={s['n']}) | {s['recall_at_k'][3]:.1%} | {s['recall_at_k'][5]:.1%} | {s['mrr']:.3f} | {article} |")

    for name, misses in all_misses.items():
        if not misses:
            continue
        print(f"\n=== {name}: sample misses (showing up to {args.show_misses}/{len(misses)}) ===")
        for row in misses[: args.show_misses]:
            print(f"  [{row['tool']}] {row['query']!r} -> expected {row['expected_chunk_ids']}")


if __name__ == "__main__":
    main()
