from getpass import getpass
import mysql.connector
from db_manager import DatabaseManager

class UserSession:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def register_member(self):
        connection = self.db_manager # undvik detta
        if connection is not None:
            cursor = connection.cursor()
            print("\nRegister New Member")
            email = input("Enter your email: ")
            password = getpass("Enter your password: ")
            fname = input("Enter your first name: ")
            lname = input("Enter your last name: ")
            address = input("Enter your street address: ")
            city = input("Enter your city: ")
            zip_code = input("Enter your zip: ")
            
            try:
                cursor.execute("""
                    INSERT INTO members (email, password, fname, lname, address, city, zip) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (email, password, fname, lname, address, city, zip_code))
                connection.commit()
                print("\n\033[32m" + "You have registered successfully!" + "\033[0m")
            except mysql.connector.Error as err:
                print(f"Error: '{err}'")
            cursor.close()
        else:
            print("\033[31m" + "Failed to connect to the database." + "\033[0m")

    def login_member(self):
        connection = self.db_manager
        if connection is not None:
            cursor = connection.cursor(buffered=True)
            print("\nLogin")
            email = input("Enter your email: ")
            password = getpass("Enter your password: ")
            
            try:
                cursor.execute("""
                    SELECT * FROM members WHERE email = %s AND password = %s
                """, (email, password))
                member = cursor.fetchone()
                if member:
                    print("\n\033[32m" + "Login successfully" + "\033[0m")
                    # You can return member's information or ID based on your application's need
                    return member
                else:
                    print("\033[31m" + "Login failed. Please check your email and password." + "\033[0m")
                    return None
            except mysql.connector.Error as err:
                print(f"Error: '{err}'")
            cursor.close()
        else:
            print("\033[31m" + "Failed to connect to the database." + "\033[0m")


