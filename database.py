import sqlite3

DB_NAME = "contracts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        party1 TEXT,
        party2 TEXT,
        start_date TEXT,
        end_date TEXT,
        payment_terms TEXT,
        risk_level TEXT,
        raw_json TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_contract(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contracts 
    (party1, party2, start_date, end_date, payment_terms, risk_level, raw_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("party_1"),
        data.get("party_2"),
        data.get("start_date"),
        data.get("end_date"),
        data.get("payment_terms"),
        data.get("risk_level"),
        str(data)
    ))

    conn.commit()
    conn.close()


def get_all_contracts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contracts")
    rows = cursor.fetchall()

    conn.close()
    return rows