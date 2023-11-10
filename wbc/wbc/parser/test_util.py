from .util import (
    check_type,
    requires_keys,
    allowed_keys,
    excel_from_number,
    number_from_excel,
)
from .exceptions import ParseException
import pytest


def test_requires_keys():
    wb = {
        "name": "Empty",
        "sheets": [
            {"name": "Alice", "ranges": [], "type": "sheet"},
            {"name": "Bob", "ranges": [], "type": "sheet"},
        ],
        "type": "workbook",
    }
    assert requires_keys(wb, ["name", "sheets"])
    assert requires_keys(wb["sheets"][0], ["name", "ranges", "type"])
    assert requires_keys(wb["sheets"][0], ["name", "type"])
    with pytest.raises(ParseException):
        requires_keys(wb["sheets"][0], ["not_a_key", "name", "ranges", "type"])


def test_check_type():
    assert check_type({"type": "workbook"}, "workbook")
    assert check_type({"type": "sheet"}, "sheet")
    with pytest.raises(ParseException):
        check_type({"type": "abc"}, "123")
    with pytest.raises(ParseException):
        check_type({}, "123")
    assert check_type({}, "123", exception=False) == False


def test_allowed_keys():
    assert allowed_keys({"a": 1, "b": 2, "c": 3}, ["a", "b", "c"]) == True
    with pytest.raises(ParseException):
        allowed_keys({"a": 1, "b": 2, "c": 3}, ["a", "b"])


def test_excel_from_number():
    assert excel_from_number(1) == "A"
    assert excel_from_number(255) == "IU"


def test_number_from_excel():
    assert number_from_excel("A") == 1
    assert number_from_excel("Z") == 26
    assert number_from_excel("AA") == 27
    assert number_from_excel("IU") == 255
