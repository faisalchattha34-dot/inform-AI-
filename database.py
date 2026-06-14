# database.py

import sqlite3
from datetime import datetime

DB_NAME = ".data/app.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        created_at TEXT
    )
    """)

    # Forms
    cur.execute("""
    CREATE TABLE IF NOT EXISTS forms (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        form_name TEXT,
        columns_json TEXT,
        created_at TEXT
    )
    """)

    # Responses
    cur.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id TEXT PRIMARY KEY,
        form_id TEXT,
        data_json TEXT,
        submitted_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# ==========================
# USER FUNCTIONS
# ==========================
def create_user(username, email, password):

    conn = get_connection()
    cur = conn.cursor()

    # Check if email already exists
    cur.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    existing_user = cur.fetchone()

    if existing_user:
        conn.close()
        return False

    cur.execute("""
    INSERT INTO users
    (username,email,password,created_at)
    VALUES (?,?,?,?)
    """, (
        username,
        email,
        password,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return True

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM users
    WHERE email=? AND password=?
    """, (email, password))

    user = cur.fetchone()

    conn.close()

    return user


# ==========================
# FORM FUNCTIONS
# ==========================

def save_form(form_id,
              user_id,
              form_name,
              columns_json):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO forms
    (id,user_id,form_name,columns_json,created_at)
    VALUES (?,?,?,?,?)
    """, (
        form_id,
        user_id,
        form_name,
        columns_json,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_user_forms(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM forms
    WHERE user_id=?
    ORDER BY created_at DESC
    """, (user_id,))

    forms = cur.fetchall()

    conn.close()

    return forms


def get_form(form_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM forms
    WHERE id=?
    """, (form_id,))

    form = cur.fetchone()

    conn.close()

    return form


# ==========================
# RESPONSE FUNCTIONS
# ==========================

def save_response(
        response_id,
        form_id,
        data_json):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO responses
    (id,form_id,data_json,submitted_at)
    VALUES (?,?,?,?)
    """, (
        response_id,
        form_id,
        data_json,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_responses(form_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM responses
    WHERE form_id=?
    ORDER BY submitted_at DESC
    """, (form_id,))

    rows = cur.fetchall()

    conn.close()

    return rows


def delete_response(response_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM responses
    WHERE id=?
    """, (response_id,))

    conn.commit()
    conn.close()
def get_all_forms():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM forms
    ORDER BY created_at DESC
    """)

    forms = cur.fetchall()

    conn.close()

    return forms
