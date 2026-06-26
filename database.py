import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        full_name VARCHAR,
        username VARCHAR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    

    cur.execute("""CREATE TABLE IF NOT EXISTS movie(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video TEXT,
        description TEXT,
        views INTEGER DEFAULT 1,
        movie_code INTEGER UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    
    conn.commit()
    conn.close()



def add_user(user_id, full_name, username):
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO users (user_id, full_name, username, created_at) VALUES (?,?,?,?)", (user_id, full_name, username, created_at))  
    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id, ))
    user = cur.fetchone()
    conn.commit()
    conn.close()
    return user



def get_all_movie_codes():
    conn = sqlite3.connect("kinox.db")
    cursor = conn.cursor()

    cursor.execute("SELECT movie_code FROM movie")
    codes = [row[0] for row in cursor.fetchall()]

    conn.close()
    return codes


def add_movie(video_id, desc, code):
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO movie(video, description, movie_code, created_at)
        VALUES (?, ?, ?, ?)
    """, (video_id, desc, code, created_at))

    conn.commit()
    conn.close()


def get_movie(code):
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM movie WHERE movie_code = ?", (code, ))
    movie = cur.fetchall()
    conn.commit()
    conn.close()
    return movie


def get_all_movie():
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM movie")
    movies = cur.fetchall()
    conn.commit()
    conn.close()
    return movies


def get_all_users():
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.commit()
    conn.close()
    return users

def delete_movie(code):
    conn = sqlite3.connect("kinox.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM movie WHERE movie_code = ?", (code, ))
    conn.commit()
    conn.close()