# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["mcp==1.15.0", "pydantic==2.11.9"]
# ///
"""Smoke-test one real local MCP stdio call, mediated by a host allowlist."""

import asyncio
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from trace import check_call


async def main() -> None:
    server_file = Path(__file__).with_name("add_server.py")
    params = StdioServerParameters(command=sys.executable, args=["-u", str(server_file)])
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as client:
            await client.initialize()
            listed = await client.list_tools()
            assert [tool.name for tool in listed.tools] == ["add"]
            schema = listed.tools[0].inputSchema
            assert set(schema["required"]) == {"a", "b"}, schema
            assert all(schema["properties"][key]["type"] == "integer"
                       for key in ("a", "b")), schema
            print("REAL local MCP stdio: discovered only add(a: integer, b: integer)")

            for name, args in (
                ("add", {"a": 3, "b": 4}),
                ("overwrite", {"path": "work.txt"}),
                ("add", {"a": 3}),
                ("add", {"a": "3", "b": 4}),
            ):
                refusal = check_call(name, args)
                if refusal:
                    print(f"proposed {name}({args}) -> {refusal}")
                    continue
                result = await client.call_tool(name, args)
                assert not result.isError, result
                assert len(result.content) == 1 and result.content[0].type == "text"
                assert result.content[0].text == "7", result
                print(f"proposed {name}({args}) -> MCP tool result: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
