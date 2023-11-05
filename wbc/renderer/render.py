import re

import openpyxl as pxl
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import quote_sheetname, absolute_coordinate

from parser.workbook import Workbook
from parser.range import Range, LinearRange, DegenerateRange
from parser.cell import Cell
from base.exceptions import RenderException

def normalize(s):
    s = re.sub("\\s+", "_", s)
    s = s.lower()
    return s


def add_named_range(opwb, opsh, sh, r, prepend_sheet_name = False):
    # Add as a global named range
    range_start = r.start.as_a1()
    range_end = r.end.as_a1()
    ref = f"{quote_sheetname(opsh.title)}!{absolute_coordinate(range_start + ':' + range_end)}"
    range_name = r.name
    if prepend_sheet_name:
        range_name = normalize(f"{sh.name}_{r.name}")
    else:
        # In case a named range is duplicated on the global table
        # Automatically prepend in that case.
        for k, _ in opwb.defined_names.items():
            if r.name == k:
                range_name = normalize(f"{sh.name}_{r.name}")
    opwb.defined_names[range_name] = DefinedName(range_name, attr_text=ref)


# This asks for a list of locations from the range.
# It will create Cell objects for each location, and 
# populate it with its contents. This way, we can easily
# populate cells in the workbook from those Cell objects.
def fill_range_values(opsh, r):
    if isinstance(r, DegenerateRange):
        r: DegenerateRange
        if r.contents:
            for cell in r.locations():
                cell: Cell
                wbc = opsh[cell.as_a1()]
                wbc.value = f"{cell.contents.value}"
    elif isinstance(r, LinearRange):
        r: LinearRange
        if r.contents:
            for cell in r.locations():
                cell: Cell
                wbc = opsh[cell.as_a1()]
                wbc.value = f"{cell.contents.value}"
    elif isinstance(r, Range):
        r: Range
        # raise RenderException("cannot render Range")
        pass
    else:
        raise RenderException(f"cannot render range of type {type(r)}")

# opwb : openpxl workbook
# opsh : openpxl sheet
# wb : Workbook
# sh : Sheet
def render(wb: Workbook):
    opwb = pxl.Workbook()
    for sh in wb.sheets:
        opsh = opwb.create_sheet(sh.name)
        for r in sh.ranges:
            add_named_range(opwb, opsh, sh, r)
        for r in sh.ranges:
            fill_range_values(opsh, r)
    opwb.remove(opwb["Sheet"])
    return opwb
