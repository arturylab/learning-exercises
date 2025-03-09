import mysql.connector

try:
    conn = mysql.connector.connect(
        host="20.3.143.124",
        user="testuser",
        password="testpassword",
        database="testdb"
    )
    print("Connection successful!")
except Exception as e:
    print(f"An error has occurred: {e}")
finally:
    if conn.is_connected():
        conn.close()
        print("Connection closed.")
