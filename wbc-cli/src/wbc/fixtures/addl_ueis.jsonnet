local header = {
  name: 'header',
  type: 'linear_range',
  start: { notation: 'RC', column: 1, row: 1 },
  length: 2,
  direction: 'right',
  contents: [{ value: 'Description' }, { value: 'Value' }],
};


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
        func: "random_uei",
        direction: 'right',
      },
    ],
  },
];

local workbook = {
  name: 'Additional UEIs',
  sheets: sheets,
};

{} + workbook
