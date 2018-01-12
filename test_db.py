from db.user import User
from db.squad import Squad
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
		
	def test_user_create(self):
		user = User()
		result = User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png')
		self.assertEqual(user, result)
		
if __name__ == '__main__':
	unittest.main()