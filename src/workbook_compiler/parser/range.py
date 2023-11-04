from base.exceptions import ParseException
from .cell import Cell, Contents
from typing import List

class Range():
    VALID_RANGE_TYPES = ['range', 'linear_range', 'degenerate_range']

    def __init__(self, type: str, name: str, start_cell : Cell, end_cell: Cell):
        if type not in Range.VALID_RANGE_TYPES:
            raise ParseException(f"{type} is not a valid Range type")
        self.type = type
        self.name = name
        self.start = start_cell
        self.end = end_cell
    
    def __str__(self):
        base = f"[{self.name}] R{self.start.row}C{self.start.column} -> R{self.end.row}C{self.end.column}"
        return base
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, Range) and
            (self.start == other.start) and
            (self.end == other.end))

class LinearRange(Range):
    VALID_DIRECTIONS = ['down', 'right']
    def __init__(self, 
                 name: str, 
                 start_cell : Cell, 
                 length: int, 
                 header: Contents = None, 
                 contents: List[Contents] = None,
                 direction: str = 'down'):
        
        self.length = length
        self.contents = contents

        # Construct the end_cell from the offset.
        # Then, set the notation to be the same as the start cell.
        # Construct as RC to save on construction complexity.
        if header:
            self.header = Cell('RC', start_cell.row, start_cell.column, contents=header)
        else:
            self.header = None

        offset = 0 if header else -1
        self.direction = direction

        if direction == 'down':
            # This offset is because we need to be inclusive of the first cell if 
            # there is no header. That is, R1C1 -> R10C1 is length 10. With a header in R1C1, 
            # We then want R1C1->R11C1, where the values are in R2C1->R11C1.
            if header:
                start_cell.row += 1
            end_cell = Cell('RC', start_cell.offset_row(length+offset), start_cell.column)
        elif direction == 'right':
            if header:
                start_cell.column += 1
            end_cell = Cell('RC', start_cell.row, start_cell.offset_column(length+offset))
        end_cell.notation = start_cell.notation
        
        # EITHER our rows are the same, and columns are different
        # OR the rows are different, and columns are the same
        # Degenerate rows are not linear rows.
        if (start_cell.row == end_cell.row) and (start_cell.column != end_cell.column):
            super(LinearRange, self).__init__('linear_range', name, start_cell, end_cell)
        elif (start_cell.row != end_cell.row) and (start_cell.column == end_cell.column):
            super(LinearRange, self).__init__('linear_range', name, start_cell, end_cell)
        elif (start_cell.row == end_cell.row) and (start_cell.column == end_cell.column):
            raise ParseException(f"{name} is degenerate, not linear")
        else:
            raise ParseException(f"{name} is not a linear range (start {start_cell}, end {end_cell})")

    def locations(self):
        if self.direction == 'down':
            values = range(self.start.row, self.end.row + 1)
            return [Cell('RC', ndx, self.start.column, v) for ndx, v in zip(values, self.contents)]
        if self.direction == 'right':
            values = range(self.start.column, self.end.column + 1)
            return [Cell('RC', self.start.row, ndx, v) for ndx, v in zip(values, self.contents)]

    def __eq__(self, other):
        return (
            isinstance(other, LinearRange) and
            self.direction == other.direction and
            super(LinearRange, self).__eq__(other)
        )
    
    def __str__(self):
        base = super(LinearRange, self).__str__()
        addl = ""
        if self.header:
            addl += f' header: {self.header}' 
        if self.direction:
            addl += f' direction: {self.direction}'
        return base + addl


class DegenerateRange(Range):
    def __init__(self, name: str, start_cell : Cell):
        r = Range('degenerate_range', name, start_cell, start_cell)
        super(DegenerateRange, self).__init__('degenerate_range', name, start_cell, start_cell)