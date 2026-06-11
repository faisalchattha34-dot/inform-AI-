import sqlite3
import json

DB_NAME = "database.db"

def get_connection():
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
conn.row_factory = sqlite3.Row
return conn

def init_db():
conn = get_connection()
cur = conn.cursor()

```
# Users
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    created_at TEXT
)
""")

# Forms
cur.execute("""
CREATE TABLE IF NOT EXISTS forms (
    id TEXT PRIMARY KEY,
    form_name TEXT,
    columns TEXT,
    created_at TEXT
)
""")

# Recipients
cur.execute("""
CREATE TABLE IF NOT EXISTS recipients (
    id TEXT PRIMARY KEY,
    form_id TEXT,
    email TEXT,
    token TEXT,
    status TEXT
)
""")

# Responses
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
```

# --------------------------

# Forms

# --------------------------

def create_form(form_id, form_name, columns, created_at):
conn = get_connection()
cur = conn.cursor()

```
cur.execute("""
INSERT INTO forms(id, form_name, columns, created_at)
VALUES (?, ?, ?, ?)
""", (
    form_id,
    form_name,
    json.dumps(columns),
    created_at
))

conn.commit()
conn.close()
```

def get_forms():
conn = get_connection()
cur = conn.cursor()

```
cur.execute("SELECT * FROM forms")
rows = cur.fetchall()

conn.close()
return rows
```

def get_form(form_id):
conn = get_connection()
cur = conn.cursor()

```
cur.execute(
    "SELECT * FROM forms WHERE id=?",
    (form_id,)
)

row = cur.fetchone()

conn.close()
return row
```

# --------------------------

# Responses

# --------------------------

def save_response(response_id,
form_id,
response_data,
submitted_at):

```
conn = get_connection()
cur = conn.cursor()

cur.execute("""
INSERT INTO responses
(id, form_id, response_data, submitted_at)
VALUES (?, ?, ?, ?)
""", (
    response_id,
    form_id,
    json.dumps(response_data),
    submitted_at
))

conn.commit()
conn.close()
```

def get_responses():
conn = get_connection()
cur = conn.cursor()

```
cur.execute("SELECT * FROM responses")

rows = cur.fetchall()

conn.close()
return rows
```

def delete_response(response_id):
conn = get_connection()
cur = conn.cursor()

```
cur.execute(
    "DELETE FROM responses WHERE id=?",
    (response_id,)
)

conn.commit()
conn.close()
```
