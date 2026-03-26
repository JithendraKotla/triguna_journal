import bcrypt
from db import get_connection

def create_user(username, password):
    """Create a new user with bcrypt-hashed password."""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username,password) VALUES(?,?)", (username, hashed))
    conn.commit()
    conn.close()

def login_user(username, password):
    """Validate credentials and return user id on success, else None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[1]):
        return row[0]
    return None
