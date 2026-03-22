import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Create discussions table
c.execute("""
CREATE TABLE IF NOT EXISTS discussions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT
)
""")

# Create messages table
c.execute("""
CREATE TABLE IF NOT EXISTS messages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
discussion_id INTEGER,
user_id INTEGER,
message TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Insert default discussion topics
c.execute("INSERT INTO discussions(title) VALUES('Python Discussion')")
c.execute("INSERT INTO discussions(title) VALUES('Java Discussion')")
c.execute("INSERT INTO discussions(title) VALUES('Web Development')")
c.execute("INSERT INTO discussions(title) VALUES('Placement Preparation')")

conn.commit()
conn.close()

print("Discussion tables created successfully 🚀")
