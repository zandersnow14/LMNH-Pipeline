"""Script which resets the database."""
from os import environ
import sys

from dotenv import load_dotenv
from psycopg2 import OperationalError

from pipeline import get_db_connection

RESET_QUERY = """
    TRUNCATE TABLE reviews;
    TRUNCATE TABLE assistances;
    TRUNCATE TABLE emergencies;
    """


if __name__ == "__main__":

    load_dotenv()

    try:
        db_conn = get_db_connection(environ)
    except OperationalError:
        print("Failed to connect to database")
        sys.exit()

    with db_conn.cursor() as cur:
        cur.execute(RESET_QUERY)

    db_conn.commit()
