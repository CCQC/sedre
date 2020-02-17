import sedre
import unittest

class look_forTestCase(unittest.TestCase):
	def test1(self):
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
		o = test_parser.look_for('Lorem')
		self.assertEqual(o,['Lorem'])

	def test2(self):
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
		o = test_parser.look_for('lit')
		self.assertEqual(o,['lit','lit','lit'])

if __name__ == "__main__":
	unittest.main()
