from wbc import (
    Cell,
    Contents,
    LinearRange,
    Sheet,
    Workbook, 
    render
)

if __name__ in "__main__":
    lr1 = LinearRange("Numbers", 
                      Cell("RC", 1, 1), 
                      3,
                      header = None, 
                      contents = [Contents(1), Contents(2), Contents(3)])
    sh1 = Sheet("First Sheet", [lr1])
    wb = Workbook("Empty Workbook", [sh1])
    render(wb).save("03-ranges.xlsx")