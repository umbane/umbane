import psycopg2
import os

DATABASE_URL = (
    os.environ.get("DATABASE_URL")
    or "postgresql://umbane:password@localhost:5432/carbon"
)


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    return conn
