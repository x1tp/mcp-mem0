from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
from dotenv import load_dotenv
from mem0 import Memory
import asyncio
import json
import os

from utils import get_mem0_client
import nest_asyncio
nest_asyncio.apply()

load_dotenv()

# Default user ID for memory operations
DEFAULT_USER_ID = "user"

# Initialize the MCP server
server = Server("mcp-mem0")

# Global mem0 client
mem0_client = None

async def initialize_mem0():
    """Initialize the Mem0 client"""
    global mem0_client
    if mem0_client is None:
        mem0_client = get_mem0_client()
    return mem0_client

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="save_memory",
            description="Save information to your long-term memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The content to store in memory, including any relevant details and context"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="get_all_memories",
            description="Get all stored memories for the user",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="search_memories",
            description="Search memories using semantic search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string describing what you're looking for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 3)",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    await initialize_mem0()
    
    if name == "save_memory":
        text = arguments.get("text", "")
        try:
            messages = [{"role": "user", "content": text}]
            mem0_client.add(messages, user_id=DEFAULT_USER_ID)
            result = f"Successfully saved memory: {text[:100]}..." if len(text) > 100 else f"Successfully saved memory: {text}"
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error saving memory: {str(e)}")]
    
    elif name == "get_all_memories":
        try:
            memories = mem0_client.get_all(user_id=DEFAULT_USER_ID)
            if isinstance(memories, dict) and "results" in memories:
                flattened_memories = [memory["memory"] for memory in memories["results"]]
            else:
                flattened_memories = memories
            result = json.dumps(flattened_memories, indent=2)
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error retrieving memories: {str(e)}")]
    
    elif name == "search_memories":
        query = arguments.get("query", "")
        limit = arguments.get("limit", 3)
        try:
            memories = mem0_client.search(query, user_id=DEFAULT_USER_ID, limit=limit)
            if isinstance(memories, dict) and "results" in memories:
                flattened_memories = [memory["memory"] for memory in memories["results"]]
            else:
                flattened_memories = memories
            result = json.dumps(flattened_memories, indent=2)
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching memories: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
