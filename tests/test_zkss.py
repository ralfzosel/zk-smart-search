import unittest
import os
import sys
from unittest.mock import MagicMock, patch, mock_open

# Add parent directory to path so we can import zkss
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zkss import ZKSearcher

class TestZKSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = ZKSearcher(base_dir="/tmp/test_zk", ending=".md")
        # Mock the console to prevent printing during tests
        self.searcher.console = MagicMock()

    def test_strip_ending(self):
        """Test that strip_ending removes the configured extension."""
        self.assertEqual(self.searcher.strip_ending("note.md"), "note")
        self.assertEqual(self.searcher.strip_ending("image.png"), "image.png")
        self.assertEqual(self.searcher.strip_ending("archive.tar.gz"), "archive.tar.gz")
        
        # Test with different ending
        txt_searcher = ZKSearcher(ending=".txt")
        self.assertEqual(txt_searcher.strip_ending("note.txt"), "note")
        self.assertEqual(txt_searcher.strip_ending("note.md"), "note.md")

    def test_strip_ending_regex_safety(self):
        """Test strip_ending with special characters."""
        self.assertEqual(self.searcher.strip_ending("my[note].md"), "my[note]")
        self.assertEqual(self.searcher.strip_ending("version 1.0.md"), "version 1.0")

    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.lstat')
    def test_get_sorted_filenames(self, mock_lstat, mock_isfile, mock_listdir):
        """Test getting files sorted by access time."""
        # Setup mocks
        mock_listdir.return_value = ["file1.md", "file2.md", "not_a_note.txt", "folder"]
        
        # mock isfile to return true for files and false for folders
        def isfile_side_effect(path):
            return "folder" not in path
        mock_isfile.side_effect = isfile_side_effect
        
        # mock lstat to return different access times
        mock_stat1 = MagicMock()
        mock_stat1.st_atime = 1000 # Older
        
        mock_stat2 = MagicMock()
        mock_stat2.st_atime = 2000 # Newer
        
        def lstat_side_effect(path):
            if "file1.md" in path: return mock_stat1
            if "file2.md" in path: return mock_stat2
            return MagicMock()
        mock_lstat.side_effect = lstat_side_effect

        # Run method
        files = self.searcher.get_sorted_filenames()

        # Check results
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0], "file2.md") # Newer should be first
        self.assertEqual(files[1], "file1.md")

    def test_filter_and_print(self):
        """Test that filter_and_print correctly separates matches and calls console."""
        filenames = ["match.md", "no_match.md", "match2.md"]
        
        def predicate(filename):
            return "match" in filename and "no" not in filename

        # Run method
        remaining = self.searcher.filter_and_print(filenames, predicate, "Header")

        # Check returned remaining files
        self.assertEqual(remaining, ["no_match.md"])
        
        # Check console calls
        # Should print header once
        self.searcher.console.print.assert_any_call("Header")
        # Should print matched filenames
        self.searcher.console.print.assert_any_call("    match")
        self.searcher.console.print.assert_any_call("    match2")

    def test_get_file_content(self):
        """Test reading file content safely."""
        with patch('builtins.open', mock_open(read_data="Content HERE")) as mock_file:
            content = self.searcher.get_file_content("test.md")
            self.assertEqual(content, "content here") # Should be lowercased
            mock_file.assert_called_with("/tmp/test_zk/test.md", "r", errors="ignore")

    def test_get_file_content_error(self):
        """Test handling of read errors."""
        with patch('builtins.open', side_effect=PermissionError):
            content = self.searcher.get_file_content("test.md")
            self.assertEqual(content, "")

if __name__ == '__main__':
    unittest.main()
