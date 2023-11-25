from wbc import Workbook, Sheet, render

if __name__ in "__main__":
    sh1 = Sheet("First Sheet", [])
    wb = Workbook("Empty Workbook", [sh1])
    render(wb).save("02-sheet.xlsx")