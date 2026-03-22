import sqlite3

# create database connection
conn = sqlite3.connect("database.db")

# create cursor
c = conn.cursor()

# users table
c.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
role TEXT)
''')

# skills table
c.execute('''
CREATE TABLE IF NOT EXISTS skills(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
skill TEXT,
type TEXT)
''')

# sessions table
c.execute('''
CREATE TABLE IF NOT EXISTS sessions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
teacher_id INTEGER,
learner_id INTEGER,
skill TEXT,
status TEXT,
date TEXT,
time TEXT,
zoom_link TEXT)
''')

conn.commit()
conn.close()

print("Database setup completed 🔥")
