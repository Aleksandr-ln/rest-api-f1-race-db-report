import pytest
from bs4 import BeautifulSoup
from REST_API_report_of_Monaco_2018_Racing.race_report_api import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_api_json_response(client):
    response = client.get("/api/v1/report/?format=json")
    assert response.status_code == 200
    assert response.content_type == "application/json"

    data = response.get_json()
    assert isinstance(data, dict)

    assert "race" in data
    assert "date" in data
    assert "results" in data and isinstance(data["results"], list)
    assert "disqualified" in data and isinstance(data["disqualified"], list)

    assert data["race"] == "Monaco 2018 Grand Prix - Qualification"
    assert data["date"] == "2018-05-24"


def test_api_xml(client):
    response = client.get("/api/v1/report/?format=xml")
    assert response.status_code == 200
    assert response.content_type.startswith("application/xml")

    xml_data = response.data.decode("utf-8")
    soup = BeautifulSoup(xml_data, "lxml-xml")
    assert soup.find("race") is not None
    assert soup.find("results") is not None


def test_api_invalid_format(client):
    response = client.get("/api/v1/report/?format=txt")
    assert response.status_code == 400

    json_data = response.get_json()
    assert "message" in json_data
    assert "format" in json_data["message"]
    assert json_data["message"]["format"] == "Format must be 'json' or 'xml'"


def test_api_xml_structure(client):
    response = client.get("/api/v1/report/?format=xml")
    xml_data = response.data.decode("utf-8")
    soup = BeautifulSoup(xml_data, "lxml-xml")

    assert soup.find("race").text == "Monaco 2018 Grand Prix - Qualification"
    assert soup.find("date").text == "2018-05-24"
    assert soup.find("results") is not None
    assert soup.find("disqualified") is not None
