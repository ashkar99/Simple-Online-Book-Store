# Simple-Online-Book-Store

## Overview
The Online Bookstore is a Python-based web application that allows users to register, log in, browse books by subject, search for books by author or title, and manage their shopping cart. Users can also check out and receive an invoice for their orders. The application connects to a MySQL database to manage user data, book inventory, and orders.

## Features

- **User Registration and Authentication**: Users can register and log in to their accounts securely.
- **Browse Books**: Users can browse books by subject.
- **Search Books**: Users can search for books by author or title.
- **Shopping Cart**: Users can add books to their cart and manage the cart contents.
- **Checkout and Invoicing**: Users can check out, receive an invoice, and view the estimated delivery date.

## Project Structure

- `main.py`: The main entry point of the application. It handles user input and navigation through the application.
- `user_session.py`: Manages user registration and authentication.
- `book_store.py`: Contains functionalities for browsing books, searching books, managing the cart, and checking out.
- `db_manager.py`: Manages the database connection and handles database-related operations.
- `book_store_tables.sql`: SQL script for creating the necessary database tables.
- `books.sql`: SQL script for populating the database with book data.

## Getting Started

### Prerequisites

- Python 3.x
- MySQL Server
- MySQL Connector for Python

### Installation

1. **Clone the Repository**:
   git clone https://github.com/ashkar99/Simple-Online-Book-Store.git
   cd Simple-Onlline-Book-Store
   

2. **Install Required Python Packages**:
    pip install mysql-connector-python

3. **Setup MySQL Database**:
    - Create a new database in MySQL.
    - Run the book_store_tables.sql script to create the necessary tables
        - mysql -u yourusername -p yourpassword yourdatabase < /path/to/book_store_tables.sql
    - Run the books.sql script to populate the database with initial book data:
        - mysql -u yourusername -p yourpassword yourdatabase < /path/to/books.sql
### Running the Application
1. **Start the Application**:
    - Copy code
    - python main.py
2. **Follow the On-Screen Prompts**:
    - Enter your database connection details.
    - Register a new user or log in with an existing account.
    - Browse books, search for books, add books to your cart, and proceed to checkout.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License