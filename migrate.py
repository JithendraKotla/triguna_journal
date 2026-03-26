"""
migrate.py — Safe database migration script.
Run this once to upgrade an existing triguna.db to the new schema.
Usage: python migrate.py
"""
import sqlite3

DB_NAME = "triguna.db"

def run():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    migrations = {
        "journals": [
            ("reason",     "TEXT"),
            ("emotion",    "TEXT"),
            ("energy",     "TEXT"),
            ("focus",      "TEXT"),
            ("entry_time", "TEXT"),
        ]
    }

    for table, columns in migrations.items():
        cur.execute(f"PRAGMA table_info({table})")
        existing = {row[1] for row in cur.fetchall()}
        for col, typ in columns:
            if col not in existing:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
                print(f"✅ Added column '{col}' to {table}")
            else:
                print(f"⏭  Column '{col}' already exists in {table}")

    # Create lifestyle table if missing
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
    )""")
    print("✅ lifestyle table ready")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS badges(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        badge_name TEXT NOT NULL,
        earned_date TEXT NOT NULL,
        UNIQUE(user_id, badge_name)
    )""")
    print("✅ badges table ready")

    conn.commit()
    conn.close()
    print("\n✨ Migration complete!")

if __name__ == "__main__":
    run()
