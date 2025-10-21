# python-magazine-sql-challenge
readme_content = """# 📰 Object Relations Code Challenge - Articles

A Python SQL-based challenge that models **Authors**, **Magazines**, and **Articles** using **Object-Relational Mapping (ORM)-like** behavior with **raw SQL**.  
This project simulates an ORM layer manually — establishing relationships, managing persistence, and enforcing data integrity across related entities.

---

## 📚 Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Database Design](#database-design)
5. [Class Implementations](#class-implementations)
6. [Usage](#usage)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

---

## 🧠 Overview

This project builds a simple relational data model for a magazine publication system.  
It connects three entities:

- **Author** — Represents the writer, capable of contributing to multiple magazines.  
- **Magazine** — Represents a publication that can feature many articles from multiple authors.  
- **Article** — Represents written content that ties an Author to a Magazine.

Unlike ORM frameworks like SQLAlchemy, this project manually implements persistence logic using **SQLite3** and **raw SQL statements**.

---

## 🗂 Project Structure
