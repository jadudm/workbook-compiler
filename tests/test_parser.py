from parser.parser import parse
from parser.workbook import Workbook

def test_simple():
    w = parse("fixtures/simple.jsonnet")
    assert isinstance(w, Workbook)

def test_filled():
    w = parse("fixtures/filled.jsonnet")
    assert isinstance(w, Workbook)
    