"""
Database setup utilities: parsing input data,
creating tables, and populating database.
"""
import os
from contextlib import contextmanager
from datetime import datetime
from typing import Dict

from racing_report_api.config import DATA_DIR

from .logger import logger
from .models import Driver, RaceInfo, db


def create_tables(db) -> None:
    """
    Creates database tables.
    """
    logger.info("Starting database table creation...")

    try:
        with db:
            db.create_tables([Driver, RaceInfo], safe=True)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error(f"Error during table creation: {e}")
        raise


def parse_abbreviations(filepath: str) -> Dict[str, Dict[str, str]]:
    """
    Parses abbreviations file into a dictionary.

    Args:
        filepath (str): Path to the abbreviations.txt file.

    Returns:
        Dict[str, Dict[str, str]]: Mapping of abbreviation to name and team.
    """
    logger.info(f"Starting to parse abbreviations file: {filepath}")
    abbreviations = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('_')
                if len(parts) == 3:
                    abbr, name, team = parts
                    abbreviations[abbr] = {'name': name, 'team': team}
                else:
                    logger.warning(
                        f"Invalid line format (skipped): {line.strip()}"
                    )
        logger.info(f"Successfully parsed {len(abbreviations)} abbreviations.")
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error while parsing abbreviations file {filepath}: {e}")
        raise
    return abbreviations


def parse_log_file(filepath: str) -> Dict[str, datetime]:
    """
    Parses start.log or end.log into a dictionary.

    Args:
        filepath (str): Path to log file.

    Returns:
        Dict[str, datetime]: Mapping of abbreviation to timestamp.
    """
    logger.info(f"Starting to parse log file: {filepath}")
    log_data = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    if len(line) < 4:
                        logger.warning(f"Line too short (skipped): '{line}'")
                        continue
                    abbr = line[:3]
                    timestamp = line[3:]
                    try:
                        log_data[abbr] = datetime.strptime(
                            timestamp, "%Y-%m-%d_%H:%M:%S.%f")
                    except ValueError:
                        logger.warning(
                            f"Invalid timestamp format for line (skipped): "
                            f"'{line}'"
                        )
                else:
                    logger.warning("Empty line encountered and skipped.")
        logger.info(
            f"Successfully parsed {len(log_data)} log entries from file: "
            f"{filepath}"
        )
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error while parsing log file {filepath}: {e}")
        raise
    return log_data


def populate_drivers(db) -> None:
    """
    Populates Driver table using data from abbreviations.txt.

    Args:
        db: Database connection object.
    """
    abbreviations_path = os.path.join(DATA_DIR, 'abbreviations.txt')
    logger.info(
        f"Starting to populate 'Driver' table from '{abbreviations_path}'."
    )

    try:
        abbreviations = parse_abbreviations(abbreviations_path)
        logger.debug(f"Parsed {len(abbreviations)} abbreviations from file.")

        if not abbreviations:
            logger.warning(
                "No abbreviations found in the file."
                "File may be empty or corrupted."
            )

        with db:
            for abbr, info in abbreviations.items():
                driver, created = Driver.get_or_create(
                    abbreviation=abbr,
                    defaults={'full_name': info['name'], 'team': info['team']}
                )
                if created:
                    logger.debug(
                        f"Added new driver: {abbr} - {info['name']} "
                        f"({info['team']})"
                    )
                else:
                    logger.debug(f"Driver already exists: {abbr}")

        logger.info(
            f"{len(abbreviations)} drivers processed "
            f"(added or already in database).")

    except Exception as e:
        logger.error(f"Failed to populate 'Driver' table: {e}")
        raise


def populate_race_info(db, log_file_name: str, time_field_name: str) -> None:
    """
    Populates RaceInfo table using data from corresponding
    log file (start.log or end.log).

    Args:
        db: Database connection.
        log_file_name (str): Name of the log file ('start.log' or 'end.log').
        time_field_name (str): Field name in the model
        for storing time ('start_time' or 'end_time').
    """
    log_data = parse_log_file(os.path.join(DATA_DIR, log_file_name))
    logger.info(f"Start populating RaceInfo with data from {log_file_name}.")

    with db:
        for abbr, time_value in log_data.items():
            try:
                driver = Driver.get(Driver.abbreviation == abbr)

                race_time_record, created = RaceInfo.get_or_create(
                    driver=driver,
                    event='Monaco 2018 Grand Prix',
                    session='Qualification',
                    date='2018-05-24',
                    defaults={time_field_name: time_value}
                )

                if not created:
                    setattr(race_time_record, time_field_name, time_value)
                    race_time_record.save()
                    logger.debug(
                        f"Updated {time_field_name} for driver {abbr} "
                        f"with time {time_value}."
                    )
                else:
                    logger.debug(
                        f"Created new RaceTime for driver {abbr} "
                        f"with {time_field_name}: {time_value}."
                    )

            except Driver.DoesNotExist:
                logger.warning(
                    f"Driver with abbreviation '{abbr}' not found. "
                    f"Skipping entry."
                )
            except Exception as e:
                logger.error(f"Error processing driver {abbr}: {e}")
                raise

    logger.info(
        f"{len(log_data)} records processed (added or updated) "
        f"for field {time_field_name}."
    )


@contextmanager
def database_connection(db):
    """
    Context manager for managing database connection.

    Args:
        db: Database connection object.
    """
    logger.info("Connecting to the database...")
    db.connect()
    logger.info("Database connection established.")
    try:
        yield
    finally:
        db.close()
        logger.info("Database connection closed.")


def main() -> None:
    """
    Main function to initialize database, create tables,
    and populate them with data.
    """
    logger.info("Starting database setup...")

    try:
        with database_connection(db):
            create_tables(db)
            populate_drivers(db)
            populate_race_info(db, 'start.log', 'start_time')
            populate_race_info(db, 'end.log', 'end_time')
        race_start_count = (
            RaceInfo.select()
            .where(RaceInfo.start_time.is_null(False)).count()
        )
        race_end_count = (
            RaceInfo.select()
            .where(RaceInfo.end_time.is_null(False)).count()
        )
        logger.info(
            "Database fully populated: "
            f"{Driver.select().count()} drivers, "
            f"{race_start_count} race_start records, "
            f"{race_end_count} race_end records."
        )
        logger.info("Database setup completed successfully.")
    except Exception as e:
        logger.critical(f"Unexpected error during database setup: {e}")
        raise


if __name__ == '__main__':
    main()
