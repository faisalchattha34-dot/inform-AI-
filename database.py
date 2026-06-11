import sqlite3

DB_NAME = "database.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS forms (
        id TEXT PRIMARY KEY,
        form_name TEXT,
        columns TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipients (
        id TEXT PRIMARY KEY,
        form_id TEXT,
        email TEXT,
        token TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id TEXT PRIMARY KEY,
        form_id TEXT,
        response_data TEXT,
        submitted_at TEXT
    )
    """)

    conn.commit()
    conn.close()
