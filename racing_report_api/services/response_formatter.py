"""
This module provides response formatting utilities for
the race report API, including standardized error responses
and formatting of race reports into JSON or XML formats.
"""
import json
from dataclasses import asdict

from flask import Response, jsonify, make_response

from ..services.formatters import convert_to_xml
from ..services.report_service import RaceReport
from .request_parsers import FORMAT_JSON, FORMAT_XML


def error_response(message: str, status_code: int) -> Response:
    """
    Creates a standardized error response.

    Args:
        message (str): Error message.
        status_code (int): HTTP status code.

    Returns:
        Response: JSON response containing the error message.
    """
    return make_response(jsonify({"error": message}), status_code)


def format_race_response(
        report_data: RaceReport, format_type: str
) -> Response:
    """
    Formats the race report into JSON or XML response.

    Args:
        report_data (RaceReport): The structured race report data.
        format_type (str): Desired format ('json' or 'xml').

    Returns:
        Response: Flask response object with the formatted data.
    """
    ordered_report = {
        "race": report_data.race,
        "date": report_data.date,
        "results": [
            asdict(result) for result in report_data.results
        ],
        "disqualified": [
            asdict(result) for result in report_data.disqualified
        ],
    }

    if format_type == FORMAT_JSON:
        return Response(
            json.dumps(ordered_report, indent=4, ensure_ascii=False),
            mimetype="application/json"
        )
    elif format_type == FORMAT_XML:
        return Response(
            convert_to_xml(report_data), mimetype="application/xml"
        )

    return error_response("Unsupported format", 400)
