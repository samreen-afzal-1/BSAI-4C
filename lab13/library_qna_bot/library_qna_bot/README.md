# 📚 Athena — Library QnA Bot
### Lab 10 · NLP QnA Pipeline

A full-stack Library Chatbot using a classic NLP retrieval pipeline:

```
Dataset → Preprocess → TF-IDF Embed (MiniLM-style) → FAISS Index → Flask API → HTML UI
```

---

## Project Structure

```
library_qna_bot/
├── library_data.py        # 46 curated library QnA pairs (10 topic groups)
├── nlp_pipeline.py        # Preprocessing, TFIDFEmbedder, FAISSIndex, QnAPipeline
├── app.py                 # Flask app — routes: / and POST /ask
├── run.py                 # Launcher script
├── requirements.txt
├── templates/
│   └── index.html         # Jinja2 template (uses static files)
└── static/
    ├── css/style.css      # Dark gold/teal theme
    └── js/app.js          # Fetch /ask, render results, history
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the server
```bash
python run.py
```

### 3. Open in browser
```
http://localhost:5050
```

---

## NLP Pipeline (nlp_pipeline.py)

### Stage 1 — Preprocessing
```python
preprocess("What are the library opening hours?")
# → ['librari', 'open', 'hour']
```
- Lowercase + regex strip punctuation
- Tokenise on whitespace
- Remove 60+ English stopwords
- Lightweight Porter-style suffix stemming

### Stage 2 — Embedding (TFIDFEmbedder)
Mirrors the `sentence-transformers` MiniLM interface:
- Builds a vocabulary from the question corpus
- Computes TF-IDF weights with sublinear TF and smooth IDF
- **L2-normalises** every vector → cosine similarity = dot product

### Stage 3 — FAISS Index (FAISSIndex)
Mirrors the `faiss.IndexFlatL2` API:
- `add(vectors)` — stores pre-normalised embedding matrix
- `search(query_vec, k)` — returns top-k via dot-product (≡ cosine)

### Stage 4 — Search
- Encode the user query through the same embedder
- Call `index.search(q_vec, k=3)`
- Filter by threshold (0.08), scale to 0–100% confidence
- Return ranked JSON results

---

## API

### `GET /`
Returns the HTML chat UI.

### `POST /ask`
**Request:**
```json
{ "query": "How do I renew my books?" }
```
**Response:**
```json
{
  "query": "How do I renew my books?",
  "results": [
    {
      "rank": 1,
      "question": "How do I renew my books?",
      "answer": "Renew books via the library website...",
      "similarity": 0.871,
      "confidence": 100
    }
  ]
}
```

### `GET /stats`
Returns pipeline statistics (vocab size, vector count, etc.).

---

## Dataset Topics (library_data.py)

| # | Topic | QnA Pairs |
|---|-------|-----------|
| 1 | Hours & Location | 6 |
| 2 | Membership & Cards | 6 |
| 3 | Borrowing & Returns | 8 |
| 4 | Reservations & Holds | 4 |
| 5 | Digital Resources & E-Books | 4 |
| 6 | Computers & Wi-Fi | 3 |
| 7 | Study Rooms & Events | 5 |
| 8 | Research & Reference | 3 |
| 9 | Fines & Fees | 2 |
| 10 | General | 5 |
| **Total** | | **46** |

---

## Upgrading to Real MiniLM + FAISS

To use the actual HuggingFace `all-MiniLM-L6-v2` model and FAISS:

```bash
pip install sentence-transformers faiss-cpu
```

Then replace the embedding step in `nlp_pipeline.py`:

```python
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
vectors = model.encode([qa["question"] for qa in self.qa_pairs],
                        normalize_embeddings=True)

index = faiss.IndexFlatIP(vectors.shape[1])   # Inner product = cosine on normalised vecs
index.add(vectors.astype("float32"))
```

The rest of the pipeline (Flask routes, HTML UI, similarity scoring) stays identical.
