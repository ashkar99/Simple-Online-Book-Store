from datetime import datetime, timedelta
import mysql.connector


class BookStore:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def browse_by_subject(self, userid):
        # Allow users to browse books by subject.
        connection = self.db_manager
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT _subject FROM books ORDER BY _subject ASC")
        subjects = cursor.fetchall()
        
        # Display subjects and handle user selection
        print("\nSubjects available:")
        for i, subject in enumerate(subjects, 1):
            print(f"{i}. {subject[0]}")
        
        subject_choice = int(input("Enter your choice: ")) - 1
        if subject_choice == -1:
            print

        # Display books from the selected subject
        chosen_subject = subjects[subject_choice][0]
        cursor.execute("SELECT isbn, title, author, price FROM books WHERE _subject = %s", (chosen_subject,))
        books = cursor.fetchall()

        # Browse through the list of books and offer actions
        index = 0
        while index < len(books):
            for i in range(2):
                if index < len(books):
                    book = books[index]
                    print(f"\nAuthor: {book[2]}\nTitle: {book[1]}\nISBN: {book[0]}\nPrice: {book[3]}\nSubject: {chosen_subject}")
                    index += 1

            # Process actions (add to cart, continue browsing, etc.)
            action = input("\nEnter ISBN to add to cart or ENTER to go back to menu or 'n' ENTER to continue browsing: ").strip().lower()
            if action == '':
                break  # Go back to main menu
            elif action == 'n':
                continue  # Show next set of books
            else:
                isbn_to_add = action
                qty = input("Enter quantity: ")
                try:
                    cursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qty = qty + %s",
                                (userid, isbn_to_add, qty, qty))
                    connection.commit()
                    print("\n\033[32m" + "Book added to cart." + "\033[0m")
                except mysql.connector.Error as err:
                    print("\033[31m" + "Error: " + str(err) + "\033[0m")
                    connection.rollback()

        cursor.close()

    def search_books(self, userid):
        #Allow users to search for books by author or title.
        connection = self.db_manager
        while True:
            cursor = connection.cursor()
            # Display search menu and handle input
            print("\nSearch Menu:")
            print("1. Author Search")
            print("2. Title Search")
            print("3. Go Back to Main Menu")
            search_choice = input("Type in your option: ").strip()

            if search_choice == '1':
                search_query = input("Enter author name or part of it: ").strip()
                cursor.execute("SELECT isbn, title, author, price FROM books WHERE author LIKE %s", ('%' + search_query + '%',))
            elif search_choice == '2':
                search_query = input("Enter title or part of the title: ").strip()
                cursor.execute("SELECT isbn, title, author, price FROM books WHERE title LIKE %s", ('%' + search_query + '%',))
            elif search_choice == '3':
                return
            else:
                print("\033[91m" + "Invalid option. Please try again." + "\033[0m")
                continue

            books = cursor.fetchall()
            if not books:
                print("\033[31m" + "No books found!" + "\033[0m")
                continue

            # Process search based on user choice
            index = 0
            while index < len(books):
                for i in range(3):
                    if index < len(books):
                        book = books[index]
                        print(f"\nAuthor: {book[2]}\nTitle: {book[1]}\nISBN: {book[0]}\nPrice: {book[3]}")
                        index += 1

                action = input("\nEnter ISBN to add to cart or ENTER to go back to menu or 'n' ENTER to continue browsing: ").strip().lower()
                if action == '':
                    break  # Go back to main menu
                elif action == 'n':
                    if index >= len(books):
                        print("\033[91m" + "No more books to show." + "\033[0m")
                        break
                    continue  # Show next set of books
                else:
                     #Allow adding books to cart from search results
                    isbn_to_add = action
                    qty = input("Enter quantity: ")
                    try:
                        cursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE qty = qty + %s",
                                    (userid, isbn_to_add, qty, qty))
                        connection.commit()
                        print("\033[32m" + "Book added to cat." + "\033[0m")
                    except mysql.connector.Error as err:
                        print("\033[31m" + "Error: " + str(err) + "\033[0m")
                        connection.rollback()

            cursor.close()

    def check_out(self, userid):
        # Process user checkout, including displaying cart, handling order placement, and printing an invoice.
        connection = self.db_manager
        cursor = connection.cursor(dictionary=True)
        cart_items = self.get_cart_contents(cursor, userid)
        total = sum(item['line_total'] for item in cart_items)

        # Display cart contents and total
        cursor.execute("SELECT fname AS name, address, city, zip FROM members WHERE userid = %s", (userid,))
        member_info = cursor.fetchone()
        print("Current Cart Contents:")
        print("\nISBN\t\tTitle\t\t\t\t\t\t\t\t\t\t\t\tQty\t\t\tTotal")
        for item in cart_items:
            print(f"{item['isbn']}\t{item['title']}\t{item['qty']}\t{item['line_total']}")
        print(f"Total\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{total:.2f}")
        confirmation = input("Proceed to check out (Y/N)?: ").strip().lower()
        if confirmation == 'y':
            try:
                # Insert a new order
                cursor.execute("""
                    INSERT INTO orders (userid, created, shipAddress, shipCity, shipZip) 
                    VALUES (%s, %s, (SELECT address FROM members WHERE userid = %s), 
                    (SELECT city FROM members WHERE userid = %s), 
                    (SELECT zip FROM members WHERE userid = %s))
                    """, (userid, datetime.now().date(), userid, userid, userid))
                ono = cursor.lastrowid
                
                shipment_date = datetime.now().date() + timedelta(days=7)

                # Add order details
                for item in cart_items:
                    cursor.execute("""
                        INSERT INTO odetails (ono, isbn, qty, amount) 
                        VALUES (%s, %s, %s, %s)
                        """, (ono, item['isbn'], item['qty'], item['line_total']))

                cursor.execute("DELETE FROM cart WHERE userid = %s", (userid,))
                connection.commit()
                member_info['ono'] = ono

                # Print invoice upon successful order placement
                self.print_invoice(cart_items, total, member_info)
                print("\n\033[32m" + "Estimated delivery date: " + str(shipment_date) + "\033[0m")
            except mysql.connector.Error as err:
                print("\033[31m" + "Error: " + str(err) + "\033[0m")
                connection.rollback()
        else:
            print("\033[31m" + "Checkout cancelled." + "\033[0m")
        cursor.close()

    def get_cart_contents(self, cursor, userid):
        # Fetch and return the contents of the user's cart.
        cursor.execute("SELECT c.isbn, b.title, c.qty, b.price, (c.qty * b.price) AS line_total FROM cart c JOIN books b ON c.isbn = b.isbn WHERE c.userid = %s", (userid,))
        return cursor.fetchall()

    def print_invoice(self, cart_items, total, member_info):
        # Print an invoice for the user after checkout.
        print(f"\nInvoice for Order no.{member_info['ono']}")
        print("Shipping Address")
        print(f"Name: {member_info['name']}")
        print(f"Address: {member_info['address']}")
        print(f"{member_info['city']} {member_info['zip']}")
        print("\nISBN\t\tTitle\t\t\t\t\t\t\t\t\t\t\t\tQty\t\t\tTotal")
        for item in cart_items:
            print(f"{item['isbn']}\t{item['title']}\t{item['qty']}\t{item['line_total']}")
        print(f"Total\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{total:.2f}")
        print()
