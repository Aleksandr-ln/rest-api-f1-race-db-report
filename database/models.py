"""
This module contains ORM models for race results,
including Driver, RaceStart, and RaceEnd.
"""
from peewee import Model, CharField, ForeignKeyField, DateTimeField

from .db_connection import db


class BaseModel(Model):
    class Meta:
        database = db


class Driver(BaseModel):
    abbreviation = CharField(unique=True)
    full_name = CharField()
    team = CharField()

    class Meta:
        table_name = 'driver'


class RaceStart(BaseModel):
    driver = ForeignKeyField(
        Driver, backref='race_starts', on_delete='CASCADE')
    start_time = DateTimeField()

    class Meta:
        table_name = 'racestart'


class RaceEnd(BaseModel):
    driver = ForeignKeyField(Driver, backref='race_ends', on_delete='CASCADE')
    end_time = DateTimeField()

    class Meta:
        table_name = 'raceend'
