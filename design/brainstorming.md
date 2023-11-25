# 2023-11-04

I want to turn a textual description of a spreadsheet workbook into an actual workbook.

This suggests

```
input -> parser -> transformations -> ... -> output
```

Which... looks like a compiler to me.

## Cell: Starting at the bottom

```
python3 -m parser_types.cell
```

I know I need to represent `cell`s. I'll use a JSON-like notation. Ultimately, I think I'm going to use JSonnet to represent the language, because there are tools for it, and JSON is hard to write by hand.

```
row_limit := 2^20
column_limit := 2^8
row_a1 := integer number < row_limit
column_a1 := [A-Z]{1}[A-Z]{0,1}
row_rc := integer number < row_limit
column_rc := integer < column_limit
notation_type := "A1" | "RC"
Cell := { type: "cell", notation: notation_type, column: column_a1, row: row_a1 }
      | { type: "cell", notation: notation_type, column: column_rc, row: row_rc }

```

A `column_ref` will be a one-or-two character string composed of the letters `A` to `Z`. A `row_ref` will be an integer less than 2^20-1. This is because Excel has a limit of 1,048,576 rows. It also has a limit of 2^16 columns, but some documents suggest that `IV` is the largest column designation in A1 notation (256 columns).

That said, it seems that Excel can have a limit of 2^16 columns. So, as with most things involving Excel, it is conflicting.

I'll start with a lower limit: the `column_limit` will be 256. 

To make sure I know what kind of cell I'm dealing with, I'll also type the cell object as either `A1` or `RC`. This lets me instantiate the cells with either a RC or A1 value:

```
ca1 = Cell("A1", 1, "A")
crc = Cell("RC", 1, 1)
```

I may want to come around later and add optional properties to a cell. For now, this is a bare minimum to get started.

## Range

```
python3 -m parser_types.range
```

A Range has a type, a name, a start cell, and an end cell.

The types might be `range`, `linear_range`, or `degenerate_range`.

A range is linear because it is in one row or column. For example:

* A1:A20 is one-dimensional, and therefore linear
* A1:B20 is two-dimensional, and therefore not linear

For now, I really mostly want to work with linear ranges.

```
name_string := [A-Za-z]+[A-Za-z0-9_]*
Range := { type: "range", name: name_string, start: Cell, end: Cell}
       | { type: "linear_range", name: name_string, start: Cell, end: Cell }
       | { type: "degenerate_range", name: name_string, start: Cell }
```

For the language... I think a `LinearRange` is essentially a refinement on a `Range`. It imposes constraints that a `Range` doesn't have. I don't like, from an object perspective, that it proliferates type tags... but, that might be how this happens in a language expressed in JSonnet. 

A `degenerate_range` is a single-cell range. Internally, it becomes a range that has a start and end that are the same.

## Sheet

Sheets contain ranges.

```
Sheet := { type: "sheet", name: name_string, ranges: Range* }
```

Is it that simple? For the moment, yes.

## Workbook

Workbooks contain sheets

```
Workbook := { type: "workbook", name: name_string, sheets: Sheet* }
```

# Refinements

Ranges are going to want to have a notion of a header or title cell. That will want to be positioned at the `top`, `left`, `right`, or `bottom`. 

* Can only `linear_range`s have a header cell?
  * Should a range from A1:A10 have the header cell in A1 if the position is `top`? 
  * Or, should the header cell be A1, and the range is... A2:A11?
  * What would it mean for a linear range of A1:A10 to have a position of `left` or `right`? Or, is that an error?
  * Positions might be `start` or `end` instead.
  * If the range has a header cell, then... should the constructor allow a start, a length, and then if a header exists, the values are auto-constructed?


Cells will want some notion of formatting. Unclear whether Ranges will have formatting.

Ranges will want some notion of validation functions.

Ranges may want a notion of a fill function, so that (when generated), they are populated. This lets me create ranges of static values.

## Range refinement

This would suggest

```
name_string := [A-Za-z]+[A-Za-z0-9_]*
drection := "vertical" | "horizontal"
Range := { type: "range", name: name_string, start: Cell, end: Cell}
       | { type: "linear_range", name: name_string, start: Cell, length: int, header: Cell, direction: direction }
       | { type: "degenerate_range", name: name_string, start: Cell }
```

## Cell refinement

Now, I need a way for Cells to do more than just be a location.

```
Cell := { type: "cell", notation: notation_type, column: column_a1, row: row_a1 }
      | { type: "cell", notation: notation_type, column: column_rc, row: row_rc, properties: CellProperties }
CellProperties := { content: string, format: Format | None }
Format := ...
```