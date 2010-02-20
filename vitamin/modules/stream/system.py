import re

class StreamSystem():

    """Система обработки потоков, отвечающая за загрузку
    и сохранение файлов с помощью обработчиков(worker). 
    Обработчик - класс, имеющий функии load(name) и save(),
    с помощью которых происходит загрузка или сохранение 
    данных соответственно"""

    #словарь кортежей
    def __init__(self):
        self.workers = {} 

    def register(self, wtype, wreg):
        """Функция регистрации обработчика в системе. Фукции
        передается аргумент wrk_type, определяющий категорию
        обработчика, и wrk_obj - экземпляр класса обработчика
        Например:
        
            from vitamin.modules.template.loaders.file import File
            self.register("template", File())
            
            -регистрация файлового обработчика шаблонов в системе
            с категорией "template". 
            
            ?? Есть идея в качестве категории
            ?? использовать модуль, загрузка объектов которого производится.  
            
        Регистрация обработчикка происходит под именем его класса в нижнем
        регистре. Таким образом обработчик File() после регистрации будет
        доступен под именем file. Обработчики разрешается перерегистрировать.     
        """
                    
        if not wtype in self.workers: self.workers[wtype] = {}        
        if not hasattr(wreg, "load") or not hasattr(wreg, "save"):
            raise Exception("Worker does not have load or save")                  
        name = wreg.__class__.__name__.lower()
        self.workers[wtype][name] = wreg

     
    def load(self, wtype, wname, wobj):    
        """Загрузка объекта с именем wobj с помощью
        обработчика wname из категории wtype."""
        try:
            return self.workers[wtype][wname](wtype, wname).load(wobj)
        except KeyError:
            raise Exception(
            "No worker found with type '{0}' and name: '{1}'".format(
            wtype, wname))              
          
    def save(self, wtype, wname, wobject, obj):
        """Сохранение объекта obj с идентификатором wobj
        с помощью обработчика wname из категории wtype."""     
        self.workers[wtype][wname](wtype, wname).save(wobject, obj)        

streamSystem = StreamSystem()
