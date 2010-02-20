
#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project


#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project

"""Модуль, содержаший инструмент наследования шаблонов.

Наследование шаблонов происходит на основе директивы {{extend: smth}}
в коде шаблона. Идея наследования подсмотрена в шаблонной системе 
web-framework'a Django. Механизм наследования заключается в следующем:
Шаблон размечается с помощью заголовков {{block: name}}..{{end}}.
Когда базовый блок загружается системой наследования, то в наследующем
шаблоне осуществляется поиск блоков, имена которых совпадают с именами
в базовом блоке. Содержимое таких блоков в базовом шаблоне заменяется 
содержимым блоков наследующего шаблона. Возвращается базовый шаблон с
внесенными изменениями.

ВНИМАНИЕ! Для запуска процедуры наследования необходимо использовать
функцию mutate.

ВНИМАНИЕ! Загрузчики шаблонов автоматически инициируют процедуру наследования.
Нет необходимости самостоятельно запускать наследование вслучае их 
использования"""

try:
    from ..templates import tokens
except ValueError:
    import tokens

class Mutagen:

    def treeToDict(self, tokenList):
        """Разворачивает иерархическую структуру токенов в списке 
        tokenList в словарь блоков. Ключами становлятся имена блоков, 
        а значениями - сами объекты блоков"""
        
        lst = {x.name:x for x in tokenList \
                if type(x) == tokens.BlockToken}
                
        for token in tokenList:
            if token.children:
                lst.update(self.treeToDict(token.children))
        return lst
              
    def mutateBlock(self, baseBlocksDict: dict, block: tokens.BlockToken) -> bool:
        """Заменяет содержимое блока из baseBlocksDict, имя которого совпадает
        с block.name на содержимое блока block
        
        baseBlocksDict - словарь, сгенерированый функцией treeToDict или аналогом
        
        block - экземпляр класса tokens.BlockToken
        
        Функция вернет True, если блоки с одинаковым названием найдены и 
        замена содержимого произведена, или False, если блок с названием 
        block.name не найден в споваре baseBlocksDict"""
        
        try:
            baseBlock = baseBlocksDict[block.name]      
            baseBlock.children = block.children
            return True
        except KeyError:
            return False
      
           
    def mutate(self, loader, template):
        """Основная функция, производящая наследование шаблона.
        Именно её необходимо использовать для инициализации рекурсивного
        механизма наследования. Функция принимает два аргумента:
        
        loader - функция-загрузчик. Вызвав такую функцию с аргументом
        name, полученными из директивы extend, система должна получить
        экземпляр класса Template. Самое очевидное решение- использование
        функций, поставляемых загрузчиками.
        
        template - экземпляр класса Template, который будет унаследован
        от базового шаблона, имя которого определено директивой extend.
        Если директива extend в шаблоне не обнаружена, то функция вернет 
        данный аргумент."""
        #есть ли extend?
        try:
            extendBlock = [token for token in template.tokens 
                                if type(token) == tokens.ExtendToken][0]
        except IndexError:
            return template
        
        baseTemplate = loader(extendBlock.name)
        baseTemplate = self.mutate(loader, baseTemplate)    
        blocksDict = self.treeToDict(baseTemplate.tokens)
        candidates = [token for token in template.tokens 
                if type(token) == tokens.BlockToken and token.name in blocksDict]                
        [self.mutateBlock(blocksDict, x) for x in candidates]
        
        return baseTemplate

mutate = Mutagen().mutate
      
