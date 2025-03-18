"""
Database connection setup using Peewee's SqliteDatabase.
"""
from peewee import SqliteDatabase
from racing_report_api.config import DATABASE_URL

from .logger import logger

db = SqliteDatabase(DATABASE_URL)


def get_db():
    if db.is_closed():
        db.connect()
        logger.info("Database connection opened.")
    else:
        logger.debug("Database connection already open.")
    return db


def close_db():
    if not db.is_closed():
        db.close()
        logger.info("Database connection closed.")
    else:
        logger.debug("Database connection already closed.")
