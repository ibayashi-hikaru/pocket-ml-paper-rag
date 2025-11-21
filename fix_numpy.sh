#!/bin/bash
# Fix NumPy version issue

echo "Fixing NumPy compatibility issue..."

cd /Users/hikaruibayashi/Projects/RAG

# Check which Python versions are available
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "Using Python 3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "Using Python 3.11"
else
    echo "Error: Python 3.11 or 3.12 required"
    exit 1
fi

# Remove old venv
echo "Removing old virtual environment..."
rm -rf venv

# Create new venv
echo "Creating new virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activate and upgrade pip
echo "Upgrading pip..."
source venv/bin/activate
pip install --upgrade pip

# Install NumPy 1.x first (before other packages that might pull in NumPy 2.x)
echo "Installing NumPy 1.26.4..."
pip install "numpy==1.26.4"

# Now install other requirements
echo "Installing other requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Done! NumPy should now be version 1.26.4"
echo "Verify with: ./venv/bin/python -c 'import numpy; print(numpy.__version__)'"

