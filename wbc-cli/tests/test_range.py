from wbc.parser.range import Range, LinearRange, DegenerateRange
from wbc.parser.cell import Cell, Contents

def test_is_linear_range():
    assert LinearRange('alice', Cell('RC', 1, 1), 100)
    assert LinearRange('clarice', Cell('A1', 100, 'C'), 2000)
    assert LinearRange('elphaba', Cell('A1', 100, 'C'), 200, direction='right')
    assert LinearRange('frankie', Cell('A1', 100, 'C'), 200, direction='down')
    assert LinearRange('georgi', Cell('A1', 100, 'C'), 200, 
                       header=Contents("hi"), 
                       direction='right')
    assert LinearRange('heidi', Cell('A1', 100, 'C'), 200, 
                       header=Contents("byte"), 
                       direction='right')

def test_range_equality():
    lr1 = LinearRange('alice', Cell('RC', 1, 1), 100)
    r1 = Range('range', 'bob', Cell('RC', 1, 1), Cell('RC', 1, 100))
    r2 = LinearRange('clarice', Cell('RC', 100, 3), 1000)
    dr1 = DegenerateRange('dauntless', Cell('RC', 1, 1))

    lr2 = LinearRange('georgi', Cell('A1', 100, 'C'), 200, 
                       header=Contents("hi"), 
                       direction='right')
    lr3 = LinearRange('heidi', Cell('A1', 100, 'C'), 200, 
                       header=Contents("bye"), 
                       direction='right')
    lr4 = LinearRange('idina', Cell('A1', 100, 'C'), 200, 
                       header=Contents("wat"), 
                       direction='down')
    
    # [print(v) for v in [lr1, r1, r2, dr1, lr2, lr3, lr4]]

    assert lr1 == lr1 
    assert r1 == r1
    assert r2 == r2
    assert dr1 == dr1
    assert lr1 != r1
    assert lr1 != r2
    assert lr1 != dr1
    assert lr2 == lr3
    assert lr2 != lr4
    assert lr3 != lr4
