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


if __name__ == "__main__":
    mcp.run(transport=TRANSPORT)
