import unittest
import sys
import os
import asyncio
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server import list_tools, call_tool

class TestMCPServerIntegration(unittest.TestCase):
    def test_list_tools_in_process(self):
        """Test listing tools by importing the server module."""
        tools = asyncio.run(list_tools())
        
        tool_names = [t.name for t in tools]
        self.assertIn("search_notes", tool_names)
        self.assertIn("read_note", tool_names)
        
        # Verify schema
        search_tool = next(t for t in tools if t.name == "search_notes")
        self.assertIn("query", search_tool.inputSchema["properties"])
        self.assertIn("semantic", search_tool.inputSchema["properties"])

    @patch('mcp_server.perform_keyword_search')
    def test_call_tool_keyword_search(self, mock_search):
        """Test calling search_notes triggers keyword search."""
        # Setup mock return
        mock_search.return_value = ["Result"]
        
        # Call tool
        result = asyncio.run(call_tool("search_notes", {"query": "test query", "semantic": False}))
        
        # Verify
        mock_search.assert_called_with("test query")
        self.assertEqual(result, ["Result"])

    @patch('mcp_server.perform_semantic_search')
    def test_call_tool_semantic_search(self, mock_search):
        """Test calling search_notes triggers semantic search."""
        mock_search.return_value = ["Result"]
        
        asyncio.run(call_tool("search_notes", {"query": "test query", "semantic": True, "limit": 10}))
        
        mock_search.assert_called_with("test query", 10)

    @patch('mcp_server.read_note_content')
    def test_call_tool_read_note(self, mock_read):
        """Test calling read_note."""
        mock_read.return_value = ["Content"]
        
        asyncio.run(call_tool("read_note", {"filename": "note.md"}))
        
        mock_read.assert_called_with("note.md")

if __name__ == '__main__':
    unittest.main()
