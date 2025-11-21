# Implementation Plan

## ✅ Completed (MVP)

### Core Backend Components
- [x] **PDF Extraction** (`app/pdf_extraction.py`)
  - Uses pdfminer.six for robust text extraction
  - Text cleaning and normalization
  - Title extraction helper

- [x] **LLM Processing** (`app/llm_summary.py`)
  - Text summarization (3-6 sentences)
  - Keyword extraction (5-15 keywords)
  - OpenAI API integration

- [x] **Embedding Generation** (`app/embedder.py`)
  - sentence-transformers integration
  - Model: all-MiniLM-L6-v2 (384-dim)
  - Normalized embeddings (L2 norm)
  - Batch processing support

- [x] **Vector Store** (`app/vector_store.py`)
  - Chroma integration
  - Persistent storage
  - Cosine similarity search
  - Metadata storage

- [x] **Query Engine** (`app/query_engine.py`)
  - Query embedding
  - Similarity search
  - LLM-generated explanations

- [x] **FastAPI Backend** (`app/main.py`)
  - POST `/upload_pdf` - Upload and process papers
  - GET `/search` - Search for similar papers
  - GET `/papers/{id}` - Get specific paper
  - GET `/papers` - List all papers
  - Health check endpoint

- [x] **Streamlit UI** (`ui/streamlit_app.py`)
  - Upload page
  - Search page
  - Browse papers page

- [x] **Testing**
  - Unit tests for PDF extraction
  - Unit tests for embeddings
  - Unit tests for vector store
  - Mock tests for LLM functions

## 🚀 Next Steps (Post-MVP Enhancements)

### 1. Performance Optimizations
- [ ] Use async OpenAI client for better concurrency
- [ ] Add caching for embeddings
- [ ] Implement batch processing for multiple uploads
- [ ] Add connection pooling for database

### 2. Enhanced Features
- [ ] **Paper Clustering**
  - Use UMAP/t-SNE for visualization
  - Cluster papers by topic
  - Interactive visualization in UI

- [ ] **Similarity Graph**
  - Build cross-paper similarity network
  - Visualize with networkx/plotly
  - Find paper communities

- [ ] **Reading Recommendations**
  - Track reading history
  - Recommend unread papers based on:
    - Similarity to read papers
    - Popularity in your collection
    - Diversity (explore new topics)

- [ ] **Advanced Filtering**
  - Filter by year, author, venue
  - Filter by keywords
  - Filter by similarity threshold

- [ ] **Citation Analysis**
  - Extract citations from PDFs
  - Build citation network
  - Find highly cited papers in collection

### 3. UI Improvements
- [ ] Add paper preview modal
- [ ] Show similarity scores visually
- [ ] Add filters sidebar
- [ ] Export functionality (CSV, JSON)
- [ ] Dark mode support

### 4. Data Management
- [ ] Paper deletion with confirmation
- [ ] Bulk upload support
- [ ] Paper metadata editing
- [ ] Database backup/restore

### 5. Advanced Search
- [ ] Hybrid search (keyword + semantic)
- [ ] Query expansion
- [ ] Faceted search
- [ ] Search history

### 6. Multi-modal Support
- [ ] Extract and index figures
- [ ] Table extraction
- [ ] OCR for scanned PDFs

## 📊 Architecture Decisions

### Why Chroma over FAISS?
- **Chroma**: Easier to use, built-in metadata, persistent storage
- **FAISS**: More performant for very large datasets, but requires more setup

### Why sentence-transformers?
- Fast inference
- Good quality embeddings
- Easy to swap models
- No API costs

### Why FastAPI + Streamlit?
- **FastAPI**: Modern, fast, auto-docs, async support
- **Streamlit**: Rapid UI development, perfect for data apps

## 🔧 Configuration Options

### Embedding Models
- `all-MiniLM-L6-v2` (default, 384-dim, fast)
- `all-mpnet-base-v2` (768-dim, better quality)
- `sentence-transformers/all-MiniLM-L12-v2` (384-dim, better quality)

### Vector Database
- Current: Chroma (local, persistent)
- Alternative: FAISS (faster, but more setup)
- Future: Qdrant, Pinecone (cloud options)

### LLM Models
- Current: gpt-4o-mini (cost-effective)
- Alternative: gpt-4o (better quality)
- Future: Local models (Llama, Mistral) via Ollama

## 🧪 Testing Strategy

### Current Tests
- Unit tests for core functions
- Mock tests for LLM calls
- Integration tests for vector store

### Future Tests
- End-to-end API tests
- UI tests with Playwright
- Performance benchmarks
- Load testing

## 📈 Monitoring & Logging

### Future Additions
- Request logging
- Error tracking
- Performance metrics
- Usage analytics

