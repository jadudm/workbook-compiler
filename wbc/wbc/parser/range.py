from wbc.parser.exceptions import ParseException
from .cell import Cell, parse_cell, Contents, parse_contents
from .formula import parse_formula, Formula
from typing import List
from wbc.parser.util import check_type, requires_keys, allowed_keys
from wbc.constants import DIRECTIONS


class Range:
    VALID_RANGE_TYPES = ["range", "linear_range"]

    def __init__(self, type: str, name: str, start: Cell, end: Cell):
        if type not in Range.VALID_RANGE_TYPES:
            raise ParseException(f"{type} is not a valid Range type")
        self.type = type
        self.name = name
        self.start = start
        self.end = end

    def __str__(self):
        base = f"{self.name}|R{self.start.row}C{self.start.column}|R{self.end.row}C{self.end.column}"
        return base

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, Range)
            and (self.start == other.start)
            and (self.end == other.end)
        )


class LinearRange(Range):
    def __init__(
        self,
        # Required
        name: str,
        start: Cell,
        length: int,
        # Optional
        header: Contents = None,
        contents: List[Contents] = None,
        width: int = None,
        height: int = None,
        dynamic: str = None,
        validation: Formula = None,
        function1: Formula = None,
        direction: str = DIRECTIONS.vertical,
        style: str = None
    ):
        self.length = length
        self.dynamic = dynamic
        self.validation = validation
        self.function1 = function1
        self.style = style
        self.width = width
        self.height = height
        
        # Construct the end_cell from the offset.
        # Then, set the notation to be the same as the start cell.
        # Construct as RC to save on construction complexity.
        if header:
            self.header = Cell("RC", start.row, start.column, contents=header)
        else:
            self.header = None

        self.direction = direction

        # Build the end_cell
        end_cell = None
        if direction == DIRECTIONS.vertical:
            # This offset is because we need to be inclusive of the first cell if
            # there is no header. That is, R1C1 -> R10C1 is length 10. With a header in R1C1,
            # We then want values in R2C1->R11C1.
            if header:
                start.row += 1
            end_cell = Cell("RC", start.offset_row(length - 1), start.column)
        elif direction == DIRECTIONS.horizontal:
            if header:
                start.column += 1
            end_cell = Cell("RC", start.row, start.offset_column(length - 1))
        end_cell.notation = start.notation
        self.end = end_cell

        # EITHER our rows are the same, and columns are different
        # OR the rows are different, and columns are the same
        if ((start.row == end_cell.row) and (start.column != end_cell.column) 
            or (start.row != end_cell.row) and (start.column == end_cell.column)
            or (start.row == end_cell.row) and (start.column == end_cell.column)):
            super(LinearRange, self).__init__("linear_range", name, start, end_cell)
        else:
            raise ParseException(
                f"{name} is not a linear range (start {start}, end {end_cell})"
            )

        # Check the length of the contents and length match.
        if contents and (len(contents) != self.__len__()):
            raise ParseException(
                f"{len(contents)} contents but {self.__len__()} cells in range"
            )
        else:
            self.contents = contents

    def locations(self):
        if self.direction == DIRECTIONS.vertical:
            values = range(self.start.row, self.end.row + 1)
            if self.contents:
                return [
                    Cell("RC", ndx, self.start.column, v)
                    for ndx, v in zip(values, self.contents)
                ]
            elif self.dynamic or self.function1 or self.validation:
                return [Cell("RC", ndx, self.start.column, "") for ndx in values]
        if self.direction == DIRECTIONS.horizontal:
            values = range(self.start.column, self.end.column + 1)
            if self.contents:
                return [
                    Cell("RC", self.start.row, ndx, v)
                    for ndx, v in zip(values, self.contents)
                ]
            elif self.dynamic or self.function1 or self.validation:
                return [Cell("RC", self.start.row, ndx, "") for ndx in values]

    def _start(self):
        return self.start

    def _end(self):
        return self.end

    def __eq__(self, other):
        return (
            isinstance(other, LinearRange)
            and self.direction == other.direction
            and super(LinearRange, self).__eq__(other)
        )

    def __len__(self):
        # Have to be inclusive of the start, so +1 to arithmetic.
        if self.direction == DIRECTIONS.vertical:
            dist = self.end.row - self.start.row + 1
        else:
            dist = self.end.column - self.start.column + 1
        return dist

    def get_start_column(self, notation="RC"):
        if notation == "RC":
            return self.start.column
        if notation == "A1":
            return self.start.get_column_as_a1()
    def get_start_row(self, notation="RC"):
        return self.start.row

    def __str__(self):
        base = super(LinearRange, self).__str__()
        addl = ""
        if self.header:
            addl += f" header: {self.header}"
        if self.direction:
            addl += f" direction: {self.direction}"
        return base + addl


def parse_linear_range(rng):
    check_type(rng, "linear_range")
    requires_keys(rng, ["type", "name", "start", "length"])
    allowed_keys(
        rng,
        ["type", "name", "start", "length"]
        + ["header", "width", "height", "contents" ] 
        + ["dynamic", "validation", "function1", "direction"],
    )

    if "contents" in rng:
        contents = [parse_contents(c) for c in rng.get("contents", None)]
    else:
        # FIXME Should this be none or []?
        contents = []
    validation = parse_formula(rng.get("validation", None))
    function1 = parse_formula(rng.get("function1", None))

    return LinearRange(
        name=rng["name"],
        start=parse_cell(rng["start"]),
        length=rng["length"],
        header=parse_contents(rng.get("header", None)),
        contents=contents,
        width=rng.get("width", None),
        height=rng.get("height", None),
        dynamic=rng.get("dynamic", None),
        validation=f"={validation}" if validation else None,
        function1=f"={function1}" if function1 else None,
        direction=rng.get("direction", DIRECTIONS.vertical),
    )


def parse_base_range(rng):
    raise ParseException("no implementation for parsing base ranges")


def parse_range(rng):
    if check_type(rng, "range", exception=False):
        return parse_base_range(rng)
    if check_type(rng, "linear_range", exception=False):
        return parse_linear_range(rng)
    else:
        raise ParseException(f"no range type found for {rng}")
