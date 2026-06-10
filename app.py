import os
import sqlite3
from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

# Import LangGraph
from backend.graph import build_graph

# ----------------------------------
# App Setup
# ----------------------------------

app = Flask(__name__, static_folder="frontend")
app.secret_key = "supersecretkey"

# Absolute DB path (IMPORTANT FIX)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "users.db")

# ----------------------------------
# Initialize Database
# ----------------------------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------------------
# Serve Frontend
# ----------------------------------

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

# ----------------------------------
# Authentication APIs
# ----------------------------------

@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Missing fields"}), 400

        hashed = generate_password_hash(password)

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, hashed)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({"message": "Username already exists"}), 400

        conn.close()
        return jsonify({"message": "Registered successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if not user:
            return jsonify({"message": "Invalid username"}), 401

        if not check_password_hash(user[0], password):
            return jsonify({"message": "Incorrect password"}), 401

        session["user"] = username
        return jsonify({"message": "Login successful"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out"})


@app.route("/api/login-check")
def login_check():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify({"message": "Authorized"})


# ----------------------------------
# LangGraph Portfolio API
# ----------------------------------

graph = build_graph()

@app.route("/api/generate", methods=["POST"])
def generate():

    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        data = request.get_json()

        initial_state = {
            "profile": data,
            "logs": [],
            "retry": False
        }

        result = graph.invoke(initial_state)

        # SAFE structured response
        return jsonify({
            "risk_score": result.get("risk_score"),
            "allocation": result.get("allocation"),
            "stress_test": result.get("stress_test"),
            "explanation": result.get("explanation"),
            "compliance": result.get("compliance_review"),
            "logs": result.get("logs", [])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------
# Run Application
# ----------------------------------

if __name__ == "__main__":
    app.run(debug=True)