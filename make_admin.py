import mysql.connector
from mysql.connector import Error
from website import db
import sys

# Input 2 arguments: (1) email of user to update and
#                    (2) boolean to update is_admin to
def main(argv):   
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='database.db',
                                             user='root',
                                             password='password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    main(sys.argv[1:])