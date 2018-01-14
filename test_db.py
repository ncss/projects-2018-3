from db.user import User
from db.squad import Squad
from db.squad_members import SquadMembers
from db.dbObject import DbObject
from db.errors.squadDoesNotExist import SquadDoesNotExist
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
        result = User.get_all()
        self.assertEqual(len(result), 2)
        user = User('Jamesss', 'password', 'My name is James', 'NSW', '15/1/2018').save()
        result = User.get_all()
        self.assertEqual(len(result), 3)
        
    def test_user_get_by_username(self):
        user = User('james', 'password', 'My name is James', 'NSW', '15/1/2012')
        result = User.get_by_username('james')
        
        self.assertEqual(result, user)

    def test_squad_get_all(self):
        from_db = Squad.get_by_column(1,1)
        result = Squad.get_all()
        self.assertEqual(result, from_db)

    def test_squad_get_by_squadname(self):
        result = Squad.create(squadname='testjenga', capacity=10,squad_date='15/1/2018', description='This is a squad', location='Australia', leader='James', squad_time='12:00')
        from_db = Squad.get_by_column('squadname','testjenga')[0]
        result = Squad.get_by_squadname('testjenga')
        self.assertEqual(result, from_db)
        
        
    def test_user_create(self):
        result = User.create(username='TestUser',password='1234',description='Hi my name is James',location='Sydney',birthdate='DD/MM/YYYY',image='/file/img.png')
        from_db = User.get_by_column('username', 'TestUser')[0]
        self.assertEqual(from_db, result)
        
    def test_squad_create(self):
        result = Squad.create(squadname='testjenga', capacity=10,squad_date='15/1/2018', description='This is a squad', location='Australia', leader='James', squad_time='12:00')
        from_db = Squad.get_by_column('squadname', 'testjenga')[0]
        self.assertEqual(from_db, result)

        
    def test_squad_members_get_all(self):
        squad_members = SquadMembers.get_by_column('squadname', 'jenga')
        result = SquadMembers.get_all('jenga')
        self.assertListEqual(squad_members, result)

    def test_squad_members_get_by_status(self):
        squad_members = [User('jack', '123456', 'My name is Jack', 'NSW', '17/1/2018', '')]
        result = SquadMembers.get_by_status(1, 'ateam')
        self.assertListEqual(squad_members, result)

    def test_squad_members_apply(self):
        SquadMembers.apply('jenga','jack')

        result = SquadMembers.get_by_username('jenga','jack')
        self.assertEqual(result.status, 0)

        SquadMembers.change_status('jack', 2 ,'jenga')

        result = SquadMembers.get_by_username('jenga','jack')
        self.assertEqual(result.status, 2)

    def test_user_get_age(self):
        user_age = User.get_age_by_username('james')
        self.assertEqual(user_age, 5)



        
        



    def test_db_save(self):
        user = User()
        user.username = 'saam'

        #user.save()
        user.password = '123456'
        user.save()
        user2 = User.get_by_column("username", user.username)
        self.assertEqual(user.id, user2[0].id)
        self.assertEqual(user.password, user2[0].password)

        user2[0].password = "hello"
        user2[0].save()

    def test_squad_not_found(self):
        with self.assertRaises(SquadDoesNotExist):
            from_db = Squad.get_by_squadname('bbb')

    def test_user_create_update(self):
        new_user = User(username='Jamess', password='password', description='My name is James!!', location='NSW', birthdate='15/1/2018', image='/file/img.png').save()
        new_user.description = 'lol james'
        new_user.save()
        from_db = User.get_by_column('description', 'lol james')[0]
        #print(from_db)
        self.assertIsNot(from_db, new_user)
        self.assertEqual(from_db, new_user)

if __name__ == '__main__':
    unittest.main()