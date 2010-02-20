from abc import ABCMeta, abstractmethod
from vitamin.modules.database import expression

class Field(object, metaclass=ABCMeta):
    
    Name = None
    
    def __init__(self, database_type, native_type, features):
        
        self.NativeType = native_type
        self.StorageType = database_type          
        
        self.values = {}   
        self.default = None
        self.features = features
        
    def __get__(self, obj, objtype):
        
        if obj == self.Model: return self
        if obj:
            try:
                return self.values[obj]
            except KeyError:
                return self.default
        else:
            return self
    
    def __set__(self, instance, value):
                    
        try:
            value = value if isinstance(value, self.NativeType) else self.NativeType(value)
        except:
            raise ValueError("Can not convert {0} to {1}".format(
            repr(type(value).__name__), repr(self.NativeType.__name__)))
    
        if instance:
            self.values[instance] = value
        else:
            raise NotImplementedError()   

    @abstractmethod
    def StorageToNative(self, value): 
        pass
    
    @abstractmethod
    def NativeToStorage(self, value):
        pass
    
    def __str__(self):
        return ".".join((self.Model.Name, self.Name))
        
    def __and__(self, right):
        return expression.__and__(self, right)
    
    def __or__(self, right):
        return expression.__or__(self, right)
            
    @classmethod
    def expressionBehaviour(cls, enabled=True): 
        
        if enabled: 
                 
            def __eq__(self, right): 
                return expression.__eq__(self, right)
            def __ne__(self, right):
                return expression.__ne__(self, right)
            def __lt__(self, right):
                return expression.__lt__(self, right)
            def __le__(self, right):
                return expression.__le__(self, right)
            def __gt__(self, right):
                return expression.__gt__(self, right)
            def __ge__(self, right):
                return expression.__ge__(self, right)
            
            cls.__eq__ = __eq__
            cls.__ne__ = __ne__
            cls.__lt__ = __lt__
            cls.__le__ = __le__
            cls.__gt__ = __gt__
            cls.__ge__ = __ge__
            
        else:
            
            sp = super(type, cls)
            cls.__eq__ = sp.__eq__
            cls.__ne__ = sp.__ne__
            cls.__lt__ = sp.__lt__
            cls.__le__ = sp.__le__
            cls.__gt__ = sp.__gt__
            cls.__ge__ = sp.__ge__
    
class IntegerField(Field):
    
    def __init__(self, *features):
        Field.__init__(self, "INTEGER", int, features)
    
    def StorageToNative(self, value):        
        if (value == None) or (value == "NULL"): 
            return 0
        return self.NativeType(value)
    
    def NativeToStorage(self, value):
        if value == None:
            return "NULL"
        return str(value)

class CharField(Field):
    
    def __init__(self, *features):
        Field.__init__(self, "CHARACTER", str, features)
        
    def StorageToNative(self, value):        
        if (value == None) or (value == "NULL"): 
            return ""
        return self.NativeType(value)
    
    def NativeToStorage(self, value):
        if not value:
            return "NULL"
        return repr(value)
    
class ForeignField(IntegerField):
        
    def __init__(self, model, *features):
        IntegerField.__init__(self, *features)
        self.ForeignModel = model
              
    def __set__(self, instance, inst):
        if hasattr(inst, "value"):
            IntegerField.__set__(self, instance, inst.value(inst.PrimaryKey()))
        else:
            IntegerField.__set__(self, instance, inst)
            
            
