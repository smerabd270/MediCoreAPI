import os
import json
import hashlib
from app.core.config import settings

class VectorStoreManager:
    """
    100% Offline Local Context Manager.
    Bypasses [WinError 10054] by storing text slices directly in a local text index file.
    Requires no internet download, no network ports, and no model weight streams.
    """
    def __init__(self):
        self.storage_dir = "./vector_db"
        self.storage_file = os.path.join(self.storage_dir, "offline_knowledge.json")
        
        # Ensure local folder structure exists
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Load pre-existing document memory blocks from your disk path
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as f:
                self.database = json.load(f)
        else:
            self.database = {}

    def add_documents(self, text_chunks: list[str], doc_id_prefix: str) -> None:
        """Persists text segments safely to a zero-network text ledger cache file."""
        if not text_chunks:
            return
            
        for i, chunk in enumerate(text_chunks):
            chunk_id = f"{doc_id_prefix}_{i}"
            self.database[chunk_id] = chunk
            
        # Commit text index layout directly to the local storage target
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.database, f, ensure_ascii=False, indent=4)

    def query_similarity(self, query_text: str, n_results: int = 3) -> str:
        """Runs a completely offline word-matching overlap loop to extract relevant paragraphs."""
        if not self.database:
            return ""
            
        query_words = set(query_text.lower().split())
        matched_chunks = []
        
        # Chronologically score context paragraphs based on keyword intersect counts
        for chunk_id, content in self.database.items():
            content_words = content.lower().split()
            score = sum(1 for word in query_words if word in content_words)
            if score > 0:
                matched_chunks.append((score, content))
                
        # Sort contexts to prioritize the highest keyword match rates
        matched_chunks.sort(key=lambda x: x[0], reverse=True)
        top_results = [item[1] for item in matched_chunks[:n_results]]
        
        return "\n\n".join(top_results) if top_results else ""
