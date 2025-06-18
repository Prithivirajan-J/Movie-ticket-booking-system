import sqlite3

def init_db():
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
        username TEXT,
        movie TEXT,
        showtime TEXT,
        seat TEXT
    )""")
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def authenticate_user(username, password):
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone() is not None

def add_booking(username, movie, showtime, seat):
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings VALUES (?, ?, ?, ?)", (username, movie, showtime, seat))
    conn.commit()

def get_bookings(username):
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("SELECT movie, showtime, seat FROM bookings WHERE username = ?", (username,))
    return c.fetchall()
