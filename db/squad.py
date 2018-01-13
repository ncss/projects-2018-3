from .dbObject import DbObject
from .user import User


class Squad(DbObject):
    columns = ['squadname', 'capacity', 'squad_date', 'description','location','leader']
    table_name = 'squads'
    def __init__(self, squadname='aaa', capacity=10, squad_date='15/1/2018', description='This is a squad', location='Australia', leader='James'):
        '''
        Initialiser for squad object
        '''
        self.id = None
        self.squadname = squadname #Squad names must be unique
        self.capacity = capacity
        self.creation_date = '13/1/2018'
        self.squad_date = squad_date
        self.description = description
        self.location = location
        self.leader = leader
        #self.squad_time = squad_time

    @staticmethod
    def get_all():
        ''' This gets a list of all the available squads            
        returns 
            list of squad objects (list)
        '''

        return Squad.get_by_column(1,1)

    @staticmethod
    def get_by_squadname(squadname: str):
        ''' This gets a squad by name
        arguments
            - squadname(str)
        returns 
            Squad object
        '''
        return Squad.get_by_column('squadname', squadname)[0]

    @staticmethod
    def create(squadname: str, capacity: int, squad_date:str, description: str, location: str, leader: str):
        ''' This creates a new squad
        arguments
            - squadname(str)
            - capacity(int)
            - squad_date(str)
            - description(str)
            - location(str)
            - leader(str)
			- squad_time (str)

        returns
            squad object with inserted parameters (Squad)

        '''
        new_squad = Squad(squadname, capacity, squad_date, description, location, leader)
        new_squad.save()
        return new_squad 

        