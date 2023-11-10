from typing import List
from wbc.parser.sheet import (Sheet, parse_sheet)
from wbc.parser.util import (
    check_type,
    requires_keys
    )


class Workbook:
    def __init__(self, name: str, sheets: list[Sheet]):
        self.name = name
        self.sheets = sheets

    def __str__(self):
        return f"workbook: {self.name} sheets: {[s.name for s in self.sheets]}"

    def __repr__(self):
        return self.__str__()


def parse_workbook(wb):
    requires_keys(wb, ["type", "name", "sheets"])
    check_type(wb, "workbook")
    return Workbook(wb["name"], [parse_sheet(s) for s in wb["sheets"]])

