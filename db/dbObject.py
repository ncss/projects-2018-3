import sqlite3
connection = None

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
        a = dict(self.__dict__)
        b = dict(other.__dict__)
        del a['id']
        del b['id']
        
        return a == b 

        
    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__,self.__dict__)

    @staticmethod
    def start_database():
        global connection 
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        with open('db/schema.sql') as f: 
            cursor.executescript(f.read())
        try:
            with open('db/dummy_data.sql') as f: 
                cursor.executescript(f.read())
        except:
            print('dummy data already found, continuing')
        connection.commit()
        return cursor

    @staticmethod
    def get_connection():
        return connection

    @classmethod
    def from_row(cls, row):
        '''
        takes a <Sqlite.row> object and instantiates a DbObject based on this
        '''
        kwargs = {}
        for column in cls.columns:
            if column in row.keys():
                kwargs[column] = row[column]
        o = cls(**kwargs)
        o.id = row["rowid"]
        return o

    @classmethod
    def get_by_column(cls, column, value):
        '''
        
        '''
        cursor = connection.cursor()
        cursor.execute('''
            SELECT rowid, * FROM {} WHERE {} = ?;
            '''.format(cls.table_name, column), (value,)
        )
        rows = []
        for row in cursor.fetchall():
            rows.append(cls.from_row(row))
        return rows

    def save(self):
        '''
        if the object is new insert it into the database
        if not, update with the new values

        uses super special magic double formatttting
        '''
        cursor = connection.cursor()
        string = []
        update_string = []
        values = []
        for column in self.__class__.columns:
            values.append(getattr(self, column))
            string.append('?')
            update_string.append(column + '=?')
        
        if not self.id:
            cursor.execute('''
            INSERT INTO {} ({}) VALUES ({})
            '''.format(self.__class__.table_name,",".join(self.__class__.columns), ','.join(string)), values)
            self.id = cursor.lastrowid
        else:
            values.append(self.id)
            cursor.execute('''
            UPDATE {} SET {} WHERE rowid = ?
            '''.format(self.__class__.table_name,','.join(update_string)), values)
        connection.commit()
        return self