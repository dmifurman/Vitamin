from collections import UserList, UserDict
from functools import reduce
from inspect import isclass

print = lambda _: None

class BuildError(Exception):
    
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)

class Context(UserDict):
    
    """
    Контекст - многоуровневая структура данных, содержащая
    необходимые для построения запросов значения. Значения,
    хранящиеся в контексте различиются типами: 
        
        Переменная - значением переменной является строка.
        Каждой переменной сопоставлено имя. Доступ к
        переменной осуществляется посредством прямого
        доступа к объекту Context:
            var = Context["name"]
            
        Флаг - переменная, значением которой являются
        True или False
        
        Уровень - объект ContextLevel, который используется
        для генерации спецификаций- циклов. Каждая итерация
        цикла сопоставляется со своим элементом Context.
        ContextLevel поддерживает паттерн Iterator
    """
    
    def __init__(self, initial={}, namespace=None):
        self._init = False
        UserDict.__init__(self, initial)
        if namespace and isclass(namespace):
            self.names = {x:getattr(namespace, x)for x in dir(namespace) if not x.startswith("_")}
            self.variables = {x:self.names[x] for x in self.names if x.startswith("var")}
            self.flags = {x:self.names[x] for x in self.names if x.startswith("flag")}
            if("levelName" in self.names):
                self.levelName = self.names["levelName"]
            else: 
                self.levelName = None
            self._init = True
        
        
    def __getattribute__(self, name):
        sup = super(Context, self).__getattribute__
        try:
            return sup(name)
        except Exception:
            try:
                return sup("data")[sup("names")[name]]
            except Exception as e:
                raise e
            
    def __setattr__(self, name, value):
        sup = super(Context, self).__setattr__
        if hasattr(self, "_init") and self._init:
            if name in self.variables:
                if not isinstance(value, str):
                    raise ValueError()
                self[self.variables[name]] = value
            elif name in self.flags:
                self[self.flags[name]] = value
            else:
                raise ValueError()
        else:
            sup(name, value)
            
    def level(self, context):
        assert context.levelName
        if not context.levelName in self:
            self[context.levelName] = []
        self[context.levelName].append(context)       
        
    def copy(self):
        return dict(self.data)
    
    def value(self, name):
        return self[name]
    
def _join(x, y):
    if x.endswith(".")  or y.startswith("."):
        return "".join([x, y])
    else: 
        return " ".join([x, y])        

class Constructor():
    
    def __init__(self, obj):
        self._assign(obj)
        self.props = {}
        
    def _assign(self, obj):
        self.go = getattr(obj, "go", obj)
        
    def define(self, name, value):
        self.props[name] = value
        return self
    
    def defined(self, _dict):
        self.props = _dict
        return self
    
    def get(self, name):
        if name in self.props:
            return self.props[name]
        else:
            return None
        
    def __add__(self, obj):
        
        @Constructor
        def __go(reg, context):
            reg = self.go(reg, context)
            reg = obj.go(reg, context)
            return reg

        return __go.defined(self.props)
    
    def __or__(self, constr):
        return Constructor.alter(self, False, constr)
        
    def build(self, context={}):
        return reduce(_join, self.go([], context) or [""])
    
    @classmethod
    def text(cls, value):
        @Constructor
        def __go(reg, context):
            try:
                print("Text constructor processed: '{0}'".format(value))
                return reg + [value, ]
            except Exception as e:
                raise BuildError(str(e))
        #print("Text constructor created: '{0}'".format(value))
        return __go.define("text", value)
    
    @classmethod
    def variable(cls, name):
        @Constructor
        def __go(reg, context):
            if name in context:
                print("Variable processed: '{0}' -> '{1}'".format(name, context[name]))
                return Constructor.text(context[name]).go(reg, context)
            else:
                print("Variable processed error: '{0}'".format(name))
                raise BuildError("No '{0}' value in context".format(name))
        return __go.define("varname", name)
    
    @classmethod
    def flag(self, nameTextConstr, textConstr):
        name = nameTextConstr.get("text")
        @Constructor
        def __go(reg, context):
            if name in context and context[name]:
                print("Flag processed: '{0}'".format(name))
                return textConstr.go(reg, context)
            else: 
                print("Flag not processed: '{0}'".format(name))
                return reg
        return __go.define("flagname", name)
    
    @classmethod
    def alter(cls, skip, *constructors):
        
        @Constructor
        def __go(reg, context):
            print(constructors)
            for constr in constructors:
                try:
                    return constr.go(reg, context)
                except BuildError:
                    pass
            
            if not skip:
                exp = ["""None of alternative constructors can be create"""]
                for i, obj in enumerate(constructors):
                    exp.append(" {0}: {1} \n ".format(i, obj.props))     
                
                raise BuildError(reduce(lambda x, y: x + y, exp))
            else:
                return reg
                   
        return __go
    
    @classmethod
    def cycle(cls, refConstructor, textSep):
        name = refConstructor.get("refname")
        @Constructor
        def __go(reg, context):
            if name in context and isinstance(context[name], list):
                level = context[name]
                max = len(level) - 1
                for index, cnt in enumerate(level):
                    print("Switched to {0} level in ContextLevel: {1}".format(index, name))
                    print("Defined values: {0}".format(list(cnt.keys())))
                    try:
                        reg = refConstructor.go(reg, cnt)
                    except BuildError as b:
                        print("Switched outside of ContextLevel: {0}".format(name))
                        raise b
                    if index < max: reg = textSep.go(reg, cnt)

                return reg
            else:
                print("Cycle process error: '{0}' {1}".format(name, "not exists" if not name in context else "not a ContextLevel"))
                raise BuildError("Please make {0} a ContextLevel".format(name))   
        return __go
