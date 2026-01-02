import pytest
import asyncio
from unittest.mock import patch, MagicMock
from zkss_markdown import convert_rich_to_markdown
from mcp_server import perform_keyword_search, perform_semantic_search

def test_convert_rich_to_markdown_basic():
    """Test basic green (stripped) and yellow (bold) tag conversion."""
    markup = "[green]keyword[/green] in [yellow]filename[/yellow]"
    expected = "keyword in **filename**"
    assert convert_rich_to_markdown(markup) == expected

def test_convert_rich_to_markdown_no_closing():
    """Test tags without closing tags (Rich renders these to the end)."""
    markup = "[yellow]filename: content"
    expected = "**filename: content**"
    assert convert_rich_to_markdown(markup) == expected

def test_convert_rich_to_markdown_bold_colors():
    """Test bold combined with colors."""
    markup = "[bold green]Match found:[/bold green]"
    expected = "Match found:"
    assert convert_rich_to_markdown(markup) == expected

def test_convert_rich_to_markdown_strip_others():
    """Test that other Rich tags are stripped."""
    markup = "[blue]Blue text[/blue] [red]Red text[/red] [green]Green[/green]"
    expected = "Blue text Red text Green"
    assert convert_rich_to_markdown(markup) == expected

def test_convert_rich_to_markdown_empty():
    """Test empty input."""
    assert convert_rich_to_markdown("") == ""
    assert convert_rich_to_markdown(None) == ""

def test_convert_rich_to_markdown_mixed():
    """Test complex mixed markup."""
    markup = "[yellow]File:[/yellow] [green]key1[/green] and [green]key2[/green] found in [blue]section 1[/blue]"
    expected = "**File:** key1 and key2 found in section 1"
    assert convert_rich_to_markdown(markup) == expected

def test_perform_keyword_search_markdown_formatting():
    """Verify that keyword search output is converted to markdown."""
    with patch('mcp_server.ZKSearcher') as mock_searcher_class:
        mock_searcher = MagicMock()
        mock_searcher_class.return_value = mock_searcher
        
        def mock_run():
            mock_searcher.console.print("[green]Found 1 relevant notes:[/green]")
            mock_searcher.console.print("- \"test\" in [yellow]filename:")
            mock_searcher.console.print("    20231027 Test Note")
            
        mock_searcher.run.side_effect = mock_run
        
        results = asyncio.run(perform_keyword_search("test"))
        output = results[0].text
        
        # [green] should be stripped, not backticked
        assert "Found 1 relevant notes:" in output
        # [yellow] should be bold
        assert "- \"test\" in **filename:**" in output
        assert "    20231027 Test Note" in output
        assert "[green]" not in output
        assert "[yellow]" not in output
        assert "`" not in output # Verify no backticks for keywords

def test_perform_semantic_search_markdown_formatting():
    """Verify that semantic search output uses bold for filenames."""
    with patch('mcp_server.IndexManager') as mock_index_class:
        mock_index = MagicMock()
        mock_index_class.return_value = mock_index
        mock_index.search.return_value = ["20231027 Test Note.md"]
        
        with patch('mcp_server.ZKSearcher') as mock_searcher_class:
            mock_searcher = MagicMock()
            mock_searcher_class.return_value = mock_searcher
            mock_searcher.strip_ending.return_value = "20231027 Test Note"
            
            results = asyncio.run(perform_semantic_search("test", 5))
            output = results[0].text
            
            assert "**20231027 Test Note**" in output
            assert "(20231027 Test Note.md)" in output
