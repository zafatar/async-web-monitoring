# Database connection

import logging

import psycopg2 as driver

from src.config import settings


logger = logging.getLogger(__name__)

db_params = {
    "database": settings.POSTGRES_DB,
    "host": settings.POSTGRES_HOST,
    "port": settings.POSTGRES_PORT,
    "user": settings.POSTGRES_USER,
    "password": settings.POSTGRES_PASSWORD,
}


def connect():
    """Connect to the database"""
    try:
        conn = None
        # Try to connect to the database 3 times
        MAX_TRIES = 3
        tries = 0
        while not conn and tries < MAX_TRIES:
            conn = driver.connect(**db_params)
            tries += 1
    except driver.OperationalError as e:
        logger.error(f"DB Connection Problem: {e}")
        exit(1)

    return conn


conn = connect()
