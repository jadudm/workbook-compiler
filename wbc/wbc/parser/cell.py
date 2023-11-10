from typing import Union
from wbc.constants import (
    ALLOWED_NOTATIONS,
    MAX_ROWS,
    MAX_COLUMNS,
)
from wbc.parser.util import excel_from_number, number_from_excel
from wbc.parser.exceptions import ParseException
from .contents import Contents, parse_contents
from wbc.parser.util import check_type, requires_keys


class Cell:
    VALID_A1_COLUMNS = [excel_from_number(col) for col in range(MAX_COLUMNS)]

    # Internally, we represent the row/column as 1-indexed values
    def __init__(
        self,
        notation: str,
        row: int,
        column: Union[str, int],
        # Optional
        contents: Contents = None,
    ):
        self.notation = notation
        if notation not in ALLOWED_NOTATIONS:
            raise ParseException(f"Cell notation is not A1 or RC")
        if row >= MAX_ROWS:
            raise ParseException(f"{row} rows equals or exceeds {MAX_ROWS}")
        self.row = row
        if notation == "RC":
            if column >= MAX_COLUMNS:
                raise ParseException(
                    f"{column} columns equals or exceeds {MAX_COLUMNS}"
                )
            self.column = column
        if notation == "A1":
            if column not in Cell.VALID_A1_COLUMNS:
                raise ParseException(f"{column} not a valid A1 column")
            self.column = number_from_excel(column)
        if contents and isinstance(contents, Contents):
            self.contents = contents
        elif not contents:
            self.contents = Contents("")
        else:
            raise ParseException(f"{contents} is not a Contents object")

    def as_rc(self):
        return f"R{self.row}C{self.column}"

    def as_a1(self):
        return f"{excel_from_number(self.column)}{self.row}"

    def offset_row(self, v):
        return self.row + v

    def offset_column(self, v):
        return self.column + v

    def __str__(self):
        if self.notation == "A1":
            return f"{self.as_a1()}"
        else:
            return f"{self.as_rc()}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.row == other.row) and (self.column == other.column)
        else:
            return False


def parse_cell(c):
    requires_keys(c, ["type", "notation", "row", "column"])
    check_type(c, "cell")
    return Cell(
        c["notation"],
        c["row"],
        c["column"],
        contents=parse_contents(c) if "contents" in c else None,
    )
