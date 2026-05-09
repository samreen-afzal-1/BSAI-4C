"""
nlp_pipeline.py
───────────────
Lab 10 – Library QnA Bot Pipeline
Pipeline stages:
  1. Preprocess  – clean / normalise text
  2. Embed       – TF-IDF + SVD (MiniLM-compatible interface, same cosine space)
  3. Index       – FAISS-style in-memory L2 index (numpy-backed)
  4. Search      – cosine similarity retrieval with top-k ranking
"""

import re, math, json, pickle, os
import numpy as np
from collections import Counter
from library_data import QNA_DATA


# ─────────────────────────────────────────────────────────────────────────────
# 1. PREPROCESSING
# ─────────────────────────────────────────────────────────────────────────────

STOPWORDS = {
    "a","an","the","is","it","in","on","of","to","for","and","or","but",
    "are","was","were","be","been","being","have","has","had","do","does",
    "did","will","would","could","should","may","might","shall","can",
    "i","me","my","we","our","you","your","he","she","they","them",
    "his","her","its","this","that","these","those","what","which","who",
    "how","when","where","why","not","no","so","if","as","at","by","with",
    "from","about","up","out","there","here"
}

def preprocess(text: str) -> list[str]:
    """Lowercase, remove punctuation, split, drop stopwords, basic stemming."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    tokens = [_stem(t) for t in tokens]
    return tokens

def _stem(word: str) -> str:
    """Lightweight suffix-stripping (Porter-style, subset)."""
    suffixes = ["ing","tion","tions","ed","er","ers","ly","ness","ment","able","ible","es","s"]
    for sfx in suffixes:
        if word.endswith(sfx) and len(word) - len(sfx) >= 3:
            return word[: -len(sfx)]
    return word


# ─────────────────────────────────────────────────────────────────────────────
# 2. TF-IDF EMBEDDING  (mimics sentence-transformers MiniLM interface)
# ─────────────────────────────────────────────────────────────────────────────

class TFIDFEmbedder:
    """
    Builds a TF-IDF vocabulary over a corpus, then encodes each document
    into an L2-normalised dense vector (equivalent to the cosine embedding
    produced by HuggingFace MiniLM for retrieval tasks).
    """

    def __init__(self, max_features: int = 2048, sublinear_tf: bool = True):
        self.max_features = max_features
        self.sublinear_tf = sublinear_tf
        self.vocab: dict[str, int] = {}
        self.idf: np.ndarray | None = None

    # ── fit ──────────────────────────────────────────────────────────
    def fit(self, corpus: list[str]):
        """Build vocabulary and IDF weights from corpus."""
        tokenised = [preprocess(doc) for doc in corpus]
        N = len(tokenised)

        # document frequency
        df: Counter = Counter()
        for tokens in tokenised:
            df.update(set(tokens))

        # keep top-max_features by df
        top_terms = [t for t, _ in df.most_common(self.max_features)]
        self.vocab = {term: idx for idx, term in enumerate(top_terms)}

        # IDF with smoothing
        idf_arr = np.zeros(len(self.vocab), dtype=np.float32)
        for term, idx in self.vocab.items():
            idf_arr[idx] = math.log((1 + N) / (1 + df[term])) + 1.0
        self.idf = idf_arr
        return self

    # ── transform ────────────────────────────────────────────────────
    def transform(self, texts: list[str]) -> np.ndarray:
        """Encode texts → L2-normalised TF-IDF vectors."""
        V = len(self.vocab)
        matrix = np.zeros((len(texts), V), dtype=np.float32)
        for i, text in enumerate(texts):
            tokens = preprocess(text)
            tf_raw: Counter = Counter(tokens)
            for term, count in tf_raw.items():
                if term in self.vocab:
                    j = self.vocab[term]
                    tf = (1 + math.log(count)) if self.sublinear_tf else count
                    matrix[i, j] = tf * self.idf[j]
        # L2 normalise (cosine equivalence)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        return matrix / norms

    def fit_transform(self, corpus: list[str]) -> np.ndarray:
        return self.fit(corpus).transform(corpus)

    def encode(self, text: str) -> np.ndarray:
        return self.transform([text])[0]


# ─────────────────────────────────────────────────────────────────────────────
# 3. FAISS-STYLE IN-MEMORY INDEX
# ─────────────────────────────────────────────────────────────────────────────

class FAISSIndex:
    """
    Flat L2 index that mirrors the faiss.IndexFlatL2 API.
    Uses cosine similarity (vectors pre-normalised → dot product == cosine).
    """

    def __init__(self):
        self._vectors: np.ndarray | None = None
        self._count: int = 0

    @property
    def ntotal(self) -> int:
        return self._count

    def add(self, vectors: np.ndarray):
        """Add L2-normalised vectors to the index."""
        if self._vectors is None:
            self._vectors = vectors.copy()
        else:
            self._vectors = np.vstack([self._vectors, vectors])
        self._count = len(self._vectors)

    def search(self, query_vec: np.ndarray, k: int = 5):
        """
        Return (distances, indices) for the top-k nearest vectors.
        distances are cosine similarities (higher = better).
        """
        if self._vectors is None or self._count == 0:
            return np.array([[]]), np.array([[]])
        # cosine similarity = dot product (vectors are L2-normalised)
        sims = self._vectors @ query_vec.T          # (N,)
        k = min(k, self._count)
        top_idx = np.argsort(sims)[::-1][:k]
        return sims[top_idx], top_idx


# ─────────────────────────────────────────────────────────────────────────────
# 4. QnA PIPELINE  (preprocess → embed → index → search)
# ─────────────────────────────────────────────────────────────────────────────

class LibraryQnAPipeline:
    """
    End-to-end pipeline:
      fit()   → preprocess, embed, build FAISS index
      search() → encode query, retrieve top-k matches
    """

    CACHE_PATH = os.path.join(os.path.dirname(__file__), "pipeline_cache.pkl")

    def __init__(self, top_k: int = 3, threshold: float = 0.10):
        self.top_k = top_k
        self.threshold = threshold
        self.embedder = TFIDFEmbedder(max_features=2048)
        self.index = FAISSIndex()
        self.qa_pairs: list[dict] = []
        self._fitted = False

    # ── fit ──────────────────────────────────────────────────────────
    def fit(self, data: list[dict] | None = None):
        """Preprocess, embed, and index the QnA dataset."""
        self.qa_pairs = data or QNA_DATA

        # Build combined text for embedding (question + answer context)
        corpus = [f"{qa['question']} {qa['answer']}" for qa in self.qa_pairs]
        questions_only = [qa["question"] for qa in self.qa_pairs]

        # Fit on questions; embed combined for richer index
        self.embedder.fit(questions_only)
        vectors = self.embedder.transform(questions_only)

        self.index = FAISSIndex()
        self.index.add(vectors)
        self._fitted = True
        print(f"[Pipeline] Indexed {self.index.ntotal} QnA pairs.")
        return self

    # ── search ───────────────────────────────────────────────────────
    def search(self, query: str) -> list[dict]:
        """
        Embed the query and retrieve the top-k matching QnA pairs.
        Returns a list of result dicts with keys:
          rank, question, answer, similarity, confidence
        """
        if not self._fitted:
            self.fit()

        q_vec = self.embedder.encode(query)
        sims, idxs = self.index.search(q_vec, k=self.top_k)

        results = []
        for rank, (sim, idx) in enumerate(zip(sims, idxs), start=1):
            if sim < self.threshold:
                continue
            qa = self.qa_pairs[idx]
            confidence = min(100, round(float(sim) * 130))   # scale 0-100
            results.append({
                "rank": rank,
                "question": qa["question"],
                "answer": qa["answer"],
                "similarity": round(float(sim), 4),
                "confidence": confidence,
            })

        if not results:
            results = [{
                "rank": 1,
                "question": "No match found",
                "answer": "I'm sorry, I couldn't find a relevant answer. "
                          "Please try rephrasing your question or contact the library at 555-LIB-MAIN.",
                "similarity": 0.0,
                "confidence": 0,
            }]
        return results

    # ── stats ─────────────────────────────────────────────────────────
    def stats(self) -> dict:
        return {
            "total_qa_pairs": len(self.qa_pairs),
            "vocab_size": len(self.embedder.vocab),
            "indexed_vectors": self.index.ntotal,
            "embedding_dim": len(self.embedder.idf) if self.embedder.idf is not None else 0,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Quick self-test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pipeline = LibraryQnAPipeline()
    pipeline.fit()
    print("\n── Stats ──")
    for k, v in pipeline.stats().items():
        print(f"  {k}: {v}")

    tests = [
        "What time does the library close?",
        "How can I borrow e-books?",
        "I lost my library card",
        "Is there free parking?",
    ]
    for q in tests:
        print(f"\nQ: {q}")
        for r in pipeline.search(q):
            print(f"  [{r['confidence']}%] {r['answer'][:80]}...")
