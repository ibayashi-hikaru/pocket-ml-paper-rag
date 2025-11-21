#!/bin/bash
# Setup script for Pocket ML Paper RAG

echo "🔧 Setting up Pocket ML Paper RAG..."

# Check Python version
PYTHON_CMD=""
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✓ Found Python 3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✓ Found Python 3.11"
else
    echo "❌ Error: Python 3.11 or 3.12 is required (PyTorch doesn't support Python 3.13 yet)"
    echo "Please install Python 3.11 or 3.12:"
    echo "  brew install python@3.12"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "2. Start the server:"
echo "   ./run_server.sh"
echo ""
echo "3. In another terminal, start the UI:"
echo "   ./run_ui.sh"

