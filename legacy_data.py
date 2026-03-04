import sqlite3
import os

def setup_database():
    os.makedirs("data", exist_ok=True)
    db_path = "data/example.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer TEXT,
            status TEXT,
            amount REAL,
            notes TEXT
        )
    ''')

    mock_data = [
        (1, 'Cyberdyne Systems', 'PAID', 50000.0, 'Contact sarah.connor@gmail.com for keys.'),
        (2, 'Wayne Ent', 'PENDING', 1200.0, 'Send invoice to bruce@waynecorp.com immediately.'),
        (3, 'Umbrella Corp', 'FLAGGED', 0.0, 'Credit card 4242-4242-4242-4242 declined.')
    ]
    
    cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?,?,?,?,?)", mock_data)
    conn.commit()
    conn.close()
    print(f"Success: {db_path} created with mock data.")

if __name__ == "__main__":
    setup_database()
