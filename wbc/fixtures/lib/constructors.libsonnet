local Types = import 'types.libsonnet';

local Workbook(name, shs, named_styles=[]) =
  Types.Workbook {
    name: name,
    sheets: shs,
    "named_styles": named_styles,
  };

local Sheet(name, rs) =
  Types.Sheet {
    name: name,
    ranges: rs,
  };

local Contents(value) = 
    Types.Contents {
        "value": value
    };

local LinearRange(name,
                  start,
                  length,
                  direction='vertical',
                  header=Contents(""),
                  contents=[],
                  ) =
  Types.LinearRange {
    "name": name,
    "start": start,
    "length": length,
    "direction": direction,
    "header": header,
    "contents": contents
  };

local check_notation(v) = if (v == 'RC' || v == 'A1') then v else 'INVALID_NOTATION';

local Cell(not, r, c) =
  Types.Cell {
    notation: check_notation(not),
    row: r,
    column: c,
  };

local RC(r, c) = Cell('RC', r, c);
local A1(r, c) = Cell('A1', r, c);

local NamedStyle(name) = Types.NamedStyle + {
  "name": name
};


{
  Workbook:: Workbook,
  Sheet:: Sheet,
  LinearRange:: LinearRange,
  Cell:: Cell,
  Contents:: Contents,
  RC:: RC,
  A1:: A1,
  NamedStyle:: NamedStyle
}
