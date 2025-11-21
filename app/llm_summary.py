"""LLM-based text summarization and keyword extraction."""

import os
from typing import List

from openai import OpenAI


class LLMProcessor:
    """Processor for LLM-based text analysis."""

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize LLM processor.

        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var.
            model: Model name to use (default: gpt-4o-mini).
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    async def summarize(self, text: str, max_sentences: int = 6) -> str:
        """
        Generate a concise summary of the text.

        Args:
            text: Text to summarize
            max_sentences: Maximum number of sentences in summary

        Returns:
            Summary string
        """
        # Truncate text if too long (to avoid token limits)
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."

        prompt = f"""Summarize the following research paper text in {max_sentences} sentences or less. Focus on the main contributions, methods, and findings.

Text:
{text}

Summary:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at summarizing research papers concisely and accurately.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=300,
            )

            summary = response.choices[0].message.content.strip()
            return summary

        except Exception as e:
            raise ValueError(f"Failed to generate summary: {str(e)}")

    async def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        Extract keywords from the text.

        Args:
            text: Text to extract keywords from
            num_keywords: Number of keywords to extract

        Returns:
            List of keyword strings
        """
        # Truncate text if too long
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."

        prompt = f"""Extract {num_keywords} key terms, techniques, or concepts from the following research paper text. Return only a comma-separated list of keywords, no explanations.

Text:
{text}

Keywords:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at identifying key terms and concepts in research papers.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=200,
            )

            keywords_str = response.choices[0].message.content.strip()
            # Parse comma-separated keywords
            keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
            # Limit to requested number
            keywords = keywords[:num_keywords]

            return keywords

        except Exception as e:
            raise ValueError(f"Failed to extract keywords: {str(e)}")


# Global instance
_llm_processor: LLMProcessor = None


def _get_llm_processor() -> LLMProcessor:
    """Get or create global LLM processor instance."""
    global _llm_processor
    if _llm_processor is None:
        _llm_processor = LLMProcessor()
    return _llm_processor


async def summarize_text(text: str, max_sentences: int = 6) -> str:
    """
    Summarize text using LLM.

    Args:
        text: Text to summarize
        max_sentences: Maximum number of sentences

    Returns:
        Summary string
    """
    processor = _get_llm_processor()
    return await processor.summarize(text, max_sentences)


async def extract_keywords(text: str, num_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using LLM.

    Args:
        text: Text to extract keywords from
        num_keywords: Number of keywords to extract

    Returns:
        List of keyword strings
    """
    processor = _get_llm_processor()
    return await processor.extract_keywords(text, num_keywords)

