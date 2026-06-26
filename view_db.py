import sqlite3

conn = sqlite3.connect("insurance.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM call_logs")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()