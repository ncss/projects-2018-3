from user import User
import unittest

class Testing(unittest.TestCase):
	#def __init__(self):
	#	super(unittest.TestCase).__init__()
	#	pass
		
	def test_get_all(self):
		user = User()
		result = User.get_all()
		#user = User()
		self.assertEqual(result[0].username, user.username)
		
	def test_get_by_username(self):
		user = User()
		result = User.get_by_username('')
		self.assertEqual(result.username, user.username)
		
if __name__ == '__main__':
	unittest.main()