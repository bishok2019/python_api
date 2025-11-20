import psycopg

from python_api_backend.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Connect to PostgreSQL
conn = psycopg.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
)

# Open a cursor
cur = conn.cursor()

# ---------------- Create tables ----------------
cur.execute(
    """
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    rent_rate NUMERIC NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
)

cur.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    vehicle_id INTEGER REFERENCES vehicles(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
)

conn.commit()
print("Tables created successfully.")

# ---------------- Insert sample data ----------------
cur.execute("SELECT COUNT(*) FROM vehicles;")
if cur.fetchone()[0] == 0:
    cur.execute(
        "INSERT INTO vehicles (name, model, rent_rate) VALUES (%s, %s, %s) RETURNING id;",
        ("Toyota", "Corolla", 100),
    )
    vehicle_id = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO users (username, vehicle_id) VALUES (%s, %s);",
        ("bishok", vehicle_id),
    )
    conn.commit()
    print("Sample data inserted.")

# ---------------- Query data ----------------
cur.execute(
    """
SELECT u.username, v.name
FROM users u
LEFT JOIN vehicles v ON u.vehicle_id = v.id;
"""
)

for username, vehicle_name in cur.fetchall():
    print(f"{username} drives {vehicle_name if vehicle_name else 'no vehicle'}")

# ---------------- Close connection ----------------
cur.close()
conn.close()
print("Disconnected safely.")
