import sqlite3
from datetime import datetime

conn = sqlite3.connect("trends.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    source TEXT,
    timestamp TEXT
)
""")

# 🔥 AUTO ADD reason column if missing
cursor.execute("PRAGMA table_info(trends)")
columns = [column[1] for column in cursor.fetchall()]

if "reason" not in columns:
    cursor.execute("ALTER TABLE trends ADD COLUMN reason TEXT")
    conn.commit()

conn.commit()

def save_trend(topic, source, reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO trends (topic, source, reason, timestamp) VALUES (?, ?, ?, ?)",
        (topic, source, reason, timestamp)
    )

    conn.commit()
