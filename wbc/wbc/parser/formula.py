from wbc.parser.exceptions import ParseException

def parse_formula(node):
    if node is None:
        return None
    if node['node'] == "application":
        rands = ",".join(map(parse_formula, node['operands']))
        application = f"{node['name']}({rands})" 
        return application
    if node['node'] == 'binop':
        operator = node['operator']
        lhs = parse_formula(node['lhs'])
        rhs = parse_formula(node['rhs'])
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
