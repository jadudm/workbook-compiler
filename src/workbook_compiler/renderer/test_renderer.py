import openpyxl as pxl

from parser.parser import parse
from renderer.render import render, normalize
from parser.workbook import Workbook

def run_test(file):
    w = parse(file)
    r = render(w)
    r.save(f"{normalize(w.name)}.xlsx")
    assert isinstance(r, pxl.Workbook)

def test_simple():
    run_test("fixtures/simple.jsonnet")
def test_filled():
    run_test("fixtures/filled.jsonnet")
