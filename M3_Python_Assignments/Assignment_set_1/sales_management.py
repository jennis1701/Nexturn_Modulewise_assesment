# sales_management.py

from customer_management import Customer
from book_management import inventory


class Transaction(Customer):
    def __init__(self, name, email, phone, book_title, quantity_sold):
        super().__init__(name, email, phone)
        self.book_title = book_title
        self.quantity_sold = quantity_sold

    def display_details(self):
        return f"Customer: {self.name}, Book: {self.book_title}, Quantity Sold: {self.quantity_sold}"


# List to store sales records
sales = []


def sell_book(customer_name, customer_email, customer_phone, book_title, quantity_sold):
    try:
        quantity_sold = int(quantity_sold)
        if quantity_sold <= 0:
            raise ValueError("Quantity must be a positive number.")
        for book in inventory:
            if book.title.lower() == book_title.lower():
                if book.quantity >= quantity_sold:
                    book.quantity -= quantity_sold
                    new_transaction = Transaction(customer_name, customer_email, customer_phone, book.title, quantity_sold)
                    sales.append(new_transaction)
                    return f"Sale successful! Remaining quantity: {book.quantity}"
                else:
                    return f"Error: Only {book.quantity} copies available. Sale cannot be completed."
        return "Error: Book not found in inventory."
    except ValueError as e:
        return f"Invalid input! {e}"


def view_sales():
    if not sales:
        return "No sales records found."
    return "\n".join(sale.display_details() for sale in sales)
