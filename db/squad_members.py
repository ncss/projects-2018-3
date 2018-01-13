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


    @classmethod
    def get_by_username(cls, squadname : str, username : str):
        connection = cls.get_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT rowid, * FROM squad_members WHERE squadname = ? AND username = ?''', (squadname, username))
        for row in cursor.fetchall():
            return cls.from_row(row)

    @classmethod
    def change_status(cls, username : str, new_status : int, squadname : str):
        ''' This method changes the status of the user in a specific squad.

        arguments
            -username(str)
            -new_status (int)
            -squadname (str)

        returns
            the new status (int)
        '''
        squad_member = cls.get_by_username(squadname, username)
        squad_member.status = new_status
        squad_member.save()

    @staticmethod
    def apply(squadname : str, username : str):
        ''' This method puts in an application to become a member of a squad.

        arguments
            -squadname (str)
            -username (str)

        returns
            status of the application (int)
        '''
        squad_member = SquadMembers(squadname, username, 0)
        squad_member.save()
        return squad_member
