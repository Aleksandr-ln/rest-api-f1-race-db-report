"""
Service to generate formatted race reports based on database content.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from monaco_2018_racing.report import (
    Race, Racer, SortedRaceResults,
    format_timedelta, sort_race_results
)

from ..database.logger import logger
from ..database.models import Driver, RaceInfo


@dataclass
class RaceResult:
    """Dataclass representing a single race result."""
    position: int
    driver: str
    team: str
    lap_time: str


@dataclass
class RaceReport:
    """Dataclass representing a complete race report."""
    race: str
    date: str
    results: List[RaceResult]
    disqualified: List[RaceResult]


class ReportAdapter:
    """
    Adapter class to override file-based functions from report.py
    and replace them with database queries.
    """

    @staticmethod
    def parse_log_from_db(log_type: str) -> Dict[str, datetime]:
        """
        Fetches race start or end times from the database.

        Args:
            log_type (str): Either "start"
            or "end" to determine which log to fetch.

        Returns:
            Dict[str, datetime]: Mapping
            of driver abbreviations to their timestamps.
        """
        if log_type == "start":
            return {
                entry.driver.abbreviation: entry.start_time
                for entry in RaceInfo.select()
            }
        elif log_type == "end":
            return {
                entry.driver.abbreviation: entry.end_time
                for entry in RaceInfo.select()
            }
        else:
            raise ValueError("Invalid log type. Use 'start' or 'end'.")

    @staticmethod
    def parse_abbreviations_from_db() -> Dict[str, Race]:
        """
        Fetches driver details from the database.

        Returns:
            Dict[str, Race]: Mapping of driver abbreviations to Race objects.
        """
        return {
            driver.abbreviation: Racer(
                name=driver.full_name,
                team=driver.team
            )
            for driver in Driver.select()
        }

    @staticmethod
    def build_report_from_db() -> Dict[str, Race]:
        """
        Builds the race report directly from the database.

        Returns:
            Dict[str, Race]: Mapping of driver abbreviations to Race objects.
        """
        start_data = ReportAdapter.parse_log_from_db("start")
        end_data = ReportAdapter.parse_log_from_db("end")
        abbreviations = ReportAdapter.parse_abbreviations_from_db()

        return {
            abbr: Race(
                racer=abbreviations[abbr],
                start_time=start_data.get(abbr),
                end_time=end_data.get(abbr)
            )
            for abbr in abbreviations
        }


def format_race_results(races: List[Race], start_pos: int) -> List[RaceResult]:
    """
    Converts a list of Race objects into RaceResult dataclass instances.

    Args:
        races (List[Race]): List of Race objects.
        start_pos (int): The starting position in ranking.

    Returns:
        List[RaceResult]: A list of formatted race results.
    """
    return [
        RaceResult(
            position=position,
            driver=race.racer.name,
            team=race.racer.team,
            lap_time=format_timedelta(
                race.lap_time) if race.lap_time else "N/A"
        )
        for position, race in enumerate(races, start=start_pos)
    ]


def get_race_info(event: str, session: str) -> Optional[RaceInfo]:
    """
    Retrieves race information based on event and session.

    Args:
        event (str): Race event name.
        session (str): Session name.

    Returns:
        Optional[RaceInfo]: Race information if found, otherwise None.
    """
    try:
        race = RaceInfo.get(
            (RaceInfo.event == event) & (RaceInfo.session == session)
        )
        logger.debug(f"Race info found: {race}")
        return race
    except RaceInfo.DoesNotExist:
        logger.warning(
            f"Race info not found for event='{event}', session='{session}'")
        return None


def get_race_report(event: str, session: str) -> RaceReport:
    """
    Retrieves and formats the race report for the given event and session.

    Args:
        event (str): Race event name.
        session (str): Session name.

    Returns:
        RaceReport: The structured race report data.
    """
    logger.info(
        f"Generating race report for event='{event}', session='{session}'")

    race_info = get_race_info(event, session)

    if race_info is None:
        logger.info(
            f"No race info found for event='{event}', session='{session}'. "
            f"Returning empty report.")
        return RaceReport(
            race=f"{event} - {session}",
            date="N/A",
            results=[],
            disqualified=[]
        )

    report_data = ReportAdapter.build_report_from_db()
    sorted_results: SortedRaceResults = sort_race_results(report_data)

    return RaceReport(
        race=f"{race_info.event} - {race_info.session}",
        date=str(race_info.date),
        results=format_race_results(
            [race for _, race in sorted_results.positive_times], start_pos=1),
        disqualified=format_race_results(
            [race for _, race in sorted_results.negative_times], start_pos=16)
    )
