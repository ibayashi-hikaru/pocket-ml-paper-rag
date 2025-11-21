# ML Paper Recommender

A personal LLM-powered research paper recommendation engine that helps you discover similar papers from your personal collection.

## 🚀 Features

- **PDF Upload & Processing**: Upload research papers in PDF format
- **Automatic Summarization**: LLM-generated summaries of papers
- **Keyword Extraction**: Automatic extraction of key terms and concepts
- **Vector Search**: Semantic search using sentence-transformers embeddings
- **AI Explanations**: LLM-generated explanations of why papers are relevant
- **Web Interface**: Clean Streamlit UI for easy interaction

## 📋 Requirements

- Python 3.10, 3.11, or 3.12 (Python 3.13 not yet supported due to PyTorch compatibility)
- OpenAI API key (for summarization and explanations)
- ~500MB disk space (for embedding models)

## 🛠️ Installation

1. **Clone or navigate to the project directory:**
```bash
cd /Users/hikaruibayashi/Projects/RAG
```

2. **Create a virtual environment (recommended):**
```bash
# Use Python 3.11 or 3.12 (not 3.13 - PyTorch compatibility issue)
python3.11 -m venv venv  # or python3.12
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Note:** If you're on Python 3.13, you'll need to use Python 3.11 or 3.12. Check your Python version:
```bash
python3 --version
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set environment variables:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## 🚀 Usage

### Start the Backend API

```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Run the main file
python -m app.main
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Start the Streamlit UI

In a new terminal:

```bash
streamlit run ui/streamlit_app.py
```

The UI will open in your browser at `http://localhost:8501`

### Using the API Directly

#### Upload a Paper

```bash
curl -X POST "http://localhost:8000/upload_pdf" \
  -F "file=@paper.pdf" \
  -F "title=Optional Title"
```

#### Search for Papers

```bash
curl "http://localhost:8000/search?query=papers%20similar%20to%20SAM&top_k=5"
```

#### Get a Specific Paper

```bash
curl "http://localhost:8000/papers/{paper_id}"
```

#### List All Papers

```bash
curl "http://localhost:8000/papers"
```

## 📁 Project Structure

```
ml-paper-recommender/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── pdf_extraction.py    # PDF text extraction
│   ├── llm_summary.py       # LLM summarization & keywords
│   ├── embedder.py          # Sentence-transformers embeddings
│   ├── vector_store.py      # Chroma vector database
│   └── query_engine.py      # Search & explanation engine
├── ui/
│   └── streamlit_app.py     # Streamlit UI
├── uploads/                 # Uploaded PDFs (created automatically)
├── db/                      # Chroma database (created automatically)
├── requirements.txt
└── README.md
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=app --cov-report=html
```

## 🔧 Configuration

### Embedding Model

Default: `all-MiniLM-L6-v2` (384 dimensions)

To use a different model, modify `app/embedder.py`:

```python
embedder = Embedder(model_name="all-mpnet-base-v2")
```

### LLM Model

Default: `gpt-4o-mini`

To use a different model, set the `model` parameter in `app/llm_summary.py` and `app/query_engine.py`.

### Vector Database

Default: Chroma (persistent, local)

The database is stored in `db/chroma/` directory.

## 📊 How It Works

1. **Upload PDF**:
   - Extract text using pdfminer.six
   - Clean and normalize text

2. **LLM Processing**:
   - Generate 3-6 sentence summary
   - Extract 5-15 keywords

3. **Document Representation**:
   - Combine: Title + Summary + Keywords + Content Snippet
   - Create a single text representation

4. **Embedding**:
   - Generate 384-dim embedding using sentence-transformers
   - Normalize embeddings (L2 norm)

5. **Vector Storage**:
   - Store embedding + metadata in Chroma
   - Use cosine similarity for search

6. **Query**:
   - Embed user query
   - Retrieve top-k similar papers
   - Generate LLM explanations for relevance

## 🎯 Future Enhancements

- [ ] Paper clustering and visualization (UMAP/t-SNE)
- [ ] Cross-paper similarity graph
- [ ] "Unread paper recommendations" based on reading history
- [ ] Citation network analysis
- [ ] Multi-modal support (figures, tables)
- [ ] Advanced filtering (by year, author, venue)
- [ ] Export functionality (CSV, JSON)

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 🙏 Acknowledgments

- [sentence-transformers](https://www.sbert.net/) for embeddings
- [Chroma](https://www.trychroma.com/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Streamlit](https://streamlit.io/) for the UI

