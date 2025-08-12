# MCP Ping Tool Usage Guide

This guide demonstrates how to use the local MCP server's ping tool.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
python3 demo.py
```

### 3. Run Tests
```bash
python3 test_client.py
```

### 4. Start the MCP Server
```bash
python3 mcp_server.py
```

## Using the Ping Tool

The ping tool accepts an optional `message` parameter and responds with "pong" optionally followed by the message.

### Examples

**Simple ping (no message):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "ping",
    "arguments": {}
  }
}
```
Response: `"pong"`

**Ping with message:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "ping",
    "arguments": {
      "message": "Hello World!"
    }
  }
}
```
Response: `"pong: Hello World!"`

## Tool Schema

```json
{
  "name": "ping",
  "description": "A simple ping tool that responds with 'pong' and optional message",
  "inputSchema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "Optional message to include in the response",
        "default": ""
      }
    },
    "additionalProperties": false
  }
}
```

## Integration with MCP Clients

This server can be integrated with any MCP-compatible client by:

1. Starting the server: `python3 mcp_server.py`
2. Connecting via stdio transport
3. Sending standard MCP protocol messages

The server supports the full MCP protocol including:
- `initialize` - Initialize the session
- `tools/list` - List available tools
- `tools/call` - Call the ping tool

## Development

To extend this server with additional tools:

1. Add new tool definitions in the `handle_list_tools()` function
2. Add corresponding handlers in the `handle_call_tool()` function
3. Update tests to cover the new functionality

## Troubleshooting

- Ensure Python 3.8+ is installed
- Verify all dependencies are installed with `pip install -r requirements.txt`
- Check logs for any error messages
- Run `python3 test_client.py` to validate the setup