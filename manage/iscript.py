from abc import ABCMeta, abstractmethod
from optparse import OptionParser

class IScript(metaclass=ABCMeta):
    
    options = OptionParser()
    
    @classmethod
    @abstractmethod    
    def run(cls):
        pass
    
