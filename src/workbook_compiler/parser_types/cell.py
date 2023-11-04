import typing
from typing import Union
from base.exceptions import ParseException


ALLOWED_NOTATIONS = ['A1', 'RC']
MAX_ROWS = 2**20
MAX_COLUMNS = 2**8

def excel_from_number(column: int) -> str:
    col_string = ''
    col_num = column
    while (col_num > 0):
         current_letter_number = (col_num - 1) % 26
         current_letter = chr(current_letter_number + 65)
         col_string = current_letter + col_string
         col_num = (col_num - (current_letter_number + 1)) // 26
    return col_string 

def number_from_excel(column: str) -> int:
    total = 0
    for ndx, letter in enumerate(column[::-1]):
        letter_val = (ord(letter) - 65) + 1
        val = letter_val * (26**ndx)
        total += val
    return total

class Cell():
    VALID_A1_COLUMNS = [excel_from_number(col) for col  in range(256)]

    # Internally, we represent the row/column as 1-indexed values
    def __init__(self, notation: str, row: int, column: Union[str, int]):
        self.notation = notation
        if notation not in ALLOWED_NOTATIONS:
            raise ParseException(f'Cell notation is not A1 or RC')
        if row >= MAX_ROWS:
            raise ParseException(f'{row} rows equals or exceeds {MAX_ROWS}')
        self.row = row
        if notation == 'RC':
            if column >= MAX_COLUMNS:
                raise ParseException(f'{column} columns equals or exceeds {MAX_COLUMNS}')
            self.column = column
        if notation == 'A1':
            if column not in Cell.VALID_A1_COLUMNS:
                raise ParseException(f'{column} not a valid A1 column')
            self.column = number_from_excel(column)

    def as_rc(self):
        return f'R{self.row}C{self.column}'
    def as_a1(self):
        return f'{excel_from_number(self.column)}{self.row}'
    
    def __str__(self):
        if self.notation == 'A1':
            return self.as_a1()
        else:
            return self.as_rc()

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.row == other.row) and (self.column == other.column)
        else:
            return False
 

def _test_excel_from_number():
    assert excel_from_number(1) == 'A'
    assert excel_from_number(255) == 'IU'

def _test_number_from_excel():
    assert number_from_excel('A') == 1
    assert number_from_excel('Z') == 26
    assert number_from_excel('AA') == 27
    assert number_from_excel('IU') == 255
    

def _test_conversion():
    # RC cells come back in __str__ as RC
    assert f"{Cell('RC', 8, 2)}" == 'R8C2'
    assert Cell('RC', 8, 2).as_a1() == 'B8'
    # A1 cells come back in __str__ as A1
    assert f"{Cell('A1', 1, 'A')}" == 'A1'
    assert Cell('A1', 22, 'AA').as_rc() == 'R22C27'

def _test_equality():
    assert Cell('A1', 1, 'A') == (Cell('A1', 1, 'A'))
    assert Cell('A1', 1, 'A') != Cell('A1', 2, 'A')
    assert Cell('RC', 1, 1) == (Cell('A1', 1, 'A'))
    assert Cell('RC', 1, 1) != Cell('A1', 2, 'A')
    assert Cell('A1', 22, 'AA') == Cell('RC', 22, 27)

    

if __name__ == '__main__':
    _test_excel_from_number()
    _test_conversion()
    _test_number_from_excel()
    _test_equality()