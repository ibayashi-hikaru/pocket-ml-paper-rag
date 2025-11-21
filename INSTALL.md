# Installation Guide

## Standard Installation

```bash
pip install -r requirements.txt
```

## Platform-Specific Issues

### If you encounter torch installation errors:

#### For Apple Silicon (M1/M2/M3 Macs):

```bash
# Install torch separately first
pip install torch torchvision torchaudio

# Then install other requirements
pip install -r requirements.txt
```

#### For Linux/Windows:

If torch installation fails, try installing from PyTorch's official index:

```bash
# For CPU-only (lighter)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
pip install -r requirements.txt
```

#### Alternative: Let sentence-transformers handle it

If you're still having issues, you can install sentence-transformers first (it will pull in torch):

```bash
pip install sentence-transformers
pip install -r requirements.txt --no-deps
pip install -r requirements.txt  # This will install remaining deps
```

### Minimal Installation (if you want to skip torch for now)

If you just want to test the API without embeddings, you can comment out sentence-transformers temporarily:

```bash
# Edit requirements.txt and comment out:
# sentence-transformers>=2.2.2

pip install -r requirements.txt
```

Note: The embedding functionality won't work without sentence-transformers.

## Verify Installation

After installation, verify everything works:

```python
python -c "import torch; print(f'PyTorch {torch.__version__}')"
python -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers OK')"
```

