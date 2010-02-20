from vitamin.modules.database import PDO
from vitamin.modules.database.fields import IntegerField, CharField, \
    ForeignField
from vitamin.modules.database.features import autoinc, primary, length, default, \
    notnull
from vitamin.modules.database.model import Model
from unittest import TestCase

class User(Model):
    
    id = IntegerField(autoinc, primary)    
    name = CharField(default("John"), length(100))
    address = CharField(length(100))

class Parent(Model):
    
    id = IntegerField(autoinc, primary)
    name = CharField(length(100), notnull)

class Children(Model):
    
    id = IntegerField(autoinc, primary)    
    parent = ForeignField(Parent)   
    
pdo = PDO()
pdo.regiserModel(User)
pdo.regiserModel(Parent)
pdo.regiserModel(Children)
pdo.connect()   
    
class TestSQL(TestCase):
        
    def test_0create(self):
        User.Create().go()
        
    def test_1insert(self):
        u = User()
        u.name = "Karlson"
        u.address = "roof"
        User.Insert().instance(u).go()
        u2 = User()
        User.Insert().instance(u2).go()
        
    def test_2update(self):
        u = User()
        u.id = 1
        u.name = "Sith"
        User.Update().fields(User.name).instance(u).go()
        
    def test_3select(self):
        query = (User.Select().where(User.id > 0).single().go())
        self.assertTrue(isinstance(query, User))
        self.assertEqual(query.id, 1)
        self.assertEqual(query.name, "Sith")     
        self.assertEqual(query.address, "roof")   
        
    def test_4delete(self):
        User.Delete().where((User.id == 1) & (User.id < 3)).go()
        
    def test_5foreign(self):
        Parent.Create().go()
        Children.Create().go()
        p = Parent()
        p.name = "first"
        p.Append()
        p.name = "second"
        p.Append()
        s = Children()
        parent = Parent.Select().where(Parent.name == "first").single().go()
        s.parent = parent
        s.Append()
        s.Append()
        s.Append()
        s.Append()
        s.Append()
        childrens = parent.Foreign(Children.parent)
        self.assertTrue(len(list(childrens)) == 5)



