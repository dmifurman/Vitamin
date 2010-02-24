from .exceptions import *
from .lexical import *
from helpers.log import ConsoleLogWriter, Levels
from helpers.vitaparse.exceptions import ParserError, FunctionError, FatalParserError
import sys

__all__ = ["Node",
           "Ignore",
           "State",
           "many",
           "check",
           "maby",
           "future",
           "exact",
           "oneplus",
           "skip",
           "ntype",
           "nvalue",
           "Spec",
           "Token",
           "Tokenizer",
           "FatalParserError"]

class Tuple(tuple):
    pass

class Node():    
    """
    Node - базовый класс парсера. Он выполняет всю работу, 
    связанную с анализом токенов и преобразованием их сочетаний
    в объекты на Python
    
    Одной из важнейших частей любой Node является функция go,
    которя принимает два аргумента - список токенов (tokens)
    и объект состояния (state). Функция go возвращает
    кортеж из объекта и нового состояния.
    
    Объект Node может работать в качестве декоратора,
    декорируя функцию go или другой Node, копируя его функцию
    go.
    
    Над объектами Node определены операции сложения, "или" и
    сдвига вправо. Результатом операций сложения и "или" двух 
    объектов Node является новый объект Node, который последовательно
    выполняет функции go своих родителей, передавая каждой
    следующей фунции go состояние предидущей. Это позволяет
    анализировать цепочки идущих подряд токенов или их групп.       
    """    
    def __init__(self, function, name="default"): 
        self.name = name
        self._assign(function)
        self.reversion = []
        
    def revert(self):
        if self.reversion:
            del self.reversion[-1]
        if self.reversion:
            self._assign(self.reversion.pop())
        
    def _assign(self, function):
        """
        Присвоение функции go объекта function
        """
        assert function, "Null function"
        run = getattr(function, "go", function)
        setattr(self, "go", run)
        
    def define(self, node):
        """
        Определение парсера. Данная операция необходима тогда,
        когда возникает необходимость в циклический зависимости
        парсеров. "Пустые" парсеры определяются комбинатором future(),
        вносятся в определение других парсеров, а затем доопределяются
        любыми элементами, в том числе и теми, в состав которых входят
        они сами. Данный фокус позволяет разбирать сложные рекурсивные
        грамматики.
        """
        assert node
        self._assign(node)
        return self
    
    def define_with_revert(self, node):
        self.reversion.append(node)     
        self.define(node)        
        
    def withGo(self, func):
        self.__go = func
        return self
    
    def withName(self, name):
        self.name = name
        return self
        
    def __rshift__(self, f):
        """
        Сдвиг вправо: Node() >> function
        Данная операция отличается от остальных операций тем, что
        она определена не между двуми объектами Node, а между
        объектом Node и произвольной функцией. Результатом этой
        операции является новый парсер, результат выполнения которого
        (если анализ был успешным), пропустит результат через
        функцию function и вернет результат этой операции.
        Таким образом мы получаем возможность перейти от объектов
        Token к любым объектам языка Python через призму функции
        function, определяющей алгоритм преобразования.
        """
        @Node
        def __go(tokens, state):
            (v, s) = self.go(tokens, state)
            #try:
            assert f
            result = f(v)
            if isinstance(result, Tuple):
                raise Exception("Can not build Tuple obj")
            return (result, s)
            #except Exception as e:
                        
        __go.name = self.name
        return __go
    
    def __or__(self, node):
        """
        Или: Node() | Node()
        Операция "или" создает парсер, посоледовательно проверяющий
        на цепочке токенов распознавание родительских парсеров, и
        возвращает результать первого из сработавших. Если ни один
        из родительских парсеров не в состоянии распознать следующую
        цепочку токенов, генерируется исключение ParserError.
        """
        @Node
        def __go(tokens, state):
            assert node
            assert isinstance(node, Node)
            try:
                return self.go(tokens, state)
            except ParserError:
                return node.go(tokens, state)
        return __go
    
    def join(self, node):
        """
        Join - высокоуровневый комбинатор, создающий парсер,
        который распознает цепочку объектов, разделенных определяемыми
        node объектами.         
        Примером такой последовательности может
        служить список, разделенный запятыми. В этом случае для
        построения парсера такого списка нужно парсер элементов
        списка обернуть вызовом join с парсером запятой.
        """
        
        assert node
        
        @Node
        def __go(tokens, state):
            (t, s) = (many(self + node) + self).go(tokens, state)
            return t, s
        return __go.withName("join")
    
    def __add__(self, p):   
             
        """
        Сложение: Node() + Node()        
        Сложение парсеров создает парсер, распознающий целую
        группу токенов. Результатом выполнения функции go у этого
        парсера является кортеж объектов, элементами которого
        являются распознанные родительскими парсерами объекты.
        """        
        assert p                       
        @Node
        def __go(tokens, state):
            (t1, s1) = self.go(tokens, state)
            (t2, s2) = p.go(tokens, s1)
            return (_combine(t1, t2), s2)            
        return __go
    
    def parse(self, tokens):
        assert tokens
        try: 
            _ = getattr(self, "go")(list(tokens), State())
            if not _[0]:
                raise ParserError(_[1], tokens)
            return _
        except ParserError as e:
            raise FatalParserError(
            "Some problem occured while parsing line {0} near >>'{1}'".format(
                    e.token.line + 1, e.token.value))
    
class Ignore():
    
    def __init__(self, token=None):
        self.value = getattr(token, "value", token) if token else ""
    
class State():
    
    def __init__(self, index=0):
        self.index = index
        
    def move(self, step=1):
        return State(index=self.index + step)
    
def check(function):    
    """
    Комбинатор check возвразает парсер, срабатывающий
    тогда, когда фукнция function(token) вернет True.
    Используется в основном для геренации парсеров первого
    уровня, когда необходимо отобрать единичные токены
    по какому- либо признаку.
    """    
    @Node
    def __go(tokens, state):
        
        try:
            token = tokens[state.index]
        except IndexError:
            raise ParserError(state, tokens)
   
        if function(token):
            return (token, state.move())
        else:
            raise ParserError(state, tokens)
        
    return __go.withName("check")

def many(node):
    """
    Комбинатор many возвращает парсер, обрабатывающий
    от нуля срабатываний переданного парсера node,
    и возвращающий кортеж из результатов этой обработки
    
    many(IntegerParser).parse("1 2 3 4 5")-> (1,2,3,4,5)
    """
    assert node
    @Node
    def __go(tokens, state):
        res = []
        _s = state
        try:
            while True:
                t, _s = node.go(tokens, _s)
                res.append(t)
        except ParserError:
            return (Tuple(res), _s)
        
    return __go.withName("many")

def maby(node):
    assert node
    """
    Комбинатор maby возвращает парсер, обрабатывающий
    ноль или одно срабатывание переданного парсера node,
    и возвращающий либо результат этого срабатывания, 
    либо игнорируемое значение Ignore()
    """    
    return (node | nvalue(Ignore())).withName("maby")

def future():
    """
    (см. Node.define)
    Служит для объявления недоопределенного парсера, который
    будет определен в последствии при помощи define. Необходим
    для построения рекурсивных комбинаций парсеров.
    """
    @Node
    def __go(tokens, state):
        raise NotImplementedError("Please define future somewhere!")
    return __go.withName("go")

def exact(value):
    """
    Надстройка над комбинаторов check. Первоуровневый парсер, 
    полученный в результате операции сравнивает значение токена
    Token.value со значением value, срабатывает только в случае
    полного совпадения.
    
    Внимание! Чувствителен к регистру!
    """   
    return check(lambda t: t.value == value).withName("exact")

def finish():
    @Node
    def __go(tokens, state):
        if state.index == len(tokens):
            return (Ignore(), state)
        else:
            raise ParserError(state, tokens)
    return __go
        
def oneplus(node):
    """
    Высокоуровневый комбинатор. Результатом является парсер,
    эквивалентный Node + many(Node), результатом его выполнения
    является кортеж значений.
    """
    assert node
    @Node
    def __go(tokens, state):
        (t, s) = (node + many(node)).go(tokens, state)
        return t, s
    return __go.withName("onemore")

def skip(node):
    """
    Высокоуровневый комбинатор. Результаты, возвращенные родительским
    парсером node будут проигнорированы при выдаче. Необходим для
    избавления от различных "шумов": запятых, скобок или других
    ненужных символов (в зависимости от обстоятельств), репрезентации
    которых не нужно передавать в функцию- обработчик парсера.
    """
    assert node
    return (node >> (lambda t: Ignore(t))).withName("skip")

#Node creators

def nvalue(value):
    """
    Создает парсер- пустышку, который ничего не делает и в результате
    своей обработки возвращает текущее состояние и значение value,
    переданное при конструкции парсера. Используется для внутренних
    нужд парсера, в частности для реализации комбинатора maby.
    """
    @Node
    def __go(tokens, state):
        return (value, state)
    return __go.withName("value")

def ntype(ttype):
    """
    Надстройка над комбинаторов check. Первоуровневый парсер, 
    полученный в результате операции сравнивает тип токена
    (совпадает с типом спецификации, на основе которой он был построен)
    Token.type со значением ttype, срабатывает только в случае
    полного совпадения.

    К регистру не чувствителен.
    """
    assert ttype
    ttype = ttype.lower() 
    return check(lambda t: t.type == ttype).withName("type")

def _combine(*items):
    assert len(items) < 3
    lst = [x for x in items if not isinstance(x, Ignore)]
    if len(lst) == 1:
        return lst[0]
    if len(lst) == 2:
        l1 = lst[0]
        l2 = lst[1]
        if isinstance(l1, (Tuple)):
            if isinstance(l2, (Tuple)):
                return (l1 , l2)
            else:
                return l1 + (l2,)
        else:
            if isinstance(l2, (Tuple)):
                return (l1,) + l2
            else:
                return (l1 , l2)
    if not lst:
        return Ignore()
    
