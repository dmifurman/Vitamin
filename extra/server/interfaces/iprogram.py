from abc import ABCMeta, abstractmethod

class IProgram(metaclass = ABCMeta):
    
    @abstractmethod
    def go(self, header:"IHeader"):
        pass
    
    @abstractmethod
    def info(self):
        pass
        
    @abstractmethod
    def restart(self):
        pass

