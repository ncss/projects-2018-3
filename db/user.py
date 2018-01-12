class User:
	def __init__(self):
		self.id = "0"
		self.username = "sandy" 
		self.password = "1234"
		self.description = "sample text"
		self.location = "Sydney"
		self.birthdate = "DD/MM/YYYY"
		self.image = "image.img"
	
	@staticmethod
	def get_all():
		''' This method gets a list of all users. 
		returns	
			list of user objects (list)
		'''
		return [User()]
	
	@staticmethod
	def get_by_username(username : str):
		''' This method gets a user by their username. 
		arguments
			- username(str)
		returns
			user object (User)
		'''
		return User()
	
	