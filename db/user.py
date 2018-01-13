from .dbObject import DbObject


class User(DbObject):
    columns = ['username', 'password']
    table_name = 'users'

    def __init__(self,username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'):
        self.id = None
        self.username = username
        self.password = password
        self.description = description
        self.location = location
        self.birthdate = birthdate
        self.image = image
    
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
    
    @staticmethod
    def create(username : str, password : str, description : str, location : str, birthdate : str, image : str):
        ''' This method creates a new user with its profile information
            arguments
                - username (str)
                - password (str)
                - description (str)
                - location (str)
                - birthdate (str)
                - image (str)
            returns
                user object with inserted parameters (User)
        '''
        new_user = User(username, password, description, location, birthdate, image)
        return new_user
        
    
    