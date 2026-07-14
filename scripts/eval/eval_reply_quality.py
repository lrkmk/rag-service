"""
Build the context bundle needed to grade real-conversation replies for
factual accuracy against the docs corpus.

For each {question, answer} record this calls the deployed MCP service's
search_* tools (over streamable-http — no local chromadb/sentence-transformers
needed), pools the hits by distance, dedupes by source_path, and keeps the
top --top-k as reference context. This script does NOT judge anything itself
— grading requires actual reading comprehension (does the answer's claims
match the retrieved text?), which belongs to an LLM/agent, not a heuristic.
Feed the output to an agent (or a human) with a prompt like:

    对每条记录判断 Eva 的回复 (a) 是否被 context 里的片段支持:
    - verdict: 正确 / 部分正确 / 有事实错误 / 无法判断（context 不足以验证）
    - issues: 具体指出回复里哪句话查不到依据或和文档冲突
    - evidence_source_path: 支持判断的 source_path

Usage:
    python eval_reply_quality.py --input records.json --output judge_input.json \
        --mcp-url https://ai-test.atlastravel.tech/mcp

Input records.json: [{"q": "...", "a": "...", "traceId": "...", ...}, ...]
Output adds a "context" field per record: [{"source_path", "snippet", "distance"}, ...]
"""
import argparse
import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# (tool_name, top_k) — search_product_news skipped on purpose: none of the
# real-conversation traffic this was built for is news/status related, and
# its recency-collapsing logic isn't relevant to grading a static answer.
TOOLS = [
    ("search_help_center", 3),
    ("search_help_center_faq", 3),
    ("search_api_docs", 5),
    ("search_api_docs_faq", 3),
    ("search_product_intro", 2),
]


async def build_context(session: ClientSession, query: str, top_k: int) -> list[dict]:
    pooled = []
    for tool_name, n in TOOLS:
        result = await session.call_tool(tool_name, {"query": query, "top_k": n})
        # Each hit comes back as its own TextContent block (not one JSON
        # array in content[0]) — confirmed by inspecting result.content.
        for block in result.content:
            hit = json.loads(block.text)
            if "question" in hit and "answer" in hit:
                # FAQ-shaped hit: no standalone "text" field, the Q/A pair
                # itself is the snippet.
                snippet = f"Q: {hit.get('question')}\nA: {hit.get('answer')}"
            else:
                snippet = hit.get("text") or ""
            pooled.append({
                "source_path": hit.get("source_path"),
                "distance": hit.get("distance"),
                "snippet": snippet,
            })

    pooled.sort(key=lambda h: h["distance"] if h["distance"] is not None else 999)

    deduped = []
    seen_paths = set()
    for h in pooled:
        key = h["source_path"]
        if key in seen_paths:
            continue
        seen_paths.add(key)
        deduped.append(h)
        if len(deduped) >= top_k:
            break
    return deduped


async def run(input_path: str, output_path: str, mcp_url: str, top_k: int):
    with open(input_path, encoding="utf-8") as f:
        records = json.load(f)

    enriched = []
    async with streamablehttp_client(mcp_url) as (read, write, _get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for i, r in enumerate(records, 1):
                context = await build_context(session, r["q"], top_k)
                enriched.append({**r, "context": context})
                print(f"[{i}/{len(records)}] {r['q'][:40]!r} -> {len(context)} context chunks")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=1)
    print(f"\nWrote {len(enriched)} records to {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="records.json path")
    parser.add_argument("--output", required=True, help="where to write the enriched judge_input.json")
    parser.add_argument("--mcp-url", default="https://ai-test.atlastravel.tech/mcp", help="deployed MCP service URL")
    parser.add_argument("--top-k", type=int, default=8, help="max context chunks per record (default 8)")
    args = parser.parse_args()
    asyncio.run(run(args.input, args.output, args.mcp_url, args.top_k))


if __name__ == "__main__":
    main()
