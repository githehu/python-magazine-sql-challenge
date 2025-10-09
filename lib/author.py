from .database_utils import get_connection

class Author:
    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.name = name  # use property setter
        self.email = email
     # Property with validation
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = value.strip()
    
     # Relationships

    def articles(self):
        """Return all articles written by this author."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from .article import Article  # lazy import to avoid circular dependency
        return [Article.new_from_db(row) for row in rows]


    def magazines(self):
        """Return all magazines this author has contributed to."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        from .magazine import Magazine  # lazy import to avoid circular dependency
        return [Magazine.new_from_db(row) for row in rows]

        #database method to get magazines for an author


    


    @classmethod
    def new_from_db(cls, row):
        """Instantiate an Author object from a DB row tuple."""
        return cls(id=row[0], name=row[1], email=row[2])

    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID and return an Author instance."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        """Insert a new author or update an existing one."""
        # Use a context manager so the connection is always closed even on error.
        # sqlite3's Connection supports the context manager protocol where
        # entering returns the connection and exiting commits (or rolls back on
        # exception) and closes the connection.
        with get_connection() as conn:
            cursor = conn.cursor()

            if self.id is None:
                cursor.execute(
                    "INSERT INTO authors (name, email) VALUES (?, ?)",
                    (self.name, self.email)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE authors SET name = ?, email = ? WHERE id = ?",
                    (self.name, self.email, self.id)
                )

        # connection committed and closed by context manager
        print(f"\u2705 Author saved: {self.name}")
