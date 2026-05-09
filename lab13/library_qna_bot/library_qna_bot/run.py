#!/usr/bin/env python3
"""
run.py  —  Launcher for Athena Library QnA Bot
Usage:  python run.py
Then open:  http://localhost:5050
"""
import sys, os

# Make sure we run from the project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, pipeline
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Install dependencies with:  pip install -r requirements.txt")
    sys.exit(1)

if __name__ == "__main__":
    print("=" * 55)
    print("  📚  Athena — Library QnA Bot  (Lab 10)")
    print("=" * 55)
    stats = pipeline.stats()
    print(f"  ✓  Loaded  {stats['total_qa_pairs']} QnA pairs")
    print(f"  ✓  Vocab   {stats['vocab_size']} tokens")
    print(f"  ✓  Indexed {stats['indexed_vectors']} FAISS vectors")
    print(f"  ✓  Dim     {stats['embedding_dim']}")
    print("=" * 55)
    print("  🌐  http://localhost:5050")
    print("  Press Ctrl+C to stop")
    print("=" * 55)
    app.run(host="0.0.0.0", port=5050, debug=False)
