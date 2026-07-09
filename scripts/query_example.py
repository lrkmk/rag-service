"""
Fixed demo queries against the Chroma store built by ingest_chroma.py.
For ad hoc natural-language questions, use `ask.py` instead.

Run `python ingest_chroma.py` first. Then:
    python query_example.py

Shows three patterns:
  1. Plain semantic search over rule chunks, with a parent summary bolted on.
  2. Same search pre-filtered by applicable_carrier (航司精确匹配 fallback 通用).
  3. FAQ search (embeds the question only, returns the stored answer).
"""

from rag_search import search_faq, search_rules

if __name__ == "__main__":
    print("=== 1. Plain semantic search ===")
    for h in search_rules("退票超过多久Atlas就不再处理了"):
        print(f"- [{h['distance']:.3f}] {h['section']} (parent: {h['parent_title']})")
        print(f"  {h['text'][:80]}...")

    print("\n=== 2. Filtered by carrier (FR-specific retrieval) ===")
    for h in search_rules(
        "航班提前多久可以非自愿退票",
        where={"applicable_carrier": "FR"},
    ):
        print(f"- [{h['distance']:.3f}] {h['section']}")
        print(f"  {h['text'][:80]}...")

    print("\n=== 3. FAQ search ===")
    for h in search_faq("出票要多长时间"):
        print(f"- [{h['distance']:.3f}] Q: {h['question']}")
        print(f"  A: {h['answer'][:80]}...")
