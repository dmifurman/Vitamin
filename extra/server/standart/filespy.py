from extra.server.interfaces.ispy import ISpy
from time import sleep
import os
import threading
          
class FileSpy(threading.Thread, ISpy):

    """
    Файловый шпион, отслеживающий изменения указанных файлов.
    Работает в отдельном потоке для обеспечения раздельной работы
    сервера и шпиона. Может определять изменения произвольного набора
    файлов. 
    
    Списки файлов делятся на две категории: 
    
        1. Файлы сервера. Основной рабочий модуль самого сервера или
        дополнительные сопроводительные файлы. Изменения этих файлов
        приводят к вызову restartServer().
        
        2. Файлы программы. Программа - объект, обрабатывающий запросы
        клиентов и посылающий им ответы. Изменения этих файлов вызывают
        перезагрузку программы без изменения состояния самого сервера.        
    """
    
    def __init__(self, restartServer,
                        restartProgram,
                        stopCallback,
                        interval):
            
        threading.Thread.__init__(self)

        #коллекции файлов
        self.filesProgram = {}
        self.filesServer = {}
        
        #процедуры обратной связи
        self.restartProgram = restartProgram
        self.restartServer = restartServer
        
        #интервал проверки файлов
        self.interval = interval
        
        #служебный флаг состояния потока
        self._killed = False
        
        #процедура обратной связи, вызываемая просле того, 
        #как был завершен поток
        self.stopCallback = stopCallback
            
    def _rule(self, collection, fList):
        """Добавление пути в коллекцию"""
        collection.update({
             name:os.path.getmtime(name) for name 
             in fList if os.path.exists(name) })

    def addProgramList(self, fList):
        """Добавление нового пути в правила программы"""
        self._rule(self.filesProgram, fList)
                    
    def addServerList(self, fList):
        """Добавление нового пути в правила сервера"""
        self._rule(self.filesServer, fList)
        
    def delProgramList(self, fList):
        """Удаление правила программы"""
        for name in fList: del self.filesProgram[name]
    
    def delServerList(self, fList):
        """Удаление правила сервера"""
        for name in fList: del self.filesServer[name]
        
    def _processCollection(self, collection, function):
    
        """Обработка коллекции путей и точек изменеия
        в цикле. Процедура последовательно проверяет
        наличие изменений в каждом файле, и, в случае
        нахождения расхождения - обновляет точки изменения
        всех файлов и производит перезагрузку"""
        
        _call = False
        for name, time in collection.items():
            mtime = os.path.getmtime(name)
            if mtime > time:              
                _call = True      
                collection[name] = mtime                                     
        if _call:function()                    
        
    def run(self):    
        """Основной рабочий цикл"""        
        while not self._killed:
            sleep(float(self.interval))
            self._processCollection(self.filesProgram, self.restartProgram)
            self._processCollection(self.filesServer, self.restartServer)
        #вызов callback процедуры происходит при выходе из потока
        self.stopCallback()       
                    
    def kill(self):
        """Установка фалага заверешения работы потока"""
        self._killed = True  
