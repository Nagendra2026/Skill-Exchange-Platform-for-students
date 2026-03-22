import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE sessions ADD COLUMN zoom_link TEXT")
    print("zoom_link column added successfully 🔥")
except:
    print("Column already exists 👍")

conn.commit()
conn.close()
