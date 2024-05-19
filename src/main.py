from db_manager import DatabaseManager as db
from user_session import UserSession as us
from book_store import BookStore as bs
from getpass import getpass

# Prompt for database connection details
host = input('Enter your host of the database: ')
user = input('Enter your user name: ')
passwd = getpass('Enter your password: ')
database = input('Enter your database name (schema name): ')

# Create a database connection
dbConnection = db(host, user, passwd, database)
connection = dbConnection.create_db_connection()

# Initialize user session and bookstore instances with the established database connection
userConnection = us(connection)
bookStore = bs(connection)

# Main function to run the bookstore application
def main():
    # Check if the database connection was successfully established
    if connection is not None:
        print("\n\033[32m" + "Welcome to the BookStore!" + "\033[0m")
        while True:
            # Main menu options
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                # Register a new user
                userConnection.register_member()
            elif choice == '2':
                # Login an existing user
                member = userConnection.login_member()
                if member:
                    userid = member[0]
                    # User-specific menu after successful login
                    while True:
                        print("\nMember Menu:")
                        print("1. Browse by Subject")
                        print("2. Search by Author/Title")
                        print("3. Check Out")
                        print("4. Logout")

                        member_choice = input("Choose an option: ")
                        if member_choice == '1':
                            bookStore.browse_by_subject(userid)
                        elif member_choice == '2':
                            bookStore.search_books(userid)
                        elif member_choice == '3':
                            bookStore.check_out(userid)
                        elif member_choice == '4':
                            print("\033[31m" + "You have been logged out." + "\033[0m")
                            break  # Logs the user out
                        else:
                            print("\033[91m" + "Invalid option. Please try again." + "\033[0m")
            elif choice == '3':
                # Exit message and close database connection
                print("\nThank you for visiting the BookStore. Goodbye!")
                connection.close()
                break
            else:
                print("\033[91m" + "Invalid option. Please try again." + "\033[0m")

main()
