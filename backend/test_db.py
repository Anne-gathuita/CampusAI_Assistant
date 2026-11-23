import sys
from database import get_connection

try:
    connection = get_connection()

    if connection.is_connected():
        print("SUCCESS: Connected to CampusAI MySQL database!")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")

        result = cursor.fetchone()
        print("Connected database:", result[0])

        cursor.close()
        connection.close()

except Exception as error:
    print("DATABASE CONNECTION FAILED:")
    print(error)