import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    registration_date TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    url TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')

users = []
for i in range(100):
    username = f'user{i}'
    registration_date = datetime.now() - timedelta(days=random.randint(1, 100))
    users.append((username, registration_date.strftime('%Y-%m-%d %H:%M:%S')))

cursor.executemany('INSERT INTO users (username, registration_date) VALUES (?, ?)', users)

links = []
for user_id in range(100):
    num_links = random.randint(0, 10)  
    for _ in range(num_links):
        url = f'http://test.com/{random.randint(1000, 9999)}'
        links.append((user_id, url))

cursor.executemany('INSERT INTO links (user_id, url) VALUES (?, ?)', links)

conn.commit()
