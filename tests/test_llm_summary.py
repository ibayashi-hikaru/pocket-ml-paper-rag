"""Tests for LLM summarization (with mocks)."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.llm_summary import LLMProcessor, summarize_text, extract_keywords


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="This is a test summary."))
    ]
    return mock_response


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@patch("app.llm_summary.OpenAI")
def test_llm_processor_initialization(mock_openai):
    """Test LLM processor initialization."""
    processor = LLMProcessor()
    assert processor.api_key == "test-key"
    assert processor.model == "gpt-4o-mini"


@patch.dict(os.environ, {}, clear=True)
def test_llm_processor_no_key():
    """Test LLM processor fails without API key."""
    with pytest.raises(ValueError, match="OpenAI API key not provided"):
        LLMProcessor()


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@patch("app.llm_summary.OpenAI")
@pytest.mark.asyncio
async def test_summarize_text(mock_openai_class, mock_openai_response):
    """Test text summarization."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai_class.return_value = mock_client

    processor = LLMProcessor()
    summary = await processor.summarize("This is a long text that needs summarization.")

    assert summary == "This is a test summary."
    mock_client.chat.completions.create.assert_called_once()


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@patch("app.llm_summary.OpenAI")
@pytest.mark.asyncio
async def test_extract_keywords(mock_openai_class):
    """Test keyword extraction."""
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="machine learning, deep learning, neural networks"))
    ]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai_class.return_value = mock_client

    processor = LLMProcessor()
    keywords = await processor.extract_keywords("Text about machine learning and neural networks.")

    assert isinstance(keywords, list)
    assert len(keywords) > 0
    assert "machine learning" in keywords or "machine" in keywords


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@pytest.mark.asyncio
async def test_summarize_text_function():
    """Test summarize_text convenience function."""
    with patch("app.llm_summary._get_llm_processor") as mock_get:
        mock_processor = MagicMock()
        mock_processor.summarize = AsyncMock(return_value="Test summary")
        mock_get.return_value = mock_processor

        summary = await summarize_text("Test text")
        assert summary == "Test summary"


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@pytest.mark.asyncio
async def test_extract_keywords_function():
    """Test extract_keywords convenience function."""
    with patch("app.llm_summary._get_llm_processor") as mock_get:
        mock_processor = MagicMock()
        mock_processor.extract_keywords = AsyncMock(return_value=["keyword1", "keyword2"])
        mock_get.return_value = mock_processor

        keywords = await extract_keywords("Test text")
        assert keywords == ["keyword1", "keyword2"]

