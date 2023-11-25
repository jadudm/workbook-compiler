from wbc.parser.reader import read_jsonnet, read_json
from wbc.parser.workbook import parse_workbook


def parse_jsonnet(file):
    obj = read_jsonnet(file)
    return parse_workbook(obj)

def parse_json(file):
    obj = read_json(file)
    return parse_workbook(obj)
