#!/usr/bin/env python3
"""
MCP Server for zk-smart-search.
Exposes Zettelkasten search functionality to AI assistants.
"""
import asyncio
import sys
import os
from unittest.mock import MagicMock, patch
from typing import Any, List, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zkss import ZKSearcher
from indexer import IndexManager
from zkss_markdown import convert_rich_to_markdown

# Initialize Server
server = Server("zk-smart-search")

class CapturingConsole:
    """Mock console to capture output from ZKSearcher."""
    def __init__(self):
        self.output = []

    def print(self, msg, *args, **kwargs):
        # Strip rich formatting tags if possible, or just keep them
        # For simplicity, we just store the message
        self.output.append(str(msg))
    
    def pager(self, styles=True):
        # Return a context manager that does nothing
        return MagicMock()

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_notes",
            description="Search for notes in the Zettelkasten. Supports both exact keyword matching (default) and semantic/meaning-based search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (keywords or concept)"
                    },
                    "semantic": {
                        "type": "boolean",
                        "description": "If true, uses semantic search (embedding-based). If false/omitted, uses keyword search.",
                        "default": False
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of results to return (default: 15)",
                        "default": 15
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="read_note",
            description="Read the full content of a note.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The exact filename of the note to read"
                    }
                },
                "required": ["filename"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "search_notes":
        query = arguments.get("query")
        semantic = arguments.get("semantic", False)
        limit = arguments.get("limit", 15)
        
        if semantic:
            return await perform_semantic_search(query, limit)
        else:
            return await perform_keyword_search(query)
            
    elif name == "read_note":
        filename = arguments.get("filename")
        return await read_note_content(filename)
    
    raise ValueError(f"Unknown tool: {name}")

async def perform_semantic_search(query: str, limit: int) -> list[TextContent]:
    try:
        # We need to suppress console output from IndexManager too
        indexer = IndexManager()
        indexer.console = MagicMock() 
        
        # Ensure index is up to date (this might take a moment if many changes)
        # For an interactive tool, maybe we skip update or do it?
        # Let's do a lightweight update check
        indexer.update_index()
        
        results = indexer.search(query, n_results=limit)
        
        formatted_results = []
        searcher = ZKSearcher() # Helper for strip_ending
        
        for fname in results:
            clean_name = searcher.strip_ending(fname)
            formatted_results.append(f"- **{clean_name}** ({fname})")
            
        return [TextContent(
            type="text",
            text=f"Found {len(results)} relevant notes (Semantic):\n" + "\n".join(formatted_results)
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"Error performing semantic search: {str(e)}")]

async def perform_keyword_search(query: str) -> list[TextContent]:
    try:
        # Initialize Searcher
        searcher = ZKSearcher()
        
        # Inject capturing console
        capture = CapturingConsole()
        searcher.console = capture
        
        # Mock sys.argv to pass the query
        # ZKSearcher uses argparse on sys.argv
        with patch.object(sys, 'argv', ['zkss.py', *query.split()]):
            try:
                searcher.run()
            except SystemExit:
                # argparse or sys.exit() might trigger this
                pass
        
        # Process output
        # The output contains Rich markup like [yellow]...[/yellow]
        # Convert it to Markdown for better AI assistant readability
        formatted_lines = [convert_rich_to_markdown(line) for line in capture.output]
        output_text = "\n".join(formatted_lines)
        
        return [TextContent(
            type="text",
            text=f"Search Results for '{query}':\n{output_text}"
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error performing keyword search: {str(e)}")]

async def read_note_content(filename: str) -> list[TextContent]:
    try:
        searcher = ZKSearcher()
        content = searcher.get_file_content(filename)
        if not content:
             return [TextContent(type="text", text=f"Note '{filename}' not found or empty.")]
        
        return [TextContent(
            type="text",
            text=f"Content of {filename}:\n\n{content}"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"Error reading note: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
