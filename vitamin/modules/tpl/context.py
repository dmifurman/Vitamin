
#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project

from vitamin.modules.tpl.builtins import methods, modificators
import operator
from functools import partial

builtins_methods = {x:getattr(methods, x) for x in dir(methods) if not x.startswith("_")}
builtins_modificators = {x:getattr(modificators, x) for x in dir(modificators) if not x.startswith("_")}

#переменаая, зависящая от контекста
class ContextVar(str): 
    
    def __repr__(self):
        return "ctx.var:" + self.__str__()
        

#функция, зависящая от контекста
class ContextFunction():
    
    def __init__(self, name, *args, **kwargs):
        
        """
        Переменные должны быть только следующих типов:
            int, float, String, ContextVar, ContextFunction
        """
        
        self.name = name
        self.args = args
        self.kwargs = kwargs

class Context(dict):
        
    def get(self, var):
        
        if isinstance(var, ContextVar):   
                     
            if "." in var:
                name, *path = var.split(".")
                getter = operator.attrgetter(path)
                if name in self:
                    getter(self[name])
                else:
                    raise Exception("context var failure: " + repr(name))
            else:
                if var in self:
                    return self[var]
                else:
                    raise Exception("context var failure: " + repr(var))
                
        elif isinstance(var, ContextFunction):
            
            function = None
            if var.name in self and hasattr(self[var.name], "__call__"):
                function = self[var.name]
            elif var.name in builtins_methods:
                function = builtins_methods[var.name]
            else:
                raise Exception("context function failure: " + repr(var.name))
            
            args = list(map(self.get, var.args))
            return partial(function, *args)
        
        else:
            return var

class Aggregator(list):

    def join(self):
        return "".join(self)
    

            

