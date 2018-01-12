from dbObject import DbObject
class Squad(DbObject):
    def __init__(self):
        '''
        Initialiser for squad object
        '''
        self.id = 0
        self.name = 'aaa' #Squad names must be unique
        self.capacity = 10
        self.creation_date = '13/1/2018'
        self.event_date = '15/1/2018' 
        self.description = 'This is the squad'
        self.location = 'IT Lab'
        self.leader = 0

    @staticmethod
    def get_all():
        ''' This gets a list of all the available squads			
		returns 
			list of squad objects (list)
        '''
        return [Squad()] 

    @staticmethod
    def get_by_name(name: str):
        ''' This gets a squad by name
        arguments
            - name(str)
        returns 
            Squad object
        '''
        return Squad()
