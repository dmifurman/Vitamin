from unittest import TestCase
from vitamin.modules.tpl import Templates
from vitamin.config import Tweak, Parameter

from vitamin.config import config
import os

class TestSystem(TestCase, Tweak("Templates")):
    
    def __init__(self, *args, **kwargs):
        
        TestCase.__init__(self, *args, **kwargs)        
        self.TEMPLATE_TESTS_PACKAGE = Parameter()
        self.tweak()        
        self.test_folder = os.path.dirname(
            self.TEMPLATE_TESTS_PACKAGE.__file__)
        
    def test_init(self):
        system = Templates(self.test_folder)
        template = system.load("test1")
        print(template.info())
        
