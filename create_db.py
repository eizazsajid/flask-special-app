import sqlite3
from werkzeug.security import generate_password_hash

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized.")

def create_test_user():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    username = "test"
    password = "password123"  # sample password
    hashed = generate_password_hash(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print(f"Test user created -> username: {username} password: {password}")
    except sqlite3.IntegrityError:
        print("Test user already exists.")
    conn.close()

if __name__ == "__main__":
    init_db()
    create_test_user()
