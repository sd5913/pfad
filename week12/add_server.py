# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["mcp==1.15.0", "pydantic==2.11.9"]
# ///
"""One-tool, local stdio MCP server. Run via check_mcp.py for a bounded demo."""

from mcp.server.fastmcp import FastMCP

from trace import add

server = FastMCP("Week 12 addition")
server.tool()(add)

if __name__ == "__main__":
    # stdio belongs to MCP messages; do not print teaching text from this process.
    server.run(transport="stdio")
