from .dbObject import DbObject
from .user import User
from .squad import Squad

class Squad_Members(DbObject):

	def __init__(self, event_id_id : int, user_id : int, status : str):
		self.id = 0
		self.event_id = 0
		self.user_id = 0
		self.status = "Pending..."
	
	def get_all(event_id : int):
		'''  This method gets all usernames of the users in a specific squad.
		
		argument
			-event_id(int)
		
		returns
			list of usernames (User)
			
		'''
		return [
			User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
			User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
		]	
		
	
	