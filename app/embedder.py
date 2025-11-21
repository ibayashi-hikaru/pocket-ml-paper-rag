"""Embedding generation using sentence-transformers."""

from typing import List, Union

import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    """Embedding generator using sentence-transformers."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        normalize: bool = True,
    ):
        """
        Initialize the embedder.

        Args:
            model_name: Name of the sentence-transformers model
            normalize: Whether to normalize embeddings (L2 norm)
        """
        self.model_name = model_name
        self.normalize = normalize
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def embed(self, text: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Generate embedding(s) for text.

        Args:
            text: Single text string or list of text strings

        Returns:
            Embedding vector(s) as numpy array(s)
        """
        if isinstance(text, str):
            embeddings = self.model.encode(
                text,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
            )
            return embeddings
        else:
            embeddings = self.model.encode(
                text,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
            )
            return embeddings

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[np.ndarray]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of text strings
            batch_size: Batch size for processing

        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=self.normalize,
            batch_size=batch_size,
            show_progress_bar=True,
        )
        return embeddings.tolist()

    def get_embedding_dim(self) -> int:
        """Get the dimension of embeddings."""
        return self.embedding_dim

