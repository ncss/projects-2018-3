from dbObject import DbObject
class User(DbObject):
	def __init__(self):
		self.username = "sandy" 
	
	@staticmethod
	def get_all():
		return [User()]
	
	@staticmethod
	def get_by_username(username : str):
		return User()
	
	