"""
Library QnA Dataset
Topic: Library Chatbot (Lab 10)
"""

QNA_DATA = [
    # ── Hours & Location ──────────────────────────────────────────────
    {
        "question": "What are the library opening hours?",
        "answer": "The library is open Monday–Friday 8:00 AM–9:00 PM, Saturday 9:00 AM–6:00 PM, and Sunday 12:00 PM–5:00 PM."
    },
    {
        "question": "When does the library close?",
        "answer": "The library closes at 9:00 PM on weekdays, 6:00 PM on Saturdays, and 5:00 PM on Sundays."
    },
    {
        "question": "Is the library open on weekends?",
        "answer": "Yes! The library is open Saturday 9 AM–6 PM and Sunday 12 PM–5 PM."
    },
    {
        "question": "Is the library open on public holidays?",
        "answer": "The library is closed on major public holidays. Please check the library website or call ahead on holiday weekends."
    },
    {
        "question": "Where is the library located?",
        "answer": "The main library is located at 123 Knowledge Avenue, City Center. We also have two branch libraries — North Branch (45 Oak Street) and South Branch (78 Riverside Drive)."
    },
    {
        "question": "How do I get to the library?",
        "answer": "The library is accessible by Bus Routes 5, 12, and 22 (stop: City Library). Free parking is available in Lot B behind the building."
    },

    # ── Membership & Cards ────────────────────────────────────────────
    {
        "question": "How do I get a library card?",
        "answer": "Visit any library branch with a valid government-issued photo ID and proof of address. Library cards are free and issued on the spot."
    },
    {
        "question": "Can I apply for a library card online?",
        "answer": "Yes! You can apply for a temporary digital library card online at library.city.gov/register. Bring your ID within 30 days to convert it to a permanent card."
    },
    {
        "question": "Is a library card free?",
        "answer": "Yes, library membership and the library card are completely free for all residents."
    },
    {
        "question": "I lost my library card. What should I do?",
        "answer": "Report your lost card immediately at the circulation desk or online. A replacement card costs $2. Your account will be suspended until the card is replaced."
    },
    {
        "question": "Can children get a library card?",
        "answer": "Children under 18 can get a library card with a parent or guardian's signature and a valid ID."
    },
    {
        "question": "How long is a library card valid?",
        "answer": "Library cards are valid for 3 years. You will receive a renewal reminder by email before expiry."
    },

    # ── Borrowing & Returns ───────────────────────────────────────────
    {
        "question": "How many books can I borrow at once?",
        "answer": "Standard members may borrow up to 10 books, 5 DVDs/CDs, and 3 magazines at a time."
    },
    {
        "question": "What is the borrowing period for books?",
        "answer": "Books can be borrowed for 3 weeks (21 days). DVDs and CDs are for 1 week, and magazines for 1 week."
    },
    {
        "question": "Can I renew my borrowed items?",
        "answer": "Yes! You can renew items up to 2 times online, by phone, or in person, provided no one else has reserved them."
    },
    {
        "question": "How do I renew my books?",
        "answer": "Renew books via the library website (My Account), by calling 555-LIB-RENEW, or at any branch circulation desk."
    },
    {
        "question": "Where can I return library books?",
        "answer": "Return books at any library branch desk or use the 24-hour drop box outside the main entrance."
    },
    {
        "question": "Can I return books to a different branch?",
        "answer": "Yes, you can return books to any of our branch libraries, not just the one you borrowed from."
    },
    {
        "question": "What happens if I return a book late?",
        "answer": "Late fees are $0.25 per day per item for books and $1.00 per day for DVDs. Fees are capped at the replacement cost of the item."
    },
    {
        "question": "What if I lose or damage a library book?",
        "answer": "You will be charged the replacement cost of the item plus a $5 processing fee. Please report lost or damaged items as soon as possible."
    },

    # ── Reservations & Holds ──────────────────────────────────────────
    {
        "question": "How do I reserve a book?",
        "answer": "You can place a hold on any item through the library catalogue online, by phone, or at the desk. You'll be notified when it's ready for pickup."
    },
    {
        "question": "How long will the library hold a reserved book for me?",
        "answer": "Reserved items are held for 7 days after you are notified. After that, the item is returned to the shelves."
    },
    {
        "question": "Is there a fee to reserve a book?",
        "answer": "Placing holds is free for all library members."
    },
    {
        "question": "How many items can I have on hold at once?",
        "answer": "You can have up to 15 items on hold simultaneously."
    },

    # ── Digital Resources & E-Books ──────────────────────────────────
    {
        "question": "Does the library offer e-books?",
        "answer": "Yes! Access thousands of e-books and audiobooks through OverDrive/Libby and hoopla using your library card."
    },
    {
        "question": "How do I borrow e-books from the library?",
        "answer": "Download the Libby or hoopla app, sign in with your library card number and PIN, then browse and borrow digital titles instantly."
    },
    {
        "question": "Does the library have online databases?",
        "answer": "Yes, we subscribe to JSTOR, ProQuest, Britannica, and several newspaper archives. Access them free with your library card from home."
    },
    {
        "question": "Can I access library resources from home?",
        "answer": "Absolutely! E-books, audiobooks, databases, and digital magazines are all accessible remotely with your library card credentials."
    },

    # ── Computers & Wi-Fi ────────────────────────────────────────────
    {
        "question": "Does the library have free Wi-Fi?",
        "answer": "Yes, free Wi-Fi is available throughout all library buildings. Connect to 'CityLibrary_Guest' — no password required."
    },
    {
        "question": "Does the library have computers I can use?",
        "answer": "Yes, we have 30 public computers available on a first-come, first-served basis. Sessions are 60 minutes with a possible 30-minute extension if no one is waiting."
    },
    {
        "question": "Can I print documents at the library?",
        "answer": "Yes. Printing costs $0.15 per black-and-white page and $0.50 per colour page. Scanning and photocopying are also available."
    },

    # ── Study Rooms & Events ──────────────────────────────────────────
    {
        "question": "Can I book a study room?",
        "answer": "Yes, private and group study rooms can be booked up to 2 weeks in advance online or at the information desk. Rooms are free for library members."
    },
    {
        "question": "How long can I book a study room for?",
        "answer": "Study rooms can be booked for 2-hour blocks. You can book a maximum of 4 hours per day."
    },
    {
        "question": "Does the library have events or programs?",
        "answer": "Yes! We host author talks, children's story hours, coding workshops, book clubs, and more. Check our events calendar at library.city.gov/events."
    },
    {
        "question": "Does the library have a children's section?",
        "answer": "Yes, our dedicated Children's Library features picture books, early readers, activity kits, and weekly story time sessions for ages 2–8."
    },
    {
        "question": "Are there programs for seniors at the library?",
        "answer": "Yes, we offer Senior Tech Help sessions, large-print book clubs, and oral history programs. All are free and no booking is required."
    },

    # ── Research & Reference ──────────────────────────────────────────
    {
        "question": "Can library staff help me with research?",
        "answer": "Absolutely! Our reference librarians are available during library hours for in-person, phone, email, and live-chat research assistance."
    },
    {
        "question": "Does the library offer interlibrary loans?",
        "answer": "Yes, if we don't have a title, we can request it from partner libraries through our Interlibrary Loan (ILL) service. Requests take 3–10 business days."
    },
    {
        "question": "Does the library have a local history collection?",
        "answer": "Yes, our Special Collections room holds historical newspapers, photographs, maps, and genealogy records. Access is by appointment."
    },

    # ── Fines & Fees ─────────────────────────────────────────────────
    {
        "question": "How do I pay library fines?",
        "answer": "Fines can be paid in person at any branch, online via your library account, or by phone with a debit/credit card."
    },
    {
        "question": "What is the maximum fine I can have before my account is blocked?",
        "answer": "Your borrowing privileges are suspended when outstanding fines exceed $10.00."
    },

    # ── General ──────────────────────────────────────────────────────
    {
        "question": "How do I contact the library?",
        "answer": "Phone: 555-LIB-MAIN | Email: info@citylibrary.gov | Live Chat: available on our website during library hours."
    },
    {
        "question": "Can I donate books to the library?",
        "answer": "Yes! Book donations are accepted at the main branch Tuesday–Saturday. Items are evaluated and added to the collection or sold at our Friends of the Library book sales."
    },
    {
        "question": "Does the library have a café?",
        "answer": "Yes, The Page Turner Café on the ground floor serves coffee, tea, and light snacks. It is open Monday–Saturday 8 AM–7 PM."
    },
    {
        "question": "Is the library wheelchair accessible?",
        "answer": "All library branches are fully wheelchair accessible with ramps, lifts, accessible restrooms, and reserved parking spaces."
    },
    {
        "question": "Can I suggest a book for the library to purchase?",
        "answer": "Yes! Submit purchase suggestions via our website under 'Suggest a Title' or fill in a suggestion card at the information desk."
    },
]
