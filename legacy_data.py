import sqlite3
import os

def setup_database():
    os.makedirs("data", exist_ok=True)
    db_path = "data/example.db"

    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            company_name TEXT,
            contact_email TEXT,
            account_tier TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            status TEXT,
            total_amount REAL,
            internal_notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_tickets (
            ticket_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            issue_type TEXT,
            priority TEXT,
            agent_notes TEXT,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        )
    ''')

    customers = [
        (101, 'Cyberdyne Systems', 'miles.bennett@cyberdyne.com', 'Gold'),
        (102, 'Wayne Enterprises', 'l.fox@waynecorp.com', 'Platinum'),
        (103, 'Umbrella Corp', 'albert.wesker@umbrella.io', 'Silver')
    ]

    orders = [
        (5001, 101, 'COMPLETED', 75000.0, 'Sensitive: Prototype CPU delivery. Email t800@future.com for gate code.'),
        (5002, 102, 'PENDING', 1200.50, 'Standard bat-widget shipment. Billing: finance@waynecorp.com'),
        (5003, 101, 'CANCELLED', 0.0, 'Client complained about "judgment day" delays.'),
        (5004, 103, 'SHIPPED', 890.0, 'Biological samples. Handling CC: 1234-5678-9012-3456')
    ]

    tickets = [
        (901, 5001, 'Delivery', 'HIGH', 'Sarah Connor reported suspicious activity near the truck.'),
        (902, 5004, 'Refund', 'LOW', 'Wesker requested a refund for leaked vials.')
    ]

    cursor.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)
    cursor.executemany("INSERT INTO support_tickets VALUES (?,?,?,?,?)", tickets)

    conn.commit()
    conn.close()
    print(f"Success: {db_path} created with Relational Mock Data.")

if __name__ == "__main__":
    setup_database()
