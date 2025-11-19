"""FAISS vector store implementation."""
import faiss
import numpy as np
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..types import Symbol

class FAISSStore:
    def __init__(self, index_path: Optional[Path] = None, dim: int = 768):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim) # Inner Product (Cosine if normalized)
        self.metadata: List[Dict[str, Any]] = []
        self.index_path = index_path

    def add(self, vectors: np.ndarray, metadatas: List[Dict[str, Any]]):
        if len(vectors) != len(metadatas):
            raise ValueError("Vectors and metadata must have same length")
        
        # Normalize for cosine similarity
        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self.metadata.extend(metadatas)

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        
        faiss.normalize_L2(query_vector)
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx].copy()
                item['score'] = float(dist)
                results.append(item)
        return results

    def save(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / "index.faiss"))
        with open(path / "metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self, path: Path):
        if not (path / "index.faiss").exists():
            return
        self.index = faiss.read_index(str(path / "index.faiss"))
        with open(path / "metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)
