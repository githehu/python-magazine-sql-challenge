from .database_utils import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self._name = None
        self._category = None
        self.name = name
        self.category = category

    # --------------------------
    # Property validation
    # --------------------------
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
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value.strip()

    # --------------------------
    # Relationship methods
    # --------------------------
    def articles(self):
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def contributors(self):
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author.new_from_db(row) for row in rows]

    # --------------------------
    # Database methods
    # --------------------------
    @classmethod
    def new_from_db(cls, row):
        return cls(id=row[0], name=row[1], category=row[2])

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE magazines SET name=?, category=? WHERE id=?", (self.name, self.category, self.id))
            conn.commit()
            print(f"✅ Magazine saved: {self.name}")
        except Exception as e:
            print(f"❌ Error saving magazine: {e}")
        finally:
            conn.close()

    # --------------------------
    # Phase 4: Aggregate / Bonus
    # --------------------------
    def article_titles(self):
        """Return all article titles for this magazine."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        """Return authors who have written more than 2 articles for this magazine."""
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT author_id FROM articles
            WHERE magazine_id = ?
            GROUP BY author_id
            HAVING COUNT(id) > 2
        """, (self.id,))
        author_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return [Author.find_by_id(aid) for aid in author_ids]

    @classmethod
    def top_publisher(cls):
        """Return the magazine with the highest number of articles."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazine_id, COUNT(id) AS article_count
            FROM articles
            GROUP BY magazine_id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return cls.find_by_id(row[0])
