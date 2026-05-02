from flask import Flask, render_template, request, jsonify, session
import random
import re
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
app.secret_key = "library_bot_secret_2024"

# ─── Library Data ───────────────────────────────────────────────────────────

LIBRARY_INFO = {
    "hours": {
        "Monday":    "8:00 AM – 9:00 PM",
        "Tuesday":   "8:00 AM – 9:00 PM",
        "Wednesday": "8:00 AM – 9:00 PM",
        "Thursday":  "8:00 AM – 9:00 PM",
        "Friday":    "8:00 AM – 7:00 PM",
        "Saturday":  "10:00 AM – 6:00 PM",
        "Sunday":    "12:00 PM – 5:00 PM",
    },
    "contact": {
        "phone": "+1 (555) 234-5678",
        "email": "library@citylib.org",
        "address": "13km raiwind road, lake City, RC 10001",
    },
    "membership": {
        "basic":    {"fee": "Free", "books": 3,  "days": 14},
        "standard": {"fee": "$5/month", "books": 7,  "days": 21},
        "premium":  {"fee": "$10/month", "books": 15, "days": 30},
    },
    "fine": "$0.25 per day per book",
    "renewal_limit": 2,
    "wifi_password": "ReadMore2024",
}

BOOK_CATALOG = [
    {"id": "B001", "title": "The Great Gatsby",         "author": "F. Scott Fitzgerald", "genre": "Classic Fiction",  "available": True,  "copies": 3},
    {"id": "B002", "title": "To Kill a Mockingbird",    "author": "Harper Lee",           "genre": "Classic Fiction",  "available": True,  "copies": 2},
    {"id": "B003", "title": "1984",                     "author": "George Orwell",        "genre": "Dystopian",        "available": False, "copies": 0},
    {"id": "B004", "title": "Dune",                     "author": "Frank Herbert",        "genre": "Sci-Fi",           "available": True,  "copies": 4},
    {"id": "B005", "title": "The Hobbit",               "author": "J.R.R. Tolkien",       "genre": "Fantasy",          "available": True,  "copies": 2},
    {"id": "B006", "title": "Harry Potter & the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "Fantasy",      "available": True,  "copies": 5},
    {"id": "B007", "title": "The Alchemist",            "author": "Paulo Coelho",         "genre": "Fiction",          "available": False, "copies": 0},
    {"id": "B008", "title": "Sapiens",                  "author": "Yuval Noah Harari",    "genre": "Non-Fiction",      "available": True,  "copies": 3},
    {"id": "B009", "title": "Atomic Habits",            "author": "James Clear",          "genre": "Self-Help",        "available": True,  "copies": 6},
    {"id": "B010", "title": "Pride and Prejudice",      "author": "Jane Austen",          "genre": "Classic Fiction",  "available": True,  "copies": 4},
    {"id": "B011", "title": "The Midnight Library",     "author": "Matt Haig",            "genre": "Fiction",          "available": True,  "copies": 2},
    {"id": "B012", "title": "Project Hail Mary",        "author": "Andy Weir",            "genre": "Sci-Fi",           "available": False, "copies": 0},
    {"id": "B013", "title": "Educated",                 "author": "Tara Westover",        "genre": "Memoir",           "available": True,  "copies": 3},
    {"id": "B014", "title": "The Psychology of Money",  "author": "Morgan Housel",        "genre": "Finance",          "available": True,  "copies": 2},
    {"id": "B015", "title": "Where the Crawdads Sing",  "author": "Delia Owens",          "genre": "Mystery",          "available": True,  "copies": 4},
]

EVENTS = [
    {"name": "Children's Story Hour",   "day": "Every Saturday",  "time": "11:00 AM", "location": "Room A"},
    {"name": "Book Club Meeting",        "day": "First Tuesday",   "time": "6:30 PM",  "location": "Conference Room"},
    {"name": "Author Talk: Local Writers", "day": "Third Thursday","time": "7:00 PM",  "location": "Main Hall"},
    {"name": "Digital Literacy Workshop","day": "Every Wednesday", "time": "2:00 PM",  "location": "Computer Lab"},
    {"name": "Teen Reading Challenge",   "day": "Ongoing (July)",  "time": "All Day",  "location": "Teen Section"},
    {"name": "Resume Writing Help",      "day": "Every Friday",    "time": "10:00 AM", "location": "Room B"},
]

SERVICES = [
    "📚 Book borrowing & returns",
    "🖨️ Printing & photocopying ($0.10/page B&W, $0.25 color)",
    "💻 Computer & internet access (free, 2-hour sessions)",
    "📖 eBook & audiobook lending (via LibbyApp)",
    "🔬 Research assistance & reference desk",
    "🎧 Quiet study rooms (book online or walk-in)",
    "📦 Interlibrary loan (ILL) – get books from other branches",
    "👶 Children's section & educational toys",
    "🧑‍🎓 Tutoring referral network",
    "📰 Newspaper & magazine archive access",
]

# ─── Intent Detection ────────────────────────────────────────────────────────

def detect_intent(text):
    t = text.lower()
    if any(w in t for w in ["hour", "open", "close", "time", "when", "schedule", "today"]):
        return "hours"
    if any(w in t for w in ["book", "find", "search", "look", "available", "borrow", "genre", "author", "title"]):
        return "books"
    if any(w in t for w in ["due", "return", "deadline", "overdue", "extend", "renew"]):
        return "due_dates"
    if any(w in t for w in ["fine", "fee", "late", "penalty", "pay", "charge"]):
        return "fines"
    if any(w in t for w in ["member", "card", "join", "sign up", "register", "plan", "subscription"]):
        return "membership"
    if any(w in t for w in ["event", "program", "workshop", "activity", "class", "club", "story hour"]):
        return "events"
    if any(w in t for w in ["service", "offer", "provide", "print", "computer", "wifi", "internet", "ebook"]):
        return "services"
    if any(w in t for w in ["contact", "phone", "email", "address", "location", "where", "call"]):
        return "contact"
    if any(w in t for w in ["hello", "hi", "hey", "help", "start", "what can"]):
        return "greeting"
    if any(w in t for w in ["wifi", "password", "internet", "network"]):
        return "wifi"
    if any(w in t for w in ["reserve", "hold", "put on hold", "reservation"]):
        return "reservation"
    if any(w in t for w in ["recommend", "suggest", "popular", "best", "top"]):
        return "recommend"
    return "unknown"

# ─── Response Generator ──────────────────────────────────────────────────────

def get_response(user_message):
    intent = detect_intent(user_message)
    t = user_message.lower()

    if intent == "greeting":
        return (
            "👋 Welcome to <strong>City Library Assistant</strong>! I'm here to help you with:\n\n"
            "• 🕐 <strong>Opening hours</strong> – Ask \"What are your hours?\"\n"
            "• 📚 <strong>Finding books</strong> – Ask \"Find books by Tolkien\"\n"
            "• 📅 <strong>Due dates & renewals</strong> – Ask \"How do I renew a book?\"\n"
            "• 💳 <strong>Membership plans</strong> – Ask \"What membership plans do you have?\"\n"
            "• 🎉 <strong>Events & programs</strong> – Ask \"What events are coming up?\"\n"
            "• 🛠️ <strong>Library services</strong> – Ask \"What services do you offer?\"\n"
            "• 📞 <strong>Contact info</strong> – Ask \"How can I contact the library?\"\n\n"
            "What can I help you with today? 😊"
        )

    elif intent == "hours":
        today = datetime.now().strftime("%A")
        today_hours = LIBRARY_INFO["hours"].get(today, "Closed")
        rows = "".join(
            f"<tr{'class=\"today\"' if day == today else ''}><td>{day}</td><td>{h}</td></tr>"
            for day, h in LIBRARY_INFO["hours"].items()
        )
        return (
            f"🕐 <strong>Library Hours</strong>\n\n"
            f"<strong>Today ({today}):</strong> {today_hours}\n\n"
            f"<table class='info-table'><tr><th>Day</th><th>Hours</th></tr>{rows}</table>\n\n"
            f"📌 Holiday hours may vary. Call us to confirm on public holidays."
        )

    elif intent == "books":
        # Search by author, genre, or title
        search_terms = re.sub(r"(find|search|look for|books?|by|from|author|genre|title)", "", t).strip()
        if not search_terms or len(search_terms) < 2:
            genres = sorted(set(b["genre"] for b in BOOK_CATALOG))
            return (
                "📚 <strong>Book Search</strong>\n\n"
                "I can help you find books! Try asking:\n"
                "• \"Find books by J.K. Rowling\"\n"
                "• \"Search for Fantasy books\"\n"
                "• \"Is 1984 available?\"\n\n"
                f"<strong>Available Genres:</strong> {', '.join(genres)}\n\n"
                f"We have <strong>{len(BOOK_CATALOG)}</strong> titles in our catalog."
            )
        matches = [
            b for b in BOOK_CATALOG
            if search_terms in b["title"].lower()
            or search_terms in b["author"].lower()
            or search_terms in b["genre"].lower()
        ]
        if not matches:
            return (
                f"😕 No books found matching <strong>\"{user_message}\"</strong>.\n\n"
                "Try searching by author name, genre, or partial title.\n"
                "You can also request an <strong>Interlibrary Loan (ILL)</strong> if we don't have it!\n"
                "Ask: \"How do I request an interlibrary loan?\""
            )
        items = ""
        for b in matches[:6]:
            status = f"✅ Available ({b['copies']} copies)" if b["available"] else "❌ Checked Out"
            items += f"<div class='book-card'><strong>{b['title']}</strong> <span class='book-id'>#{b['id']}</span><br>by {b['author']} · <em>{b['genre']}</em><br>{status}</div>"
        return f"📚 Found <strong>{len(matches)}</strong> result(s):\n\n{items}"

    elif intent == "due_dates":
        due = (datetime.now() + timedelta(days=14)).strftime("%B %d, %Y")
        return (
            f"📅 <strong>Due Dates & Renewals</strong>\n\n"
            f"• <strong>Standard loan period:</strong> 14–30 days (depends on membership)\n"
            f"• <strong>If borrowed today</strong>, your due date would be: <strong>{due}</strong>\n\n"
            f"<strong>Renewals:</strong>\n"
            f"• You can renew up to <strong>{LIBRARY_INFO['renewal_limit']} times</strong>\n"
            f"• Renew online at <em>citylib.org/myaccount</em>, by phone, or in person\n"
            f"• Cannot renew if another patron has placed a hold on the book\n\n"
            f"<strong>Late Fines:</strong> {LIBRARY_INFO['fine']}"
        )

    elif intent == "fines":
        return (
            f"💰 <strong>Fines & Fees</strong>\n\n"
            f"• <strong>Late return fine:</strong> {LIBRARY_INFO['fine']}\n"
            f"• <strong>Lost book:</strong> Replacement cost + $5 processing fee\n"
            f"• <strong>Damaged book:</strong> Assessed on a case-by-case basis\n\n"
            f"<strong>Paying Fines:</strong>\n"
            f"• In person at the circulation desk (cash or card)\n"
            f"• Online at <em>citylib.org/pay</em>\n\n"
            f"📌 Accounts with fines over $10 cannot borrow until resolved."
        )

    elif intent == "membership":
        plans = LIBRARY_INFO["membership"]
        rows = "".join(
            f"<tr><td><strong>{p.title()}</strong></td><td>{v['fee']}</td><td>{v['books']} books</td><td>{v['days']} days</td></tr>"
            for p, v in plans.items()
        )
        return (
            f"💳 <strong>Membership Plans</strong>\n\n"
            f"<table class='info-table'><tr><th>Plan</th><th>Cost</th><th>Books</th><th>Loan Period</th></tr>{rows}</table>\n\n"
            f"<strong>To register:</strong> Visit the library with a valid photo ID and proof of address.\n"
            f"Children under 12 require a parent/guardian signature.\n\n"
            f"📌 All members also get free Wi-Fi, computer access, and event discounts!"
        )

    elif intent == "events":
        items = "".join(
            f"<div class='event-card'>🎉 <strong>{e['name']}</strong><br>"
            f"📅 {e['day']} at {e['time']} · 📍 {e['location']}</div>"
            for e in EVENTS
        )
        return f"🎉 <strong>Upcoming Events & Programs</strong>\n\n{items}\n\nTo register for events, visit the front desk or go to <em>citylib.org/events</em>"

    elif intent == "services":
        items = "\n".join(f"• {s}" for s in SERVICES)
        return f"🛠️ <strong>Library Services</strong>\n\n{items}\n\nFor more details on any service, just ask!"

    elif intent == "contact":
        c = LIBRARY_INFO["contact"]
        return (
            f"📞 <strong>Contact Information</strong>\n\n"
            f"📍 <strong>Address:</strong> {c['address']}\n"
            f"📞 <strong>Phone:</strong> {c['phone']}\n"
            f"📧 <strong>Email:</strong> {c['email']}\n\n"
            f"🌐 <strong>Website:</strong> www.citylib.org\n"
            f"💬 <strong>Live chat:</strong> Available on our website (Mon–Fri, 9 AM–5 PM)"
        )

    elif intent == "wifi":
        return (
            f"📶 <strong>Library Wi-Fi</strong>\n\n"
            f"Network: <strong>CityLibrary_Public</strong>\n"
            f"Password: <strong>{LIBRARY_INFO['wifi_password']}</strong>\n\n"
            f"• Free for all visitors\n"
            f"• Available throughout the building\n"
            f"• Sessions auto-renew every 2 hours\n"
            f"• Please be mindful of other patrons — no streaming in quiet zones"
        )

    elif intent == "reservation":
        return (
            f"📌 <strong>Book Reservations & Holds</strong>\n\n"
            f"You can place a hold on any book that's currently checked out:\n\n"
            f"• <strong>Online:</strong> citylib.org/catalog → search book → click 'Place Hold'\n"
            f"• <strong>Phone:</strong> Call {LIBRARY_INFO['contact']['phone']}\n"
            f"• <strong>In person:</strong> Ask at the circulation desk\n\n"
            f"You'll be notified by email/SMS when the book is ready.\n"
            f"Books are held for <strong>5 days</strong> once available."
        )

    elif intent == "recommend":
        popular = [b for b in BOOK_CATALOG if b["available"]]
        picks = random.sample(popular, min(4, len(popular)))
        items = "".join(
            f"<div class='book-card'>⭐ <strong>{b['title']}</strong><br>by {b['author']} · <em>{b['genre']}</em></div>"
            for b in picks
        )
        return f"⭐ <strong>Popular Picks Right Now</strong>\n\n{items}\n\nWant recommendations by genre? Ask: \"Recommend a Sci-Fi book\""

    else:
        return (
            f"🤔 I'm not sure I understood that. Here are some things I can help with:\n\n"
            f"• \"What are your opening hours?\"\n"
            f"• \"Find books about space\"\n"
            f"• \"When is my book due?\"\n"
            f"• \"What membership plans are available?\"\n"
            f"• \"What events do you have?\"\n"
            f"• \"What services does the library offer?\"\n\n"
            f"Or type <strong>help</strong> to see the full menu."
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please type a message."})
    response = get_response(user_message)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
