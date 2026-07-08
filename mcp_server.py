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

# Quiet noisy ML/HF tooling before those libraries are imported. This only
# reduces log noise; the stdout guard below is what actually protects the
# JSON-RPC protocol.
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zkss import ZKSearcher
from indexer import IndexManager
from zkss_markdown import convert_rich_to_markdown
from settings import ENDING

# Initialize Server
server = Server("zk-smart-search")


def format_note_hit(filename: str, title: str | None = None) -> str:
    """Format a search hit with a copy-paste-ready filename for read_note."""
    if title is None:
        title = ZKSearcher().strip_ending(filename)
    return f"- **{title}** — `{filename}`"


def _append_filenames_to_keyword_results(text: str) -> str:
    """Turn bare note titles into read_note-ready filenames in keyword output."""
    lines = []
    for line in text.splitlines():
        if line.startswith("    ") and line.strip():
            title = line.strip()
            if title.endswith(ENDING):
                filename = title
            else:
                filename = f"{title}{ENDING}"
            lines.append(f"    {format_note_hit(filename, title)}")
        else:
            lines.append(line)
    return "\n".join(lines)

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
            description="Search for notes in the Zettelkasten. Supports both exact keyword matching (default) and semantic/meaning-based search. Results include the note filename (with .md suffix) for use with read_note.",
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
            description="Read the full content of a note. Use the filename from search_notes results (including the .md suffix).",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Note filename, e.g. '202203291059 my django_project.md'. The .md suffix may be omitted."
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
        
        formatted_results = [format_note_hit(fname) for fname in results]
            
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
        output_text = _append_filenames_to_keyword_results("\n".join(formatted_lines))
        
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
        if not content and filename and not filename.endswith(ENDING):
            filename = f"{filename}{ENDING}"
            content = searcher.get_file_content(filename)
        if not content:
             return [TextContent(type="text", text=f"Note '{filename}' not found or empty.")]
        
        return [TextContent(
            type="text",
            text=f"Content of {filename}:\n\n{content}"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"Error reading note: {str(e)}")]

def _install_stdout_guard():
    """
    stdio MCP uses stdout exclusively for JSON-RPC. Any stray text written to
    stdout by our dependencies (rich/tqdm progress bars, sentence-transformers,
    chromadb, huggingface_hub) corrupts the message stream and drops the
    connection with errors like `Unexpected token ... is not valid JSON`.

    We keep a private copy of the real stdout for the transport, then point the
    process's stdout at stderr so nothing else can pollute the protocol.
    """
    sys.stdout.flush()
    saved_stdout_fd = os.dup(1)          # private JSON-RPC channel
    os.dup2(2, 1)                        # fd 1 now writes to stderr
    private_stdout = os.fdopen(saved_stdout_fd, "w", encoding="utf-8", buffering=1)
    sys.stdout = sys.stderr              # Python-level prints go to stderr too
    return private_stdout


async def main():
    private_stdout = _install_stdout_guard()
    async with stdio_server(stdout=anyio.wrap_file(private_stdout)) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
