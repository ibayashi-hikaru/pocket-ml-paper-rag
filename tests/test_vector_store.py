"""Tests for vector store."""

import numpy as np
import pytest
from pathlib import Path
import shutil

from app.embedder import Embedder
from app.vector_store import VectorStore


@pytest.fixture
def temp_db_dir(tmp_path):
    """Create a temporary database directory."""
    db_dir = tmp_path / "test_chroma"
    yield db_dir
    # Cleanup
    if db_dir.exists():
        shutil.rmtree(db_dir, ignore_errors=True)


@pytest.fixture
def embedder():
    """Create embedder instance."""
    return Embedder()


@pytest.fixture
def vector_store(temp_db_dir, embedder):
    """Create vector store instance."""
    return VectorStore(embedder, persist_directory=str(temp_db_dir))


def test_vector_store_initialization(vector_store):
    """Test vector store initialization."""
    assert vector_store.is_ready()
    assert vector_store.count() == 0


def test_add_paper(vector_store, embedder):
    """Test adding a paper to the vector store."""
    title = "Test Paper"
    summary = "This is a test summary."
    keywords = ["test", "paper", "example"]
    content_snippet = "This is a content snippet."
    full_text = "This is the full text of the paper."
    embedding = embedder.embed("Test document text")

    paper_id = vector_store.add_paper(
        title=title,
        summary=summary,
        keywords=keywords,
        content_snippet=content_snippet,
        full_text=full_text,
        embedding=embedding,
    )

    assert paper_id is not None
    assert isinstance(paper_id, str)
    assert vector_store.count() == 1


def test_search_papers(vector_store, embedder):
    """Test searching for papers."""
    # Add a few papers
    texts = [
        "Machine learning and deep learning",
        "Natural language processing and transformers",
        "Computer vision and image recognition",
    ]

    for i, text in enumerate(texts):
        embedding = embedder.embed(text)
        vector_store.add_paper(
            title=f"Paper {i+1}",
            summary=f"Summary {i+1}",
            keywords=["keyword1", "keyword2"],
            content_snippet=text,
            full_text=text * 10,
            embedding=embedding,
        )

    # Search for similar papers
    query = "deep learning neural networks"
    query_embedding = embedder.embed(query)
    results = vector_store.search(query_embedding, top_k=2)

    assert len(results) <= 2
    assert all("id" in result for result in results)
    assert all("metadata" in result for result in results)


def test_get_paper(vector_store, embedder):
    """Test retrieving a paper by ID."""
    embedding = embedder.embed("Test paper content")
    paper_id = vector_store.add_paper(
        title="Test Paper",
        summary="Test summary",
        keywords=["test"],
        content_snippet="Snippet",
        full_text="Full text",
        embedding=embedding,
    )

    paper = vector_store.get_paper(paper_id)
    assert paper is not None
    assert paper["id"] == paper_id
    assert paper["metadata"]["title"] == "Test Paper"


def test_list_all_papers(vector_store, embedder):
    """Test listing all papers."""
    # Add multiple papers
    for i in range(3):
        embedding = embedder.embed(f"Paper {i} content")
        vector_store.add_paper(
            title=f"Paper {i}",
            summary=f"Summary {i}",
            keywords=["test"],
            content_snippet=f"Snippet {i}",
            full_text=f"Full text {i}",
            embedding=embedding,
        )

    papers = vector_store.list_all_papers()
    assert len(papers) == 3


def test_delete_paper(vector_store, embedder):
    """Test deleting a paper."""
    embedding = embedder.embed("Test content")
    paper_id = vector_store.add_paper(
        title="Test",
        summary="Summary",
        keywords=["test"],
        content_snippet="Snippet",
        full_text="Full",
        embedding=embedding,
    )

    assert vector_store.count() == 1
    success = vector_store.delete_paper(paper_id)
    assert success is True
    assert vector_store.count() == 0

