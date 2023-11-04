from base.exceptions import ParseException
from .cell import Cell

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
        return f"R{self.start.row}C{self.start.column} -> R{self.end.row}C{self.end.column}"
    
class LinearRange(Range):
    def __init__(self, name: str, start_cell : Cell, end_cell: Cell):
        r = Range('linear_range', name, start_cell, end_cell)
        # EITHER our rows are the same, and columns are different
        # OR the rows are different, and columns are the same
        # Degenerate rows are not linear rows.
        if (r.start.row == r.end.row) and (r.start.column != r.end.column):
            super(LinearRange, self).__init__('linear_range', name, start_cell, end_cell)
        elif (r.start.row != r.end.row) and (r.start.column == r.end.column):
            super(LinearRange, self).__init__('linear_range', name, start_cell, end_cell)
        elif (r.start.row == r.end.row) and (r.start.column == r.end.column):
            raise ParseException(f"{r.name} is degenerate, not linear")
        else:
            raise ParseException(f"{r.name} is not a linear range (start {r.start}, end {r.end})")
        
        def __eq__(self, other):
            if isinstance(other, Range):
                return (self.start == other.start) and (self.end == other.end)
            else:
                return False

class DegenerateRange(Range):
    def __init__(self, name: str, start_cell : Cell):
        r = Range('degenerate_range', name, start_cell, start_cell)
        super(DegenerateRange, self).__init__('degenerate_range', name, start_cell, start_cell)

def _test_is_linear_range():
    assert LinearRange('alice', Cell('RC', 1, 1), Cell('RC', 1, 100))
    assert LinearRange('clarice', Cell('RC', 100, 3), Cell('A1', 1000, 'C'))
    try:
        assert LinearRange('bob', Cell('RC', 1, 1), Cell('RC', 100, 100))
    except ParseException as pe:
        assert "bob is not a linear range" in f"{pe}"

def _test_range_equality():
    lr1 = LinearRange('alice', Cell('RC', 1, 1), Cell('RC', 1, 100))
    r1 = Range('range', 'bob', Cell('RC', 1, 1), Cell('RC', 1, 100))
    r2 = LinearRange('clarice', Cell('RC', 100, 3), Cell('A1', 1000, 'C'))
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