from user import User
import unittest

class Testing(unittest.TestCase):
	#def __init__(self):
	#	super(unittest.TestCase).__init__()
	#	pass
		
	def test_get_all_users(self):
		user = User()
		result = user.get_all_users()
		#user = User()
		self.assertEqual(result[0].username, user.username)
		
if __name__ == '__main__':
	unittest.main()