#!/usr/bin/env python3
"""
Simple MCP client to test the mcp-mem0 server
"""
import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test the MCP server functionality"""
      # Server parameters - this should point to your MCP server
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "src/main.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                print("🔧 Listing available tools...")
                tools = await session.list_tools()
                print(f"Available tools: {[tool.name for tool in tools.tools]}")
                
                # Test save_memory
                print("\n💾 Testing save_memory...")
                result = await session.call_tool(
                    "save_memory",
                    arguments={"text": "Test memory from MCP client - server restart strategy works"}
                )
                print(f"Save result: {result.content}")
                
                # Test search_memories
                print("\n🔍 Testing search_memories...")
                search_result = await session.call_tool(
                    "search_memories",
                    arguments={"query": "server restart", "limit": 5}
                )
                print(f"Search result: {search_result.content}")
                
                # Test get_all_memories
                print("\n📋 Testing get_all_memories...")
                all_memories = await session.call_tool(
                    "get_all_memories",
                    arguments={}
                )
                print(f"All memories: {all_memories.content}")
                
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
