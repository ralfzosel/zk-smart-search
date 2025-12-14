import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Add parent directory to path so we can import zkss
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zkss import ZKSearcher

class TestZKSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = ZKSearcher(base_dir="/tmp/test_zk", ending=".md")

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

if __name__ == '__main__':
    unittest.main()
