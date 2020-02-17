import sedre

def func():
    myp = sedre.Parser(program='molpro',filename='data/test_molpro_rhf.dat')
    return myp.data['energy']['RHF']['raw']['vals'][0]
def test_answer():
    assert func() == ['-191.342257373013']