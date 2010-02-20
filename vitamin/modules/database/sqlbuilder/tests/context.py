from unittest import TestCase
from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder.definitions import Names


class ContextTest(TestCase):
    
    def test_context(self):
        a = Context(namespace=Names.Create)
        a.flagTemp = True
        a.varDatabaseName = "test"
        def fail_test():
            nonlocal a
            a.varDatabaseName = 123
        self.assertRaises(ValueError, fail_test)
