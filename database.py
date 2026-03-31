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


def insert_contract(data, full_text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contracts 
    (party1, party2, start_date, end_date, payment_terms, risk_level, raw_json, full_text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("party_1"),
        data.get("party_2"),
        data.get("start_date"),
        data.get("end_date"),
        data.get("payment_terms"),
        data.get("risk_level"),
        str(data),
        full_text
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

def get_summary_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM contracts")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM contracts WHERE risk_level='High'")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM contracts WHERE risk_level='Medium'")
    medium_risk = cursor.fetchone()[0]

    conn.close()

    return total, high_risk, medium_risk


def get_contracts_by_filter(risk=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if risk:
        cursor.execute("SELECT * FROM contracts WHERE risk_level=?", (risk,))
    else:
        cursor.execute("SELECT * FROM contracts")

    rows = cursor.fetchall()
    conn.close()
    return rows