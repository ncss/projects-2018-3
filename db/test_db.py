from user import User
from squad import Squad
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
		
	def test_user_get_all(self):
		user = User()
		result = User.get_all()
		self.assertEqual(result, [user])
		
	def test_user_get_by_username(self):
		user = User()
		result = User.get_by_username('')
		self.assertEqual(result, user)

	def test_squad_get_all(self):
		squad = Squad()
		result = Squad.get_all()
		self.assertEqual(result, [squad])

	def test_squad_get_by_name(self):
		squad = Squad()
		result = Squad.get_by_name('')
		self.assertEqual(result, squad)
		
if __name__ == '__main__':
	unittest.main()