"""Tests for embedding generation."""

import numpy as np
import pytest

from app.embedder import Embedder


def test_embedder_initialization():
    """Test embedder initialization."""
    embedder = Embedder()
    assert embedder.model_name == "all-MiniLM-L6-v2"
    assert embedder.normalize is True
    assert embedder.embedding_dim > 0


def test_embed_single_text():
    """Test embedding a single text."""
    embedder = Embedder()
    text = "This is a test sentence."
    embedding = embedder.embed(text)

    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (embedder.embedding_dim,)
    assert not np.isnan(embedding).any()


def test_embed_multiple_texts():
    """Test embedding multiple texts."""
    embedder = Embedder()
    texts = ["First sentence.", "Second sentence.", "Third sentence."]
    embeddings = embedder.embed(texts)

    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape[0] == len(texts)
    assert embeddings.shape[1] == embedder.embedding_dim


def test_embed_batch():
    """Test batch embedding."""
    embedder = Embedder()
    texts = [f"Sentence {i}." for i in range(10)]
    embeddings = embedder.embed_batch(texts)

    assert len(embeddings) == len(texts)
    assert all(isinstance(emb, list) for emb in embeddings)


def test_normalized_embeddings():
    """Test that embeddings are normalized when normalize=True."""
    embedder = Embedder(normalize=True)
    text = "Test sentence for normalization."
    embedding = embedder.embed(text)

    # Check L2 norm is approximately 1
    norm = np.linalg.norm(embedding)
    assert abs(norm - 1.0) < 0.01  # Allow small floating point error

