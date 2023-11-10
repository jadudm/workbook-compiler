from typing import List
from pprint import pformat
from wbc.parser.sheet import Sheet, parse_sheet
from wbc.parser.util import check_type, requires_keys
from wbc.parser.style import (
    NamedStyle,
    parse_named_style
    )

class Workbook:
    def __init__(self, name: str, 
                 sheets: List[Sheet],
                 named_styles: List[NamedStyle]=[]
                 ):
        self.name = name
        self.sheets = sheets
        self.named_styles = named_styles

    def __str__(self):
        o = {
            "type": "workbook",
            "name": self.name,
            "sheets": [str(s) for s in self.sheets],
        }
        if self.named_styles:
            o["named_styles"] = [str(ns) for ns in self.named_styles]
        return pformat(o, indent=2)

    def __repr__(self):
        return self.__str__()


def parse_workbook(wb):
    requires_keys(wb, ["type", "name", "sheets"])
    check_type(wb, "workbook")
    return Workbook(wb["name"], 
                    [parse_sheet(s) for s in wb["sheets"]],
                    named_styles = [parse_named_style(ns) 
                                    for ns 
                                    in wb.get("named_styles", [])]
                    )
