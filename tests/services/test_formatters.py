import xml.etree.ElementTree as ET

from REST_API_report_of_Monaco_2018_Racing.services.formatters import \
    convert_to_xml


def test_xml_conversion_basic():
    sample_data = {
        "race": "Monaco 2018 Grand Prix",
        "results": [
            {"position": 1, "driver": "Lewis Hamilton", "team": "MERCEDES"}
        ]
    }
    xml_output = convert_to_xml(sample_data)
    root = ET.fromstring(xml_output)

    assert root.find("race").text == "Monaco 2018 Grand Prix"
    assert root.find("results/entry/position").text == "1"
    assert root.find("results/entry/driver").text == "Lewis Hamilton"
    assert root.find("results/entry/team").text == "MERCEDES"


def test_xml_conversion_with_none():
    sample_data = {
        "race": "Test Grand Prix",
        "winner": None
    }
    xml_output = convert_to_xml(sample_data)
    root = ET.fromstring(xml_output)

    assert root.find("race").text == "Test Grand Prix"
    assert root.find("winner").text == "N/A"


def test_xml_conversion_with_booleans():
    sample_data = {
        "is_finished": True,
        "has_errors": False
    }
    xml_output = convert_to_xml(sample_data)
    root = ET.fromstring(xml_output)

    assert root.find("is_finished").text == "true"
    assert root.find("has_errors").text == "false"


def test_xml_conversion_with_numbers():
    sample_data = {
        "lap_time": 1.234,
        "laps_completed": 58
    }
    xml_output = convert_to_xml(sample_data)
    root = ET.fromstring(xml_output)

    assert root.find("lap_time").text == "1.234"
    assert root.find("laps_completed").text == "58"


def test_xml_conversion_nested_dict():
    sample_data = {
        "race": "Nested Test",
        "metadata": {
            "season": 2023,
            "circuit": "Monaco"
        }
    }
    xml_output = convert_to_xml(sample_data)
    root = ET.fromstring(xml_output)

    assert root.find("race").text == "Nested Test"
    assert root.find("metadata/season").text == "2023"
    assert root.find("metadata/circuit").text == "Monaco"


def test_xml_conversion_empty_list():
    sample_data = {
        "race": "Monaco 2018 Grand Prix",
        "results": []
    }
    xml_output = convert_to_xml(sample_data)
    root = ET.fromstring(xml_output)

    assert root.find("race").text == "Monaco 2018 Grand Prix"
    assert root.find("results") is not None


def test_xml_conversion_empty_dict():
    sample_data = {}
    xml_output = convert_to_xml(sample_data)
    root = ET.fromstring(xml_output)

    assert root.tag == "report"
    assert len(root) == 0


def test_xml_conversion_invalid_input():
    sample_data = 12345
    try:
        convert_to_xml(sample_data)
        assert False, "Expected TypeError"
    except TypeError:
        pass
