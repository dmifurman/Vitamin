from vitamin.modules.tpl import Templates

class ModelsCollection():
    pass

class ViewsCollection():
    pass

class LogicCollection():
    pass

class Site():
    
    """
    Модуль, являющийся фасадом нашего сайта, связывает между собой и
    хранит все необходимые для его работы компоненты:
        - модели из каталога /models
        - шаблоны из каталога /templates
        - отображения из каталога /views
        - логику и модули из каталога /logic
    
    Доступ к указанным объектам осуществляется через поля класса,
    названные соответственно models, templates, views, logic
    """
    
    @property
    def Models(self):
        return self.__models
    
    @property
    def Views(self):
        return self.__views
    
    @property
    def Logic(self):
        return self.__logic
    
    @property
    def Templates(self):
        return self.__templates
    
    @property
    def Config(self):
        return self.__config

    def __init__(self):
        
        self.__models = ModelsCollection()
        self.__views = ViewsCollection()
        self.__logic = LogicCollection()
        self.__templates = Templates()
        self.__config = None
    
    
