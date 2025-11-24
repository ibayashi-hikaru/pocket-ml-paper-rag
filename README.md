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
1. **Create a virtual environment (highly recommended):**
```bash
python -m venv venv
```

2. **Activate the virtual environment:**
```bash
source venv/bin/activate
```
After activation, you should see `(venv)` in your terminal prompt.

3. **Set up your OpenAI API key:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 🚀 Quick Start

After installation, follow these steps to run the application:

### 1. Start the Backend API

Open a terminal and make sure your virtual environment is activated (you should see `(venv)` in your prompt). Then run:

```bash
./run_server.sh
```
### 2. Start the Streamlit UI

Open a **new terminal window** (keep the API server running in the first terminal). Navigate to the project directory, activate the virtual environment, and run:

```bash
cd /path/to/pocket-ml-paper-rag
source venv/bin/activate
./run_ui.sh
```

The Streamlit UI will automatically open in your default web browser at `http://localhost:8501`

If it doesn't open automatically, navigate to `http://localhost:8501` manually.

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