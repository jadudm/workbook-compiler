local r1 = {
  name: 'alice',
  type: 'range',
  start: { notation: 'RC', column: 1, row: 1 },
  end: { notation: 'A1', column: 'A', row: 10 },
};

local r2 = {
  name: 'bob',
  type: 'linear_range',
  start: { notation: 'RC', column: 2, row: 1 },
  length: 2,
  contents: [{ value: "hi" }, { value: "bye" },],
};

{
  name: 'Filled Workbook',
  sheets: [
    {
      name: 'First sheet',
      ranges: [r1, r1, r1, r1],
    },
    {
      name: 'Second sheet',
      ranges: [r1, r2],
    },
  ],
}
