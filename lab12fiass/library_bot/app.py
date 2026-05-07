"""
app.py  –  Library Assistant Bot (Flask backend)
Run:  python app.py
Then visit:  http://127.0.0.1:5000
"""

import os
import pickle
import numpy as np
import faiss
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

# ─── Config ──────────────────────────────────────────────────────────────────
INDEX_PATH  = "faiss_index.index"
META_PATH   = "qna_meta.pkl"
TOP_K       = 3           # return top-3 matches
THRESHOLD   = 1.5         # L2 distance — above this = "not confident"

app = Flask(__name__)

# ─── Load model + index once at startup ──────────────────────────────────────
print("Loading MiniLM model …")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Loading FAISS index …")
faiss_index = faiss.read_index(INDEX_PATH)

print("Loading QnA metadata …")
with open(META_PATH, "rb") as f:
    qna_pairs = pickle.load(f)

print(f"✅ Ready – {faiss_index.ntotal} entries indexed.")

# ─── Search helper ───────────────────────────────────────────────────────────
def search(query: str, top_k: int = TOP_K):
    q_emb = model.encode([query]).astype("float32")
    distances, indices = faiss_index.search(q_emb, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue
        results.append({
            "question":  qna_pairs[idx]["question"],
            "answer":    qna_pairs[idx]["answer"],
            "distance":  float(dist),
            "confident": dist < THRESHOLD,
        })
    return results

# ─── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data  = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    results = search(query)

    if not results or not results[0]["confident"]:
        fallback = (
            "I'm not sure about that. Please ask the librarian at the front desk, "
            "or try rephrasing your question (e.g. 'Is <book title> available?' or "
            "'What are the opening hours?')."
        )
        return jsonify({
            "query":   query,
            "answer":  fallback,
            "matches": results,
        })

    best = results[0]
    return jsonify({
        "query":   query,
        "answer":  best["answer"],
        "matches": results,
    })

if __name__ == "__main__":
    if not os.path.exists(INDEX_PATH):
        print("❌  FAISS index not found. Run:  python preprocess.py  first.")
    else:
        app.run(debug=True, port=5000)
