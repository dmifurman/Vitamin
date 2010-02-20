from abc import ABCMeta, abstractmethod
import sys

class SingletonProperty(metaclass=ABCMeta):   
    
    def __init__(self, value):
        self.value = value
    
    def __get__(self, obj, classobj):        
        return self.value
    
    def __set__(self, obj, value):
        self.value = value
