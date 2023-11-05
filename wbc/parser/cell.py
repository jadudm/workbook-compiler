from typing import Union, Dict, Any
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
    # Fancy notation to reverse a string is str[::-1]
    for ndx, letter in enumerate(column[::-1]):
        letter_val = (ord(letter) - 65) + 1
        val = letter_val * (26**ndx)
        total += val
    return total

class Contents():
    def __init__(self, value, properties: Dict[str, Any] = None):
        if isinstance(value, Contents):
            raise ParseException(f"Contents cannot contain Contents")
        self.value = value
        self.properties = properties
    
    def __str__(self):
        return self.value

class Cell():
    VALID_A1_COLUMNS = [excel_from_number(col) for col in range(MAX_COLUMNS)]

    # Internally, we represent the row/column as 1-indexed values
    def __init__(self, 
                 notation: str, 
                 row: int, 
                 column: Union[str, int], 
                 contents: Contents = None):
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
        if contents and isinstance(contents, Contents):
            self.contents = contents
        elif not contents:
            self.contents = Contents("")
        else:
            raise ParseException(f'{contents} is not a Contents object')
            

    def as_rc(self):
        return f'R{self.row}C{self.column}'
    
    def as_a1(self):
        return f'{excel_from_number(self.column)}{self.row}'
    
    def offset_row(self, v):
        return self.row + v
    
    def offset_column(self, v):
        return self.column + v

    def __str__(self):
        if self.notation == 'A1':
            return f"{self.as_a1()} <- {self.contents.value}"
        else:
            return f"{self.as_rc()} <- {self.contents.value}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.row == other.row) and (self.column == other.column)
        else:
            return False