# Language reference

## `Workbook`


```
{
    // Required
    type: "workbook",
    name: string,
    sheets: List[Sheet]
}
```

The workbook object represents the entire workbook. It is composed of zero or more sheets.

## Sheet

```
{
    // Required
    type: "sheet",
    name: string,
    ranges: List[Range]
}
```

Sheets represent the tabbed spreadsheets in a workbook.

Sheets contain zero or more *named ranges*. All ranges go into the spreadsheets as named ranges, regardless of whether they contain constant values, are calculated dynamically, or exist only for input and validation.

## Range

```
{
    // Required
    type: "linear_range",
    name: string,
    start: Cell,
    length: integer,
    // Optional
    header: Contents,
    contents: List[Contents],
    dynamic: string,
    validation: Formula,
    function1: Formula,
    direction: string (default = "vertical")
}
```

A future version of the language may introduce other types of ranges (e.g. a two-dimensional range). 

Linear ranges (or 1-dimensional ranges) represent one or more cells in a workbook. The range is either horizontal or vertical. 

A header silently adjusts the range extent. If the range was declared "vertical" as beginning at R1C1 and has a length of 10, then the range object will be "bumped" from its original range of R1C1->R10C1 to R2C1->R11C1, with a header cell in R1C1.

The range is made up of `Cell`s. Those cells might:

* have no values assigned
* have static values assigned (e.g. `contents`)
* be populated dynamically by a Python function at compile-time (e.g. `dynamic`)
* be populated dynamically by a function at runtime (e.g. `formula1`)
* have validations attached (e.g. `validation`)

## Cell

```
{
    type: "cell",
    notation: "RC" | "A1",
    row: integer,
    column: integer | string
}
```

A `Cell` represents a single cell in a range.

A cell can either be in row/column notation (`RC`) or A1 notation (`A1`). 

The top-left corner of a sheet is R1C1 or A1, depending on the notation. The cells

```
{ type: "cell", notation: "RC", row: 1, column: 1}
```

and

```
{ type: "cell", notation: "A1", row: 1, column: "A"}
```

are considered to be equal.


RC notation is either to work with for relative references. For example, to refer to a cell one row above from the current cell, the value `R-1C0` is used. 

