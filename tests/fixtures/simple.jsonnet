local r1 = {
  name: 'alice',
  type: 'range',
  start: { notation: 'RC', column: 1, row: 1 },
  end: { notation: 'A1', column: 'AB', row: 10 },
};

{
  name: 'The Workbook',
  sheets: [
    {
      name: 'First sheet',
      ranges: [r1, r1, r1, r1],
    },
    {
      name: 'Second sheet',
      ranges: [r1, r1],
    },
  ],
}
