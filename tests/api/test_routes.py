import pytest
from REST_API_report_of_Monaco_2018_Racing.race_report_api import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_routes_registration(app):
    assert "api" in app.blueprints
    assert any(
        rule.rule == "/api/v1/report/"
        for rule in app.url_map.iter_rules()
    )
