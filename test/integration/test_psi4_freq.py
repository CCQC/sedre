import sedre

def func():
    myp = sedre.Parser(program='psi4',filename='./data/psi4_freq.dat')
    return myp.data['properties']['freq']['entry']['vals'][0]

def test_answer():
    assert func() == [('2170.8264', '4139.1667', '4389.8052')]