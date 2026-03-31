
import sqlite3

conn = sqlite3.connect("contracts.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE contracts ADD COLUMN full_text TEXT")

conn.commit()
conn.close()