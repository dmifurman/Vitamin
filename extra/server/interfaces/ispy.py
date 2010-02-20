from abc import ABCMeta, abstractmethod

class ISpy(metaclass=ABCMeta):
        
    @abstractmethod
    def __init__(self, restartServer,
                        restartProgram,
                        stopCallback,
                        interval): pass
                        
    @abstractmethod              
    def addServerList(self, list): pass
    
    @abstractmethod
    def addProgramList(self, list): pass
    
    @abstractmethod
    def delProgramList(self, list): pass
    
    @abstractmethod
    def delServerList(self, list): pass
    
    @abstractmethod                    
    def start(self): pass
    
    @abstractmethod                    
    def run(self): pass
    
    @abstractmethod
    def kill(self): pass
