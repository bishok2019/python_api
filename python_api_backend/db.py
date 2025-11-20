import psycopg2
from psycopg2.extras import RealDictCursor

from .settings import *


def get_db_connection():
    """Create and return a PostgreSQL database connection"""
    conn = psycopg2.connect(
        # host=DATABASE_CONFIG['HOST'],
        # port=DATABASE_CONFIG['PORT'],
        # database=DATABASE_CONFIG['NAME'],
        # user=DATABASE_CONFIG['USER'],
        # password=DATABASE_CONFIG['PASSWORD']
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    return conn


def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create vehicles table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vehicles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            model VARCHAR(255) NOT NULL,
            rent_rate DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Create users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            vehicle_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
        )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully")


def get_dict_cursor(conn):
    """Get a cursor that returns results as dictionaries"""
    return conn.cursor(cursor_factory=RealDictCursor)


def close_db(conn):
    """Close database connection"""
    if conn:
        conn.close()
