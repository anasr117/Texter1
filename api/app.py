# app.py
from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

def init_db():
    # Initialiser la base de données
    with sqlite3.connect("users.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                        sender TEXT,
                        receiver TEXT,
                        message TEXT
                        )''')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = hash_password(data.get("password"))

    with sqlite3.connect("users.db") as conn:
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return jsonify({"message": "Inscription réussie"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"message": "Nom d'utilisateur déjà pris"}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = hash_password(data.get("password"))

    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Connexion réussie"}), 200
        else:
            return jsonify({"message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data.get("sender")
    receiver = data.get("receiver")
    message = data.get("message")

    with sqlite3.connect("users.db") as conn:
        conn.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)", (sender, receiver, message))
        return jsonify({"message": "Message envoyé"}), 201

@app.route('/get_messages', methods=['GET'])
def get_messages():
    user = request.args.get("user")
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT sender, message FROM messages WHERE receiver=?", (user,))
        messages = [{"sender": row[0], "message": row[1]} for row in cursor.fetchall()]
        return jsonify(messages), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

