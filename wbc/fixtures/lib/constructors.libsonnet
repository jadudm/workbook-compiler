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

local Contents(value, style=null, wrap=false) =
  Types.Contents {
    value: value,
    style: style,
    wrap: wrap
  };

local LinearRange(
  name,
  start,
  length,
  direction='vertical',
  width=null,
  height=null,
  header=Contents(''),
  contents=[],
      ) =
  Types.LinearRange {
    name: name,
    start: start,
    length: length,
    width: width,
    height: height,
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

local Font(face=null, color=null, bold=false, size=12) = Types.Font + {
  face: face,
  bold: bold,
  size: size,
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

local NamedStyle(name, border=null, font=null, fill=null) = Types.NamedStyle {
  name: name,
  border: border,
  font: font,
  pattern_fill: fill,
};


{
  A1:: A1,
  Border:: Border,
  Cell:: Cell,
  Contents:: Contents,
  Font:: Font,
  LinearRange:: LinearRange,
  NamedStyle:: NamedStyle,
  PatternFill:: PatternFill,
  RC:: RC,
  Sheet:: Sheet,
  Side:: Side,
  SolidFill:: SolidFill,
  Workbook:: Workbook,
}
