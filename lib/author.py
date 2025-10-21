from .database_utils import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self._name = None
        self.name = name

    # --------------------------
    # Property validation
    # --------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    # --------------------------
    # Relationship methods
    # --------------------------
    def articles(self):
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def magazines(self):
        from .magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine.new_from_db(row) for row in rows]

    # --------------------------
    # Database methods
    # --------------------------
    @classmethod
    def new_from_db(cls, row):
        return cls(id=row[0], name=row[1])

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
            conn.commit()
            print(f"✅ Author saved: {self.name}")
        except Exception as e:
            print(f"❌ Error saving author: {e}")
        finally:
            conn.close()

    # --------------------------
    # Phase 4: Aggregate / Bonus
    # --------------------------
    def add_article(self, magazine, title, content=""):
        """Create and save a new Article for this author in a given magazine."""
        from .article import Article
        article = Article(title=title, content=content, author=self, magazine=magazine)
        article.save()
        return article

    def topic_areas(self):
        """Return a list of unique categories from all magazines this author writes for."""
        magazines = self.magazines()
        categories = {m.category for m in magazines if m.category}
        return list(categories)
