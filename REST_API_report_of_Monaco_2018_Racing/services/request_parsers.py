"""
Contains utilities for parsing and validating incoming API request
parameters for race reports, including request parsers and dataclass
encapsulation for structured data handling.
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
    return parser


def parse_request() -> ReportRequest:
    """
    Parses the incoming request arguments.

    Returns:
        ReportRequest: Parsed request parameters encapsulated in a dataclass.
    """
    args = get_base_parser().parse_args()
    return ReportRequest(format=args["format"])
