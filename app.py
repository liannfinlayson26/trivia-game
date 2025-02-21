from flask import Flask, jsonify,render_template, request, session
import sqlite3 as sql
import random
from questions import trivia_questions

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure sqlite3 database
def get_db_connection():
    conn = sql.connect("leaderboard.db")
    conn.row_factory = sql.Row
    return conn

# Configure route to get questions
@app.route('/get_question')
def get_question():
    if "answered_questions" not in session:
        session["answered_questions"] = []
    # Flatten all questions into a single list with their categories
    all_questions = []
    for category, questions in trivia_questions.items():
        for q in questions:
            q["category"] = category # Add the category inside question dictionary
            all_questions.append(q)
    
    # Filter the already answered questions
    available_questions = [q for q in all_questions if q["id"] not in session["answered_questions"]]

    # If there are no more questions available, return a message (or handle accordingly)
    if not available_questions:
        return jsonify({"message": "No more questions available"})
    
    # Pick a random question
    question = random.choice(available_questions)
    
    #Store answered question
    session["answered_questions"].append(question["id"])
    session.modified = True

    # Send multiple values as a JSON response
    return jsonify({
        "category": question["category"],
        "question": question["question"],
        "choices": question["choices"],
        "correct_answer": question["correct_answer"]
    })    

# Configure route to update the score in sqlite3 database
@app.route('/update_score', methods=["POST"])
def update_score():
    data = request.get_json()

    # Insert the new score into the database
    name = data["name"]
    selected_answer = data["answer"]
    correct_answer = data["correct_answer"]

    points = 1 if selected_answer == correct_answer else 0
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM leaderboard WHERE name = ?", (name,))
    existing_score = cursor.fetchone()

    if existing_score:
    # Update existing score    
        new_score = existing_score[0] + points
        cursor.execute("UPDATE leaderboard SET score = ? WHERE name = ?", (new_score, name))
    else:
    # Insert new player
        cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, points))

    conn.commit()
    conn.close()
    return jsonify({"message": "Score updated successfully"})

# Configure route that updates the leaderboard score
@app.route("/leaderboard")
def get_leaderboard():
    # Get the top 10 players from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch top scores
    cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 10")
    leaderboard_data = [{"name": row[0], "score": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(leaderboard_data)

# Configure home route
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)