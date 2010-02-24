
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
    
    """
    Контекст - объект связывания переменных в шаблоне
    с переменными окружения. Каждая сессия отрисовки шаблона
    имеет свой контекст со своим набором переменных, изменяющихся
    в зависимости от ситуации. Контекст также позвляет шаблону
    получить доступ к определенным заранее модификаторам и методам
    обработки информации, которые расположены в модуле builtins.
    """
        
    def get(self, var):

        if isinstance(var, ContextVar):   
            #разруливание переменных любой глубины var1.var2.var3... 
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
            #разруливание вызова функций с аргументами из шаблона
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
            #неразруливаемые типы(int, String, и проч.) просто возвращаются
            return var

class Aggregator(list):

    def __init__(self):
        self.mod_line = OrderedDict()
        self.aggregation = []

    def push_modificator(self, name, state):
        
        """
        Добавляет новое состояние модификатора в аггрегатор.
        Модификатор имеет состояние вкл/выкл(bool), и начинает
        применяться ко всем дальнейшим добавляемым строкам.
        
        Перед изменением состояния модификатора вызывает
        flush_mods().
        """
        
        assert name in builtin_modificators
        self.flush_mods()
        if not name in self.mod_line:
            self.mod_line[name] = []         
        self.mod_line[name].append(state)
        
    def del_modificator(self, name):
        
        """
        Удаляет состояние модификатора из аггрегатора. Если
        удаляемое состояние - последнее из состояний модификатора,
        модификатор удаляется из аггрегатора.
        
        Перед изменением состояния модификатора вызывает
        flush_mods().
        """
        
        self.flush_mods()
        if self.mod_line[name]:
            del self.mod_line[name][-1]
        if not self.mod_line[name]:   
            del self.mod_line[name]
        
    def slice(self):
        
        """
        Возвращает словарь - срез текущих состояних модификаторов,
        подставляя каждому активному модификатору только одно (последнее)
        состояние. Таким образом мы получаем возможность включать -
        отключать модификаторы в шаблоне по мере необходимости.
        """
        
        return OrderedDict(((x, self.mod_line[x][-1]) for x in self.mod_line))
            
    def append(self, item):
        
        """
        Операция добавления текста в аггрегатор.
        """

        if self.mod_line:
            self.aggregation.append(item)
        else:       
            list.append(self, item)
    
    def flush_mods(self):
        
        """
        Операция применения модификаторов в состоянии текущего
        среза на накопленный буфер и сброс буфера. Применяется 
        при изменении состояния какого- либо модификатора.
        """
        
        slice = self.slice()
        result = "".join(self.aggregation)
        for name, active in slice.items():
            if active:
                result = builtin_modificators[name](result)
        list.append(self, result)
        self.aggregation = []

    def join(self):
        
        """
        Свертка аггрегатора в результирующую строку
        """
        return "".join(self)
