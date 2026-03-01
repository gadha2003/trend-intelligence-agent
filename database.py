import sqlite3
from datetime import datetime

conn = sqlite3.connect("trends.db", check_same_thread=False)
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

def save_trend(topic, source):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO trends (topic, source, timestamp) VALUES (?, ?, ?)",
        (topic, source, timestamp)
    )

    conn.commit()

def get_all_trends():

    cursor.execute("SELECT * FROM trends ORDER BY timestamp DESC")

    return cursor.fetchall()
