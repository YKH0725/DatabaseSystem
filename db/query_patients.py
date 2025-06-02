
from db.db_config import conn, cursor

cursor.execute("SELECT * FROM Patient")
for row in cursor.fetchall():
    print(row)
conn.close()
