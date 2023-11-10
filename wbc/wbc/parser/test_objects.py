from .objects import (
    check_type,
    requires_keys
)
from .exceptions import ParseException
import pytest

wb = {
    "name": "Empty",
    "sheets": [
        {
            "name": "Alice",
            "ranges": [],
            "type": "sheet"
        },
        {
            "name": "Bob",
            "ranges": [],
            "type": "sheet"
        }
    ],
    "type": "workbook"
}


def test_check_type():
    assert check_type({'type': 'workbook'}, 'workbook')
    assert check_type({'type': 'sheet'}, 'sheet')
    with pytest.raises(ParseException):
        check_type({'type': 'abc'}, '123')


def test_requires_keys():
    assert requires_keys(wb, ['name', 'sheets'])
    assert requires_keys(wb['sheets'][0], ['name', 'ranges', 'type'])
    assert requires_keys(wb['sheets'][0], ['name', 'type'])
    with pytest.raises(ParseException):
        requires_keys(wb['sheets'][0], ['not_a_key', 'name', 'ranges', 'type'])
