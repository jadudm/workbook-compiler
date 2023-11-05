from wbc.parser.reader import read
from wbc.parser.workbook import Workbook
from wbc.parser.sheet import Sheet
from wbc.parser.range import Range, LinearRange, DegenerateRange
from wbc.parser.cell import Cell, Contents
from wbc.base.exceptions import ParseException


def parse_contents(c):
    requires = ['value']
    for r in requires:
        if r not in c:
            raise ParseException(f'missing key {r} in cell')
    return Contents(c['value'])


def parse_cell(c):
    requires = ['notation', 'row', 'column']
    for r in requires:
        if r not in c:
            raise ParseException(f'missing key {r} in cell')
    return Cell(c['notation'],
                c['row'],
                c['column'],
                contents=parse_contents(c) if 'contents' in c else None)


def parse_range(rng):
    requires = {
        'range': ['type', 'name', 'start', 'end'],
        'linear_range': ['type', 'name', 'start', 'length'],
        'degenerate_range': ['type', 'name', 'start']
    }
    optional = {
        'range': [],
        'linear_range': ['header', 'contents', 'func', 'direction'],
        'degenerate_range': []
    }
    may_not_have = {
        'range': [],
        'linear_range': ['end'],
        'degenerate_range': []
    }

    if 'type' not in rng:
        raise ParseException(f"missing `type` key in range")

    for r in requires[rng['type']]:
        if r not in rng:
            raise ParseException(f'missing key {r} in range')

    for r in optional[rng['type']]:
        if r in rng:
            pass

    for r in may_not_have[rng['type']]:
        if r in rng:
            raise ParseException(f"key {r} not allowed in {rng['type']} range")

    if rng['type'] == 'range':
        return Range(rng['type'],
                     rng['name'],
                     parse_cell(rng['start']),
                     parse_cell(rng['end']))

    elif rng['type'] == 'linear_range':
        requires = ['length']
        for r in requires:
            if r not in rng:
                raise ParseException(f'missing key {r} in linear_range')
        return LinearRange(name=rng['name'],
                           start=parse_cell(rng['start']),
                           length=rng['length'],
                           header=rng.get('header', None),
                           contents=[parse_contents(
                               c) for c in rng.get('contents', None)],
                           direction=rng.get('direction', 'down')
                           )
    elif rng['type'] == 'degenerate_range':
        return DegenerateRange(name=rng['name'],
                               start=parse_cell(rng['start']))
    else:
        raise ParseException(f'unknown range {rng}')


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
