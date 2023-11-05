from wbc.parser.sheet import Sheet
from typing import List

class Workbook():
    def __init__(self, name: str, sheets: list[Sheet]):
        self.name = name
        self.sheets = sheets
    
    def __str__(self):
        return f"workbook: {self.name} sheets: {[s.name for s in self.sheets]}"

    def __repr__(self):
        return self.__str__()