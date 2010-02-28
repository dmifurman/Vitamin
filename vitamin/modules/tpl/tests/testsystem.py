from unittest import TestCase
from vitamin.modules.tpl import Templates
from vitamin.config import Tweak, Parameter

import os

class TestSystem(TestCase, Tweak("Templates")):
    
    def __init__(self, *args, **kwargs):
        
        TestCase.__init__(self, *args, **kwargs)        
        self.TEMPLATE_TESTS_PACKAGE = Parameter()
        self.tweak()        
        self.test_folder = os.path.dirname(
            self.TEMPLATE_TESTS_PACKAGE.__file__)
        self.system = Templates(self.test_folder)
        
    def test_init(self):        
        template = self.system.load("test1")
        print(template.info())
        
    def test_extend(self):
        template = self.system.load("test_extend_child")
        print(template.render())
        
