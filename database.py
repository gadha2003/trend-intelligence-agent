import sqlite3
from datetime import datetime

DB = "trends.db"

def init_db():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            source TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_trend(topic, source):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO trends (topic, source, timestamp) VALUES (?, ?, ?)",
        (topic, source, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

def get_trends():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic, source, timestamp
        FROM trends
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

init_db()
