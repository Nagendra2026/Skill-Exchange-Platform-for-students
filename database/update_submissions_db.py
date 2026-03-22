import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS submissions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
language TEXT,
code TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("Submissions table ready 🔥")
