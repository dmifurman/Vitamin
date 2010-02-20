from abc import ABCMeta, abstractmethod, abstractproperty
from vitamin.config import Tweak, Parameter
from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder import Builder
from vitamin.modules.database.fields import CharField, IntegerField, Field
from collections import OrderedDict
from vitamin.modules.database.queries import QueryCreate, QueryInsert, \
    QuerySelect, QueryUpdate, QueryDelete
from vitamin.modules.database.sqlbuilder.definitions import Names
from vitamin.modules.database.expression import Expression
import sys
import sqlite3

#ip = re.compile("(?P<lim>2(?=[0-9]{2}))?(?(lim)([0-5][0-5])|([1][0-9][0-9]|[1-9]?[0-9]))$")
    
#class IProvider(ABCMeta):
#class ICursor
"""
Тут оговорочка. Не будем мутить воду и изобратать
какие- то интерфейсы для провайдеров баз данных,
т.к. существует обкатанный интерфейс 
DB-API 2.0 interface, и все известные провайдеры
баз данных на Python ориентируются на соответствие
этому интерфейсу.

http://www.python.org/dev/peps/pep-0249/
"""

class PDO(Tweak("Database")):
    
    def __init__(self):
        
        self.PROVIDER = Parameter()
        self.LOCATION = Parameter()
        self.USER = Parameter()
        self.PASSWD = Parameter()
        self.CONNECT_WITH = Parameter() 
        self.tweak()
        self.models = []
        self.builder = Builder()
        self.connection = None        
        self.preload()
        
    def connect(self):
        _args = []
        for arg in self.CONNECT_WITH:
            try:
                _args.append(getattr(self, arg))
            except AttributeError as err:
                raise err
            print(_args)
            self.connection = self.PROVIDER.connect(*_args)
        if self.connection:             
            print("connected")
            
    def regiserModel(self, model):
        model.PDO = self
        self.models.append(model)
        
    def preload(self):
        QueryCreate.builder = self.builder.create(Names.Create.definition)
        QueryInsert.builder = self.builder.create(Names.Insert.definition)
        QuerySelect.builder = self.builder.create(Names.Select.definition)
        QueryUpdate.builder = self.builder.create(Names.Update.definition)
        QueryDelete.builder = self.builder.create(Names.Delete.definition)
        Expression.builder = self.builder.create(Names.Expression.definition)
        
    def gosql(self, function):
        if self.connection:
            return self.connection.execute(function())
        else:
            raise Exception("No connection")
    
    def execute(self, query):
        if self.connection:
            return self.connection.execute(query)
        else:
            raise Exception("No connection")            
