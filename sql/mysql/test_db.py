import mysql.connector

conn = mysql.connector.connect(
    host="20.3.143.124",
    user="testuser",
    password="testpassword",
    database="testdb"
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE
    )
""")

cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Juan Pérez", "juan@example.com"))
conn.commit()

cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()