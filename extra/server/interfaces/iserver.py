
#В этом файле хранятся настройки программы, которая
#будет использоваться нашим сервером для получения запросов
#от клиентов и ответа на эти запросы. Реализацию этих задач
#необходимо вынести за пределы проекта, так как они уже реализованы
#в достаточном количестве библиотек.

from abc import ABCMeta, abstractmethod

class IServer(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, settings:dict):
        #Настройки сервера должны быть переданны серверу в виде объекта,
        #среди полей которого будут, в том числе, ip:string, port:int,
        #и handler:class    
        pass
           
    @abstractmethod
    def run(self):
        pass
    
    @abstractmethod
    def kill(self):
        pass
    
    @abstractmethod
    def setRedirect(self, object): pass
    
    @abstractmethod
    def getRedirect(self): pass
        
class IHandler(metaclass=ABCMeta):
       
    @abstractmethod   
    def getPath(self):
        pass
        
    @abstractmethod   
    def setPath(self, path):
        pass      
    
    @abstractmethod   
    def sendCode(self, code:int):
        pass
    
    @abstractmethod  
    def sendHeader(self, name, value):
        pass
    
    @abstractmethod  
    def closeHeaders(self): pass
    
    @abstractmethod   
    def send(self, buf):
        pass
    
    @abstractmethod    
    def closeSession(self):
        pass
    
        
    
