"""
Standalone test: launches mcp_server.py as a subprocess over stdio and calls
each of its 4 tools once, to verify the MCP protocol wiring actually works
end-to-end (not just that rag_search.py works when imported directly).
"""
import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable
SERVER = os.path.join(HERE, "mcp_server.py")


async def main():
    params = StdioServerParameters(command=PYTHON, args=[SERVER], cwd=HERE)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print(f"=== {len(tools.tools)} tools registered ===")
            for t in tools.tools:
                print(f"- {t.name}: {t.description.splitlines()[0]}")

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
    asyncio.run(main())
