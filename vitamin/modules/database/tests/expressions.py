from unittest import TestCase
from vitamin.modules.database.fields import IntegerField
from helpers.mock import Mock
from vitamin.modules.database.model import Model
from vitamin.modules.database import PDO

pdo = PDO()

class TestExpressions(TestCase):
    
    def test_bin(self):
        field = IntegerField()
        field.Model = Model()
        field.Model.Name = "test"
        field.expressionBehaviour()
        field.Name = "id"
        self.assertEqual(str(field > 1), "test.id > 1")
        self.assertEqual(str(field == 1), "test.id = 1")
        self.assertEqual(str(field < 1), "test.id < 1")
        self.assertEqual(str(field >= 1), "test.id >= 1")
        self.assertEqual(str(field <= 1), "test.id <= 1")
        self.assertEqual(str(field != 1), "test.id != 1")
