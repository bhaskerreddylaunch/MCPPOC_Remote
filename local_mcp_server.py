#!/usr/bin/env python3
"""
Local MCP Server with ping tool for connectivity testing.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime

class MCPServer:
    """A minimal MCP server implementation with ping tool."""
    
    def __init__(self):
        self.tools = {
            "ping": {
                "name": "ping",
                "description": "Test connectivity to the MCP server",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Optional message to include in ping response",
                            "default": "ping"
                        }
                    }
                }
            }
        }
    
    async def handle_ping(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ping tool requests."""
        message = params.get("message", "ping")
        timestamp = datetime.now().isoformat()
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"pong: {message} (server time: {timestamp})"
                }
            ]
        }
    
    async def handle_list_tools(self) -> Dict[str, Any]:
        """Return list of available tools."""
        return {
            "tools": list(self.tools.values())
        }
    
    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool calls."""
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})
        
        if tool_name == "ping":
            return await self.handle_ping(tool_params)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                result = await self.handle_list_tools()
            elif method == "tools/call":
                result = await self.handle_call_tool(params)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
    
    async def run_stdio(self):
        """Run server using stdio transport."""
        print("MCP Server starting with ping tool...", file=sys.stderr)
        
        while True:
            try:
                line = input()
                if not line:
                    break
                
                request = json.loads(line)
                response = await self.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
                
            except EOFError:
                break
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32000,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

async def main():
    """Main entry point."""
    server = MCPServer()
    await server.run_stdio()

if __name__ == "__main__":
    asyncio.run(main())