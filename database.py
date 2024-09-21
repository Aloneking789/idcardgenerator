import sqlite3

def init_db():
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT,
                        phone TEXT,
                        course TEXT,
                        fee_paid REAL,
                        fee_due REAL
                    )''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
