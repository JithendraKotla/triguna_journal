import sqlite3
import os

# On Streamlit Cloud, use /tmp/ for writable storage.
# Locally, it will use triguna.db in the current directory.
DB_NAME = os.environ.get("DB_PATH", "/tmp/triguna.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and run migrations safely."""
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Journals table with constraints
    cur.execute("""
    CREATE TABLE IF NOT EXISTS journals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        journal_date TEXT NOT NULL,
        journal_text TEXT NOT NULL,
        guna TEXT CHECK(guna IN ('Sattva','Rajas','Tamas')),
        sattva REAL CHECK(sattva BETWEEN 0 AND 1),
        rajas REAL CHECK(rajas BETWEEN 0 AND 1),
        tamas REAL CHECK(tamas BETWEEN 0 AND 1),
        reason TEXT,
        emotion TEXT,
        energy TEXT,
        focus TEXT,
        entry_time TEXT,
        UNIQUE(user_id, journal_date)
    )
    """)

    # Lifestyle tracking table (for correlation engine)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS lifestyle(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        log_date TEXT NOT NULL,
        sleep_hours REAL,
        exercise_minutes REAL,
        screen_time REAL,
        meditation_minutes REAL,
        UNIQUE(user_id, log_date)
    )
    """)

    # Badges table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS badges(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        badge_name TEXT NOT NULL,
        earned_date TEXT NOT NULL,
        UNIQUE(user_id, badge_name)
    )
    """)

    conn.commit()

    # Run migrations for existing databases
    _run_migrations(cur, conn)
    conn.close()

def _run_migrations(cur, conn):
    """Safely add new columns to existing tables."""
    columns_to_add = {
        "journals": [
            ("reason", "TEXT"),
            ("emotion", "TEXT"),
            ("energy", "TEXT"),
            ("focus", "TEXT"),
            ("entry_time", "TEXT"),
        ]
    }
    for table, columns in columns_to_add.items():
        cur.execute(f"PRAGMA table_info({table})")
        existing = {row[1] for row in cur.fetchall()}
        for col_name, col_type in columns:
            if col_name not in existing:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}")
    conn.commit()
