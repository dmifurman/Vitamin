from .exceptions import NoSpecError
import re

class Spec():
    
    """
    Класс спецификации токена лексического анализатора.
    Используя указанную спецификацию анализатор выделяет в
    тексте специальные объекты - токены и создает список
    классов Token для дальшейшего анализа парсером.
    
    Объект Spec инициализирутся следующими параметрами:
    
        type - любая уникальная строка, идентифицирующая
        токен. Используется для идентификации токенов и
        вывода отладочных сообщений
        
        regexp - паттерн для компиляции регулярного выражения,
        с помощью которого будет идентифицирован токен.
        
        flags - список констант модуля re, влияющих на поведение
        анализатора.
        
        >>Spec("name", "[a-zA-Z_]+")   
    """    
     
    def __init__(self, type, regexp, flags=[]):
        self.type = type
        self.flags = flags
        self.regexp = re.compile(regexp, *flags)
        
class BlockSpec(Spec): 
    """ 
    Класс спецификации тегов, определяющих текст
    для последующего анализа. Наследуется от Spec.
    type, flags тоже что и в Spec.
    regexp - паттерн для компиляции регулярного выражения,
    с помощью которого будет определяться группа для последующего анализа.
    lenT - длина тега        
    """
    def __init__(self, type, open_pattern, close_pattern, inner_specs=[], compile_flags=re.M + re.S):
        self.pattern_len = len(open_pattern)
        assert self.pattern_len == len(close_pattern)
        self.type = type
        self.flags = compile_flags
        self.inner_specs = inner_specs
        self.regexp = re.compile(re.escape(open_pattern) + 
                                 ".*?" + 
                                 re.escape(close_pattern), flags=compile_flags)
    
class Token():
    
    """
    Токен - лексическая единица для грамматического разбора.
    Список экземпляров класса Token создается на этапе лексического
    разбора текста, каждый экземпляр имеет ряд параметров:
    
        type - тип токена, идентичен типу спецификации, на основе
        которой токен был создан
        
        value - часть разбираемого текста, которая соответствует
        спецификации токена
        
        pos - позиция токена в тексте, является кортежем (tuple),
        первым элементом которого является позиция начала value
        в текте, вторым - позиция конца
        
        line - номер строки, в котором находится value. Используется
        для вывода отладочной информации
        
    Над токенами определена регистрозависимая операция сравнения как
    с другими токенами определяющая равенства value- значений экземпляров 
    класса Token, так и с произвольной строкой. 
    
    Нет необходимости в ручном создании экземпляров класса Token. Эту 
    работу за нас сделает лексический анализатор.
    """
    
    def __init__(self, type, value, pos, line):
        self.type = type
        self.value = value
        self.pos = pos
        self.line = line
        
    def __cmp__(self, token):
        _val = getattr(token, "value", token)
        if self.value == _val:
            return True
        else:
            return False
        
    def __str__(self):
        return "{0} token: '{1}'".format(self.type, self.value)
    
    def __repr__(self):
        return self.__str__()
    
def create_token(string, type, start, end=None):
    """
    Функция возвращает объект типа Token, созданный на основе части текста,
    не удовлетворяющей ни одной из спецификаций в sepSpecs.
    В качетсве значения токена выступает срез исходного текста: str[start:end]        
    """
    if(start != end) and not start == len(string):
        return Token(type,
                    string[start:end],
                    (start, end),
                    line=string[:start].count("\n"))
    
def recognize(specs, string, i):
    """
    Функция recognize берет на себя всю работу по непосредственно
    анализу текста. Вызывается каждый раз, с аргументами:
        
        string - строка, в которой ищутся токены по спецификациям
        из specs
        
        i - позиция, с который необходимо начинать поиск при данном
        вызове.
        
    Функция последовательно проверяет при помощи регулярных выражений
    (данная версия анализатора использует функцию re.match) совпадение 
    текста, следующего после указанного индекса со спецификациями
    токенов из списка specs возвращает экземпляр класса Token при 
    нахождении первого совпадения.
    
    Если все спецификации проверены, а совпадение так и не было найдено,
    то функция сгенерирует исключение NoSpecError.
    """        
    for spec in specs:
        match = spec.regexp.match(string, i)            
        if match:
            return create_token(string,
                                spec.type.lower(),
                                match.start(),
                                match.end())          
    raise NoSpecError(string[:i].count("\n"), string[i:i + 10])

def BlockTokenizer(block_specs, external_type):
            
    def tokenizer(string):
        
        tokens = []
        zones = []
        for block in block_specs:
            zones += ((block, x) for x in block.regexp.finditer(string))

        zones = sorted(zones, key=lambda x: x[1].start())

        def smart_append(string, type, start, end=None):
            nonlocal tokens
            obj = create_token(string, type, start, end)
            if obj:
                tokens.append(obj)
                
        if not zones:
            smart_append(string, external_type, 0)
            return tokens
        
        #добавляем external до первого найденного блока
        smart_append(string, external_type, 0, zones[0][1].start())
        
        def routine(block, match):
            nonlocal tokens
            #добавляем _open токен
            smart_append(string, block.type + "_open", match.start(), match.start() + block.pattern_len)
            
            #распознаем токены внутри блока
            tokenizer = Tokenizer(block.inner_specs)
            tokens += tokenizer(string[match.start() + block.pattern_len:match.end() - block.pattern_len])
            
            #добавляем _close токен
            smart_append(string, block.type + "_close", match.end() - block.pattern_len, match.end())    
        
        for i, (block, match) in list(enumerate(zones))[:-1]:                        
            routine(block, match)                        
            next_block, next_match = zones[i + 1]
            #добавляем external от конца текущего блока до следующего         
            smart_append(string, external_type, match.end(), next_match.start())
        
        last_block, last_match = zones[-1]
        routine(last_block, last_match)
        #добавляем external от последнего блока и до конца      
        smart_append(string, external_type, last_match.end())
        return tokens
            
    return tokenizer
            
   

def Tokenizer(specs):    
    
    """
    Функция - фабрика для создания лексического анализатора на
    основе переданного в качестве аргумента списка спецификаций
    токенов. Созданный лексический анализатор можно вызвать,
    передав ему анализируемый текст в качесве аргумента.
    """   
  
    def tokenizer(str):  
        """            
        При вызове лексический анализатор вернет генератор finder,
        который при вызове next() будет возвращать следующий токен
        в тексте. Однако для работы парсера необходимо наличие в памяти
        полного списка токенов, что подразумевает явное использование
        обертки из list() при вызове лексического анализатора.
        """      
        def finder():
            i = 0
            while i < len(str):
                t = recognize(specs, str, i)
                if not t: raise StopIteration()
                yield t
                i = t.pos[1]
        return finder()    
    return tokenizer
