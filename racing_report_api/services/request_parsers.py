"""
Contains utilities for parsing and validating incoming API request
parameters for race reports, including request parsers and dataclass
encapsulation for structured data handling.

Expected query parameters:
- event: Name of the race event (required).
- session: Name of the session (required).
- format: Output format (json/xml), default is 'json'.
"""
from dataclasses import dataclass

from flask_restful import reqparse


@dataclass
class ReportRequest:
    """
    Represents the parsed request parameters for a race report.

    Attributes:
        format (str): The desired output format ('json' or 'xml').
    """
    event: str
    session: str
    format: str


def get_base_parser() -> reqparse.RequestParser:
    """
    Creates and configures a request parser for race report requests.

    Returns:
        reqparse.RequestParser: Configured request parser.
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        "format",
        type=str,
        choices=("json", "xml"),
        default="json",
        help="Format must be 'json' or 'xml'",
        location="args",
    )
    parser.add_argument(
        "event",
        type=str,
        required=True,
        help="Event name is required",
        location="args",
    )
    parser.add_argument(
        "session",
        type=str,
        required=True,
        help="Session name is required",
        location="args",
    )
    return parser


def parse_request() -> ReportRequest:
    """
    Parses the incoming request arguments.

    Returns:
        ReportRequest: Parsed request parameters encapsulated in a dataclass.
    """
    args = get_base_parser().parse_args()
    return ReportRequest(
        event=args["event"], session=args["session"], format=args["format"]
    )
