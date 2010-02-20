"""
server

Модуль содержит реализацию основной функциональности сервера приложений.
Инициализация класса Server приводит к запуску низкоуровневого сервера
обработки сетевых запросов по протоколу TCP/IP и демона слежения за 
состоянием файлов сервера и приложеня. Сервер приложений берет настройки
из модуля конфигурации config.config, в котором должны быть описаны
необходимые для работы параметры. 
"""

from extra.server.config import messages, Tweak, Parameter
import os
import sys

class Server(Tweak("Server")):   

    def __init__(self):        
        
        self.PROGRAM = Parameter()        
        self.AUTORESTART = Parameter()
        self.SERVER_REALIZATION = Parameter()
        self.SERVER_SETTINGS = Parameter()
        self.SPY_REALIZATION = Parameter()
        self.SPY_INTERVAL = Parameter(5)
        self.FILES_SERVER = Parameter([])
        self.FILES_PROGRAM = Parameter([])
        self.PYTHON_BIN = Parameter(sys.executable)
         
        self.tweak()
        
        #инициализируем программу
        self.PROGRAM = self.PROGRAM()
        
        messages.log.init
        messages.log.program_init       
        
        self.server = self.createServer()
        self.server.setRedirect(self.PROGRAM)
        
        if self.AUTORESTART:  
            self.enableRestart()
            self.spy = self.startSpy()            
            self.spy.addServerList(self.FILES_SERVER)
            self.spy.addServerList(self.FILES_PROGRAM)            
            messages.log.monitor
        else: 
            self.enableRestart(False)        
               
    def enableRestart(self, value=True):
        self.restart = value        
   
    def restartProgram(self):
        """Перезагрузка программы сервера.
        changed_file - имя изменившегося файла, вызвавшего перезагрузку"""
        messages.log.restart_program
        self.program.restart()        
    
    def createServer(self):
        return self.SERVER_REALIZATION(self.SERVER_SETTINGS)
    
    def kill(self):   
        self.server.kill()
        if self.AUTORESTART: 
            self.spy.kill()
        else: sys.exit()
        
    def run(self):
        messages.log.started
        messages.log.toexit
        
        self.server.run()
    
    def threadsStopped(self):
        """Callback- функция. Вызывается после остановки
        всех потоков. Производит очищение буферов записи
        стандартных потоков ввода-вывода и перезапускает
        текущий скрипт"""
        if self.restart:
            print("restarting ->>")
            os.execl(self.PYTHON_BIN, "", sys.argv[0])
                  
    def startSpy(self):
        """Запуск файлового шпиона, отслеживающего изменения
        даты модификации указанных файлов и вызывающего процедуры
        перезагрузки программы или сервера, в зависимости от того,
        какие файлы были изменены"""        
        spy = self.SPY_REALIZATION(self.restartServer,
                  self.restartProgram,
                  self.threadsStopped,
                  self.SPY_INTERVAL)
        spy.start()
        return spy   

    def restartServer(self):
        """Перезапуск сервера."""
        messages.log.restart_server
        messages.log.sep
        self.kill() 
        
