import sedre

def func():
	myp = sedre.Parser(program='psi4',filename='./data/test_load.dat')
	return myp.data['energy']['HF']['raw']['vals'][0][0]

def test_answer():
	assert func() == '-78.30620272588796'
	
