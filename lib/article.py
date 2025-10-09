from .database_utils import get_connection


class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        self.id = id
        self._title = None
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

        # Property with validation

    @property
    def title(self):
        return self._title

    
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Article title must be a non-empty string.")
        self._title = value.strip()

    # --------------------------
    # Database mapping helpers
    # --------------------------

    
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Content must be a non-empty string.")
        self._content = value.strip()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        from .author import Author
        if not isinstance(value, Author):
            raise ValueError("author must be an instance of Author.")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        from .magazine import Magazine
        if not isinstance(value, Magazine):
            raise ValueError("magazine must be an instance of Magazine.")
        self._magazine = value

    # --------------------------
    # Database methods
    # --------------------------
    
    

    @classmethod
    def new_from_db(cls, row):
          # get connected objects
        from .author import Author
        from .magazine import Magazine
        author = Author.find_by_id(row[3])
        magazine = Magazine.find_by_id(row[4])
        """Instantiate an Article object from a DB row tuple."""
        return cls(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4])

    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def save(self):
        """Insert or update an article."""
        if not self.author or not self.magazine:
            raise ValueError("Article must be linked to both an Author and a Magazine.")
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute(
                "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                (self.title, self.content, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.content, self.author_id, self.magazine_id, self.id)
            )

        conn.commit()
        conn.close()
        print(f"✅ Article saved: {self.title}")
