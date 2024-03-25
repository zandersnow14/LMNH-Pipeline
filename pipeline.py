"""Pipeline script which consumes and processes live data from Kafka"""

from os import environ, _Environ
import sys
import json
import logging
import argparse
from datetime import datetime

from confluent_kafka import Consumer
from dotenv import load_dotenv
from psycopg2.extensions import connection
from psycopg2.extras import execute_values
from psycopg2 import connect, OperationalError


EMERGENCIES_QUERY = """
            INSERT INTO emergencies (at, exhibition_id)
                VALUES %s
            ON CONFLICT DO NOTHING;
        """
ASSISTANCES_QUERY = """
            INSERT INTO assistances (at, exhibition_id)
                VALUES %s
            ON CONFLICT DO NOTHING;
        """
REVIEWS_QUERY = """
            INSERT INTO reviews (at, exhibition_id, rating_id)
                VALUES %s
            ON CONFLICT DO NOTHING;
        """


def get_db_connection(config: _Environ) -> connection:
    """Gets a connection to a database given config data."""

    return connect(
        dbname=config["DB_NAME"],
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        port=config["DB_PORT"])


def configure_kafka(config: _Environ) -> dict:
    """Configures Kafka properties."""

    return {
        'bootstrap.servers': config["BOOTSTRAP_SERVERS"],
        'security.protocol': config["SECURITY_PROTOCOL"],
        'sasl.mechanisms': config["SASL_MECHANISM"],
        'sasl.username': config["USERNAME"],
        'sasl.password': config["PASSWORD"],
        'group.id': config["GROUP"],
        'auto.offset.reset': environ["AUTO_OFFSET"]
    }


def get_ratings(data: dict[str]) -> list[str]:
    """Returns the ratings data from the overall data."""

    return [[
        data['at'],
        int(data['site']) + 1,
        data['val'] + 1
    ]]


def get_emergencies(data: list[dict[str]]) -> list[list[str]]:
    """Returns the emergencies data from the overall data."""

    return [[
        data['at'],
        int(data['site']) + 1
    ]]


def get_assistances(data: list[dict[str]]) -> list[list[str]]:
    """Returns the assistances data from the overall data."""

    return [[
        data['at'],
        int(data['site']) + 1
    ]]


def get_log_arg():
    """Sets up the log argument and returns it."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l',
        '--log',
        action='store_true',
        help='log progress to a file'
    )

    args = parser.parse_args()

    return args.log


def configure_log(choice: bool) -> None:
    """Configures logging properties."""

    if choice:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s - %(message)s",
            filename='data_errors.log'
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s - %(message)s"
        )


def missing_key(data: dict[str]) -> bool:
    """Tells us if a key is missing from the data, and logs the error."""

    rating_keys = {'at', 'site', 'val'}
    data_keys = set(data.keys())

    common_keys = rating_keys.intersection(data_keys)

    if common_keys != rating_keys:
        missed_key = list(rating_keys.difference(data_keys))[0]
        logging.error(f"missing {missed_key} - {data}")
        return True
    return False


def invalid_hour(data: dict[str]) -> bool:
    """Tells us if the hour is invalid and logs the error."""

    at = datetime.fromisoformat(data['at'])
    if at.hour not in range(8, 19):
        logging.error(f"hour ({at.hour}) not within opening hours - {data}")
        return True
    return False


def invalid_site(data: dict[str]) -> bool:
    """Tells us if the site is invalid and logs the error."""

    site = data['site']
    if not site.isnumeric() or int(site) not in range(0, 6):
        logging.error(f"site {site} does not exist - {data}")
        return True
    return False


def invalid_val(data: dict[str]) -> bool:
    """Tells us if the value is invalid, and logs the error."""

    val = data['val']
    if val not in range(-1, 5):
        logging.error(f"value {val} is invalid - {data}")
        return True
    return False


def missing_type(data: dict[str]) -> bool:
    """Tells us if the type is missing, and logs the error."""

    if data.get('type') is None:
        logging.error(f"missing type - {data}")
        return True
    return False


def invalid_type(data: dict[str]) -> bool:
    """Tells us if the type is invalid, and logs the error."""

    if data['type'] not in (0, 1):
        logging.error(f"type {data['type']} is invalid - {data}")
        return True
    return False


def is_assistance(data: dict[str]) -> bool:
    """Tells us if the data is an assistance call."""

    return data.get('val') == -1 and data.get('type') == 0


def is_emergency(data: dict[str]) -> bool:
    """Tells us if the data is an emergency."""

    return data.get('val') == -1 and data.get('type') == 1


if __name__ == "__main__":

    load_dotenv()

    log_choice = get_log_arg()
    configure_log(log_choice)

    kafka_config = configure_kafka(environ)

    consumer = Consumer(kafka_config)
    consumer.subscribe([environ["TOPIC"]])

    try:
        db_conn = get_db_connection(environ)
    except OperationalError:
        logging.error("Failed to connect to database.")
        sys.exit()

    while True:
        msg = consumer.poll(1.0)

        if not msg:
            continue

        msg_data = json.loads(msg.value().decode("utf-8"))

        if missing_key(msg_data):
            continue

        if invalid_hour(msg_data):
            continue

        # if at < november_2023:
        #     logging.error(f"date {at.day}/{at.month}/{at.year} not recent enough")
        #     continue

        if invalid_site(msg_data):
            continue

        if invalid_val(msg_data):
            continue

        if msg_data['val'] == -1:
            if missing_type(msg_data):
                continue

            if invalid_type(msg_data):
                continue

        print(msg_data)

        if is_assistance(msg_data):
            assistance = get_assistances(msg_data)
            with db_conn.cursor() as cur:
                execute_values(cur, ASSISTANCES_QUERY, assistance)

        elif is_emergency(msg_data):
            emergency = get_emergencies(msg_data)
            with db_conn.cursor() as cur:
                execute_values(cur, EMERGENCIES_QUERY, emergency)

        else:
            rating = get_ratings(msg_data)
            with db_conn.cursor() as cur:
                execute_values(cur, REVIEWS_QUERY, rating)

        db_conn.commit()
