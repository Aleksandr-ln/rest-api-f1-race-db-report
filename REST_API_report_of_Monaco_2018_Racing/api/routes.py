"""
Defines and registers the race report API endpoint at '/v1/report/'.
"""
from flask_restful import Api

from . import api_bp
from .race_report_resource import RaceReportResource

api = Api(api_bp)
api.add_resource(RaceReportResource, "/v1/report/")
