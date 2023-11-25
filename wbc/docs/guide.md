# Guide

This document assumes you know Python, and are very familiar with spreadsheets. At the least, you should be familiar with the structure of spreadsheet documents (workbook, sheets, named ranges), both A1 and RC notation, formulas, and styles.

## The empty workbook

To get started, we'll compose some documents as Python programs. We'll start with the simplest workbooks, and build up from there.

The simplest workbook is the empty workbook.

```python
from wbc import Workbook, render

if __name__ in "__main__":
    wb = Workbook("Empty Workbook", [])
    render(wb).save("01-empty.xlsx")
```

This code, when run, creates a workbook object with no sheets. This workbook object can then be converted, or *rendered*, into an [openpyxl](https://openpyxl.readthedocs.io/en/stable/index.html) object. From there, it is ready to be written to a file.

## A workbook with a sheet

By default, every workbook has the sheet named `Sheet`. However, once you add a sheet of your own, that sheet is removed.

```python
from wbc import Workbook, Sheet, render

if __name__ in "__main__":
    sh1 = Sheet("First Sheet", [])
    wb = Workbook("Empty Workbook", [sh1])
    render(wb).save("02-sheet.xlsx")
```

This example creates a workbook with a single sheet which has the name `First Sheet`. The workbook constructor takes the name of the workbook overall, and then a list of `Sheet` objects.

## Adding data

All manipulation of data in the workbook is via named ranges. This is an opinionated choice; we are working from the assumption that everything should have a name, and be able to be manipulated/extracted via named range. 

```
from wbc import (
    Cell,
    Contents,
    LinearRange,
    Sheet,
    Workbook, 
    render
)

if __name__ in "__main__":
    lr1 = LinearRange("numbers", 
                      Cell("RC", 1, 1), 
                      3,
                      header = None, 
                      contents = [Contents(3), Contents(5), Contents(8)])
    sh1 = Sheet("First Sheet", [lr1])
    wb = Workbook("Empty Workbook", [sh1])
    render(wb).save("03-ranges.xlsx")
```

This example introduces three new classes: `LinearRange`, `Cell`, and `Contents`.

`Cell` objects are a foundational representation. They represent an individual cell in a spreadsheet. They carry a row and column value; when created, they can either be created in `RC` notation or `A1` notation. For example:

```
c1 = Cell("RC", 3, 5)
```

and 

```
c2 = Cell("A1", 3, "E")
```

are the same cell. It is often easiest (computationally) to work with RC notation.

Cells have contents. That content is always wrapped with a `Contents` object. Properties (alignment, styling, typeface, etc.) are attached to contents objects. Here, the contents objects are just holding the value of the cell, nothing more.

The named range is a `LinearRange`. At this time, the only kind of named range is a linear, or 1-dimenstional, range. For example, it is not possible to have a range go from cell `A1` to `C3`; that would be a two-dimenstional range. The library assumes all values are arranged into either horizontal or vertical ranges; the default is vertical.

In this example, we:

1. create a range with the name `numbers`, 
2. declare it to have a length of `3`, 
3. it has no header cell, and 
4. the contents are the numbers 3, 5, and 8. 

## From here

From here, building spreadsheets is a matter of using the sheets, ranges, and the styles offered by the `style` module to construct a workbook.

TODO: Document style examples.