from .dbObject import DbObject
from .user import User
from .squad import Squad


class SquadMembers(DbObject):
    columns = ['squadname', 'username', 'status']
    table_name = 'squad_members'

    def __init__(self, squadname='game', username='James', status=0):
        self.id = 0
        self.squadname = squadname
        self.username = username
        self.status = status 
        
        
    @staticmethod
    def get_all(squadname : str):
        '''  This method gets all usernames of the users in a specific squad.
        
        argument
            -squadname (str)
        
        returns
            list of user objects (list)
            
        '''
        return [
            User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
            User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
        ]    
        
    @staticmethod
    def get_by_status(status : int, squadname : str):
        ''' This method gets all users of the same status in a specific squad
        
        arguments
            -status (int)
            -squadname (str)
        
        returns
            list of user objects (list)
        '''
        return [
            User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
            User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
        ]
    
    @staticmethod    
    def change_status(username : str, new_status : int, squadname : str):
        ''' This method changes the status of the user in a specific squad. 
        
        arguments
            -username(str)
            -new_status (int)
            -squadname (str)
            
        returns
            the new status (int)
        '''
        status = new_status
        return status
    
    @staticmethod
    def apply(squadname : str, username : str):
        ''' This method puts in an application to become a member of a squad.
        
        arguments
            -squadname (str)
            -username (str)
            
        returns
            status of the application (int)
        '''
        status = 0
        return status
