class DbObject:
    '''
    DbObject, a super class for generic methods used by other objects
    '''
    def __init__():
        raise NotImplementedError
    
    def __eq__(self, other):
        '''
        compares the internal dictionaries of objects
        arguments:
            self, others
        returns:
            True or False
        '''
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__  == other.__dict__
