import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.connection = None

    def create_db_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database
            )
            return self.connection
        except mysql.connector.Error as err:
            print("\033[31m" + "Error: " + str(err) + "\033[0m")
            return None
