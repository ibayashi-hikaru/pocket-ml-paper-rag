# Testing Guide

## 🧪 Running Unit Tests

### Run All Tests
```bash
# Make sure you're in the project directory and venv is activated
source venv/bin/activate
pytest tests/ -v
```

### Run Specific Test Files
```bash
# Test PDF extraction
pytest tests/test_pdf_extraction.py -v

# Test embeddings
pytest tests/test_embedder.py -v

# Test vector store
pytest tests/test_vector_store.py -v

# Test LLM functions (mocked)
pytest tests/test_llm_summary.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

This will:
- Run all tests
- Generate coverage report in terminal
- Create `htmlcov/index.html` with detailed coverage report

## 🚀 Testing the API

### 1. Start the Server

```bash
# Activate venv
source venv/bin/activate

# Set API key (required for LLM features)
export OPENAI_API_KEY="your-api-key-here"

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Test Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","vector_store_ready":true}
```

#### API Documentation
Open in browser: `http://localhost:8000/docs`

This provides an interactive Swagger UI where you can test all endpoints.

#### Upload a PDF (using curl)
```bash
curl -X POST "http://localhost:8000/upload_pdf" \
  -F "file=@path/to/your/paper.pdf" \
  -F "title=Optional Title"
```

#### Search for Papers
```bash
curl "http://localhost:8000/search?query=deep%20learning&top_k=3"
```

#### List All Papers
```bash
curl http://localhost:8000/papers
```

#### Get Specific Paper
```bash
curl http://localhost:8000/papers/{paper_id}
```

### 3. Test with Python Script

Create a test script `test_api.py`:

```python
import requests
import os

API_BASE = "http://localhost:8000"

# Test health
response = requests.get(f"{API_BASE}/health")
print("Health:", response.json())

# Test search (if you have papers uploaded)
response = requests.get(f"{API_BASE}/search", params={"query": "machine learning", "top_k": 3})
print("Search results:", response.json())
```

Run it:
```bash
python test_api.py
```

## 🎨 Testing the UI

### 1. Start the UI

In a new terminal:
```bash
# Activate venv
source venv/bin/activate

# Set API URL (if server is on different host/port)
export API_BASE_URL="http://localhost:8000"

# Start Streamlit
streamlit run ui/streamlit_app.py
```

The UI will open at `http://localhost:8501`

### 2. Test UI Features

1. **Upload Page**:
   - Upload a PDF paper
   - Verify summary and keywords are generated
   - Check that paper appears in database

2. **Search Page**:
   - Enter a search query
   - Verify similar papers are returned
   - Check that explanations are generated

3. **Browse Page**:
   - Verify all uploaded papers are listed
   - Check paper details are displayed

## 🔍 Manual Component Testing

### Test PDF Extraction
```python
from app.pdf_extraction import extract_text_from_pdf
from pathlib import Path

# Test with a PDF file
text = extract_text_from_pdf(Path("path/to/paper.pdf"))
print(f"Extracted {len(text)} characters")
print(text[:500])  # First 500 chars
```

### Test Embeddings
```python
from app.embedder import Embedder

embedder = Embedder()
text = "This is a test sentence about machine learning."
embedding = embedder.embed(text)
print(f"Embedding shape: {embedding.shape}")
print(f"Embedding norm: {embedding.norm():.4f}")  # Should be ~1.0 if normalized
```

### Test Vector Store
```python
from app.embedder import Embedder
from app.vector_store import VectorStore
import numpy as np

# Initialize
embedder = Embedder()
vector_store = VectorStore(embedder)

# Add a test paper
doc_text = "Title: Test Paper\n\nSummary: This is a test\n\nKeywords: test, paper\n\nContent: Test content"
embedding = embedder.embed(doc_text)
paper_id = vector_store.add_paper(
    title="Test Paper",
    summary="This is a test",
    keywords=["test", "paper"],
    content_snippet="Test content",
    full_text="Full test text",
    embedding=embedding,
)
print(f"Added paper with ID: {paper_id}")

# Search
query = "test paper"
query_embedding = embedder.embed(query)
results = vector_store.search(query_embedding, top_k=1)
print(f"Search results: {results}")
```

## 🐛 Troubleshooting Tests

### If tests fail with import errors:
```bash
# Make sure you're in the project root
cd /Users/hikaruibayashi/Projects/RAG

# Make sure venv is activated
source venv/bin/activate

# Reinstall in development mode
pip install -e .
```

### If vector store tests fail:
- Make sure Chroma can create the database directory
- Check file permissions in `db/chroma/`

### If LLM tests fail:
- These use mocks, so they should work without API key
- If they fail, check that OpenAI client is properly mocked

## 📊 Expected Test Results

When all tests pass, you should see:
```
tests/test_embedder.py ................ [100%]
tests/test_llm_summary.py .............. [100%]
tests/test_pdf_extraction.py ........... [100%]
tests/test_vector_store.py ............. [100%]

========= X passed in Y seconds =========
```

## 🎯 Integration Testing

For a full integration test:

1. Start the server
2. Upload a test PDF via API
3. Search for it
4. Verify results make sense
5. Check UI displays correctly

Example integration test script:

```python
import requests
import time

API_BASE = "http://localhost:8000"

# 1. Health check
print("1. Health check...")
r = requests.get(f"{API_BASE}/health")
assert r.status_code == 200
print("✓ Server is healthy")

# 2. Upload (if you have a test PDF)
# print("2. Uploading PDF...")
# with open("test_paper.pdf", "rb") as f:
#     r = requests.post(f"{API_BASE}/upload_pdf", files={"file": f})
#     assert r.status_code == 200
#     paper_id = r.json()["paper_id"]
#     print(f"✓ Uploaded paper: {paper_id}")

# 3. Search
print("3. Testing search...")
r = requests.get(f"{API_BASE}/search", params={"query": "machine learning", "top_k": 1})
assert r.status_code == 200
print("✓ Search works")

print("\n✅ All integration tests passed!")
```

