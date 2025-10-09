from .database_utils import get_connection
 

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self._name = None
        self._category = None
        self.name = name
        self.category = category

    # Property with validation
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Magazine name must be a non-empty string.")
        self._name = value.strip()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Category must be a string or None.")
        self._category = value.strip() if value else None

    # --------------------------
    # Relationships
    # --------------------------
    def articles(self):
        """Return all articles for this magazine."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from .article import Article  # lazy import to avoid circular dependency
        return [Article.new_from_db(row) for row in rows]

    def contributors(self):
        """Return all authors who have written for this magazine."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles ar ON au.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        from .author import Author  # lazy import to avoid circular import
        return [Author.new_from_db(row) for row in rows]

    # --------------------------
    # Database methods
    # --------------------------


    @classmethod
    def new_from_db(cls, row):
        """Instantiate a Magazine object from a DB row tuple."""
        return cls(id=row[0], name=row[1], category=row[2])

    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        """Insert or update a magazine."""
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )

        conn.commit()
        conn.close()
        print(f"✅ Magazine saved: {self.name}")
