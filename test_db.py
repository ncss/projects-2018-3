from db.user import User
from db.squad import Squad
from db.squad_members import SquadMembers
from db.dbObject import DbObject
import db.dbObject
import unittest, sqlite3

class Testing(unittest.TestCase):
    # def __init__(self):
    # 	super(unittest.TestCase).__init__()
    # 	self.connection = None

    def setUp(self):
        db.dbObject.connection = connection = sqlite3.connect(':memory:')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        with open('db/schema.sql') as f: 
            cursor.executescript(f.read())

        with open('db/dummy_data.sql') as f: 
            cursor.executescript(f.read())
    
    def test_db_object(self):
        '''
        Makes sure that __eq__ method overide works
        '''
        user1 = User()
        user2 = User()
        self.assertEqual(user1, user2)
        
    def test_user_get_all(self):
        user = User()
        result = User.get_all()
        self.assertEqual(result, [user])
        
    def test_user_get_by_username(self):
        user = User('James', 'password', 'My name is James', 'NSW', '15/1/2018')
        result = User.get_by_username('James')
        print(repr(user.password))
        print(repr(result.password))
        
        self.assertEqual(result, user)

    def test_squad_get_all(self):
        squad = Squad()
        result = Squad.get_all()
        self.assertEqual(result, [squad])

    def test_squad_get_by_squadname(self):
        squad = Squad()
        result = Squad.get_by_squadname('')
        self.assertEqual(result, squad)
        
    def test_user_create(self):
        user = User()
        result = User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png')
        self.assertEqual(user, result)
    
    def test_squad_create(self):
        squad = Squad()
        result = Squad.create(squadname='aaa', capacity=10,squad_date='15/1/2018', description='This is a squad', location='Australia', leader=User(), squad_time='12:12:12')
        self.assertEqual(squad, result)

        
    def test_squad_members_get_all(self):
        squad_members = [
            User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
            User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
        ]
        result = SquadMembers.get_all(0)
        self.assertListEqual(squad_members, result)
        
    def test_squad_members_get_by_status(self):
        squad_members = [
            User.create(username='James',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png'),
            User.create(username='Tim',password='5678',description='Hi my name is Tim',location='Syd',birthdate='DD/MM/YYYY',image='/file/imag.png')
        ]
        result = SquadMembers.get_by_status(0, 0)
        self.assertListEqual(squad_members, result)

    def test_squad_members_change_status(self):
        newmember = SquadMembers()
        status = 1
        result = newmember.change_status(0,1,0)
        self.assertEqual(result, status)
    
    def test_squad_members_apply(self):
        newmember = SquadMembers()
        status = 0
        result = newmember.apply(0,0)
        self.assertEqual(result, status)


    def test_db_save(self):
        user = User()
        user.username = 'saam'

        # user.save()
        user.password = '123456'
        user.save()
        user2 = User.get_by_column("username", user.username)
        self.assertEqual(user.id, user2[0].id)
        self.assertEqual(user.password, user2[0].password)

        user2[0].password = "hello"
        user2[0].save()

if __name__ == '__main__':
    unittest.main()