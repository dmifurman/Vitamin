import unittest
from vitamin.modules.database.sqlbuilder.constructor import Constructor, Context, \
    BuildError

class ConstructorTest(unittest.TestCase):
    
    def base(self):
        @Constructor
        def __go(reg, context):
            reg.append("1")
            return reg
        return __go
        
    
    def test_creation(self):                

        constr = self.base()
        res = constr.build()
        self.assertEqual(res, "1")
        
    def test_defines(self):
                
        constr = self.base().define("test", "test")
        self.assertEqual(constr.get("test"), "test")
        
    def test_add(self):
        
        constr = self.base()
        add = constr + constr
        res = add.build()
        self.assertEqual(res, "1 1")
        
    def test_text(self):
        
        constr = Constructor.text("test")
        add = constr + constr
        res = add.build()
        self.assertEqual(res, "test test")
        
    def test_value(self):
        
        constr = Constructor.text("test")
        constr2 = Constructor.variable("name")
        add = constr + constr2
        res = add.build(Context({"name":"test"}))
        self.assertEqual(res, "test test")
        
    def test_flag(self):
        
        name = Constructor.text("name")
        text = Constructor.text("SUCCESS!")
        flag = Constructor.flag(name, text)
        
        res = flag.build(Context({"name":True}))
        self.assertEqual(res, "SUCCESS!")
        
        res = flag.build(Context({"name":False}))
        self.assertEqual(res, "")
        
        res = flag.build()
        self.assertEqual(res, "")
        
    def test_alter_noskip(self):
        
        text = Constructor.text("test")
        var = Constructor.variable("name")
        var2 = Constructor.variable("name2")
        var_or_text = Constructor.alter(False, var, var2, text)
        
        res = var_or_text.build()
        self.assertEqual(res, "test")
        
        res = var_or_text.build(Context({"name":"}{}{}{"}))
        self.assertEqual(res, "}{}{}{")
        
        var_or_text = Constructor.alter(False, var, var2)
        self.assertRaises(BuildError, var_or_text.build)
        self.assertEqual("test", var_or_text.build(Context({"name2":"test"})))
        
    def test_alter_skip(self):
        
        var = Constructor.variable("name")
        var2 = Constructor.variable("name2")
        var_or_text = Constructor.alter(True, var, var2)
        self.assertEqual("", var_or_text.build())
        self.assertEqual("test", var_or_text.build(Context({"name2":"test"})))
        
    def test_cycle(self):
        
        ref = (Constructor.variable("var") + Constructor.text("test")).define("refname", "level")
        sep = Constructor.text(";")
        cycle = Constructor.cycle(ref, sep)
        
        level = [
            Context({"var":"test1"}),
            Context({"var":"test2"}),
            Context({"var":"test3"}),
            Context({"var":"test4"}),
            Context({"var":"test5"}),
        ]
        
        res = cycle.build(Context({"level":level}))
        self.assertEqual(res, "test1 test ; test2 test ; test3 test ; test4 test ; test5 test")
        
        level = [
            Context({"var":"test1"}),
            Context(),
        ]

        self.assertRaises(BuildError, cycle.build, Context({"level":level}))

