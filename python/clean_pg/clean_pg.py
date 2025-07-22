import os
import logging
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("db_maintenance.log"),
        logging.StreamHandler()
    ]
)

# Read DB credentials from environment
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DB = os.getenv("DB_NAME")

def connect():
    """
    Establish a connection to the PostgreSQL database.
    Returns:
        conn: A psycopg2 connection object.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB,
            user=USER,
            password=PASSWORD,
            host=HOST
        )
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        raise

def get_size(conn, table_name):
    """Retrieve the size of a specific table in the database.
    Args:
        conn: Database connection object.
        table_name: Name of the table to check size for."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                relname AS table_name,
                pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
                pg_size_pretty(pg_indexes_size(relid)) AS index_size,
                pg_size_pretty(pg_relation_size(relid)) AS actual_size
            FROM pg_catalog.pg_statio_user_tables
            WHERE relname = %s;
        """, (table_name,))
        return cur.fetchone()

def reindex(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f"REINDEX TABLE {table_name};")
    conn.commit()
    logging.info(f"Reindexed table: {table_name}")

def vacuum(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f"VACUUM {table_name};")
    conn.commit()
    logging.info(f"Vacuumed table: {table_name}")

def query_size(conn, when, table_name):
    result = get_size(conn, table_name)
    if not result:
        logging.warning(f"Could not retrieve size for table {table_name}")
        return

    name, total, index, actual = result
    when0, when1, when2 = ("had", "was", "was") if when == "before" else ("has", "is", "are")
    message = (f"Name: {name} {when0} a total size of: {total}, "
               f"The table size {when1}: {actual} and all index {when2}: {index}")
    logging.info(message)

def main():
    try:
        with open("tbl.lst", "r") as f:
            table_names = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error("tbl.lst file not found.")
        return

    with connect() as conn:
        for table_name in table_names:
            logging.info(f"Processing table: {table_name}")
            query_size(conn, "before", table_name)
            logging.info("Performing cleanup...")
            reindex(conn, table_name)
            vacuum(conn, table_name)
            query_size(conn, "after", table_name)
            logging.info(f"#### Table {table_name} Done ####")

if __name__ == "__main__":
    main()
