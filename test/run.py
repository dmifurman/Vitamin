#! /usr/bin/python3

import os
import sys
import unittest
from functools import reduce

class TestRunner():
    
    """Класс, производящий последовательный запуск
    тестов проекта и выводящий результаты тестирования
    в удобном виде"""

    def __init__(self, *filters):
        self.filters = filters
        self.modules = []
        self.suites = []
        
    def snoop(self):             
        for root, dirs, files in os.walk(".."):
            self.modules += [os.path.join(root, f)
                          .replace("./", "")
                          .replace("/", ".")[:-len(".py")] for f in files
                          if os.path.splitext(f)[1] == ".py" 
                            and f != "__init__.py" 
                            and f != sys.argv[0]
                            and os.path.split(root)[-1].replace("\\", "") == "tests"
                            and (len(list(filter(lambda name: name in f, self.filters))) > 0 if self.filters else True)]

        self.modules = sorted(self.modules)
        print(self.modules)
        
    def load(self):
        loader = unittest.TestLoader()
        for module in self.modules:
            try:
                m = __import__(module[1:] if module.startswith(".") else module, fromlist=[1])
                self.suites.append(loader.loadTestsFromModule(m))
            except Exception as e:
                raise e
            
    def run(self):
        a = reduce(lambda x, y: unittest.TestSuite((x, y)), self.suites)
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        runner.run(a)
        
t = TestRunner()
t.snoop()
t.load()
t.run()
#print(t.modules)     
