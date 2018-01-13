from .dbObject import DbObject
from .user import User
from .squad import Squad


class SquadMessages(DbObject):
    columns = ['squadname', 'sender_username', 'message', 'time_sent']
    table_name = 'squad_messages'

    def __init__(self, squadname='game', sender_username='James', message='Hi', time_sent='05:00'):
        self.id = 0
        self.squadname = squadname
        self.sender_username = sender_username
        self.message = message
        self.time_sent = time_sent

    @classmethod
    def get_by_squadname(cls, squadname : str):
        ''' This method gets all squad members by their squad name.
        arguments
            - squadname(str)
        returns
            list of squad message object (squadmessage)
        '''
        result = cls.get_by_column('squadname', squadname)

        return result

    @classmethod
    def get_most_recent_5(cls, squadname):
        connection = cls.get_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT rowid, * FROM squad_messages WHERE squadname=? ORDER BY time_sent LIMIT 5;''', (squadname,))
        rows = []
        for row in cursor.fetchall():
            rows.append(cls.from_row(row))
        return rows


    @staticmethod
    def create(squadname : str, sender_username : str, message : str, time_sent : str):
        ''' This method creates a new message with its sending information and saves it to the database
            arguments
                - squadname (str)
                - sender_username (str)
                - message (str)
                - time_sent (str)
            returns
                all messages
        '''

        message = SquadMessages(squadname, sender_username, message, time_sent)
        message.save()
        return message
