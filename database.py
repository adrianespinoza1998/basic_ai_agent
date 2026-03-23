import sqlite3
import json
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT,
            tool_calls TEXT,
            tool_call_id TEXT,
            date TEXT NOT NULL
        )
    """)

    # Migración para DBs existentes sin las columnas nuevas
    for column in ["tool_calls TEXT", "tool_call_id TEXT"]:
        try:
            cursor.execute(f"ALTER TABLE historial ADD COLUMN {column}")
        except sqlite3.OperationalError:
            pass  # La columna ya existe

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

def save_message(session: str, role: str, date: datetime, content: str = None, tool_calls=None, tool_call_id: str = None) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tool_calls_json = None
    if tool_calls:
        tool_calls_json = json.dumps([{
            "id": tc.id,
            "type": tc.type,
            "function": {"name": tc.function.name, "arguments": tc.function.arguments}
        } for tc in tool_calls])

    cursor.execute(
        "INSERT INTO historial (session, role, content, tool_calls, tool_call_id, date) VALUES (?, ?, ?, ?, ?, ?)",
        (session, role, content, tool_calls_json, tool_call_id, date.strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()
    return f"Mensaje guardado en la sesión '{session}'"

def read_ideas(category: str = None) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT text, category, role, date FROM ideas WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT text, category, role, date FROM ideas ORDER BY date DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No hay ideas guardadas todavía."
    
    result = "Ideas guardadas:\n"
    for text, category, date in rows:
        result += f"- [{category}] {text} ({date})\n"
    return result

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

def read_messages(session: str = None) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if session:
        cursor.execute("SELECT role, content, tool_calls, tool_call_id FROM historial WHERE session = ? ORDER BY date ASC", (session,))
    else:
        cursor.execute("SELECT role, content, tool_calls, tool_call_id FROM historial ORDER BY date ASC")

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return []

    messages = []
    for role, content, tool_calls_json, tool_call_id in rows:
        if role == "assistant" and tool_calls_json:
            messages.append({
                "role": "assistant",
                "content": content,
                "tool_calls": json.loads(tool_calls_json)
            })
        elif role == "tool":
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content
            })
        else:
            messages.append({"role": role, "content": content})

    return messages