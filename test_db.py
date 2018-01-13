from db.user import User
from db.squad import Squad
from db.squad_members import SquadMembers
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
	
	def test_squad_create(self):
		squad = Squad()
		result = Squad.create(name='aaa', capacity=10, event_date='15/1/2018', description='This is a squad', location='Australia', leader=0)
		self.assertEqual(squad, result)

		
	def test_squad_members_get_all(self):
		squad_members = [
			User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
			User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
		]
		result = SquadMembers.get_all(0)
		self.assertListEqual(squad_members, result)
		
	def test_squad_members_get_by_status(self):
		squad_members = [
			User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
			User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
		]
		result = SquadMembers.get_by_status('Pending...', 0)
		self.assertListEqual(squad_members, result)

	def test_squad_members_change_status(self):
		newmember = SquadMembers()
		status = 'Approved!'
		result = newmember.change_status(0,'Approved!',0)
		self.assertEqual(result, status)
	
	def test_squad_members_apply(self):
		status = 'Pending...'
		result = SquadMembers().apply(0,0)
		self.assertEqual(result, status)

if __name__ == '__main__':
	unittest.main()