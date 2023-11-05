from wbc.parser.cell import Cell, excel_from_number, number_from_excel


def test_excel_from_number():
    assert excel_from_number(1) == "A"
    assert excel_from_number(255) == "IU"


def test_number_from_excel():
    assert number_from_excel("A") == 1
    assert number_from_excel("Z") == 26
    assert number_from_excel("AA") == 27
    assert number_from_excel("IU") == 255


def test_conversion():
    # RC cells come back in __str__ as RC
    assert "R8C2" in f"{Cell('RC', 8, 2)}"
    assert Cell("RC", 8, 2).as_a1() == "B8"
    # A1 cells come back in __str__ as A1
    assert "A1" in f"{Cell('A1', 1, 'A')}"
    assert Cell("A1", 22, "AA").as_rc() == "R22C27"


def test_equality():
    assert Cell("A1", 1, "A") == (Cell("A1", 1, "A"))
    assert Cell("A1", 1, "A") != Cell("A1", 2, "A")
    assert Cell("RC", 1, 1) == (Cell("A1", 1, "A"))
    assert Cell("RC", 1, 1) != Cell("A1", 2, "A")
    assert Cell("A1", 22, "AA") == Cell("RC", 22, 27)
