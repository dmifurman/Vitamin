import unittest
from vitamin.modules.database.sqlbuilder import Builder
b = Builder()
def test_def(name, builder):
    def __foo(self):
        self.assertTrue(builder.create(name))
    return __foo
tests = {"test_" + x: test_def(x, b) for x in b.loader.DEFINITIONS if not x.startswith("_")}
DefinitionsTest = type("DefinitionsTest", (unittest.TestCase,), tests)
