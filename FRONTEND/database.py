import sqlite3

DB_NAME = "returnback.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            education TEXT,
            previous_role TEXT,
            experience_years TEXT,
            career_break_years TEXT,
            career_break_reason TEXT,
            restart_score REAL
        )
    """)

    connection.commit()
    connection.close()