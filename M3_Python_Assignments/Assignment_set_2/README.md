BookBuddy: A Book Collection Manager

Overview

BookBuddy is a RESTful API designed for managing a personal book collection. It allows users to perform CRUD (Create, Read, Update, Delete) operations on a SQLite database. The API is built using Flask and supports robust error handling and input validation.

This project is ideal for anyone looking to manage their book collection programmatically or as a backend for a book-related application.

Features

CRUD Operations:
Add a new book to the collection.
Retrieve all books or a specific book by ID.
Update book details.
Delete a book from the collection.

Filtering:
Retrieve books filtered by genre or author.

Validation:
Ensures all required fields are provided.
Validates published_year and genre against predefined criteria.

Error Handling:
Graceful handling of missing resources and invalid inputs.
Errors returned in JSON format for easy integration.