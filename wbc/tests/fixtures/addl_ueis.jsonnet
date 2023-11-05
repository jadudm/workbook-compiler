local header = {
  name: 'header',
  type: 'linear_range',
  start: { notation: 'RC', column: 1, row: 1 },
  length: 2,
  direction: 'right',
  contents: [{ value: 'Description' }, { value: 'Value' }],
};

local make_boolean(v) = if v == true then 
  { node: "operand", value: true, type: "boolean" }
  else   
  { node: "operand", value: false, type: "boolean" };

local derive_type(value) =  if std.isBoolean(value) then "boolean" 
      else if std.isNumber(value) then "integer" 
      else if std.isString(value) then "string";

local make_operand(value) = if std.isObject(value) 
  then value
  else {
  node: "operand",
  value: value,
  type: derive_type(value)

};

local make_operator(name, operands) = {
  node: "operator",
  name: name,
  operands: std.map(make_operand, operands)
};

local node = {
  node: "operator",
  name: "MOD",
  operands: [
    {
      node: "operand",
      value: 3,
      type: "string"
    },
    make_operator("AND", [true, false, 3, "hi", {
      node: "operand",
      value: "random_numbers",
      type: "named_range"
    }]),
    {
      node: "operand",
      value: 2,
      type: "integer"
    },
    {
      node: "operand",
      value: true,
      type: "bool"
    },
    {
      node: "operand",
      value: { row: 2, column: 2},
      type: "absolute"
    },
    {
      node: "operand",
      value: { row: 2, column: 2},
      type: "relative"
    },
    {
      node: "operand",
      value: "random_numbers",
      type: "named_range"
    },
  ],
};

local make_relative_ref(row, col) = {
  node: "operand",
  value: {
    [if row != null then "row"]: row,
    [if col != null then "column"]: col,
  },
  type: "relative"
};

local make_absolute_ref(row, col) = {
  node: "operand",
  value: {
    row: row, column: col
  },
  type: "absolute"
};

local addone = make_operator("SUM", [make_relative_ref(-1, null), 1]);
local addtwo = make_operator("SUM", [make_relative_ref(-2, null), 2]);
local adduei = make_operator("SUM", [
  make_relative_ref(-3, null), 
  make_absolute_ref(2, 2)]);

 
local sheets = [
  {
    name: 'Cover Sheet',
    ranges: [
      header,
      {
        name: 'auditee_uei',
        type: 'degenerate_range',
        start: { notation: 'RC', row: 2, column: 1 },
        header: { value: 'Auditee UEI' },
        dynamic: "random_uei",
        direction: 'right',
      },
      {
        name: 'random_numbers',
        type: 'linear_range',
        start: { notation: 'RC', row: 3, column: 1 },
        length: 5,
        direction: 'right',
        header: { value: 'Random numbers' },
        dynamic: "random_uei",
      },
      {
        name: 'added_numbers',
        type: 'linear_range',
        start: { notation: 'RC', row: 4, column: 1 },
        length: 5,
        direction: 'right',
        header: { value: 'Plus 1' },
        function1: addone,
      },
      {
        name: 'added_numbers_also',
        type: 'linear_range',
        start: { notation: 'RC', row: 5, column: 1 },
        length: 5,
        direction: 'right',
        header: { value: 'Plus 2' },
        function1: addtwo,
      },
      {
        name: 'add_uei',
        type: 'linear_range',
        start: { notation: 'RC', row: 6, column: 1 },
        length: 5,
        direction: 'right',
        header: { value: 'Add UEI' },
        function1: adduei,
      },
    ],
  },
];

local workbook = {
  name: 'Additional UEIs',
  sheets: sheets,
};

{} + workbook
