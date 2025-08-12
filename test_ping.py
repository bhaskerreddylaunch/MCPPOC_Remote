#!/usr/bin/env python3
"""
Test script for the local MCP server ping tool.
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

class MCPClient:
    """Simple MCP client for testing."""
    
    def __init__(self, server_command: list):
        self.server_command = server_command
        self.process = None
    
    async def start_server(self):
        """Start the MCP server process."""
        self.process = await asyncio.create_subprocess_exec(
            *self.server_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    
    async def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to the server and get response."""
        if not self.process:
            raise RuntimeError("Server not started")
        
        request_line = json.dumps(request) + "\n"
        self.process.stdin.write(request_line.encode())
        await self.process.stdin.drain()
        
        response_line = await self.process.stdout.readline()
        return json.loads(response_line.decode().strip())
    
    async def stop_server(self):
        """Stop the MCP server process."""
        if self.process:
            self.process.stdin.close()
            await self.process.wait()

async def test_ping_tool():
    """Test the ping tool functionality."""
    print("Starting MCP server test...")
    
    # Start the MCP server
    client = MCPClient([sys.executable, "local_mcp_server.py"])
    await client.start_server()
    
    try:
        # Test 1: List available tools
        print("\n1. Testing tools/list...")
        list_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
        
        response = await client.send_request(list_request)
        print(f"Response: {json.dumps(response, indent=2)}")
        
        # Verify ping tool is listed
        tools = response.get("result", {}).get("tools", [])
        ping_tool = next((tool for tool in tools if tool["name"] == "ping"), None)
        
        if ping_tool:
            print("✓ Ping tool found in tools list")
        else:
            print("✗ Ping tool not found in tools list")
            return False
        
        # Test 2: Call ping tool without message
        print("\n2. Testing ping tool (default message)...")
        ping_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "ping",
                "arguments": {}
            }
        }
        
        response = await client.send_request(ping_request)
        print(f"Response: {json.dumps(response, indent=2)}")
        
        # Verify response
        if "result" in response and "content" in response["result"]:
            content = response["result"]["content"][0]["text"]
            if "pong: ping" in content:
                print("✓ Ping tool responded correctly")
            else:
                print("✗ Ping tool response unexpected")
                return False
        else:
            print("✗ Ping tool response malformed")
            return False
        
        # Test 3: Call ping tool with custom message
        print("\n3. Testing ping tool (custom message)...")
        ping_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "ping",
                "arguments": {
                    "message": "hello from test"
                }
            }
        }
        
        response = await client.send_request(ping_request)
        print(f"Response: {json.dumps(response, indent=2)}")
        
        # Verify response
        if "result" in response and "content" in response["result"]:
            content = response["result"]["content"][0]["text"]
            if "pong: hello from test" in content:
                print("✓ Ping tool with custom message responded correctly")
            else:
                print("✗ Ping tool with custom message response unexpected")
                return False
        else:
            print("✗ Ping tool with custom message response malformed")
            return False
        
        print("\n🎉 All tests passed! MCP server ping tool is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    
    finally:
        await client.stop_server()

async def main():
    """Main test function."""
    success = await test_ping_tool()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())