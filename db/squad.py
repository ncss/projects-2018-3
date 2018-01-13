from .dbObject import DbObject
from .user import User

class Squad(DbObject):
    def __init__(self, name='aaa', capacity=10, event_date='15/1/2018', description='This is a squad', location='Australia', leader=0):
        '''
        Initialiser for squad object
        '''
        self.id = 0
        self.name = name #Squad names must be unique
        self.capacity = capacity
        self.creation_date = '13/1/2018'
        self.event_date = event_date
        self.description = description
        self.location = location
        self.leader = leader

    @staticmethod
    def get_all():
        ''' This gets a list of all the available squads            
        returns 
            list of squad objects (list)
        '''
        conn = sqlite3.connect('squadify.db')
        cur = conn.cursor()
        squads = cur.execute('SELECT * FROM squads;')
        cur.close()
        conn.close()
        return squads

    @staticmethod
    def get_by_name(name: str):
        ''' This gets a squad by name
        arguments
            - name(str)
        returns 
            Squad object
        '''
        
        conn = sqlite3.connect('squadify.db')
        cur = conn.cursor()
        squad = cur.execute('SELECT * FROM squads WHERE name=?;',(name,))
        cur.close()
        conn.close()
        return squad

    @staticmethod
    def create(name: str, capacity: int, event_date:str, description: str, location: str, leader: str):
        ''' This creates a new squad
        arguments
            - name(str)
            - capacity(int)
            - event_date(str)
            - description(str)
            - location(str)
            - leader(str)

        returns
            squad object with inserted parameters (Squad)

        '''
        conn = sqlite3.connect('squadify.db')
        cur = conn.cursor()
        squad = cur.execute('INSERT INTO squads VALUES(name=?, capacity=?,event_date=?,description=?,location=?,leader=?);',(name, capacity, description, location, leader))
        return Squad(name, capacity, event_date, description, location, leader) 

        