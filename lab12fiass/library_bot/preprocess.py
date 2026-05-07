"""
preprocess.py  –  Library Assistant Bot
Reads library_data.csv, builds QnA pairs, embeds with MiniLM, stores in FAISS.
Run this ONCE before starting the Flask app.
"""

import pandas as pd
import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

DATA_PATH   = "library_data.csv"
INDEX_PATH  = "faiss_index.index"
META_PATH   = "qna_meta.pkl"

# ─── 1. Load dataset ────────────────────────────────────────────────────────
print("📚 Loading dataset …")
df = pd.read_csv(DATA_PATH)
df.fillna("N/A", inplace=True)

# ─── 2. Build QnA pairs from structured data ────────────────────────────────
print("🔨 Building QnA pairs …")
qna_pairs = []

# Fixed / global FAQs
faq = [
    {
        "question": "What are the library opening hours?",
        "answer":   "The library is open Monday–Friday 8 AM – 8 PM, Saturday 9 AM – 5 PM, and closed on Sundays."
    },
    {
        "question": "What time does the library close?",
        "answer":   "The library closes at 8 PM on weekdays and 5 PM on Saturdays."
    },
    {
        "question": "When does the library open?",
        "answer":   "The library opens at 8 AM on weekdays and 9 AM on Saturdays."
    },
    {
        "question": "How many days can I borrow a book?",
        "answer":   "Books can be borrowed for up to 14 days. Renewals are allowed once for another 7 days."
    },
    {
        "question": "What is the fine for late return?",
        "answer":   "A fine of PKR 5 per day is charged for overdue books."
    },
    {
        "question": "How do I renew a book?",
        "answer":   "You can renew a book at the front desk or by contacting the library helpdesk. Renewal is allowed once per book."
    },
    {
        "question": "How many books can I borrow at once?",
        "answer":   "Students may borrow up to 3 books at a time. Faculty members may borrow up to 5."
    },
    {
        "question": "Is there a study room?",
        "answer":   "Yes, the library has 4 study rooms available. They can be booked at the front desk for up to 2 hours."
    },
    {
        "question": "Does the library have Wi-Fi?",
        "answer":   "Yes, free Wi-Fi is available throughout the library. Ask at the front desk for the password."
    },
    {
        "question": "How do I find a book?",
        "answer":   "You can search for any book using this Library Assistant. Just type the book title, author, or category."
    },
]
qna_pairs.extend(faq)

# Per-book QnA generated from dataset
for _, row in df.iterrows():
    title    = row["Title"]
    author   = row["Author"]
    category = row["Category"]
    status   = row["Status"]
    cabinet  = row["Cabinet"]
    rack     = row["Rack"]
    row_num  = row["Row"]
    book_id  = row["Book_ID"]
    ts       = row["Timestamp"]

    location_str = f"Cabinet {cabinet}, Rack {rack}, Row {row_num}"
    status_str   = (
        "available on the shelf"    if status == "Present"     else
        "currently checked out"                                 if status == "Checked Out" else
        "marked as missing — please ask staff for help"
    )

    # Q1: availability
    qna_pairs.append({
        "question": f"Is '{title}' available?",
        "answer":   f"'{title}' by {author} is {status_str}. Location: {location_str}."
    })
    # Q2: location
    qna_pairs.append({
        "question": f"Where can I find '{title}'?",
        "answer":   f"'{title}' (ID: {book_id}) is located at {location_str}. Current status: {status}."
    })
    # Q3: author lookup
    qna_pairs.append({
        "question": f"Who wrote '{title}'?",
        "answer":   f"'{title}' was written by {author}. It belongs to the {category} category."
    })
    # Q4: category lookup
    qna_pairs.append({
        "question": f"What category is '{title}'?",
        "answer":   f"'{title}' by {author} is in the {category} section."
    })
    # Q5: due date / timestamp
    qna_pairs.append({
        "question": f"When was '{title}' last updated in the system?",
        "answer":   f"The last system update for '{title}' was at {ts}. Status: {status}."
    })

# Category-level questions
for cat in df["Category"].unique():
    books_in_cat = df[df["Category"] == cat]
    available    = books_in_cat[books_in_cat["Status"] == "Present"]["Title"].tolist()
    qna_pairs.append({
        "question": f"What {cat} books are available?",
        "answer":   (
            f"Available {cat} books: {', '.join(available[:8])}{'…' if len(available) > 8 else ''}."
            if available else
            f"Sorry, no {cat} books are currently on the shelf."
        )
    })
    qna_pairs.append({
        "question": f"Show me books in the {cat} section.",
        "answer":   (
            f"Available {cat} books right now: {', '.join(available[:8])}."
            if available else
            f"All {cat} books are currently checked out or missing."
        )
    })

print(f"   ✅ {len(qna_pairs)} QnA pairs built ({len(faq)} FAQ + {len(qna_pairs)-len(faq)} book-derived)")

# ─── 3. Embed questions with MiniLM ─────────────────────────────────────────
print("🤖 Loading MiniLM model …")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

questions  = [pair["question"] for pair in qna_pairs]
print(f"📐 Encoding {len(questions)} questions …")
embeddings = model.encode(questions, show_progress_bar=True)
embeddings = np.array(embeddings, dtype="float32")

# ─── 4. Build FAISS index ───────────────────────────────────────────────────
print("🗄️  Building FAISS index …")
dim         = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dim)
faiss_index.add(embeddings)
faiss.write_index(faiss_index, INDEX_PATH)

# ─── 5. Save metadata ───────────────────────────────────────────────────────
with open(META_PATH, "wb") as f:
    pickle.dump(qna_pairs, f)

print(f"\n✅ Done!  FAISS index → {INDEX_PATH}   Metadata → {META_PATH}")
print(f"   Index contains {faiss_index.ntotal} vectors of dimension {dim}.")
