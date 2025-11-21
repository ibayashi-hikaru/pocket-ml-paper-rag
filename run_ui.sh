#!/bin/bash
# Startup script for Streamlit UI

echo "Starting ML Paper Recommender UI..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run run_server.sh first or create venv manually."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start Streamlit with headless mode to skip welcome screen
echo "Starting Streamlit UI on http://localhost:8501"
echo "Note: If prompted for email, just press Enter to skip"
streamlit run ui/streamlit_app.py --server.headless=true

