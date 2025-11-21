# Pocket ML Paper RAG

A personal LLM-powered research paper recommendation engine that helps you discover similar papers from your personal collection.

## 🚀 Features

- **PDF Upload & Processing**: Upload research papers in PDF format
- **Automatic Summarization**: LLM-generated summaries of papers
- **Keyword Extraction**: Automatic extraction of key terms and concepts
- **Vector Search**: Semantic search using sentence-transformers embeddings
- **AI Explanations**: LLM-generated explanations of why papers are relevant
- **Web Interface**: Clean Streamlit UI for easy interaction

## 📋 Requirements

- **Python**: 3.10, 3.11, or 3.12
- **OpenAI API key**: Required for LLM summarization and explanations ([Get one here](https://platform.openai.com/api-keys))
- **Disk space**: ~500MB for embedding models and dependencies
- **Internet connection**: Required for initial setup (downloading models and packages)

## 🛠️ Installation

### Step-by-Step Installation

1. **Clone the repository:**

On GitHub, navigate to the repository page and click the green "Code" button to get the clone URL, then run:

```bash
git clone https://github.com/ibayashi-hikaru/pocket-ml-paper-rag.git
cd pocket-ml-paper-rag
```

**Note:** Replace `ibayashi-hikaru` with the actual GitHub username or organization name where the repository is hosted. You can also use SSH if you have SSH keys set up:

```bash
git clone git@github.com:ibayashi-hikaru/pocket-ml-paper-rag.git
cd pocket-ml-paper-rag
```

2. **Check your Python version:**
```bash
python --version
```

3. **Create a virtual environment (highly recommended):**
```bash
python -m venv venv
```

4. **Activate the virtual environment:**
```bash
# On macOS/Linux:
source venv/bin/activate
```

After activation, you should see `(venv)` in your terminal prompt.

5. **Upgrade pip (recommended):**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
This may take a few minutes as it downloads and installs PyTorch and other dependencies.

6. **Set up your OpenAI API key:**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 🚀 Quick Start

After installation, follow these steps to run the application:

### 1. Start the Backend API

Open a terminal and make sure your virtual environment is activated (you should see `(venv)` in your prompt). Then run:

```bash
# Using uvicorn directly (recommended)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Alternative: Run as a Python module
python -m app.main
```

The API server will start and be available at `http://localhost:8000`

- API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

Keep this terminal window open while using the application.

### 2. Start the Streamlit UI

Open a **new terminal window** (keep the API server running in the first terminal). Navigate to the project directory, activate the virtual environment, and run:

```bash
# Navigate to project directory
cd /path/to/pocket-ml-paper-rag

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start Streamlit UI
streamlit run ui/streamlit_app.py
```

The Streamlit UI will automatically open in your default web browser at `http://localhost:8501`

If it doesn't open automatically, navigate to `http://localhost:8501` manually.

### First Steps

1. **Upload a PDF**: Use the Streamlit UI to upload your first research paper
2. **Search**: Enter a query to find similar papers in your collection
3. **Explore**: Browse uploaded papers and view summaries and keywords

## 📖 Detailed Usage

### Using the Streamlit UI

The Streamlit UI provides an easy-to-use interface for:
- Uploading PDF papers
- Searching your paper collection
- Viewing paper summaries and keywords
- Getting AI-generated explanations for paper recommendations

Simply follow the on-screen instructions in the web interface.

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
pocket-ml-paper-rag/
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

## ❗ Troubleshooting

### Python Version Issues

If you get errors about Python version compatibility:

```bash
# Check your Python version
python3 --version

# If you're using Python 3.13, install Python 3.11 or 3.12
# On macOS using Homebrew:
brew install python@3.11

# On Ubuntu/Debian:
sudo apt-get install python3.11 python3.11-venv
```

### PyTorch Installation Errors

If you encounter PyTorch installation errors, see the `INSTALL.md` file for detailed instructions.

### Import Errors

If you get import errors after installation:

1. Make sure your virtual environment is activated (`(venv)` should appear in your terminal)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Verify installation: `pip list | grep torch`

### API Key Not Working

1. Check that your `.env` file is in the project root directory
2. Verify the file contains: `OPENAI_API_KEY=your-key-here` (no quotes in the file)
3. Restart both the API server and Streamlit UI after adding/changing the API key

### Port Already in Use

If port 8000 or 8501 is already in use:

```bash
# For API server (change port to 8001):
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# For Streamlit (change port to 8502):
streamlit run ui/streamlit_app.py --server.port 8502
```

### Connection Refused Errors

- Make sure the API server is running before starting the Streamlit UI
- Check that both services are running in separate terminals
- Verify the API is accessible at `http://localhost:8000/docs`

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

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [sentence-transformers](https://www.sbert.net/) for embeddings
- [Chroma](https://www.trychroma.com/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Streamlit](https://streamlit.io/) for the UI

