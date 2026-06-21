# src/db.py

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


def get_connection(mode="read"):
    """
    Create PostgreSQL connection.

    mode = "read"  -> uses READ_USER credentials
    mode = "write" -> uses WRITE_USER credentials
    """

    # Find project root folder
    project_root = Path(__file__).resolve().parent.parent

    # Build path to .env file
    env_path = project_root / ".env"

    # Load environment variables
    load_dotenv(env_path)

    # Select credentials based on mode
    if mode == "read":
        user = os.getenv("READ_USER")
        password = os.getenv("READ_PASSWORD")

    elif mode == "write":
        user = os.getenv("WRITE_USER")
        password = os.getenv("WRITE_PASSWORD")

    else:
        raise ValueError(
            "Invalid mode. Use 'read' or 'write'."
        )

    # Create PostgreSQL connection
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=user,
        password=password
    )

    return conn


def test_connection(conn):
    """
    Verify database connection using SELECT 1.
    """

    cursor = conn.cursor()

    cursor.execute("SELECT 1;")

    result = cursor.fetchone()

    cursor.close()

    return result == (1,)