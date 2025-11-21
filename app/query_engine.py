"""Query engine for searching papers and generating explanations."""

import os
from typing import List, Dict, Any

from openai import OpenAI

from app.embedder import Embedder
from app.vector_store import VectorStore


class QueryEngine:
    """Engine for querying papers and generating LLM explanations."""

    def __init__(self, vector_store: VectorStore, embedder: Embedder):
        """
        Initialize the query engine.

        Args:
            vector_store: Vector store instance
            embedder: Embedder instance
        """
        self.vector_store = vector_store
        self.embedder = embedder

        # Initialize LLM client for explanations
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.llm_client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    async def search(
        self, query: str, top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Search for similar papers and generate explanations.

        Args:
            query: Search query string
            top_k: Number of results to return

        Returns:
            Dictionary with query, papers, and explanations
        """
        # Embed the query
        query_embedding = self.embedder.embed(query)

        # Search vector store
        results = self.vector_store.search(query_embedding, top_k=top_k)

        # Format papers
        papers = []
        for result in results:
            metadata = result.get("metadata", {})
            paper = {
                "id": result.get("id"),
                "title": metadata.get("title", "Unknown"),
                "summary": metadata.get("summary", ""),
                "keywords": metadata.get("keywords", "").split(",")
                if metadata.get("keywords")
                else [],
                "content_snippet": metadata.get("content_snippet", ""),
                "metadata": metadata,
                "similarity_score": 1.0 - result.get("distance", 0.0),  # Convert distance to similarity
            }
            papers.append(paper)

        # Generate explanations
        explanations = await self._generate_explanations(query, papers)

        return {
            "query": query,
            "papers": papers,
            "explanations": explanations,
        }

    async def _generate_explanations(
        self, query: str, papers: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate LLM explanations for why each paper is relevant.

        Args:
            query: Original search query
            papers: List of paper dictionaries

        Returns:
            List of explanation strings
        """
        explanations = []

        for paper in papers:
            title = paper.get("title", "Unknown")
            summary = paper.get("summary", "")
            keywords = ", ".join(paper.get("keywords", []))

            prompt = f"""Given the user query "{query}", explain in 1-2 sentences why this research paper is relevant:

Title: {title}
Summary: {summary}
Keywords: {keywords}

Explanation:"""

            try:
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert at explaining why research papers are relevant to queries. Be concise and specific.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=150,
                )

                explanation = response.choices[0].message.content.strip()
                explanations.append(explanation)

            except Exception as e:
                # Fallback explanation if LLM fails
                explanations.append(
                    f"This paper is relevant because it matches keywords and topics from your query."
                )

        return explanations

