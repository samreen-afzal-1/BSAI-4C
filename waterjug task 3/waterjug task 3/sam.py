from flask import Flask, render_template, request, session
from collections import deque

app = Flask(__name__)
app.secret_key = "waterjuggame"

# ✅ BFS Recommendation (Shortest Path)
def bfs_recommend(cap1, cap2, goal, start):
    queue = deque([(start[0], start[1], [])])
    visited = set()

    while queue:
        jug1, jug2, path = queue.popleft()

        if (jug1, jug2) in visited:
            continue

        visited.add((jug1, jug2))

        if jug1 == goal or jug2 == goal:
            return path[0] if path else "🎯 Goal Reached!"

        next_states = []

        # Fill
        next_states.append((cap1, jug2, path + ["Fill Jug1"]))
        next_states.append((jug1, cap2, path + ["Fill Jug2"]))

        # Empty
        next_states.append((0, jug2, path + ["Empty Jug1"]))
        next_states.append((jug1, 0, path + ["Empty Jug2"]))

        # Pour Jug1 → Jug2
        transfer = min(jug1, cap2 - jug2)
        next_states.append((jug1 - transfer, jug2 + transfer,
                            path + ["Pour Jug1 → Jug2"]))

        # Pour Jug2 → Jug1
        transfer = min(jug2, cap1 - jug1)
        next_states.append((jug1 + transfer, jug2 - transfer,
                            path + ["Pour Jug2 → Jug1"]))

        for state in next_states:
            queue.append(state)

    return "❌ No Solution"


@app.route("/", methods=["GET", "POST"])
def index():

    if "jug1" not in session:
        session["jug1"] = 0
        session["jug2"] = 0
        session["steps"] = 0

    if request.method == "POST":

        # 🔄 Start Game
        if "start" in request.form:
            session["cap1"] = int(request.form["cap1"])
            session["cap2"] = int(request.form["cap2"])
            session["goal"] = int(request.form["goal"])
            session["jug1"] = 0
            session["jug2"] = 0
            session["steps"] = 0

        # 🔁 Reset
        elif "reset" in request.form:
            session.clear()
            return render_template("index.html")

        # 🎮 Manual Move
        else:
            cap1 = session["cap1"]
            cap2 = session["cap2"]
            jug1 = session["jug1"]
            jug2 = session["jug2"]
            move = request.form["move"]

            if move == "fill1":
                jug1 = cap1
            elif move == "fill2":
                jug2 = cap2
            elif move == "empty1":
                jug1 = 0
            elif move == "empty2":
                jug2 = 0
            elif move == "pour12":
                transfer = min(jug1, cap2 - jug2)
                jug1 -= transfer
                jug2 += transfer
            elif move == "pour21":
                transfer = min(jug2, cap1 - jug1)
                jug2 -= transfer
                jug1 += transfer

            session["jug1"] = jug1
            session["jug2"] = jug2
            session["steps"] += 1

    recommendation = None
    goal_reached = False

    if "cap1" in session:
        recommendation = bfs_recommend(
            session["cap1"],
            session["cap2"],
            session["goal"],
            (session["jug1"], session["jug2"])
        )

        if session["jug1"] == session["goal"] or session["jug2"] == session["goal"]:
            goal_reached = True

    return render_template("index.html",
                           jug1=session.get("jug1", 0),
                           jug2=session.get("jug2", 0),
                           cap1=session.get("cap1"),
                           cap2=session.get("cap2"),
                           goal=session.get("goal"),
                           recommendation=recommendation,
                           steps=session.get("steps", 0),
                           goal_reached=goal_reached)


if __name__ == "__main__":
    app.run(debug=True)