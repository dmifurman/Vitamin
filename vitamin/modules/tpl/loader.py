from abc import ABCMeta, abstractmethod


class ITemplateLoader(metaclass=ABCMeta):
    
    """
    Интерфейс загрузчика шаблонов. Любой загрузчик должен
    предоставлять следующие методы:
    
        .load(name) - получить Template, производя поиск по имени
        
        .loadText(text) - получить Template, анализируя исходный
        текст шаблона
        
        .__init__(load_from) - метод инициализации должен поддерживать
        возможность модификации источника, из которого будут загружаться
        шаблоны. Формат источника свой у каждой конкретной реализации
        загрузчика
    """
    
    def __init__(self, load_from=None):
        pass
    
    @abstractmethod
    def load(self, name):
        pass

    @abstractmethod
    def loadText(self, text):
        pass
