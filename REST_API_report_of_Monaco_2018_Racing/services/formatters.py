"""
Provides utility functions to convert Python dictionaries and dataclass
instances into well-structured and formatted XML strings for API responses.
"""
from dataclasses import asdict, is_dataclass
from typing import Any
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring


def _serialize_value(value: Any) -> str:
    """
    Convert different Python types to string for XML representation.

    Args:
        value (Any): The value to be converted.

    Returns:
        str: The string representation of the value.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float, str)):
        return str(value)
    return "N/A"


def _dict_to_xml(parent: Element, data: Any) -> None:
    """
    Recursively converts a dictionary, list, or dataclass to XML elements.

    Args:
        parent (Element): The parent XML element.
        data (Any): The data to convert.
    """
    if is_dataclass(data):
        data = asdict(data)

    if isinstance(data, dict):
        for key, value in data.items():
            sub_element = SubElement(parent, key)
            if isinstance(value, (dict, list)):
                _dict_to_xml(sub_element, value)
            else:
                sub_element.text = _serialize_value(value)
    elif isinstance(data, list):
        for item in data:
            child = SubElement(parent, "entry")
            _dict_to_xml(child, item)
    else:
        parent.text = _serialize_value(data)


def convert_to_xml(data: Any) -> str:
    """
    Convert a dataclass instance or dictionary to a formatted XML string.

    Args:
        data (Any): A dataclass instance or dictionary to convert.

    Returns:
        str: The XML representation of the data.
    """
    if is_dataclass(data):
        data = asdict(data)

    if not isinstance(data, dict):
        raise TypeError(
            "convert_to_xml expects a dataclass instance or dictionary")

    root = Element("report")
    _dict_to_xml(root, data)
    return parseString(tostring(root)).toprettyxml()
