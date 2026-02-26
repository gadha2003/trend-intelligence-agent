import sqlite3

conn = sqlite3.connect("trends.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM trends WHERE topic='Unknown'")

conn.commit()

print("Unknown rows deleted")

conn.close()