import sqlite3
import re

DATABASE = 'transcripts.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_transcript(title, url, content):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT OR REPLACE INTO transcripts (title, url, content)
            VALUES (?, ?, ?)
            ''', (title, url, content))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Failed to insert or replace transcript at {url}: {e}")
    finally:
        conn.close()
        
if __name__ == "__main__":
    init_db()

