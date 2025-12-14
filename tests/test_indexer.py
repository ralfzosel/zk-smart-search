import unittest
import os
import sys
from unittest.mock import MagicMock, patch, mock_open

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock external ML libraries BEFORE importing indexer
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.utils'] = MagicMock()
sys.modules['chromadb.utils.embedding_functions'] = MagicMock()

from indexer import IndexManager

class TestIndexManager(unittest.TestCase):
    def setUp(self):
        # Setup mocks for ChromaDB that IndexManager uses
        self.mock_client = MagicMock()
        self.mock_collection = MagicMock()
        self.mock_client.get_or_create_collection.return_value = self.mock_collection
        
        with patch('chromadb.PersistentClient', return_value=self.mock_client):
            self.indexer = IndexManager(base_dir="/tmp/test_zk")
        
        # Mock console
        self.indexer.console = MagicMock()

    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    def test_get_all_files(self, mock_mtime, mock_isfile, mock_listdir):
        """Test scanning directory for files and mtimes."""
        mock_listdir.return_value = ["note1.md", "note2.md", "image.png", "folder"]
        mock_isfile.side_effect = lambda p: "folder" not in p
        mock_mtime.return_value = 12345.0

        files = self.indexer._get_all_files()
        
        self.assertEqual(len(files), 2)
        self.assertIn("note1.md", files)
        self.assertIn("note2.md", files)
        self.assertNotIn("image.png", files) # Wrong extension

    def test_update_index_incremental(self):
        """Test logic for identifying new, modified, and deleted files."""
        # 1. Setup Filesystem state
        current_files = {
            "new.md": 2000.0,      # New file
            "modified.md": 2000.0, # Modified (newer than DB)
            "unchanged.md": 1000.0 # Unchanged
        }
        
        # 2. Setup DB state
        # existing in DB: modified (old), unchanged, deleted
        existing_ids = ["modified.md", "unchanged.md", "deleted.md"]
        existing_metadatas = [
            {"mtime": 1000.0}, # Old mtime
            {"mtime": 1000.0}, # Same mtime
            {"mtime": 1000.0}
        ]
        
        self.mock_collection.get.return_value = {
            'ids': existing_ids,
            'metadatas': existing_metadatas
        }

        # Mock _get_all_files to return our controlled state
        self.indexer._get_all_files = MagicMock(return_value=current_files)

        # Mock file reading
        with patch('builtins.open', mock_open(read_data="content")):
            self.indexer.update_index()

        # 3. Assertions
        
        # Verify Upserts (New + Modified)
        # Should upsert "new.md" and "modified.md"
        # "unchanged.md" should be skipped
        self.assertTrue(self.mock_collection.upsert.called)
        call_args = self.mock_collection.upsert.call_args[1] # kwargs
        
        upserted_ids = call_args['ids']
        self.assertIn("new.md", upserted_ids)
        self.assertIn("modified.md", upserted_ids)
        self.assertNotIn("unchanged.md", upserted_ids)
        
        # Verify Deletes
        # Should delete "deleted.md"
        self.mock_collection.delete.assert_called_with(ids=["deleted.md"])

    def test_search(self):
        """Test search delegation to collection."""
        self.mock_collection.query.return_value = {'ids': [['result1.md', 'result2.md']]}
        
        results = self.indexer.search("query")
        
        self.mock_collection.query.assert_called_with(
            query_texts=["query"],
            n_results=15
        )
        self.assertEqual(results, ['result1.md', 'result2.md'])

if __name__ == '__main__':
    unittest.main()
