#!/usr/bin/env python3
"""
Local MCP Server with ping tool
"""

import asyncio
import logging
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the server instance
server = Server("local-mcp-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="ping",
            description="A simple ping tool that responds with 'pong' and optional message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Optional message to include in the response",
                        "default": ""
                    }
                },
                "additionalProperties": False
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> Sequence[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if name == "ping":
        message = arguments.get("message", "") if arguments else ""
        response = "pong"
        if message:
            response += f": {message}"
        
        logger.info(f"Ping tool called with message: '{message}', responding: '{response}'")
        
        return [
            types.TextContent(
                type="text",
                text=response
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    try:
        logger.info("Starting local MCP server...")
        
        # Run the server using stdio transport
        async with stdio_server() as streams:
            await server.run(
                streams[0], streams[1],
                server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())