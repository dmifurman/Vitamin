# -*- coding: utf-8 -*-
from modules.module import BaseModule
import os

class Requests(BaseModule):
    """Класс, хранящий и выполняющий необходимые запросы к базе данных"""
    
    def __init__(self, engine):
        """ Базовая инициализация """
        BaseModule.__init__(self,engine)
        
    depends_on = ("messages","config","database")

        
    def __execute__(func):
        """ Декорирующая функция. Немедленно выполняет запрос,
        сформированный декорируемой функцией """        
        def wrap(self, *args, **kwargs):
            return self.engine.database.execute(func(self,*args, **kwargs))
        return wrap
    
    @__execute__
    def dropDatabase(self,base):
        """Удаляет базу данных base"""
        return "DROP DATABASE %s" % (base,)
    
    @__execute__
    def createDatabase(self,base, soft = False):
        """Создает базу данных base"""
        if not soft:
            return "CREATE DATABASE %s" % (base,)
        else:
            return "CREATE DATABASE IF NOT EXISTS %s;" % (base,)

    
    @__execute__
    def useDatabase(self,base):
        """Указывает SQl использовать базу данных base"""
        return "USE %s" % (base,)
    
    @__execute__
    def dropTables(self,*tables):
        """Сбрасывает таблицы, перечисленные в tables"""
        tables = ','.join([name for name in tables])        
        res = "DROP TABLE IF EXISTS " + tables
        return res
    
    @__execute__
    def insertInto(self, name, *values):
        res = "INSERT INTO %s VALUES %s" %(name,values)
        return res
    
    @__execute__
    def createTableEx(self, table, fields):
        """Создает таблицу table с параметрами,
         указанными в nodes"""
              
        #Создаем строки запроса
        #>>>>>>>>>>>>>>>>>>>>>>
        
        res = ", ".join([x for x in fields])    
        #<<<<<<<<<<<<<<<<<<<<<<          
        return "CREATE TABLE IF NOT EXISTS %s (%s);" % (table,res)
    
    def createTable(self, table):
        """Создает таблицу table на основе информации из модуля tables"""
        
        #импортируем модуль tables
        path = self.engine.config.db_tbl_def_folder
        lst = os.listdir(path)
        names = [os.path.split(os.path.splitext(x)[0])[1] for x in lst if os.path.splitext(x)[1] == ".tbl"]        
        
        if not table in names: 
            raise Exception(self.engine.messages.req_table_not_defined % (table,))            
        
        f = open(path+table+".tbl","r")
        lines = f.readlines()
        lines = [x.split("\n")[0] for x in lines if x.expandtabs(4).strip() != ""]
        lines = [(x.split("#")[0]).expandtabs(4).strip() for x in lines if (x.split("#")[0]).expandtabs(4).strip() != ""]
        f.close()   

        self.createTableEx(table,lines) #создаем таблицу
    
    @__execute__
    def runsaved(self, request, **kwargs):
        path = self.engine.config.db_saved_requests
        
        lst = os.listdir(path)
        names = [os.path.split(os.path.splitext(x)[0])[1] for x in lst if os.path.splitext(x)[1] == ".req"]        
        
        if not request in names: 
            raise Exception(self.engine.messages.req_req_not_defined % (request,))            
        
        f = open(path+request+".req","r")
        lines = f.readlines()
        f.close() 
        
        lines = [x.split("\n")[0] for x in lines if x.expandtabs(4).strip() != ""]
        lines = [(x.split("#")[0]).expandtabs(4).strip() for x in lines if (x.split("#")[0]).expandtabs(4).strip() != ""]
        res = " ".join(lines)
        res = res % kwargs
        return res
        
        
        

        
        
