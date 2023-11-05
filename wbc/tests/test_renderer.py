import openpyxl as pxl

from wbc.parser.parser import parse
from wbc.renderer.render import render, normalize
from wbc.parser.workbook import Workbook

def run_test(file):
    w = parse(file)
    r = render(w)
    r.save(f"{normalize(w.name)}.xlsx")
    assert isinstance(r, pxl.Workbook)

def test_simple():
    run_test("tests/fixtures/simple.jsonnet")
def test_filled():
    run_test("tests/fixtures/filled.jsonnet")
def test_hortz():
    run_test("tests/fixtures/horizontal.jsonnet")
def test_uei():
    run_test("tests/fixtures/addl_ueis.jsonnet")