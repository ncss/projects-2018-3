from .dbObject import DbObject
from .user import User
from .squad import Squad
import sqlite3


class SquadMembers(DbObject):
    columns = ['squadname', 'username', 'status']
    table_name = 'squad_members'

    def __init__(self, squadname='game', username='james', status=0):
        self.id = 0
        self.squadname = squadname
        self.username = username
        self.status = status 
        
    # TODO def get_by_user()

    @staticmethod
    def get_all(squadname : str):
        '''  This method gets all usernames of the users in a specific squad.
        
        argument
            -squadname (str)
        
        returns
            list of user objects (list)
            
        '''
        return SquadMembers.get_by_column('squadname', squadname)  
        
    @classmethod
    def get_by_status(cls, status : int, squadname : str):
        ''' This method gets all users of the same status in a specific squad
        
        arguments
            -status (int)
            -squadname (str)
        
        returns
            list of user objects (list)
        '''
        conn = cls.get_connection()
        cur = conn.cursor()
        #cur.execute('''SELECT * FROM squad_members WHERE status = ? AND squadname = ?''',(status,squadname))
        cur.execute("""SELECT username FROM squad_members WHERE squadname = ? AND status = ?;""",(squadname, status))
        members = []
        while True:
            row = cur.fetchone()
            if not row:
                break
            members.append(User.get_by_username(row[0]))
        return members
         
    
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
