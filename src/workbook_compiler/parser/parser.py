from parser.reader import read
from parser.workbook import Workbook
from parser.sheet import Sheet
from parser.range import Range, LinearRange, DegenerateRange
from parser.cell import Cell, Contents
from base.exceptions import ParseException

def parse_cell(c):
    requires = ['notation', 'row', 'column']
    for r in requires:
        if r not in c:
            raise ParseException(f'missing key {r} in cell')

    contents = None
    if 'contents' in c:
        contents = "..."
    return Cell(c['notation'], c['row'], c['column'], contents=Contents(contents))


def parse_range(rng):
    requires = ['type', 'name', 'start']
    for r in requires:
        if r not in rng:
            raise ParseException(f'missing key {r} in range')

    if rng['type'] == 'range':
        return Range(rng['type'],
                     rng['name'],
                     parse_cell(rng['start']),
                     parse_cell(rng['end']))


def parse_sheet(sh):
    requires = ['name', 'ranges']
    for r in requires:
        if r not in sh:
            raise ParseException(f'missing key {r} in sheet')
    return Sheet(sh['name'], [parse_range(r) for r in sh['ranges']])


def parse_workbook(wb):
    requires = ['name', 'sheets']
    for r in requires:
        if r not in wb:
            raise ParseException(f'missing key {r} in workbook')
    return Workbook(wb['name'], [parse_sheet(s) for s in wb['sheets']])


def parse(file):
    obj = read(file)
    return parse_workbook(obj)
