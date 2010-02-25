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

"""
Модуль для грамматического разбора текста и поска в нем т.н. токенов - 
логических элементов. Все токены определяются заголовками, имеющими
строго определенный правилами синтаксис.
"""

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

class String(str): pass

class TemplateAnalyzer():
    
    """
    Основной лексический анализатор шаблонной системы.
    Выполняет все операции по анализу текста шаблона и создания
    структуры Chunk'ов на основе этого текста. Анализ исходных
    текстов шаблона происходит при помощи комбинаторных парсеров,
    описанных в модуле vitaparse. 
    
    См. док.
    """
    
    #спецификации для токенизатора
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
    
    #анализ только данных блоков текста
    delimeters = [
        BlockSpec(LONG, LONG_OPEN, LONG_CLOSE, specs),
        BlockSpec(SHORT, SHORT_OPEN, SHORT_CLOSE, specs)]
    
    #игнорируемые символы
    #TODO: добавить перевод строки??
    unused = ("space")
    
    def tokenize(self, text):
        
        """
        Токенизация исходного кода шаблона при помощи указанных
        выше спецификаций. При спецификации используется блочный токенизатор - 
        специальный токенизатор, обрабатывающий токены только внутри указанных
        блоков, все остальное считая токеном типа EXTERNAL.
        """
        
        tokenizer = BlockTokenizer(self.delimeters, EXTERNAL)
        return [x for x in tokenizer(text) if not x.type in self.unused]
    
    def parse(self, tokens):
        
        #=======================================================================
        # helpers
        #=======================================================================
        
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
        
        text = ntype(EXTERNAL) >> (lambda t: TextChunk(t.value))
        
        #=======================================================================
        # reserved words
        #=======================================================================
        rfor = exact("for")
        rif = exact("if")
        relse = skip(exact("else"))
        rin = skip(exact("in"))
        rblock = (exact("block"))
        rextend = skip(exact("extend"))
        rmethod = skip(exact("method"))
        rstrict = exact("strict") >> (lambda t: t.value)
        rimplicit = exact("implicit") >> (lambda t: t.value)
        
        #=======================================================================
        # small items
        #=======================================================================
        word = ntype("word") >> (lambda t: ContextVar(t.value))
        integer = ntype("integer") >> (lambda t: int(t.value))
        binopt = ntype("binary") >> (lambda t: select_opt(t.value))
        string = ntype("string") >> (lambda t: String(t.value[1:-1]))
        number = integer
        twospot = skip(exact(":"))
      
        #=======================================================================
        # границы блоков
        #=======================================================================
        
        short_op = skip(exact(SHORT_OPEN))
        short_cl = skip(exact(SHORT_CLOSE))
        
        long_op = skip(exact(LONG_OPEN))
        long_cl = skip(exact(LONG_CLOSE))
        
        stuff = future()
        
        #=======================================================================
        # chain chunk
        #=======================================================================
        
        short_meat = future()        
        short_block = short_op + short_meat + short_cl
        
        #=======================================================================
        # function
        #=======================================================================
        function = future()
        function.define((word + 
            skip(exact("(")) + 
            maby((number | string | word | function).join(skip(exact(",")))) + 
            skip(exact(")"))) >> self.__function)      
                       
        #=======================================================================
        # chain chunk  
        #=======================================================================
        arrow = skip(exact(">"))
        short_meat.define((word + many(arrow + function)) >> self.__chain)
                
        #=======================================================================
        # if chunk
        #=======================================================================
        endif = future()
        ifchunk = (long_op + (rif >> create_end(endif)) + 
            (((number | word) + maby(binopt + (number | word))) >> self.__if_head) + 
            long_cl + 
            ((stuff + maby(long_op + relse + long_cl + stuff)) >> self.__if_body) + 
            endif) >> self.__if

        #=======================================================================
        # for chunk
        #=======================================================================
        endfor = future()
        forchunk = (long_op + (rfor >> create_end(endfor)) + 
            ((word.join(skip(exact(","))) + rin + (function | word)) >> self.__for_head) + 
            long_cl + 
            (stuff >> list) + 
            endfor) >> self.__for
        
        #=======================================================================
        # block chunk
        #=======================================================================
        endblock = future()
        block_chunk = (long_op + 
            (rblock >> create_end(endblock)) + twospot + word + long_cl + 
            (stuff >> list) + endblock) >> self.__block
              
        #=======================================================================
        # mod chunk
        #=======================================================================
        endmod = future()
        mod_chunk = (long_op + 
            (word >> create_end(endmod, ignore=False)) + 
            ((exact("+") >> (lambda _: True)) | (exact("-") >> (lambda _: False))) + 
            long_cl + (stuff >> list) + (endmod >> revert(endmod))) >> self.__mod
                 
        #=======================================================================
        # comment
        #=======================================================================
        comment = skip(long_op + exact("#") + string + long_cl)
        
        #=======================================================================
        # extend chunk
        #=======================================================================
        extend = (long_op + skip(exact("#")) + rextend + twospot + word + 
            maby(rmethod + twospot + (rstrict | rimplicit)) + long_cl) >> self.__extend
        
        #=======================================================================
        # разный стафф
        #=======================================================================
        stuff.define(many(
            text | short_block | ifchunk | 
            forchunk | block_chunk | mod_chunk | 
            comment | extend))           
        
        return [x for x in (stuff + finish()).parse(tokens)[0] if not isinstance(x, Ignore)]
    
    def load(self, text):
        return self.parse(self.tokenize(text))
    
    #===========================================================================
    # дальше идут обработчики, которые непосредственно помогают в анализе токенов
    # ниче интересного ;-)
    #===========================================================================

    #===========================================================================
    # chain
    #===========================================================================
    
    def __function(self, value):
        if isinstance(value, tuple):
            name, *args = value
            args = args[0]
        else:
            name = value
            args = []
        return ContextFunction(name, *args)
    
    def __chain(self, values):
        value, *functions = values
        return ChainChunk(value, functions)
    
    #===========================================================================
    # if chunk processor
    #===========================================================================
    class __if_head():        
        def __init__(self, values):
            self.left = values[0]
            if len(values) == 2:
                self.operator = values[1][0]
                self.right = values[1][1]
            else:
                self.right = None
                self.operator = None
            
    class __if_body():
        def __init__(self, values):
            self.true_children = values[0]
            if len(values) == 2:
                self.false_children = values[1]
            else:
                self.false_children = []
    
    def __if(self, values):
        head = values[0]
        assert isinstance(head, self.__if_head)
        body = values[1]
        assert isinstance(body, self.__if_body)
        return QualChunk(head, body)
    
    #===========================================================================
    # for chunk processor
    #===========================================================================
    
    def __for(self, values):
        head = values[0]
        assert isinstance(head, self.__for_head)
        children = values[1]
        assert isinstance(children, list)
        return LoopChunk(head, children)
    
    class __for_head():
        def __init__(self, values):
            self.values = values[0]
            self.iterator = values[1]
            
    #===========================================================================
    # other chunk processor
    #===========================================================================
            
    def __block(self, values):
        return BlockChunk(values[0], values[1])
    
    def __mod(self, values):
        name, state = values[0]
        if len(values) == 2:
            children = values[1]
        else:
            children = None
        return ModChunk(name, state, children)
    
    def __extend(self, values):
        method = "strict"
        if isinstance(values, str):
            name = values
        else:
            name = values[0]
            if len(values) == 2:
                method = values[1]
        return ExtendChunk(name, method)
        
