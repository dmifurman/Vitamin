from vitamin.modules.tpl.context import ContextFunction

#$Rev: 122 $     
#$Author: fnight $  
#$Date: 2009-08-28 16:12:56 +0400 (Пт, 28 авг 2009) $ 

#This file is part of Vitamin Project

"""Модуль, содержащий описания классов токенов. 
Токен- логическая единаца шаблонной системы. У токена 
модут быть дочерние токены. Каждый токен имеет собственную
процедуру отрисовки, которая по умолчанию называется
render. Как правило, отрисовывая себя, токен отрисовывает
и дочерние токены, вызывая их процедуру render.
Результат отрисовки токена зависит от т.н. контекста.
Объект Context описан в соответствующем модуле."""

from functools import partial

class Chunk:
    """Основной класс для всех токенов. Определяет
    некоторые нужные функции, а также содержит 
    интерфейсную функцию render."""    

    def __init__(self):
        """Инициализация базовых переменных.
        children - список дочерних токенов
        """
        self.children = []
        self.parent = None

    def renderChildren(self, context, aggregator, children):
        """Отрисовка и объединение результат отрисовки 
        всех дочерних токенов."""
        [x.render(context, aggregator) for x in children]
                  
    def render(self, context, aggregator):
        """Пустышка для определения интерфейса функции 
        render у всех токенов"""
        raise NotImplementedError()
        
    def append(self, Chunk):
        """Интерфейс добавления токенов в список дочерних"""
        self.children.append(Chunk)
        Chunk.parent = self
                      
class TextChunk(Chunk):

    """
    Самый часто- используемый токен шаблонной системы.
    Определяет простую текстовую строку.
    """

    def __init__(self, value: str) -> None:
        """
        Инициализация.
        
        value - строка с текстом
        """
        Chunk.__init__(self)
        self.value = value
        
    def __repr__(self):
        return "<TextChunk value:{0}>".format(self.value)
        
    def render(self, context, aggregator): 
        
        """
        Объект context имеет т.н. модификаторы,
        которые применяются динамически в процессе отрисовки
        только к определенному типу токенов. В данном случае
        к объекту Context идет запрос на обработку текста
        модификаторами, применимыми к TextChunk
        """       
        aggregator.append(self.value)
        
class ValueChunk(Chunk):

    """
    Не является напрямую токеном, его заголовки
    не описаны в синтаксисе шаблонной системы. Однако используется
    в рендеринге цепочек как объект, определяющий переменную,
    значение которой зависит от контекста и будет извлечено из
    текущего объекта Context
    """

    def __init__(self, value):
        Chunk.__init__(self)
        self.value = value
        
    def render(self, context):    
        return str(context.get(self.value))
            
    def __repr__(self):
        return """<ValueChunk value={0} converted={1}>""".format(self.value,
            self.converted)
        
class FunctionChunk(Chunk):

    def __init__(self, function):
        Chunk.__init__(self)
        self.function = function
        
    def render(self, context, arg=None):  
        part = context.get(self.function)
        if arg:
            part = partial(part.func, *((arg,) + part.args))
        return part()
            
    def __repr__(self):
        return """<FunctionChunk>"""

class ChainChunk(Chunk):

    """
    
    Токен цепочки. 
    Очень важный токен шаблонной системы. Только с его помощью можно
    вывести в текст значение переменной. Стандартным образом это делается
    с помощью сигнатуры вида [name], вместо которой будет подставлено
    значение переменной name, определенное в текущем контексте.
    Так- же с помощью данной сигнатуры можно запустить т.н. цепочку обработки.
    Вот применое описание возможностей такой записи:
        [name upper shuffle escape]
    Смысл записи в следующем: из контекста берется значение переменной
    name, передается аргументом в фильтр upper, затем значенеи, которе 
    вернул upper передается в фильтр shuffle, потом та же процедура 
    повторяется с фильтном escape(замена ">" и "<" на соответствующие
    коды для экранирования символов.
    
    Фильтры могут иметь агрументы. Например:
        [now date("dd:mm:yyyy")] выведет дату в соответствующем формате."""   

    def __init__(self, value, functions):
        
        """Инициализация.

        ВНИМАНИЕ! Прежде чем разбираться в реализации ChainChunk
        прочтите описание ValueChunk.

        """
        Chunk.__init__(self)       
        self.value = ValueChunk(value)
        self.children += list(map(FunctionChunk, functions))               
                            
    #@timer("Цепочка отрисована за")
    def render(self, context, aggregator):
        """Процедура отрисовки цепочки.
        После отрисовки всех звеньев на результат применяются
        модификаторы"""
        result = self.value.render(context)
        for function in self.children:
            result = function.render(context, result)      
        aggregator.append(str(result))

class LoopChunk(Chunk):

    """Токен, позволяющий использовать циклы в шаблонах.
    Полный синтаксис заголовка этого токена можно описать так:
        {{for name in smth}}, т.е. визульно синтаксис похож на
    синтаксис цикла в языке Python, но есть одно отличие.
    То, что в Python мы бы записали как "for x in range(100)" 
    тут нужно писать как "for x in 100". Такая замена введена
    вследствие того, что вызывать функции в заголовке токенов
    (всех, кроме chain), запрещено. Сделано это для того,
    чтоб упростить синтаксис заголовка.

    В процедуру инициализации передается три аргумента(строковых):
    value, number и iterator. 
    
    value - имя переменной цикла, 

    number - None или числовое представление строки, в зависимости
    от того, задан ли итератор числом или именем переменной.
    
    iterator - коллекция, значения из которой будет принимать value.
    Принимает значения либо None, либо имя переменной, в зависимости
    от того, оперделен ли number"""

    def __init__(self, head, children) -> None:
        Chunk.__init__(self)
        self.iterator = head.iterator
        self.values = head.values
        self.children = children        
    
    #@timer("Отрисовка цикла за")
    def render(self, context, aggregator):

        """Определяем конечный итератор и отрисовывем дочерние
        токены столько раз, сколько нужно, не забывая обновлять контекст.        
        """ 

        if isinstance(self.iterator, ContextFunction):
            iterator = FunctionChunk(self.iterator).render(context)
        else:
            iterator = context.get(self.iterator)
        
        for values in iterator:
            if len(self.values) == 1:
                context[str(self.values[0])] = values
            elif len(values) == len(self.values):
                for name, value in zip(self.values, values):
                    context[str(name)] = value
            else: raise Exception("to many values to unpack")
            self.renderChildren(context, aggregator, self.children)
              

class QualChunk(Chunk):

    """
    Токен, определяющий возможность условного перехода в коде
    шаблона. Полный синтаксис описывается следующим предложением:
        {{if x [in|>|<|==|>=|<= y]}}, где x и y могут быть как 
    переменными, зависимыми от контекста, так и числами. Y можно 
    опустить по аналогии с условным оператором в Python
    """

    def __init__(self, head, body):   
        
        """
        Инициализация. 
                
        invert - строковая переменная. Принимает значение
            "not" если в загаловок токена помещена частица not.
        
        value_left - первая переменная в выражении        
        value_right - вторая переменная в выражении        
        operator - один из операторов выражения
        """       
            
        Chunk.__init__(self)
        self.invert = False
        self.value_left = head.left
        self.value_right = head.right
        self.operator = head.operator
        self.trueChunks = body.true_children
        self.falseChunks = body.false_children

        #выбор операторов. В качетстве функций
        #используются build-in модуль operators

    def render(self, context, aggregator): 
        
        """
        Процедура отрисовки.
        
        Тут имеется два варианта развития ситуации.
        Вариант первый: задана только первая переменная
        Запись этого варианта может быть такой:
            {{if sessionOpen}}
                Hello [[session.user.name]]
            {{else}}
                Autorization required
            {{end}}
        
        Вариант второй: заданы обе переменные и опрератор.
        В этом случае поведение оператора эквивалентно
        оператору if в Python.
        """
        
        assert self.value_left
                
        ctx_value_left = context.get(self.value_left)
        if not self.value_right:                            
            result = bool(ctx_value_left)
        else:   
            ctx_value_right = context.get(self.value_right)
            result = self.operator(ctx_value_left, ctx_value_right)  
            
        if self.invert: result = not result
        toRender = self.trueChunks if result else self.falseChunks
                
        return self.renderChildren(context, aggregator, toRender)
       
           
class BlockChunk(Chunk):

    """
    Токен отображения блоков текста. 
    Сам по себе блок никак не влияет на поведение 
    содержащихся в нем объектов, т.е. они отрисовываются
    точно таким- же образом, как и без блока. Однако
    на блоках основан механизм наследования, являющийся
    важной функцией шаблонной системы
    """
    
    def __init__(self, name, children):
        Chunk.__init__(self)
        self.name = name
        self.children = children
           
    def render(self, context, aggregator):
        return self.renderChildren(context, aggregator, self.children)

class ModChunk(Chunk):

    """
    Токен модификаторов.
    
    На отображение текста в системе шаблонов
    могут повлиять Модификаторы - процедуры пост-
    обработки сгенерированного токенами текста.
    Все возможные модификаторы описаны в модуле
    modificators. Включение и выключение
    модификаторов происходит через методы аггрегатора
    
    Модификатор имет дигитальное состояние on/off,
    определяющее его применение или не применение 
    на дочерние объекты
    """
    
    def __init__(self, name, state, children):
        Chunk.__init__(self)
        self.name = name
        self.children = children
        self.state = state
           
    def render(self, context, aggregator):
        aggregator.push_modificator(self.name, self.state)
        self.renderChildren(context, aggregator, self.children)
        aggregator.del_modificator(self.name) 
        
class ExtendChunk(Chunk):
    
    """
    Токен, определяющий маршрут системы наследования.
    Имеет единственный аттрибут - имя
    """
    
    def __init__(self, name, method):
        Chunk.__init__(self)
        self.name = name
        self.method = method

    def render(self, context, aggregator):
        return
            
    
    
