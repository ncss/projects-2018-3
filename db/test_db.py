from user import User
import unittest

class Testing(unittest.TestCase):
	#def __init__(self):
	#	super(unittest.TestCase).__init__()
	#	pass
	def test_db_object(self):
		'''
		Makes sure that __eq__ method overide works
		'''
		user1 = User()
		user2 = User() 
		self.assertEqual(user1, user2)
		
	def test_get_all(self):
		user = User()
		result = User.get_all()
		#user = User()
		self.assertListEqual([user],result)
		
	def test_get_by_username(self):
		user = User()
		result = User.get_by_username('')
		self.assertEqual(user, result)
		
if __name__ == '__main__':
	unittest.main()