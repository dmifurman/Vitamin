from abc import ABCMeta, abstractmethod

class Levels():
    
    INFO = 0
    WARNING = 1
    ERROR = 2
    
    @classmethod
    def t(cls, level):
        if level == 0:
            return Levels.INFO
        elif level == 1:
            return Levels.WARNING
        else:
            return Levels.ERROR

class ILogWriter(metaclass=ABCMeta):

    def __init__(self, level): pass
    
    @abstractmethod
    def line(self, type, message): pass
    
class ConsoleLogWriter(ILogWriter):
    
    def __init__(self, level):
        self.velel = level
    
    def line(self, type, message, *args, **kwargs):
        if type >= self.velel:
            print("{0}: {1}".format(Levels.t(type),
                                    message.format(*args, **kwargs)))
    
    
    
    
