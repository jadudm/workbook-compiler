local wbb = import 'workbook_base.libsonnet';
local xlsx = import 'workbook_functions.libsonnet';

local header = {
  name: 'header',
  type: 'linear_range',
  start: { notation: 'RC', column: 1, row: 1 },
  length: 2,
  direction: 'right',
  contents: [{ value: 'Description' }, { value: 'Value' }],
};

local node = {
  node: 'application',
  name: 'MOD',
  operands: [
    {
      node: 'operand',
      value: 3,
      type: 'string',
    },
    wbb.make_application('AND', [true, false, 3, 'hi', wbb.named_range('random_numbers')]),
    {
      node: 'operand',
      value: 2,
      type: 'integer',
    },
    {
      node: 'operand',
      value: true,
      type: 'bool',
    },
    {
      node: 'operand',
      value: { row: 2, column: 2 },
      type: 'absolute',
    },
    {
      node: 'operand',
      value: { row: 2, column: 2 },
      type: 'relative',
    },
    {
      node: 'operand',
      value: 'random_numbers',
      type: 'named_range',
    },
  ],
};

local addone = wbb.app('SUM', [wbb.make_relative_ref(-1, null), 1]);
local addtwo = wbb.app('SUM', [wbb.make_relative_ref(-2, null), 2]);
local adduei2 = wbb.app('SUM', [wbb.make_relative_ref(-3, null), wbb.named_range('auditee_uei')]);
local adduei = wbb.app('SUM', [xlsx.RELATIVE(-3, null), xlsx.ABSOLUTE(2, 2)]);
local adduei3 = xlsx.PLUS(10, wbb.named_range('auditee_uei'));

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
        dynamic: 'random_uei',
        direction: 'right',
      },
      {
        name: 'random_numbers',
        type: 'linear_range',
        start: { notation: 'RC', row: 3, column: 1 },
        length: 5,
        direction: 'right',
        header: { value: 'Random numbers' },
        dynamic: 'random_uei',
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
      {
        name: 'add_uei3',
        type: 'linear_range',
        start: { notation: 'RC', row: 7, column: 1 },
        length: 5,
        direction: 'right',
        header: { value: 'Add UEI 3' },
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
