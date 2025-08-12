# MCPPOC_Remote

This repository contains a local MCP (Model Context Protocol) server implementation with a ping tool for POC testing.

## Description
This repository implements a local MCP server that provides a "ping" tool for testing MCP functionality. The server follows the MCP protocol specification and can be used as a starting point for developing more complex MCP tools.

## Features
- **Local MCP Server**: A Python-based MCP server implementation
- **Ping Tool**: A simple tool that responds to ping requests with "pong" and optional messages
- **Test Client**: A test client to validate the ping tool functionality

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MCPPOC_Remote
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Running the MCP Server
```bash
python3 mcp_server.py
```

#### Testing the Ping Tool
```bash
python3 test_client.py
```

#### Manual Testing
You can also test the ping tool manually by sending JSON-RPC requests to the server:

1. Start the server
2. Send initialization request
3. Call the ping tool with or without a message

### API Reference

#### Ping Tool
- **Name**: `ping`
- **Description**: A simple ping tool that responds with 'pong' and optional message
- **Parameters**:
  - `message` (optional): String message to include in the response

#### Example Usage
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "ping",
    "arguments": {
      "message": "Hello from client!"
    }
  }
}
```

#### Response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "pong: Hello from client!"
      }
    ]
  }
}
```

## Files Structure
- `mcp_server.py`: Main MCP server implementation
- `test_client.py`: Test client for validating functionality
- `requirements.txt`: Python dependencies
- `package.json`: Project metadata and scripts

## License
MIT License
