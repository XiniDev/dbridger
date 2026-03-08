import sqlite3
import os

def setup_database():
    os.makedirs("data", exist_ok=True)
    db_path = "data/example.db"

    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON") 
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            ssn TEXT,
            registration_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            address_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            address_type TEXT, -- 'BILLING' or 'SHIPPING'
            street TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_methods (
            payment_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            card_type TEXT,
            card_number TEXT,
            expiration TEXT,
            cvv TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            sku TEXT UNIQUE,
            name TEXT,
            category TEXT,
            unit_price REAL,
            stock_level INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            shipping_address_id INTEGER,
            payment_id INTEGER,
            status TEXT,
            order_date TEXT,
            total_value REAL,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (shipping_address_id) REFERENCES addresses (address_id),
            FOREIGN KEY (payment_id) REFERENCES payment_methods (payment_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price_at_purchase REAL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT,
            internal_email TEXT,
            manager_id INTEGER, -- Self-referencing FK
            FOREIGN KEY (manager_id) REFERENCES employees (emp_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            tracking_num TEXT PRIMARY KEY,
            order_id INTEGER,
            handler_emp_id INTEGER,
            carrier TEXT,
            status TEXT,
            driver_notes TEXT,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (handler_emp_id) REFERENCES employees (emp_id)
        )
    ''')


    users = [
        (1, 'Bruce', 'Wayne', 'b.wayne@wayne-enterprises.com', '555-0192', '000-11-2222', '2025-01-15'),
        (2, 'Clark', 'Kent', 'ckent@dailyplanet.news', '555-8831', '999-88-7777', '2025-02-10'),
        (3, 'Diana', 'Prince', 'diana@themyscira.gov', '555-4444', '111-22-3333', '2025-03-01')
    ]

    addresses = [
        (101, 1, 'BILLING', '1007 Mountain Drive', 'Gotham', 'NJ', '07001'),
        (102, 1, 'SHIPPING', 'Batcave Entrance 4', 'Gotham', 'NJ', '07001'),
        (103, 2, 'SHIPPING', '1938 Sullivan Ln', 'Metropolis', 'NY', '10001')
    ]

    payments = [
        (501, 1, 'AMEX', '3782-111122-33334', '12/28', '456'),
        (502, 2, 'VISA', '4000-1234-5678-9010', '08/26', '123')
    ]

    products = [
        (1001, 'SKU-TAC-01', 'Tactical Grapple Hook', 'Gear', 450.00, 15),
        (1002, 'SKU-OPT-99', 'Lead-Lined Glasses', 'Apparel', 120.50, 200),
        (1003, 'SKU-DEF-44', 'Bracelets of Submission', 'Armor', 9999.99, 2)
    ]

    orders = [
        (50001, 1, 102, 501, 'DELIVERED', '2026-03-01', 900.00),
        (50002, 2, 103, 502, 'IN_TRANSIT', '2026-03-04', 120.50)
    ]

    order_items = [
        (1, 50001, 1001, 2, 450.00),
        (2, 50002, 1002, 1, 120.50)
    ]

    employees = [
        (1, 'Lex Luthor', 'CEO', 'lluthor@lexcorp.com', None),
        (2, 'Mercy Graves', 'Head of Logistics', 'mgraves@lexcorp.com', 1),
        (3, 'John Doe', 'Warehouse Worker', 'jdoe@lexcorp.com', 2)
    ]

    shipments = [
        ('TRK-999-XYZ', 50001, 2, 'LexPost', 'DELIVERED', 'Left package in the cave. Bats everywhere.'),
        ('TRK-888-ABC', 50002, 3, 'LexPost', 'DELAYED', 'Package glowing green. Driver felt sick. Call manager Mercy Graves immediately.')
    ]

    cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?)", users)
    cursor.executemany("INSERT INTO addresses VALUES (?,?,?,?,?,?,?)", addresses)
    cursor.executemany("INSERT INTO payment_methods VALUES (?,?,?,?,?,?)", payments)
    cursor.executemany("INSERT INTO products VALUES (?,?,?,?,?,?)", products)
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", orders)
    cursor.executemany("INSERT INTO order_items VALUES (?,?,?,?,?)", order_items)
    cursor.executemany("INSERT INTO employees VALUES (?,?,?,?,?)", employees)
    cursor.executemany("INSERT INTO shipments VALUES (?,?,?,?,?,?)", shipments)

    conn.commit()
    conn.close()
    print(f"Success: {db_path} created with Complex Enterprise Mock Data.")

if __name__ == "__main__":
    setup_database()
