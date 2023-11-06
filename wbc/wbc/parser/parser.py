from wbc.parser.reader import read
from wbc.parser.workbook import Workbook
from wbc.parser.sheet import Sheet
from wbc.parser.range import Range, LinearRange, DegenerateRange
from wbc.parser.cell import Cell, Contents
from wbc.base.exceptions import ParseException


def parse_contents(c):
    if c is None:
        return None
    requires = ["value"]
    for r in requires:
        if r not in c:
            raise ParseException(f"missing key {r} in cell")
    return Contents(c["value"])

def parse_node(node):
    if node is None:
        return None
    if node['node'] == "application":
        rands = ",".join(map(parse_node, node['operands']))
        application = f"{node['name']}({rands})" 
        return application
    if node['node'] == 'binop':
        operator = node['operator']
        lhs = parse_node(node['lhs'])
        rhs = parse_node(node['rhs'])
        return f"{lhs}{operator}{rhs}"
    if node['node'] == 'operand':
        if node['value'] is None or node['type'] in ['None', 'null', 'nil']:
            return ""
        if node['type'] in ['str', 'string']:
            return f"\"{node['value']}\""
        elif node['type'] in ['int', 'integer', 'named_range']:
            return f"{node['value']}"
        elif node['type'] in ['bool', 'boolean']:
            if node['value'] == True:
                return "1"
            else:
                return "0"
        # Abs determines the type of reference:
        # 1: absolute ($A$1)
        # 2: row reference type is absolute; column reference is relative (A$1)
        # 3: row (relative); column (absolute) ($A1)
        # 4: relative (A1)
        elif node['type'] in ['absolute']:
            row = node['value'].get('row', None)
            column = node['value'].get('column', None)
            if row is None or column is None:
                raise ParseException("absolute addresses need both a row and column")
            return f"INDIRECT(ADDRESS({row},{column},1,0),0)"
        elif node['type'] in ['relative']:
            row = node['value'].get('row', "0")
            column = node['value'].get('column', "0")
            if row == "" and column  == "":
                raise ParseException("relative address must have a row or column")
            return f"INDIRECT(ADDRESS({row},{column},4,0),0)"
        else:
            raise ParseException(f"no type for operand {node['value']}")

def parse_cell(c):
    requires = ["notation", "row", "column"]
    for r in requires:
        if r not in c:
            raise ParseException(f"missing key {r} in cell")
    return Cell(
        c["notation"],
        c["row"],
        c["column"],
        contents=parse_contents(c) if "contents" in c else None,
    )


def parse_range(rng):
    requires = {
        "range": ["type", "name", "start", "end"],
        "linear_range": ["type", "name", "start", "length"],
        "degenerate_range": ["type", "name", "start"],
    }
    optional = {
        "range": [],
        "linear_range": ["header", "contents", "dynamic", "direction", "validation", "function"],
        "degenerate_range": ["header", "contents", "dynamic", "direction", "validation", "function"],
    }
    may_not_have = {"range": [], "linear_range": [
        "end"], "degenerate_range": []}
    one_of = {
        "range": [],
        "linear_range": ["contents", "function1", "dynamic"],
        "degenerate_range": ["contents", "function1", "dynamic"]
    }

    if "type" not in rng:
        raise ParseException(f"missing `type` key in range")

    for r in requires[rng["type"]]:
        if r not in rng:
            raise ParseException(f"missing key {r} in range")

    for r in optional[rng["type"]]:
        if r in rng:
            pass

    for r in may_not_have[rng["type"]]:
        if r in rng:
            raise ParseException(f"key {r} not allowed in {rng['type']} range")

    found_one = False
    for r in one_of[rng["type"]]:
        if (r in rng) and found_one:
            print(rng)
            raise ParseException(f"may only have one of {one_of[rng['type']]} in {rng['name']}")
        elif (r in rng) and not found_one:
            found_one = True

    if rng["type"] == "range":
        return Range(
            rng["type"], rng["name"], parse_cell(
                rng["start"]), parse_cell(rng["end"])
        )

    elif rng["type"] == "linear_range":
        requires = ["length"]
        for r in requires:
            if r not in rng:
                raise ParseException(f"missing key {r} in linear_range")
        if 'contents' in rng:
            contents = [parse_contents(c) for c in rng.get("contents", None)]
        else:
            contents = None
        validation = parse_node(rng.get("validation", None))
        function1 = parse_node(rng.get("function1", None))
        return LinearRange(
            name=rng["name"],
            start=parse_cell(rng["start"]),
            length=rng["length"],
            header=parse_contents(rng.get("header", None)),
            contents=contents,
            dynamic=rng.get("dynamic", None),
            validation=f"={validation}" if validation else None,
            function1=f"={function1}" if function1 else None,
            direction=rng.get("direction", "down"),
        )
    elif rng["type"] == "degenerate_range":
        if 'contents' in rng:
            contents = [parse_contents(c) for c in rng.get("contents", None)]
        else:
            contents = None
        validation = parse_node(rng.get("validation", None))
        function1 = parse_node(rng.get("function1", None))

        return DegenerateRange(name=rng["name"],
                               start=parse_cell(rng["start"]),
                               header=parse_contents(rng.get("header", None)),
                               contents=contents,
                               dynamic=rng.get("dynamic", None),
                               validation=f"={validation}" if validation else None,
                               function1=f"={function1}" if function1 else None,
                               direction=rng.get("direction", "down"),
                               )
    else:
        raise ParseException(f"unknown range {rng}")


def parse_sheet(sh):
    requires = ["name", "ranges"]
    for r in requires:
        if r not in sh:
            raise ParseException(f"missing key {r} in sheet")
    return Sheet(sh["name"], [parse_range(r) for r in sh["ranges"]])


def parse_workbook(wb):
    requires = ["name", "sheets"]
    for r in requires:
        if r not in wb:
            raise ParseException(f"missing key {r} in workbook")
    return Workbook(wb["name"], [parse_sheet(s) for s in wb["sheets"]])


def parse(file):
    obj = read(file)
    print(obj)
    return parse_workbook(obj)
