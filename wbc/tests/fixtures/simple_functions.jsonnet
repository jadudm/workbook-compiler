local xlsx = import 'workbook_functions.libsonnet';

local sheets = [
  {
    name: 'Cover Sheet',
    ranges: [
      {
        name: 'random_numbers',
        type: 'linear_range',
        start: { notation: 'RC', row: 1, column: 1 },
        length: 10,
        direction: 'right',
        header: { value: 'Random numbers' },
        dynamic: 'random_number',
      },
      {
        name: 'add_ten',
        type: 'linear_range',
        start: { notation: 'RC', row: 2, column: 1 },
        length: 10,
        direction: 'right',
        header: { value: 'Add 10' },
        function1: xlsx.PLUS(xlsx.named_range("random_numbers"), 10),
      },

    ],
  },
];

local workbook = {
  name: 'Simple Function Use',
  sheets: sheets,
};

{} + workbook
