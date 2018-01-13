from .dbObject import DbObject
from .user import User
from .squad import Squad

class SquadMembers(DbObject):

	def __init__(self, event_id=0, user_id=0, status=0):
		self.id = 0
		self.event_id = event_id
		self.user_id = user_id
		self.status = status 
		
		
	@staticmethod
	def get_all(event_id : int):
		'''  This method gets all usernames of the users in a specific squad.
		
		argument
			-event_id(int)
		
		returns
			list of user objects (list)
			
		'''
		return [
			User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
			User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
		]	
		
	@staticmethod
	def get_by_status(status : int, event_id : int):
		''' This method gets all users of the same status in a specific squad
		
		arguments
			-status (int)
			-event_id (int)
		
		returns
			list of user objects (list)
		'''
		return [
			User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
			User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
		]
		
	def change_status(self, user_id : int, new_status : int, event_id : int):
		''' This method changes the status of the user in a specific squad. 
		
		arguments
			-user_id(int)
			-new_status (int)
			-event_id (int)
			
		returns
			the new status (int)
		'''
		self.status = new_status
		return self.status
	
	def apply(self, event_id : int, user_id : int):
		''' This method puts in an application to become a member of a squad.
		
		arguments
			-event_id (int)
			-user_id(int)
			
		returns
			status of the application (int)
		'''
		self.status = 0
		return self.status