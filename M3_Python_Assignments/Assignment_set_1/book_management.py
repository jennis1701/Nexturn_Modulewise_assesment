# book_management.py

class Book:
    def __init__(self, title, author, price, quantity):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity

    def display_details(self):
        return f"Title: {self.title}, Author: {self.author}, Price: ${self.price:.2f}, Quantity: {self.quantity}"


# Inventory list to store books
inventory = []


def add_book(title, author, price, quantity):
    try:
        price = float(price)
        quantity = int(quantity)
        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive numbers.")
        new_book = Book(title, author, price, quantity)
        inventory.append(new_book)
        return "Book added successfully!"
    except ValueError as e:
        return f"Invalid input! {e}"


def view_books():
    if not inventory:
        return "No books available in inventory."
    return "\n".join(book.display_details() for book in inventory)


def search_book(keyword):
    results = [book for book in inventory if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
    if not results:
        return "No matching books found."
    return "\n".join(book.display_details() for book in results)
