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
                    { type: "contents", value: 3 },
                    { type: "contents", value: 5 },
                    { type: "contents", value: 8 },
                ],
            }],
        },
    ],
}