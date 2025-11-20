"""Qdrant vector store implementation."""
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid
import time
import subprocess
import os

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
except ImportError:
    raise ImportError("Please install qdrant-client to use QdrantStore.")

class QdrantStore:
    def __init__(self, index_path: Optional[Path] = None, collection_name: str = "codebase", dim: int = 768, max_retries: int = 3):
        self.dim = dim
        self.collection_name = collection_name
        self.index_path = Path(index_path) if index_path else Path("./qdrant_data")
        
        # Try to connect with retry logic
        for attempt in range(max_retries):
            try:
                path_str = str(self.index_path)
                self.client = QdrantClient(path=path_str)
                break
            except RuntimeError as e:
                if "already accessed" in str(e) and attempt < max_retries - 1:
                    print(f"Qdrant lock detected (attempt {attempt + 1}/{max_retries}). Cleaning up...")
                    self._cleanup_stale_locks()
                    time.sleep(1)
                else:
                    raise
        
        # Ensure collection exists
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE),
            )
    
    def _cleanup_stale_locks(self):
        """Clean up stale lock files and kill zombie processes."""
        # Remove lock files
        lock_file = self.index_path / ".lock"
        if lock_file.exists():
            try:
                lock_file.unlink()
                print(f"Removed stale lock file: {lock_file}")
            except Exception as e:
                print(f"Failed to remove lock file: {e}")
        
        # Kill any zombie agentic-docs processes (except current)
        try:
            result = subprocess.run(
                ["pgrep", "-f", "agentic-docs"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                current_pid = os.getpid()
                for pid in result.stdout.strip().split('\n'):
                    if pid and int(pid) != current_pid:
                        try:
                            subprocess.run(["kill", "-9", pid], check=False)
                            print(f"Killed stale process: {pid}")
                        except Exception:
                            pass
        except Exception as e:
            print(f"Failed to clean up processes: {e}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Properly close the Qdrant client."""
        if hasattr(self, 'client') and self.client:
            try:
                self.client.close()
            except Exception:
                pass

    def add(self, vectors: np.ndarray, metadatas: List[Dict[str, Any]]):
        if len(vectors) != len(metadatas):
            raise ValueError("Vectors and metadata must have same length")
        
        points = []
        for i, (vec, meta) in enumerate(zip(vectors, metadatas)):
            # Qdrant requires unique IDs. We can use UUIDs or hash-based IDs.
            # Using UUIDs for simplicity here, or derived from symbol_id if stable.
            point_id = str(uuid.uuid4())
            points.append(models.PointStruct(
                id=point_id,
                vector=vec.tolist(),
                payload=meta
            ))
            
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        if query_vector.ndim > 1:
            query_vector = query_vector[0] # Take first if batch
            
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=k
        )
        
        results = []
        for hit in response.points:
            item = hit.payload.copy()
            item['score'] = hit.score
            results.append(item)
        return results

    def save(self, path: Path):
        # Qdrant persists automatically to the path given in __init__
        pass

    def load(self, path: Path):
        # Qdrant loads automatically from the path given in __init__
        pass
