local wbb = import 'workbook_base.libsonnet';

local INDIRECT(ref, rc) = {
  node: 'application',
  name: 'INDIRECT',
  operands: std.map(wbb.make_operand, [ref, rc]),
};

local ADDRESS(row, col, abs, rc, sheet) = {
  node: 'application',
  name: 'ADDRESS',
  operands: if sheet != null then
    std.map(wbb.make_operand, [row, col, abs, rc, sheet])
  else std.map(wbb.make_operand, [row, col, abs, rc]),
};

local ABSOLUTE(row, col) = INDIRECT(ADDRESS(row, col, 1, 0, null), 0);
local RELATIVE(row, col) = INDIRECT(ADDRESS(row, col, 4, 0, null), 0);

local PLUS(a, b) = wbb.binop('+', a, b);

wbb + {
  ABSOLUTE:: ABSOLUTE,
  ADDRESS:: ADDRESS,
  INDIRECT:: INDIRECT,
  RELATIVE:: RELATIVE,
  PLUS:: PLUS,
}
