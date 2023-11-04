from parser.reader import read
from parser.workbook import Workbook
from parser.sheet import Sheet
from parser.range import Range, LinearRange, DegenerateRange
from parser.cell import Cell, Contents
from base.exceptions import ParseException

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
    if 'contents' in c:
        print("CONTENTS", c)
    return Cell(c['notation'], 
                c['row'], 
                c['column'], 
                contents=parse_contents(c) if 'contents' in c else None)


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
    
    elif rng['type'] == 'linear_range':
        requires = ['length']
        for r in requires:
            if r not in rng:
                raise ParseException(f'missing key {r} in linear_range')
        return LinearRange(name = rng['name'], 
                           start_cell = parse_cell(rng['start']),
                           length = rng['length'],
                           header = rng.get('header', None),
                           contents = [parse_contents(c) for c in rng.get('contents', None)],
                           direction = rng.get('direction', 'down')
                           )
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
