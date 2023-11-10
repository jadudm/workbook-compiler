import re

import openpyxl as pxl
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import quote_sheetname, absolute_coordinate
from openpyxl.styles import NamedStyle, Font, Border, Side

from wbc.parser.workbook import Workbook
from wbc.parser.range import Range, LinearRange
from wbc.parser.cell import Cell
from wbc.parser.exceptions import RenderException


def normalize(s):
    s = re.sub("\\s+", "_", s)
    s = s.lower()
    return s


def add_named_range(opwb, opsh, sh, r, prepend_sheet_name=False):
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
def fill_range_values(wbcwb, opsh, r):
    if isinstance(r, LinearRange):
        r: LinearRange
        if r.header:
            wbc = opsh[r.header.as_a1()]
            wbc.value = f"{r.header.contents.value}"
        if r.contents:
            for cell in r.locations():
                cell: Cell
                wbc = opsh[cell.as_a1()]
                wbc.value = f"{cell.contents.value}"
                if r.style:
                    wbc.style = r.style
        if r.dynamic:
            m = getattr(wbcwb, "functions")
            fun = getattr(m, r.dynamic)
            for cell in r.locations():
                cell: Cell
                wbc = opsh[cell.as_a1()]
                wbc.value = fun(cell)
                if r.style:
                    wbc.style = r.style
        if r.validation:
            pass
        if r.function1:
            for cell in r.locations():
                cell: Cell
                wbc = opsh[cell.as_a1()]
                wbc.value = r.function1
                if r.style:
                    wbc.style = r.style

    elif isinstance(r, Range):
        r: Range
        # raise RenderException("cannot render Range")
        pass
    else:
        raise RenderException(f"cannot render range of type {type(r)}")


# opwb : openpxl workbook
# opsh : openpxl sheet
# wbcwb : workbook compiler Workbook
# wbcsh : Sheet
def render(wbcwb: Workbook):
    opwb = pxl.Workbook()
    for wbcsh in wbcwb.sheets:
        opsh = opwb.create_sheet(wbcsh.name)
        for r in wbcsh.ranges:
            add_named_range(opwb, opsh, wbcsh, r)
        for r in wbcsh.ranges:
            fill_range_values(wbcwb, opsh, r)
    for ns in wbcwb.named_styles:
        the_style = NamedStyle(name=ns.name)
        if ns.font:
            the_style.font = ns.font
        if ns.border:
            the_style.border = ns.border
        opwb.add_named_style(the_style)

    # If there is more than one sheet, remove the default.
    if len(opwb.sheetnames) > 1:
        opwb.remove(opwb["Sheet"])
    return opwb
