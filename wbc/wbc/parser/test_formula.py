from .exceptions import ParseException
from .formula import (
    parse_formula,
    _parse_formula,
    Application,
    BinOp,
    Formula,
    Operand,
    TYPES,
)

operands = [
    ({"type": "operand:null"}, Operand(TYPES.null), ""),
    ({"type": "operand:integer", "value": 3}, Operand(TYPES.integer, 3), "3"),
    (
        {"type": "operand:integer", "value": 358358358},
        Operand(TYPES.integer, 358358358),
        "358358358",
    ),
    (
        {"type": "operand:string", "value": "HELO"},
        Operand(TYPES.string, "HELO"),
        '"HELO"',
    ),
    ({"type": "operand:boolean", "value": True}, Operand(TYPES.boolean, True), "1"),
]

applications = [
    (
        {"type": "application", "name": "SUM", "operands": []},
        Formula(Application("SUM", [])),
        "=SUM()",
    ),
    (
        {
            "type": "application",
            "name": "BOB",
            "operands": [
                {"type": "operand:integer", "value": 3},
                {"type": "operand:integer", "value": 5},
            ],
        },
        Formula(
            Application("BOB", [Operand(TYPES.integer, 3), Operand(TYPES.integer, 5)])
        ),
        "=BOB(3, 5)",
    ),
    (
        {
            "type": "application",
            "name": "BOB",
            "operands": [
                {"type": "operand:integer", "value": 3},
                {
                    "type": "binop",
                    "operator": "+",
                    "lhs": {"type": "operand:integer", "value": 3},
                    "rhs": {"type": "operand:integer", "value": 5},
                },
            ],
        },
        Formula(
            Application(
                "BOB",
                [
                    Operand(TYPES.integer, 3),
                    BinOp("+", Operand(TYPES.integer, 3), Operand(TYPES.integer, 5)),
                ],
            )
        ),
        "=BOB(3, (3+5))",
    ),
]

binops = [
    (
        {
            "type": "binop",
            "operator": "+",
            "lhs": {"type": "operand:integer", "value": 3},
            "rhs": {"type": "operand:integer", "value": 5},
        },
        Formula(BinOp("+", Operand(TYPES.integer, 3), Operand(TYPES.integer, 5))),
        "=(3+5)",
    ),
    (
        {
            "type": "binop",
            "operator": "+",
            "lhs": {"type": "operand:integer", "value": 3},
            "rhs": {
                "type": "application",
                "name": "BOB",
                "operands": [
                    {"type": "operand:integer", "value": 3},
                    {"type": "operand:integer", "value": 5},
                ],
            },
        },
        Formula(
            BinOp(
                "+",
                Operand(TYPES.integer, 3),
                Application(
                    "BOB", [Operand(TYPES.integer, 3), Operand(TYPES.integer, 5)]
                ),
            )
        ),
        "=(3+BOB(3, 5))",
    ),
]


def test_operands():
    for op in operands:
        parsed = _parse_formula(op[0])
        assert parsed == op[1]
        assert str(op[1]) == op[2]


def test_applications():
    for app in applications:
        parsed = parse_formula(app[0])
        assert parsed == app[1]
        assert str(app[1]) == app[2]


def test_binops():
    for bo in binops:
        parsed = parse_formula(bo[0])
        assert parsed == bo[1]
        assert str(bo[1]) == bo[2]
