"""
Database connection setup using Peewee's SqliteDatabase.
"""
from peewee import SqliteDatabase
from REST_API_report_of_Monaco_2018_Racing.config import DATABASE_URL

db = SqliteDatabase(DATABASE_URL)


def get_db():
    if db.is_closed():
        db.connect()
    return db


def close_db():
    if not db.is_closed():
        db.close()
