import sqlite3
from .dbObject import DbObject
import datetime


class User(DbObject):
    columns = ['username', 'password','description','location','birthdate','image']
    table_name = 'users'

    def __init__(self,username='james',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'):
        
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
        all_user = User.get_by_column(1,1)

        return all_user

        # conn = sqlite3.connect('squadify.db')
        # cur = conn.cursor()
        # all = cur.execute('SELECT * FROM users')
        # return all
    
    @classmethod
    def get_by_username(cls, username : str):
        ''' This method gets a user by their username. 
        arguments
            - username(str)
        returns
            user object (User)
        '''
        result = cls.get_by_column('username', username)

        user = None 

        if len(result) == 1:
            user = result[0]
        
        return user
    
    @staticmethod
    def create(username : str, password : str, description : str, location : str, birthdate : str, image : str):
        ''' This method creates a new user with its profile information and saves it to the database
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

        user = User(username, password, description, location, birthdate, image)
        user.save()
        return user
    
    @staticmethod
    def get_age_by_username(username: 'str'):
        user = User.get_by_username(username)
        birthdate = user.birthdate
        now = datetime.datetime.now()
        birth_date = birthdate.split('/')
        (day,month,year) = birth_date

        age = now.year - int(year)
        if int(month) == now.month:
            if int(day) >=  now.day:
                age -= 1
        elif int(month) > now.month:
            age -= 1
                
        return age
    
    