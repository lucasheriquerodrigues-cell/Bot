import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        tarefa TEXT,
        horario TEXT,
        concluido INTEGER DEFAULT 0
    )
    """)
    conn.commit()