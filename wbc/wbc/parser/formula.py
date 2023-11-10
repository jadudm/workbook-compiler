from dotmap import DotMap
from typing import List, Union
from wbc.parser.exceptions import ParseException
from wbc.parser.util import (
    check_type,
)


TYPES = DotMap()
TYPES.null = "null"
TYPES.integer = "integer"
TYPES.string = "string"
TYPES.boolean = "boolean"
TYPES.named_range = "named_range"


class Operand:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __eq__(self, other):
        return (
            isinstance(other, Operand)
            and self.type == other.type
            and self.value == other.value
        )

    def __str__(self):
        if self.type == "null":
            return ""
        elif self.type == "integer":
            return f"{self.value}"
        elif self.type == "boolean":
            return "1" if self.value == True else "0"
        elif self.type == "string":
            return f'"{self.value}"'
        elif self.type == "named_range":
            return self.value

    def __repr__(self):
        # return "Operand(type=%r, value=%r)".format(self.type, self.value)
        return self.__str__()


class BinOp:
    def __init__(self, operator, lhs: Operand, rhs: Operand):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return (
            isinstance(other, BinOp)
            and self.operator == other.operator
            and self.lhs == other.lhs
            and self.rhs == other.rhs
        )

    def __str__(self):
        return f"({self.lhs}{self.operator}{self.rhs})"

    def __repr__(self):
        # return "BinOp(op=%r, lhs=%r, rhs=%r)".format(self.operator, self.lhs, self.rhs)
        return self.__str__()


class Application:
    def __init__(self, name: str, operands: List[Union[Operand, BinOp]]):
        self.name = name
        for o in operands:
            if not (isinstance(o, Operand) or isinstance(o, BinOp)):
                raise ParseException(f"{o} is not of type Operand in Application")
        self.operands = operands

    def __eq__(self, other):
        ops_equal = list(map(lambda a, b: a == b, self.operands, other.operands))
        return (
            isinstance(other, Application)
            and self.name == other.name
            and all(ops_equal)
        )

    def __str__(self):
        operands = ", ".join(list(map(str, self.operands)))
        return f"{self.name}({operands})"

    def __repr__(self):
        # return "Application(name=%r, operands=%r)".format(self.name, self.operands)
        return self.__str__()

class Formula():
    def __init__(self, node):
        if isinstance(node, Application) or isinstance(node, BinOp):
            self.node = node
        else:
            raise ParseException("formulas may only contain Applications or BinOps")
    
    def __eq__(self, other):
        return (isinstance(other, Formula)
                and self.node == other.node
                )
    
    def __str__(self):
        return f"={self.node}"

    def __repr__(self):
        return self.__str__()

def _parse_formula(node):
    if node is None:
        return None

    if check_type(node, "application", exception=False):
        return Application(node["name"], list(map(_parse_formula, node["operands"])))

    elif check_type(node, "binop", exception=False):
        return BinOp(
            node["operator"], _parse_formula(node["lhs"]), _parse_formula(node["rhs"])
        )

    elif check_type(node, "operand:null", exception=False):
        return Operand(TYPES.null, None)

    elif check_type(node, "operand:string", exception=False):
        return Operand(TYPES.string, node["value"])

    elif check_type(node, "operand:integer", exception=False):
        return Operand(TYPES.integer, node["value"])

    elif check_type(node, "operand:boolean", exception=False):
        return Operand(TYPES.boolean, node["value"])

    elif check_type(node, "operand:named_range", exception=False):
        return Operand(TYPES.named_range, node["value"])
    else:
        raise ParseException(f"no type for operand {node['value']}")

def parse_formula(node):
    return Formula(_parse_formula(node))