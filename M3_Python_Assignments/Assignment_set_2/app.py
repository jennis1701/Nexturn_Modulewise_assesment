from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'bookbuddy.db'

# Initialize the database
def init_db():
    if not os.path.exists(DATABASE):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_year INTEGER NOT NULL,
                genre TEXT NOT NULL
            )
        ''')
        sample_books = [
            ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction"),
            ("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction"),
            ("1984", "George Orwell", 1949, "Sci-Fi"),
            ("Murder on the Orient Express", "Agatha Christie", 1934, "Mystery"),
        ]
        cursor.executemany('''
            INSERT INTO books (title, author, published_year, genre)
            VALUES (?, ?, ?, ?)
        ''', sample_books)
        connection.commit()
        connection.close()
        print("Database initialized.")

# Helper function to connect to the database
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    required_fields = ['title', 'author', 'published_year', 'genre']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Invalid data", "message": "All fields are required"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, published_year, genre)
            VALUES (?, ?, ?, ?)
        ''', (data['title'], data['author'], data['published_year'], data['genre']))
        connection.commit()
        book_id = cursor.lastrowid
        connection.close()
        return jsonify({"message": "Book added successfully", "book_id": book_id}), 201
    except Exception as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500

# Retrieve all books or filter by genre/author
@app.route('/books', methods=['GET'])
def get_books():
    genre = request.args.get('genre')
    author = request.args.get('author')
    query = 'SELECT * FROM books WHERE 1=1'
    params = []
    if genre:
        query += ' AND genre = ?'
        params.append(genre)
    if author:
        query += ' AND author = ?'
        params.append(author)

    connection = get_db_connection()
    books = connection.execute(query, params).fetchall()
    connection.close()
    return jsonify([dict(book) for book in books]), 200

# Retrieve a book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    connection = get_db_connection()
    book = connection.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    connection.close()
    if book is None:
        return jsonify({"error": "Book not found", "message": "No book exists with the provided ID"}), 404
    return jsonify(dict(book)), 200

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    connection = get_db_connection()
    book = connection.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        return jsonify({"error": "Book not found", "message": "No book exists with the provided ID"}), 404

    connection.execute('''
        UPDATE books
        SET title = ?, author = ?, published_year = ?, genre = ?
        WHERE id = ?
    ''', (data.get('title', book['title']),
          data.get('author', book['author']),
          data.get('published_year', book['published_year']),
          data.get('genre', book['genre']),
          book_id))
    connection.commit()
    connection.close()
    return jsonify({"message": "Book updated successfully"}), 200

# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    connection = get_db_connection()
    book = connection.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        return jsonify({"error": "Book not found", "message": "No book exists with the provided ID"}), 404

    connection.execute('DELETE FROM books WHERE id = ?', (book_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == "__main__":
    init_db()  # Initialize the database on the first run
    app.run(debug=True)
