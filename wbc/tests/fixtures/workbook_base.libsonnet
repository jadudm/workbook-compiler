local derive_type(value) = if std.isBoolean(value) then 
  'boolean'
  else if std.isNumber(value) then 'integer'
  else if std.isString(value) then 'string'
  else if value == null then 'null'
  else 'UNKNOWN_TYPE';

local make_operand(value) = if std.isObject(value)
then value
else {
  node: 'operand',
  value: value,
  type: derive_type(value),
};


local make_application(fun_name, operands) = {
  node: 'application',
  name: fun_name,
  operands: std.map(make_operand, operands),
};


local named_range(name) = {
  node: 'operand',
  value: name,
  type: 'named_range',
};


local make_relative_ref(row, col) = {
  node: 'operand',
  value: {
    [if row != null then 'row']: row,
    [if col != null then 'column']: col,
  },
  type: 'relative',
};

local make_absolute_ref(row, col) = {
  node: 'operand',
  value: {
    row: row,
    column: col,
  },
  type: 'absolute',
};

local make_binop(op, lhsv, rhsv) = {
  node: 'binop',
  operator: op,
  lhs: make_operand(lhsv),
  rhs: make_operand(rhsv),
};

local make_unary_op(op, rand) = {
  node: 'unaryop',
  operator: op,
  rand: make_operand(rand),
};

{
  derive_type:: derive_type,
  op:: make_operand,
  make_operand:: make_operand,
  app:: make_application,
  make_application:: make_application,
  make_relative_ref:: make_relative_ref,
  make_absolute_ref:: make_absolute_ref,
  named_range:: named_range,
  binop:: make_binop,
  unaryop:: make_unary_op,
}
