from base.exceptions import ParseException
from .cell import Cell, Contents

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

class LinearRange(Range):
    VALID_DIRECTIONS = ['down', 'right']
    def __init__(self, name: str, start_cell : Cell, length: int, header: Contents = None, direction: str = 'down'):
        # Construct the end_cell from the offset.
        # Then, set the notation to be the same as the start cell.
        # Construct as RC to save on construction complexity.
        if header:
            self.header = Cell('RC', start_cell.row, start_cell.column, contents=header)
        else:
            self.header = None

        if direction == 'down':
            # This offset is because we need to be inclusive of the first cell if 
            # there is no header. That is, R1C1 -> R10C1 is length 10. With a header in R1C1, 
            # We then want R1C1->R11C1, where the values are in R2C1->R11C1. 
            offset = 0 if header else -1
            end_cell = Cell('RC', start_cell.offset_row(length+offset), start_cell.column)
            end_cell.notation = start_cell.notation

        elif direction == 'right':
            offset = 0 if header else -1
            end_cell = Cell('RC', start_cell.row, start_cell.offset_column(length+offset))
            end_cell.notation = start_cell.notation
        
        self.direction = direction

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

    def __eq__(self, other):
        if isinstance(other, Range):
            return (self.start == other.start) and (self.end == other.end)
        else:
            return False
    
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

def _test_is_linear_range():
    assert LinearRange('alice', Cell('RC', 1, 1), 100)
    assert LinearRange('clarice', Cell('A1', 100, 'C'), 2000)
    assert LinearRange('elphaba', Cell('A1', 100, 'C'), 200, direction='right')
    assert LinearRange('frankie', Cell('A1', 100, 'C'), 200, direction='down')
    assert LinearRange('georgi', Cell('A1', 100, 'C'), 200, 
                       header=Contents("hi"), 
                       direction='right')

def _test_range_equality():
    lr1 = LinearRange('alice', Cell('RC', 1, 1), 100)
    r1 = Range('range', 'bob', Cell('RC', 1, 1), Cell('RC', 1, 100))
    r2 = LinearRange('clarice', Cell('RC', 100, 3), 1000)
    dr1 = DegenerateRange('dauntless', Cell('RC', 1, 1))
    assert lr1 == lr1 
    assert r1 == r1
    assert r2 == r2
    assert dr1 == dr1
    assert lr1 != r1
    assert lr1 != r2
    assert lr1 != dr1

if __name__ == '__main__':
    _test_is_linear_range()
    _test_range_equality()