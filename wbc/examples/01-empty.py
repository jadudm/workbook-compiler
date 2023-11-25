from wbc import Workbook, render

if __name__ in "__main__":
    wb = Workbook("Empty Workbook", [])
    render(wb).save("01-empty.xlsx")