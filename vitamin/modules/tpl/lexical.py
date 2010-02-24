from helpers.vitaparse.lexical import BlockSpec, Spec, BlockTokenizer
from helpers.vitaparse import exact, ntype, future, skip, maby, many, finish, \
    Ignore
from vitamin.modules.tpl.chunks import ChainChunk, QualChunk, LoopChunk, \
    BlockChunk, TextChunk, ModChunk, ExtendChunk
from vitamin.modules.tpl.context import ContextVar, ContextFunction
from functools import partial

#$Rev: 122 $     
#$Author: fnight $  
#$Date: 2009-08-28 16:12:56 +0400 (Пт, 28 авг 2009) $ 

#This file is part of Vitamin Project

"""Модуль для грамматического разбора текста и поска в нем т.н. токенов - 
логических элементов. Все токены определяются заголовками, имеющими
строго определенный правилами синтаксис. Сами правила (экземпляры класса
Rule) можно добавлять в анализатор для расширения функциональности 
системы шаблонов. Так- же можно изменить существующий набор правил.

ВНИМАНИЕ! Если вы решите изменить существующий наблор правил, обратите внимание, 
что системе обязательно наличие правла для токена с типом "end" для определения
закрывающего токена для токенов, требующих закрытия. Если вы решите удалить 
данное правило, то вам придется полностью отказаться и от правил, описывающих
токены, которые нужно закрывать. Помните об этом.

Правила изменяются в конструкторе класса Snoop. Для осуществления разбора
класс определяет функцию analyse, однако нет необходимости напрямую создавать
и использовать класс Snoop. Функция analyse поставляется на уровне модуля
и желательно использовать именно её."""


LONG = "long"
SHORT = "short"
DECLARATION = "declaration"
EXTERNAL = "text"

SHORT_OPEN = "["
SHORT_CLOSE = "]"

LONG_OPEN = "{"
LONG_CLOSE = "}"

import operator as ops
def select_opt(value):
    
    """
    Преобразование операторов из строки в фукнцию
    """
    
    if value == "in":
        return ops.contains
    elif value == ">":
        return ops.gt
    elif value == "<":
        return ops.lt
    elif value == "!=":
        return ops.ne
    elif value == "==":
        return ops.eq     

#строка вида 'str'
class String(str): pass

class TemplateAnalyzer():
    
    specs = [
        Spec("space", "\s+"),
        Spec("comment", "[#]"),
        Spec("end", "[/]\w+"),
        Spec("word", "[a-zA-Z][\w0-9_.]*"),
        Spec("integer", "[0-9]+"),
        Spec("binary", "[<>|=]|in"),
        Spec("special", "[[]]"),
        Spec("brace", "\(|\)"),
        Spec("comma", ","),
        Spec("descr", "[:]"),
        Spec("string", "'.*?'"),
        Spec("plus", "[+-]")]
    
    delimeters = [
        BlockSpec(LONG, LONG_OPEN, LONG_CLOSE, specs),
        BlockSpec(SHORT, SHORT_OPEN, SHORT_CLOSE, specs)]
    
    unused = ("space")
    
    def tokenize(self, text):
        
        tokenizer = BlockTokenizer(self.delimeters, EXTERNAL)
        return [x for x in tokenizer(text) if not x.type in self.unused]
    
    def parse(self, tokens):
        
        text = ntype(EXTERNAL) >> (lambda t: TextChunk(t.value))
        
        #reserved words
        rfor = (exact("for"))
        rif = (exact("if"))
        relse = skip(exact("else"))
        rin = skip(exact("in"))
        rblock = (exact("block"))
        rextend = skip(exact("extend"))
        rmethod = skip(exact("method"))
        rstrict = exact("strict")
        rimplicit = exact("implicit")
        
        word = ntype("word") >> (lambda t: ContextVar(t.value))
        integer = ntype("integer") >> (lambda t: int(t.value))
        binopt = ntype("binary") >> (lambda t: select_opt(t.value))
        string = ntype("string") >> (lambda t: String(t.value[1:-1]))
        number = integer
        twospot = skip(exact(":"))
      
        short_op = skip(exact(SHORT_OPEN))
        short_cl = skip(exact(SHORT_CLOSE))
        
        long_op = skip(exact(LONG_OPEN))
        long_cl = skip(exact(LONG_CLOSE))
        
        short_meat = future()
        
        short_block = short_op + short_meat + short_cl
        stuff = future()
        
        def create_end(node, ignore=True):
            def _foo(token):
                val = getattr(token, "value", token)
                node.define_with_revert(long_op + skip(exact("/" + val)) + long_cl)
                return Ignore() if ignore else token
            return _foo
        
        def revert(node, ignore=True):          
            def _foo(token):
                node.revert()
                return Ignore() if ignore else token            
            return _foo
        
        #chain token
        arrow = skip(exact(">"))
        function = future()
        function.define((word + 
                    skip(exact("(")) + 
                    maby((number | string | word | function).join(skip(exact(",")))) + 
                    skip(exact(")"))) >> self._function) 
        short_meat.define((word + many(arrow + function)) >> self._chain)
                
        #if token
        endif = future()
        ifchunk = (long_op + (rif >> create_end(endif)) + 
                   (((number | word) + maby(binopt + (number | word))) >> self.if_head) + 
                   long_cl + 
                   ((stuff + maby(long_op + relse + long_cl + stuff)) >> self.if_body) + 
                  endif) >> self._if

        endfor = future()
        forchunk = (long_op + (rfor >> create_end(endfor)) + 
                    ((word.join(skip(exact(","))) + rin + (function | word)) >> self.for_head) + 
                    long_cl + 
                    (stuff >> list) + 
                   endfor) >> self._for
        
        endblock = future()
        block_chunk = (long_op + (rblock >> create_end(endblock)) + twospot + word + long_cl + 
                            (stuff >> list) + endblock) >> self._block
                            
        endmod = future()
        mod_chunk = (long_op + 
            (word >> create_end(endmod, ignore=False)) + 
            ((exact("+") >> (lambda _: True)) | (exact("-") >> (lambda _: False))) + 
            long_cl + (stuff >> list) + (endmod >> revert(endmod))) >> self._mod
                            
        comment = skip(long_op + exact("#") + string + long_cl)
        
        extend = (long_op + skip(exact("#")) + rextend + twospot + word + 
         maby(rmethod + twospot + (rstrict | rimplicit)) + long_cl) >> self._extend
        
        stuff.define(many(text | short_block | ifchunk | forchunk | block_chunk | mod_chunk | comment | extend))
        
        return [x for x in (stuff + finish()).parse(tokens)[0] if not isinstance(x, Ignore)]
    
    def load(self, text):
        return self.parse(self.tokenize(text))
    
    #===========================================================================
    # chain
    #===========================================================================
    
    def _function(self, value):
        if isinstance(value, tuple):
            name, *args = value
            args = args[0]
        else:
            name = value
            args = []
        return ContextFunction(name, *args)
    
    def _chain(self, values):
        value, *functions = values
        return ChainChunk(value, functions)
    
    #===========================================================================
    # if chunk processor
    #===========================================================================
    class if_head():        
        def __init__(self, values):
            self.left = values[0]
            if len(values) == 2:
                self.operator = values[1][0]
                self.right = values[1][1]
            else:
                self.right = None
                self.operator = None
            
    class if_body():
        def __init__(self, values):
            self.true_children = values[0]
            if len(values) == 2:
                self.false_children = values[1]
            else:
                self.false_children = []
    
    def _if(self, values):
        head = values[0]
        assert isinstance(head, self.if_head)
        body = values[1]
        assert isinstance(body, self.if_body)
        return QualChunk(head, body)
    
    #===========================================================================
    # for chunk processor
    #===========================================================================
    
    def _for(self, values):
        head = values[0]
        assert isinstance(head, self.for_head)
        children = values[1]
        assert isinstance(children, list)
        return LoopChunk(head, children)
    
    class for_head():
        def __init__(self, values):
            self.values = values[0]
            self.iterator = values[1]
            
    #===========================================================================
    # other chunk processor
    #===========================================================================
            
    def _block(self, values):
        return BlockChunk(values[0], values[1])
    
    def _mod(self, values):
        name, state = values[0]
        if len(values) == 2:
            children = values[1]
        else:
            children = None
        return ModChunk(name, state, children)
    
    def _extend(self, values):
        name = values[0]
        if len(values) == 2:
            method = values[1]
        else:
            method = "strict"
        return ExtendChunk(name, method)
        
