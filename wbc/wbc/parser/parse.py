from wbc.parser.reader import read
from wbc.parser.workbook import parse_workbook


def parse(file):
    obj = read(file)
    return parse_workbook(obj)
