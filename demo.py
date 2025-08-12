#!/usr/bin/env python3
"""
Demo script showing the MCP ping tool in action
"""

import asyncio
import json
import sys
import logging

# Add the current directory to the path
sys.path.insert(0, '.')

from mcp_server import handle_list_tools, handle_call_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_ping_tool():
    """Demonstrate the ping tool functionality."""
    print("🏓 MCP Ping Tool Demo")
    print("=" * 40)
    
    # Show available tools
    print("\n📋 Available Tools:")
    tools = await handle_list_tools()
    for tool in tools:
        print(f"  • {tool.name}: {tool.description}")
    
    print("\n🚀 Testing Ping Tool:")
    
    # Demo 1: Simple ping
    print("\n1. Simple ping (no message):")
    result1 = await handle_call_tool("ping", {})
    print(f"   → {result1[0].text}")
    
    # Demo 2: Ping with message
    print("\n2. Ping with custom message:")
    result2 = await handle_call_tool("ping", {"message": "Hello, MCP World!"})
    print(f"   → {result2[0].text}")
    
    # Demo 3: Ping with another message
    print("\n3. Ping with different message:")
    result3 = await handle_call_tool("ping", {"message": "Testing successful!"})
    print(f"   → {result3[0].text}")
    
    print("\n✅ Demo completed successfully!")
    print("\nThe local MCP server's ping tool is working correctly.")
    print("You can use this as a foundation for building more complex MCP tools.")


if __name__ == "__main__":
    asyncio.run(demo_ping_tool())