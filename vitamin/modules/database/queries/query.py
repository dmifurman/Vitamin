from types import GeneratorType
from abc import ABCMeta, abstractmethod

class Query(metaclass=ABCMeta):
    
    def __init__(self, model):
        self.model = model
        self.hooks = {}
    
    def __get_builder(self):
        return self._builder        
    def __set_builder(self, builder):
        self._builder = builder
               
    def __get_model(self):
        return self._model    
    def __set_model(self, model):
        self._model = model

    builder = property(__get_builder, __set_builder)
    model = property(__get_model, __set_model)
    
    @abstractmethod
    def sql(self):
        pass

    def go(self):
        query = self.sql()
        if isinstance(query, (list, tuple, set, GeneratorType)):
            for q in query:
                print("executed: ", q)
                self.model.PDO.execute(q)
            return True
        else:    
            print("executed: ", query)            
            return self.model.PDO.execute(query)
    
    @staticmethod
    def chain(function):        
        def new(self, *args, **kwargs):
            function(self, *args, **kwargs)
            return self
        return new
    
