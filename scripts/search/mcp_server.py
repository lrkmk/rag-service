"""
MCP server exposing the Atlas documentation RAG store as tools an agent can
call directly, instead of shelling out to ask.py.

Wraps rag_search.py's four search functions (帮助中心 rules/FAQ, API文档
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
def search_help_center(
    query: str,
    top_k: int = 3,
    carrier: Optional[str] = None,
) -> list[dict]:
    """Search Atlas's Chinese Help Center (帮助中心) — customer-service /
    operations policy content: refund and void rules, flight-change policy,
    payment methods, billing, notifications, security & compliance, SLAs.

    Use this for questions about WHAT the policy/rule is and WHEN it applies
    (e.g. "退票超过多久不再处理", "航班提前多久可以非自愿退票"). Do NOT use
    this for API integration questions (endpoint parameters, error codes,
    request/response fields) — use search_api_docs for those instead.

    Args:
        query: Natural-language question, Chinese or English.
        top_k: Number of results to return (default 3).
        carrier: Optional airline IATA code (e.g. "FR", "IJ", "W6") to
            restrict results to that airline's specific rules instead of
            generic ones. Only set this if the question names a specific
            airline — otherwise leave it unset to search generic + all
            airline-specific content together.

    Returns:
        List of hits, each with: chunk_id, distance (lower = more relevant),
        level1_category, level2_category, section, text (the actual rule),
        applicable_carrier, parent_title, parent_summary, source_path.
    """
    where = {"applicable_carrier": carrier} if carrier else None
    return rag_search.search_rules(query, n_results=top_k, where=where)


@mcp.tool()
def search_help_center_faq(query: str, top_k: int = 3) -> list[dict]:
    """Search the Help Center's FAQ section (customer service / API
    integration / payment / feature questions phrased as short Q&A pairs,
    e.g. "出票需要多长时间？"). Try this alongside search_help_center when a
    question sounds like a quick factual lookup rather than a policy rule
    with conditions.

    Args:
        query: Natural-language question, Chinese or English.
        top_k: Number of results to return (default 3).

    Returns:
        List of hits, each with: chunk_id, distance, topic, question, answer.
    """
    return rag_search.search_faq(query, n_results=top_k)


@mcp.tool()
def search_api_docs(
    query: str,
    top_k: int = 3,
    doc_type: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> list[dict]:
    """Search Atlas's developer/API documentation (API文档) — integration
    guides, booking-flow product guides, OpenAPI endpoint reference (request/
    response fields, components), error-code disambiguation guides, sandbox
    setup, rate limits.

    Use this for HOW-TO-INTEGRATE questions: endpoint parameters, field
    types, what an error code means, which endpoint to call next, how two
    similar endpoints/codes differ (e.g. "429和110的区别", "search.do和
    getOffers.do怎么选", "创建订单的请求体有哪些字段"). Do NOT use this for
    customer-service policy questions (refund windows, billing) — use
    search_help_center for those instead.

    Note: large lookup tables (the 43-code master error reference, sandbox
    test card/route lists, locale reference data) are NOT in this search
    index by design — they're exact-lookup data, not semantic search
    content. If a query is clearly "look up code/value X", prefer reading
    the structured JSON files directly (see RAG-切片设计总览.md for paths)
    rather than relying on this search.

    Args:
        query: Natural-language question, Chinese or English.
        top_k: Number of results to return (default 3).
        doc_type: Optional filter to one chunk type, e.g. "对比消歧" (code/
            endpoint disambiguation), "响应组件" (reusable schema component
            fields), "请求参数", "端点概览", "概念说明", "操作步骤",
            "错误处理". Leave unset to search all types together.
        endpoint: Optional filter to a specific OpenAPI path, e.g.
            "/search.do". Only set this if the question clearly names one
            endpoint and you want to restrict results to just it.

    Returns:
        List of hits, each with: chunk_id, distance, doc_type,
        level1_category, level2_category, section, text, applicable_carrier,
        compares (present on 对比消歧 chunks — the codes/endpoints being
        contrasted), endpoint (present on API-reference chunks),
        source_path.
    """
    where = None
    conditions = []
    if doc_type:
        conditions.append({"doc_type": doc_type})
    if endpoint:
        conditions.append({"endpoint": endpoint})
    if len(conditions) == 1:
        where = conditions[0]
    elif len(conditions) > 1:
        where = {"$and": conditions}
    return rag_search.search_api_docs(query, n_results=top_k, where=where)


@mcp.tool()
def search_api_docs_faq(query: str, top_k: int = 3) -> list[dict]:
    """Search the API文档's troubleshooting FAQ section (integration
    onboarding, payment methods, order/ticketing, finance, kickoff
    checklist — phrased as short Q&A pairs).

    Args:
        query: Natural-language question, Chinese or English.
        top_k: Number of results to return (default 3).

    Returns:
        List of hits, each with: chunk_id, distance, topic, question, answer.
    """
    return rag_search.search_api_faq(query, n_results=top_k)


@mcp.tool()
def search_product_intro(query: str, top_k: int = 3) -> list[dict]:
    """Search Atlas 产品介绍 (product overview + 10 role-based guide pages:
    what Atlas is, how search/booking/payment/webhook/customer-service
    capabilities fit together). Evergreen positioning/capability content —
    NOT policy rules (use search_help_center) and NOT API field reference
    (use search_api_docs). Use this for "what is Atlas" / "what can Atlas
    do" / "how do the pieces fit together" questions, e.g. "Atlas支持哪些
    支付方式" at a product level (vs. search_help_center for the detailed
    policy) or "MCP辅助开发是什么".

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
    NOT for stable policy rules (use search_help_center) or product
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
    trying to find this data via search_help_center/search_api_docs.

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
    present on every search_help_center/search_api_docs hit instead of a
    URL — call a search tool first, then pass its source_path here if you
    need more surrounding context than that one chunk gives you.

    Most questions are answerable from a single chunk (each one is a
    complete rule/concept on its own) — reach for this when a procedure
    spans multiple chunks and you need to see them in original order, or
    when the chunk text references something ("见上文"/"如下表") that got
    cut at the chunk boundary.

    Args:
        source_path: The source_path value from a search_help_center or
            search_api_docs hit, e.g. "04-售后票务/退票/Atlas退票服务说明.md".

    Returns:
        {source_path, title, text} with the article's full cleaned
        markdown (GitBook-specific {% hint %} boilerplate stripped), or
        {error} if source_path doesn't resolve to a file in either corpus.
    """
    return rag_search.get_full_article(source_path)


if __name__ == "__main__":
    mcp.run(transport=TRANSPORT)
