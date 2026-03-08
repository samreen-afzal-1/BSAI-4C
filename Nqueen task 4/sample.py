from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "nqueensinteractive"

# Check if safe
def is_safe(board, row, col):
    for r in range(len(board)):
        c = board[r]
        if c == -1:
            continue
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

# Get blocked cells
def get_blocked_cells(board):
    n = len(board)
    blocked = set()

    for r in range(n):
        c = board[r]
        if c != -1:
            for i in range(n):
                # Same column
                blocked.add((i, c))
                # Same row
                blocked.add((r, i))

                # Diagonals
                if 0 <= r+i < n and 0 <= c+i < n:
                    blocked.add((r+i, c+i))
                if 0 <= r-i < n and 0 <= c-i < n:
                    blocked.add((r-i, c-i))
                if 0 <= r+i < n and 0 <= c-i < n:
                    blocked.add((r+i, c-i))
                if 0 <= r-i < n and 0 <= c+i < n:
                    blocked.add((r-i, c+i))

    return blocked

# AI Recommendation
def recommend_move(board):
    n = len(board)
    for row in range(n):
        if board[row] == -1:
            for col in range(n):
                if is_safe(board, row, col):
                    return (row, col)
            break
    return None


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        if "start" in request.form:
            n = int(request.form["n"])
            session["n"] = n
            session["board"] = [-1] * n
            session["message"] = ""

        elif "quit" in request.form:
            session.clear()
            return render_template("index.html")

        elif "restart" in request.form:
            n = session["n"]
            session["board"] = [-1] * n
            session["message"] = ""

        elif "place" in request.form:
            row = int(request.form["row"])
            col = int(request.form["col"])
            board = session["board"]

            if is_safe(board, row, col):
                board[row] = col
                session["board"] = board
                session["message"] = "✅ Queen placed!"

                if -1 not in board:
                    session["message"] = "🎉 Congratulations! You solved N-Queens!"
            else:
                session["message"] = "❌ Invalid move!"

    board = session.get("board")
    n = session.get("n")
    message = session.get("message", "")
    recommendation = None
    blocked = set()

    if board:
        recommendation = recommend_move(board)
        blocked = get_blocked_cells(board)

    return render_template("index.html",
                           n=n,
                           board=board,
                           message=message,
                           recommendation=recommendation,
                           blocked=blocked)


if __name__ == "__main__":
    app.run(debug=True)