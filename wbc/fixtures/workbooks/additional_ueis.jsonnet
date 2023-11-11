local const = import '../lib/constants.libsonnet';
local C = import '../lib/constructors.libsonnet';

local version = '1.0.0';

local make_field(name,
                 row,
                 column,
                 header,
                 contents) =
  C.LinearRange(name,
                C.RC(row, column),
                1,
                direction='horizontal',
                header=C.Contents(header, style='hello'),
                contents=[C.Contents(contents)]);

local coversheet = C.Sheet(
  'Coversheet',
  [
    make_field('version', 1, 1, 'Version number', version),
    make_field('auditee_uei', 2, 1, 'Auditee UEI', ''),
  ],
);

local form = C.Sheet(
  'Form',
  [],
);

local validations = C.Sheet(
  'Validations',
  [],
);

local styles = [
    C.NamedStyle(
      'hello',
      C.Border(outline=C.Side(const.BORDER.thick,
                              const.COLORS.midnightblue))
    ),
  ];

C.Workbook(
  'Additional UEIs',
  [
    coversheet,
    form,
    validations,
  ],
  named_styles=styles
)
