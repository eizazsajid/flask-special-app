from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB_PATH = "users.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_user_by_username(username):
    cur = get_db().execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    cur.close()
    return row

@app.route("/")
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        if not username or not password:
            flash("Please provide username and password.", "error")
            return redirect(url_for("signup"))
        if get_user_by_username(username):
            flash("Username already taken. Try another.", "error")
            return redirect(url_for("signup"))
        hashed = generate_password_hash(password)
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        db.commit()
        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        user = get_user_by_username(username)
        if user and check_password_hash(user["password"], password):
            session['user'] = {"id": user["id"], "username": user["username"]}
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Try again.", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out.", "success")
    return redirect(url_for("index"))

# DASHBOARD - protected
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if 'user' not in session:
        flash("Please login to access dashboard.", "error")
        return redirect(url_for("login"))

    username = session['user']['username']
    message = ""
    if request.method == "POST":
        name = request.form.get("name", username).strip()
        msgs = [
            f"{name}, you're amazing! ✨",
            f"{name}, today will be a special day for you 😊",
            f"{name}, keep shining bright 💛",
            f"{name}, someone is thinking about you 😉",
            f"{name}, you're stronger than you think! 💫",
            f"{name}, a sweet surprise is heading your way! 🎁",
            f"{name}, keep smiling — it suits you! 😄"
        ]
        message = random.choice(msgs)
    return render_template("dashboard.html", username=username, message=message)

if __name__ == "__main__":
    # ensure DB exists
    if not os.path.exists(DB_PATH):
        print("Database not found. Run create_db.py first.")
    app.run(debug=True) 
  
# forgot_password
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # Check if user exists
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user:
            flash("Password reset link sent to your email.", "success")
        else:
            flash("Email not found.", "error")

    return render_template('forgot_password.html')