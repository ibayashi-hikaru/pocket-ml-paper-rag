#!/usr/bin/env python3
"""Quick test script to verify the setup."""

import sys

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✓ fastapi")
    except ImportError as e:
        print(f"✗ fastapi: {e}")
        return False
    
    try:
        import uvicorn
        print("✓ uvicorn")
    except ImportError as e:
        print(f"✗ uvicorn: {e}")
        return False
    
    try:
        from pdfminer.high_level import extract_text
        print("✓ pdfminer.six")
    except ImportError as e:
        print(f"✗ pdfminer.six: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✓ sentence-transformers")
    except ImportError as e:
        print(f"✗ sentence-transformers: {e}")
        return False
    
    try:
        import chromadb
        print("✓ chromadb")
    except ImportError as e:
        print(f"✗ chromadb: {e}")
        return False
    
    try:
        import openai
        print("✓ openai")
    except ImportError as e:
        print(f"✗ openai: {e}")
        return False
    
    try:
        import streamlit
        print("✓ streamlit")
    except ImportError as e:
        print(f"✗ streamlit: {e}")
        return False
    
    return True

def test_app_imports():
    """Test that app modules can be imported."""
    print("\nTesting app imports...")
    
    try:
        from app.embedder import Embedder
        print("✓ app.embedder")
    except ImportError as e:
        print(f"✗ app.embedder: {e}")
        return False
    
    try:
        from app.pdf_extraction import extract_text_from_pdf
        print("✓ app.pdf_extraction")
    except ImportError as e:
        print(f"✗ app.pdf_extraction: {e}")
        return False
    
    try:
        from app.vector_store import VectorStore
        print("✓ app.vector_store")
    except ImportError as e:
        print(f"✗ app.vector_store: {e}")
        return False
    
    try:
        from app.llm_summary import LLMProcessor
        print("✓ app.llm_summary")
    except ImportError as e:
        print(f"✗ app.llm_summary: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.executable}\n")
    
    if not test_imports():
        print("\n❌ Some dependencies are missing!")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    if not test_app_imports():
        print("\n❌ Some app modules failed to import!")
        sys.exit(1)
    
    print("\n✅ All imports successful!")
    print("\nYou can now:")
    print("1. Run unit tests: pytest tests/ -v")
    print("2. Start the server: uvicorn app.main:app --reload")
    print("3. Start the UI: streamlit run ui/streamlit_app.py")

