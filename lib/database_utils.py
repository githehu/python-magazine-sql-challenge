import sqlite3

# Database file name
DB_FILE = 'magazine.db'

def get_connection(timeout: float = 30.0):
    """
    Creates and returns a connection to the SQLite database.
    Ensures foreign key support is turned ON.

    timeout: number of seconds to wait for the database lock to clear before
    raising an OperationalError. Increasing this helps transient "database is
    locked" errors under light concurrency.
    """
    # allow caller to tune timeout; default 30s to reduce spurious locking
    conn = sqlite3.connect(DB_FILE, timeout=timeout)
    # Ensure foreign keys are enforced for this connection
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    """
    Creates tables for authors, magazines, and articles with
    proper foreign key relationships.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create authors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """)

    # Create magazines table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT
        );
    """)

    # Create articles table with foreign key constraints
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
            FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    create_tables()
