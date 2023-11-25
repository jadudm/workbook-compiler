# Using the compiler

Once installed, the `wbc` command (workbook compiler) is the main entrypoint into transforming JSonnet documents into workbooks. To begin, these examples mirror the examples provided in the [guide](guide.md).

## An empty workbook

The simplest, empty workbook we can compose looks like this:

```jsonnet
{
    type: "workbook",
    name: "Empty workbook",
    sheets: [],
}
```

When saved in a file called `01-empty.jsonnet`, and the compiler is invoked:

```
wbc 01-empty.jsonnet 01-empty.xlsx
```

this produces an empty workbook just like when the Python library is called directly. A workbook must have a `type` and `name`, in addition to a (possibly empty) list of `sheets``.

## A single sheet

Adding a single sheet is a composition similar to the Python code:

```
{
    type: "workbook",
    name: "Empty workbook",
    sheets: [
        {
            type: "sheet",
            name: "First sheet",
            ranges: [],
        },
    ],
}
```

A sheet object must have a `type` and a `name`, as well as a (possibly empty) list of `ranges`.

## Adding a named range


```
{
    type: "workbook",
    name: "Empty workbook",
    sheets: [
        {
            type: "sheet",
            name: "First sheet",
            ranges: [{
                type: "linear_range",
                name: "numbers",
                start: { type: "cell", notation: "RC", row: 1, column: 1 },
                length: 3,
                header: null,
                contents: [
                    { type: "contents", value: 1 },
                    { type: "contents", value: 2 },
                    { type: "contents", value: 3 },
                ],
            }],
        },
    ],
}
```

This is starting to get verbose.

### You could construct workbooks this way...

It is possible to construct workbooks as JSonnet or JSON documents, and compile them into workbooks. Using the `render_jsonnet` and `render_json` entrypoints into the library are where you would begin with this path. However, if you are going to generate JSonnet representations of workbooks, there is an easier way than doing so than expressing the objects directly.

## An easier way

The library includes a set of JSonnet libraries for composing workbooks. These libraries are where a significant amount of expressive power resides. Specifically, if you are going to compose static workbook definitions to be compiled into workbooks, then you *must* use these libraries; they simplify workbook authoring as well as provide a set of checks and balances to help you construct correct workbooks.

Using the support library, the JSonnet document above can be simplified to the following:

```
local C = import '../fixtures/lib/constructors.libsonnet';

C.Workbook(
  'Empty workbook',
  [
    C.Sheet(
      'First Sheet',
      [
        C.LinearRange('numbers',
                      C.Cell('RC', 1, 1),
                      3,
                      contents=[
                        C.Contents(3),
                        C.Contents(5),
                        C.Contents(8),
                      ],),
      ],
    ),
  ],
)
```

The support library provides a wide range of constructors that help you "do the right thing" while building a document. More importantly, all of the features of JSonnet exist for naming values (e.g. a named style), mapping over values, etc. The value of the support library is even more obvious when it becomes time to specify validations and functions. The JSonnet code looks almost exactly like an Excel function, is rendered correctly into JSON, and can then be reliably parsed by `wbc` and rendered out as functions that Excel can execute.
