"""
This module initializes and configures the Flask application,
sets up API blueprints, integrates Swagger for API documentation,
and applies Bootstrap styling.
"""
from flasgger import Swagger
from flask import Blueprint, Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
api_bp = Blueprint('api', __name__)


def create_app():
    app = Flask(__name__)

    bootstrap.init_app(app)

    from REST_API_report_of_Monaco_2018_Racing.api import api_bp
    app.register_blueprint(api_bp)

    Swagger(app, template_file="swagger_docs.yml")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
