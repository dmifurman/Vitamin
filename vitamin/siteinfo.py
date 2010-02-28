import inspect
import os

class SiteInfo():
    
    """
    Класс, содержащий информацию о сайте, основанном
    на фреймворке Vitamin. Данный класс является прототипом,
    его заполненная копия помещается в корень vitamin- сайта
    в файл __info__.py и не модифицируется пользователем
    или разработчиками сайта.
    """

    __name = {0}
    __description = {1}
    __version = {2}
    __authors = {3}
    __vitamin_version = {4}

    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    @property
    def version(self):
        return self.__version
    
    @property
    def authors(self):
        return self.__authors
    
    @property
    def vitamin(self):
        return self.__vitamin_version
    
def create_info(name, description, version, authors, vitamin_version):
    
    """
    Создает исходный текст класса SiteInfo с заполненной информацией о
    сайте для последующей записи в файл __info__.py
    """
    
    text = inspect.getsource(SiteInfo)
    return text.format(*(map(lambda x: "\"\"\"" + x + "\"\"\"",
        (name, description, version, authors, vitamin_version))))

def write_to(text, path):
    
    """
    Записывает исходный текст класса SiteInfo (text) в файл __info__.py,
    расположенный по указанному пути (path)
    """
    
    if os.path.exists(path):
        respath = os.path.join(path, "__info__.py")
        with open(respath, "wt") as f:
            f.write(text)
    else:
        raise IOError("path not exists")
    
def read_info():
    
    """
    Импортирует модуль __info__ из текущей области видимости
    и возвращает объект SiteInfo
    """
