# 📚 City Library Assistant Bot

A Flask-powered chatbot web application for library self-service.

## Features

| Feature | Example Query |
|---|---|
| Opening Hours | "What are your hours?" / "Are you open Sunday?" |
| Book Search | "Find books by Tolkien" / "Search for Sci-Fi" |
| Availability Check | "Is 1984 available?" |
| Due Dates & Renewals | "How do I renew a book?" / "When is my book due?" |
| Late Fines & Fees | "What are the late fees?" |
| Membership Plans | "What plans do you offer?" |
| Events & Programs | "What events are coming up?" |
| Library Services | "What services do you offer?" |
| Wi-Fi Info | "What's the WiFi password?" |
| Book Reservations | "How do I place a hold on a book?" |
| Book Recommendations | "Recommend a popular book" |
| Contact Information | "How do I contact the library?" |

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Open in browser
# http://localhost:5000
```

## Project Structure

```
library-bot/
├── app.py              # Flask backend (routes + intent engine)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Full frontend (HTML/CSS/JS)
└── README.md
```

## Extending the Bot

- **Add books:** Edit `BOOK_CATALOG` list in `app.py`
- **Add events:** Edit `EVENTS` list in `app.py`
- **Add intents:** Add patterns to `detect_intent()` and handle in `get_response()`
- **Connect a real DB:** Replace list lookups with SQLAlchemy queries
