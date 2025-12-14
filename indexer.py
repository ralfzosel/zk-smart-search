import os
import time
from typing import List, Dict, Optional
import chromadb
from chromadb.utils import embedding_functions
from rich.console import Console
from rich.progress import track

from settings import ZK_BASE_DIR, ENDING

class IndexManager:
    DB_DIR_NAME = ".zkss_index"
    COLLECTION_NAME = "zettelkasten"
    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self, base_dir: str = ZK_BASE_DIR):
        self.base_dir = base_dir
        self.db_path = os.path.join(os.path.expanduser("~"), self.DB_DIR_NAME)
        self.console = Console()
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Use Sentence Transformer for embeddings
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.MODEL_NAME
        )
        
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def _get_all_files(self) -> Dict[str, float]:
        """Returns a dict of {filename: mtime} for all valid zettels."""
        files = {}
        try:
            for f in os.listdir(self.base_dir):
                full_path = os.path.join(self.base_dir, f)
                if os.path.isfile(full_path) and f.endswith(ENDING):
                    files[f] = os.path.getmtime(full_path)
        except FileNotFoundError:
            self.console.print(f"[red]Directory not found: {self.base_dir}[/red]")
        return files

    def update_index(self, force_reindex: bool = False):
        """
        Synchronizes the vector index with the filesystem.
        Adds new/modified files, removes deleted ones.
        """
        current_files = self._get_all_files()
        
        if not current_files:
            return

        # Get existing IDs from DB
        existing_data = self.collection.get(include=['metadatas'])
        existing_ids = set(existing_data['ids'])
        existing_metadata = {
            id_: meta 
            for id_, meta in zip(existing_data['ids'], existing_data['metadatas']) 
            if meta
        }

        # Determine changes
        to_add = []
        to_update = []
        to_delete = []

        for filename, mtime in current_files.items():
            if filename not in existing_ids:
                to_add.append(filename)
            elif force_reindex or existing_metadata.get(filename, {}).get('mtime', 0) < mtime:
                to_update.append(filename)
        
        for filename in existing_ids:
            if filename not in current_files:
                to_delete.append(filename)

        # Execute changes
        if to_delete:
            self.console.print(f"[yellow]Removing {len(to_delete)} deleted files from index...[/yellow]")
            self.collection.delete(ids=to_delete)

        files_to_process = to_add + to_update
        if files_to_process:
            self.console.print(f"[green]Indexing {len(files_to_process)} files...[/green]")
            
            ids = []
            documents = []
            metadatas = []

            for filename in track(files_to_process, description="Embedding..."):
                try:
                    with open(os.path.join(self.base_dir, filename), "r", errors="ignore") as f:
                        content = f.read()
                    
                    ids.append(filename)
                    documents.append(content)
                    metadatas.append({"mtime": current_files[filename]})
                    
                    # Batch processing to avoid memory issues with huge lists
                    if len(ids) >= 100:
                        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
                        ids = []
                        documents = []
                        metadatas = []
                except Exception as e:
                    self.console.print(f"[red]Error reading {filename}: {e}[/red]")

            # Process remaining batch
            if ids:
                self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            
            self.console.print("[bold green]Index updated successfully![/bold green]")
        else:
            if not to_delete:
                pass 
                # self.console.print("Index is up to date.") 

    def search(self, query_text: str, n_results: int = 15) -> List[str]:
        """
        Performs a semantic search and returns a list of filenames.
        """
        # Ensure index is roughly up to date (lightweight check could go here, 
        # but for now we rely on explicit update or call update_index() implicitly)
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Chroma returns lists of lists (one list per query string)
        if results['ids']:
            return results['ids'][0]
        return []
