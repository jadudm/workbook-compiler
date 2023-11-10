from pytest import raises
from wbc.parser.cell import Cell, parse_cell
from wbc.parser.util import excel_from_number, number_from_excel
from .exceptions import ParseException


def test_notations():
    with raises(ParseException):
        Cell("WOOGIE", 3, 5)
    with raises(ParseException):
        Cell("A1", 8, "ZZ")


def test_maxima():
    with raises(ParseException):
        Cell("RC", 3000000, 5)
    with raises(ParseException):
        Cell("RC", 100, 1000000)


def test_contents():
    with raises(ParseException):
        Cell("RC", 1, 1, "Not a contents object")


def test_internals():
    assert Cell("RC", 1, 1).__repr__() == "R1C1"
    assert Cell("RC", 1, 1) != "Not a cell"


def test_conversion():
    # RC cells come back in __str__ as RC
    assert "R8C2" in f"{Cell('RC', 8, 2)}"
    assert Cell("RC", 8, 2).as_a1() == "B8"
    # A1 cells come back in __str__ as A1
    assert "A1" in f"{Cell('A1', 1, 'A')}"
    assert Cell("A1", 22, "AA").as_rc() == "R22C27"


def test_equality():
    assert Cell("A1", 1, "A") == (Cell("A1", 1, "A"))
    assert Cell("A1", 1, "A") != Cell("A1", 2, "A")
    assert Cell("RC", 1, 1) == (Cell("A1", 1, "A"))
    assert Cell("RC", 1, 1) != Cell("A1", 2, "A")
    assert Cell("A1", 22, "AA") == Cell("RC", 22, 27)


def test_parse():
    cell_obj = {"type": "cell", "notation": "RC", "row": 1, "column": 1}
    assert Cell("RC", 1, 1) == parse_cell(cell_obj)
