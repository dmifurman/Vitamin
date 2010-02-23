
#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project

from vitamin.modules.tpl.builtins import methods, modificators
import operator
from functools import partial
from collections import OrderedDict

builtin_methods = {x:getattr(methods, x) for x in dir(methods) if not x.startswith("_")}
builtin_modificators = {x:getattr(modificators, x) for x in dir(modificators) if not x.startswith("_")}

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
            elif var.name in builtin_methods:
                function = builtin_methods[var.name]
            elif var.name in builtin_modificators:
                function = builtin_modificators[var.name]
            else:
                raise Exception("context function failure: " + repr(var.name))
            
            args = list(map(self.get, var.args))
            return partial(function, *args)
        
        else:
            return var

class Aggregator(list):

    def __init__(self):
        self.mod_line = OrderedDict()
        self.temp_container = []

    def push_modificator(self, name, state):
        assert name in builtin_modificators
        if not name in self.mod_line:
            self.mod_line[name] = []         
        self.mod_line[name].append(state)

    def del_modificator(self, name):
        result = "".join(self.temp_container)
        self.temp_container = []
        
        if self.mod_line[name].pop():
            result = builtin_modificators[name](result)
        
        self.append(result)
        
        if not len(self.mod_line[name]):
            del self.mod_line[name]
            
    def append(self, item):
        if self.mod_line:
            self.temp_container.append(item)
        else:
            list.append(self, item)
            
    def join(self):
        return "".join(self)
