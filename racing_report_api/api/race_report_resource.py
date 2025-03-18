"""
Defines the RaceReportResource API endpoint for
serving race reports in JSON or XML format.
"""
from flask import Response
from flask_restful import Resource
from racing_report_api.services.report_service import get_race_report
from racing_report_api.services.request_parsers import parse_request
from racing_report_api.services.response_formatter import format_race_response


class RaceReportResource(Resource):
    """
    API endpoint for retrieving race reports in JSON or XML format.
    """

    def get(self) -> Response:
        """
        Retrieve the race report in JSON or XML format.

        Returns:
            Response: JSON/XML race report or error message.
        """
        request_params = parse_request()
        report_data = get_race_report(
            request_params.event, request_params.session
        )

        return format_race_response(report_data, request_params.format)
