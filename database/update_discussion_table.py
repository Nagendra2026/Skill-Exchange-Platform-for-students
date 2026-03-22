import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Create discussion_messages table if not exists
c.execute("""
CREATE TABLE IF NOT EXISTS discussion_messages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
discussion_id INTEGER,
user_id INTEGER,
message TEXT,
file TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# If table already exists and file column missing, this will add it
try:
    c.execute("ALTER TABLE discussion_messages ADD COLUMN file TEXT")
except:
    pass  # column already exists

conn.commit()
conn.close()

print("Discussion table updated successfully 🚀")
