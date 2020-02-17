import sedre

def ParserLoad():
	myp = sedre.Parser(filename='./data/test_load.dat')
	myp.program = 'psi4'	
	myp.psi4()
	myp.load()
	return len(myp.content['list'])

def test_answer():
	assert ParserLoad() == 252
