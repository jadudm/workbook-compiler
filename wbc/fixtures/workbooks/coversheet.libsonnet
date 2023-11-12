local const = import '../lib/constants.libsonnet';
local C = import '../lib/constructors.libsonnet';

local make_field(name,
                 row,
                 column,
                 header,
                 contents) =
  C.LinearRange(name,
                C.RC(row, column),
                1,
                height=60,
                direction='horizontal',
                header=C.Contents(header, style='bold_white_on_blue'),
                contents=[C.Contents(contents)]);

{
    make_field:: make_field
}