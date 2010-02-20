    
class Rule():
    
    """Правило обаботки URL. Администратор сервера
    задает правила в виде словаря, содержащего обобщения
    URL, в виде ключей, и пользовательские функции обработки
    в виде значений.    
    """
    
    __slots__ = ["regexp", "block"]
    
    def __init__(self, block, regexp):
        self.block = block
        self.regexp = regexp

    def check(self, url):
        matchobj = self.regexp.match(url)        
        if matchobj:        
            _arguments = matchobj.groupdict()      
            return (True, _arguments)
        else:
            return (False, None)
