import sqlite3
from datetime import datetime

DB_PATH = "ideas.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_idea(text: str, category: str = "general") -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ideas (text, category, date) VALUES (?, ?, ?)",
        (text, category, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()
    return f"Idea guardada en categoría '{category}': '{text}'"

def read_ideas(category: str = None) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT text, category, date FROM ideas WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT text, category, date FROM ideas ORDER BY date DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No hay ideas guardadas todavía."
    
    result = "Ideas guardadas:\n"
    for text, category, date in rows:
        result += f"- [{category}] {text} ({date})\n"
    return result