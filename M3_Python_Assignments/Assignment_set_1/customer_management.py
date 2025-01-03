# customer_management.py

class Customer:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def display_details(self):
        return f"Name: {self.name}, Email: {self.email}, Phone: {self.phone}"


# List to store customer details
customers = []


def add_customer(name, email, phone):
    if not name or not email or not phone:
        return "Invalid input! All fields are required."
    new_customer = Customer(name, email, phone)
    customers.append(new_customer)
    return "Customer added successfully!"


def view_customers():
    if not customers:
        return "No customers found."
    return "\n".join(customer.display_details() for customer in customers)
