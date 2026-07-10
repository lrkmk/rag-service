"""
Test the deployed MCP service over streamable-http transport (as opposed to
test_mcp_server.py, which spawns a local stdio subprocess). Calls each of
the 4 tools once against a running remote/containerized instance.

Usage:
    python test_mcp_remote.py <base_url>
    python test_mcp_remote.py https://ai-test.atlastravel.tech/mcp
"""
import asyncio
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main(url: str):
    async with streamablehttp_client(url) as (read, write, _get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print(f"=== {len(tools.tools)} tools registered ===")
            for t in tools.tools:
                print(f"- {t.name}")

            print("\n=== call: search_help_center('退票超过多久不再处理') ===")
            r = await session.call_tool("search_help_center", {"query": "退票超过多久不再处理", "top_k": 1})
            print(r.content[0].text[:300])

            print("\n=== call: search_api_docs('429和110的区别', doc_type='对比消歧') ===")
            r = await session.call_tool("search_api_docs", {"query": "429和110的区别", "top_k": 1, "doc_type": "对比消歧"})
            print(r.content[0].text[:300])

            print("\n=== call: search_help_center_faq('出票要多长时间') ===")
            r = await session.call_tool("search_help_center_faq", {"query": "出票要多长时间", "top_k": 1})
            print(r.content[0].text[:300])

            print("\n=== call: search_api_docs_faq('如何开始使用API') ===")
            r = await session.call_tool("search_api_docs_faq", {"query": "如何开始使用API", "top_k": 1})
            print(r.content[0].text[:300])


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000/mcp"
    asyncio.run(main(url))
