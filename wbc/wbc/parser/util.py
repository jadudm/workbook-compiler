from .exceptions import ParseException


def check_type(o, type, exception=True):
    if "type" not in o:
        if exception:
            raise ParseException(f"Object does not contain key `type`")
        else:
            return False
    if o["type"] != type:
        if exception:
            raise ParseException(f"Object is not of type `{type}`")
        else:
            return False
    return True


def requires_keys(o, keys):
    for r in keys:
        if r not in o:
            raise ParseException(f"missing key {r} in sheet")
    return True


def allowed_keys(o, keys):
    for k in o.keys():
        if k not in keys:
            raise ParseException(f"key {k} not allowed in object {o}")


def excel_from_number(column: int) -> str:
    col_string = ""
    col_num = column
    while col_num > 0:
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
