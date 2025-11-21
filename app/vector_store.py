"""Vector database integration using Chroma."""

import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any

import chromadb
from chromadb.config import Settings
import numpy as np


class VectorStore:
    """Vector store for paper embeddings using Chroma."""

    def __init__(self, embedder, persist_directory: str = "db/chroma"):
        """
        Initialize the vector store.

        Args:
            embedder: Embedder instance for generating embeddings
            persist_directory: Directory to persist Chroma database
        """
        self.embedder = embedder
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False),
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="ml_papers",
            metadata={"hnsw:space": "cosine"},  # Use cosine similarity
        )

    def is_ready(self) -> bool:
        """Check if vector store is ready."""
        try:
            return self.collection is not None
        except Exception:
            return False

    def add_paper(
        self,
        title: str,
        summary: str,
        keywords: List[str],
        content_snippet: str,
        full_text: str,
        embedding: np.ndarray,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a paper to the vector store.

        Args:
            title: Paper title
            summary: Paper summary
            keywords: List of keywords
            content_snippet: Content snippet
            full_text: Full text of the paper
            embedding: Embedding vector
            metadata: Additional metadata

        Returns:
            Paper ID (UUID string)
        """
        paper_id = str(uuid.uuid4())

        # Prepare metadata
        paper_metadata = {
            "title": title,
            "summary": summary,
            "keywords": ",".join(keywords),
            "content_snippet": content_snippet,
            "full_text_length": len(full_text),
            **(metadata or {}),
        }

        # Convert embedding to list
        embedding_list = embedding.tolist() if isinstance(embedding, np.ndarray) else embedding

        # Add to collection
        self.collection.add(
            ids=[paper_id],
            embeddings=[embedding_list],
            metadatas=[paper_metadata],
            documents=[content_snippet],  # Store snippet as document
        )

        return paper_id

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar papers.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of result dictionaries with id, distance, and metadata
        """
        query_embedding_list = (
            query_embedding.tolist()
            if isinstance(query_embedding, np.ndarray)
            else query_embedding
        )

        # Perform search
        results = self.collection.query(
            query_embeddings=[query_embedding_list],
            n_results=top_k,
            where=filter_metadata,
        )

        # Format results
        formatted_results = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                result = {
                    "id": results["ids"][0][i],
                    "distance": results["distances"][0][i] if results["distances"] else None,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "document": results["documents"][0][i] if results["documents"] else "",
                }
                formatted_results.append(result)

        return formatted_results

    def get_paper(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a paper by ID.

        Args:
            paper_id: Paper ID

        Returns:
            Paper data dictionary or None if not found
        """
        try:
            results = self.collection.get(ids=[paper_id])
            if results["ids"] and len(results["ids"]) > 0:
                return {
                    "id": results["ids"][0],
                    "metadata": results["metadatas"][0] if results["metadatas"] else {},
                    "document": results["documents"][0] if results["documents"] else "",
                }
            return None

        except Exception:
            return None

    def list_all_papers(self) -> List[Dict[str, Any]]:
        """
        List all papers in the database.

        Returns:
            List of paper dictionaries
        """
        try:
            results = self.collection.get()
            papers = []
            if results["ids"]:
                for i in range(len(results["ids"])):
                    paper = {
                        "id": results["ids"][i],
                        "metadata": results["metadatas"][i] if results["metadatas"] else {},
                        "document": results["documents"][i] if results["documents"] else "",
                    }
                    papers.append(paper)
            return papers

        except Exception:
            return []

    def delete_paper(self, paper_id: str) -> bool:
        """
        Delete a paper from the database.

        Args:
            paper_id: Paper ID

        Returns:
            True if deleted, False otherwise
        """
        try:
            self.collection.delete(ids=[paper_id])
            return True
        except Exception:
            return False

    def count(self) -> int:
        """Get the number of papers in the database."""
        try:
            return self.collection.count()
        except Exception:
            return 0

