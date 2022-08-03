import sqlite3
from flask import Flask, session, redirect, render_template, url_for, request
import hashlib

app = Flask(__name__)
app.secret_key = 'the random string'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session["user_id"]
    else:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = result.fetchone()
    username = user['username']
    result = cur.execute(f"SELECT * FROM posts where username='{username}'")
    posts = result.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        result = cur.execute(f"SELECT * FROM users WHERE username=? and password=?", (username, password))
        user = result.fetchone()
        if user:
            session['user_id'] = user["user_id"]
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        else:
            cur.close()
            conn.close()
            return "Incorrect user or password"
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('signup.html')