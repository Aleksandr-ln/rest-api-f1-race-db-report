"""
Defines the RaceReportResource API endpoint for
serving race reports in JSON or XML format.
"""
from flask import Response
from flask_restful import Resource
from REST_API_report_of_Monaco_2018_Racing.services.report_service import \
    get_race_report
from REST_API_report_of_Monaco_2018_Racing.services.request_parsers import \
    parse_request
from REST_API_report_of_Monaco_2018_Racing.services.response_formatter import \
    format_race_response


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
        report_data = get_race_report()

        return format_race_response(report_data, request_params.format)
