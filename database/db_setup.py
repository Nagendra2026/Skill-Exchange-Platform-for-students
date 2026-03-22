import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
role TEXT)
''')

# Skills table
cursor.execute('''
CREATE TABLE IF NOT EXISTS skills(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
skill TEXT,
type TEXT)
''')

# Sessions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sessions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
teacher_id INTEGER,
learner_id INTEGER,
skill TEXT,
status TEXT,
meeting_link TEXT)
''')

conn.commit()
conn.close()

print("Database created successfully")
