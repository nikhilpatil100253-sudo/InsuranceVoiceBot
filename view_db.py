import sqlite3

conn = sqlite3.connect("insurance.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM call_logs")
print(cursor.fetchone())

conn.close()