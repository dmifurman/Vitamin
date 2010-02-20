from .constructor import Constructor, Context
from abc import ABCMeta, abstractmethod
from functools import reduce
from helpers.vitaparse import skip, ntype, maby, future, many, oneplus, finish
from helpers.vitaparse.lexical import Spec, Tokenizer
from vitamin.config import Parameter, Tweak

#------------------------------------------------------------------------------ 
# sqlite info here http://www.sqlite.org/lang.html
#------------------------------------------------------------------------------ 

#datatypes = dict(
#             
#        INTEGER={
#            ("INT",),
#            ("INTEGER",),
#            ("TINYINT",),
#            ("SMALLINT",),
#            ("EDT"#  ("UNSIGNED BIG INT",),
#            ("INT2",),
#            ("INT8",)
#        },
#        
#        TEXT={
#            ("CHARACTER", 20),
#            ("VARCHAR", 255),
#            ("VARYING CHARACTER", 255),
#            ("NCHAR", 55),
#            ("NATIVE CHARACTER", 70),
#            ("NVARCHAR", 100),
#            ("TEXT",),
#            ("CLOB",) 
#        },
#        
#        REAL={
#            ("REAL",),
#            ("DOUBLE",),
#            ("DOUBLE PRECISION",),
#            ("FLOAT",)
#        },
#        
#        NUMERIC={
#            ("NUMERIC",),
#            ("DECIMAL",),
#            ("BOOLEAN",),
#            ("DATE",),
#            ("DATETIME",)
#        }
#     
#)

class LoaderError(Exception):
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return repr("Can not load '{0}' definition".format(self.name))
    
class IDefLoader(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def load(self, name):
        pass
    
class DictDefLoader(IDefLoader, Tweak("Database")):
    
    def __init__(self):
        self.DEFINITIONS = Parameter()
        self.tweak()
        self.cache = {}
        if not isinstance(self.DEFINITIONS, dict):
            self.DEFINITIONS = self.DEFINITIONS.__dict__
            
    def load(self, name):
        if name in self.cache:
            return self.cache[name]
        elif name in self.DEFINITIONS:
            return self.DEFINITIONS[name]
        else:
            raise LoaderError(name)

def zip(constrs):
    return reduce(lambda x, y: (x + y), constrs)

class Builder():
    
    def __init__(self):
        self.loader = DictDefLoader()
    
    def load(self, name):
        return self.loader.load(name)        

    def create(self, name):
        text = self.load(name)
        return self.parse(self.tokenize(text))
    
    def create_str(self, token):
        assert token
        return Constructor.text(token.value)
    
    def create_var(self, textToken):
        assert textToken
        return Constructor.variable(textToken.get("text"))
    
    def create_ref(self, textToken):
        assert textToken
        return self.create(textToken.get("text")).define("refname", textToken.get("text"))
    
    def create_cycle(self, ref_n_text):
        assert isinstance(ref_n_text, (list, tuple))
        assert len(ref_n_text) < 3
        return Constructor.cycle(ref_n_text[0], ref_n_text[1])
    
    def create_flag(self, lst):
        assert isinstance(lst, (list, tuple))
        return Constructor.flag(lst[0], lst[1])
    
    def create_alter(self, lst):
        assert isinstance(lst, (list, tuple))
        return Constructor.alter(False, *lst)
    
    def create_tryme(self, lst):
        assert isinstance(lst, (list, tuple))        
        return Constructor.alter(True, *lst)
    
    #===========================================================================
    # Парсер
    #===========================================================================
    
    def tokenize(self, text):    
        
        specs = [
            Spec("text", "[a-zA-Z_0-9.(),*=]+"),
            Spec("newline", "\n"),
            Spec("{", "[{]"),
            Spec("}", "[}]"),
            Spec("space", "\s+"),
            Spec(">>", ">>"),
            Spec("[", "[[]"),
            Spec("]", "[]]"),
            Spec("#", "[#]"),
            Spec("|", "[|]"),
            Spec(":", "[:]"),
            Spec("@", "[@]"),
            Spec("?", "[?]")
        ]
        useless = ("newline",
                   "space")
        tokenizer = Tokenizer(specs)
        return [t for t in list(tokenizer(text)) if not t.type in useless]

    def parse(self, tokens):        
        
        #вспомогательные конструкции первого уровня
        obr = skip(ntype("{"))
        cbr = skip(ntype("}"))
        osbr = skip(ntype("["))
        csbr = skip(ntype("]"))
        check = skip(ntype("?"))
        ref = skip(ntype(">>"))
        alt = skip(ntype("|"))
        uns = skip(ntype("#"))
        star = skip(ntype("@"))        
        twospot = skip(ntype(":"))
        #текст
        text = ntype("text") >> self.create_str
        value = (obr + text + cbr) >> self.create_var
        reference = (ref + text) >> self.create_ref      
        cycle = (uns + reference + star + text + uns) >> self.create_cycle
        flag = (obr + text + twospot + (oneplus(text) >> zip) + cbr) >> self.create_flag    
        alternative = future()
        tryme = future()
        ctr_ = oneplus(text | value | reference | alternative | flag | cycle | tryme) >> zip
        ctr = ctr_ + finish()
        alternative.define((osbr + ctr_.join(alt) + csbr) >> self.create_alter)
        tryme.define((check + osbr + ctr_.join(alt) + csbr) >> self.create_tryme)
        return ctr.parse(tokens)[0]
