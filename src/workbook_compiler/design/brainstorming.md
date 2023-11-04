# 2023-11-04

I want to turn a textual description of a spreadsheet workbook into an actual workbook.

This suggests

```
input -> parser -> transformations -> ... -> output
```

Which... looks like a compiler to me.

## Starting at the bottom

I know I need to represent `cell`s. I'll use a JSON-like notation. Ultimately, I think I'm going to use JSonnet to represent the language, because there are tools for it, and JSON is hard to write by hand.

```
row_limit := 2^20
column_limit := 2^8
row_a1 := integer number < row_limit
column_a1 := [A-Z]{1}[A-Z]{0,1}
row_rc := integer number < row_limit
column_rc := integer < column_limit
notation_type := [A1, RC]
cell_a1 := { notation: notation_type, column: column_a1, row: row_a1 }
cell_rc := { notation: notation_type, column: column_rc, row: row_rc }
```

A `column_ref` will be a one-or-two character string composed of the letters `A` to `Z`. A `row_ref` will be an integer less than 2^20-1. This is because Excel has a limit of 1,048,576 rows. It also has a limit of 2^16 columns, but some documents suggest that `IV` is the largest column designation in A1 notation (256 columns).

That said, it seems that Excel can have a limit of 2^16 columns. So, as with most things involving Excel, it is conflicting.

I'll start with a lower limit: the `column_limit` will be 256. 

To make sure I know what kind of cell I'm dealing with, I'll also type the cell object as either `A1` or `RC`.



