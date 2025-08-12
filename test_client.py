#!/usr/bin/env python3
"""
Test script for the local MCP server ping tool
"""

import asyncio
import logging
import sys
import os
import json
import tempfile
import subprocess
from typing import Dict, Any

# Add the current directory to the path so we can import our server
sys.path.insert(0, os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_ping_tool_directly():
    """Test the ping tool functionality directly without full JSON-RPC protocol."""
    try:
        # Import and test the server handlers directly
        from mcp_server import handle_list_tools, handle_call_tool
        
        logger.info("Testing ping tool directly...")
        
        # Test list_tools
        tools = await handle_list_tools()
        logger.info(f"Available tools: {[tool.name for tool in tools]}")
        
        assert len(tools) == 1
        assert tools[0].name == "ping"
        assert "ping tool" in tools[0].description.lower()
        
        # Test ping without message
        result1 = await handle_call_tool("ping", {})
        logger.info(f"Ping without message result: {result1[0].text}")
        assert result1[0].text == "pong"
        
        # Test ping with message
        result2 = await handle_call_tool("ping", {"message": "Hello World!"})
        logger.info(f"Ping with message result: {result2[0].text}")
        assert result2[0].text == "pong: Hello World!"
        
        # Test unknown tool (should raise ValueError)
        try:
            await handle_call_tool("unknown", {})
            assert False, "Should have raised ValueError for unknown tool"
        except ValueError as e:
            logger.info(f"Correctly caught error for unknown tool: {e}")
        
        logger.info("✅ All direct tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Direct test failed: {e}")
        return False


async def test_server_startup():
    """Test that the server can start up without errors."""
    try:
        logger.info("Testing server startup...")
        
        # Start the server process
        process = await asyncio.create_subprocess_exec(
            sys.executable, "mcp_server.py",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Give it a moment to start
        await asyncio.sleep(1)
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        request_json = json.dumps(init_request) + "\n"
        process.stdin.write(request_json.encode())
        await process.stdin.drain()
        
        # Try to read response with timeout
        try:
            response_line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=5.0
            )
            if response_line:
                response = json.loads(response_line.decode())
                logger.info(f"Initialize response: {response}")
                logger.info("✅ Server startup test passed!")
                result = True
            else:
                logger.warning("No response received from server")
                result = False
        except asyncio.TimeoutError:
            logger.warning("Server startup test timed out")
            result = False
        
        # Clean up
        process.terminate()
        await process.wait()
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Server startup test failed: {e}")
        return False


async def main():
    """Run all tests."""
    logger.info("🚀 Starting MCP ping tool tests...")
    
    success = True
    
    # Test direct functionality
    if not await test_ping_tool_directly():
        success = False
    
    # Test server startup
    if not await test_server_startup():
        success = False
    
    if success:
        logger.info("🎉 All tests passed! The ping tool is working correctly.")
        print("\n" + "="*50)
        print("SUCCESS: MCP ping tool implementation is working!")
        print("="*50)
        return 0
    else:
        logger.error("💥 Some tests failed!")
        print("\n" + "="*50)
        print("FAILURE: Some tests failed. Check logs above.")
        print("="*50)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())