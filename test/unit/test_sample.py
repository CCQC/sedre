import sedre
def fun(x):
	test_parser = sedre.Parser()
	test_parser.content['str'] =\
		"""Lorem ipsum dolor sit amet, consectetur 
		adipiscing elit, sed do eiusmod tempor incididunt 
		ut labore et dolore magna aliqua. Ut enim ad minim 
		veniam, quis nostrud exercitation ullamco laboris 
		nisi ut aliquip ex ea commodo consequat. Duis aute 
		irure dolor in reprehenderit in voluptate velit esse 
		cillum dolore eu fugiat nulla pariatur. Excepteur 
		sint occaecat cupidatat non proident, 
		sunt in culpa qui officia deserunt mollit anim 
		id est laborum."""
	o = test_parser.look_for(x)
	#self.assertEqual(o,['Lorem'])
	return o

def test_answer():
	"""
	Simple test case of sedre.Parser.look_for using lorem ipsum
	"""
	assert fun('Lorem') == ['Lorem']
