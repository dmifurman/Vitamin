from unittest import TestCase
from vitamin.modules.database.model import Model
from vitamin.modules.database.fields import IntegerField, CharField
from vitamin.modules.database.features import primary, autoinc

class ModelTest(TestCase):
    
    class Simple(Model):
        id = IntegerField(primary, autoinc)
        name = CharField()
    
    def test_creation_and_name(self):
        self.assertEqual(self.Simple.Name, "simple")
        
    def test_iteration(self):
        self.assertTrue(hasattr(self.Simple, "__iter__"))
        fields = list(self.Simple)
        self.assertEqual(fields[0].Name, "id")
        self.assertEqual(fields[1].Name, "name")

    def test_field_to_str(self):
        self.assertEqual(str(self.Simple.id), "simple.id")
        self.assertEqual(str(self.Simple.name), "simple.name")
        
    def test_simple_int_field(self):
        s = self.Simple()
        self.assertEqual(s.id, None)
        self.assertEqual(s.name, None)        
        s.id = 1
        self.assertEqual(s.id, 1)
        s.id = 1.0
        self.assertEqual(s.id, 1)
        s.id = "1"
        self.assertEqual(s.id, 1)
        def fail_test():
            nonlocal s
            s.id = "some strange value"
        self.assertRaises(ValueError, fail_test)
        
    def test_primary_addition(self):
        class NoPrim(Model):
            name = CharField()
        self.assertTrue(hasattr(NoPrim, "id"))   
             
        
