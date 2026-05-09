"""
app.py  –  Library QnA Bot  (Lab 10)
Flask server wiring the NLP pipeline to a REST API + HTML UI
"""

from flask import Flask, request, jsonify, render_template
from nlp_pipeline import LibraryQnAPipeline

app = Flask(__name__)

# ── Boot pipeline ──────────────────────────────────────────────────────────
pipeline = LibraryQnAPipeline(top_k=3, threshold=0.08)
pipeline.fit()
STATS = pipeline.stats()

# ── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", stats=STATS)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    query = (data.get("query") or "").strip()
    if not query:
        return jsonify({"error": "Empty query"}), 400
    results = pipeline.search(query)
    return jsonify({"query": query, "results": results})


@app.route("/stats")
def stats():
    return jsonify(STATS)


@app.route("/topics")
def topics():
    """Return unique topic categories derived from the dataset."""
    from library_data import QNA_DATA
    import re
    # simple keyword grouping
    categories = {
        "Hours & Location": ["hour","open","close","location","park","get to"],
        "Membership & Cards": ["card","member","register","lost","child","valid"],
        "Borrowing & Returns": ["borrow","return","renew","late","lose","damage"],
        "Reservations": ["reserv","hold","wait"],
        "Digital Resources": ["ebook","digital","database","online","home","app"],
        "Computers & Wi-Fi": ["wifi","computer","print","scan"],
        "Study Rooms & Events": ["study","room","event","program","children","senior"],
        "Research & Reference": ["research","interlibrary","loan","histor","reference"],
        "Fines & Fees": ["fine","fee","pay","block"],
        "General": ["contact","donat","café","wheel","suggest"],
    }
    return jsonify(list(categories.keys()))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
