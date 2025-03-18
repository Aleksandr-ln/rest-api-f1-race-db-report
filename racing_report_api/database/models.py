"""
This module contains ORM models for race results,
including Driver, RaceStart, and RaceEnd.
"""
from peewee import (
    AutoField, CharField, DateField, DateTimeField,
    ForeignKeyField, Model
)

from .db_connection import db


class BaseModel(Model):
    class Meta:
        database = db


class Driver(BaseModel):
    abbreviation = CharField(unique=True, max_length=3)
    full_name = CharField(max_length=50)
    team = CharField(max_length=50)

    class Meta:
        table_name = 'driver'


class RaceInfo(BaseModel):
    id = AutoField()
    driver = ForeignKeyField(Driver, on_delete='CASCADE')
    event = CharField(max_length=100)
    session = CharField(max_length=50)
    date = DateField()
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)

    class Meta:
        table_name = 'race_info'
        indexes = (
            (('driver', 'event', 'session'), True),
        )
