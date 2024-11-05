# user_manager.py
import sqlite3
import hashlib

def create_user_table():
    # Crée la table utilisateur si elle n'existe pas encore
    with sqlite3.connect("storage.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT
                        )''')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    create_user_table()
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    hashed_pw = hash_password(password)

    with sqlite3.connect("storage.db") as conn:
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            print("Inscription réussie !")
        except sqlite3.IntegrityError:
            print("Nom d'utilisateur déjà pris.")

def login_user():
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    hashed_pw = hash_password(password)

    with sqlite3.connect("storage.db") as conn:
        cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
        user = cursor.fetchone()
        if user:
            print("Connexion réussie !")
            return username
        else:
            print("Nom d'utilisateur ou mot de passe incorrect.")
            return None
