# MCP Meta-Agent Enhancement Guide

## Overview

The meta-agent has been enhanced with comprehensive Model Context Protocol (MCP) knowledge, enabling it to build MCP servers and agents for connecting AI to external systems.

## What's New

The meta-agent can now:
- ✅ Build MCP servers in Python (and guide for other languages)
- ✅ Generate complete MCP server code with tools, resources, and prompts
- ✅ Create Claude Desktop configuration files
- ✅ Provide implementation guidance based on official docs + video tutorials
- ✅ Apply MCP best practices automatically
- ✅ Generate security-conscious code with proper error handling

## MCP Knowledge Included

### Core Concepts
- **Architecture**: JSON-RPC 2.0 client-server protocol
- **Capability Types**: Tools (functions), Resources (data), Prompts (templates)
- **Transport Types**: STDIO (local) vs HTTP (remote)
- **Supported Languages**: Python 3.10+, Node.js, Java 17+, Kotlin, C#, Go, Swift, Ruby, Rust, PHP

### Best Practices
- Never use stdout for STDIO server logging (use stderr or files)
- Always use absolute paths in configuration
- Implement JSON Schema validation for all inputs
- Use async/await patterns
- Keep dependencies minimal
- Implement robust error handling

### Real-World Patterns
Based on official documentation and video tutorials:
- File system access servers
- Database integration servers
- API wrapper servers
- Documentation lookup (Context7 pattern)
- System command servers (with security controls)
- Docker-based isolation for dangerous operations

## How to Use

### Basic MCP Server Creation

**User prompt:**
```
Create an MCP server that provides weather information
```

**Meta-agent will:**
1. Ask clarifying questions (if needed):
   - What data/tools to expose?
   - Local or remote server?
   - Language preference?
2. Generate complete Python server code
3. Create Claude Desktop configuration
4. Provide installation and testing instructions

### Example Request Flow

**User:** "Build an MCP server to search my project files"

**Meta-agent delivers:**

1. **Server Code** (`mcp-file-search/server.py`):
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import os
import glob

server = Server("file-search")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_files",
            description="Search for files matching a pattern",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern to search for"},
                    "directory": {"type": "string", "description": "Directory to search in"}
                },
                "required": ["pattern", "directory"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_files":
        pattern = arguments["pattern"]
        directory = arguments["directory"]

        # Security: Validate directory path
        if not os.path.exists(directory):
            return [TextContent(type="text", text=f"Directory not found: {directory}")]

        # Search for files
        search_path = os.path.join(directory, pattern)
        results = glob.glob(search_path, recursive=True)

        return [TextContent(
            type="text",
            text=f"Found {len(results)} files:\\n" + "\\n".join(results)
        )]

async def main():
    from mcp.server.stdio import stdio_server
    import asyncio

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

2. **Configuration** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "file-search": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-file-search/server.py"]
    }
  }
}
```

3. **Documentation**:
   - Installation steps
   - How to configure in Claude Desktop
   - Example prompts to test
   - Troubleshooting tips

## Advanced Use Cases

### Multi-Tool Server

**User:** "Create an MCP server for GitHub operations - list repos, create issues, search code"

**Meta-agent will:**
- Create server with multiple tools
- Implement proper GitHub API authentication
- Add input validation for all tools
- Generate comprehensive error handling
- Provide environment variable configuration

### Resource-Based Server

**User:** "Build an MCP server that exposes my project documentation as resources"

**Meta-agent will:**
- Use Resource primitive instead of Tools
- Implement direct resources (fixed URIs)
- Set up resource templates (dynamic URIs)
- Configure MIME types and descriptions

### Prompt Template Server

**User:** "Create MCP server with code review and bug report templates"

**Meta-agent will:**
- Use Prompts primitive
- Create reusable template structures
- Support parameter completion
- Implement user-controlled invocation

## Security Features

The enhanced meta-agent includes security awareness:

**Automatically implements:**
- Input sanitization
- Path traversal protection
- Command injection prevention
- Environment variable handling for secrets
- User approval requirements for dangerous operations

**Warns about:**
- Unrestricted system command access
- Hardcoded credentials
- Missing input validation
- Overly permissive file access

## Configuration Patterns

### Local STDIO Server (Default)
```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

### Remote HTTP Server
```json
{
  "mcpServers": {
    "remote-server": {
      "url": "https://api.example.com/mcp",
      "apiKey": "authentication-token"
    }
  }
}
```

### With Environment Variables
```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}",
        "API_TOKEN": "${API_TOKEN}"
      }
    }
  }
}
```

## Testing and Debugging

Meta-agent provides guidance on:

**Testing Tools:**
- MCP Inspector for protocol validation
- Manual testing with curl (for HTTP servers)
- Unit tests for tool handlers

**Common Issues:**
- Server not appearing: Check config syntax, paths, restart Claude
- Tool not executing: Verify schema, check logs
- Authentication failures: Validate credentials, environment vars

**Logging Best Practices:**
```python
import sys
import logging

# For STDIO servers - NEVER use stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Critical: stderr not stdout
)

# Or use file logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO
)
```

## Project Structure Generated

```
mcp-[project-name]/
├── server.py                 # Main implementation
├── requirements.txt          # Python dependencies
│   └── mcp>=1.0.0
├── README.md                 # Setup and usage guide
├── config.example.json       # Claude Desktop config template
├── .env.example             # Environment variables template
└── tests/                    # Optional test suite
    └── test_server.py
```

## Language Support

While Python is the default (workspace standard), meta-agent can provide guidance for:

- **Node.js/TypeScript**: npm package, async/await patterns
- **Java**: Maven/Gradle setup, Spring Boot integration
- **Go**: Module setup, goroutines
- **C#**: .NET project structure, async tasks

## Real-World Examples from Knowledge Base

### 1. Context7 Pattern (Documentation Server)
**Use Case**: Access 20,000+ library docs
**Type**: Remote HTTP server
**Key Feature**: Free tier, shared resources

### 2. File System Server
**Use Case**: Give AI access to local files
**Type**: STDIO server
**Key Feature**: Directory boundaries with Roots

### 3. Kali Linux Server (Advanced)
**Use Case**: Ethical hacking tools access
**Type**: Docker-isolated STDIO server
**Key Feature**: Security through containerization

### 4. Obsidian Vault Server
**Use Case**: Personal knowledge management
**Type**: STDIO server with file resources
**Key Feature**: Bi-directional sync

## Quick Start Examples

### Minimal Weather Tool
```
User: "Create a simple MCP weather tool"
Meta-agent: Generates basic STDIO server with one tool
```

### Database Query Server
```
User: "Build MCP server to query my PostgreSQL database"
Meta-agent: Creates server with connection pooling, query validation, resource exposure
```

### API Wrapper
```
User: "Make an MCP server for the GitHub API"
Meta-agent: Implements OAuth, rate limiting, multiple tools (repos, issues, PRs)
```

## Comparison: MCP Server vs Claude Code Agent

**When to use MCP Server:**
- Connecting to external systems (databases, APIs, file systems)
- Want tool reusability across multiple AI apps (Claude Desktop, Cursor, etc.)
- Need standardized protocol for ecosystem/sharing
- Building production-ready integrations

**When to use Claude Code Agent:**
- Workflow orchestration within Claude Code only
- Task coordination and delegation
- No external system integration needed
- Temporary/project-specific automation

**Can combine both:**
- Claude Code agent uses MCP servers as tools
- Layered architecture: Agents orchestrate, MCP servers provide capabilities

## Troubleshooting Guide

Meta-agent includes knowledge of common issues:

| Issue | Solution |
|-------|----------|
| Server not showing in Claude | Verify JSON syntax, use absolute paths, restart Claude Desktop |
| STDIO communication broken | Check for stdout usage (use stderr instead) |
| Tool not executing | Validate input schema matches call signature |
| Import errors | Check requirements.txt installed, Python version 3.10+ |
| Path not found | Use absolute paths, verify __file__ usage correct |

## Resources Referenced

The enhanced meta-agent draws knowledge from:
- ✅ Official MCP documentation (modelcontextprotocol.io)
- ✅ 3 comprehensive video tutorials
- ✅ Real-world implementation examples
- ✅ Community best practices

## Next Steps

After meta-agent creates your MCP server:

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Test independently**: Use MCP Inspector or manual testing
3. **Configure Claude Desktop**: Add to config file
4. **Restart Claude**: Required for new servers
5. **Test integration**: Try example prompts
6. **Iterate**: Refine based on usage

## Example Meta-Agent Prompts

Try these to see the MCP knowledge in action:

```
"Create an MCP server to manage my task list"
"Build an MCP server that searches my codebase"
"Make an MCP server for Slack notifications"
"Create an MCP server to access my database"
"Build a Docker-isolated MCP server for running shell commands"
```

---

**The meta-agent is now MCP-ready!** It can build production-quality MCP servers following official specifications and community best practices.
