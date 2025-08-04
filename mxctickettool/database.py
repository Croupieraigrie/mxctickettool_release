import sqlite3

DB_PATH = "data/tickets.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        thread_id INTEGER,
        status TEXT,
        created_at TEXT,
        closed_at TEXT
    )''')
    conn.commit()
    conn.close()

def create_ticket(user_id, thread_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tickets (user_id, thread_id, status, created_at) VALUES (?, ?, 'open', datetime('now'))", (user_id, thread_id))
    conn.commit()
    conn.close()

def close_ticket(thread_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE tickets SET status='closed', closed_at=datetime('now') WHERE thread_id=?", (thread_id,))
    conn.commit()
    conn.close()

# ... get_ticket_by_user etc.
