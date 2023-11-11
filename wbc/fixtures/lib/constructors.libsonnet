local Types = import 'types.libsonnet';

local Workbook(name, shs, named_styles=[]) =
  Types.Workbook {
    name: name,
    sheets: shs,
    named_styles: named_styles,
  };

local Sheet(name, rs) =
  Types.Sheet {
    name: name,
    ranges: rs,
  };

local Contents(value, style=null) =
  Types.Contents {
    value: value,
    style: style
  };

local LinearRange(
  name,
  start,
  length,
  direction='vertical',
  header=Contents(''),
  contents=[],
      ) =
  Types.LinearRange {
    name: name,
    start: start,
    length: length,
    direction: direction,
    header: header,
    contents: contents,
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

local Border(left=null,
             right=null,
             top=null,
             bottom=null,
             outline=null) = Types.Border {
  left: left,
  right: right,
  top: top,
  bottom: bottom,
  outline: outline,
};

local Side(style=null, color=null) = Types.Side + {
  style: style,
  color: color
};

local PatternFill(fill_type, start_color, end_color) = Types.PatternFill {
  fill_type: fill_type,
  start_color: start_color,
  end_color: end_color,
};

local SolidFill(color) = Types.PatternFill {
  fill_type: "solid",
  start_color: color,
  end_color: color
};

local NamedStyle(name, border=null, patt=null) = Types.NamedStyle {
  name: name,
  border: border,
  pattern_fill: patt,
};


{
  Workbook:: Workbook,
  Sheet:: Sheet,
  LinearRange:: LinearRange,
  Cell:: Cell,
  Contents:: Contents,
  RC:: RC,
  A1:: A1,
  NamedStyle:: NamedStyle,
  Border:: Border,
  Side:: Side,
  PatternFill:: PatternFill,
  SolidFill:: SolidFill
}
