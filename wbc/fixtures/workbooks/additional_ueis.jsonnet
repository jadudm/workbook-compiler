local coversheet_helpers = import "coversheet.libsonnet";

local const = import '../lib/constants.libsonnet';
local C = import '../lib/constructors.libsonnet';
local S = import '../lib/styles.libsonnet';

local version = '1.0.0';
local styles = [S.white_on_black, S.bold_white_on_blue];

local long_header_message = 'This workbook contains two worksheets: '
                            + 'a coversheet (this sheet)\nand a data entry sheet.'
                            + '\n\n'
                            + 'Before submitting, please make sure the fields below are filled out.';

local coversheet = C.Sheet(
  'Coversheet',
  [
    C.LinearRange('header_cells',
                  C.RC(1, 1),
                  2,
                  direction='horizontal',
                  header=null,
                  width=60,
                  height=60,
                  contents=[
                    C.Contents('Federal Audit Clearinghouse\nfac.gov',
                               style='white_on_black',
                               wrap=true),
                    C.Contents(long_header_message,
                               style='white_on_black',
                               wrap=true),
                  ]),

    coversheet_helpers.make_field('version', 2, 1, 'Version number', version),
    coversheet_helpers.make_field('section_name', 3, 1, 'Section', 'AdditionalUeis'),
    coversheet_helpers.make_field('auditee_uei', 4, 1, 'Auditee UEI', ''),

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

C.Workbook(
  'Additional UEIs',
  [
    coversheet,
    form,
    validations,
  ],
  named_styles=styles
)
