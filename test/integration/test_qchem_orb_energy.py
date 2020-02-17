import sedre

def orbTest():
    myp = sedre.Parser(program='qchem',filename='data/qchem_orbital_eigenvalue.dat')
    eigs = myp.data['properties']['orbitals']['alpha']['occ']['e']['vals'][0]
    return eigs

def test():
    assert orbTest() == ['-20.570',\
    '-11.346',\
    '-11.249',\
    '-1.400', \
    '-1.020', \
    '-0.805', \
    '-0.676', \
    '-0.625', \
    '-0.606', \
    '-0.562', \
    '-0.503', \
    '-0.425'] 

