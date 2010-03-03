
class SitesManager():
    
    """
    Инструмент для управления сайтами Vitamin, необходим для
    поддержки нескольких сайтов Vitamin на одном интерпретаторе
    Python. Для организации нормальной работы лучше запускать
    на одном интерпретороне один сайт
    """
    
    @property
    def Sites(self):
        return self.__sites
    
    def __init__(self):
        self.__sites = {}
    
    def LoadSite(self, path):
        pass
    
    def UnloadSite(self, name):
        pass
    
    def ReloadSite(self, name):
        pass
