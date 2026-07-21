"""
MCP server exposing the Atlas documentation RAG store as tools an agent can
call directly, instead of shelling out to ask.py.

Wraps rag_search.py's search functions (帮助中心 rules/FAQ, API文档
chunks/FAQ) as MCP tools. Same BGE model, same asymmetric query-prefix
handling, same Chroma store — this is a thin protocol adapter, not a
reimplementation.

Local stdio mode (default — for `claude mcp add` / Claude Desktop, no network):
    python mcp_server.py

    Register with Claude Code:
        claude mcp add atlas-docs -- <path-to-venv-python> <path-to-this-file>

    Register with Claude Desktop, add to claude_desktop_config.json:
        {
          "mcpServers": {
            "atlas-docs": {
              "command": "<path-to-venv-python>",
              "args": ["<path-to-this-file>"]
            }
          }
        }

    Both need ABSOLUTE paths — MCP client processes don't inherit this
    project's venv activation or working directory.

Container / network mode (set by the Dockerfile, see ../Dockerfile):
    MCP_TRANSPORT=streamable-http MCP_PORT=8000 python mcp_server.py

    Then register as a remote MCP server, e.g. for Claude Code:
        claude mcp add --transport http atlas-docs http://<host>:8000/mcp
"""

import os
from typing import Optional

from mcp.server.fastmcp import FastMCP

import lookup_tables
import rag_search

TRANSPORT = os.environ.get("MCP_TRANSPORT", "stdio")
HOST = os.environ.get("MCP_HOST", "0.0.0.0")
PORT = int(os.environ.get("MCP_PORT", "8000"))

mcp = FastMCP("atlas-docs", host=HOST, port=PORT)


@mcp.tool()
def search_all(query: str) -> dict:
    """Search ALL THREE corpora at once (帮助中心 policy/FAQ, API文档
    integration docs/FAQ, 产品介绍 product overview/news) and return a small
    top-k from each, labeled by corpus.

    Use this FIRST when a question could plausibly be answered from more
    than one corpus, or when you're not confident which corpus applies —
    do not guess a single corpus and only fall back to search_all if that
    guess turns out wrong. Also use this if a corpus-specific search
    (search_help_center_context/search_api_docs_context/search_product_intro/
    search_product_news) came back with nothing that actually answers the
    question — that usually means the answer is in a different corpus, not
    that it doesn't exist.

    Once search_all shows you which corpus actually has the relevant
    content, switch to that corpus's *_context tool (search_help_center_context
    or search_api_docs_context) with a higher top_k for deeper results — this
    tool intentionally returns fewer results per corpus than a dedicated
    deep dive since its job is figuring out WHERE the answer lives, not
    exhausting it.

    top_k/faq_top_k are deliberately NOT caller-settable here (fixed at 5
    standard + 2 FAQ per corpus). They used to be, but trace analysis on
    2026-07-17 (question: "Atlas 的价格怎么计算？月费、交易费、附加服务费
    分别是多少？") caught the calling agent passing top_k=3&faq_top_k=1 —
    below even the pre-2026-07-16 default — which pushed the one chunk that
    actually answered the question (Fulfilment API 交易费说明) out of the
    returned results despite it existing in the corpus. A docstring telling
    the agent what to pass isn't enforcement; it can always choose a smaller
    number. Pinning the value here is. If a corpus-specific follow-up with
    the *_context tools (which do still take top_k) comes back empty even
    at a high top_k, that's a real documentation/chunking gap — not a
    reason to want a lower top_k on search_all.

    Args:
        query: Natural-language question, Chinese or English. If the
            question bundles multiple distinct asks (e.g. "月费、交易费、
            附加服务费分别是多少" = 3 separate asks), do not merge them
            into one query string — call search_all once per sub-question
            instead. A merged query dilutes the embedding toward none of
            the sub-topics specifically, which is a different failure mode
            from a too-small top_k but produces the same symptom (the
            right chunk doesn't come back).

    Returns:
        {query, 帮助中心: {standard_results, faq_results}, API文档:
        {standard_results, faq_results}, 产品介绍: {product_intro_results,
        product_news_results}}.
    """
    return rag_search.search_all(query, n_results=5, faq_n_results=2)


@mcp.tool()
def search_help_center_context(
    query: str,
    top_k: int = 3,
    faq_top_k: int = 2,
    carrier: Optional[str] = None,
) -> dict:
    """Search Help Center policy/rule documents and related FAQ together.

    Preferred Help Center search tool once you know the question is a
    Help Center question — if you're not sure yet, use search_all first
    instead of guessing. It always retrieves both types, so an agent does
    not need a second FAQ decision. Results are returned as
    ``standard_results`` and ``faq_results`` rather than a mixed ranking:
    their distance scores are not comparable because the two collections use
    different indexed text shapes.

    Standard results are authoritative for policy, conditions, and
    airline-specific rules; FAQ results are concise supplementary guidance.

    Args:
        query: Natural-language policy or operational question.
        top_k: Number of standard rule chunks (default 3).
        faq_top_k: Number of FAQ pairs (default 2).
        carrier: Optional airline IATA code, e.g. "FR" or "W6".
    """
    where = {"applicable_carrier": carrier} if carrier else None
    return rag_search.search_help_center_context(
        query, n_results=top_k, faq_n_results=faq_top_k, where=where
    )


@mcp.tool()
def search_api_docs_context(
    query: str,
    top_k: int = 3,
    faq_top_k: int = 2,
    doc_type: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> dict:
    """Search API documentation and troubleshooting FAQ together.

    Preferred API-documents search tool once you know the question is an
    API文档 question — if you're not sure yet, use search_all first instead
    of guessing. It returns labelled
    ``standard_results`` for integration guides/reference chunks and
    ``faq_results`` for concise troubleshooting guidance. Do not compare or
    mix their distance values: the indexed text differs between the two
    collections.

    Args:
        query: Natural-language integration or API question.
        top_k: Number of API-documentation chunks (default 3).
        faq_top_k: Number of troubleshooting FAQ pairs (default 2).
        doc_type: Optional filter to one chunk type, e.g. "对比消歧" (code/
            endpoint disambiguation), "响应组件" (reusable schema component
            fields), "请求参数", "端点概览", "概念说明", "操作步骤",
            "错误处理". Leave unset to search all types together.
        endpoint: Optional OpenAPI path filter, e.g. "/search.do".
    """
    conditions = []
    if doc_type:
        conditions.append({"doc_type": doc_type})
    if endpoint:
        conditions.append({"endpoint": endpoint})
    if len(conditions) == 1:
        where = conditions[0]
    elif len(conditions) > 1:
        where = {"$and": conditions}
    else:
        where = None
    return rag_search.search_api_docs_context(
        query, n_results=top_k, faq_n_results=faq_top_k, where=where
    )


@mcp.tool()
def search_product_intro(query: str, top_k: int = 3) -> list[dict]:
    """Search Atlas 产品介绍 (product overview + 10 role-based guide pages:
    what Atlas is, how search/booking/payment/webhook/customer-service
    capabilities fit together). Evergreen positioning/capability content —
    NOT policy rules (use search_help_center_context) and NOT API field
    reference (use search_api_docs_context). Use this for "what is Atlas" /
    "what can Atlas do" / "how do the pieces fit together" questions, e.g.
    "Atlas支持哪些支付方式" at a product level (vs. search_help_center_context
    for the detailed policy) or "MCP辅助开发是什么".

    Args:
        query: Natural-language question, Chinese or English.
        top_k: Number of results to return (default 3).

    Returns:
        List of hits, each with: chunk_id, distance, title, section, text,
        source_path.
    """
    return rag_search.search_product_intro(query, n_results=top_k)


@mcp.tool()
def search_product_news(query: str, top_k: int = 3) -> list[dict]:
    """Search Atlas资讯 — product news and announcements (new airline
    integrations, policy changes, feature launches, service disruptions and
    their resolutions). Use this for "什么时候上线的" / "现在还能订吗" /
    "最近有什么变化" style questions about a specific airline or feature,
    NOT for stable policy rules (use search_help_center_context) or product
    positioning (use search_product_intro).

    Important: some subjects (mainly airlines) get MULTIPLE posts over time
    where a later one supersedes an earlier one's conclusion (e.g. an
    airline stops operating, then later resumes) — this tool already
    collapses same-subject hits down to the most recent post before
    returning, so you do NOT need to cross-check dates yourself or warn the
    user about conflicting older posts. Every result IS the current status.

    Args:
        query: Natural-language question, Chinese or English.
        top_k: Number of results to return (default 3).

    Returns:
        List of hits, each with: chunk_id, distance, title, entity_tags
        (airline/product codes this post is about, if any), recency_rank
        (site listing order, 1=newest — informational only, already applied),
        text, source_path.
    """
    return rag_search.search_product_news(query, n_results=top_k)


@mcp.tool()
def list_lookup_tables() -> list[dict]:
    """List the structured reference tables (error codes, refund/void time
    limits, sandbox test data, locale codes, payment card requirements —
    17 tables total) that are NOT covered by the search_* tools. These are
    exact-lookup data (e.g. "what does error code 308 mean", "what's the
    refund deadline for airline FR"), deliberately kept out of semantic
    search because chunking a lookup table destroys its queryability — use
    query_lookup_table against the table_name this returns instead of
    trying to find this data via search_help_center_context/search_api_docs_context.

    Returns:
        List of tables, each with: table_name, path, row_count, columns
        (the field names present in each row), meta (any wrapper-level
        info the source file carried, e.g. which API endpoint an error
        code table belongs to).
    """
    return lookup_tables.list_tables()


@mcp.tool()
def query_lookup_table(
    table_name: str,
    filters: Optional[dict] = None,
    limit: int = 50,
) -> dict:
    """Query one of the structured reference tables by exact/substring
    field match. Call list_lookup_tables first if you don't already know
    the exact table_name and column names — a wrong table_name returns a
    did_you_mean suggestion, but getting the columns right the first time
    avoids a round trip.

    Args:
        table_name: Exact name from list_lookup_tables (e.g.
            "退票时限结构化表", "错误码速查表", "lookup-table-search-status").
        filters: Optional dict of {column: value} to narrow results, e.g.
            {"carrier_code": "FR"} or {"code": "308"}. String values match
            case-insensitively as substrings; non-string values (numbers)
            match exactly. Omit to get the whole table (capped by limit).
        limit: Max rows to return (default 50). If total_matched exceeds
            this, the response is truncated — narrow with filters instead
            of raising limit for large tables like the 131-row refund
            deadline table.

    Returns:
        {table_name, meta, total_matched, rows, truncated} — or
        {error, did_you_mean} if table_name doesn't match any table.
    """
    return lookup_tables.query_table(table_name, filters=filters, limit=limit)


@mcp.tool()
def get_full_article(source_path: str) -> dict:
    """Fetch the complete source article a search hit came from, when a
    chunk's snippet isn't enough context. Equivalent to the old GitBook
    MCP's getPage(url) tool, but takes the source_path field already
    present on every search_help_center_context/search_api_docs_context hit
    instead of a URL — call a search tool first, then pass its source_path
    here if you need more surrounding context than that one chunk gives you.

    Most questions are answerable from a single chunk (each one is a
    complete rule/concept on its own) — reach for this when a procedure
    spans multiple chunks and you need to see them in original order, or
    when the chunk text references something ("见上文"/"如下表") that got
    cut at the chunk boundary.

    Args:
        source_path: The source_path value from a search_help_center_context
            or search_api_docs_context hit, e.g.
            "04-售后票务/退票/Atlas退票服务说明.md".

    Returns:
        {source_path, title, text} with the article's full cleaned
        markdown (GitBook wrapper tags stripped while hint text is retained), or
        {error} if source_path doesn't resolve to a file in either corpus.
    """
    return rag_search.get_full_article(source_path)


if __name__ == "__main__":
    mcp.run(transport=TRANSPORT)
