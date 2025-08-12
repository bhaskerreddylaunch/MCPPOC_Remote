# MCPPOC_Remote

MCP (Model Context Protocol) Proof of Concept with local server implementation.

## Description
This repository contains a local MCP server implementation with a "ping" tool for testing connectivity.

## Features
- Local MCP server with JSON-RPC over stdio transport
- Ping tool for connectivity verification
- Automated test suite

## Getting Started

### Prerequisites
- Python 3.7 or higher

### Installation
1. Clone the repository
2. Install dependencies (optional):
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server
Start the MCP server:
```bash
./start_server.sh
# or directly:
python3 local_mcp_server.py
```

### Testing the Ping Tool
Run the automated test suite:
```bash
python3 test_ping.py
```

### Manual Testing
You can manually test the server by sending JSON-RPC requests via stdin:

1. List available tools:
   ```json
   {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
   ```

2. Call the ping tool:
   ```json
   {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "ping", "arguments": {}}}
   ```

3. Call ping with custom message:
   ```json
   {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "ping", "arguments": {"message": "hello"}}}
   ```

## API Documentation

### Available Tools

#### ping
Tests connectivity to the MCP server.

**Parameters:**
- `message` (optional, string): Custom message to include in response (default: "ping")

**Response:**
Returns a pong response with timestamp and the provided message.

## License
MIT License
