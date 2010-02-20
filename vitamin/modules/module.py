# -*- coding: utf-8 -*-

class BaseModule():
    """ Класс базового модуля. Определяет основные параметры
    модулей """    
    
    def __init__(self, engine):
        self.log = engine.log
        self.engine = engine
        self.version = None
        self.depends_on = ()
        
    def turnOffLog(self, bool):
        if bool:
            self.log = lambda x:x
        else:
            self.log = self.engine.log
            
    def depends(self, name):
        if name in self.depends_on: return True
            
    def prepare(self):
        pass
