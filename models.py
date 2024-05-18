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

def get_all_transcripts():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM transcripts')
    transcripts = c.fetchall()
    conn.close()
    return transcripts

def get_transcript_by_id(transcript_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM transcripts WHERE id = ?', (transcript_id,))
    transcript = c.fetchone()
    conn.close()
    return transcript

def search_transcripts(query):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query = f"%{query}%"
    c.execute('SELECT * FROM transcripts WHERE title LIKE ? OR content LIKE ?', (query, query))
    results = c.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_db()