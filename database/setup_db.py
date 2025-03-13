"""
Database setup utilities: parsing input data, creating tables, and populating database.
"""
import os
from peewee import Model
from datetime import datetime
from .models import db, Driver, RaceStart, RaceEnd
from .logger import logger
from typing import Dict, Type
from contextlib import contextmanager
from REST_API_report_of_Monaco_2018_Racing.config import DATA_DIR


def create_tables() -> None:
    """
    Creates database tables.
    """
    with db:
        db.create_tables([Driver, RaceStart, RaceEnd], safe=True)
    logger.info("Tables created successfully.")


def parse_abbreviations(filepath: str) -> Dict[str, Dict[str, str]]:
    """
    Parses abbreviations file into a dictionary.

    Args:
        filepath (str): Path to the abbreviations.txt file.

    Returns:
        Dict[str, Dict[str, str]]: Mapping of abbreviation to name and team.
    """
    abbreviations = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('_')
            if len(parts) == 3:
                abbr, name, team = parts
                abbreviations[abbr] = {'name': name, 'team': team}
    return abbreviations


def parse_log_file(filepath: str) -> Dict[str, datetime]:
    """
    Parses start.log or end.log into a dictionary.

    Args:
        filepath (str): Path to log file.

    Returns:
        Dict[str, datetime]: Mapping of abbreviation to timestamp.
    """
    log_data = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                abbr = line[:3]
                timestamp = line[3:]
                log_data[abbr] = datetime.strptime(timestamp, "%Y-%m-%d_%H:%M:%S.%f")
    return log_data


def populate_drivers() -> None:
    """
    Populates Driver table using data from abbreviations.txt.
    """
    abbreviations = parse_abbreviations(os.path.join(DATA_DIR, 'abbreviations.txt'))
    for abbr, info in abbreviations.items():
        Driver.get_or_create(
            abbreviation=abbr,
            defaults={'full_name': info['name'], 'team': info['team']}
        )
    logger.info(f"{len(abbreviations)} drivers added or found in the database.")


def populate_race_times(log_file_name: str, model: Type[Model], time_field_name: str) -> None:
    """
    Populates RaceStart or RaceEnd table using data from corresponding log file.

    Args:
        log_file_name (str): Name of the log file (start.log or end.log).
        model (Type[Model]): The Peewee model to insert data into (RaceStart or RaceEnd).
        time_field_name (str): Field name in the model for storing time (start_time or end_time).
    """
    log_data = parse_log_file(os.path.join(DATA_DIR, log_file_name))
    for abbr, time_value in log_data.items():
        try:
            driver = Driver.get(Driver.abbreviation == abbr)
            model.get_or_create(
                driver=driver,
                defaults={time_field_name: time_value}
            )
        except Driver.DoesNotExist:
            logger.warning(f"Driver with abbreviation {abbr} not found.")
        except Exception as e:
            logger.error(f"Error processing {abbr}: {e}")
    logger.info(f"{len(log_data)} {'race start' if model == RaceStart else 'race end'} times added or found.")

@contextmanager
def database_connection():
    db.connect()
    try:
        yield
    finally:
        db.close()

def main() -> None:
    """
    Main function to initialize database, create tables, and populate them with data.
    """
    with database_connection():
        create_tables()
        populate_drivers()
        populate_race_times('start.log', RaceStart, 'start_time')
        populate_race_times('end.log', RaceEnd, 'end_time')
        logger.info("Database setup completed successfully.")


if __name__ == '__main__':
    main()
