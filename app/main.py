"""FastAPI main application."""

import os
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.pdf_extraction import extract_text_from_pdf
from app.llm_summary import summarize_text, extract_keywords
from app.embedder import Embedder
from app.vector_store import VectorStore
from app.query_engine import QueryEngine

app = FastAPI(
    title="ML Paper Recommender API",
    description="Personal LLM-powered ML paper recommendation engine",
    version="0.1.0",
)

# Initialize components
embedder = Embedder()
vector_store = VectorStore(embedder)
query_engine = QueryEngine(vector_store, embedder)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
DB_DIR = Path("db/chroma")
DB_DIR.mkdir(parents=True, exist_ok=True)


class PaperResponse(BaseModel):
    """Response model for a paper."""

    id: str
    title: str
    summary: str
    keywords: List[str]
    content_snippet: str
    metadata: dict


class SearchResponse(BaseModel):
    """Response model for search results."""

    query: str
    papers: List[PaperResponse]
    explanations: List[str]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ML Paper Recommender API",
        "version": "0.1.0",
        "endpoints": {
            "upload": "/upload_pdf",
            "search": "/search",
            "paper": "/papers/{paper_id}",
            "health": "/health",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "vector_store_ready": vector_store.is_ready()}


@app.post("/upload_pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    title: Optional[str] = Query(None, description="Optional paper title override"),
):
    """
    Upload and process a PDF paper.

    Steps:
    1. Extract text from PDF
    2. Generate summary using LLM
    3. Extract keywords using LLM
    4. Create document representation
    5. Generate embedding
    6. Store in vector database
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extract text
        text = extract_text_from_pdf(file_path)
        if not text or len(text.strip()) < 100:
            raise HTTPException(
                status_code=400, detail="Could not extract sufficient text from PDF"
            )

        # Generate summary and keywords
        summary = await summarize_text(text)
        keywords = await extract_keywords(text)

        # Extract title (use provided or extract from text)
        if not title:
            # Try to extract title from first few lines
            lines = text.split("\n")[:5]
            title = lines[0].strip() if lines else file.filename.replace(".pdf", "")

        # Create content snippet (first 500 chars)
        content_snippet = text[:500].strip()

        # Build document representation
        doc_text = f"Title: {title}\n\nSummary: {summary}\n\nKeywords: {', '.join(keywords)}\n\nContent: {content_snippet}"

        # Generate embedding
        embedding = embedder.embed(doc_text)

        # Store in vector database
        paper_id = vector_store.add_paper(
            title=title,
            summary=summary,
            keywords=keywords,
            content_snippet=content_snippet,
            full_text=text,
            embedding=embedding,
            metadata={
                "filename": file.filename,
                "file_path": str(file_path),
            },
        )

        return {
            "paper_id": paper_id,
            "title": title,
            "summary": summary,
            "keywords": keywords,
            "content_snippet": content_snippet,
            "message": "Paper uploaded and processed successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.get("/search")
async def search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(5, ge=1, le=20, description="Number of results to return"),
):
    """
    Search for similar papers and get LLM explanations.

    Returns top-k similar papers with explanations of why they're relevant.
    """
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        results = await query_engine.search(query, top_k=top_k)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")


@app.get("/papers/{paper_id}")
async def get_paper(paper_id: str):
    """Get a specific paper by ID."""
    try:
        paper = vector_store.get_paper(paper_id)
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        return paper

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving paper: {str(e)}")


@app.get("/papers")
async def list_papers():
    """List all papers in the database."""
    try:
        papers = vector_store.list_all_papers()
        return {"papers": papers, "count": len(papers)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing papers: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

