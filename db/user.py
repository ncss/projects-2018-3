import sqlite3
from .dbObject import DbObject

class User(DbObject):
    def __init__(self,username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'):
        self.id = 0
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
        conn = sqlite3.connect('squadify.db')
        cur = conn.cursor()
        all = cur.execute('SELECT * FROM users')
        return all
    
    @staticmethod
    def get_by_username(username : str):
        ''' This method gets a user by their username. 
        arguments
            - username(str)
        returns
            user object (User)
        '''
        conn = sqlite3.connect('squadify.db')
        cur = conn.cursor()
        user = cur.execute('SELECT * FROM users WHERE username=?;',(username,))
        cur.close()
        conn.close()
        return user
    
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
        conn = sqlite3.connect('squadify.db')
        cur = conn.cursor()
        new_user = cur.execute('INSERT INTO users VALUES (username=?, password=?, description=?, location=?, birthdate=?, image=?);',(username,password,description,location,birthdate,image))
        cur.close()
        conn.close()
        return new_user
        
    
    