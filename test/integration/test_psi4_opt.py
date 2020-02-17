import sedre

def func():
    myp = sedre.Parser(program='psi4',filename='./data/test_psi4_opt.dat')
    return myp.data['properties']['opt']['iteration']['vals'][0]
def test_answer():
    assert func() == [('1', '-74.96453503', '-7.50e+01', '2.27e-02', '2.10e-02', '1.04e-01')]